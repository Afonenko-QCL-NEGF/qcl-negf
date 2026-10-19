# DOC07 C1: исходники RED, Phase 1

Подготовлен только `tests/test_model_help.py` в изолированном local clone
`/tmp/qcl-doc07-contract-worktree`; branch `codex/review-closure-model-help-contract`,
HEAD/base `12fc26462bbab3df76904c6deb01f8c6596de7be`. Clone сделан локально с
`--no-hardlinks`, без сети и submodule init. Owning status — ровно один untracked
новый test file. Production resource и C2 helper не созданы, loader не изменён.

Canonical DOC03 после принятого append проверен SHA256
`fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`.
Accepted D2 и high R проверены соответственно
`20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` и
`f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231`.
Root HEAD при чтении `d4113f43cddf02d46025434eb3a9dd8e110e90d6`; его dirty
состояние и recursive submodule status прочитаны, root и исходный component
не изменялись этим исполнителем. Source graph не обновлялся.

## Содержимое и локаторы

Новый test source — 624 строки, 30871 bytes, 28 test functions с параметризацией.
Factory helpers задают пять полных независимых synthetic документов с literal
public fields/formats; будущая schema не используется для построения expected
objects. Положительные объекты включают каждый nested object type и затем
используются как основа для одиночных negative mutations.

| Группа | Источник test function | Что ловит |
| --- | --- | --- |
| Resource/offline/five formats | `test_resource_name_and_offline_local_refs`, `test_all_five_complete_authored_formats` | Missing resource, неверная версия, remote refs, неверный basename, non-object root |
| Closed/required nested objects | `test_every_exercised_object_is_closed_and_all_fields_required` | Extra/missing field в каждом nested instance всех пяти healthy factories |
| Ten Fact coverage | `test_all_ten_fact_classes_are_required`, `test_repeated_fact_names_allow_distinct_authored_contexts` | Missing любой из десяти classes; ошибочный max10/unique-by-name, invented Fact/status |
| Atom/finite | `test_scalar_atom_kinds_and_known_null` … `test_finite_decoded_atom_boundary` | Kind/value/unit mismatch, bool-as-number, arrays/objects, unknown vs known-null; NaN/Inf/-Inf/1e400 через existing finite boundary |
| Origin/ValueOrigin | `test_origin_status_matrix` … `test_value_origin_shape_status_reason_matrix` | Closed status/kind/locator/note/binding/reason matrix; no compulsory DOI; empty research-assumption note |
| View independent axes | `test_documentation_binding_shape_status_reason_null_matrix` … `test_available_snapshot_with_empty_projection_and_unbound_docs_is_shape_valid` | Docs status/reason/null identity matrix; retained known scalars на unbound; typed input_status; available metadata с empty safe projection |
| Scalar/assignment/context | `test_scalar_known_unknown_null_obligations` … `test_context_identity_scalar_types` | Known Atom+Evidence / unknown null; source-or-rule known; redacted source=null; UUID/scientific ID/hash/attempt/model_revision types |
| Snapshot | `test_snapshot_is_local_closed_and_has_no_api_origin_fields`, `test_snapshot_effective_step_kinds` | Standalone local context, no fake actor/release identity; no API value_origin/evidence; origin_bindings=[] допустим; capture/phase/step enums |
| Index | `test_index_entry_status_reason_matrix_and_oversized_measurement`, `test_index_exact_logical_path_grammar` | valid/ok vs invalid/non-ok; oversized typed bytes retained; exact path including no leading-zero attempt |
| Published limits/common refs | Remaining five tests plus applicability note | Explicit Unicode/array caps, pins, hashes, selectors, DocRef; no eight-leaf global enum; no mandatory applicability condition |

Caps проверяются на boundary и boundary+1. Для cap positives используются
различные fragment IDs/paths, input paths, index point IDs/paths и condition IDs;
тесты не требуют принимать semantic keyed collisions. Index boundary создаёт
10000 простых metadata entries в памяти; это synthetic unit fixture без файлов,
arrays или solver. Сериализованные byte guards и trusted full context/hash/source
proof относятся к C2/owner boundary, не подменены count проверкой.

## Строгая граница доказательств

`bound` в positive View/ValueOrigin — literal shape control, **не** доказанный
reference/actual-origin/release binding. Это написано в module docstring и
локальных комментариях. Reference Origin не становится origin run по числу;
source/historical/current equality, last assignment, exact mapping, retained
bytes/receipts и полнота effective chain здесь не проверяются и не реализуются.
Historical no-capture snapshots допускают `origin_bindings=[]`; actual-origin
missing proof останется unknown в C2, а не guessed bound. Empty mapping policy
представлена permissive healthy View `inputs=[]`, available/ok, fragment=null;
сама schema не устанавливает отсутствие/наличие mapping proof.

C1 не требует arbitrary equation ID pattern, обязательного DOI, нового unit
registry, mandatory temperature/composition conditions, новой public helper API
или changes `__init__.py`. Public locator provenance/query policy и normalized
source/file safety — отдельные C2 semantic controls, здесь их pass не заявлен.

## Выполненная проверка и ожидаемый RED

Выполнены только чтение текста/Git/hash, shell local clone/checkout, запись test
source и /tmp artifacts, `git diff --check`, `git diff --exit-code HEAD -- tests`.
Последний exit0 доказывает сохранение всех tracked test sources; SHA256
`tests/test_contracts.py` до/после
`0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7`.
`git diff --check` exit0. Новый untracked test включён в отдельный no-index patch.

Python, imports, parser/compile/pytest/schema validation НЕ запускались. Runtime
call budget из поручения Root не расходовался. RED ещё **не наблюдался**;
синтаксическая исполнимость и healthy validity ещё не подтверждены runtime.
Source inspection + shell absence check подтверждают, что resource отсутствует;
ожидаемый первый feature failure — resource name/loader, без намеренно malformed
healthy fixture. До runtime нужен independent high source R; затем Root выполняет
один разрешённый targeted RED и сохраняет raw output:

`pytest tests/test_model_help.py tests/test_contracts.py::test_all_schemas_are_valid_and_references_stay_in_bundle tests/test_contracts.py::test_offline_validator_resolves_bundled_schema_references -q`

Полные suites/build/solver, installation/network/server, другие агенты,
stage/commit/push и root/checkpoint writes не выполнялись. Logical source read
оценён консервативно <1 MiB (лимит 5 MiB); physical Git/fs I/O не измерялся.

## Артефакты

- Test SHA256: `c2fdf66a51a5b772e270cd520e1c560794c11a39c191bfe2ed8abc61e33bf684`.
- `/tmp/qcl-doc07-C1-red-patch.diff` SHA256: `45d7cb0e2184363932da4ec5b5160b55cb453605a7935a562f9e404984b34d92`.
- `/tmp/qcl-doc07-C1-red-identity.json` содержит exact binding и нулевые runtime счётчики.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| C1 имеет independent authored positive и paired negative shape sources | Exact test SHA + five factories/28 functions | Source-only; ещё нет independent R или observed RED | дополнительно измерить |
| Existing tests и owning production сохранены | `git diff --exit-code HEAD -- tests` exit0, preserved SHA, status только ??new test | Untracked test проверен отдельным patch | сохранить |
| Shape-valid bound означает actual binding | Только synthetic literal shape fixtures | Retained bytes/context/receipt proof отсутствует в этом этапе | данных недостаточно |
| Phase1 можно передать source reviewer | Frozen exact artifacts; runtime calls=0 | Production implementation только после independent R и Root RED | сохранить |

STOP: жду независимый high source review и Root runtime RED; C2 не начинался.
