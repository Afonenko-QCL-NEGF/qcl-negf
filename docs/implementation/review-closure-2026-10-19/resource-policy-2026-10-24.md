# Принятая ресурсная поправка initial/production S1

**ADOPTED, 2026-10-24.** Source authority — прямое поручение пользователя:
«Значительно упростить механизмы контроля ресурсов. Мне уже наконец нужно запустить
физику. А вместо этого решаются какие-то незначительные и мелочное проблемы».
Это принятое изменение ресурсной политики [P1](operator-permissions.md),
а не новый scientific model, grant или требование очередного design approval.
Исходный Root до docs-поправки: `0071a9850641b0370aa741149f76a2f88525f1ba`.

## Действующий ресурсный контракт

Для initial и production S1 снимается обязательность custom HDF5 VFD, controller
NBD, общего per-effect allocator, exhaustive source-program/emitter/alias proof и
теоремы всех native allocations. Их незавершённость не блокирует B0. Используется
обычный HDF5 с поддерживаемым ABI и существующий Runner `:standalone` под явно
привязанными внешними Slurm/systemd/cgroup v2 controls. Прежний `campaign_strict`
не объявляется accepted; source/trust checks и разумные numerical/storage
preflights обычного пути сохраняются. Эта политика разрешает такой operational
mode, но не доказывает, что текущий source/native путь уже исправен или READY.

До запуска нужны fresh host/VM/allocation facts, protected host/foreign reserves,
консервативный memory/headroom estimate и inventory всех retained/pending/final/
temp/retrieval/export copies, logs и filesystem overhead. RAM/CPU/tasks/time
ограничиваются actual Slurm/cgroup/systemd controls с readback; disk/logs — конечными
allocation/quota и reserves. Storage preflight, checkpoint и early-stop margin
сохраняются. Нет требования доказать fit каждого будущего native effect или
выполнить guard перед каждым growth/phase/allocation. Неизвестная capacity или
отсутствие нужного ограничения по-прежнему блокируют зависимый запуск.

Числа [таблицы P1](operator-permissions.md) сохраняются: resident W1 128 GiB,
остальные 256 GiB, shared 2 TiB; logs 1 GiB/attempt, 13 GiB/shared — **space budgets**.
Writes/reads W1 2/4 TiB, W2/W3/R/H 4/8 TiB, shared 44/88 TiB — **monitored planning/
early-stop budgets**, допускающие зафиксированный технический overshoot.
Quota не cumulative writes bound. Применяются доступные I/O rate caps; telemetry
фиксирует scope/units/cadence/coverage/reset/gaps, пороги и stop requests через
существующие jobs/receipts. Missing counter = unknown+gap, никогда not_measured=pass;
не нужно доказать полное покрытие всех native/NFS aliases до SCI. Точная атомарная
cumulative per-byte граница HDF5/PostgreSQL/AiiDA/native/NFS/retrieval не обещается.

`io.max` допускает краткие bursts; device `io.stat` не полный logical/NFS счётчик.
`memory.max` — backstop с возможным кратким overshoot/OOM. OOM/ENOSPC/timeout —
failed technical attempt, не штатный durable STOP и не scientific PASS. Shutdown
не гарантирует допубликацию pending generation; сохраняется последняя verified.

## Сохранённые gates и свидетельства

Без изменений: все пять scattering channels, e–e none, 0 mV/70 K, frozen model/
grid/basis/windows, strict scientific criteria; full final/failed raw/arrays и
provenance/hashes; две verified recovery generations, cadence1800 s, существующий
atomic/fsync publish. 13 attempts/936 node-h/72 h на attempt, concurrency≤2,
max_attempts=1; fresh admission и BUILD/OPS technical BIND к exact source,
foreign protection/rollback, genuine AiiDA first submit, scientific sourcegraph
и исправления. Sole final CI 0/1 на final ready ref без auto-reruns; light GUI,
Linux x86 worker bundle; public release требует отдельного решения.

Приёмка рабочего пути: ordinary HDF5 ABI/roundtrip с independent readback/hashes;
recovery/failure/cancel mid-write без публикации partial и с сохранением verified
generation; actual limits/quotas/reserves, failure containment и counter coverage.
Сохраняются применимые scientific/recovery/trust/native tests; новые finite checks
исполняются только в отдельно admitted envelope, без нового общего framework.
SCI07/08 применяются в этой семантике, не требуют завершения legacy strict branches.

Frozen partial branches, original failed logs/raw/provenance и receipts сохраняются;
их нельзя удалять, merge как готовые или переименовать в новую приёмку. Старый
failed ENV3 и узкий C/SPY outcome не становятся ordinary HDF5/runtime PASS.
Удаление bespoke driver само по себе не закрывает реальные remaining gates.
