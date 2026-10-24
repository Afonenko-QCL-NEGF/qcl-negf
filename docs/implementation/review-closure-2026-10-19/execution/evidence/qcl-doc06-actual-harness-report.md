# DOC06 actual selected-source — подготовка harness

2026-10-20. Статус: **proposed, not executed**. Подготовлены source exporter,
план двух отдельных DEV CLI projections и launcher; требуется независимый high
review и затем отдельные Root READY. Этот отчёт — авторская source-проверка,
не независимый verdict и не разрешение запуска.

Наблюдаемый managed Root HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`.
`GIT_OPTIONAL_LOCKS=0 git status --short` показывает два изменённых coordinator
JSON и четыре untracked coordinator/evidence файла. Все восемь submodules в
`git submodule status --recursive` совпадают с выбранными gitlinks без `+`/`-`.
Их checkout files не являются входом exporter: authority — committed Root tree.
Прочитаны architecture, accepted DOC06 design и final synthetic56 review;
новый scope не наследует runtime/render/native/scientific acceptance.

Старый `/tmp/qcl-DOC06-ACTUAL-PREP-1` прочитан только как существующее evidence:
его graph имеет Root `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, Runner1acc,
Contracts d791 и Coree431. Он не current, не изменялся и не будет входом новых
calls. Новый namespace `/tmp/qcl-DOC06-ACTUAL-2bb05d3-v1` пока **не создан**.

Подготовленные файлы:

- `/tmp/qcl-doc06-actual-source-prep-v1.py`: отдельный readonly Git exporter;
  после отдельного review + Root `READY_SOURCE_PREPARATION` получает восемь
  gitlinks из exact Root tree и только девять allowlisted blobs из selected
  component object stores. Каждому предшествуют mode/type/size проверки;
  file≤128KiB, aggregate≤512KiB. Никакого чтения component working source,
  checkout/submodule update/target import или выполнения source нет.
  Derived graph + input receipt + preparation evidence — ephemeral evidence,
  а не вручную сопровождаемый lock. Namespace и failed evidence сохраняются.
- `/tmp/qcl-doc06-actual-local-run-v1.py`: только A1/A2, permanent reservation
  до READY/guard проверок, Root sole execution/count writer. A2 требует новую
  READY, успешный complete-partial receipt A1 и его exact hash. Любая неудача
  потребляет identity; automatic retry отсутствует.
- `/tmp/qcl-doc06-actual-engineering-plan-v1.json`: конечный порядок, scope,
  exact pinning, readiness schema, бюджеты, границы и дальнейший meaning review.

Точные SHA/размеры находятся в companion identity. CLI launcher проверяет
plan/harness/preparation/input-receipt hashes, источник до/после, adapter до/после,
точный pinned runtime перед Popen. Runtime binary во время этой подготовки не
читался и не запускался; его pin взят из ранее reviewed engineering evidence.
Actual adapter SHA проверен чтением:
`3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`.

## API, module loader и cache

У actual `ops/docs/static-slice.ts:1063–1154` API сначала проверяет absolute paths,
overlap, real directories/no symlinks, fresh output, bounded receipt и ровно9
known paths. Перед чтением проверяются размеры; затем raw SHA/length и strict
UTF-8. `facts.json`/output receipt≤32KiB, diagnostics≤8KiB; facts публикуются
после bounded projection через pending file. Refusal остаётся refusal.
`:1156–1177` main требует ровно6 argv, только три unique flags `--snapshot`,
`--source-receipt`, `--out`; console JSON status и exit2 для refused, иначе0.
Supported execution возвращает **partial**, что ожидается launcher, а не pass
всех semantics. Source receipt сообщает внешний commit-to-bytes limitation.

Проверен текстовый поиск по всему actual adapter: единственный `import` —
`import.meta.main`; нет static/dynamic module imports, eval, Function,
WebAssembly, fetch, Command или dlopen. Это source observation; Deno module
loader читает script независимо от runtime read grants, поэтому source identity
и review обязательны. Existing final high review остаётся evidence полного
unchanged adapter; здесь отдельно прочитаны актуальные API/main guards.
Target `.jl/.json/.yaml/.md` передаются только bytes. Built-in JSON.parse
разбирает данные; Julia/Python target imports и package loading отсутствуют.

Trusted capture/sampler загружаются только из bounded verified sourcebuffer:
SHA → `compile(buffer, exact_path, 'exec')` → `exec` в свежем `ModuleType` с
non-main name. Нет `SourceFileLoader`, importlib, `.pyc` lookup/creation для этих
источников. Проверены текущие helper SHA `e88ca8…be3f` и sampler `16a038…b12e`;
их import-time source состоит из stdlib imports/constants/definitions, их
`__main__` guard не выполняется. Capture buffer — exact verified bytes;
проверка файла отдельно от последующего loader/cache больше не применяется.

## Proposed bounds и результат

Один Root call запускает один Deno CLI `run`, no-config/no-lock/cached-only/
no-npm/no-remote/no-prompt. Read: exact adapter + snapshot + input receipt + own
TMP. Write: own TMP. Нет allow-env/run/net/ffi. Popen env — exact fresh map,
не filtered inherited environment; HOME/DENO_DIR/TMPDIR разделены внутри own TMP.

На call: wall120s, affinity1, RLIMIT_CPU120s, sampled process-tree RSS1GiB,
sampled own regular logical TMP16MiB, raw1MiB со stop threshold896KiB. Сохраняются
original raw, guard errors, failed/partial outputs, receipt и sampled observations
prelaunch/loop/terminal/final; terminal samples участвуют в refusal predicate.
Raw capture дренируется, overshoot сохраняется и не выдаётся за capped success.
Каждый facts/receipt hash и размер записываются после complete capture и проверки
ровно двух output files. CLI status=partial, exit0 и guard success дают только
`complete_partial_projection`; не научную приёмку и не доказательство смысла.

RSS/TMP — sampling, не hard cgroup/quota, transient peak, physical allocation
или hostile namespace proof. Process-group kill — local cleanup, не escaped
process sandbox proof. ROOT READY — текущий trusted coordinator handoff,
а не самостоятельная криптографическая подпись или production admission.

После обоих calls отдельно сравнить **полные facts bytes**, затем проверить
meaning по exact owning docs/schema/API и все public refs/unknown origins.
План намеренно не превращает одинаковые bytes/exit0 в доказательство смысла.
No absolute/private assigning filenames/secrets в public facts требуется
проверить при этом readback. Actual source extraction ещё не произведена.

Подготовка выполнила только bounded source/metadata reads, SHA и `ast.parse`
двух созданных Python sources как inert синтаксиса. Exporter, launcher, trusted
helper code, Deno, target code/parsers, tests/native/build/science/network не
исполнялись. Product/CP/Git writes отсутствуют. Новых subprocess target calls0;
первоначальные unit attempts и C08 не переоткрыты. Envelope15min/1CPU/1GiB,
source read≤3MiB, outputs≤160KiB соблюдён консервативно по объёму прочитанных
source и созданных файлов; CPU/RSS/physical I/O этой подготовки не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Prepared old graph применим как current | PREP-1 graph=e22; current Root=2bb05d3 | Новых selected blobs ещё нет | данных недостаточно |
| Новый exact-Git export можно независимо рассмотреть | Exporter + finite plan + AST syntax check | Не запускался; нужен high review/Root READY | изменить |
| Новый launcher исключает guard `.pyc` substitution | Verified buffer compile/exec fresh ModuleType | Stdlib trusted host остаётся предпосылкой | сохранить |
| Actual sources дали reproducible facts | Calls0; snapshot namespace отсутствует | Нет bytes A1/A2 | данных недостаточно |
| Meaning/render/native/scientific acceptance | Никакого такого execution/evidence в scope | Synthetic56 и source harness не дают приёмку | данных недостаточно |

STOP: передано Root для независимого high review; execution не выполнялся.
