# SCI05-N1 Contracts — независимый CP-SOURCE review

2026-10-19. **Вердикт: PASS, source eligible for bounded coordinator test.**
Блокирующих замечаний к frozen четырём файлам не обнаружено. Реализация
соответствует принятому D2 format/status/limits/equality contract в пределах
source review. Это не runtime GREEN, завершённый CP-CODE с test receipt,
scientific acceptance или разрешение нового исполнения.

## Входы, порядок и граница

Вопрос review: реализован ли accepted D2 без расширения physics/API и без
принятия missing/error как pass. Сначала прочитаны D2 normative §6–8,
уточнение overflow/status и их independent reviews, затем весь candidate
source, schema и literal tests. Авторский report прочитан после собственной
сверки. Вывод не получен из авторского списка проверок.

Прочитаны root AGENTS.md, docs/architecture.md, implementation entrypoint,
canonical role policy, применимые P1/SCI05/SCI08/C08 и owning CONTRIBUTING.md.
Owning AGENTS.md отсутствует. Исторический PLAN/standby P1 не отменяет
прямой source-review grant. Этап остаётся source audit.

Исполнены только text reads, sha256sum, read-only Git и запись этого отчёта.
Python invocation/import/pytest/Julia/build/install/network/server/native
HDF5/scientific payload reads, solver, Git mutations и дети отсутствуют.
**C08 calls=0; corrective rounds=0.** Общий cap8 и уже использованные Core
correction2/2 этим review не изменены. Native HDF5 preflight, point identity,
owner SHA и physical read accounting принадлежат Results и здесь не проверены
исполнением. Grant review: ≤30min/1CPU/2GiB/read4MiB/output64KiB; чтение
ограничено текстовыми входами, без распаковки/массивов.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`: actual HEAD
`9d8cf0cad32743791cc3b80ac7c2a948dab02f48`. В начале уже были dirty Core/Runner,
checkpoint/census/runbook и untracked execution evidence. Они не менялись
reviewer-ом. Recursive submodule status снят; Contracts selected/current
`02a564b78dc9c5e19eacf496bc8c891361eafaab`, остальные компоненты не являются
candidate этого review. Root actual Core/Runner отличаются от gitlinks,
что не переносит их runtime evidence на рассматриваемые Contracts.

Candidate `/tmp/qcl-sci05-contracts-worktree`: HEAD
`02a564b78dc9c5e19eacf496bc8c891361eafaab`; recursive submodules отсутствуют.
Status: ` M README.md`, untracked `src/qcl_negf_contracts/final_audit.py`,
`src/qcl_negf_contracts/schemas/final-fixed-point-audit.schema.json`,
`tests/test_final_audit.py`. Ровно разрешённые четыре пути. Финальный повтор
hashes совпал с frozen identity.

| Frozen input | SHA256 |
| --- | --- |
| D2 /tmp/qcl-sci04-design-v2.md | d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c |
| Independent D2 review | ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1 |
| Narrow status clarification | a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8 |
| Independent status review | f5a06df97644ec6d7c576f10ae6fdbbdcdb1187cbef6f4ba3d61cd3aa7f3dab3 |
| /tmp/qcl-sci05-contracts-identity.json | a1fb1c4783dc925d45336e52e35d72a6bafbe370af85187ef5f276ed0c44fb49 |
| /tmp/qcl-sci05-contracts-patch.diff | 83800d665d6acf06b7e84653d70a17458f2ded3d45583e823f6f8497b9fd4b58 |
| Author report, read last | bde103220b43bc7922891dcc28472defe1b8fffadc7e902d683eabcb480852a8 |

| Candidate file | SHA256 |
| --- | --- |
| src/qcl_negf_contracts/final_audit.py | 1c19ba7f27912c739b349fb7c517a9030be3c4f50c4b75932c08d0c02f3219d1 |
| src/qcl_negf_contracts/schemas/final-fixed-point-audit.schema.json | ef25a90acfdc8445a20fb53bc40a861de355e07a8abca4dd90f7ee9a0143dc28 |
| tests/test_final_audit.py | 23098050f2fbc1d282b0de3a84ba0d034be034a3f69f62920fee6fba64914b12 |
| README.md | a95dc9b6f09160f06b1197d57c83147718152b914c6c6da4e7aa3e3f6753f94c |

## Независимые source выводы

**Inventory/types/units.** Schema содержит точный required top-level набор,
six-field state_identity, shape, units, context/source_paths, history и все
dyson/spectral/keldysh/selfenergy/charge/poisson fields D2§8.5–8.6. Nullable
keys остаются required. Все object inventories закрыты. Shape≤2^31−1,
остальные положительные Int≤2^53−1; `_matches_type` final_audit.py:82–88
отделяет bool и float от Int. Fixed units, paths, schema и floors заданы
constants. Context unknown/alignment и canonical nullable field order
проверяются в174–187; default model/context не выводится.

**Bounded strict representation.** final_audit.py:30–79,354–375 отвергает
duplicate keys, NaN/Inf tokens, Float64 overflow, invalid UTF-8, NUL/BOM,
decoded surrogates, depth>9, members>1024 и raw bytes вне1..65536.
Schema и byte checks ограничивают detail512, selectors64, identity128.
Canonical enabled channels и ровно3*(channels+3) ordered rows с обязательными
embedding_total/plus/minus и R/L/G проверяются185–193; нельзя принять
missing/duplicate/extra row даже для unavailable. Arrays и finite scalars
не заменяются defaults. HDF5 dtype/filter/vlen preflight заявлен caller
responsibility, что соответствует owning границе D2§8.3/8.8.

**Статусы и доступность.** Schema `$defs.measure` задаёт exact M keys и
measured finite/null/null, finite error либо tagged-null error, tagless-null
invalid_prerequisite, unavailable/not_applicable null mappings. Source196–237
ограничивает optional scope, reasons и domain bounds; required target≤0 или
stored_raw≤0 нельзя выдать measured. Negative finite candidate raw/λ
принимаются без clipping. History239–259 различает empty, one-row и actual
nonadjacent previous row. Witness261–285 связывает статус с M и coordinates,
проверяет shape и approved finite-zero/nonfinite-normalization mapping.
В299–339 mandatory M определяют record status/reason, unavailable map требует
fresh-dependent unavailable fields; required отсутствие не становится measured0.
Optional history не заменяет candidate map. Ни одного status `pass` нет.

**Overflow clarification.** D2 finite error0/null-tag/nonfinite_measurement
допускается в schema; denominator tag с finite ratio требует error-статус
обоих witnesses и aggregate Dyson ratio в276–285. Independent finite absolute
numerators не принудительно помечаются error. Literal control235–265 содержит
все три отдельные measured0 mutations; это source observation о controls,
не выполненная assertion. Никакой повторной norm/map arithmetic нет.

**Equality/identity/legacy/recovery.** `_bind`342–351 сравнивает все шесть
actual identity fields по exact type/value и допускает unrelated actual commit
fields. Pair411–434 валидирует обе bounded копии, требует согласованного
presence и equality; recursive comparison91–101 не зависит от object key order,
сохраняет array order и bool distinction, измерения сравнивает как exact
Float64 без tolerance. Integer-only metadata уже ограничены safe exact range.
Encoder379–408 канонизирует float −0 перед shortest-roundtrip JSON, не меняет
caller object. Absent legacy final→not_recorded; absent recovery→
not_applicable/not_a_final_state; recovery с record и one-sided final presence
отвергаются. Present wrapper переносит measurement record_status/reason,
не создаёт acceptance. Отдельная native point/owner проверка остаётся caller-у.

**Граница owning component и fixtures.** В production module нет Core imports,
kernel recomputation, scientific gate tolerances/acceptance evaluator, services
или нового public `__init__` export. Row-winner consistency использует только
portable scalar format inventory. README diff — одна schema reference;
schema refs локальны. Tests18–76 построены из literal manufactured format
data, а не observed Core output; tests137–356 различают signed candidate,
error/tag/null, unknown context, exact pair disagreement, history, recovery,
Unicode bytes и hostile budgets. Полностью просмотрены оба new source/schema
и весь test file. Runtime, meta-schema и import behaviour из чтения не следуют.

Tracked `git diff --check` не сообщил whitespace diagnostics; добавленный
final_audit.py также проверен `git diff --no-index --check /dev/null ...`
без diagnostics, exit1 означает наличие added diff. Hashes всех четырёх файлов
проверены повторно. Эти проверки не выдаются за Python syntax/test execution.

## Решение и STOP

Конкретных findings для исправления нет. Согласие этого review и автора не
является runtime доказательством. Следующее различающее свидетельство —
координаторский prepared-source bounded targeted test по frozen files и
schema-validity control в оставшемся общем C08, с original logs и receipt;
missing environment/dependency остаётся blocker без install/build. Этот
review не запускает check и не создаёт дополнительного budget/correction grant.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Frozen Contracts реализует D2 portable inventory/status/limits | Exact hashes; schema и final_audit.py30–339; literal controls | Source evidence, runtime ещё не выполнен | сохранить |
| Missing/error не принимается как pass; measured0 сохранён | M schema; mandatory status299–314; pair420–434 | Format не доказывает measurement provenance или physical acceptance | сохранить |
| Identity/equality и legacy/recovery согласованы с D2 | bind342–351, encoder379–408, pair411–434 | Native point/owner/layout/I/O ещё проверяет Results | сохранить |
| Candidate eligible для bounded coordinator test | Source findings отсутствуют; immutable input/file hashes совпали | Общий C08 accounting и prepared environment обязательны | дополнительно измерить |
| Tests/runtime/scientific acceptance уже подтверждены | Исполняемых checks здесь0 | Нет runtime/native/scientific receipt | данных недостаточно |

STOP. Implementation edits, runtime invocation и автоматические remediation
не выполнялись. Единственный новый output — этот файл.
