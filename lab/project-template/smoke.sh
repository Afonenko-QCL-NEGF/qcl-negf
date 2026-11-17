#!/bin/bash
set -euo pipefail
seconds=${QCL_SECONDS:-10}
case "$seconds" in ''|*[!0-9]*) printf '%s\n' 'QCL_SECONDS must be an integer from 0 to 120' >&2; exit 2;; esac
if ((${#seconds} > 3)); then printf '%s\n' 'QCL_SECONDS exceeds smoke bound 120' >&2; exit 2; fi
if ((10#$seconds > 120)); then printf '%s\n' 'QCL_SECONDS exceeds smoke bound 120' >&2; exit 2; fi
printf 'host=%s\nuser=%s\ncpus=%s\n' "$(hostname)" "$(id -un)" "${OMP_NUM_THREADS:-unset}" > result.txt
cat input.txt >> result.txt
sleep "$seconds"
printf 'completed=yes\n' >> result.txt
