# DEV18 final CP-CODE: PASS в согласованной engineering scope

Итог: **PASS** для generic runtime checkpoint durability/failclosed implementation и согласованного targeted fixture packet. Блокирующих замечаний не осталось. Единственное finding предыдущего CP-CODE — literal YAML-кодировка H01 — исправлено ровно согласованной локальной правкой; production source не менялся. Ни native/NFS/power-loss durability, ни scientific acceptance, ни S1 этим решением не утверждаются.

Это read-only recheck exact delta и уже полученного root runtime receipt. Рецензент не запускал Julia, imports, тесты, solver, сборки или Git и не менял исходники. Создан только этот final review artifact. Полный source-first protocol/reader/55-cell analysis сохранён в `/tmp/qcl-dev18-code-review.md`, SHA256 `58dbdae4206c2a26a2db876642336d570961bdfac69b0f3b54f00522e7e964fc`; он остаётся историческим pendingGREEN2 review, а этот документ закрывает его runtime/finding gates.

## Независимо сверённые hashes

Root worktree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, component `components/QCLNEGFRunner.jl`.

| Артефакт | SHA256 |
| --- | --- |
| Production `src/infrastructure/runtime/filesystem_repository.jl` | `44a1d6e907b985bdcd5fb89b73a50ca434ab6209462564d63936562317521849` |
| Corrected `test/infrastructure/runtime_checkpoint_durability_faults.jl` | `db32630942eace2429ca7014df4caec66044fca2cd643386617a2c0413b1c69c` |
| Old frozen fixture `/tmp/qcl-dev18-h01-before.jl` | `4e74a26ab5caf80e12ddae3e85ca4b3bb793081686bd0bbaeeb0fa35028ac429` |
| Existing integrity fixture | `a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef` |
| Unchanged `src/infrastructure/persistence/atomic_files.jl` | `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4` |
| Unchanged accepted owning durability doc | `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc` |
| `/tmp/qcl-dev18-h01-fix.patch` | `e47ac818f7e4700a613c7048f0c7a6d2e093cf8a7a3be592381ef908764b54c3` |
| `/tmp/qcl-dev18-full-h01-fixed.patch` | `7defab1387e58b52e36eb1f971f91e10b0195fc78869ea281ad372aec64f99bc` |
| `/tmp/qcl-dev18-h01-fix-report.md` | `4ba2cc21212e94a1b986b24a6328df782f613ac4f54bacfc3d2931aa10b9c701` |
| GREEN2 `/tmp/qcl-DEV18-GREEN-2/receipt.json` | `b8f811d1c3c802f1803c4cbd8cb31c82e3bdab6ac2fed80224a5ad33fa5fe7e1` |
| GREEN2 `/tmp/qcl-DEV18-GREEN-2/original.log` | `0b46b9399977964069948db2a2394159ca336950723817ab247b8044a36f9456` |

## Exact delta и закрытие finding

Прямой `diff -u` old frozen fixture против actual corrected fixture показывает единственный hunk на344–350: H01 `complete(r,1,1,NEW)` заменён `complete(r,1,1,"state: \"new\"\n")` и добавлены два поясняющих комментария. Никакие другие строки fixture не менялись. Source bytes production/old fixture/atomic/doc равны прежним проверенным hashes.

H01 использует built-in `YamlCheckpointCodec` с `Dict("state"=>"new")`, поэтому quoted string literal отражает codec serialization. Остальные54cells по-прежнему используют прежние raw literals там, где запись делает callback. Expected bytes не вычисляются writer-ом и не берутся из target file. Общие exact byte и independently computed SHA assertions в `complete` сохранены. Набор из55cells, tolerances, physical/model/discretization assumptions и source barriers не изменены. Finding H01 закрыто.

## Фактический GREEN2

Независимо прочитаны complete original log и receipt; их fixture hashes совпадают с actual source. Log также явно содержит production repository SHA `44a1d6…` и выбранный реальный composition module SHA `ad8b0fe43df8d21765d91dbfcbef7cbbc498453b0d1b41a8193c0db8d2a99efe`.

| Packet | Фактический denominator и outcome |
| --- | --- |
| `Runtime checkpoint publication faults` | **3199/3199 assertions PASS**,55cells; log содержит55-element cells/trees, independently найдены55 retained `cell.txt` |
| `YAML repository, provenance, spans, and checkpoint integrity` | **15/15 assertions PASS**; отдельный summary подтверждает, что второй include действительно исполнился |
| Общий процесс | **3214/3214 assertions**, exit0, guard/error/stop/overrun отсутствуют, raw capture complete |

Измерение root: wall27.7s, sampled peak process-tree RSS973373440B, sampled owned TMP290020B, raw output1170B. Receipt фиксирует `--threads=1`, `--check-bounds=yes`, selected Julia1.13.0/prepared offline environment, CPU affinity1, wall cap120s, RSS cap2GiB, TMP cap16MiB и output cap2MiB. Source-selected new fixture и existing owning fixture исполнились одним процессом; это не full CI или native acceptance.

GREEN1 остаётся историческим failed3197/2; он не переписан в pass, а existing fixture в нём по-прежнему not-run. GREEN2 — отдельная attempt. По переданному root grant audit это третья invocation total: первоначальные две плюс одно конечное explicit human extension после различающей H01 correction; рецензент не расходовал runtime budget и не делал автоматических retries. Проверка разрешения на extension основана на trusted root handoff; log доказывает фактическое исполнение, а не сам по себе пользовательскую авторизацию.

## Поддержанные выводы и границы

Полный production review остаётся применим, поскольку production hash не изменился: closed/chmod/hash/file-fsync payload → single same-directory rename → complete ancestry fsync → closed/chmod/file-fsync metadata → metadata rename → final directory fsync → canonical/identity/size/SHA readback → reference; serialized object writer и reentry rejection; raw temporaries/orphans/previous verified bytes сохраняются; latest reader failclosed без repair/fallback. Optional expected_attempt проверяется до payload decode, default cross-attempt resume сохранён. Scientific point artifact protocol, wire schema и criteria не менялись.

Гарантия условна для поддерживаемого local POSIX fsync/rename и закрытого codec writer, trusted non-symlink/stable ancestry и единственного writer между object/process/machine. Synthetic exception cells измеряют live-byte integrity и ordering; они не моделируют dirty-page loss, NFS cache/device failure или real power loss. Shared YAML/SHA library — ограничение независимого oracle. Resource sampling50ms не доказывает transient peak/hard quota; пути вне owned TMPDIR не измерены. Root HEAD/source integration, publication и full release acceptance остаются отдельными gates.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Scoped production durability/failclosed protocol принят | source SHA44a1d6…, source-first CP-CODE и GREEN2 3199/3199 | conditional local POSIX; synthetic faults | сохранить |
| H01 independent literal finding устранено без ослабления критерия | единственный diff hunk; new fixture db326…; exact byte/hash assertions сохранены | codec-specific literal | сохранить |
| Existing provenance/integrity fixture прошла | separate GREEN2 summary15/15, unchanged a672… | targeted fixture, не full suite | сохранить |
| Native/NFS/device/power-loss durability измерена | такого receipt нет | runtime tests не real crash | данных недостаточно |
| Scientific/model/numerical acceptance или S1 закрыты | scientific solve отсутствует | generic engineering storage scope | данных недостаточно |

STOP. Final CP-CODE PASS ограничен этим exact source/test packet; дополнительных executions, reruns или изменений не требуется.
