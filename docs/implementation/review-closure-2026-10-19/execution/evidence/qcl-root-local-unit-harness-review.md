# Root local unit harness v1 — независимый source review

**APPROVED — guards/capture source, с явно незавершённым source binding перед первым запуском.** `/tmp/qcl-root-local-unit-run-v1.py` соответствует заявленному узкому расширению ранее принятого Python harness. Нового ослабления capture/resource predicates в actual diff не найдено. Reviewer ничего не исполнял: imports/parsers/Python/Node/Deno/Nix/tests/build/network/children отсутствуют; только read-only source/metadata/hash checks и запись report/identity. Это не разрешение дополнительных попыток, runtime pass или BUILD/science acceptance.

## Exact inputs

| Вход | SHA256 |
| --- | --- |
| `/tmp/qcl-root-local-unit-run-v1.py`, 9477 bytes | `eb55de0a1c668723871ea1ae142630df43b024d164fd9564f36be3df68187195` |
| Parent `/tmp/qcl-python-sci03-m1-run-v1.py`, 8124 bytes | `98d91c6795ca4c9425c7dd91a62a3619ca703a936ebac6097158924f7c42124b` |
| RawCapture helper `/tmp/qcl-local-julia-guard-v2.py` | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| TEMP sampler `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| `/tmp/qcl-local-runtime-metadata-preflight-3.json` | `b27ccee2713efb6f23e4895f449cab2973b15ce061b62902de7c5d6f7c1965bc` |
| `/tmp/qcl-local-runtime-binary-identities.json` | `2dda0b8ab62059f6d1dc5a20ce1d3a229a18729e864a192829e4d88312ed9a45` |
| `/tmp/qcl-checkpoint-local-unit-plans.json` | `da756134038875ccd174390b73d36e4147ca0046672d3326f715a3ee6155043d` |
| Pending `/tmp/qcl-doc04-bind-red.py` | `147aa01dd616391d1315e3ae9f79220b6135c72bf8d91fd4a189a7e12fcd91b1` |
| Pending `/tmp/qcl-doc04-red-run.py` | `a5d5a57628979fe863f3c0eccae07966ae207f90872d36b11ace5d026999ff8e` |

Полный harness и diff к parent прочитаны; helper RawCapture и sampler прочитаны без import. Также прочитаны root deno.json, локальные import seams `ops/{solver,application_cd,git,process}.ts` и существующие Deno fixtures для проверки типа side effects. Это не новый CP-CODE verdict для OPS04 продукта или ещё не интегрированных OPS04 tests.

## Guard composition / отсутствие расширения исполнения

Harness9–13 допускает ровно три `(task,kind,ordered fixtures)` комбинации: DOC04/PY один test_docs_assembly.py, DOC04/NODE один docs_math_test.mjs, OPS04/DENO ровно solver_test.ts и application_cd_test.ts. Аргументы не идут через shell. Resolved fixture должен быть существующим файлом внутри fixed root/tests; `::` или иной suffix не проходит exact list equality. Attempt identity ограничена ASCII uppercase/digits/hyphen, поэтому `/tmp/qcl-{task}-{attempt}` не может получить path traversal. `mkdir(exist_ok=False)` сохраняет previous attempt directory и исключает перезапись прежнего raw. Это защита trusted local run, не adversarial concurrent namespace/TOCTOU boundary.

Runtime31 хешируется до Popen; paths явные, не PATH resolution. Python command остаётся selected `.venv/bin/python -m pytest`, ровно заданные fixtures, cacheprovider disabled/basetemp owned. Node — explicit pinned Node24 `--test`, без npm/install/auto-discovery лишних fixtures. NODE_OPTIONS/NODE_PATH вместе с LD/Python injection variables удаляются. DOC04_KATEX_ROOT задан exact supplied 0.16.8 source/package; неизменённый math source дополнительно проверяет ESM/CSS content pins перед target dynamic import. Missing adapter на module import остаётся ожидаемым readiness RED; это не behavioral proof.

Deno37 — pinned2.8.3 `test --cached-only --no-remote --no-npm`, read только root+own TMP, write только own TMP, env только TMPDIR; run/net permissions не выдаются. DENO_DIR находится внутри sampled owned TMP и update check выключен. Root deno.json содержит tasks, но прямой `deno test` их не запускает. Прочитанный current import graph локальный; imported CLI bodies защищены import.meta.main. Current solver fixtures передают fake execute callbacks; production `Deno.Command` в process.ts не вызывается import-ом, а отсутствие run permission не даёт превратить его в разрешённый solver/Nix subprocess. Чтение local source/config разрешено и не эквивалентно execution внешних скриптов.

Node/Python не OS network sandbox: «нет network calls» ограничено reviewed pure source/import envelope, как честно записано в receipt; это не kernel запрет. Deno permissions также не подменяют общий OS/native security proof. Inherited environment не полностью очищается, pytest autoload не отключён новым delta: exact prepared environment/import binding остаётся обязанностью coordinator. Новый install/setup step harness не содержит.

## Runtime evidence chain

Preflight3 связывает selected Node/Deno outPaths с уже зарегистрированным locked nixpkgs source и offline eval, затем хранит version outputs. Ограничение регистрации прямо сохранено: trusted local read-only store metadata, не свежая NAR content verification. Version-output SHA не выдан за binary hash.

Отдельный coordinator receipt binary-identities фиксирует actual binary byte reads, chunk866fb6: Node SHA `decd3927d7a6b9f7c00a58da94f209ea92377a647fd232d4d865ba0e3a28e928`, Deno `cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c`; оба совпадают с literals harness30. Receipt честно указывает217435448 logical bytes и отсутствие CPU/RSS/physical-I/O sampling. Reviewer не повторял эти большие binary reads под своим2MiB read cap. Harness повторно сравнит actual runtime bytes перед каждым launch. Python expected SHA `dd65a07e8f535525443d63e2bd6dd10efbf22bf22e0b6d65e634266acc7ac976` остаётся selected prepared runtime literal; отдельный named Node/Deno receipt не доказывает его version, а launch-time comparison обязателен. `.venv/bin/python` — symlink на `/usr/bin/python3.14`; read_bytes следует к executable.

## Limits / raw и failure truthfulness

Actual delta не меняет set affinity1, RLIMIT_CPU(90,95), 90s wall stop trigger, sampled process-tree RSS1GiB, sampled owned TMP logical regular-file bytes32MiB, raw2MiB envelope и stop threshold за128KiB до него. BLAS/OMP threads1. RawCapture/helper hash, sampler hash, TERM→3s wait→KILL, finally drain/fallback и post-drain output overrun predicate сохранены. Sampler не следует directory symlinks, использует one no-follow stat result и терпит только concurrent ENOENT. Его предел — trusted temporary tree, logical size не allocated disk, sampled не hard quota/transient proof.

Raw thread — byte-preserving, non-daemon, проверяет progress каждого write, сохраняет error; fallback тоже дописывает все partial writes до complete/error. Raw создаётся exclusive до Popen, capture запускается до polling. Final receipt хранит guard error, stop reason, capture completeness/error и overrun; harness exit0 требует child0 **и** отсутствие всех guard/capture/overrun failures. Поэтому child exitcode отдельно не объявляет pass, missing module/assertion failure не превращается в green.

90s — start of stop, не доказанный абсолютный deadline. Номинальная последовательность cleanup может добавить до23s (3+5+2×5+5) плюс sampling, I/O/scheduler overhead; unresponsive I/O и escaped inherited pipe/non-daemon capture не имеют hard realtime guarantee. RLIMIT_CPU per-process, affinity ограничивает используемые CPUs, это не общий cgroup CPU-time/memory quota. Быстро завершившийся процесс может иметь0 samples; peak0 тогда не доказывает отсутствие расходов. Избыточный raw сохраняется и честно маркируется failed, а не молча обрезается до2MiB. Эти унаследованные ограничения не расширять до claims90s hard wall/1GiB guaranteed peak/32MiB hard disk ceiling.

Prelaunch assertions, missing fixture/runtime/helper и source hashing происходят до guarded try и могут остановить harness без собственного receipt. Это известная граница: coordinator должен сохранить outer failed output/intent и reconcile, не повторять молча. Post-launch timeout/error ветки сохраняют original raw и receipt. Общий counter в harness не реализован: unique attempt folder не ограничивает число произвольных labels. Конечные cap4DOC и cap4OPS принадлежат checkpoint/coordinator, не должны выводиться из этого review как новые попытки.

## Current source binding — ещё не ready для call

Hardcoded root3 — `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, actual observed HEAD `d4113f43cddf02d46025434eb3a9dd8e110e90d6`. На момент read обе DOC04 test paths в нём отсутствовали. Reviewed source находится `/tmp/qcl-doc04-root-worktree`; запуск сейчас упал бы на line13, **не** на intended missing adapter. Такой prelaunch stop нельзя засчитать как planned readiness RED и нельзя тратить на него unit attempt.

Parent подтвердил intended pending placement. Прочитанные wrappers адресуют этот gap без расширения harness: bind-red проверяет review SHA, exact reviewed source hashes и отсутствие destination files, копирует только два test files и записывает exact source/harness/review binding. red-run повторно проверяет hashes, отсутствие двух adapter modules, operation/attempt uniqueness, active/unknown/counter state, fresh memory/TMP headroom; intent/call increment фиксируется до subprocess. Missing receipt требует reconciliation без resubmit. Initial PY требует calls0, NODE calls1; это два RED slots, не полный новый4call budget. Result state явно pending_classification при nonzero; исходный raw/receipt ещё должен показать именно expected missing adapter, а guard/time/resource failure должен оставаться failure/unknown, не принятым RED.

Wrappers прочитаны как доказательство заявленного pending mechanism, не исполнялись и не образуют нового broad review checkpoint writer или final source graph. Actual bind JSON/fresh operation admission и OPS04 fresh source binding пока не наблюдались; их наличие/равенство обязателен до sole coordinator execution. Existing Deno fixtures в main сейчас SHA610091e9e5b8a8d30babf5798e3035c164c5b2750e539a6b3e7b0b317ebebd7d / fe4ed69f3c2eeb81813ed0ead23ac1ef70b4edd3745625d311bfade342525034 — это current observation, не утверждение о будущих frozen OPS04 RED sources.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Узкий harness delta сохраняет guards/raw | Полный source+parent diff, helpers hashes | Source only; унаследованные sampled/cleanup caveats | сохранить |
| Node/Deno binary pins согласованы | Preflight3 + actual-byte receipt + harness30–31 | Reviewer не повторял large binary hash; runtime ещё не запускался | сохранить |
| Only exact fixtures / no setup subprocess | Harness9–43, local import seams и fake callbacks | Node/Python без OS network sandbox; owning source binding обязателен | сохранить |
| DOC04 source готов к first RED | Текущие files отсутствуют в hardcoded root; wrappers pending | Нельзя считать missing fixture intended adapter RED | дополнительно измерить |
| Finite calls сохраняются | Plan4DOC/4OPS и wrapper intent/counter preflight | Harness сам общий cap не enforce; нет нового grant | сохранить |
| Actual RED/GREEN/public/native/science pass | Измерений reviewer нет | Unit calls ещё не выполнены; BUILD/public license/schema/science отдельны | данных недостаточно |

**STOP. APPROVED guards source; call readiness pending exact source/runtime/operation binding. Reviewer executions=0.**
