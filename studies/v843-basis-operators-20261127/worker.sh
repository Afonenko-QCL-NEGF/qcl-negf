#!/usr/bin/env bash
set -euo pipefail
umask 077
task=$1
cpus=$2
budget=$3
shift 3
printf 'task = "%s"\nstatus = "technical_error"\nerror_type = "worker_setup"\n' "$task" > summary.toml
mkdir source
tar -xzf source.tar.gz -C source
export QCL_SLOT_CPUS="$cpus" QCL_BUDGET_GIB="$budget" QCL_PARENT_RESULTS="$PWD"
export QCL_RESULT="$PWD/summary.toml" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
threads=$cpus
case "$task" in B7|B9|B11) threads=1;; esac
exec julia --startup-file=no --compiled-modules=existing --threads="$threads,0" --gcthreads=1,0 \
    --project=source/runner source/studies/v843-basis-operators-20261127/worker.jl "$task" "$@"
