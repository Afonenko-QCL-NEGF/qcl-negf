# SCI05-N1 Runner E3 v2: независимый CP-CODE source review

Дата: 2026-10-19. **REQUEST_CHANGES / SOURCE_NOT_READY.** F1–F5 исходного review исправлены по исходникам. При проверке полного recovery-role contract и различающей силы новых controls найдены ещё два конкретных gap, перечисленные ниже. Никаких target imports/parser/Julia/Python/tests/solver/build/install/network/server/Git mutations/children не выполнялось. C08 reviewer: **0**, общий consumed6/8 по coordinator не изменён.

## Frozen source и порядок проверки

Worktree `/tmp/qcl-sci05-runner-worktree`, HEAD/base `9378396a3681c1eddf2c62f16674834fc4465583`, branch `codex/review-closure-final-audit-writer`. Status: четыре modified tracked paths и один untracked test; light_results.jl unchanged. Recursive submodules отсутствуют. `git diff --check` exit0. Прочитаны actual source/test, v1→v2 patch delta, D2 recovery/native binding и прежние primary profile A/source conclusions; затем авторский v2 report. Старые пакеты/review сохраняются, verdict ими не подменялся.

| Артефакт / source | SHA256 |
| --- | --- |
| `/tmp/qcl-sci05-runner-v2-identity.json` | `0616f8d9fd3043e93b97497b0173a6a6ad1cbb218dce01829e5dc2a97a2c2338` |
| `/tmp/qcl-sci05-runner-v2-patch.diff` | `3987f6cdcbd798c06a277fd02d4774c8a82e6cc41c5fa442409f0ed185c1f316` |
| `/tmp/qcl-sci05-runner-v2-report.md` | `7cbfb82840b81fc91250026676bc274ba6a0f14d4d86148946f16a4b924bf020` |
| `src/infrastructure/persistence/physics_diagnostics.jl` | `66a0eb7072c6ba871d1009d8543a103c30c9cc28f0b6640c9f7a511daa417f7c` |
| `src/infrastructure/persistence/hdf5.jl` | `d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143` |
| `src/infrastructure/persistence/point_artifacts.jl` | `9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4` |
| `src/infrastructure/persistence/light_results.jl` unchanged | `75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06` |
| `test/infrastructure/final_fixed_point_audit.jl` | `282471a5ca516ad0c4806451e86d483bfe6339232579e6e2ea69c764c9ca4dce` |
| `docs/src/user/results.md` | `cc302e70fe27ac11f0820fbe9675731c21393c7e37f373310e13abd0c1fbbd44` |
| Initial review `/tmp/qcl-sci05-runner-code-review.md` | `b1c995927188a1c21879ec56e14020b893ba5cee67f2c51884af8e52fa0f696c` |

Primary D2 `/tmp/qcl-sci04-design-v2.md` SHA `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`; profile A design SHA `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206`, independent accepted review `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916`. Core7324/Contracts12fc read bindings сохранены; production Core этим patch не меняется.

## F1–F5 closure

| Original finding | Actual source / authored control | Вывод source review |
| --- | --- | --- |
| F1 null ≠ absence | physics_diagnostics:631–642 uses record_present=haskey; recovery требует !record_present, final present non-object отвергается. Test257–266 проверяет copied recovery/legacy explicit-null, healthy absence сохранена | Закрыт по исходникам; tests not_run |
| F2 optional analysis | helper role от actual artifact в point_artifacts:1186/1189; absent analysis audit допускается после проверки present-null. Test216–229 удаляет group с refreshed actual owner bytes/SHA и проверяет positive; contradictory present analysis negative | Закрыт по исходникам; canonical full parity сохранён |
| F3 native binding без legacy marker | physics_diagnostics:647–652 требует analysis identity_json либо full point_identity_json и все шесть actual fields независимо от top-level state_id. Test230–250 содержит healthy marker removal и missing/stale metadata controls обеих ролей | Production gap закрыт; full negative controls имеют отдельный F7 ниже |
| F4 safe Int ceiling | physics_diagnostics:502 проверяет `1<=value<=9007199254740991`, non-Bool Integer. Test70–75 содержит max-valid/max+1 обоих fields | Закрыт по исходникам, без coercion/порогов физики |
| F5 measured TMP | test:7/276–285 exact whitelist `/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture`; historical/suffix paths rejected; fresh-path guard сохранён | Закрыт по исходникам; actual output ещё не создан |

Actual analysis field `metadata/identity_json` подтверждён существующим Runner writer `point_artifacts:304–317` и verifier role selector1176–1181. Full field — `metadata/point_identity_json` (`hdf5:295`). Уточнение предыдущего consumer review не стало требованием создавать новый alias в native4: здесь выбран правильный role field. В новый record записываются ровно шесть полей; native metadata может содержать существующие дополнительные поля, которые не превращаются в record inventory.

## Новые коллированные findings

### F6 — P1: HDF recovery owner в final archive обрабатывается как canonical final owner

**Локаторы:** `physics_diagnostics.jl::_verify_final_audit_pair:630–646`, особенно `final_state=get(commit,"storage_class",nothing)=="archive"` и отсутствие отдельной ветки `role=="recovery"`; `point_artifacts.jl:1185–1187` вызывает helper и для checkpoint schema с actual role. `_NATIVE_SCIENCE_ROLES` в `hdf5.jl:181` сопоставляет `qcl-negf-checkpoint-v4` с `recovery`.

D2 §8.7 прямо различает recovery generation и recovery payload внутри final generation: canonical record сравнивается с physics.full, **recovery payload group запрещён и в equality не участвует**. Новый role argument используется только для optional analysis и выбора identity path. При `storage_class="archive"` role recovery не влияет на scope.

Отсюда два противоположных нарушения одной missing role branch:

- Корректный archive с canonical full+commit audit и дополнительным HDF checkpoint/recovery owner **без** audit group отвергается `final audit presence differs` на646. Его group по контракту и должна отсутствовать.
- Тот же recovery owner **с** равной audit group, правильной point_identity_json и storage headers может пройти все проверки helper. Это запрещённое финальное свидетельство в recovery payload. Type/schema/hash checks не мешают: checkpoint-v4 роль recovery является поддержанным native role, а helper принимает его actual role и продолжает final equality.

Дешёвый различающий контроль без solve: к manufactured archive добавить HDF checkpoint owner либо заменить recovery reference declaration на checkpoint HDF declaration. Можно скопировать tiny native full payload, установить соответствующие checkpoint-v4 schema/recovery role, дать отдельный path и корректные bytes/SHA/identity. Positive case удаляет audit group; negative case оставляет identical final group. Public verifier должен принять первое и отвергнуть второе. Existing recovery.json reference в обычном writer — JSON, поэтому этот HDF branch им не покрыт. Existing test251–260 проверяет recovery **generation**, а не recovery **role** в archive.

Минимальный repair contract: presence guard для native role recovery действует независимо от commit storage_class. Recovery HDF без group в archive допускается и не сравнивается с canonical commit final record; recovery HDF с group всегда отвергается. Для recovery generation запрет nested key остаётся. Full/analysis binding и absent/null distinctions не ослабляются. Нужны оба role-specific controls с валидными schema/role/hash, без пересчёта physics и без изменения format policy.

Это существующая явная ветвь D2 и owning caller path, не предложение нового формата. Необходимость полного второго schema engine либо scientific-contract reopen из finding не следует.

### F7 — P2: full-owner F3 negatives не обнаружат удаление проверяемого identity guard

**Локаторы:** `test/infrastructure/final_fixed_point_audit.jl::mutated_bundle_check:138–156` обновляет только `artifact[bytes/sha256]`; full identity mutants находятся232–248. Existing `point_artifacts.jl::_verify_recovery_reference:101–108` отдельно проверяет `recovery.json.payload.bytes/sha256` против actual physics.h5.

Каждый produced tiny archive содержит recovery.json, ссылающийся на исходный physics.h5 hash/bytes (`commit_point_artifacts:828–851`). Когда F3 mutant меняет full physics.h5 identity, copied helper обновляет declared full owner SHA, **но оставляет recovery.json.payload прежним**. Если удалить/обойти новую native identity check, `verify_point_artifacts` всё равно бросит ArgumentError позднее в `_verify_recovery_reference` на107–108. Поэтому `@test_throws ArgumentError` остаётся green при именно той регрессии, которую должен различать. Это не hypothetical hash mismatch: source helper явно не обновляет JSON dependency reference. Correct implementation сейчас отвергает раньше по нужной причине, но runtime green такого test не докажет чувствительность oracle к guard removal.

Analysis mutants не меняют canonical physics.h5, поэтому конкретно этот nested recovery-reference hash conflict их не маскирует. Healthy marker-removal controls также оставляют full bytes неизменными. F1 null controls не меняют HDF owner и остаются различающими.

Минимальный repair contract: после full-owner mutation привести recovery.json payload bytes/SHA к actual full bytes, затем обновить declaration самого recovery.json и записать modified commit; либо использовать валидный controlled bundle без этой отдельной recovery reference obligation. Сохранить все обязательные dependency/owner gates, canonical untouched source и healthy copied control. Различающий test должен перестать удовлетворять `@test_throws` при удалении только новой identity check. Receipt не является входом public verify_point_artifacts, поэтому требование обновить её здесь не вводится.

Никакой реализации или guard-removal execution reviewer не выполнял. Finding установлен непосредственно по двум независимым hash obligations и их call order. Это тестовая доказательность, не утверждение дефекта production full identity correction.

## Остальной scope и ограничения

- Единственный bound object по-прежнему создаётся после actual state_id/sequence и переносится в full/analysis/commit. Recovery generation не получает supplied Core template. Numerical arrays/layout/ratios и public required arguments не менялись.
- Candidate Dyson/spectral/lambda required stationary list и старые Core thresholds не регрессировали. Status error/nonfinite/missing/unavailable-zero handling сохранён, full evaluator остаётся authority. Никакого numeric criterion widening нет; разрешение отсутствующей analysis copy восстанавливает frozen D2, а не расширяет его.
- Profile A producer recipe unchanged: scalar instance String fixed UTF8, четыре exact constants заданы до generic annotation, которая сохраняет existing attrs. Existing attribute cap/shape/cset checks и native equality сохранены. Авторский trusted-producer transport guard не выдаётся за полный hostile JSON/native sandbox.
- New test imports SHA stdlib; это source dependency, reviewer его не импортировал. Copied tests пишут только owned mktempdir; original retained canonical archive не мутируется. Права existing generation files допускают owner write (existing chmod640), так что источник здесь не показывает отдельного permission blocker. No runtime claim из этого не следует.
- Retained fixture root и archive/final layout совпадают с запрошенным consumer handoff; source не доказывает наличие actual bytes. Запуск call7 и actual Results call8 остаются отдельными coordinator gates. Results v4 известный wrong analysis path исправляется своим owning scope; Runner не должен подстраивать published native4 layout добавлением alias ради consumer green.
- Source hashes/Git diff не устанавливают Julia parse/runtime behavior, loaded native libraries, actual I/O/RAM/time, full release CI или independent device physics. Synthetic literal measurements не являются согласованным physical fixed-point oracle и не закрывают full S1 all-five/e–e/finite_chain4/current-bound/discretization/experiment.

## Решение / STOP

F1–F5 source closure признано, но общий Runner N1 CP-CODE source PASS не выдан из-за F6/F7. Original review/freeze и E3 provenance должны сохраняться. Это review не разрешает новый corrective round, reset общего effective cap5, дополнительный runtime invocation или auto-rerun. Coordinator отдельно сопоставляет эти конкретные gaps с действующим разрешением; при отсутствии дальнейшего engineering grant остаётся blocker. Core закрытый CPP2/E1 scope не переоткрывался.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Original F1–F5 corrected | Helper presence/role identity/Int branches, exact TMP guard и controls | Tests not_run; full control issue F7 | сохранить |
| Recovery payload scope соответствует D2 во всех поддержанных roles | helper630–646 + checkpoint caller1185 | F6 archive recovery HDF branch перепутан с full | изменить |
| Full identity negative oracle различает guard removal | copied owner SHA refresh + expected ArgumentError | F7 nested recovery.json reference stale | изменить |
| Physical model/criteria/native4 identity layout сохранены | v1→v2 delta, Core limits unchanged, actual role fields | Source only, не scientific/runtime acceptance | сохранить |
| Actual producer→Results handoff выполнен | Есть согласованные будущие paths | Bytes/runtime отсутствуют; consumer отдельный blocker | дополнительно измерить |
| Научная/экспериментальная приёмка достигнута | Нового scientific evidence нет | Manufactured transport-only scope | данных недостаточно |

**STOP.** Sole output — этот report. Product/tests/archives/Git state не изменены. Все выявленные замечания собраны выше; C08=0.
