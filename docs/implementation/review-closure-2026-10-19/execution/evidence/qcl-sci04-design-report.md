# SCI04-D1 — author report

2026-10-19. Выполнен source/design audit до SCI05; независимый CP-DESIGN ещё
нужен. Deliverable: `/tmp/qcl-sci04-design.md`. Никакого numerical acceptance
или runtime READY не заявляется. Автор не является независимым reviewer.

## Выполненные действия и сохранённые границы

Прочитаны supplied/root AGENTS, architecture, qcl-physics-audit и его памятка,
science SCI03/04/05/06, P1/autonomy checkpoints, approved SCI03-D2/owningdoc
bindings; адресно прочитаны immutable production source и existing scalar test.
Сняты root HEAD/status/submodule status. Fresh Core production `src/` diff с
HEAD пуст. Git использовался read-only с GIT_OPTIONAL_LOCKS=0.

Делались только чтения текста, rg/sed и stdlib hashlib/Path для source hashes,
запись двух `/tmp` документов. Не запускались Julia/imports/tests, solver,
SCBA/Poisson experiment, benchmark/profile/install/build, native/server probes,
submit, архивные scripts или чтение научных массивов. Git mutation отсутствует.
Old S01 не затронут. Никакие component code/docs этим task не менялись.

Доступные четыре agent slots были заняты: отдельный reviewer в этом task не
создавался. Координатору переданы source observations; согласована граница
с final_ug_design, который отдельно ведёт DEV05. Его failed first GREEN и
планируемый D2 не являются accepted numerical evidence этого отчёта.

Наблюдавшийся root status содержал concurrent Core docs/untracked fixture,
AiiDA gitlink+changes, Platform internals, Research untracked owning SCI03 doc,
root checkpoint/system docs/evidence/tooling. Они не включены в production
source claims и сохранены. Actual submodule status:

| Component | Actual checkout commit | Root gitlink relation |
| --- | --- | --- |
| Core | f5b73369a96d1225bd96fb34f5262c8dcf965f86 | matches; concurrent docs/test overlay |
| Runner | 2d0190d5573f74d847d92a0dac8dd6ec524d494c | matches |
| AiiDA | 312ed8a6363103d05a971d14ac9cbcca1c782358 | differs (+); вне данного audit |
| Contracts | 26cacbe1688fee0af300d0949fc6b94e55a29f4a | matches |
| Platform | 6c5b11f3c74d44fed8b2c159f890b83e0b5456b9 | matches; concurrent overlay |
| Portal | ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363 | matches |
| Research | b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3 | matches; untracked SCI03 doc |
| Results | 17574ca4c5495f74d86ed9bef51c60dea8265062 | matches |

Дизайн: 31278 bytes; SHA256 `c4e61ff6a9aac94c349b9e941f35f8652606928a7be7c3a23e22245adbaf49fc`.

## Findings и ready next action

Production final snapshot/map/Poisson control flow можно переиспользовать.
SCI05 skip не обоснован: final raw norm components и explicit availability/
lineage record отсутствуют, stationary summary не требует candidate rD/rA/λ,
existing scalar test не закрывает coupled/full transport negative controls.
Design задаёт два bounded owning tickets C1/N1, compatible interfaces, exact
dataset semantics, independent literal scalar/2×2/Poisson controls и failure
semantics. Threshold/model/grid/kernel changes исключены.

Ближайший checkpoint — independent CP-DESIGN над exact design bytes/hash,
production source hashes ниже и approved SCI03 context. Только после pass
координатор назначает owning I с оставшимся общим C08 cap. Admission/BIND и
научные arrays/plans здесь unknown; runtime SCI не готов.

## Source byte manifest

Пути относительно immutable workspace; SHA256 — bytes прочитанных файлов.
Core C=f5b73369, Runner N=2d0190d5, Contracts K=26cacbe1,
Results V=17574ca4, Research R=b1a3be2b; root=9f8b08bb. Это audit receipt,
не параллельный source lock. Research measurement doc — согласованный untracked
SCI03 owning artifact, hash связывает exact overlay.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| docs/architecture.md | 5501 | 8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7 |
| docs/implementation/review-closure-2026-10-19/science.md | 42428 | 0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a |
| docs/implementation/review-closure-2026-10-19/autonomy.md | 29026 | 056fb2bcbca56ea7700fa2a4de36b0da9ad7533a44e4e6b0dfcfab94ed76b1bd |
| docs/implementation/review-closure-2026-10-19/operator-permissions.md | 32033 | 4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0 |
| C/src/numerics/reference/final_audit.jl | 17312 | 8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673 |
| C/src/numerics/reference/validation.jl | 30956 | 29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a |
| C/src/numerics/reference/poisson.jl | 2385 | 8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645 |
| C/src/numerics/optimized/production_solver.jl | 52279 | ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa |
| C/src/numerics/optimized/certification.jl | 5278 | de2dd971a8d466b53b0b2b4c682e085c743cd789b7e9e0c839f0a9042c5a13e3 |
| C/src/numerics/optimized/production_operators.jl | 50736 | 7b4e6cd55b259a2477b799ecfb30ae818ce17a3bbf5c6ff81d2087af17bb62df |
| C/test/numerics/fresh_candidate_residual.jl | 1276 | 8ab459b5be0c39f96839b862aad38e1dbcd6a8dc633770838fd239c8a871a6a0 |
| N/src/infrastructure/persistence/physics_diagnostics.jl | 17287 | 9f54466882634797a165e30c156b3e7bd2e64f9156da7a7549ef0c5cda2fc043 |
| N/src/infrastructure/persistence/hdf5.jl | 30957 | c946ba5fb71f035d1a0b564b561700b9a5c3360ed67bf890c668b0ced769d511 |
| N/src/infrastructure/persistence/point_artifacts.jl | 76808 | 81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a |
| N/src/infrastructure/persistence/light_results.jl | 10363 | 75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06 |
| K/src/qcl_negf_contracts/artifacts.py | 13757 | 639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa |
| V/src/qcl_negf_results/state.py | 25269 | a8e96fc0edcc087aa71126dcbad57bc3ab2acdddbef4630b17c685dcafa7d323 |
| V/src/qcl_negf_results/native.py | 10798 | 892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b |
| V/src/qcl_negf_results/equilibrium.py | 31385 | 3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6 |
| R/docs/equilibrium-measurement-contract.md | 45385 | 758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f |

| C/src/domain/types.jl | 36507 | f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b |
| C/src/numerics/reference/acceptance_metadata.jl | 30629 | 4d1880b7d6e475534d0bbfa229ced25dd40b062f674ec8a2ea86b45e0db1dd86 |
| C/src/numerics/reference/periodicity.jl | 16572 | b7c3b7098ae1ed79492f6a84ddd1e55ba53e14fa703c264c2c4a8ff0f3864b35 |
| C/src/physics/observables.jl | 16436 | b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f |
| N/src/infrastructure/persistence/scientific_history.jl | 12277 | afecbfb4ad3716af06c0ee0d7fc49563387b69948061a0102f1240e1ab6189a1 |
| N/src/infrastructure/persistence/physical_markers.jl | 20138 | 30daf04f72a14557af815a7cb51ad2a250c5a46b6788b8bad41fb86826dce65b |

## Итог

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Production source имеет fresh aligned final map | Pinned source trace design §2–3 | Не runtime result | сохранить |
| SCI03 raw evidence уже полно сериализован | Existing fields против missing norm/availability record | Только ratios/occupied numbers/history сохранены | изменить |
| Existing физическая задача сохраняется при closure | Narrow append-only C1/N1 и literal oracle | Physical/code evidence остаются раздельны | сохранить |
| Tests/scientific acceptance выполнены | Ни одного такого запуска не было | CP-DESIGN/I/runtime gates впереди | данных недостаточно |
