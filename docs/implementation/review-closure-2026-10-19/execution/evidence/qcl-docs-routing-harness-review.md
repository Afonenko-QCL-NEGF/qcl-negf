# Docs-routing local harness v1 — независимый high source review

Вердикт: **CHANGES_REQUIRED_SOURCE**. Два замечания ниже относятся к текущему
harness/finite plan. Этот review не разрешает execution. RED/GREEN, target
parser/import, runtime/version probe, native/build/solver/network и full CI не
выполнялись; test pass и native readiness не установлены.

## Замороженные основания

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-docs-routing-local-unit-run-v1.py`,15570 B | `4dbc78e81ff40f4a70e317dce8e7538dfe5f0f68f458896a8bf910309fae2920` |
| `/tmp/qcl-docs-routing-engineering-plan-v1.json`,5977 B | `e21b6446c4a83275e0b3877c2d32271a887ce2ea48baafe3bf5d424157cb0591` |
| Frozen fixture,38723 B | `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` |
| D1 | `fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270` |
| D2 | `bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70` |
| Accepted D2 review | `939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967` |
| Accepted v2 fixture review | `8c0d8d06fa5b21623bf593446d1cac63ff803f682b5d72dd2663d9a772fa4b79` |
| RawCapture dependency | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| TMP sampler dependency | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |

Root HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; исходный dirty status
прочитан. Все8 gitlinks прочитаны через `git submodule status --recursive`.
Routing worktree HEAD `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, status только
`?? tests/docs_test_routing_test.ts`. Product helper и обе attempt directories
отсутствуют при read-only inventory. Архитектура и D1/D2 с исходными reviews
прочитаны; accepted fixture review используется для ранее выполненной проверки
227 nominal registrations. Это не новый engine count и не повторный fixture audit.

## R1 — hash проверяет .py, а loader может исполнить непривязанный .pyc

**P1, blocking.** Harness:59–63 проверяет `digest(path)`, затем вызывает
`spec_from_file_location` и `spec.loader.exec_module`. Это SourceFileLoader;
SHA256 проверенного source не связывает исполняемый bytecode cache.
`/usr/lib/python3.14/importlib/_bootstrap_external.py`:840–890 сначала читает
cache, проверяет timestamp/size и возвращает `_compile_bytecode`; только895–906
проверяют `sys.dont_write_bytecode` при записи нового cache. Поэтому один `-B`
или `dont_write_bytecode` не устраняет чтение старого cache.

Это существующий путь, а не предположение о необходимости создавать файл:
`/usr/bin/python3` указывает на `python3.14`; read-only stat/od установили:

| Dependency | Source mtime/size | Cache header flags/mtime/size |
| --- | --- | --- |
| `/tmp/qcl-local-julia-guard-v2.py` |1792415830 /14409 |0 /1792415830 /14409 |
| `/tmp/qcl-owned-temp-sampler-v2.py` |1792424527 /1567 |0 /1792424527 /1567 |

Caches находятся в `/tmp/__pycache__/` под соответствующими
`*.cpython-314.pyc`, принадлежат текущему пользователю, mode0644. Их payload
не разбирался и не исполнялся; утверждения, что payload вредоносный либо
отличается от source, нет. Утверждение уже: текущий reviewed SHA не доказывает
identity фактически импортируемого кода. Импорт идёт до attempt reservation
(166–170); при cache miss/stale loader также может писать cache вне owned TMP.
Следовательно, в этом месте нельзя обосновать ни полную code binding, ни
исключение скрытых import effects одной проверкой .py hashes.

Требуемая коррекция: для этих двух trusted guard dependencies прочитать exact
source bytes, проверить их SHA и скомпилировать/исполнить именно эти bytes
в отдельном namespace с explicit source filename и `dont_inherit=True`, обходя
SourceFileLoader/.pyc. Не применять это к target/fixture/helper. Сохранить
source-before/after checks и самостоятельный source review импортируемых guard
dependencies. Это не создаёт hard/adversarial sandbox. Исторические результаты
здесь не пересматривались; sourcehash-only loader не даёт общего доказательства
исторического cache identity.

## R2 — GREEN не привязан к сохранённому и принятому RED predecessor

**P2, требуется до принятия конечной последовательности RED→GREEN.**
Harness:139 перечисляет exact READY fields без RED predecessor reference;
147–161 проверяют helper/review,170 резервирует только выбранный attempt.
Ни наличие, ни digest, ни terminal status RED receipt/log не проверяются.
Plan:89–93 также требует source I/review, но не устанавливает обязательный
Root review genuine RED evidence перед GREEN. При helper/review и fresh GREEN
READY эти ветки допускают GREEN без RED; наличие не связанного с ожиданием
RED failure также не блокирует GREEN. Это статический путь, не выполненный опыт.

Требуемая коррекция: exact GREEN handoff должен ссылаться на retained original
RED receipt/log и независимую принятую интерпретацию, с hash binding на этот
harness/plan/fixture/runtime/RED attempt. GREEN должен fail closed при missing,
mismatched либо непринятом predecessor. Root обязан подтвердить именно missing
`../ops/docs_tests.ts` diagnostic с nonzero child exit и полным capture;
guard failure или иной compiler failure потребляет попытку и не заменяет RED.
Ни автоматического RED rerun, ни новой alias attempt из этой коррекции не следует.

## Подтверждённое и сохраняемые границы

Harness:131–144 ограничивает scope, две exact attempt identities, explicit
execute и fresh READY≤300s, exact JSON keys/duplicates и hashes. Reservation
`mkdir(exist_ok=False)` предотвращает повторное использование сохранённого
attempt path; same-user deletion/adversarial namespace не защищены. READY
остаётся trusted active Root handoff, не аутентифицированным доказательством
полномочий из произвольного JSON. Review ref/hash не означает review approval.

Harness:177–179,212 задаёт ровно absolute Deno argv с единственным frozen file,
typecheck включён, `--no-config --no-lock --cached-only --no-npm --no-remote
--no-prompt --reporter=tap`; directory discovery/filters/only отсутствуют.
Script read/write/env/run/net/ffi grants отсутствуют. `env` полностью заменяет
ambient environment ровно на DENO_DIR/TMPDIR/HOME в новых disjoint0700 children.
Empty new DENO_DIR и запреты npm/remote устраняют разрешение на cache-backed
remote import в этом child contract. CLI source loader всё же читает local
source; future GREEN helper требует отдельного import-safe source review всей
closure, без дополнительных imports и import-time native/product work.

Fixture:3–13 импортирует только отсутствующий production helper. Source и
accepted fixture review различают manufactured reports/fakeExecutor от native
execution. Expected RED — missing-module compile/load failure до регистрации,
не227 executed assertions. Expected GREEN — полный positive TAP227 с проверкой
имён по frozen registrations, counters/exit и source/capture guards; одного
exit0/числа227 недостаточно. Эти predicates должен проверить отдельный результатный
review: harness:268 сохраняет observed_engine_tests=null и unit_result review-required;
272 return0 означает guard completion, включая ожидаемый nonzero RED.

RawCapture source:49–72 дренирует merged raw bytes одним reader, учитывает
partial writes, EOF и ошибки; main harness:224–267 пытается drain/kill/fallback
и терминально наблюдает TMP/RSS даже у быстрого child. RawCapture thread-start
failure имеет fallback; incomplete/error/overrun не становится pass. Исходный
log не обрезается, retained TMP не удаляется. Полная runtime корректность этих
веток не проверена. Process-group cleanup не доказывает escaped-descendant
termination; non-daemon reader и sampled guards не являются hard time/resource
guarantee. Заявленные sampled RSS/TMP/log overshoot limits честно сохранены.
После permanent reservation setup171–176 ещё находится вне внутреннего try;
его failure даст outer blocked stderr без полноценного attempt receipt.
Caller должен удержать этот stderr и reconcile consumed reservation, без retry.

Deno executable SHA фиксируется и проверяется до child (164), версия не
измеряется. Binary не читался данным reviewer. Терминальные checks256–259
проверяют fixture/harness/plan/guard/helper; runtime digest после child не
повторяется. Не следует описывать эту гарантию как before/after runtime check.
Nix path иммутабельность — внешняя предпосылка, не измеренный здесь факт.

Source-only review ограничен named reads и метаданными. Консервативный reserve
named file reads≤1.5MiB<2MiB; physical I/O/CPU/RSS не инструментировались.
Один слишком широкий file-name inventory `/tmp` дал лишний truncated display;
содержимое найденных посторонних файлов не читалось. Report artifacts<96KiB;
точный terminal display cap не заявляется. Созданы только два requested review
artifacts; source/product/checkpoint/index/commits не изменялись. Для решения
достаточны source locators и cache headers, без исполнения target/guard/parser.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact hashes гарантируют actual guard module code | Harness59–63 и existing matching timestamp .pyc; Python loader840–890 | Payload не исполнялся/не диагностирован как отличный | изменить |
| Конечный план требует accepted RED перед GREEN | Harness139,147–170; plan89–93 не связывают predecessor | Trusted Root мог бы соблюсти порядок вне schema | изменить |
| Child ограничен singlefile/empty script grants/exact env | Harness177–179,212, frozen fixture3–13 | CLI source loading остаётся отдельной closure review obligation | сохранить |
|227 engine tests / GREEN / native readiness приняты | Execution0; receipt semantics review-required | Только nominal source count; никаких test passes | данных недостаточно |
| Raw capture и sampled guards имеют предусмотренные failure paths | RawCapture49–72; harness191–272 | Runtime/overshoot/escaped tree не доказаны | дополнительно измерить |

STOP. Новая исправленная source identity требует отдельного review/Root handoff;
этот review не создаёт READY, не расходует попытки и не разрешает execution.
