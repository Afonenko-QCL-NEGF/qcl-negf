# SCI05-N1 Runner v3 E5: независимый финальный CP-CODE source review

Дата: 2026-10-19. **PASS — CP-SOURCE; eligible для уже выделенного coordinator C08 call7 после fresh admission/source binding.** F1–F7 закрыты по исходникам в проверенном scope; новых воспроизводимых blocking findings не найдено. Это не runtime PASS, не исполнение call7 и не разрешение нового budget/corrective round. Reviewer C08=**0**.

## Frozen identity и границы

Worktree `/tmp/qcl-sci05-runner-worktree`, branch `codex/review-closure-final-audit-writer`, HEAD/base `9378396a3681c1eddf2c62f16674834fc4465583`. Actual status содержит только прежние пять owning changed paths: physics_diagnostics.jl, hdf5.jl, point_artifacts.jl, existing results.md и новый test. light_results.jl unchanged. Recursive submodules отсутствуют. `git diff --check` exit0.

Первичными были actual source/test, v2→v3 patch delta, D2 §8.7 и existing native-role/reference checks; авторский v3 report прочитан после них. Порядок author claims не использован как замена независимому trace. Review только read-only text/Git/hash: no target imports/parsers/Julia/Python/HDF execution/tests/solver/build/install/network/server/Git mutation/children. Единственная запись — этот report.

| Артефакт / source | SHA256 |
| --- | --- |
| `/tmp/qcl-sci05-runner-v3-identity.json` | `60e466612ef9ab6ef336cf8f07d7599807baa8622502bbbe6dfd0574ee068b5d` |
| `/tmp/qcl-sci05-runner-v3-patch.diff` | `c834a73d54aedc4e0506cf777cb9e52144d2c33cc5923a1d2963b006e04cfdf4` |
| `/tmp/qcl-sci05-runner-v3-report.md` | `b58e4442055f34e966e9cce1bc590b503a1ceae4756ad51cfffc86720d762c1a` |
| `src/infrastructure/persistence/physics_diagnostics.jl` | `fb4eda44e533c171678d8d8efe18b60c03fdaf72f16db72efebf69ded0901ba9` |
| `src/infrastructure/persistence/hdf5.jl` | `d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143` |
| `src/infrastructure/persistence/point_artifacts.jl` | `9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4` |
| `src/infrastructure/persistence/light_results.jl` unchanged | `75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06` |
| `test/infrastructure/final_fixed_point_audit.jl` | `dbb1b210374060f85b96ee82355bd5afacb9a4b6244515d00ea1930cd45caa5c` |
| `docs/src/user/results.md` | `39e1178fc88a940b69ad61298d54538f44d1e39df6b9d9c2dd8e5264f395f561` |
| Previous review `/tmp/qcl-sci05-runner-v2-code-review.md` | `00d13991e7df95bb36ce7f4ca6a6dcfa42fa11162a589b5555aee04b01988182` |
| Effective E5 checkpoint `/tmp/qcl-checkpoint-SCI05-N1-E5-DEV07-errata.json` | `98a096d1ed1bbc82e88a131e4e705679e4f18d6407ee59794e7a76913a02c5af` |

D2 `/tmp/qcl-sci04-design-v2.md`: `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`; accepted profile A design: `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206`, independent review `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916`. Owning read bindings Core `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c` и Contracts `12fc26462bbab3df76904c6deb01f8c6596de7be` сохранены. Review не переносит выводы на иной source tuple.

## F6 closure: recovery role внутри archive

`physics_diagnostics.jl::_verify_final_audit_pair:630–650` теперь разделяет три scopes в правильном порядке:

1. Не-archive generation сначала отвергает любую audit group и любое присутствие nested commit key, включая null; ранний return сохраняет recovery-generation ban.
2. В archive actual `role=="recovery"` на640–643 требует отсутствия audit group и возвращается без final equality. Canonical commit record при этом не приписывается recovery payload.
3. Full/analysis затем проходят свои прежние presence/type/binding/equality rules. Canonical full strict parity сохраняется; analysis copy может отсутствовать, present copy проверяется полностью.

Actual role поступает из validated schema/role declaration public verifier (`point_artifacts:1185–1189`), а не угадывается по filename. Supported native mapping `hdf5:181` задаёт checkpoint-v4→recovery. Таким образом архивный контейнер больше не делает checkpoint payload финальным.

Новые test controls (`test:173–193`,268–272) проходят именно HDF checkpoint path: отдельная копия tiny native payload получает literal `qcl-negf-checkpoint-v4`/`recovery` headers, сохраняет current native4 markers/tables и declaration actual identity. Helper пересчитывает actual owner bytes/SHA. Positive удаляет group, negative оставляет **равную** canonical audit copy. Различие устраняет старую симметричную ошибку: positive больше не попадает в full parity, negative явно запрещён ролью. Header/group assertions подтверждают форму controls по исходнику. Pinned HDF5.jl source содержит используемый `delete_attribute` API; его runtime behavior этим не утверждается.

F6 **закрыт по исходникам**. Tests authored, не выполнены. Добавление recovery HDF происходит только в owned copied control bundle; ordinary retained producer archive сохраняет свой прежний JSON recovery reference layout.

## F7 closure: dependency reference больше не маскирует full identity negative

`mutated_bundle_check` теперь после mutation и **до** hashing declarations (`test:147–163`):

- находит recovery-reference JSON declaration;
- обновляет nested payload.bytes и payload.sha256 по фактическому canonical physics.h5;
- записывает recovery.json;
- отдельно утверждает успешность existing `_verify_recovery_reference` на157;
- затем пересчитывает bytes/SHA всех artifact declarations, включая изменённый reference JSON, и записывает copied commit.

Независимая существующая obligation `point_artifacts::_verify_recovery_reference:101–108` проверяет именно actual referenced file, поэтому pre-assertion различает прежний stale reference defect до ожидания identity rejection. Производственный reference validator не менялся и не отключён.

Для full identity mutants (`test:276–292`) top-level state_id удалён, declared identity и оба audit records остались исходными; owner hashes и nested reference теперь согласованы. Удаление только нового native identity guard больше не оставляет известного позднего recovery hash reject. Healthy marker-removal positive и analysis negatives сохранены. Это причинный source trace, **не выполненный mutation test**; actual guard-removal runtime не заявляется.

Receipt copied mutant не обновляется, поскольку public `verify_point_artifacts` её не читает. Её stale SHA не может маскировать проверяемый reject и не выдаётся за новую подтверждённую receipt. Original retained canonical generation не мутируется, owning mktempdir cleanup ограничен копиями.

F7 **закрыт по исходникам**.

## F1–F5 и общий N1 contract: regression check

| Scope | Проверенный locator / поведение | Source conclusion |
| --- | --- | --- |
| F1 null/absence | helper631–638/644–646 различает haskey и значение; recovery nested presence запрещён; final present non-object/null reject. Tests301–309 сохраняют legacy/recovery explicit-null negatives | Без регрессии |
| F2 optional analysis | helper649 допускает absent analysis copy;650 сохраняет full presence parity; present copy требует equality | Без регрессии |
| F3 actual identity | helper651–656 требует шесть фактических fields независимо от legacy top-level marker; analysis `identity_json`, full `point_identity_json` | Без регрессии; правильный существующий native4 layout |
| F4 Int ceiling | `_final_audit_identity:500–503`, Integer non-Bool и `1..9007199254740991`; прежние boundary/type tests сохранены | Без регрессии |
| F5 measured TMP | exact allowed root в test helper, tail320–330; old/suffix roots negative; existing path отказ сохранён | Без регрессии |
| One portable object | commit_point_artifacts создаёт actual state_id/sequence до binding, один bound object в full/analysis/commit; internal Core template не мутируется | Сохранено |
| Legacy/recovery generation | no-template legacy omission; new-context-without-template final reject; recovery не копирует supplied template | Сохранено |
| Numeric/assessment | candidate Dyson/spectral/lambda required stationary summary; old gates/Core thresholds/evaluator unchanged | No widening / no new physics evaluator |
| Profile A | instance String fixed UTF8 scalar JSON и четыре exact constant attrs до generic annotation; existing haskey сохраняет values | Сохранено |

E5 delta в production содержит только recovery-role branch; hdf5.jl и point_artifacts.jl byte-exact v2. Docs отражают эту scope rule. Internal bounded transport guard по-прежнему не дублирует полный Contracts nested schema/hostile JSON parser. Это допустимая ранее принятая trusted producer boundary, не основание объявить arbitrary native input sandboxed.

## Eligibility и пределы доказательства

Exact future retained root:
`/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`.
Future canonical commit:
`ROOT/archive/final/commit.json`.
Env: `QCL_SCI05_RUNNER_FIXTURE_ROOT`.

Source совпадает с предназначенным measured TMP и сохраняет fresh-path refusal, synthetic source label и no-overwrite behavior. Наличие/происхождение actual Julia bytes, fresh prepared project/source/native-library binding и runtime admission этот report не устанавливает. Coordinator должен связать их перед уже выделенным call7; actual independent Results readback остаётся отдельным call8 с его собственным frozen source и явным env. Skip/not_run не закрывает producer transport gate. Source review не потребляет и не добавляет invocation.

Shared C08 cap8/consumed6 и effective explicit corrective cap7 остаются по parent/checkpoint. Этот PASS не сбрасывает счётчики, не разрешает повтор после red и не открывает новые corrective loops. V1/v2 frozen packages, original reviews и raw failures сохраняются. Никакого silent source repair reviewer не делал.

Не измерены Julia parse/runtime, HDF5/JLL behavior, actual resource guards/stream counters, actual source-bound producer→Results compatibility, broader integration/native release или final CI. Whole-process hostile HDF metadata RAM, hard realtime и transient quota proof не заявляются. Synthetic format fixture вызывает seed/embedding construction при будущем разрешённом test, но не SCBA/Poisson solve и не full S1. Его literal measurements не являются independent device physics oracle. Сходимость уравнений, all-five/e–e/finite_chain4/current-bound acceptance, discretization и experimental validation остаются отдельными gates; Core CPP2/E1 не переоткрывался.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1–F7 закрыты в reviewed source | Role/presence/binding/bound checks и dependency-refresh controls выше | Authored tests not_run | сохранить |
| Runner v3 source eligible для выделенного call7 | Exact hashes, diff check, measured TMP/root handoff | Fresh admission/project/runtime/source binding ещё coordinator obligation | дополнительно измерить |
| Native/commit/Profile A roundtrip выполнен | Подготовлен actual tiny writer test | Actual producer bytes/runtime пока не установлены | дополнительно измерить |
| Модель/критерии не изменены | Узкий transport delta, unchanged Core evaluator/limits | Не подтверждает scientific correctness полного device | сохранить |
| Научная/экспериментальная приёмка достигнута | Новых scientific evidence нет | Transport-only synthetic scope | данных недостаточно |

**STOP.** PASS ограничен CP-SOURCE exact v3 tuple. Sole output — этот report; execution и runtime/science PASS не заявляются.
