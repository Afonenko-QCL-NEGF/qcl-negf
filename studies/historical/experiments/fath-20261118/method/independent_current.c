/* Read only. Independent compensated-scale current integration from archived arrays. */
#include <hdf5.h>
#include <complex.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

enum { ENERGY_CHUNK = 256 };
typedef double complex C;

static void fail(const char *message) {
    fprintf(stderr, "%s\n", message);
    exit(2);
}

static void read_axis(hid_t file, const char *key, double *values, hsize_t count) {
    hid_t d = H5Dopen2(file, key, H5P_DEFAULT);
    if (d < 0) fail(key);
    hid_t space = H5Dget_space(d);
    if (H5Sget_simple_extent_ndims(space) != 1 ||
        H5Sget_simple_extent_npoints(space) != (hssize_t)count ||
        H5Dread(d, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL, H5P_DEFAULT, values) < 0)
        fail(key);
    H5Sclose(space);
    H5Dclose(d);
}

static void read_chunk(hid_t file, const char *key, C *output, double *buffer,
                       const hsize_t expected[4], hsize_t offset, hsize_t ne) {
    const hsize_t start[] = {0, 0, 0, offset};
    hsize_t count[] = {expected[0], expected[1], expected[2], ne};
    hsize_t size = count[0]*count[1]*count[2]*count[3];
    hid_t memory = H5Screate_simple(1, &size, NULL);
    for (int component = 0; component < 2; ++component) {
        char name[256];
        snprintf(name, sizeof name, "%s_%s", key, component == 0 ? "real" : "imag");
        hid_t dataset = H5Dopen2(file, name, H5P_DEFAULT);
        if (dataset < 0) fail(name);
        hid_t space = H5Dget_space(dataset);
        hsize_t found[4];
        if (H5Sget_simple_extent_ndims(space) != 4 ||
            H5Sget_simple_extent_dims(space, found, NULL) < 0) fail(name);
        for (int dimension = 0; dimension < 4; ++dimension)
            if (found[dimension] != expected[dimension]) fail(name);
        if (H5Sselect_hyperslab(space, H5S_SELECT_SET, start, NULL, count, NULL) < 0 ||
            H5Dread(dataset, H5T_NATIVE_DOUBLE, memory, space, H5P_DEFAULT, buffer) < 0)
            fail(name);
        for (hsize_t i = 0; i < size; ++i) {
            if (!isfinite(buffer[i])) fail(name);
            if (component == 0) output[i] = CMPLX(buffer[i], 0);
            else output[i] = CMPLX(creal(output[i]), buffer[i]);
        }
        H5Sclose(space);
        H5Dclose(dataset);
    }
    H5Sclose(memory);
}

static size_t index_hdf(size_t a, size_t b, size_t k, size_t e,
                        size_t nb, size_t nk, size_t ne) {
    return (((b*nb + a)*nk + k)*ne + e);
}

int main(int argc, char **argv) {
    if (argc != 6) fail("Specify model.h5, field state.h5, spin degeneracy, E0 in eV and L0 in m");
    hid_t model = H5Fopen(argv[1], H5F_ACC_RDONLY, H5P_DEFAULT);
    hid_t state = H5Fopen(argv[2], H5F_ACC_RDONLY, H5P_DEFAULT);
    if (model < 0 || state < 0) fail("Input archive unreadable");
    int spin = atoi(argv[3]);
    long double energy_eV = strtold(argv[4], NULL), length_m = strtold(argv[5], NULL);
    if (spin < 1 || energy_eV <= 0 || length_m <= 0) fail("Invalid scales");
    hsize_t shape[4];
    hid_t lesser = H5Dopen2(state, "/green/GL_real", H5P_DEFAULT);
    if (lesser < 0) fail("Missing GL");
    hid_t space = H5Dget_space(lesser);
    if (H5Sget_simple_extent_ndims(space) != 4 ||
        H5Sget_simple_extent_dims(space, shape, NULL) < 0 ||
        shape[0] != shape[1] || shape[1] > 16 || shape[2] > 128 || shape[3] > 50000)
        fail("Unexpected GL dataset dimensions");
    H5Sclose(space);
    H5Dclose(lesser);
    hsize_t nb = shape[0], nk = shape[2], ne = shape[3];
    size_t field = nb*nb*nk*ENERGY_CHUNK;
    C *values = malloc(6*field*sizeof(*values));
    double *buffer = malloc(field*sizeof(*buffer));
    double *wk = malloc(nk*sizeof(*wk)), *we = malloc(ne*sizeof(*we));
    if (!values || !buffer || !wk || !we) fail("Allocation failed");
    read_axis(model, "/weight_k", wk, nk);
    read_axis(model, "/weight_energy", we, ne);
    int fath_layout = H5Lexists(state, "/selfenergy/embedding_plus/L_real", H5P_DEFAULT)>0;
    const char *fields[6] = {"/green/GL", "/green/GG",
        fath_layout ? "/selfenergy/embedding_plus/L" : "/selfenergy/embedding_plus/lesser",
        fath_layout ? "/selfenergy/embedding_plus/G" : "/selfenergy/embedding_plus/greater",
        fath_layout ? "/selfenergy/embedding_minus/L" : "/selfenergy/embedding_minus/lesser",
        fath_layout ? "/selfenergy/embedding_minus/G" : "/selfenergy/embedding_minus/greater"};
    long double real_flux[2] = {0}, imag_flux[2] = {0}, flux_abs[2] = {0}, number = 0;
    for (hsize_t offset = 0; offset < ne; offset += ENERGY_CHUNK) {
        hsize_t chunk = ne-offset < ENERGY_CHUNK ? ne-offset : ENERGY_CHUNK;
        for (int i = 0; i < 6; ++i)
            read_chunk(state, fields[i], values+i*field, buffer, shape, offset, chunk);
        for (hsize_t e = 0; e < chunk; ++e) for (hsize_t k = 0; k < nk; ++k) {
            long double weight = (long double)we[offset+e]*wk[k];
            long double real_trace[2] = {0}, imag_trace[2] = {0};
            for (hsize_t row = 0; row < nb; ++row) for (hsize_t col = 0; col < nb; ++col) {
                size_t ab = index_hdf(row,col,k,e,nb,nk,chunk);
                size_t ba = index_hdf(col,row,k,e,nb,nk,chunk);
                long double complex lesser_G = values[ba];
                long double complex greater_G = values[field+ba];
                for (int side = 0; side < 2; ++side) {
                    size_t greater_offset = (3+2*side)*field;
                    size_t lesser_offset = greater_offset-field;
                    long double complex term = (long double complex)values[greater_offset+ab]*lesser_G -
                                               (long double complex)values[lesser_offset+ab]*greater_G;
                    real_trace[side] += creall(term);
                    imag_trace[side] += cimagl(term);
                }
                if (row == col) number += weight*cimagl(lesser_G);
            }
            for (int side = 0; side < 2; ++side) {
                real_flux[side] += weight*real_trace[side];
                imag_flux[side] += weight*imag_trace[side];
                flux_abs[side] += weight*hypotl(real_trace[side],imag_trace[side]);
            }
        }
    }
    /* CODATA exact e, h in SI. E0 stored here in eV, so e converts it into joules. */
    const long double e_si = 1.602176634e-19L, h_si = 6.62607015e-34L;
    const long double hbar_e171 = 1.054571817e-34L;
    long double two_pi = 2*acosl(-1.L);
    long double factor = spin/two_pi*1e-4L*e_si*e_si*energy_eV/length_m/length_m;
    printf("{\"blocks\":%llu,\"J_A_cm2\":%.17Lg,\"J_A_cm2_exact_SI_h\":%.17Lg,"
           "\"J_minus_A_cm2\":%.17Lg,\"normalized_charge\":%.17Lg,"
           "\"relative_imag_flux\":%.17Lg,\"relative_imag_flux_minus\":%.17Lg,"
           "\"relative_flux_cancellation\":%.17Lg}\n",
           (unsigned long long)(ne*nk), real_flux[0]*factor/hbar_e171, real_flux[0]*factor/(h_si/two_pi),
           real_flux[1]*factor/hbar_e171, number*spin/two_pi,
           fabsl(imag_flux[0])/fmaxl(flux_abs[0],1e-300L),
           fabsl(imag_flux[1])/fmaxl(flux_abs[1],1e-300L),
           fabsl(real_flux[0])/fmaxl(flux_abs[0],1e-300L));
    free(we);free(wk);free(buffer);free(values);
    H5Fclose(state);
    H5Fclose(model);
}
