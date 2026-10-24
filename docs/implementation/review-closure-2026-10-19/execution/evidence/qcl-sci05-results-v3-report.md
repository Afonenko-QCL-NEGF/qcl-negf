# SCI05-N1 Results v3 — единственная correction E2/F1, source frozen

2026-10-19. Исправлен только F1 independent Results review SHA256
`9ae7330b6a4ba3bdf5f7ffd358a976be48b36037fa37a1319e93efce6335e6b0`.
Автор не закрывает независимый CP-CODE и не заявляет runtime PASS. Все checks
ниже — source/text/hash; imports/target execution отсутствуют.

## Полномочия и identity

READY: отдельный finite N1 E2 corrective round по latest human development
resource grant; checkpoint `/tmp/qcl-checkpoint-root7-E2.json` SHA256
`ba3de6c1986595ff9c45d47e8189ff68ad954c83dc0c4ff8d620a5a13c816469`.
Original2+Core E1extra1 сохранены, N1extra1 — четвёртый общий finite engineering
round, без дополнительного Core loop. Этот task не расширяет C08: consumed6/8,
данной работой calls0; будущий Results call только после CPP+actual Runner fixture.

Worktree `/tmp/qcl-sci05-results-worktree`, branch
`codex/review-closure-final-audit-reader`, actual HEAD/base
`e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`; actual status содержит только два
modified production paths native.py/state.py и untracked owning test file.
Recursive submodule status пуст. Native source unchanged from v2. Root/original
dirty checkout не менялись; stage/commit/push не выполнялись. Прочитаны полный
review/caller graph, применён receiving-code-review; выбран source-only этап.

## F1: проверка и узкая correction

Review counterexample подтверждён чтением source: canonical helper проверял
native point identity, sidecar helper проверял только record pair. Owner SHA
и copied record equality не доказывали identity самого analysis контейнера.

`state.py::_validate_final_audit_sidecar` теперь после успешного present pair
требует `metadata/point_identity_json`, читает его через `_json_scalar` на
**том же переданном open handle** и проверяет exact type-strict JSON equality
с actual `commit['identity']` посредством existing `_same_json_value`.
Нет reopen filename или дополнительного stream. StateReader вызывает helper
в прежнем sidecar hash→HDF pass с тем же общим `_IOBudget`; добавившиеся identity
metadata reads считаются этим stream. Budget failures не подавляются.

`raw is None` возвращается до нового identity gate: absent legacy/optional
analysis policy не ужесточена. Recovery prohibition срабатывает до нового
analysis identity gate; recovery absent policy остаётся прежней. Тот же helper
применён existing current/prior-final verifier loops; их прежняя public API
без aggregate I/O cap остаётся ограничением, а не blanket StateReader guarantee.

Изменение production относительно v2 — только пять строк F1 binding. Profile A,
JSONschema, native/commit equality/status, public API, scientific formulas,
thresholds и equilibrium reducer не менялись. Новой wire нормы не введено.

## Literal controls

Добавлен helper `replace_analysis_identity_and_refresh`: меняет только native
analysis identity, заново вычисляет sidecar declared bytes/SHA и commit receipt
SHA, сохраняя literal copied record и canonical physics.full bytes. Использует
stdlib JSON/SHA, не product artifact/final-audit encoder как oracle.

Добавлены controls:

- Healthy present analysis с заново опубликованной matching identity и
  refreshed SHA/receipt; private canonical status/identity и summed owner SHA
  byte accounting остаются assertions.
- Present analysis с missing identity и отдельно stale execution_id/point_id/
  attempt/state_id/state_sequence/plan_fingerprint при неизменных copied records
  и корректных refreshed integrity metadata; требуется конкретный analysis
  native-identity rejection, не случайная checksum failure.
- Absent analysis audit + missing analysis identity с absent либо present
  canonical final record: сохраняется not_recorded либо measured scope.

Canonical full bytes до/после identity mutation сравниваются точно. Existing
recovery/pair/profile-A/budget controls не изменены. Все новые controls —
**неисполненный test source**. Byte/schema/identity checks не принимают физику.

## Фактическая verification и limitations

Выполнены read-only Git/text/hash operations, source diff review и
`git diff --check` (exit0). Python/product imports, parser/tests/HDF5/Julia/
SCBA/Poisson/build/install/network/server/target execution=0; children=0;
stage/commit/push=0. Finite≤25min/1CPU/2GiB/read4MiB/output64KiB соблюдён.
Один N1 E2 corrective round использован, автономного следующего round нет.

Independent source re-review, actual Runner→Results transport и единственный
source-bound Results targeted call остаются required gates. Никаких scientific
arrays не читалось. Existing `_json_scalar` identity format/memory behavior не
перепроектирован; новое общее hostile-HDF5 RSS/native-sandbox доказательство не
заявлено. Same budgeted retained handle claim относится к StateReader;
old `verify_recovery_bundle` public I/O boundary сохранена.

## Preservation и frozen outputs

Все v2 artifacts повторно проверены byte-exact и не перезаписаны:

| Artifact | SHA256 |
| --- | --- |
| /tmp/qcl-sci05-results-v2-report.md | 0f121f3f3f6cd699b516e5d713d408116e7a196a13f94ec1c7ebc056f375786a |
| /tmp/qcl-sci05-results-v2-identity.json | 078894c9107de84d123daa8e799cee535bd7ff3833a791f464185bff063810cc |
| /tmp/qcl-sci05-results-v2-patch.diff | fb936c596a035670426ad64c90c4c97a2e0a663dfd663c34a594e51a2853a55e |

Initial artifacts также не менялись. V3 patch включает полный owning diff от
exact e2fdeda и untracked test, а v2 patch сохраняет source до correction.

| Frozen source/artifact | Bytes | SHA256 |
| --- | ---: | --- |
| src/qcl_negf_results/native.py | 16498 | 532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5 |
| src/qcl_negf_results/state.py | 29877 | 4de0129ca7a5d0a85d9e33b06bf9c5e48858c1c1c73c56e2949e1f9376c93823 |
| tests/test_final_fixed_point_audit.py | 30703 | b43074d234422cc577f84f06519d86b2e5b2e9eb3b2bfd38dee71bc34bdebc70 |
| /tmp/qcl-sci05-results-v3-patch.diff | 45087 | c6b9a9cf45ae0cfbc284de64ddc82cb1eae32567ddec5f30406a3594636a67e3 |

Identity manifest `/tmp/qcl-sci05-results-v3-identity.json`.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 missing analysis-native binding адресован | Five-line sidecar binding + exact source hashes | Independent CP-CODE pending, runtime не выполнен | изменить |
| Refreshed integrity не маскирует stale/missing identity в controls | New literal fixtures перезаписывают SHA/receipt, canonical bytes preserved | Assertions не исполнялись | дополнительно измерить |
| Absent/recovery/profile-A/scientific scope сохранён | Early-return/prohibition до binding; native hash unchanged | Source observation, не integration receipt | сохранить |
| Runtime/native/scientific PASS достигнут | Новых execution receipts нет | Остаются CPP/Runner fixture/targeted Results gates | данных недостаточно |

STOP после freeze. Дальнейшие edits/исполнения не выполняются без нового READY.
