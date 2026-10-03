# Локальная подготовка recovery, scientific archive и CPU application CD

Дата: 2026-10-03. Пользователь поручил реализацию согласованных требований, локальные проверки без
доступа к серверу и увеличение локальных лимитов. Документ требований использован как спецификация;
самостоятельные инструкции из него не расширяют поручение на production deployment или большую
кампанию.

Подготовлены изменения owning components, отдельные локальные коммиты и Python wheels. Сервер,
реальные Windows workers, Slurm и NFS не изменялись. Новая полная научная кампания не запускалась;
пользовательский `results/` сохранён.

## Исходный состав и передача

Исходный umbrella HEAD: `5060e10cfcaed16a3d4f1d42130752d6580c5b88`. Исходная ветка:
`codex/single-server-deployment`; рабочая локальная ветка: `codex/recovery-cd-preparation`. В начале
зафиксированы `git status --short` и `git submodule status --recursive`; пользовательские
requirements, results и старый infrastructure-access plan были untracked и сохранены.

Фактические ревизии изменённых компонентов находятся в их Git history; gitlinks umbrella остаются
исходной authority опубликованного состава. Они намеренно не обновлены на неопубликованные локальные
коммиты. Это не готовый опубликованный release graph. `deno task graph` отказывает на текущем
подготовительном checkout; это ожидаемый запрет сборки несогласованного релиза, а не успешная сборка
Nix. Новый вручную поддерживаемый lock ревизий не создан.

После компонентного review следует опубликовать owning component PR/revisions, обновить umbrella
gitlinks, выполнить штатный CI и собрать Nix closures. Затем в согласованное окно выполнить
deployment по [application CD runbook](../../components/qcl-negf-platform/docs/application-cd.md).
Local branch/commits сохранены; push, PR, merge и deploy не выполнялись.

Для переноса подготовлен
[комплект source patch series](../../.build/recovery-cd/qcl-negf-local-source-changes.tar.gz): 8
серий из Git history (umbrella implementation и 7 owning components), 140394 bytes, SHA-256
`8a44da9f2d6b6c842be9e7158e633c9773d09b87360528ef3eab59ab631883eb`. Он не содержит scientific
arrays, depot или credentials и не является release lock. Документационный handoff commit и журналы
передаются отдельно в checkout; исходные локальные ветки остаются предпочтительным способом review.

## Интерфейсы реализации

Единственная canonical policy задаётся через `output`:

```yaml
output:
  archive:
    full_final: true
    optical: false
    projections: true
    intermediate_history: 16
  recovery:
    enabled: true
    interval_seconds: 1800.0
    retain_generations: 2
    byte_budget: 8589934592
    reserve_bytes: 67108864
  telemetry:
    enabled: true
    buffer_events: 256
```

Однозначные legacy `outputs` преобразуются с предупреждением; одновременные старые и новые поля
отвергаются. Research examples переведены без изменения model/grid/algorithm settings. Archive
finals находятся в `archive/EXECUTION/POINT/final`; recovery generations и указатели
current/previous разделены с архивом. Nonconvergence сохраняется как полный scientific final с
причинами непринятия, pause сохраняет recovery. Analysis и optical artifacts не дублируют тяжёлые
Green/self-energy arrays. Optical HDF5 содержит source receipt и stationary quality; bare-bubble
diagnostics не получают физической приёмки.

Publication receipt `qcl-negf-recovery-receipt-v1` содержит verified status, commit SHA-256, state
ID/sequence и identity, с областью `local_filesystem`. Он доказывает локальную проверку комплекта, а
не доступность NFS с другого узла. Execution progress содержит frozen plan fingerprint и точные
archive references завершённых точек. Проверяются их commit/receipt identities и комплект
`physics.full`, `model`, `science.history`; recovery payload нельзя выдать за final.

`StateReader` возвращает выбранные HDF5 hyperslabs с axes/units/coordinates и имеющимися weights;
отсутствующие weights остаются `None`. Проверка целостности потоково читает весь файл, но не
материализует full numerical arrays. Ограничение `max_bytes` относится к возвращаемым массивам и
векторам; HDF5 chunk/cache workspace остаётся дополнительной памятью. External links, raw external
storage и virtual datasets отвергаются: хеш HDF5 должен покрывать численные значения. Receiver
отдельно проверяет это свойство старых single-file exports до `verified`/restore. Его
`verification_scope` — `transport_hashes_and_hdf5_storage`; legacy multipart scope — только
`transport_hashes`. Ни один из них не означает scientific acceptance или resumability. Seekable
compressed HDF5 member может повторно декомпрессироваться; второй numerical payload tree не
создаётся.

AiiDA использует конечные `BaseRestartWorkChain` attempts/backoff, конкретные
execution/attempt/commit и cumulative numerical budget. Nonconvergence не запускает инфраструктурный
retry. Неоднозначное владение останавливает retry. Slurm `JobRequeue=0`, `ReturnToService=0`;
InstalledCode закреплён на immutable solver executable. Deployed service проверяет shared release
gate до dispatch.

Application CD использует stable profile и runtime configuration, immutable application/solver
closures с NAR hashes, исходный Git graph и release digest. CI и защищённый delivery job разделены.
После однократной подготовки образа routine activation не выполняет `nixos-rebuild`. Проверка
каждого узла включает службы, release identity и короткий solver self-check. Частичный сбой
сохраняет закрытый admission; повтор идентичного delivery запускает остановленные службы. До
закрытия admission controller получает обе closures из указанного Nix cache и сверяет их локальные
NAR hashes с manifest. Неполный inventory или отказ prefetch сохраняет прежние gate и службы. URI
передаётся отдельным argv; настройки доверия Nix не ослабляются. Cache metadata не меняет release
identity.

Windows adapters учитывают все allocated jobs узла и каждого пользователя, сохраняют snapshot до
pause и ждут подтверждения с постоянного узла. Исчезновение job из `squeue` не удаляет требование
receipt. Idle shutdown не ждёт checkpoint; следующая allocation не является условием выключения.
Unsupported allocated states дают явный отказ. Реальное GPO/Hyper-V/network ordering ещё не
проверено.

## Среда и конечный бюджет

Совокупный разрешённый лимит после увеличения: 4 CPU одновременно, 10 GiB RAM, 4.5 часа тестового
wall time, 4 GiB временных данных, до 4 исправлений на один сбой. Runner использовал 2 Julia
threads; native integration и operator fixtures — 1 Julia thread, BLAS/OMP=1. Лимит относится к всем
агентам вместе. Для малых операторных запусков с JIT/retries дополнительно зафиксировано 30 минут, 1
CPU, 3 GiB RAM и 10 MiB вывода в
[research fixture plan](../../components/qcl-negf-research/docs/fresh-fixtures-2026-10-03.md). Это
расширенный локальный инженерный бюджет; строгие малые RAM limits без JIT научной постановки
отдельно не сертифицированы измерителем peak RSS.

Первоначальный общий предел составлял 4 часа. Из пользовательского разрешения увеличить локальное
время сделано одно конечное расширение до 15:20 UTC: если финальный whole suite не завершится в
прежнем guard 2100 секунд, допускается один focused run только незавершённого хвоста на той же
immutable ревизии, максимум 20 минут, 2 CPU/6 GiB. Полный suite повторно не запускается; ошибки и
timeout не переписываются в pass. Бюджет операторных probes ниже сохраняется отдельно и не начинает
новый отсчёт.

Использован точный Julia 1.13.0, а не системный 1.13.1. Официальный архив: SHA-256
`8975da61c128a5e5ded3e719e868da8c8781deb7ad7913d37fb99be02a81904b`. Временный Project/Manifest
использует исходные pinned versions и абсолютные локальные component paths;
`Pkg.instantiate(update_registry=false,
allow_autoprecomp=false)` выполнен без package
update/resolve. Temporary depot: `/tmp/qcl-implementation-depot:/home/tolya/.julia`. Production
project не переключён на другую Julia. В umbrella Manifest добавлена зависимость Runner на уже
закреплённый stdlib Downloads; версии пакетов не обновлены.

Python 3.14.7, pytest 8.4.2, AiiDA 2.9.2, h5py 3.16.0; Deno 2.9.7. Nix evaluation использовала
существующий cached nixpkgs. Полная Nix/NixOS сборка не выполнялась. Отключён compiled-module cache
для Julia probes: JIT составляет минуты и явно включён в wall time. Один ранний Pkg DNS failure был
повторён успешно; после сообщения пользователя об исправленном интернете незавершённых network tasks
не найдено. Native fixture timeouts были связаны с JIT и устаревшими fixture ожиданиями, а не
соединением. Старые большие temporary test fixtures удалены после успешных повторных проверок;
журналы и текущие малые native fixtures сохранены.

## Проверки и свидетельства

Полные журналы находятся в `/tmp/qcl-implementation-tests/`. Выбранные короткие финальные журналы
сохранены в [evidence](evidence/recovery-cd-2026-10-03/). Ниже перечислены разные наборы; их
счётчики не складываются с повторными regression runs, поскольку некоторые проверки перекрываются.

| Проверка                                                    | Свежий результат                                                                             | Ограничение                                                                                                                                      |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Runner `c4e5b37`, общий запуск пяти групп                   | 57 файлов последовательно завершены без failure diagnostics; guard 2100s, финальный exit 137 | SIGTERM застал компиляцию текущего SCBA fixture; завершён только own process group. Это **не pass** полного suite, итогового assertion total нет |
| Runner `c4e5b37`, оставшийся хвост                          | 405/405 assertions, 19 файлов, 14m46.1s, exit 0                                              | Отдельный finite процесс на той же ревизии; whole single-process status остаётся timeout/exit137                                                 |
| Runner до последних review fixes                            | 2001/2001 assertions, 23m32.0s                                                               | Предыдущая ревизия; её успех не заменяет проверку финального `c4e5b37`                                                                           |
| Contracts + results + research pytest                       | 299 passed, 504.05s                                                                          | Окончательный results `f50c35a`; включает external/VDS export/receive regressions и большие transport fixtures                                   |
| Реальный Julia → HDF5 → selective reader → Python export    | 1 passed, 331.74s                                                                            | 33 E, 3 k, 2 basis; диагностическая SCBA fixture, scientific accepted=false                                                                      |
| AiiDA полный suite после review fixes                       | 92 passed, 173 warnings, 68.79s                                                              | Изолированные localhost AiiDA fixtures, не Slurm hardware                                                                                        |
| Platform `deno task check`                                  | 9 Deno + 107 Python tests, pass                                                              | Включая cache prefetch/NAR preflight; unit/simulated adapters, без реальной активации                                                            |
| Umbrella `deno task check`                                  | 14 Deno + 8 Python transfer tests, pass                                                      | Closure build/delivery не запускались                                                                                                            |
| Nix release/monitoring/Munge evaluation                     | pass                                                                                         | Cached nixpkgs, dummy store evaluation; не сборка image                                                                                          |
| PowerShell startup/shutdown parse                           | syntax OK для обоих файлов                                                                   | Syntax не доказывает порядок выключения Windows                                                                                                  |
| Frozen support + impurity + PV + literal contraction oracle | 15 assertions pass                                                                           | Операторные проверки, без большого SCBA/Poisson                                                                                                  |
| Existing full-window basis + analytic product integration   | 47 assertions pass                                                                           | Фиксированная represented geometry и finite window                                                                                               |
| Runner strict Documenter build                              | pass                                                                                         | HTML warning 117.51 KiB при warn threshold 100 KiB, ниже hard threshold 200 KiB                                                                  |
| Реальный холодный CLI `self-check`                          | exit 0 в пределах `timeout 300`, PV error 1.766974823035287e−17, HDF5 round-trip true        | Julia 1.13.0, 1 CPU, compiled modules отключены; это operational/code evidence, scientific accepted=false                                        |
| Python wheel build/ZIP integrity/entrypoints                | contracts, results, AiiDA                                                                    | Package artifacts локальные; Nix release closures ещё не собраны                                                                                 |

Готовый локальный
[комплект Python wheels](../../.build/recovery-cd/qcl-negf-local-python-packages.tar.gz) содержит
contracts/results/AiiDA 0.2.0 и автоматически полученный build-evidence JSON с component
commit/bytes/SHA-256. SHA-256 комплекта:
`83978a23c0c58411366baa36b77d4329f29caeb9c6c5fbf10c044ed8d4304723`. Из извлечённых wheels проверены
imports, schema resources и все 6 entrypoints; editable source packages для этих проверок не
использовались. Архив находится в ignored `.build/`, не является опубликованным release или revision
lock. Его зависимости следует устанавливать по существующему shared lock; полная Nix closure и
scientific Julia environment не упакованы в этот Python комплект.

Воспроизводимые команды для обычных entrypoints:

```bash
.venv/bin/python -m pytest -q components/qcl-negf-contracts/tests components/qcl-negf-results/tests components/qcl-negf-research/tests
.venv/bin/python -m pytest -q components/qcl-negf-aiida/tests
deno task check
# из components/qcl-negf-platform:
deno task check
```

Native producer требует точного локального Julia environment:

```bash
JULIA=/tmp/qcl-implementation-tests/julia-exact-no-cache \
JULIA_DEPOT_PATH=/tmp/qcl-implementation-depot:/home/tolya/.julia \
QCL_NEGF_SOLVER_PROJECT=/tmp/qcl-implementation-julia \
QCL_NEGF_INTEGRATION_TIMEOUT_SECONDS=840 \
timeout 900 .venv/bin/python -m pytest -q \
  components/qcl-negf-results/integration/test_live_julia_export.py
```

Wrapper добавляет `--compiled-modules=no --check-bounds=yes` к `/tmp/qcl-julia-1.13.0/bin/julia`.
Его назначение — воспроизводить эту временную проверку; deployment должен использовать закреплённый
executable выбранного Nix release, не временный wrapper.

Холодный публичный CLI проверен отдельно на Runner `c4e5b37`, без SCBA/Poisson:

```bash
mkdir -p /tmp/qcl-implementation-tests/cli-selfcheck-final
JULIA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
JULIA_DEPOT_PATH=/tmp/qcl-implementation-depot:/home/tolya/.julia \
QCL_NEGF_PROJECT=/tmp/qcl-implementation-julia \
timeout 300 /tmp/qcl-julia-1.13.0/bin/julia --compiled-modules=no \
  --startup-file=no --check-bounds=yes \
  components/QCLNEGFRunner.jl/bin/qcl-negf self-check \
  --directory /tmp/qcl-implementation-tests/cli-selfcheck-final
```

Первый CLI запуск остановлен timeout 124 при компиляции общего `main`. Служебные команды отделены от
solver inference отдельными handlers через `Base.invokelatest`. Первый повтор вернул exit 2 из-за не
созданного parent directory в моей тестовой команде; после исправления fixture setup получен exit 0
при том же лимите 300 секунд. Ответ сохраняет scientific accepted=false,
iterative/discretization/experiment=`not_evaluated`. Это не сравнительный benchmark скорости solver.
Production admission сохраняет отказ при любом неуспешном self-check; его timeout не увеличен ради
зелёного результата.

Финальный полный Runner entrypoint запущен с конечным timeout и остановлен по этому guard; нулевой
exit и полная итоговая сводка не получены:

```bash
JULIA_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
JULIA_DEPOT_PATH=/tmp/qcl-implementation-depot:/home/tolya/.julia \
timeout 2100 /tmp/qcl-julia-1.13.0/bin/julia --compiled-modules=no \
  --project=/tmp/qcl-implementation-julia --startup-file=no --check-bounds=yes \
  components/QCLNEGFRunner.jl/test/runtests.jl \
  application contracts infrastructure presentation integration
```

Финальный whole запуск завершён guard/SIGTERM и принудительной остановкой только его own process
group, exit 137. Отдельный хвост завершился exit 0: 405/405 assertions, 19 файлов, 14m46.1s. Сверка
completed-prefix и tail manifest с каталогами test подтверждает 57 + 19 = 76 файлов всех пяти групп
без пересечений и пропусков. Это покрытие двумя ограниченными процессами на immutable `c4e5b37`, а
не успешный непрерывный whole suite; общий assertion total не восстанавливается из частичного
процесса. Перед публикацией остаётся штатный CI на опубликованном составе.

Warmed scalar sender probe: 1000 самостоятельных событий по 293 bytes, 1 CPU, Julia 1.13.0;
compilation time в измеренном producer span равен нулю. Для отключённого mocked collector producer
занял 0.031515812 s, allocated 5,061,944 bytes, queued 256/dropped 744. Closed sender: 0.000016434
s, 0 allocated bytes, rejected 1000. Outer wall time 4.725168789 s, peak RSS 245244 KiB <256 MiB.
Это стоимость малого scalar producer в fixture, не production network/solver overhead и не обещание
ускорения.

## Научные выводы и их пределы

В `QCLNEGF.jl/test/numerics/frozen_scientific_fixtures.jl`, baseline core
`4143ed54cecef7a858a6a372b624dfab11280df5`, новые test commits `6110288` и `aebe181`, fixed-spectral
remap даёт:

| Наблюдаемая                                                       | Свидетельство                                                                                                                                              | Ограничение                                                                     | Решение             |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------- |
| Shift влияет на represented connectivity                          | bias shift 0/0.5: sectors 2/1, edges 47/77                                                                                                                 | Scalar fixed spectrum 17 nodes, не нелинейный QCL fixed point                   | сохранить           |
| Weighted sector collision balance                                 | actual Sigma lesser/greater и G lesser/greater; sums −1.0547118733938987e−15 и −7.771561172376096e−16, критерий 64 eps × positive weighted collision scale | Не диагноз старой несходимости и не conservation certificate произвольной сетки | сохранить           |
| Frozen impurity contraction согласуется с независимой квадратурой | midpoint oracle 2048/4096: change 8.059506788280591e−7; weighted relative error 3.8065916387746864e−7; oracle norm 0.0007898656815498527                   | Общие geometry/screening inputs; не ошибка integrated current                   | сохранить           |
| PV analytic element                                               | absolute error 1.766974823035287e−17 против analytic triangular element                                                                                    | Finite window/tails остаются ограничением                                       | сохранить           |
| Причина старой SCBA несходимости                                  | Старые numerical arrays отсутствуют; synthetic fixtures не восстанавливают кампанию                                                                        | Нет принятого stationary result или experiment evidence                         | данных недостаточно |

Oracle contraction использует буквальные индексные суммы, а не production contraction helper. Sector
balance измеряется из фактических Sigma/G collision terms, а не определяется как тождественно
зануляющийся graph inflow−outflow. Basis fixture сохраняет represented geometry и pre-crop
reference; physics production equations, tolerance, mixing и grids не изменены.

В support/PV fixtures энергии, ширины ячеек и абсолютные ошибки безразмерны: это объявленные
synthetic operator coordinates. Support widths равны 1 внутри окна и 0.5 на концах. Collision
criterion нормирован положительной взвешенной суммой модулей обоих collision terms по всему
represented окну; fixture требует scale>0, отдельной приёмки нулевой нормы не заявляет. Impurity
relative error и oracle refinement change безразмерны и нормированы ненулевой norm(oracle4096);
physical inputs этой отдельной fixture имеют K, eV, nm и nm⁻¹, как заданы в исходном коде.

## Хранение и AC0–AC8

Runner recovery accounting включает regular files в `OUTPUT/executions` и `OUTPUT/recovery`:
локальную историю, progress, logs, retained generations, pending staging и импортируемый bundle.
Проверки выполняются при import и до/после staging, перед publication. Это не quota на каждую
промежуточную запись observer. Plan/series/control JSON и scheduler stdout/stderr вне этих roots.
При включённом recovery старый scratch staging обходится; recovery-disabled legacy scratch не
получает hard byte guard. Для finals проверяются lower-bound forecast, staging и свободное место, но
весь архив не ограничивается размером и не удаляется.

Prior archive transfer имеет отдельный конечный `archive_byte_budget` (default 64 GiB), точную
declared closure и reserve. AiiDA FolderData/retrieved outputs добавляют тяжёлые
transport/provenance copies; наличие одного владельца physics payload в научном комплекте не
устраняет эту цену. Полная accounting retrieval/stdout и hard physical limits требуют штатной
filesystem quota или отдельного bounded volume на deployment. Free-space forecast не заменяет quota.

В prior dependency verifier сначала читается commit metadata с cap 16 MiB и оставшегося budget,
сверяются полный owner inventory и реальные размеры всех файлов. Только затем запускаются
receipt/hash/native checks. Регрессия с omitted тяжёлым `physics.h5` подтверждает ноль вызовов
тяжёлого verifier до отказа.

Export spool имеет finite logical byte guard (default 64 GiB, reserve 64 MiB): capture, history
proof copies, HDF5/Parquet derivations, XZ archive и temporary receipt учитываются одновременно.
Controlled writes проверяют growth, refusal сохраняет исходные данные/предыдущий archive и очищает
только own staging. Logical counter не покрывает filesystem allocation/metadata или другие процессы;
подробнее [export budget](../../components/qcl-negf-results/docs/export-budget.md).

| Критерий                                  | Локальное свидетельство                                                                                                                 | Ограничение                                                                            | Решение                |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------- |
| AC0 единая policy/состав                  | Schema/conflict/migration tests, canonical examples, graph guard                                                                        | Опубликованный новый Git graph ещё не собран                                           | изменить               |
| AC1 round-trip/качество/выборочное чтение | Native Julia→Python export, identity/axes/unit/receipt and optical tests; unknown не accepted                                           | Reader output cap не whole-process RAM cap                                             | сохранить              |
| AC2 retention и bytes                     | Fault tests, finite recovery/import/export logical guards, no final pruning                                                             | Aggregate hard quota scratch/log/retrieval и полный forecast **не выполнены** локально | изменить               |
| AC3 resume/fallback                       | Двухточечная portable fixture сохраняет first final SHA/attempt1 и second-point cumulative budget в attempt2; corrupt/no-bundle refusal | Cross CPU/NFS durability и release compatibility на hardware not_verified              | дополнительно измерить |
| AC4 finite attempts                       | AiiDA classification, exact selection, ambiguous-owner/nonconvergence/no double event tests                                             | Реальная Slurm node migration not_verified                                             | дополнительно измерить |
| AC5 CD/admission                          | Partial/idempotent/offline/old-job tests; mandatory self-check и immutable Code                                                         | Реальный Nix closure delivery и services not_verified                                  | дополнительно измерить |
| AC6 Windows lifecycle                     | Multi-user/multi-job snapshot, permanent-node receipt, no-allocation wait и syntax tests                                                | GPO/VMMS/LAN ordering на обеих Windows machines **not_verified**                       | дополнительно измерить |
| AC7 monitoring/resources                  | Bounded scalar sender/drop tests, resource/provenance probes, collector/export example и fictional access template                      | Central ingestion/production overhead и объяснение прежних 1–2/16 CPU не измерены      | дополнительно измерить |
| AC8 новые fixtures/следующий plan         | Independent operator oracles, новые native states без старых matrices, finite research plan                                             | Полная stationary/discretization/experiment acceptance отсутствует                     | сохранить              |

Таким образом, локальный инженерный комплект подготовлен; AC2–AC7 нельзя объявить общей
infrastructure acceptance до перечисленных deployment checks. Telemetry failure не является причиной
scientific retry. Отсутствие данных или измерений не записывается как pass.

## Независимое review и следующий шаг

Независимый reviewer читал неизменяемые component commits и использовал малые HDF5/JSON fixtures,
без запуска solver. Исправлены incomplete final closure, conflicting progress identity, HDF5
external/VDS ownership, смешение final/recovery в parser, неверный release guard path, пропущенная
deployed release identity, идемпотентный start служб, per-unit health, mandatory solver self-check и
shutdown state coverage. Согласие reviewer не заменяет численные или hardware свидетельства; общие
geometry и native contract helpers ограничивают независимость. Дополнительное review выявило
пропущенный controller cache prefetch: он добавлен перед maintenance вместе со сверкой обеих
closures и регрессиями. Pinned HDF5 ABI проверен независимо по headers и экспортируемому
`H5Lget_info1`; прямой вызов использует тот же native library lock, что и стандартные wrappers, и
освобождает его в `finally`. На immutable Runner `c4e5b37` reviewer подтвердил закрытие preflight
finding и отсутствие новых блокирующих source замечаний. Cold CLI exit 0 проверен отдельно; runtime
evidence и source review остаются разными свидетельствами.

Для внедрения нужны: опубликованные компонентные ревизии и gitlinks; CI closures; однократная
image/profile подготовка; реальные storage quota и LAN fsync/rename probes; startup→shutdown на
каждой Windows машине с двумя jobs и недоступным collector; короткая AiiDA/Slurm pause→resume на
совместимом CPU; проверка gate при partial CD/offline worker. Реальные credentials в исходники не
добавлены: используется
[фиктивный access template](../../components/qcl-negf-platform/examples/access-inventory.md.example).
Большое следующее исследование выбирается после просмотра малой новой stationary точки и её
отдельных scientific gates согласно research fixture plan.
