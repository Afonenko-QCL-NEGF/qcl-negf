# OPS03 local identity — независимый narrow CP-DESIGN

**Вердикт: PASS для exact варианта B как trusted-direct/process-only primitive.** Можно реализовать описанное уточнение binder/ordering/controls в существующем OPS03 edit set. Это не CP-CODE и не разрешение native операции с None. Full node assertion и process ownership остаются разными фактами.

## Source-first и binding

До D note прочитаны accepted OPS02 §§3–4, actual candidate owner/activation/CLI и native controller/worker callers; собственное наблюдение передано coordinator до чтения author conclusion. Основная граница: actual PID/start/boot + runtime/lock/release/deadline не удостоверяет full configured/enrolled node. Existing CLI activate проверяет protected settings.role; prepare-initial branch эквивалентной проверки не имеет.

SHA-256 независимо пересчитаны:

| Input | SHA-256 |
| --- | --- |
| Design note | c673a2b11df3be0096388b0280cc4714271be90c9dc11e11c409a59b25f4bfee |
| Question | ec2b485b779d299cb84f8d996833c442a4d42bffcfdb004407e920461230583d |
| Frozen candidate patch | 8de400d2bae1c39bfbe265d3b8285676b975914d8fefb5fa1a573c108ef74fc1 |
| application_release.py | 750198092c6f123b7a8baf2ba82129f6b1b2ee597edce002c327544bd5a09472 |
| worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |

Platform gitlink/HEAD 6c5b11f3c74d44fed8b2c159f890b83e0b5456b9; dirty candidate совпадает с frozen hashes. Root snapshot при чтении 7d179b28647f0b89347d2d6358f08cf2fe479653; unrelated Runner/root/Portal activity не относится к этой приёмке. Прочитаны architecture, Platform CONTRIBUTING, OPS02/03 handoff и autonomy; historical PLAN statements не отменяют переданное coordinator действующее EXEC/resource grant.

## Spec и качество

1. **B явно ограничен trusted interpreter** (note:38–69). None не wildcard/enrollment, returned record не получает invented node_identity. Сохранение configurable run/profile/runtime/gate объясняет API boundary, но не доказывает безопасность произвольной maintenance цели. Note:200–210 отдельно запрещает наследование operational permission из source pass/root privileges. Нет нового unsafe flag, observer/trust root, автоматического guest probe или switch по UID/temp/run identity.
2. **Точный immutable bind до journal** (note:87–141): pure private seam нормализует valid role и identity, копирует flat values, фиксирует actual process boot; whole_update и worker update не принимают None. Full↔None/role/identity drift на том же owner запрещён; repeat exact equality допустим. Existing observer/stopped proof должен пройти до _begin_local_mutation/ready unlink/mask removal. Final checks используют snapshot, не caller dict. Это исправляет candidate ordering, где _begin_local_mutation сейчас предшествует optional node validation (application_release.py:1387–1402); frozen candidate пока не CP-CODE accepted.
3. **Stopped worker не заменяется running probe**: existing observe_stopped_update + bind_node_observation до mask removal и full assert после restart. Это сохраняет supported stopped-daemon route и не создаёт новый trust probe.
4. **Production call-site audit соответствует owning source**: controller local helper :2756–2760 получает literal controller и explicit enrolled binding; remote update :2774 и startup worker_lifecycle.py:493–498,526 получают full expected flags/own stop-or-startup context. По source search в root/native components иных direct wrapper callers не найдено; Nix wrapper передаёт CLI argv, AiiDA guard/readers не являются activation calls. Никакой production caller не может молча заменить уже установленную full binding на None.
5. **Существенная точность CLI scope**: note:150,176 сохраняет существующий standalone CLI с omitted expected: protected settings.role check + process ownership, без full node assertion. Это не означает, что *каждый* CLI invocation имеет full identity. Primary OPS03 handoff прямо сохраняет `activate --manifest RELEASE --role controller` без обязательного нового expected flag; поэтому blanket mandatory full identity на этом CLI было бы отдельным изменением контракта/совместимости. Настоящий PASS относится к B и этой явной existing CLI границе, не к утверждению «все native entrypoints доказывают full node». Root обязан сохранять это различие в readiness. Prepare-initial protected-role gap назван note:178, не объявлен устранённым и не оправдан правами interpreter; provisioning/OS writers и CR04 atomic admission residual также не waived.
6. **LI01–LI10 различают нужные отказы**: две valid roles/process-only без observer; invalid role/update None; schema/role/boot mismatch; provided pre-observation mismatch; final drift и mutable input отдельно; whole_update None; same-owner rebind; CLI role mismatch; supported stopped worker; existing ownership/unknown/gate controls. Pure binder и positive validator не mock-ятся. LI05 должен оставаться двумя различимыми cases (actual drift inhibiting intent vs caller-dict mutation not changing snapshot). LI10 ссылается на actual O-controls, не заменяет их повторным зелёным label. Дополнительный test invocation этим D review не дан.

Согласование reviewer не является proof runtime. Все rejection-before-mutation, immutable snapshot и final ready predicates ещё должны быть проверены в exact implementation и finite fixtures. Existing synthetic fake observer должен иметь boot, согласованный с fake process generation, без глобального смешения controller/worker.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Trusted direct None допустим как process-only primitive | Explicit B; configurable existing API; owner generation/inode/gate checks | Нет full node/target/admission authority | сохранить |
| Уже provided full node context не может деградировать до None | Once-only binder + whole/update requirements + LI03–07/09 | Пока design, candidate ordering требует реализации | изменить |
| Existing CLI role check сохраняется при None | main:2986–2993; LI08 | Full node assertion отсутствует при omitted expected; prepare gap остаётся | сохранить |
| Native production operation безопасна/разрешена этим PASS | Такого evidence нет | Нужны separate exact CP-OPS BIND/grant/target/window/trust/rollback и required source/native gates | данных недостаточно |
| OPS03 narrow implementation готова продолжаться | Exact accepted B interface/errors/controls/callers | CP-CODE/runtime и broader release gates открыты | изменить |

Новых blocking gaps в exact B note не найдено. Reviewer не менял product/harness, не запускал imports/tests/native/Nix/SSH/services/build, не делал Git mutation; только source/text/hash inspection и этот /tmp report.
