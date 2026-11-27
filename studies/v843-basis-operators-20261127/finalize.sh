#!/usr/bin/env bash
set -euo pipefail
umask 077
run=$PWD
publication="$run/publication"
python3 collect.py "$run" "$publication"
