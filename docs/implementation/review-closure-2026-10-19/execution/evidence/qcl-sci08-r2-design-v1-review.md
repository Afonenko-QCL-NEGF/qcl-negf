# Независимый high source review SCI08-R2 v1

2026-10-20. Объект: `/tmp/qcl-sci08-r2-design-v1.md`, SHA256 `69313bd117c140cf28b68d62ebb85b09bbc078a0ad305b3199c65ee55636e08c`. Review выполнен отдельным агентом, без детей; author diagnosis в качестве доказательства не использован. Исходный вопрос: достаточно ли одного finite Runner resident/growth contract, чтобы реализовать отказ до uncontrolled write с сохранением последнего verified состояния и исходных failed данных, не выдавая design за campaign admission?

**Вердикт: узкая обязательная поправка к cleanup перед writer-enabled I; арифметика, fail-closed authority port и refusal-only subset I-ready.** Это один воспроизводимый конфликт интеграции, а не требование нового общего design цикла. Полный R2 v1 нельзя передавать как безусловно однозначный writer-enabled implementation contract. Поправку ниже можно включить непосредственно в owning I task; второй полный дизайн не нужен. Runtime/test/native grant и CP-SCI READY не выданы.

## Первичные источники и binding

Независимо сначала прочитаны SCI07 D2 §§2–3, SCI07 D1 inventory/lifetime paragraphs и `science.md:151–176,374–405`, затем сопоставлены с R2 и текущими writer loci. D1 inequality прочитана только вместе с заменяющим D2; historical pins не представлены current source graph.

Selected tree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`: actual Root `107bac5697b37cf0e47c3feb44883a907837645c`; Runner gitlink `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`. `git status --short` показал только прежние root checkpoint/docs artifacts из identity автора; компоненты не отмечены dirty. `git submodule status --recursive` дал те же восемь gitlinks, что author identity. Gitlinks — authority; identity этого review — forensic observation, не второй revision lock.

Проверены точные SHA256:

| Input | SHA256 |
| --- | --- |
| R2 design | `69313bd117c140cf28b68d62ebb85b09bbc078a0ad305b3199c65ee55636e08c` |
| R2 identity | `5fe810be19f9279fe915374a8bab8f8e83d2e0b1e22cbc286c904dcba5824ff1` |
| R2 read ledger | `7334cf7b7f3f648007e2eedebc8d1a5e42f37f01bab0f6b66b7e6901005a7ab6` |
| SCI07 D1 | `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635` |
| SCI07 D2 | `fc78a0c77394f4d12a1c5633b7e4acb587429667abc106f5aa72c1dc4dd9d010` |
| science.md | `0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a` |
| Runner point_artifacts.jl | `18bcd0fe2c6ff42050c500b57f17678b06a38f14871a9a3de437841cb5f8d1ad` |
| Runner scratch_execution.jl | `cad52756bb47a6d1fa63cd8c86a03c4e4dcd0d9a4e12383a0671dd766697f395` |

Применён qcl-performance-audit только как source audit стоимости/coverage хранения. Production results, native capacity и научная приемлемость здесь не измерялись. Scientific unit — frozen S1, принятый handoff, без изменения physics/grids/basis/scattering/tolerances/full_final.

## F1 — high: strict failure preservation конфликтует с существующим unconditional cleanup

**Локатор design:** R2 §5 шаг 5 требует partial/failed/temp оставлять E либо conservatively retained U и запрещает R2 delete/prune; §6 требует original failed logs/receipts сохранять. §2 одновременно сохраняет existing publication contract и перечисляет перехват writer growth, но не разрешает этот уже существующий cleanup конфликт.

**Локатор source:** Runner `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`, `src/infrastructure/persistence/point_artifacts.jl:1100–1101` содержит `finally; isdir(stage) && rm(stage; recursive=true, force=true)`. Такой же pattern найден у operator writer `:1323–1324`. `src/composition/scratch_execution.jl:110–111` удаляет `temporary` в `finally`; `scientific_history.jl:222–223` имеет cleanup временного history файла. Первое тело прочитано непосредственно; остальные — точные source-search loci, требующие body trace на I.

**Воспроизводимый source сценарий:** strict operation получил permit; `_write_checkpoint` материализовал часть `pending-*/physics.h5`; следующий subpermit отказал либо callback бросил exception до `mv(stage,final)`. Стек исполняет существующий unconditional `finally` раньше, чем outer `with_storage_operation` сможет settle authority. Last verified pointer может сохраниться, но partial failed массив уже удалён. Удержание U вместо refund сохраняет консервативный долг, однако не восстанавливает исходные данные. Поэтому wrapper alone недостаточен для обещания §§5–6.

**Минимальная обязательная поправка I-контракта:** перечислить cleanup/delete transitions вместе с growth transitions. В `campaign_strict` после первой mutation любого failure/unknown outcome дочерний writer не удаляет partial stage/temp; operation передаёт их exact path/domain/identity и conservative debt в settlement. Не писать новый receipt сверх уже выданного capability. До первой mutation освобождать лишь доказанно unmaterialized reservation. Для успешной existing publication отдельно сохранить обычный verified recovery retention/prune, если это прежний контракт, но не использовать будущий prune как admission credit. Standalone cleanup можно оставить прежним. Если конкретная ветка не умеет так сохранять partial data, она остаётся strict-refused до первой mutation. Это не поручение менять format, atomic ordering или retention policy научных finals.

**Различающее I evidence:** handwritten fake writer/event log: partial stage существует; next growth refusal; далее ни одного delete этого stage, last verified current/previous не изменён, materialized/uncertain debt не освобождён. Отдельно успешный путь сохраняет существующий publish/verify/receipt/pointer/fsync порядок и только допустимый existing post-ack recovery pruning. Источники таких fixtures допустимы в I; запуск не разрешён этим review. Недостаточно проверить только mutation-count0 при initial refusal: он не достигает проблемного `finally`.

## Что подтверждено и остаётся конечным I scope

1. `G=U+P+S`, `T=E+G`, `T≤A` и независимое `Gphysical≤Hphysical` соответствуют SCI07 D2. E не debit второй раз к already-remaining H. Net normalization допускается только с exact same-epoch disjoint reservation IDs; materialized/preallocated blocks не add-back. Literal total/free boundary pairs различают исходную ошибку baselines. Это source arithmetic, не выполненный scalar test.
2. Resident inventory включает shared S1 2 TiB, per-attempt 128/256 GiB, исходные и новые copies, pending/final/history/receipts/pointers/logs/import/retrieval/export/repository и завершённые failed attempts. Hardlink/reflink credit без identity/lifetime proof запрещён; physical domain aliases не создают дополнительную capacity. Physical allocation, logical attribution и inodes различаются. Неполная attribution или external consumer coverage явно отказывает/блокирует READY.
3. Reservation linearization, single parent permit, disjoint child allowances, U→E transfer, uncertain leases и no reset on retry/restart/exit заданы достаточно для source protocol. Они не доказывают native concurrency. Materialized E может уменьшаться после independently attested lifetime end; historical high-water/cumulative counters не уменьшаются вместе с ним.
4. Unknown capacity, ownership, growth bound, FS mapping или authority не превращается в 0/pass. HDF5 forecast `16 MiB + 4×…` прямо исключён как native upper bound; high-level pre-call checks и post-size samples не заменяют finite allocation proof. Поэтому production strict serializer без доказательства остаётся закрытым. Это допустимый refusal-only результат реализации.
5. R3 stop, P1 physical/native ownership, P2 cumulative I/O/logs, A1 consumers и C1 persistent campaign reservation оставлены отдельными незакрытыми gates. Source API не выдаёт чужому exporter enforcement и не создаёт новый service/registry/UI owner. R1 historical 349 PASS, cgroup/boot/free/prewriter checks не становятся campaign acceptance.

**Наименьший I-ready subset сейчас:** typed finite inventory/domain/identity/refusal structs; checked baseline arithmetic; authority interface с production default refusal; scoped permit/subpermit state machine и handwritten source fixture definitions; strict dispatch, который при missing authority/bounds/coverage отказывает до любого filesystem mutation. Этот subset не включает production разрешение serialization/copy, внешние consumers или заявление shared enforcement. С F1 как обязательным implementation condition один owning Runner PR может также подключать writer hooks; любая неаудированная cleanup/growth ветка остаётся strict-refused. Не требуется расширять scope до C1/P1 implementation.

## Границы проверки

Только чтение и хеширование исходников/документов, read-only Git и создание двух review outputs в `/tmp`. Source reads ограничены указанными диапазонами и symbol searches; whole-callgraph не проверен. Попытка `cat components/QCLNEGFRunner.jl/AGENTS.md` обнаружила отсутствие файла; `rg --files -g AGENTS.md` в Runner дополнительных инструкций не нашёл. Reference telemetry вывод одного чтения был усечён; непрочитанное не используется как доказательство. Полный design/identity/ledger прочитаны. Записанные source hashes не означают semantic read всего файла.

Не исполнялись scripts/imports/parsers/compiler/tests/runtime/native/network/CP/CI/solver; source/index/checkpoint не изменялись. CPU/RAM/I/O и полный byte total не замерялись независимо; измеренное соблюдение лимитов не заявляется. C08 SCI05/SCI08 остаётся **8/8 EXHAUSTED**, product runtime90/source9 — полученный контекст, не новый grant. Review не обнуляет round/campaign counters. Budget исполнения controls не появился.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D2 total authority и incremental headroom перенесены корректно | SCI07 D2 §§2–3; R2 §§4,7 | Source reasoning; нет actual capacity | сохранить |
| Refusal-only Runner port/arithmetic subset пригоден для I | R2 §§1,3,5,7 и explicit unknown→refusal | Не production serializer/enforcement | изменить |
| Writer-enabled strict preservation требует cleanup correction F1 | Runner4f60 point_artifacts:1100–1101,1323–1324; staging:110–111; history:222–223; R2 §§5–6 | Остальные тела cleanup ещё требуют I trace | изменить |
| Finite native HDF5 upper bound и ownership пока не доказаны | R2 §5 явно требует proof/refuse; science.md Admission/guards | Нет native measurements/enforcement | данных недостаточно |
| R3/P1/P2/A1/C1 и campaign READY закрыты | R2 §8; science.md SCI07/08; C08 exhausted context | Review не исполняет и не финансирует gates | дополнительно измерить |

**STOP.** Передать узкую F1 поправку как binding condition owning I. Без нового runtime grant только source implementation/fixtures; кампанию не запускать.
