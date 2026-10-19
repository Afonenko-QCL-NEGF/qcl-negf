# SCI05-N1 Runner v2 — единственная E3 source correction F1–F5

2026-10-19. Статус: **SOURCE_CANDIDATE_STOP; CPP и runtime не закрыты**.
Ровно один выделенный E3 engineering repair выполнен по checkpoint
`/tmp/qcl-checkpoint-SCI05-N1-E3.json`, SHA256
`92d54fd93e5097b4389a1150da7712ade6bc1701959e346ae08d0ad2e152b4b0`.
Полный collated independent review прочитан и проверен по SHA256
`b1c995927188a1c21879ec56e14020b893ba5cee67f2c51884af8e52fa0f696c`.
Новых causal schema/scientific gaps при source correction не установлено;
это авторское наблюдение, не independent CPP.

## Identity / полномочия / сохранённый freeze

Тот же isolated worktree `/tmp/qcl-sci05-runner-worktree`, branch
`codex/review-closure-final-audit-writer`, HEAD/base
`9378396a3681c1eddf2c62f16674834fc4465583`; submodules отсутствуют. Исходные
пять changed paths сохранены: physics_diagnostics.jl, hdf5.jl,
point_artifacts.jl, existing results.md и новый distinct owning test.
`light_results.jl` unchanged. Root actual HEAD при E3
`cfc38e1761f24caf436d938f378dbcdbf71a28f0`; его status содержит только
координационные checkpoint/evidence changes других исполнителей. Recursive
selected inventory: Core7324d98, Runner9378396, Contract12fc264,
Resultse2fdeda, AiiDAd8f8092, Platformb067723, Portal2622de5, Research1eacefc.
Root/selected component working trees и original dirty checkout не изменялись.

Initial frozen package не перезаписан; hash повторно подтверждён:

| Initial artifact | SHA256 |
| --- | --- |
| /tmp/qcl-sci05-runner-report.md | 0e0c89e6ba8c641399268eb633bd78310d7f70b0134bb8626f3d61d6e319fa94 |
| /tmp/qcl-sci05-runner-identity.json | 7d2a44cee5c8074e6b4a1db1c421ea080e32cae57f3d1b42c14d6cfc61878857 |
| /tmp/qcl-sci05-runner-patch.diff | 9fc71bb3ca3c9724b6d545c7b231c90dd4b053455f7d298eb63692d523e6ad70 |

D2/profile A/authority и untouched numerical paths остаются по initial report.
E3 effective shared corrective total cap5 = original2 + CoreE1extra1 +
ResultsE2extra1 + RunnerE3extra1. C08 sharedcap8/consumed6 неизменен;
здесь calls0. Core closed scope не открывался. Writer envelope30min/1CPU/
2GiB/read4MiB/output64KiB; только текст/Git/hash, ни runtime, ни children.
Прочитан skill receiving-code-review: findings сопоставлены с owning source
до edits. Direct runtime запрет сохранён; никакой RED/GREEN claim нет.

## Repair / distinguishing controls

| Finding | Узкая correction | Независимый различающий control, authored/not_run |
| --- | --- | --- |
| F1 null/absence | `_verify_final_audit_pair` использует `haskey` nested key; recovery запрещает любое его присутствие; final present non-object/null отвергается до legacy/optional branches | Healthy legacy absent и recovery absent сохранены; копии обоих bundles с явным `null` отклоняются public verifier |
| F2 optional analysis | Private helper принимает role от actual artifact; canonical full strict parity сохранён; absent analysis audit разрешён, present analysis проходит все identity/value checks | В copied actual archive удаляется только analysis group, owner bytes/SHA обновляются — positive; present analysis record с normalized_sheet2 вместо1 — negative |
| F3 native identity | Для каждой present native copy helper требует metadata identity_json (analysis) либо point_identity_json (full) и exact six-field native↔actual commit match независимо от top-level state_id | Для full и analysis: healthy archive без top-level state_id — positive; native identity missing либо stale attempt/sequence/plan при удалённом top marker — negatives; audit copies/declared identities остаются исходными |
| F4 portable Int | `_final_audit_identity`: both attempt/sequence bounded `1..9007199254740991`, Integer non-Bool, без coercion | Каждый max-valid сохраняется точно; каждый max+1 отвергается; прежние Boolean/Float/missing/mismatch controls сохранены |
| F5 measured TMP | Единственный retained whitelist теперь exact `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`; fresh-path error и synthetic label сохранены | Exact assigned root positive, historical root и suffix path negatives; actual coordinator env проходит ту же whitelist function |

Новый test helper `mutated_bundle_check` копирует tiny actual writer final/
recovery bundle во временную owned подпапку, меняет только заданные metadata/
record/key, обновляет фактические artifact bytes/SHA и пишет mutated commit.
Затем вызывает **public** `verify_point_artifacts`, чтобы negative не отвечал
лишь existing checksum gate. Receipt не является входом этой public функции
и не выдаётся за обновлённую receipt authority; временный copied bundle удаляет
владеющий mktempdir. Canonical retained producer bundle не мутируется.
Literal expected values/identity targets не вычисляются tested encoder;
existing `_light_json` используется только как транспорт modified metadata.
Новых schema engines, numerical formulas, tolerance/API-requiredargs/deps нет.

F3 comparison использует прежний private exact semantic scalar/type helper
после validation actual six-field inventory. Truly absent-record legacy
сохраняет прежнюю совместимость. Отсутствующая optional analysis copy не
объявляется новым native record и не создаёт fake measured status.

## Consumer / runtime handoff

Results v4 report прочитан **только для actual layout/handoff**:
`/tmp/qcl-sci05-results-v4-report.md`, SHA256
`de1a8c421ac9ed09596d46309e05b00c6ac23b45bfaaee7e083791927cd02c4b`.
Consumer не изменялся. Его actual-producer control ожидает тот же env root,
`root/archive/final/commit.json`, execution `fixture-execution`, point
`fixture-point`, attempt2, fingerprint `a`×64, generated state_id/sequence,
shape9×3×2, literal Unicode detail и measured0. E3 сохраняет эти значения и
layout. Optional analysis writer по-прежнему создаёт identical copy; optional
absence здесь лишь public reader compatibility control.

Для единственного coordinator call7 **после independent high R**:

`QCL_SCI05_RUNNER_FIXTURE_ROOT=/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`

Запуск existing prepared/source-bound Julia с --startup-file=no и
--check-bounds=yes, единственный owning test
`/tmp/qcl-sci05-runner-worktree/test/infrastructure/final_fixed_point_audit.jl`.
Никакого install/instantiate/precompile или rerun этот документ не разрешает.
Точный project/runtime/source binding и original log/receipt — координатору.
Test требует output root ещё не существует и ничего не overwrites.

Будущие locators, **не созданные этим writer**:

- `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture/archive/final/commit.json`
- соседние physics.h5 / analysis.h5 / receipt.json;
- `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture/fixture-source.txt` после
  успешного test body; synthetic/no-solve label сохранён;
- recovery artifacts/generation-000001 и legacy/archive/final — дополнительные
  tiny format controls, не canonical producer owner.

Call8 обязан задать тот же env и применить independent Results/Contracts
проверку actual retained canonical full+commit; skip не transport PASS.
Произведённые массивы/measurements synthetic, не согласованный scientific
fixed-point oracle. Нет SCBA/Poisson solve или production archive mutation.

## Frozen source и фактическая verification

| Path | SHA256 |
| --- | --- |
| src/infrastructure/persistence/physics_diagnostics.jl | 66a0eb7072c6ba871d1009d8543a103c30c9cc28f0b6640c9f7a511daa417f7c |
| src/infrastructure/persistence/hdf5.jl (unchanged vs initial) | d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143 |
| src/infrastructure/persistence/point_artifacts.jl | 9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4 |
| src/infrastructure/persistence/light_results.jl (unchanged) | 75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06 |
| test/infrastructure/final_fixed_point_audit.jl (294 lines) | 282471a5ca516ad0c4806451e86d483bfe6339232579e6e2ea69c764c9ca4dce |
| docs/src/user/results.md | cc302e70fe27ac11f0820fbe9675731c21393c7e37f373310e13abd0c1fbbd44 |
| /tmp/qcl-sci05-runner-v2-patch.diff | 3987f6cdcbd798c06a277fd02d4774c8a82e6cc41c5fa442409f0ed185c1f316 |

`git diff --check` exit0; diff/source trace reviewed. Full patch от exact base
включает untracked new test. `git diff --no-index` exit1 означает new-file diff,
не test result. No imports/parsers/Julia/tests/HDF runtime/build/install/network/
server/stage/commit/push/children. E3 runtime calls0, shared C08 consumed6/8.
Source/format verification не доказывает runtime behavior, all tests not_run.
Полная nested/hostile structural authority остаётся independent Contracts;
Runner не дублирует её private transport guard.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1–F5 source repairs представлены | Scoped helpers/call sites и copied-owner controls | Independent R/runtime открыты | дополнительно измерить |
| Initial freeze сохранён | Повторные три SHA выше | Worktree теперь содержит candidate v2 | сохранить |
| Call7/8 имеют одинаковый exact fixture root/layout | Whitelist + Results v4 read report | Actual artifact ещё не создан | дополнительно измерить |
| Physical/discretization/experimental acceptance установлены | Новых расчётов нет | Synthetic transport test не scientific evidence | данных недостаточно |

**STOP.** Ровно выделенная E3 correction завершена source freeze; дальнейших
edits/исполнений нет без нового ready decision. Отдельный high R и sole
coordinator call7 остаются необходимыми gates.
