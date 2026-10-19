# SCI05-N1 Contracts — frozen source handoff

2026-10-19. Этап: изменение owning Contracts по принятому SCI04-D2, source-only.
Независимый CP-CODE и bounded C08 остаются за координатором. STOP.

## Source и scope

Root в начале чтения: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`. Actual status уже содержал чужие
изменения Core/Runner, checkpoint/census/runbook и untracked evidence; эта task
их не редактировала. Root gitlinks/actual submodule status сняты до реализации;
Contracts selected/current `02a564b78dc9c5e19eacf496bc8c891361eafaab` clean.

Изолированный компонентный worktree `/tmp/qcl-sci05-contracts-worktree`,
ветка `codex/review-closure-final-audit-contract`, HEAD ровно тот же `02a564b`.
Создание worktree потребовало согласованного sandbox escalation только для
Git metadata. Stage/commit/push не выполнялись. Original dirty checkout
`/home/tolya/Загрузки/qcl-negf` не менялся.

Прочитаны root AGENTS.md/architecture, applicable science.md SCI04/SCI05/C08,
autonomy.md, component CONTRIBUTING.md, существующие pure helpers/messages/
schema loading/tests и frozen D2 §8–9. Component AGENTS.md отсутствует.
Прочитан TDD skill и writing-good-tests; тестовые fixtures записаны до модуля.
RED/GREEN не запускались: прямой brief оставил все исполняемые C08 координатору.
Ранее упомянутый Core parse failure не заявляется RED для этого нового модуля.
No Python invocation/import/test, Julia, install/build/solver/profile/server/
network, native HDF5 read, subprocess продукта или дочерний агент.

Normative inputs SHA256:

- D2 `/tmp/qcl-sci04-design-v2.md`: `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`.
- D2 review `/tmp/qcl-sci04-design-v2-review.md`: `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1`.
- Status clarification `/tmp/qcl-sci04-d2-status-clarification.md`: `a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8`.
- Clarification review `/tmp/qcl-sci04-d2-status-review.md`: `f5a06df97644ec6d7c576f10ae6fdbbdcdb1187cbef6f4ba3d61cd3aa7f3dab3`.

Core source context дополнительно прочитан через `git show` commit
`1b8fda18881007f7c0c7f68758c7dbf42b44dfc6`, path
`src/numerics/reference/final_audit.jl`; никакой current редактируемый Core test
не использован как oracle. Fixtures не импортируют Core и не выводятся из его
результатов. D2 не менялся ради совместимости с producer.

## Что реализовано

Ровно четыре разрешённых пути:

| Path | SHA256 | Bytes |
| --- | --- | --- |
| src/qcl_negf_contracts/final_audit.py | 1c19ba7f27912c739b349fb7c517a9030be3c4f50c4b75932c08d0c02f3219d1 | 22707 |
| src/qcl_negf_contracts/schemas/final-fixed-point-audit.schema.json | ef25a90acfdc8445a20fb53bc40a861de355e07a8abca4dd90f7ee9a0143dc28 | 21011 |
| tests/test_final_audit.py | 23098050f2fbc1d282b0de3a84ba0d034be034a3f69f62920fee6fba64914b12 | 17773 |
| README.md | a95dc9b6f09160f06b1197d57c83147718152b914c6c6da4e7aa3e3f6753f94c | 12876 |

README изменён ровно одной строкой schema reference. artifacts.py, native4
required markers, registry, public __init__ exports и другие файлы не менялись.
Schema использует существующий offline resource adapter и только internal
`#/$defs` references. Runtime helper dependency-free, читает bundled schema и
поддерживает её закрытый vocabulary; дополнительная семантика остаётся рядом
в pure format helper. Новый public physics/model/service API не создаётся.

Контролируются exact keys/types/enums/units/required-null fields, strict UTF-8,
NUL/BOM/duplicate/nonfinite rejection, bytes≤65536/depth≤9/members≤1024,
селекторы≤64 UTF-8 bytes, detail≤512, identity≤128, canonical channels/row inventory,
context unknown fields/alignment, Measure tagged-null/domain statuses,
mandatory vs optional history и record_status. Проверяется scope witness
coordinates/status. Finite candidate raw/λ со знаком сохраняются. Measured0
не становится pass. D2 overflow clarification не теряет finite ratio0 и
сохраняет measured finite absolute norms; actual nonfinite fields — tagged null.

Никакие формулы невязок, matrix maps, gate tolerances, scientific verdict или
runtime model inventory не вычисляются. Проверка canonical row winner — только
format ordering/tie consistency переносимого scalar inventory; она не является
расчётом self-energy. Scalar values не заменяются defaults и не clip-ятся.

## Замороженный interface для Runner/Results

Module: `qcl_negf_contracts.final_audit`. Errors: существующий `ContractError`.

```python
validate_final_audit(raw: bytes, *, expected_identity: dict | None = None) -> dict
encode_final_audit(record: dict, *, expected_identity: dict | None = None) -> bytes
validate_final_audit_pair(native_raw: bytes | None, commit_record: dict | None, *,
                         expected_identity: dict, final_state: bool = True) -> dict
```

`validate_final_audit` принимает **JSON bytes**, не HDF5 padding/dataset/str,
и возвращает fresh decoded record. `encode_final_audit` валидирует и возвращает
bounded shortest-roundtrip UTF-8 JSON bytes с canonical +0; не добавляет identity,
не меняет input. Caller сначала связывает actual six-field state_identity.

Record.state_identity всегда ровно execution_id/point_id/state_id/attempt/
state_sequence/plan_fingerprint. expected_identity может быть полным actual
commit identity: из него обязательны все шесть полей с точным type/value;
лишние commit fields не становятся record keys. Boolean/float не заменяют
integer attempts/sequence. Results отдельно проверяет native point identity
тем же helper against that actual identity и прежний owning SHA.

Pair wrapper всегда ровно `{'record': ..., 'status': ..., 'reason': ...}`:

- Обе final копии absent → record=None,status=not_recorded,reason=None.
- Recovery обе absent (`final_state=False`) → record=None,status=not_applicable,
  reason=not_a_final_state.
- One-sided presence, любой record в recovery, wrong identity или semantic
  disagreement → ContractError.
- Обе final present → record=native decoded object, status=record.record_status,
  reason=record.reason. Status всегда measurement status, никогда pass.

Pair проверяет bounded format обеих копий до equality. Object order неважен,
array order точен, bool/type-sensitive identity точны; finite measurement
numbers сравниваются как Float64 exact value без tolerance. Caller обязан
сохранить исходные bytes/owner provenance и неизменяемый snapshot во время call.

Native HDF5 preflight **остаётся в Results**: scalar fixed S dtype, 1..65536
itemsize, UTF-8 attrs, отсутствие vlen/chunks/compression/filters/external
storage, точные dataset/group attrs и physical read accounting. Только после
этого caller читает bytes, удаляет right padding и вызывает helper. Проверка
native vlen/attrs не притворяется частью pure byte formatter. Recovery payload
presence и optional physics.analysis copy проверяются owning reader с тем же
canonical record. Новый format cap не увеличивает archive grant.

## Fixtures и проверка

Literal independent fixture + negative controls: measured0, wrong schema/units/
status/keys/identity/type, canonical rows/channels, null context/order, domain
errors и invalid dependencies, optional empty/one/nonadjacent history, signed
candidate/raw/λ, NaN/+Inf/−Inf tagged mapping, finite zero overflow + each
measured-zero mutant, Unicode byte limits/NUL/surrogates, duplicate/nonfinite/
invalid UTF-8 JSON, budget preflight, pair contradictions/identity/one-sided,
legacy/recovery и canonical zero encoding. Positive fixture дополнительно
проходит existing schema_validator **при будущем выполнении теста**.

`git diff --check` tracked README: без замечаний. Для каждого untracked source/
schema/test выполнен `git diff --no-index --check /dev/null <path>`: без whitespace
diagnostics (exit1 означает наличие добавленного diff, не выполненный test).
`git apply --check --reverse /tmp/qcl-sci05-contracts-patch.diff` завершился exit0
на frozen worktree: patch соответствует текущим четырём изменённым файлам.
Schema constructed как JSON serialization authoring dictionary; meta-schema и
Python syntax/import/runtime здесь не проверялись исполнением. Hashes проверены
sha256sum; test SHA дополнительно openssl на промежуточном snapshot, final SHA
в таблице повторно снят после последнего добавления budget controls.

Executable C08 calls=0; env/install/build/solver/native/server calls=0.
Общий C08 cap SCI05/08 не изменён, retry/corrective allowance не присвоен task.
Следующий допустимый check: coordinator-only prepared Python targeted test
`tests/test_final_audit.py` плюс existing schema validity test, в его remaining
C08 accounting. Full suite/environment не поднимать автоматически.

Patch `/tmp/qcl-sci05-contracts-patch.diff`: SHA256
`83800d665d6acf06b7e84653d70a17458f2ded3d45583e823f6f8497b9fd4b58`, bytes64679.
Identity `/tmp/qcl-sci05-contracts-identity.json` привязывает исходники и inputs.
Это reviewable candidate, не claim завершённой runtime/scientific acceptance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D2 portable format реализован в owning Contracts | Frozen four-file hashes, source/schema/literal controls | CP-CODE и runtime pending | изменить |
| API готов для согласованного consumer implementation | Три signatures и точный pair wrapper выше | Native HDF5 checks принадлежат Results | сохранить |
| Healthy/negative controls проходят | Здесь tests не выполнялись | Source-only candidate, не GREEN | дополнительно измерить |
| Новая физика/solver acceptance доказана | Отсутствует numerical/runtime evidence | Формат не доказывает уравнения/эксперимент | данных недостаточно |

STOP: не продолжать source/runtime correction без coordinator review/remaining budget.
