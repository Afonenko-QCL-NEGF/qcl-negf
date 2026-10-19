# SCI05-N1 E4/v5 — role selector correction, source frozen

2026-10-19. Выполнен ровно один разрешённый finite E4 source round по
`/tmp/qcl-checkpoint-SCI05-N1-E4.json`, SHA256
`63f0b1679f94522f2143c12e49877aeccbe0fc51f900057602acfdf502c0505e`.
Коллированный review `/tmp/qcl-sci05-results-v4-code-review.md` SHA256
`91e1ab77033d3c95f2cd03cb4efa7aeb7a9216c6d49b6260bac9c112b83da198`
прочитан полностью; исправлено только его единственное load-bearing замечание.
Independent CP-CODE/runtime PASS этим автором не заявляются.

## Erratum и первичная authority

Original F1 review выявил отсутствие sidecar identity binding, но указал
`metadata/point_identity_json` для analysis неточно. E2 ошибочно перенёс этот
full-owner selector в analysis и synthetic fixture. Original report и v2/v3/v4
сохранены без переписывания; erratum явно принят из collated review.

Фактический native4 producer является authority: Runner
`point_artifacts.jl::save_analysis_physics` пишет schema
`qcl-negf-physics-analysis-v4`, role physics.analysis и
`metadata/identity_json` (прочитаны строки304–317); Runner verifier также выбирает
этот role field. Это существующий layout, не новая schema/модель/норма.
Canonical physics.full продолжает использовать `metadata/point_identity_json`.

## Узкая correction

`state.py::_validate_final_audit_sidecar` для present analysis audit теперь
требует и читает **только `metadata/identity_json`**, затем выполняет прежнюю
exact type-strict equality с actual commit identity. Поле point_identity_json
не является fallback и не удовлетворяет этому требованию. Canonical helper
и его full-owner field остались прежними.

Чтение остаётся на том же переданном open sidecar handle после native/commit
pair и owner SHA verification; StateReader общий `_IOBudget/_BudgetStream`
считает actual metadata reads. Нового filename reopen/публичного API нет.
Raw-absent return и recovery prohibition остаются до analysis identity gate,
поэтому historical absent-copy/recovery policy не ужесточается.

Test fixture `publish` теперь пишет analysis identity_json согласно role/schema;
`native` helper принимает явный fixture-only identity_path, чтобы не добавлять
ложный full-owner alias. Healthy analysis control требует actual identity_json
и отсутствие point_identity_json. Stale/missing controls меняют actual field,
обновляют owner bytes/SHA и receipt commit SHA. Каждый из шести stale fields
и missing case проверяется также при оставленном свежем alias point_identity_json:
он не должен заменить authoritative analysis field. Canonical bytes/records
не мутируются; expected data не получены через product encoder.

Profile A/native.py, JSON schema/status/measurement semantics, scientific
formulas/thresholds, stored equilibrium reducer и actual-producer env control
не менялись. Additional contract gaps не обнаружены этим ограниченным source
проходом; отсутствие runtime остаётся ограничением, не pass.

## Identity, preservation и checks

Worktree `/tmp/qcl-sci05-results-worktree`, branch
`codex/review-closure-final-audit-reader`, фактический HEAD/base
`e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`; recursive submodules отсутствуют.
Status ограничен native.py/state.py и untracked owning test. Original/root
checkout не менялся; Git stage/commit/push отсутствуют.

V2/v3/v4 report/identity/patch hashes повторно сверены и совпадают с предыдущими
freeze; полные значения сохранены в v5 identity manifest. Original F1 review и
collated erratum не редактировались. V5 patch полный от e2fdeda, старые patches
сохраняют весь rejected source/fixture graph для воспроизводимого сравнения.

Выполнены только text/Git/hash операции и `git diff --check` (exit0).
Imports/parser/tests/HDF5/Julia/solver/build/install/network/server/target
execution=0; Git mutations=0; children=0. Один E4 source round использован;
finite≤15min/1CPU/2GiB/read2MiB/output48KiB соблюдён. C08 consumed6/8 не изменён,
новых calls0. Только координатор может выполнить sole call8 после actual
Runner fixture/source binding и independent high R; автоматических reruns нет.

Prepared controls не исполнялись. Actual Julia archive и linked native behavior
не читались/не измерялись. Historical `_json_scalar` не получил нового общего
allocation bound; whole-process hostile-native-metadata RAM не доказана.
StateReader budget/retained-handle claim не распространяется на весь historical
`verify_recovery_bundle` API без aggregate cap. Transport/physical/scientific
acceptance остаются отдельными gates.

## Frozen outputs

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| src/qcl_negf_results/native.py | 16498 | 532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5 |
| src/qcl_negf_results/state.py | 29863 | 335e67678120fd0c8e222fcb5e937b277ccadac35303fca2250c9f345983b477 |
| tests/test_final_fixed_point_audit.py | 33890 | 45111262df9b7744ca9f7397a887af4133ee602d9b6e325af2d3ee4a5e12f95a |
| /tmp/qcl-sci05-results-v5-patch.diff | 48313 | 7be93766f021e2e8a3a4c4afc5a4d56f1302d5317c001d36c108408c9d2034c1 |

Identity manifest: `/tmp/qcl-sci05-results-v5-identity.json`.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Analysis binding адресует actual native4 field | Producer identity_json locator; v5 exact source | Independent high R pending | изменить |
| Свежий alias не подменяет stale/missing authoritative field | Literal refreshed-SHA/receipt controls с fresh_alias=False/True | Не исполнялись | дополнительно измерить |
| Canonical/absent/recovery/profile-A semantics сохранены | Unchanged full selector, early branches, native exact SHA | Source-only observation | сохранить |
| Runtime/native/scientific acceptance достигнута | Исполнений/actual producer reads0 | Sole call8 и science gates впереди | данных недостаточно |

STOP: exact v5 source freeze. Новых edits/исполнений без READY нет.
