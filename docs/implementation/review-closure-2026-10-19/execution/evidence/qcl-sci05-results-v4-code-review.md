# SCI05-N1 Results v4: независимый CP-CODE review

Дата: 2026-10-19. **REQUEST_CHANGES / SOURCE_NOT_READY.** Один коллированный P1: E2 связывает analysis audit с неправильным native4 identity path, из-за чего original F1 не закрыт для фактического producer и здоровый будущий Julia archive будет отвергнут. Исполнений, Python/Julia/HDF imports, parser, pytest, solver, build/install, network/server, Git mutations и дочерних агентов: **0**. C08 этим review: **0**.

## Объект review и свидетельства

Worktree `/tmp/qcl-sci05-results-worktree`, HEAD/base `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`, branch `codex/review-closure-final-audit-reader`. Status: modified native.py/state.py, untracked new test; иных изменений нет, recursive submodules отсутствуют. `git diff --check` exit0. Primary D2/profile A, actual diff/source/tests и actual Runner identity writer прочитаны до авторского отчёта v4. Relevant results-analysis/CONTRIBUTING прочитаны; это source review, не анализ произведённого Julia archive.

| Артефакт / путь | SHA256 |
| --- | --- |
| `/tmp/qcl-sci05-results-v4-identity.json` | `8fbe43b60f8cbcb45ebf4d050a63be5c9965c123d36217340743e545204828b6` |
| `/tmp/qcl-sci05-results-v4-patch.diff` | `d2fe0d8e4830cfca663e734950294ebf3292c39c0d1061e0790ef4d869706c88` |
| `/tmp/qcl-sci05-results-v4-report.md` | `de1a8c421ac9ed09596d46309e05b00c6ac23b45bfaaee7e083791927cd02c4b` |
| `src/qcl_negf_results/native.py` | `532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5` |
| `src/qcl_negf_results/state.py` | `4de0129ca7a5d0a85d9e33b06bf9c5e48858c1c1c73c56e2949e1f9376c93823` |
| `tests/test_final_fixed_point_audit.py` | `c94bd68fa6b328c880211d15d61ec1baaeb2da2b3a8e72e429edf8f6b5fccb6f` |
| D2 `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| Profile A `/tmp/qcl-sci05-attribute-encoding-design.md` | `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206` |
| Original v2 review `/tmp/qcl-sci05-results-code-review.md` | `9ae7330b6a4ba3bdf5f7ffd358a976be48b36037fa37a1319e93efce6335e6b0` |

Profile A independent approval `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916` принят coordinator. Contracts source binding — published `12fc26462bbab3df76904c6deb01f8c6596de7be`. Runner baseline `9378396a3681c1eddf2c62f16674834fc4465583`; frozen v1 test SHA `2deeff785cc09ee724dbbaffd0d99693178483c90b7b5685eefe47bbcc773e8b`. Ни actual Julia fixture, ни его hash/readback результат этим review не установлен.

Сравнение frozen v2/v4 patches показывает: native.py byte-exact прежний; state.py дополнен именно пятью строками analysis identity check, прочие отличия patch headers — line offsets. Tests дополнены E2 identity controls и explicit producer control. V2/v3/v4 и original review не перезаписывались.

## F1-v4 — P1: analysis связывается с full-owner identity path, а actual native4 field остаётся непроверенным

**Production locator:** `src/qcl_negf_results/state.py:201–218`, `_validate_final_audit_sidecar`; новые строки214–216 требуют и читают только `metadata/point_identity_json`.

**Primary producer locator:** Runner `src/infrastructure/persistence/point_artifacts.jl::save_analysis_physics`, baseline937 строки304–317 и frozen v1 строки304–317: schema=`qcl-negf-physics-analysis-v4`, artifact_role=`physics.analysis`, actual identity записывается в **`metadata/identity_json`**. Это существующий native4 layout; frozen N1 writer добавляет audit group, но этот identity path не меняет. Runner verifier выбирает `identity_json` для analysis (`point_artifacts.jl:1176–1181` в v1). В full owner используется другой path — `metadata/point_identity_json`.

D2 §8.7 требует record.state_identity ↔ actual commit.identity ↔ native identity. Термин «native point identity» в D2 обозначает привязку состояния; он не вводит новый одноимённый dataset для всех native roles. Правильный path устанавливается фактической role/schema native4.

Два воспроизводимых следствия по исходнику:

1. **False rejection здорового producer.** Actual Runner archive с identical full/analysis/commit audit records и правильным analysis metadata/identity_json проходит hashes/layout/pair, затем `_validate_final_audit_sidecar` неизбежно бросает `analysis final audit requires native point identity`, потому что `point_identity_json` в analysis writer не создаётся. Новый actual-producer test (594–635) дошёл бы до этой ошибки внутри `StateReader` до своих положительных assertions. Расходовать единственный remaining Results call8 на известную несовместимость нельзя.
2. **Original provenance gap остаётся.** Synthetic/native analysis с двумя полями может иметь свежий point_identity_json и stale **фактический** identity_json. При равных records/commit и refreshed sidecar SHA/commit receipt новый helper проверяет только посторонний alias и принимает противоречащую actual analysis identity. `validate_native_handle` проверяет schema/role/history/markers, но identity dataset не сверяет; canonical StateReader identity loop работает с full handle, а не sidecar. Этот путь достижим и через current/prior-final `verify_recovery_bundle` calls того же helper.

**Tests locators:** `tests/test_final_fixed_point_audit.py:245–259` пишет point_identity_json всем ролям; helper `native:76–78` также добавляет его автоматически. E2 `replace_analysis_identity_and_refresh:530–554` удаляет/изменяет только этот же неправильный path; tests557–591 поэтому проверяют согласованный synthetic alias, а не published native4 producer layout. Refresh bytes/SHA/receipt сделан корректно и не маскирует отказ checksum; независимость literal raw audit numbers сохранена. Недостаток именно в выборе container identity field.

**Минимальный ready repair contract:** present analysis copy связывается с actual analysis `metadata/identity_json` на том же уже открытом budgeted handle, без filename reopen, нового reader API, numerical evaluator или изменения native4 producer layout. Full продолжает использовать свой point_identity_json. Анализ absent-copy сохраняет прежний scoped return и не получает новый required metadata field. Stale/missing controls должны менять actual analysis identity_json и обновлять sidecar owner bytes/SHA + commit receipt; healthy control должен воспроизводить producer layout без fabricated full-owner identity alias. Добавить контроль actual-field mismatch при оставленном свежем alias, чтобы alias не заменил authoritative field. Tagged/nonfinite/finite0/legacy/recovery и Profile A остаются прежними.

**Уточнение ответственности original review.** В original v2 F1 доказано отсутствие какой-либо проверки sidecar identity, но буквальный locator `metadata/point_identity_json` для analysis был указан мной неточно. Это уточнение сохранено явно здесь; прошлый report остаётся byte-exact как часть provenance. Нельзя превращать ту неточную recommendation в обязательный формат. Нормативное требование bind к native role identity сохраняется, actual producer field является первичным.

Это один P1 с связанным fixture defect, а не два независимых требования расширить научный контракт. Никакой правки этим review не выполнено и дополнительный corrective loop не разрешён.

## Что корректно в E2 и что остаётся прежним

- Новые `_json_scalar`/equality calls расположены внутри `_validate_final_audit_sidecar(handle,...)`; callers `state.py:221–236` резервируют owner SHA obligation, хешируют и открывают HDF5 через **тот же** `_BudgetStream` и общий `_IOBudget`. Исправление selector не требует нового I/O path. Actual metadata read будет accounted тем же handle; это delivered stream bytes, не обещание физического disk/cgroup quota.
- Optional analysis без record возвращается до identity requirement; recovery payload с record запрещён; recovery commit presence, final canonical parity и present-null record rejection делегируются сохранённым branches/Contracts helper. Legacy absent+absent final сохраняет not_recorded, recovery absent — not_applicable. Новые healthy/missing/stale controls охватывают все шесть identity fields, но сейчас используют неправильный path.
- `_read_final_fixed_point_audit`/`_audit_attribute` byte-exact относительно reviewed v2. Profile A fixed atomic scalar type/space, charset ASCII/UTF8, width L..65536, разрешённые padding, raw read с тем же retained AttrID/file type, strict UTF8/exact constants и ExitStack cleanup не регрессировали. Genuine fixed/vlen/null/numeric/compound/array/opaque/hidden-suffix/bounds controls до строки527 не менялись. Старый conditional512 не применяется как норма.
- Canonical full audit cache private/immutable; bounded record parsing, schema/member/depth/unknown/nonfinite/rows/context и semantic pair equality остаются в published Contracts. Raw numeric values, reducers и public API не менялись. Results не выполняет acceptance equations и не повышает status measurement до pass.

## Новый explicit actual-producer control

`test_actual_runner_producer_transport_when_explicitly_bound:594–635` в source подготовлен корректно по запрошенной форме handoff:

1. Unset/empty env `QCL_SCI05_RUNNER_FIXTURE_ROOT` даёт явный `pytest.skip('not_run: ...')`; это не runtime producer evidence и не закрытие gate.
2. Переданный root должен быть absolute, а exact `root/archive/final/commit.json` обязан существовать; provided missing root/file приводит к assertion failure, search/fallback отсутствует.
3. Test только читает StateReader с expected execution/point/attempt2/plan и cap4MiB, проверяет generated state fields, pair measured/identity/shape/detail/zero/source_owner_role и оба owner paths. В теле нет вызова Python publish/native generator и нет solve.
4. SHA accounting ожидает оба actual full+analysis owners, а HDF/metadata reads входят в общий cap. Это test contract, а не измеренный объём существующего Julia output. Parent обязан отдельно связать actual call7 producer source, runtime receipt и сохранённые output hashes; один env path не удостоверяет происхождение файла.

Известный Runner v1 retained-path whitelist mismatch остаётся отдельным owning Runner repair и не исправляется в Results: v1 разрешал `/tmp/qcl-sci05-runner-portable-fixture`, intended measured root — `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`. Consumer path root/archive/final соответствует actual writer layout. Ни старый whitelist, ни будущий fixture не считаются исполненными или готовыми из-за наличия этого test. После F1-v4 known source incompatibility actual transport gate остаётся NOT_READY.

## Ограничения и STOP

Source review не доказывает actual loaded HDF5/JLL/h5py behavior, whole-process hostile-metadata RAM bound, отсутствие кратких resource peaks или native/library runtime безопасность. `_json_scalar` сохраняет исторический generic scalar JSON read; его применение к правильному identity field не является новым whole-reader allocation proof. Dataset dtype preflight и low-level dataset ID lifetime остаются ограничениями original review, без нового broadened claim. Historical `verify_recovery_bundle` не имеет StateReader maximum_io_bytes/counters API и не получает такую гарантию от новых helper calls; его inherited filename/loop behavior не переинтерпретируется как bounded StateReader proof.

Original C08 failed raws, v2/v3/v4 artifacts и explicit E2 provenance должны сохраняться. Shared consumed6/8 по parent, review добавляет0 и не сбрасывает ни scientific, ни engineering caps. Последующие owning исправления и immutable binding — отдельное решение coordinator; автоматического третьего/следующего цикла этот отчёт не разрешает. Core CPP2/E1, full S1 all-five/finite_chain4/current-bound/science gaps, native/release integration и final CI не переоткрывались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| E2 закрывает original sidecar identity gap | state.py214–218 | Использован full path вместо actual analysis identity_json; P1 | изменить |
| Новая identity read использует тот же общий budgeted handle | state.py221–236; helper handle calls | Неверный field selector; не whole-native RAM proof | сохранить |
| Profile A/D2 wire reader не регрессировал | native.py exact SHA + v2/v4 diff | Runtime не выполнялся | сохранить |
| Absence/recovery scoped compatibility сохранена | raw=None return, recovery reject, Contracts pair | Present-copy identity пока не совместима с producer | сохранить |
| Actual producer control подготовлен без Python fabrication | tests594–635, explicit env/path/assertions | Fixture не создан/не прочитан; F1-v4 и Runner path repair pending | дополнительно измерить |
| Численная/физическая/экспериментальная приёмка установлена | Новых вычислений/данных нет | Manufactured transport ≠ full S1/device oracle | данных недостаточно |

**STOP.** Sole output — этот report. Source product/tests, прежние artifacts и Git state не изменены. Verdict — REQUEST_CHANGES, source не eligible для call8 до закрытия P1.
