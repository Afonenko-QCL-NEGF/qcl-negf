# SCI05-N1 Runner v3 — focused E5 F6/F7 source freeze

2026-10-19. **SOURCE_CANDIDATE_STOP; independent high R и runtime pending.**
Один конечный E5 source repair по прямому инженерному grant/checkpoint
`/tmp/qcl-checkpoint-SCI05-N1-E5-DEV07-errata.json`, SHA256
`98a096d1ed1bbc82e88a131e4e705679e4f18d6407ee59794e7a76913a02c5af`.
Полный финальный v2 review прочитан: SHA256
`00d13991e7df95bb36ce7f4ca6a6dcfa42fa11162a589b5555aee04b01988182`.
F1–F5 source closure этого review сохранён; E5 исправляет только F6/F7.
Новые causal contract gaps при этом source pass не установлены; это не CPP.

## Source identity и сохранение

Тот же isolated `/tmp/qcl-sci05-runner-worktree`, branch
`codex/review-closure-final-audit-writer`, HEAD/base
`9378396a3681c1eddf2c62f16674834fc4465583`, recursive submodules отсутствуют.
Root actual HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, dirty чужими
coordination/evidence и Results gitlink33b1a39; Core7324/Runner937/
Contracts12fc прежние. Остальной inventory: AiiDAd8f8092, Platformb067723,
Portal2622de5, Research1eacefc. Root/main components/original dirty checkout
этим writer не изменялись. All five owning paths прежние; E5 delta меняет
только physics_diagnostics.jl, test и native-format docs. hdf5.jl и
point_artifacts.jl byte-exact v2; light_results.jl unchanged.

V1/v2 raw artifacts не перезаписывались; hashes повторно подтверждены:

| Freeze | report SHA256 | identity SHA256 | patch SHA256 |
| --- | --- | --- | --- |
| v1 | 0e0c89e6ba8c641399268eb633bd78310d7f70b0134bb8626f3d61d6e319fa94 | 7d2a44cee5c8074e6b4a1db1c421ea080e32cae57f3d1b42c14d6cfc61878857 | 9fc71bb3ca3c9724b6d545c7b231c90dd4b053455f7d298eb63692d523e6ad70 |
| v2 | 7cbfb82840b81fc91250026676bc274ba6a0f14d4d86148946f16a4b924bf020 | 0616f8d9fd3043e93b97497b0173a6a6ad1cbb218dce01829e5dc2a97a2c2338 | 3987f6cdcbd798c06a277fd02d4774c8a82e6cc41c5fa442409f0ed185c1f316 |

## F6 — actual native recovery role

`_verify_final_audit_pair` сохраняет первым recovery-generation check:
не-archive по-прежнему запрещает и native group, и nested commit key, включая
null. Следом новая отдельная ветка actual `role=="recovery"` для archive:
любая audit group запрещена; отсутствие group допустимо без comparison с
canonical final commit record. Full/analysis policies/binding и legacy
null/absence branches не менялись. Public verifier уже передаёт actual role.

`add_recovery_hdf!` в новом distinct test клонирует tiny native full payload
в отдельный `recovery.h5`, явно заменяет headers на schema
`qcl-negf-checkpoint-v4`/role `recovery` и добавляет соответствующую HDF
artifact declaration с actual commit identity. Остальные required native4
markers/typed tables сохраняются. Copied-bundle helper после edit вычисляет
реальные bytes/SHA. Это настоящий supported HDF checkpoint branch, а не JSON
reference. Canonical full+commit audit сохраняется в обоих controls:

- recovery HDF без group — public verifier positive;
- recovery HDF с равной final group — public verifier negative.

Оба controls authored/not_run. Legacy/recovery generation controls v2
сохранены; физические формулы/массивы и format policy не переопределялись.

## F7 — полный dependency chain copied mutants

`mutated_bundle_check` после mutation, до artifact declaration hashing,
находит existing recovery-reference JSON declarations. Для каждой читает
payload path, обновляет payload.bytes и payload.sha256 фактического physics.h5,
сериализует recovery.json, затем проверяет existing production
`_verify_recovery_reference` как отдельный healthy assertion. После этого
общий цикл заново считает bytes/SHA **всех** artifacts, включая изменённый JSON,
и пишет copied commit. Mandatory production guards не изменены/не отключены.

Source causal chain: у full identity mutants удалён top-level state_id,
поэтому старый legacy identity check не срабатывает; declared owner identity,
обе audit copies и их commit binding исходные; now nested reference и owner
hashes также согласованы. Следовательно removing только новый native identity
guard устранил бы intended reject, а не привёл к позднему stale-reference
reject. Это source-derived различимость, не выполненный mutation test.
Healthy marker-removal positive и analysis mutants сохранены.
Original canonical retained owner не мутируется; все контролируемые копии в
owning mktempdir очищаются. Receipt не является input public verifier и не
выдаётся за новую подтверждённую receipt copied mutants.

## Handoff / бюджет / фактическая проверка

Exact retained root не изменён:
`QCL_SCI05_RUNNER_FIXTURE_ROOT=/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`.
Canonical future path `root/archive/final/commit.json`, соседние physics.h5,
analysis.h5,receipt.json и synthetic source label прежние. Эти bytes ещё не
созданы writer. Source-bound prepared environment, independent high R затем
sole coordinator call7 и actual consumer call8 остаются отдельными gates.
Никаких aliases/consumer corrections здесь нет; Core closed scope untouched.

Effective shared corrective maximum7 = original2 + explicit extras5.
E5 использован один source round; C08 unchanged consumed6/8, writer calls0.
Envelope25min/1CPU/2GiB/read3MiB/output64KiB; only bounded text/Git/hash.
`git diff --check` exit0; diff/source/hash trace reviewed.
No imports/parsers/tests/Julia/HDF execution/build/install/network/server/
stage/commit/push/children. Authored controls **not_run**, runtime/science не PASS.
`git diff --no-index` exit1 — expected new-test diff. Initial failure logs/
reviews/frozen packages сохранены. Никакого automatic rerun/implicit loop.

| Path | v3 SHA256 |
| --- | --- |
| src/infrastructure/persistence/physics_diagnostics.jl | fb4eda44e533c171678d8d8efe18b60c03fdaf72f16db72efebf69ded0901ba9 |
| src/infrastructure/persistence/hdf5.jl | d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143 |
| src/infrastructure/persistence/point_artifacts.jl | 9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4 |
| src/infrastructure/persistence/light_results.jl unchanged | 75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06 |
| test/infrastructure/final_fixed_point_audit.jl (338 lines) | dbb1b210374060f85b96ee82355bd5afacb9a4b6244515d00ea1930cd45caa5c |
| docs/src/user/results.md | 39e1178fc88a940b69ad61298d54538f44d1e39df6b9d9c2dd8e5264f395f561 |
| /tmp/qcl-sci05-runner-v3-patch.diff | c834a73d54aedc4e0506cf777cb9e52144d2c33cc5923a1d2963b006e04cfdf4 |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Archive native recovery role не хранит final record | Отдельная role branch + true checkpoint HDF positive/negative controls | Tests not_run; high R pending | дополнительно измерить |
| Full native identity mutants не маскируются stale recovery reference | Payload refresh→existing reference assertion→all declarations refresh | Source-derived, guard-removal runtime отсутствует | дополнительно измерить |
| F1–F5/численные gates сохранены | Узкий E5 delta, прежние source hashes/call paths | Full scientific acceptance не измерена | сохранить |
| Actual producer/физическая приёмка достигнуты | Новых artifact/solve нет | Только source freeze | данных недостаточно |

**STOP freeze.** Вне этого конечного E5 edits/исполнения не выполняются.
