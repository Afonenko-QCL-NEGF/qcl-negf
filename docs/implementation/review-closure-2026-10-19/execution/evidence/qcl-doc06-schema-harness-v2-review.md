# DOC06 schema harness v2: повторная независимая source-проверка

2026-10-20. Verdict: **PASS_SOURCE_CORRECTIONS_R1_R2_R3**. Все три замечания исходного review закрыты на уровне текста. Новых блокирующих замечаний в focused scope не найдено. Это не runtime acceptance и не execution grant; после этого report остаётся **STOP_FOR_ROOT_READINESS**.

Исходный `/tmp/qcl-doc06-schema-harness-review.md` сохранён с SHA `787e5728d3541584ca91b84be1b76e181863cd83e12233b399e209110d9a3fa3`. Повторный review выполнил тот же независимый рецензент.

## Exact inputs

Все paths имеют prefix `/tmp/qcl-doc06-schema-`.

| Файл | Bytes | SHA256 |
| --- | --- | --- |
| format-run-v2.py | 24613 | 2daef993d218ac2d4e1cabfc44018725c19a55d60187d43d3d954cef33664aa4 |
| lint-run-v2.py | 24608 | 19ed0f182a51fd5022b0c1068367f92b8019beb74d0e304ee94a744da697a8ee |
| local-unit-run-v2.py | 31965 | 45e2848cc3cf193c3b9533dcdb518b5daf307da1fbb99546ab619343b1278bef |
| engineering-plan-v2.json | 4632 | 2206d06e2c072b5132db0a2a89048a7df5ef2602961bd03c19ef916cad5c824c |
| harness-report-v2.md | 9267 | 54e0a44f78729045ac914c98f425383e9647a6ff1320e7f08a691e5bde887d92 |
| harness-identity-v2.json | 2846 | 7e4d715b8cd246e1ab5bd2ac10256f776925ebeed3254434522d44f5face8fa5 |

SHA и размеры независимо пересчитаны. Вновь прочитаны current Root HEAD/status/submodule status read-only с `GIT_OPTIONAL_LOCKS=0`: HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`, modified checkpoint +2 owning source paths и untracked publication/evidence metadata, восемь initialized gitlinks без `+`/`U`. Source hashes по-прежнему adapter `aa476aabdb044b020040816fdf7c2f7983082d28f6c15b01ccf1cbae307998ee`, tests `ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04`. Это review snapshot; fresh READY должен повторно устанавливать actual Root identity перед будущим запуском.

## R1 закрыто: current HEAD проверяется, author base отделён

Все3 scripts `actual_head():46–53` выполняют фиксированный `/usr/bin/git -C <Root> rev-parse HEAD` с clean env PATH/GIT_OPTIONAL_LOCKS=0, timeout3s/check=True и40hex validation. READY.head теперь late-bound (`read_ready():62`), plan отдельно сохраняет author_cpp_base_head2bb… вместо ложного current head.

Readiness`:100–101`, prelaunch`:148–149` и terminal`:156–157` независимо сравнивают actual HEAD с READY.head. Невозможный Git readback вызывает failure; head observations записываются в receipt и outer failed metadata, недоступное значение не заменяется frozen author head. Прежние source/runtime/helper/config/harness/plan/READY bindings сохранены. Смена checkout между наблюдениями не скрывается утверждением о постоянстве HEAD; граница остаётся доверенной локальной workspace без adversarial race guarantee.

## R2 закрыто: RSS unknown не становится0/pass

Format/lint `rss_tree():209–236`, `observe_rss():238–249`, initialization`:256–260`, postspawn`:282`, terminal gate`:344–347`; E1 соответствующие sections`:278–318`,`:325–329`,`:367`,`:432–435`.

`peak=None` до измерения. Missing selected pid/VmRSS, malformed fields или read errors вызывают recorded failed observation. Только raced ENOENT при census пропускается; отсутствие selected pid затем явно unknown. Completed/failed counters, phases, errors и status сохранены в receipt. Fast exit без валидного snapshot имеет nullable peak и failure, вместо measured0. Pass требует хотя бы одно выполненное наблюдение и отсутствие failed observations; превышение measured cap также оставляет reason. Зафиксированное VmRSS0 при существующем поле является наблюдением, отсутствие поля им не является.

Это sampled lower bound, не доказательство transient maximum. Census всего `/proc` консервативно может отказать из-за чужого unreadable/malformed status; это fail closed, а не ложное acceptance. Политика не добавляет retry. TMP peak тоже nullable, phase probes сохранены.

## R3 закрыто: после reservation есть внешний failed-receipt путь

Outer `try:24` начинается до temporary.mkdir, после единственного успешного permanent exclusive folder reservation. Охвачены readiness, seed, log open, Popen, capture/drain, summary/readback, terminal bindings, receipt и console output. Format/lint outer exception`:371–428`, E1`:476–533` создаёт outcome=failed, сохраняет original exception/rescue errors и nullable unknowns; no-child capture не называется complete/0.

Старый E1 unconditional read исчез. `raw_metadata():240–272` ловит missing/unreadable log, возвращает readback_failed/error; E1`:465–470` допускает summary только при complete capture без capture_error и требует literal74-summary=true. Путь log-open failure теперь заканчивается failed receipt или outer fallback. Ошибки inner finally и persist/print также попадают в outer envelope. Пытаются записать receipt.json, затем failed-receipt.json; при отказе обоих stderr JSON, затем minimal os.write fallback содержат consumed stage/folder и reconciliation requirement. Полный отказ всех I/O нельзя сделать durable программным обещанием, и report этого не утверждает.

Streaming raw metadata ограничен64KiB blocks,128B overlap,4096B tail; overrun retained без чтения всего raw в память и без fabricated summary/hash. Readback exception не выдаётся за успешную unit acceptance. RawCapture full drain/fallback retained; незавершённый capture остаётся failed. Реальные fault paths не инъецировались.

## Сохранность scope

Exact string comparison с original unit-v2 после снятия единственного outer4-space indentation подтвердил seed inventory950B и prepare function3039B (до следующего blank separator) без изменения bytes: SHA `b4d67c005b58d18ec9e6b4c87aa1f86e372567fc70e35523859fa942150cc40d` и `9811cc1fbf1e61f884bd396183bc4cf01ab5301db82ee28124b65d40b97f5f88`. Сохраняются13nodes,10dirs/2links/1zero regular,57B links, ownership/modes/canonical backing guards. Все v1 script/plan hashes независимо проверены как прежние.

Child argv/perms/env не расширены: static fmt/lint только2paths; E1 sole test + adapter + ownedTMP read, TMP-only write, no run/env/net/FFI, cached-only/no-remote/no-npm/no-config. Новый Git — только parent metadata guard. Helper exact checked-buffer→ModuleType loading и pinned runtime/config сохранены; никаких target imports в добавленном code нет. CPP→formatter receipt→independent format-only review→fresh final source hashes цепочка retained, не привязывает final SHA навсегда к unformatted candidate.

План сохраняет FORMAT1/LINT1 max20s1CPU1GiB32MiBTMP2MiBraw, E1once120s1CPU1GiB8MiBTMP1MiBraw, expected74 и ровно1newunit; identities те же, v2 не разрешает новые attempts. Прежние unit2/2, E1 1/1, actual2/2 и milestone81→87 ceiling сохранены. Extra RED, actual/native/science/C08/CI в этот review не включены. Число74 здесь — retained source contract, execution/discovery не проводились.

Работа состояла из чтения, hashes, read-only Git metadata и inert string comparison; подготовленные scripts/helpers/runtime/target/tools/tests не выполнялись и не импортировались. Compiler/parser/typecheck/selftest отсутствуют. Записаны только этот отдельный report и identity; Root/source/CP/original review не менялись. Conservative logical source-read≤1MiB при cap4MiB, wall<600s; report+identity<128KiB. CPU/RSS/physical I/O не измерялись, отсутствие измерений не обозначено0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 current HEAD binding исправлен | Actual read-only Git в readiness/prelaunch/terminal; late-bound READY | Не запуск prepared harness | сохранить |
| R2 RSS unknown отделён от measured0 | Nullable peak, positive completed count, failed count/status/errors | Sampling не доказывает transient peak | сохранить |
| R3 consumed failed attempt имеет best-effort receipt path | Outer envelope, caught readback,2receipt targets+stderr fallback | Полный I/O отказ не имеет durability guarantee | сохранить |
| Seed/perms/budgets/74contract retained | Exact text comparison и argv/plan source review | Unit/tools не выполнялись | сохранить |
| Runtime correctness и GREEN установлены | Executions0 | Требуется отдельный Root readiness/разрешённый bounded запуск | данных недостаточно |

**PASS только source corrections; STOP_FOR_ROOT_READINESS.**
