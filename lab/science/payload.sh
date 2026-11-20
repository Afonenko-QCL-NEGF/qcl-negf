#!/bin/sh
set -eu
export JULIA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p result
exec julia --startup-file=no --project=runner runner/scripts/scientific_workflow.jl run-plan plan.json result
