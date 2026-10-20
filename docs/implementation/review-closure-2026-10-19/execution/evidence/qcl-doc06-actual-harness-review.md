# DOC06 actual nine-source export/harness: независимая статическая проверка

2026-10-20. Verdict: **PASS_SOURCE_HARNESS_WITH_ROOT_BINDING_PREREQUISITES** для
предложенного trusted-local engineering scope. Этот verdict не является READY,
не разрешает исполнение и не принимает actual projection или её смысл.

Первичный вопрос до чтения авторского отчёта: связывает ли цепочка результаты с
девятью selected Root sources, не исполняя target и не утверждая native acceptance?
Ответ: экспорт связывает Git commit с raw bytes; adapter связывает supplied receipt
с прочитанными bytes и facts. Для сквозной цепочки между этими двумя частями
нужна явно предусмотренная планом Root проверка export→READY. Сам launcher эту
внешнюю часть доказательства полностью не перепроверяет; условия ниже обязательны.

## Исходная identity и граница

Проверен selected managed Root
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`. Default cwd рецензента имел другой
HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; он не принят за selected source.
В selected Root modified coordinator JSON и untracked coordinator/evidence files;
проверяемый adapter имеет требуемый SHA. Working source submodules не использован
как authority. `git submodule status --recursive` без `+`/`-` и committed
`git ls-tree -rz 2bb05d3… components` независимо дали восемь gitlinks:

| Component | Selected commit |
| --- | --- |
| QCLNEGF.jl | 9f4a96d032ad868ec010ce92d915bb81087c8d92 |
| QCLNEGFRunner.jl | fefaa27f194bfddf85dd51a0e255beef2218c06d |
| qcl-negf-aiida | d8f8092ca1c76523d85384b4bac8198d8bfa736b |
| qcl-negf-contracts | f4009c933183d8537e289d2fa5fa898defd2d9b5 |
| qcl-negf-platform | f729e2681224d6537538179ab760fefefd575003 |
| qcl-negf-portal | 2622de5ee28b454ff4f809cc3dd00c1e5bc2295d |
| qcl-negf-research | 3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731 |
| qcl-negf-results | de70638a982f91b7e125ab1cfc70a2daef2a656d |

Фактические SHA256 совпали с dispatch:

| Input | SHA256 |
| --- | --- |
| actual-local-run-v1.py | dd12fd9383130fd77039049114a02ff513ff6eb7d1caac6bfb34d96a94ee0e61 |
| actual-source-prep-v1.py | d4b824dd2d2f5781a5853e6db35f53ad37b560fa2a9d94bab9272f85887b2cec |
| actual-engineering-plan-v1.json | 1916f0b4aa51d2a835525aa159e5411fb80f23c97233f8bba92bd1b8b223f18c |
| Root ops/docs/static-slice.ts | 3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b |
| qcl-local-julia-guard-v2.py | e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f |
| qcl-owned-temp-sampler-v2.py | 16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e |

Прочитаны accepted design (`34b80d4a…fb2e8`), его PASS_SOURCE_CP_DESIGN identity,
pointer erratum (`a2d28d0d…2475`) и applied binding. Старые selected revisions
в design являются историческим контекстом, не подменяют current Root gitlinks.
Прочитан final synthetic56 review identity: exact adapter совпадает, но тот
review явно не принимает real nine-source binding, determinism или meaning.

Новый `/tmp/qcl-DOC06-ACTUAL-2bb05d3-v1` на проверке отсутствует.
`/tmp/qcl-DOC06-ACTUAL-PREP-1` существует; он не изменялся и не использован
как текущий snapshot. Сначала изучены первичные scripts/plan/adapter/helper
sources; авторский harness report прочитан после независимого прохода.

## Что установлено статически

1. `actual-source-prep-v1.py:22–65` резервирует новый namespace без reuse,
   требует отдельный свежий READY_SOURCE_PREPARATION с exact script/current
   Root identity, получает gitlinks из committed tree, затем выполняет только
   `ls-tree`, `cat-file -s`, `cat-file blob` для девяти фиксированных paths.
   Проверяет mode100644/blob, размеры≤128KiB и сумму≤512KiB. Git имеет cleared
   explicit environment, OPTIONAL_LOCKS=0, NO_REPLACE_OBJECTS=1, отключённые
   system/global config и конечные timeouts. Нет checkout, update, target import,
   tree discovery вне fixed list или исполнения target source.
2. Независимый `ls-tree` selected component commits подтвердил все девять
   regular blobs. Packaged и Contracts schema имеют один Git blob
   `ae67f4da237a15f8b3ce1f04c2f79096c3e88d9e`. Их raw SHA/размеры этот review
   не экспортировал: это будущая обязанность source-preparation evidence.
3. Graph строится заново из восьми gitlinks. Receipt+blob OIDs+raw SHA/bytes
   являются производным ephemeral evidence; второго maintained revision lock нет.
4. `actual-local-run-v1.py:28–50` проверяет graph revision, восемь unique owners,
   ровно девять ordered paths, owner/revision, raw SHA/размер, aggregate и полную
   inventory snapshot без symlinks. Проверки повторяются в finally.
5. Полностью прочитан exact adapter. Target файлы проходят bounded raw reads,
   strict UTF-8 и hash verification, затем текстовую projection/built-in JSON
   data parse. Нет static/dynamic import target, eval, Function, WebAssembly,
   fetch, subprocess/Command или dlopen. Единственный import token —
   `import.meta.main`. Julia/YAML/config methods не исполняются. Runtime module
   loader остаётся отдельной причиной обязательного exact adapter pin/review.
6. `actual-local-run-v1.py:20–25` проверяет helper buffer SHA и выполняет именно
   этот buffer через compile/exec в fresh non-main ModuleType. Loader/pyc cache
   этих helpers не используется. Их import-time code — stdlib imports/constants/
   definitions; main guard capture helper не запускается. Это trusted tooling,
   а не target execution.
7. `:104–105` задаёт exact cleared child environment и фиксированные Deno flags.
   Read grants: adapter, snapshot, input receipt, owned TMP. Write: owned TMP.
   Нет allow-env/run/net/ffi; no-config/no-lock/cached-only/no-npm/no-remote/
   no-prompt. Runtime path+SHA pinned; сам binary в этом review не читался,
   не запускался и не проверялся version command.
8. Только A1/A2, exclusive permanent attempt mkdir до READY checks; A2 требует
   отдельный READY, prior completed-partial A1 receipt и exact hash. Дочерний
   product call ровно один в каждом attempt; automatic third call/retry нет.
9. RawCapture имеет единственного непрерывного byte reader, обрабатывает partial
   writes, drain в finally; fallback сохраняет raw при failed collector start.
   Failed/pending artifacts и original logs не удаляются. Overshoot не
   обрезается и не становится capped success. Capture failure не проходит ok.
10. Prelaunch/loop/terminal/final observations участвуют в reason predicate.
    Affinity1/RLIMIT_CPU120, sampled RSS1GiB/TMP16MiB, wall120 и raw threshold
    с finite termination/drain paths присутствуют. RSS/TMP являются sampling,
    не hard quotas; transient peak/hostile namespace/escaped-descendant sandbox
    не доказаны и не заявлены. Python guard и runtime startup не становятся
    научным или native target evidence.
11. Terminal success требует exit0, JSON stdout exactly status=partial,
    complete capture, отсутствие guard reason, ровно facts.json+source-receipt.json,
    bounded JSON и совпадение facts SHA/bytes с output receipt. Название результата
    complete_partial_projection честно: neither meaning nor native acceptance.
    Сравнение полных bytes A1/A2 и independent meaning readback — отдельный шаг.

## Обязательные Root prerequisites и дешёвое усиление

**R1 — внешний export→READY bridge.** `actual-local-run-v1.py:88,96–97`
хеширует preparation.json и отдельно input receipt, но не читает поля
preparation.json для сопоставления с bind_inputs(). Поэтому связанная пара
не удостоверяется самим launcher. В accepted trusted Root scope это покрывает
явное требование плана: Root проверяет exported graph/nine sources/preparation
receipt перед READY. Конкретная Root проверка должна установить одновременно:

- preparation.root_revision равен 2bb05d3…;
- preparation.graph_sha256 равен bind_inputs.graph_sha256;
- preparation.input_receipt_sha256 равен bind_inputs.input_receipt_sha256;
- preparation files/aggregate_source_bytes равны фактическим nine-source records;
- preparation script SHA и отдельный READY_SOURCE_PREPARATION совпадают с reviewed
  exact exporter и разрешённой подготовкой; prepared failure receipt отсутствует.

Без этих сверок этот verdict не устанавливает end-to-end selected Git binding.
Самый дешёвый fail-closed code hardening — bounded parse preparation.json и
сравнение этих полей в bind_inputs/prelaunch. Нового product call для этого нет.

**R2 — A1/A2 source continuity.** `actual-local-run-v1.py:92–97` не сравнивает
новый before с prior.before/prior.after. Поэтому same receipt/snapshot из плана
остаётся Root sequencing prerequisite. Перед READY A2 нужно потребовать
полное равенство A1.before=A1.after=current bind_inputs (graph/receipt/files/
aggregate), затем после A2 проверить аналогично. Дешёвое усиление — это же
равенство в prelaunch A2. Равенство facts позже также обязательно, но само
по себе source continuity или meaning не доказывает.

Это не hostile-namespace finding и не требование нового security sandbox.
Статически воспроизводимый пробел: supplied graph+receipt могут оставаться
внутренне согласованными, а source manifest/preparation pair либо A1/A2 pair
не сравниваются указанными строками. Root обязан замкнуть эту цепь либо
поручить описанное малое усиление до исполнения. В остальном блокирующих
finding для proposed trusted-local source-only scope не найдено.

## Выполненные действия и STOP

Только bounded чтение sources/документов, Git metadata/object-tree reads,
sha256sum и запись этого review/identity. Exporter, harness, Python parser,
helpers, Deno, target/native/tests/network не исполнялись. Git writes,
product/checkpoint changes, source export, marker/sentinel/control execution
отсутствуют. Actual facts ещё нет. Консервативный logical source read upper
bound 1MiB (в пределах2MiB); wall<10min; CPU/RSS/physical I/O не измерялись.
Report существенно меньше96KiB. Подагенты не использованы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact exporter может связать selected Git с девятью raw sources | current Root gitlinks, selected regular blob metadata, exporter:31–65 | Export не выполнялся; Root preparation READY нужен отдельно | сохранить |
| Harness автоматически доказывает всю export→projection цепь | Проверки receipt в :28–50; separate preparation hash в :88 | R1 cross-binding остаётся обязательной Root сверкой | дополнительно измерить |
| A1/A2 используют один source snapshot | fixed namespace, permanent identities, prior receipt gate | R2 equality нужно проверить Root либо добавить в guard | дополнительно измерить |
| Target остаётся inert bytes, native acceptance не объявлена | Полный exact adapter/helper source review и explicit grants | Runtime/source execution в этом review0; это статическое свидетельство | сохранить |
| Actual output deterministic и правильно описывает owning sources | Пока нет A1/A2 raw/facts | Нужны полный bytes comparison и independent meaning review | данных недостаточно |
| Scientific/render/native/full release готовы | Нет соответствующих evidence/gates | Synthetic56 и harness source review этого не устанавливают | данных недостаточно |

STOP: review/identity only; execution/count/READY и дальнейшая приёмка принадлежат Root.
