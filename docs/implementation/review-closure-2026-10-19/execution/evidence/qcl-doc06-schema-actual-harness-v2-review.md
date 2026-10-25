# DOC06 corrected actual9 v2: независимый high source review

2026-10-20. Verdict: **PASS_SOURCE_ACTUAL_PACKET_V2**. В проверенном тексте preparation/launcher и finite plan блокирующих замечаний не найдено. Verdict относится к source controls при обязательных независимых Root R1/R2 и свежем Root READY. **Это не execution grant и не приёмка actual meaning**. Status: **STOP_FOR_ROOT_FRESH_READY_R1_R2**.

Подготовленные scripts/helpers/runtime/adapter не исполнялись, не импортировались и не компилировались; target parser, formatter, linter, unit, Deno/Julia/native/network/CI/solver отсутствуют. Читались metadata/Git source blobs/старые artifacts; новый snapshot/export не создан. Записаны только этот report и identity; Root source/CP/guard/old attempts не менялись.

## Exact source packet

| Артефакт | Bytes | SHA256 |
| --- | --- | --- |
| actual-plan-v2.json | 3962 | 1f0f73b9216aa097a1b86ba455192820b6ebb872a8d7d9d57e1b5b682ccecceb |
| actual-local-run-v2.py | 21737 | 322c38d71f67c037e780e0f811b8ea67cd863d61f9a1bf7690391ffdaf3976f8 |
| actual-preparation-v2.py | 11134 | 55dba3288b2c1e8fbf84f6f03d2cda171d0466107d60db26fbd4746e175bd9b0 |
| actual-harness-report-v2.md | 11082 | 36b120e4da5497f5201a0a6a835c26da55c514492c26bbc64bb210d5ea588fc5 |
| actual-harness-identity-v2.json | 2953 | 4e797dc2c21279f616b5681d2fa269d36377cdba8cfcdbf45f4ea79d340971fb |

Все paths имеют prefix `/tmp/qcl-doc06-schema-`; hashes/размеры независимо пересчитаны, scripts полностью прочитаны как inert text. Shared authority/READY/persist source section preparation и launcher byte-equal при textual comparison. Runtime binary не читался в source budget; его pinned SHA проверяется будущим guard streaming64KiB.

Фактический Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` read-only `git rev-parse HEAD`: `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`. HEAD/status/submodule status/tree прочитаны с GIT_OPTIONAL_LOCKS=0. В status modified checkpoint/census и untracked publication/evidence; owning adapter/tests чисты и имеют exact hashes `a852318af5105aaf224913e2264342c4349cb0ed70991842f00ab78e4d6c4b72` / `45febb3ccfdd9d641447d5cec6e26bbfc6c9b97f188c2e9a620142794c1a3b31`. Все8initialized submodules совпадают с gitlinks без `+`/`U`.

## Git authority,9inert source blobs и continuity

Оба scripts `graph_objects():25–44` получают все8gitlinks из fixed Root `ls-tree -rz <HEAD> components`, проверяют160000/commit,40hex и уникальность8paths. Selected9PATHS принадлежат fixed owners Runner/Contracts/Core; object metadata требует committed100644blob, размер1…128KiB и aggregate≤512KiB. Bytes читаются `cat-file blob <gitlink>:<path>`, а не из component working files. Нет вручную поддерживаемого списка component revisions.

Administrative Git env фиксирует GIT_OPTIONAL_LOCKS=0/GIT_NO_REPLACE_OBJECTS=1 и отключает global/system config; remaining wall ограничивает каждый read-only call. Начальный/конечный actual HEAD должен быть exact c5ef. Exact binding`:45–61` сравнивает canonical derived graph, manifest root format/source-graph hash/files entries, все9exported bytes с committed blobs, отсутствие symlinks и отсутствие лишних snapshot files. Manifest files имеют fixed order и owner/revision/SHA/bytes. Directory inventory не заявляет hostile namespace protection; эти данные остаются trusted owned snapshot, у Deno нет права писать в него.

В этом review независимыми read-only Git calls, **без экспорта**, дополнительно проверена continuity old `/tmp/qcl-DOC06-ACTUAL-2bb05d3-v1/snapshot`:

- Все9 current gitlink revisions совпали с old manifest revisions.
- Каждый из9current Git blobs byte-equal соответствующему old frozen source; SHA/size равны old manifest.
- Aggregate245338B подтверждён чтением, не принят из report как данность.

Это подтверждает неизменность selected payload для planned comparison. Новый Root graph имеет другую Root revision и должен быть вновь derived; старые graph/preparation hashes нельзя перенести как new provenance. Проверка старых bytes здесь **не заменяет** Root R1 над будущим new export: new namespace ещё отсутствовал при review.

## Обязательные Root R1/R2

Preparation permanently reserves только `/tmp/qcl-DOC06-ACTUAL-c5ef91f-schemafix-v2`; ID DOC06-SCHEMA-ACTUAL-PREP-1, max1export. `main():115–128` пишет readonly source files/graph/manifest, перечитывает Git/snapshot binding и source/plan/READY, затем сохраняет preparation.json со status `prepared_exact_Git_R1_candidate`. Это корректно названо exporter evidence, не independent acceptance.

**R1 остаётся действием Root:** независимо сопоставить new exported graph/manifest/все9bytes и hashes с selected Root gitlinks/Git blobs и проверить preparation/phase receipt outcome. Затем создать свой `exact_Git_R1_verified` readback JSON с full binding и preparation SHA; ссылку и SHA включить в fresh A1 READY. Product guard`:230–234` требует этот record, одновременно повторяя exact Git binding. Нельзя выдавать R1 путём вызова той же preparation-функции и назвать это независимым oracle.

**R2 остаётся действием Root:** после A1 проверить exit/receipt/persistence errors/failed-receipt и before=after=R1 binding; только затем допускать A2. Launcher terminal`:197–208` повторяет actual HEAD, source/runtime/harness/READY/plan/helper hashes и exact9binding; after должен равняться before. A2`:235–238` дополнительно требует pinned A1 receipt с guarded_pass=true/complete_partial_projection и before=after=current A2before. A2after снова равен before. Fresh A2 READY.prior_receipt_sha256 делает continuity явной.

Эти guard checks не отменяют отдельного Root readback/admission. В частности Root должен учитывать failed exit/fallback receipt даже при доступном partial primary receipt; одно ранее записанное поле guarded_pass не заменяет reconciliation этапа. Ни failed A1, ни нарушенная provenance не открывают A2. Future output equality и смысл M1/M2/M3 проверяются отдельно; byte equality сама не semantic acceptance.

## Immutable helpers, clean permissions и bounded failures

Pinned helpers независимо перехешированы: capture `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`, sampler `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e`. `load_trusted():103–107` использует bounded exact bytes→SHA→compile/exec того же buffer в fresh non-main ModuleType, без cached pyc/importlib. Эти execution statements reviewer не исполнял.

READY требует accepted high source-review ref, exact stage/root/plan/harness/evidence map/limits и age≤300s. Adapter/test hashes связаны с accepted CPP2706…, format review0130… и outcome reviewee8620…; все3references/hash подтверждены. Before/after source/runtime/helper checks сохранены.

Child env фиксирован заново; HOME/cache/scratch только в own attempt TMP, updates disabled и numerical/Rayon threads1. Deno command запускает только trusted Root adapter с no-config/no-lock/cached-only/no-npm/no-remote/no-prompt; read только adapter+snapshot+input receipt+ownTMP; write только ownTMP; no env/run/net/FFI. Selected9Julia/YAML/JSON/Markdown strings передаются как inert data, не target imports. Нет install/Nix/bootstrap/CLI task/all-tests обходов.

RSS nullable, postspawn+loop/live-terminal samples, valid count≥1, любая ошибка/missingVmRSS fail NotCapable. Missing field error теперь сохраняет available status snapshot и timestamp; это будущая telemetry, не доказательство причины old E1. TMP nullable с prelaunch/loop/terminal probes и actual16MiB threshold. Parent/child affinity1 и finite CPU/wall controls есть; RSS/TMP остаются sampling lower bounds без transient hard quota.

Permanent attempt folders создаются exclusive, не удаляются/переиспользуются. После reservation outer protection охватывает setup/log/capture/drain/finish/readback/terminal/persist. Finalization actions independently guarded; unknown raw/hash/observations не подставляются0. RawCapture/fallback сохраняет original bytes; raw stop headroom128KiB; >1MiB retained без summary/hash и с failure. Within cap raw должен быть exact JSON status partial плюс exit0; оба32KiB output artifacts должны быть bounded JSON и source-receipt output SHA/bytes должны соответствовать facts. Это complete partial engineering projection, не проверка содержательного смысла.

Persist пробует exclusive receipt.json и failed-receipt.json, после I/O ошибки меняет guarded_pass=false и возвращает failure даже если fallback записан; при невозможной persistence выдаёт stderr/minimal consumed-identity fallback. Preparation/child final errors не становятся successful retry или обещанием абсолютной durability. Runtime/fault injection не проводились.

## Finite budget и сохранённые отрицательные evidence

Новый packet:1preparation≤120s1CPU, source≤512KiB/per-file128KiB, manifest16KiB/preparation32KiB; ровно2product calls A1/A2, каждый≤120s1CPU/1GiBsampledRSS/16MiBTMP/1MiBraw. Namespaces/IDs не alias старых exhausted attempts. План не пишет CP/census: **Root отдельно обеспечивает общий ceiling88**, свежую admission и списание всех фаз; локальные max2 не являются новым общим budget grant.

Unit74 software evidence остаётся принято с ограничениями; E1 resource guard29valid+1unknown остаётся failed. Никаких unit/source-tools/CI/solver/C08 reruns этот packet/review не разрешает.

Old namespace не менялся. Его preparation/input/graph hashes сохранены как `03db672d25120747f86469e37a1685f6dfff8bed64199b6a619b5296b8adf5b8` / `971fc29af70d409e64b37f2e331b03596e92736a2e3a993bad22e9d802bffd1a` / `b7244ee91167b688e598efea33ba9620772c974264920d7e368ec87de4d939e1`. Old A1/A2 original.log оба SHA `ff602a8401c76f68f448a0ae58b37281211b6ed20427e1cdbf0603207c92b301`; receipts `d525dd33a202c17436e85280187d692ff4297da7ab3c11ff96ed96a854fbd19f` / `6af221c17e590bc24352a016cec9da71204adf8720c76dd3a9dc1bb0710a0755` зафиксированы чтением. Старые negative meaning/provenance не переименованы в success corrected source.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Source packet реализует bounded exact9 Git export | Fixed Root/tree/owners/blobs, byte inventory и hashes | New export не создавался | сохранить |
| Selected payload сопоставим со старым snapshot | Независимо все9current Git blobs=old frozen bytes,245338B | Новый graph/manifest ещё требуют Root R1 | сохранить |
| R1/R2 обязательны и выполнимы | Readback contract+guard before/after+prior A1 chain | Root должен выполнить независимые checks/admission | сохранить |
| Guards/perms/failed receipts конечны и честны | Nullable sampling, bounded raw/artifacts, outer/fallback source review | Без runtime/fault injection/hard quota guarantee | сохранить |
| Actual corrected meaning принят | Product executions0 | Нужен отдельный bounded запуск и независимый meaning review | данных недостаточно |
| E1 resource/CI/science gates закрыты | Old E1 failed; этих calls нет | Ни source agreement, ни new grant их не закрывают | данных недостаточно |

Review budget: conservative logical reads≤2MiB при cap4MiB (включая9Git245338B+old245338B), wall<720s, report+identity<128KiB;1CPU/1GiB. Physical CPU/RSS/I/O reviewer не измерялись. Prepared-code executions0, snapshot exports0, Root/CP writes0.

**PASS_SOURCE_ACTUAL_PACKET_V2; STOP_FOR_ROOT_FRESH_READY_R1_R2.**
