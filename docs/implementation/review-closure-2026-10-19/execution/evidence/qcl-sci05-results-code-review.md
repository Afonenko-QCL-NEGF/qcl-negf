# SCI05-N1 Results v2 — independent high source review

2026-10-19. **REQUEST_CHANGES / source NOT_READY:** найден один P1 provenance gap в optional `physics.analysis` copy: reader проверяет её record против commit, но не связывает с commit собственную native point identity sidecar. Profile-A attribute implementation соответствует принятому design на уровне source. Новых runtime/producer transport claims нет.

Scope≤25 min /1 CPU/2 GiB/read≤4 MiB/output≤64 KiB. Применён `qcl-results-analysis` для source-only format/reader review; primary D2 и adopted profile A сопоставлены с actual source/tests, author report прочитан после самостоятельной оценки source/test graph. Единственный новый файл — этот review. Python/HDF5/Julia imports, parser/tests/pytest/solver/build/install/network/Git mutations/source edits/children=0; C08 calls=0. Actual Julia producer→Results round-trip не выполнялся и из чтения source не выводится.

## Identity и входы

Candidate `/tmp/qcl-sci05-results-worktree`, actual HEAD/base `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`, branch `codex/review-closure-final-audit-reader`, recursive submodule status пуст. Actual status: modified `src/qcl_negf_results/{native,state}.py`, untracked `tests/test_final_fixed_point_audit.py`; других candidate изменений нет. `git diff --check` успешен. Прочитан owning CONTRIBUTING; он требует focused relevant healthy/rejection checks и отделяет synthetic reader fixtures от actual Julia producer/scientific validation. Новая scientific environment не поднималась.

| Проверенный вход / file | SHA256 |
| --- | --- |
| Frozen D2 `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| Profile A design | `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206` |
| Profile A independent review | `95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916` |
| `/tmp/qcl-checkpoint-attrs-design-ready.json` | `0806a115cb0515e4cba7f20131e32cdb44b0158ebb8a3f136197a95c4c6337fc` |
| `/tmp/qcl-sci05-results-v2-identity.json` | `078894c9107de84d123daa8e799cee535bd7ff3833a791f464185bff063810cc` |
| Actual patch `/tmp/qcl-sci05-results-v2-patch.diff` | `fb936c596a035670426ad64c90c4c97a2e0a663dfd663c34a594e51a2853a55e` |
| Author report `/tmp/qcl-sci05-results-v2-report.md` | `0f121f3f3f6cd699b516e5d713d408116e7a196a13f94ec1c7ebc056f375786a` |
| `src/qcl_negf_results/native.py` | `532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5` |
| `src/qcl_negf_results/state.py` | `57af749bbc0c5179707871ee43e75db01da2017faa242d08bd888c2aab8ef224` |
| `tests/test_final_fixed_point_audit.py` | `8d9b6b1dae1cc271494e26773be9a2c0551acfda578c7d10c8713b797208c082` |
| Prepared/published Contracts `final_audit.py` | `1c19ba7f27912c739b349fb7c517a9030be3c4f50c4b75932c08d0c02f3219d1` (source12fc264...) |

Prompt shorthand `...v2.patch` отсутствует; authoritative identity явно называет существующий `...v2-patch.diff`, его hash совпал. Это locator clarification, не product finding.

Original partial freeze artifacts сохранены с теми же фактическими hashes: initial report `f0baf6232f46095199c84c3951132d272224837d29fefd471cc77c47b73661f1`, identity `d252c817ccdb4997656a7845f38168c93eeaa9bc7f371e44646029fc26d3d0ac`, patch `46ca0c6f56dc884bf7cf08e1d9319621fadf104fdab1d6d6384559b535790f1e`. Initial<=512 conditional choice не считается нормой; принят cap profile A L..65536.

Это source audit, archive/run/attempt/model data не анализировались. Root selected ref в packet9d8cf0c..., owning Results basee2fdeda и prepared Contracts12fc264 различаются по ролям и не выдаются за source одного scientific run. Root concurrent publication/engineering state не изменялся этим review.

## F1 / P1 — present analysis copy не связывается с native point identity её owner

**Наблюдение:** `state.py:185–198::_validated_final_fixed_point_audit` для canonical physics.full после `validate_final_audit_pair` читает `metadata/point_identity_json`, требует его наличия и exact equality с owning commit identity. Но optional sidecar path `state.py:201–213::_validate_final_audit_sidecar` после чтения raw только вызывает тот же Contracts helper с `expected_identity=commit["identity"]`. Sidecar native point JSON вообще не читается.

`_verify_final_audit_sidecars:216–231` проверяет owner SHA, internal links/storage и `validate_native_handle`, затем вызывает этот incomplete sidecar helper. `validate_native_handle` проверяет role/schema/marker layout; `metadata/point_identity_json` им не связывается. Analogous helper используется также в current/prior-final loops `verify_recovery_bundle`. Hash/receipt equality не заменяет semantic native identity proof.

**Точный нарушенный contract:** D2 §8.7 требует bound state_identity против actual commit.identity **и native point identity**; optional analysis copy при наличии равна canonical record/source_owner_role=physics.full. Published Contracts `final_audit.py:411–434`, особенно docstring418, явно оставляет caller-у native point identity и owner-hash binding. Helper проверяет шесть record fields с commit, но не получает HDF5 handle и не может выполнить missing check за Results.

**Воспроизводимый source counterexample без исполнения:**

1. Взять existing literal `publish(..., record(), sidecar="physics.analysis", sidecar_value=record())` fixture, где canonical/native/commit records имеют IDENTITY attempt1.
2. В analysis owner изменить только `metadata/point_identity_json` на тот же object с attempt2 (так же возможны stale state_id/state_sequence/plan_fingerprint либо missing point identity). Audit record внутри analysis оставить canonical attempt1.
3. Обновить declared bytes/SHA этого sidecar и commit receipt SHA как для нового immutable artifact; не менять canonical physics.full или audit record.
4. Все new checks `StateReader→_verify_final_audit_sidecars→_validate_final_audit_sidecar` зависят от valid native schema и audit record/commit attempt1, но не от изменённого metadata JSON. Следовательно, противоречивая present analysis copy не будет отвергнута указанной native-identity проверкой. Это control-flow вывод, не runtime pass claim.

**Влияние:** reader принимает archive с internally contradictory provenance analysis owner как validated optional audit copy. Это software/format identity defect, не результат физики. `source_owner_role="physics.full"` у record указывает источник scientific arrays и не делает ложную native point identity контейнера допустимой.

**Контраргумент:** canonical physics.full уже связан с commit, analysis raw record byte/semantic-equal ему. Этого достаточно для идентичности самого JSON, но недостаточно для второго независимого утверждения, что этот JSON расположен в native owner той же point/attempt/state. D2 и docstring Contracts различают эти два binding obligations. Новое ограничение на historical group-absent analysis не требуется: finding относится только к **present final-audit analysis copy**.

**Отсутствующий distinguishing test:** `tests/test_final_fixed_point_audit.py:224–231` мутирует native point identity только canonical helper path. Tests288–306 для sidecars проверяют checksum/budget и contradictory `detail`, но не sidecar native point identity при неизменном copied record. Поэтому имеющиеся negative controls не ловят данный bypass.

**Решение: изменить.** Минимальная ожидаемая correction в уже принятом format scope: present analysis record должен пройти такой же actual native point identity binding на том же budgeted open handle, сохраняя recovery prohibition и optional absent-copy compatibility. Добавить healthy analysis copy + stale/missing native point identity controls при корректных refreshed SHA/receipt; не подменять это сравнением двух record copies. Это expectation для owning author, а не исправление, выполненное review. Нет необходимости менять JSON schema/physics/public API или получать новый scientific tolerance.

До закрытия F1 полный source PASS и расход единственного Results C08 slot не рекомендуются. Review сам не выделяет corrective round и не запускает повтор.

## Что source соответствует принятому profile A

`native.py:211–254::_audit_attribute/_read_audit_attribute_bytes`:

- Открывается только known attr name через `get_id`, без high getter/value read всех attrs. ExitStack немедленно регистрирует закрытие AttrID, file type и space; порядок cleanup обратный, включая failure на получении следующего ID.
- До NumPy type/buffer allocation проверяются H5T_STRING, non-vlen, H5S_SCALAR/shape(), затем widthL..65536, ASCII/UTF8, NULLTERM/NULLPAD/SPACEPAD. Vlen pointer size не используется как payload bound. Arbitrary attr dtype→NumPy conversion отсутствует.
- Синтезируется bounded scalar S<N>, вызывается read с **тем же retained datatype и AttrID**, затем tobytes. Между preflight и read нет reopen имени или high getter, поэтому этот path не создаёт type/name TOCTOU. Caller handle тот же StateReader budgeted owner handle.
- Padding снимается только справа; для SPACEPAD только space, иначе только NUL. Любой remaining NUL corrupt. Charset-specific strict decode и exact constant equality без normalization/strip/case folding.
- N=L canonical output без обязательного terminal NUL поддержан; width65536 остаётся явным engineering cap, не новой physical tolerance. Additional raw/decode copies имеют bounded constant factor; whole-process hostile-HDF5 metadata RAM claim не делается.

Синтетические profile tests независимы от product encoder: explicit H5A file/memory type fixtures, exact metadata/raw readback assertions до product helper; четыре constants×два charsets×три pad modes×три widths; NULLTERM hidden suffix/interior-NUL; invalid decode/values; genuine small vlen sentinel; NULL/vector/rank2/numeric/compound/array/opaque/N<L/N65537; missing each attr; guarded enum/absurd-width adapters. Same-ID/cleanup test453–494 проверяет одну lookup, retained same mtype, bounded read bytes и закрытие all3 IDs на success/preflight/read_error/wrong_value. Это prepared test source, не runtime evidence.

## Dataset wire checks и ограничения

`native.py:265–317::_read_final_fixed_point_audit` проверяет internal hard-link path/group, единственный child record_json, scalar fixed-S1..65536, non-object, STRING/non-vlen/UTF8, no chunks/compression/filters/external/virtual storage. Required four attributes проходят profile A. Dataset value читается raw same-type scalar buffer и right-padding handling не скрывает interior NUL; строгий JSON UTF8/NUL/BOM/duplicate-key/NaN/Inf/schema/semantic/depth/member/bytes checks делегированы published Contracts helper.

Две важные границы source claims:

- Dataset path получает high-level `dataset.dtype` до low-class check и проверяет strpad после bounded value read. Однако value buffer остаётся ограничен accepted fixed width; этот path не является доказательством отсутствия всех metadata/dtype allocations на произвольно hostile HDF5 descriptors. Новый строгий preflight-before-NumPy contract profile A выполнен именно для четырёх attrs, а не автоматически для всех historical metadata.
- Dataset type/create-plist handling не использует такой же явный ExitStack, как attrs; не следует заявлять одинаковую finally-дисциплину всех dataset low IDs из теста только attr cleanup. Future runtime/resource evidence и обычный owning-handle lifecycle остаются отдельны. По доступному source этого недостаточно для отдельного load-bearing leakage finding, и speculative blocker не вводится.

Header tests до payload-read покрывают vlen/ASCII/numeric/vector/oversize/extra child/wrong attr values; storage features используют adapters. Это полезно для branch assertions, но не actual Julia/HDF5 native round-trip или доказательство поведения всех malformed native descriptors.

## Canonical identity/equality, legacy и recovery

Canonical full-owner path корректно использует `validate_final_audit_pair`12fc264 и дополнительно связывает native point JSON с commit; `_same_json_value` не смешивает bool/int/float. Expected record identity содержит actual six fields; callback не восстанавливает модель/defaults и не оценивает science.

Native/commit presence обе absent в final даёт not_recorded, recovery absence — not_applicable/not_a_final_state. Present null/non-object commit key отвергается. Односторонняя presence, stale record attempt/state/sequence/plan, contradictory record detail, invalid strict JSON и partial_error finite0 должны сохранять Contracts outcomes. Error finite0 тест235–242 не превращает measurement error в measured0/pass. Неизмеренность не подставляется нулём.

Recovery commit forbidden nested key проверяется и до bundle loop; recovery payload final group отвергается helper201–210, включая recovery sidecar внутри final generation. Optional analysis raw absent допустим, present raw равен canonical commit record через Contracts. F1 — missing **native-container identity** этого present analysis path, а не отсутствие record↔commit equality как такового.

Tests содержат literal constructed record и literal JSON/receipt generation; expected values не получены из `encode_final_audit`, physical map/number reducer не вызывается. Из generic selector strings/empty scattering synthetic fixture нельзя выводить S1 all-five known context или physical accuracy. Consumers не добавляют нового numerical evaluator/public API.

Unknown-field/nonfinite/incomplete/inventory rejection целиком принадлежит published Contracts validator/schema; данный reader его вызывает вместо дублирования policy. Новый tests file не исчерпывает повторно весь Contracts negative matrix — часть cases проверена на стороне owning helper; source-level делегирование сохранено. Реальный import/version binding12fc264 при runtime ещё обязателен.

## Physical stream budget и immutable-handle scope

В StateReader путь positive:

1. Commit/receipt JSON читаются через `_BudgetStream` с общим `_IOBudget`.
2. Whole physics.full owner SHA verification и HDF5 fileobj driver используют **тот же** retained raw stream; `_verify_stream` возвращает позицию0. Existing internal storage rejects external/soft links и virtual/external datasets.
3. New attrs/dataset/native point identity reads canonical record идут через этот open budgeted handle; selected logical bytes не подменяют delivered stream accounting.
4. `_verify_final_audit_sidecars:216–231` для каждого declared analysis/recovery HDF owner сначала reserve-check полного size, потом SHA и HDF metadata/audit checks через новый _BudgetStream **с тем же общим budget**. Owned size/hash проверяются, handle не переоткрывается по имени между его SHA и metadata pass. Старый owner digest не подменяет equality/identity, что и показывает F1.

Tests200–206 и273–298 используют fresh one-byte/total-minus-one caps, ожидают budget failure, проверяют sum sidecar/full SHA bytes и positive metadata/HDF counters. Они не skip expensive verification при недостатке cap. Missing actual runtime оставляет callback/error propagation unmeasured, но source accounting graph для StateReader соответствует требованию.

`verify_recovery_bundle` отдельно сохраняет прежнюю public API без maximum_io_bytes и собственных counters; его inherited dependency hash/native validation loops не являются StateReader aggregate-budget guarantee. Новые final-audit checks в них не создают ограничение всего старого recovery-verification I/O. В particular prior-final path читает HDF filename после separate dependency hash pass, как до patch. Это существующая граница этой API, не вновь установленный same-retained-handle/physical-budget proof. Не распространять авторскую формулировку про общий budget StateReader на все public verifier routes без отдельного assigned contract.

Immutable archived-file/owner checks остаются прежними. Value-width cap/byte counters не доказывают hard RAM sandbox native HDF metadata или защиту от concurrent adversarial writer; reader предназначен для verified immutable owner, а не нового live trust mode.

## Remaining gates, бюджет и STOP

Author report корректно не заявляет CP-CODE/runtime pass и actual Julia transport. Source conclusion: adopted profile A реализован, canonical StateReader pair/budget path в основном соответствует D2; F1 блокирует full source acceptance. No model/threshold/equilibrium reduction/CLI/public API changes в diff не обнаружено.

По поручению общий C08 consumed6/8; оставшиеся slots предназначены Runner и Results. Этот review не увеличивает cap, не расходует вызов и не даёт automatic rerun loop. Нужны owning correction/review с exact new source binding и только затем выделенный targeted Results call. Actual pinned Julia producer→Results transport остаётся future integration evidence даже после синтетического Python GREEN; Core software acceptance и attribute design approval его не заменяют.

Все full S1 all-five/current-bound/discretization/physical acceptance gaps остаются вне этого I scope. Любое новое numerical/model/criteria решение требует своего owning contract, не дописывается в Results ради GREEN.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Results v2 source готов без blockers | F1 sidecar-native identity bypass с точным caller graph | Runtime не запускался; source counterexample достаточен | изменить |
| Profile A attrs faithful и bounded new value-read path | native211–254, same IDs/type, ExitStack, strict width/charset/pad/constants | Native linked behaviour/whole-process RAM не доказаны | сохранить |
| Canonical pair/legacy/recovery format policy делегирована owning Contracts | state185–198, Contracts411–434, literal fixtures | Analysis-container binding incomplete F1 | сохранить |
| StateReader считает sidecar SHA+metadata в том же budget | state216–231, tests273–298 | Не blanket guarantee старого verify_recovery_bundle API | сохранить |
| Source fixtures доказывают Julia producer round-trip/scientific pass | Такого исполнения нет | Synthetic-only prepared source, remaining integration/science gates | данных недостаточно |

STOP после отчёта. No implementation или execution проверяющим.
