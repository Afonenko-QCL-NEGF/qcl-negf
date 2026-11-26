#!/usr/bin/env bash
# Prepare a new persistent submit directory from one Git tree. No scheduler calls.
set -eu
if [ "$#" -ne 1 ]; then
    echo 'Usage: stage.sh NEW_RUN_DIRECTORY' >&2
    exit 2
fi
here=$(cd -- "$(dirname -- "$0")" && pwd)
root=$(git -C "$here" rev-parse --show-toplevel)
revision=$(git -C "$root" rev-parse HEAD)
run=$1
mkdir -- "$run"
study=studies/cluster-eight-20261126
device=studies/fath-v843/controls/v843-input/dupont
mkdir -- "$run/logs" "$run/results"
for file in cluster.dag native.sub collect.sub collect_v843.py run-native.sh; do
    git -C "$root" show "$revision:$study/$file" > "$run/$file"
done
chmod +x "$run/run-native.sh"
git -C "$root" archive --format=tar.gz -o "$(cd -- "$run" && pwd)/v843-src.tar.gz" "$revision" -- \
    runner/Project.toml runner/Manifest.toml runner/src runner/ext \
    "$study/v843_native.jl" "$device/device.toml" "$device/dupont_device.jl"
echo "$revision" > "$run/revision"
(cd -- "$run" && sha256sum v843-src.tar.gz > inputs.sha256)
