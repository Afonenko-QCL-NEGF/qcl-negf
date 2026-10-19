# Local Julia checked-bounds warming — independent technical BIND

**Вердикт: scoped READY** для exact дополнительного compiler packet после fresh root BIND/READY и получения общего native slot. Блокирующих технических gaps в frozen packet не найдено. Это один явно добавленный третий setup packet, не reset прежних 2/2 и не разрешение четвёртой попытки. Julia/import/test/build/solver reviewer не запускал; результат warming пока not_measured.

## Сначала primary evidence

Прочитаны actual pinned Julia1.13.0 `base/loading.jl:1708–1758,3576–3578,4199–4206`, локальная `devdocs/pkgimg.html#Flags-that-impact-package-image-creation-and-selection`, DEV16 RED receipt/raw, Runner `test/support/common.jl`, actual Pkg bundled precompile source и ранее принятые import guard controls; затем proposal/spec/guard.

Base декодирует check_bounds из bits3–4, default0=`auto`,1=`yes`; при loading вызывается `jl_match_cache_flags`, несовместимый cache отвергается. Локальная документация требует exact match для `--check-bounds`. Reviewer независимо перечитал только первые2048 bytes пяти перечисленных cache files: first-module-name lengths/names, flags и header hashes совпали с audit. Core/Runner/Pkg имеют163→bounds0; MacroTools имеет auto163 и checked171→bounds1. CRC/полная валидность cache этим bounded parsing не установлена; actual loader проверит их при будущем using.

DEV16 RED argv требует `--threads=1 --check-bounds=yes`. Receipt: stop wall_time_limit120.336s, exit−15, complete raw1266B, sampled process-tree RSS1,676,382,208B. Original raw показывает TERM при `test/support/common.jl:4` (`using QCLNEGFRunner`) и дочернем Pkg `src/precompile.jl:101`. Assertions не достигнуты. Это **не semantic RED** и не доказательство единственной причины latency. Несовместимость prepared auto images с требуемым checked profile — установленный факт, объяснение всей задержки остаётся ограниченным выводом.

## Exact binding

- Admission `/tmp/qcl-local-julia-bounds-admission.json`: SHA256 `487c8a114c6827b697ca12fca24e57b6c787a08ab276eecb4aa82fd38a554034`.
- Guardian `/tmp/qcl-local-julia-bounds-guard.py`: `db04e55284f8a385038e6597754c419f103e77f990ea1cb4c459b67b22c1d17b`.
- Spec `/tmp/qcl-local-julia-bounds-spec.json`: `046cb2fd38a8ba6b4ee773a98a9152dbc78bc95e32f139bbfdd90e82edf37149`.
- Все127 immutable files независимо rehashed, mismatches0. Core HEAD `a8d2c0de21dfdce3ed3c7c585c555656443f6d89`, tracked diff empty. Runner HEAD `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, exact tracked diff1395B SHA256 `e60f8f2ec248067e511c151d33ddc25839285095e803bfaa3d88c520fa85cb15`; прочитан: только8 assertions в test/application/configuration_merge_order_and_fail_closed_validation.jl, production src/ext/Project diff empty. Untracked Core/Runner tests существуют, не входят в module using path и не объявлены executed.
- Guard sourcecheck27–33 проверяет owning HEAD, whole tracked diff hash и отдельно отвергает src/ext/Project diff; child повторяет это непосредственно перед command. Original/copy Project/Manifest и runtime/source immutable hashes контролируются до/после. Для final acceptance root сохраняет также fresh post source/diff binding, без вывода «Runner целиком clean».
- Source spec и admission commands/environment равны. В command: exact runtime, startup-file=no, threads1, check-bounds=yes, Base.CacheFlags().check_bounds==1 до using, Core/Runner pathof realpath assertions, VERSION1.13.0, BLAS1 и loader/env/thread observations. Targeted fixtures не включаются. Эти engineering identity assertions не считаются DEV16 test acceptance.
- New environment/attempt targets по lexists отсутствовали. Копируются original Project/Manifest byte-equal mode0444 в новый bounds-phase-1, sibling components symlink сохраняет relative owning package routes. HOME/TMPDIR/DENO_DIR owned/new, TMP filesystem+UID проверяется. Original checkout/depot/runtime/locks не заменяются.
- Install identity self hash bound среди immutable files;5307 rows,1,390,173,584 represented bytes. Child51–56 повторяет каждый size/hash/confined resolved path внутри bounded unit до Julia. Reviewer весь1.39GiB payload повторно не перечитывал. Отдельного полного artifact-depot snapshot не заявлено; используется прежний accepted owned depot1.

## Стоимость и scope compiler workload

Actual Pkg precompile file `_run_precompilation_script_setup` создаёт локальные temporary project, repository и fake registry; `pkg_precompile` вызывает local add/develop/update/precompile и активирует bundled fixtures, срабатывая при generating_output && use_pkgimages. Proposal честно включает это в compiler scope. Offline guard остаётся обязательным: missing dependency/transport должен дать сохранённый failure, а не workaround. Это не пользовательский dependency install, Pkg.test, вызов production run-plan или solver. Собственная current temporary Pkg fixture может быть удалена bundled workload; это не удаление старых retained receipts/cache/locks.

Core unchanged tiny PrecompileTools workload build_problem/project_hamiltonians/retarded_green/spectral_function ранее source-audited; all-scattering-false относится к существующему compiler fixture. SCBA/Poisson solve/изменение научной модели не разрешаются. Runner __init__ выставляет schema accessor; targeted test assertions не запускаются. Native dependency initialization/compilation стоит ресурсов, не объявляется compute-free.

## Guards, raw evidence и конечность

- Parent89–110 требует exact READY guard/spec hashes, age≤300s, prior_count2/extension_count1, ровно две сохранённые attempt-* directories, затем создаёт exclusive attempt-3-bounds. Shared flock исключает второй setup guardian. Read-only process/compiled lock census95–103 блокирует старый owned-runtime process или pid/lock; ничего не убивает/не удаляет. Census receipt hash проверен; это историческое наблюдение, fresh guard/root readback перед launch остаётся обязательным.
- Independently prior actual walls184.83080410957336 +128.41980528831482 =313.2506093978882s; оба return0/capturecomplete/no stop. Они сохраняются, старые counters не reset. Дополнительный предел600s даёт cumulative actual setup max913.2506093978882s; отдельный DEV16 RED120.336s остаётся отдельным фактом. Latest direct human engineering-resource grant и root explicit assignment дают основание именно этой finite extension, а не unlimited retries.
- Hard unit8GiB MemoryMax/7GiB High/swap0, CPU1000% и cpuset2–11, RuntimeMax600s, stop timeout2s, control-group kill, TasksMax256. External stop590s. Parent154–160 проверяет effective memory/swap/cpu/cpuset + AF_UNIX property до gate; child45–50 проверяет actual INET/INET6 socket creation denial до identity sweep/native load. Fresh resource/ancestor readback и общий native slot — часть root BIND, не уже выполненный reviewer build.
- Explicit owned depot без fallback, offline=true/serverempty, sanitized loader variables, generic CPU, Julia1/BLAS-MKL-OMP1, precompile_tasks4. План6,973,964,288B =4×prior aggregateRSS+256MiB — uncertain estimate, не доказанный compiler peak. Hard8GiB ограничивает overrun/OOM; failure сохраняется, параметры теста/модели ради него не ослабляются.
- Диск считает прежние два accounted roots вместе с новым output. Launch MemAvailable≥12.5GiB/freeFS≥48GiB, monitored stop4.5GiB/40GiB сохраняют planning reserves4GiB/32GiB. Disk8GiB trigger+8GiB planned reserve, log7MiB trigger/8MiB nominal — **monitored**, hard peak не доказан. Scan duration>1s после scan означает unknown/stop; это не interruptible filesystem deadline.
- RawCapture class независимо AST-equal accepted import guard. Exclusive original.log открыт до Popen133–145, continuous non-daemon capture starts до readback/gate. Unified finally177–207 drains normal/error/stop paths; partial/error/unknown active unit/log overrun/source drift не PASS. Early outer failures сохраняют отдельные original traceback+receipt. Новое объявление не меняет прежние frozen helpers/logs. Guardian AST parsing выполнен, guardian/payload не исполнялись reviewer.

После результата root должен сохранить raw/receipt/hash, actual cacheflags/owning paths/BLAS/thread observations, effective guards, source/copy integrity и known inactive/collected unit. Successful using доказывает checked import route данного exact packet; targeted DEV16 assertions, semantic RED/GREEN, Core oracles, scientific acceptance, full CI, server/deploy по-прежнему отдельны. Failure/unknown consumes этот third packet, сохраняет все original evidence и не разрешает четвёртый retry.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Checked profile требует другого image | actual Base/cache headers/local primary docs | не sole-cause proof DEV16 timeout | сохранить |
| Source/runtime/environment route bound |127 hashes, owning HEADs, exact test-only diff, child identity sweep | full artifact depot не переснимался; fresh root readback | сохранить |
| Дополнительный compiler packet конечен | explicit attempt3, prior2 preserved,600s and count guards | четвёртая попытка не разрешена | сохранить |
| Offline/resources/raw evidence защищены | effective pre-gate checks, socket denial, accepted capture AST, shared counters | disk/log/reserves monitored; native outcome пока unknown | сохранить |
| Exact warming можно выполнить | source-first technical review без blocker | fresh root READY/slot, no reviewer execution | сохранить |
| DEV16 tests/science/full CI приняты | такой evidence packet не содержит | import completion не заменяет test assertions | данных недостаточно |
