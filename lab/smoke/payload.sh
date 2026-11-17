#!/bin/sh
# Инженерная проба общей очереди, не научный расчёт.
set -eu
seconds=${1:-${QCL_SMOKE_SECONDS:-120}}
case "$seconds" in
  ''|*[!0-9]*|0[0-9]*) printf '%s\n' 'Ожидалось целое число секунд.' >&2; exit 2 ;;
esac
if [ "${#seconds}" -gt 4 ] || [ "$seconds" -gt 3600 ]; then
  printf '%s\n' 'Длительность ограничена 3600 секундами.' >&2
  exit 2
fi
host=$(hostname)
user=$(id -un)
started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf 'host=%s user=%s started=%s duration=%s\n' "$host" "$user" "$started" "$seconds"
printf '%s\n' 'QCL smoke: stderr доступен.' >&2
elapsed=0
: > smoke-heartbeat.txt
while [ "$elapsed" -lt "$seconds" ]; do
  stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf '%s elapsed=%s host=%s\n' "$stamp" "$elapsed" "$host" | tee -a smoke-heartbeat.txt
  step=5
  if [ "$((seconds - elapsed))" -lt "$step" ]; then step=$((seconds - elapsed)); fi
  sleep "$step"
  elapsed=$((elapsed + step))
done
finished=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 - "$host" "$user" "$started" "$finished" "$seconds" <<'PY'
import json, sys
host, user, started, finished, seconds = sys.argv[1:]
with open('smoke-output.json', 'w', encoding='utf-8') as stream:
    json.dump(dict(hostname=host, user=user, started_utc=started,
                   finished_utc=finished, duration_seconds=int(seconds)), stream)
    stream.write('\n')
PY
printf 'completed=%s host=%s\n' "$finished" "$host"
