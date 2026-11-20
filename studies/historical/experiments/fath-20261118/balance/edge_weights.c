// Read only diagonal planes from an aligned Fath terminal HDF5 file.
#include <hdf5.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

enum { ENERGY = 4801, MOMENTUM = 25, MODES = 7 };
enum { ALL, LO_LOW, LO_HIGH, FIELD_LOW, FIELD_HIGH, CHAIN_LOW, CHAIN_HIGH,
       CHAIN_LO_LOW, CHAIN_LO_HIGH, TRUST_LOW, TRUST_HIGH, OUTER_LAST_K,
       OUTER_THREE_K, REGIONS };
static const char *region_names[] = {
    "all", "lo_low", "lo_high", "field_low", "field_high", "chain_low",
    "chain_high", "chain_plus_lo_low", "chain_plus_lo_high", "outside_trust_low",
    "outside_trust_high", "largest_k_bin", "three_largest_k_bins"
};

static void require(bool ok, const char *message) {
    if (!ok) {
        fprintf(stderr, "%s\n", message);
        exit(1);
    }
}

static void read_vector(hid_t file, const char *path, hid_t kind, hsize_t length, void *value) {
    hid_t dataset = H5Dopen2(file, path, H5P_DEFAULT);
    require(dataset >= 0, path);
    hid_t space = H5Dget_space(dataset);
    hsize_t dims[1];
    require(H5Sget_simple_extent_ndims(space) == 1 &&
            H5Sget_simple_extent_dims(space, dims, NULL) == 1 && dims[0] == length, path);
    require(H5Dread(dataset, kind, H5S_ALL, H5S_ALL, H5P_DEFAULT, value) >= 0, path);
    H5Sclose(space);
    H5Dclose(dataset);
}

static void read_trace(hid_t file, const char *path, double *trace, double sign) {
    hid_t dataset = H5Dopen2(file, path, H5P_DEFAULT);
    require(dataset >= 0, path);
    hid_t space = H5Dget_space(dataset);
    hsize_t dims[4];
    require(H5Sget_simple_extent_ndims(space) == 4 &&
            H5Sget_simple_extent_dims(space, dims, NULL) == 4 &&
            dims[0] == MODES && dims[1] == MODES &&
            dims[2] == MOMENTUM && dims[3] == ENERGY, path);
    const hsize_t count[] = {1, 1, MOMENTUM, ENERGY};
    const hsize_t dest_dims[] = {MOMENTUM, ENERGY};
    hid_t dest = H5Screate_simple(2, dest_dims, NULL);
    double *plane = malloc(MOMENTUM * ENERGY * sizeof(*plane));
    require(dest >= 0 && plane != NULL, "could not allocate diagonal plane");
    for (hsize_t a = 0; a < MODES; a++) {
        const hsize_t start[] = {a, a, 0, 0};
        require(H5Sselect_hyperslab(space, H5S_SELECT_SET, start, NULL, count, NULL) >= 0, path);
        require(H5Dread(dataset, H5T_NATIVE_DOUBLE, dest, space, H5P_DEFAULT, plane) >= 0, path);
        for (size_t j = 0; j < MOMENTUM * ENERGY; j++) {
            require(isfinite(plane[j]), "nonfinite trace component");
            trace[j] += sign * plane[j];
        }
    }
    free(plane);
    H5Sclose(dest);
    H5Sclose(space);
    H5Dclose(dataset);
}

static bool in_band(double distance, double shift) {
    // Exactly in-range shifted endpoint nodes retain support.
    return distance < shift - 1e-9;
}

int main(int argc, char **argv) {
    require(argc == 3, "usage: edge_weights MODEL.h5 STATE.h5");
    hid_t model = H5Fopen(argv[1], H5F_ACC_RDONLY, H5P_DEFAULT);
    hid_t state = H5Fopen(argv[2], H5F_ACC_RDONLY, H5P_DEFAULT);
    require(model >= 0 && state >= 0, "could not open model/state");
    double energy[ENERGY], w_energy[ENERGY], k[MOMENTUM], w_k[MOMENTUM];
    unsigned char trust[ENERGY];
    read_vector(model, "/energy_dimensionless", H5T_NATIVE_DOUBLE, ENERGY, energy);
    read_vector(model, "/weight_energy", H5T_NATIVE_DOUBLE, ENERGY, w_energy);
    read_vector(model, "/k_dimensionless", H5T_NATIVE_DOUBLE, MOMENTUM, k);
    read_vector(model, "/weight_k", H5T_NATIVE_DOUBLE, MOMENTUM, w_k);
    read_vector(model, "/trusted_energy", H5T_NATIVE_UCHAR, ENERGY, trust);
    require(fabs(energy[0] + 4) < 1e-12 && fabs(energy[ENERGY - 1] - 5.6) < 1e-12 &&
            fabs(k[0]) < 1e-12 && fabs(k[MOMENTUM - 1] - 6) < 1e-12, "unexpected physical axes");

    double *trace[3];
    const char *path[] = {"/green/A_real", "/green/GL_imag", "/green/GG_imag"};
    const double sign[] = {1.0, 1.0, -1.0};
    for (int tag = 0; tag < 3; tag++) {
        trace[tag] = calloc(MOMENTUM * ENERGY, sizeof(double));
        require(trace[tag] != NULL, "could not allocate trace plane");
        read_trace(state, path[tag], trace[tag], sign[tag]);
    }
    require(H5Fclose(state) >= 0 && H5Fclose(model) >= 0, "failed to close files");

    long double weight[REGIONS][3] = {{0}};
    unsigned count[REGIONS] = {0};
    double e_min[REGIONS], e_max[REGIONS], k_min[REGIONS], k_max[REGIONS];
    for (int i = 0; i < REGIONS; i++) {
        e_min[i] = k_min[i] = INFINITY;
        e_max[i] = k_max[i] = -INFINITY;
    }
    const double e_unit_mev = 100.0, k_unit_per_nm = 0.1;
    const double field = 54.0, lo = 36.7, chain = 4 * field;
    for (size_t m = 0; m < MOMENTUM; m++) {
        require(w_k[m] > 0 && isfinite(w_k[m]), "invalid k weights");
        for (size_t q = 0; q < ENERGY; q++) {
            require(w_energy[q] > 0 && isfinite(w_energy[q]), "invalid energy weights");
            const double e = e_unit_mev * energy[q], momentum = k_unit_per_nm * k[m];
            const double low = e - e_unit_mev * energy[0], high = e_unit_mev * energy[ENERGY-1] - e;
            const bool region[] = {
                true, in_band(low, lo), in_band(high, lo), in_band(low, field),
                in_band(high, field), in_band(low, chain), in_band(high, chain),
                in_band(low, chain + lo), in_band(high, chain + lo),
                !trust[q] && q < ENERGY / 2, !trust[q] && q >= ENERGY / 2,
                m + 1 == MOMENTUM, m + 3 >= MOMENTUM
            };
            for (int j = 0; j < REGIONS; j++) {
                if (!region[j]) continue;
                count[j]++;
                e_min[j] = fmin(e_min[j], e);
                e_max[j] = fmax(e_max[j], e);
                k_min[j] = fmin(k_min[j], momentum);
                k_max[j] = fmax(k_max[j], momentum);
                for (int t = 0; t < 3; t++) {
                    weight[j][t] += (long double)w_energy[q] * w_k[m] * trace[t][m * ENERGY + q];
                }
            }
        }
    }
    const long double spin = 2.0L, l0_cm = 1e-6L;
    const long double scale = spin / (2 * acosl(-1.0L) * l0_cm * l0_cm);
    require(weight[ALL][0] > 0 && weight[ALL][1] > 0 && weight[ALL][2] > 0, "invalid integrated traces");
    puts("region,blocks,E_min_meV,E_max_meV,k_min_nm_inverse,k_max_nm_inverse,A_capacity_cm-2,occupied_cm-2,hole_capacity_cm-2,A_fraction,occupied_fraction,hole_fraction");
    for (int j = 0; j < REGIONS; j++) {
        printf("%s,%u,%.10g,%.10g,%.10g,%.10g,%.12Lg,%.12Lg,%.12Lg,%.12Lg,%.12Lg,%.12Lg\n",
                region_names[j], count[j], e_min[j], e_max[j], k_min[j], k_max[j],
                scale * weight[j][0], scale * weight[j][1], scale * weight[j][2],
                weight[j][0] / weight[ALL][0], weight[j][1] / weight[ALL][1], weight[j][2] / weight[ALL][2]);
    }
    for (int t = 0; t < 3; t++) free(trace[t]);
    return 0;
}
