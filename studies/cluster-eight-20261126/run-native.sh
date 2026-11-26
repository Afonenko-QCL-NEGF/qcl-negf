#!/usr/bin/env bash
set -eu
field=$1
rings=$2
angles=$3
maps=$4
workers=$5
budget_gib=$6
# Remains transferable even if Julia is unavailable or the worker cannot unpack the input.
cat > summary.toml <<FAILURE
status = "failed"
error = "Worker setup did not finish. Inspect the node stderr."
field_kV_cm = $field
radial_nodes = $rings
angular_nodes = $angles
FAILURE
mkdir source
tar -xzf v843-src.tar.gz -C source
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
status=0
julia --startup-file=no --compiled-modules=existing --project=source/runner --threads="$workers,0" \
    source/studies/cluster-eight-20261126/v843_native.jl "$field" "$rings" output \
    "$maps" "$budget_gib" "$angles" || status=$?
if test -s output/summary.toml; then
    cp output/summary.toml summary.toml
fi
exit "$status"
