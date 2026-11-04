# Как рос слой memory/admission: история доступного Source

Код и инфраструктура остаются остановленными по поручению пользователя. Этот документ расширяет
evidence за пределы27октября: от первых доступных Git imports до опубликованных Platform c470 и
Runner97. Новые tests, builds, VM/PG operations, resource probes или scientific runs не выполнялись.
Дальнейшая переработка здесь не начинается.

Наблюдаемая история содержит **два разных витка усложнения**. Первый — переход от обычных resource
estimates и native limits к строгому campaign/per-effect proof20–23окт; его обязательность явно
сняли24окт, затем код удалили28–30окт. Второй — новый host-memory broker для resident VM,
grow/readback и выдачи workload authority, дополненный native-attempt custody и qualification. Эти
scopes различаются, поэтому это не простое переименование удалённого strict режима. Но повторился
процессный риск: локальные safety obligations развивались в самостоятельную proof infrastructure
раньше связной установленной пользовательской цепочки. Fixed-first альтернатива была записана не
только в плане27окт, но и в самой implementation foundation28окт.

Выражение «второе ядро Linux» передаёт ощущение дополнительного слоя принятия решений, но буквально
неверно. Linux продолжал управлять страницами, процессами и cgroups; Slurm — выбирать worker и
allocation; PVE/libvirt — выполнять native VM operations. Собственный код добавил **broker ресурсов,
authorization controller, журналы неопределённых исходов и проверку происхождения evidence**. Это
существенно больше тонкого wrapper, однако не новый kernel, physical allocator или полноценная
замена Slurm scheduler.

## 1. Полнота и предел исторического чтения

Локальная история не shallow. Для заданных published heads просмотрены metadata всех222 ancestor
commits Platform `c47097225a4a798e4124e30245c7b5b2063eb32a`,104 Runner
`97ab889ff83b73d9fad5d34e278309b2efe3b299` и312 Root `a29fe2fb19aba0bab216c520653627316f099cce`. Это
commits, включая merge records; не количество независимых features или действий агента. Выполнены
path histories, birth/removal checks, чтение исходных файлов, значимых diffs и связанных
design/policy документов. Семантический аудит каждой строки всех трёх repositories этим не
объявляется.

Самые ранние доступные roots: Platform `66115da942ed46e61fb60e95f33d9d9b5a8137bd`, Runner
`c924d07dfa32949c72d390252a8cfd584668d6c9`, Root
`1e10299e99f8d9f73a5dc3d3b53141459091d1fa`,26сентября2026. Они названы initial public/integrated
source и **уже содержат работающие по замыслу modules и contracts**. Это граница доступной Git
истории, не доказанная дата изобретения кода или постановки требований. Нельзя приписать
импортированную логику конкретному разговору, человеку или агенту до этой границы. Non-shallow не
означает, что внешняя prehistory доступна.

Даты pivot ниже — даты соответствующих commits, прежде всего author dates; merge/publication может
быть позже. Например, Root4bd1085 имеет author time24окт11:35 и commit time15:41. Публичный Source и
record reason — факт истории; наличие tests в commit не означает, что этот исторический review их
исполнил. Private history inventory
`.build/session-evidence-followup-20261104/repository-history-inventory.json` — локальный указатель,
не приложение public PR. Signing-key directory не читался; private inventory/operational identifiers
не публикуются.

## 2. Pivots: от native ограничений к нескольким слоям допуска

| Pivot и ранний доступный Source                                                                                                                                                                                                                                                                                                                                                                                                                     | Записанная причина и фактическое изменение                                                                                                                                                                                                                                                                                                                                                                                                            | Что установлено / что не установлено                                                                                                                                                                                                                                                                                       | Альтернатива и степень выбора                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **H01 — импорт26сент.** Runner[c924d07](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/tree/c924d07dfa32949c72d390252a8cfd584668d6c9/src/infrastructure/resources), `linux_resources.jl`, `resource_contract.jl`, `native_phase_telemetry.jl`; Platform[66115da](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/66115da942ed46e61fb60e95f33d9d9b5a8137bd/modules/cluster.nix).                                                  | Runner уже читает affinity и все applicable cgroup ancestor bounds, имеет `ExecutionEnvelope` с numerical/runtime/allocator allowances. `_native_phase_memory_permit!` сверяет burst с headroom, при нехватке делает full GC/recheck и может выбросить pressure exception. Slurm config уже использует `select/cons_tres`, `CR_Core_Memory`, backfill, task/proctrack/cgroup и RAM constraints.                                                       | Самописное application admission **не родилось27окт**. В initial import нет найденного `campaign_strict`; ordinary callbacks ещё допускают unavailable при отсутствии некоторых данных. Source не доказывает установленный Slurm/limit или safe recovery после OOM.                                                        | Можно было исходно полагаться на estimates+external limits; но причины выбора initial callback до импорта неизвестны. Kernel и Slurm не заменялись.                                                                                         |
| **H02 —2–8окт: host/deploy ownership и process evidence.** Platform[2cd3f00](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/2cd3f00ae8de921e4f4493ad3a4e50e293490f38), [c50a771](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/c50a771a1ce4fbfc4ece5d4309cda65cb21ed458), [bbcaf47](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/bbcaf47d82c7caf47784629ef3f77eaa555586a4).                         | Первые commits описывают isolated host policy, application release admission, CPU worker lifecycle; затем `slurm_job_evidence.py` сохраняет strict read-only process evidence. Initial `application_release.py` был313строками нового файла, с release-ready gate и native subprocess.                                                                                                                                                                | Слой ownership/stop/readiness предшествовал новому memory broker. Он отвечал на deployment/maintenance safety, а не на физику. Из commit message и Source нельзя получить полную историю человеческого поручения или Native результат.                                                                                     | Native status остаётся источником фактов; дополнительный process join выбран для более сильной проверки ownership. Это ещё не host allocation ledger.                                                                                       |
| **H03 —19окт: durable cooperative lifecycle.** Platform[6a5d804](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/6a5d8048cd17e46d0149f529d03bef666276d5ce), `application_release.py`, `worker_lifecycle.py`.                                                                                                                                                                                                                          | Записанная цель — сериализовать cooperative mutations с durable owner identity. Добавлены owner/operation boundaries и regressions неопределённых исходов.                                                                                                                                                                                                                                                                                            | Это явный рост control-plane сложности ещё до strict/resource новой недели. Cooperative lock не защищает от произвольного администратора; ownership остаётся ограниченной гарантией. CD/lifecycle история требует отдельного анализа, не подменяется этим memory review.                                                   | Одна владеющая штатная service может упростить процессный lifecycle, но не автоматически закрывает lost response/partial activation. Сравнение такой альтернативы тогда не доказано этим набором.                                           |
| **H04 —20окт: strict campaign preflight.** Runner[4f60f16](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f). Root SCI07 design впервые tracked в[2bb05d3](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/2bb05d3651af4509fe7f02c1253b40f1e5146fec), уточнения —[b07974b](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/b07974b8e46bf8afdf1740947b842669a62a5ccc).                | Checked arithmetic/forecast и strict finite ancestor/burst validation. `_scientific_resource_preflight` требует envelope, затем **безусловно отказывает** strict с `R2/R3/P1/P2/A1/C1 bindings pending`. SCI07 design ставит common growth guard, stop reserve, authoritative capacity, cumulative I/O coverage и campaign ledger как7следующих tickets.                                                                                              | Это Source/design, прямо `needs_admission/needs_guard`, не accepted runtime. Folder называется closure19окт, но прочитанный SCI07 design датирован20окт — важное различие пути и события.                                                                                                                                  | Часть проверок исправляла реальные unknown/overflow semantics. Требование доказать каждый native growth/effect — более сильный выбранный contract, чем ordinary external backstop. Его полная стоимость ещё не измерена.                    |
| **H05 —22–23окт: resident storage authority и capacity proof.** Runner[604c4c1](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/604c4c11eba4ce84741f54dc7670d335773c80c2), Platform[95effdf](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/95effdf9c56a839056eab1cc23fb1ac80f095888).                                                                                                                                  | Runner добавляет703строки `resident_storage.jl`: parent/child permits, monotonic ledger, pending debt, first-refusal freeze и explicit release. Platform добавляет `scientific_resource_admission.py`: process/shared-domain binding и disjoint allowances.23окт появляются local-I/O/B0 authority primitives.                                                                                                                                        | Документы прямо говорят: resident authority port **не имеет production backend**; capacity validation не резервирует и не мутирует scientific domain. Нельзя назвать это реально действующим новым allocator. Но hooks/context распространяются на несколько writers и finalization paths — ощутимая цена для owning code. | Native quotas/cgroups и проверенный ordinary HDF5 путь могли быть operational альтернативой. Она ещё не являлась установленной приёмкой автоматически; strict failure semantics решали реальный риск ложного refund/partial publication.    |
| **H06 —24–25окт: явное упрощение до новой программы.** Root[4bd1085](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/4bd1085f037ca004b6d4e306eacf99e2c4f0e67f/docs/implementation/review-closure-2026-10-19/resource-policy-2026-10-24.md); Runner[7d47035](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/7d47035d7c6f6c82a4b57ab63deb7f271bd66c7e).                                                                              | Resource-policy документирует прямое поручение значительно упростить control mechanisms и перейти к физике. Сняты mandatory custom HDF5 VFD, NBD, common per-effect allocator, exhaustive alias/emitter proof и theorem всех native allocations. Оставлены ordinary HDF5, estimates и readback external Slurm/systemd/cgroup controls.25окт ordinary callback меняется на `external_controls_not_predicted_fit` и перестаёт прогнозировать phase fit. | Это **реальное Source упрощение**, не только обещание. Policy не объявляет обычный путь READY и сохраняет trust/integrity/foreign protection. Старые campaign numbers относятся к тому S1 поручению; не становятся вечным budget всех будущих tasks.                                                                       | Более простой operational lane был уже принят24окт. Нельзя объяснять весь последующий proof scope якобы неизменным требованием человека к exhaustive allocation proof.                                                                      |
| **H07 —27–30окт: removal старого strict и новая задача host memory.** Root initial plan[69d841f](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/69d841fdd0fa84f835803560faf80bcfd682679c); Platform[4de0970](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/4de09706691609b28cb53934543c956128a965b1); Runner[c96093f](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/c96093f4233797e2fbbb3ac5d383d42b666db4e3). | Новый план отдельно удаляет campaign CPU grant и strict unfinished path.28окт Platform удаляет scientific capacity/local-I/O/B0 proof modules;30окт Runner удаляет resident ledger/contexts и strict mode, с явным отказом obsolete requests. Ordinary planning, Linux probes и external limits сохранены.                                                                                                                                            | Diffstats removal включают tests/docs, их нельзя называть удалёнными executable SLOC. Удаление не выполняет Native acceptance. В то же время27окт явно поставлена другая задача: resident VM, safe host grants, request-before-low-guest-rejection и dynamic idle return после qualification.                              | Наличие новых proofs само по себе не доказывает нарушение removal: новая задача не совпадает со strict scientific per-effect fit. Нужно оценивать necessity каждой новой гарантии в её scope.                                               |
| **H08 —28окт: host broker, full-paid baseline и fixed-first.** Platform[4bce569](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/4bce569d3d3fd84444addfe8156769173d5e54f6), [733820e](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/733820efb7542881569cf26e6483c8bf750ce6f0), [0e7d956](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/0e7d956c23a02d0c7f9cd3cc947c0210dc7d1130).                     | P19 policy; P20-A `HostResourceController`/`FileReceiptStore` и request→grant→grow→admit→finish/shrink/reconcile; P20-B privileged facts/ingress/startup. Документ P20-B **с рождения называет первым production lane `conservative_reservation`**: все maxima оплачены, actual fixed max/balloon disabled. Dynamic закрыт из-за отсутствия mutator cleanup writer; output publication closure и build-scope join также ещё не реализованы.           | Broker действительно добавил durable resource obligations сверх Slurm allocation. Full-paid — логическое резервирование capacity, не уже выделенные resident pages. Fixed-first был Source намерением, но launch/output consumers ещё не замкнуты.                                                                         | План допускал verified fixed reservation. Незавершённость dynamic не должна сама становиться универсальным blocker fixed trial; однако actual fixed readback и launch/closure всё равно требовались.                                        |
| **H09 —28окт–1ноя: cleanup, recovery и native attempt custody.** Platform[3e807da](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/3e807dac7a4602cb08338d30aa4b696fbc118dac), [6dd6b95](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/6dd6b95c8c5b794a6d1e137b931a2b4713813b1f), [83b92fb](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/83b92fbbe54e51dff3928e79e2db0344e5c1d108).                   | Отдельные native cleanup witnesses, fence/retirement unknown targets; затем root-owned opt-in dispatch для existing CalcJob. Добавляются protected script snapshot, socket/peer/process provenance, exactly-once submit intent, Prolog/Epilog facts и finite writer closure. Последующие commits связывают actor origin, owner close, technical sideband и fresh output generation.                                                                   | Это не выбор worker или научный retry. Но поверх штатного scheduler появляется дополнительный authorization/provenance lifecycle. Initial native-attempt preflight прямо заканчивается `actor_input_binding_unavailable`; Source-only constructor не превращается в установленную submit chain.                            | Lost ACK/unknown remote operation требуют честного HOLD и неповторения submit. Конкретный объём ancestry/namespace/writer-domain proofs — implementation contract; его минимальность относительно trusted-team модели отдельно не доказана. |
| **H10 —3ноя: measured capacity и guarded calibration.** Platform[9d488a1](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/9d488a1f0d7a7d9b371f08c7d40d0068d7df116e), [74de4f3](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/74de4f3fa3cbbece97417d7b7b22b601dd56cb22).                                                                                                                                               | Вводятся capacity arithmetic, nine predicates, calibration repository/effect owner, worker route, physical/native settlement distinction, actual Source adapters и optional owned-child observer. Отдельный fence оставляет full-paid baseline без production RUN; missing input остаётся missing.                                                                                                                                                    | Source значительно продвинулся, но `open_native_jobs()` в published c470 всё ещё отказывает `qualification_worker_phase_required`. Source29 и MAIN worker design остались отдельными private proposals; два design blockers сохранены в03. Нет доказанного dynamic readiness или actual fixed acceptance в этом review.    | Более ранняя проверка existing conservative lane могла сузить critical path. Гарантия конкретной экономии времени или готового кластера из этого counterfactual не следует.                                                                 |

## 3. Почему strict удалили, а proofs снова появились

В первом витке цель SCI07/08 была сильнее обычного resource control: до effect доказать bounded
resident/growth/stop obligations, cumulative I/O и authority каждого scope. Source design честно
замечал, что HDF5 slab size не равен total native/RSS guarantee, quota не равно cumulative writes, а
sampled counters не enforceable theorem. Это корректные различия. Ответом стало расширение системы
до bindings, ports и missing-capability refusals. В результате scientific readiness зависела от ещё
не существовавших backends доказательства.

24окт operational policy изменила **требуемую силу гарантии**, а не физику. Она разрешила обычный
HDF5 и внешние caps с readback; возможный OOM/ENOSPC признала failed technical attempt, а не
гарантированным durable STOP. Не требовалось доказать fit каждого будущего native allocation или
весь NFS alias universe. Runner25окт реализовал эту уступку для ordinary phases. Это важный
положительный пример: цель безопасности можно сформулировать конечнее, сохранив verified
checkpoints, source integrity и containment.

Второй виток отвечал на другую реальную проблему: низкая память внутри idle VM могла мешать
запросить ресурсы, а configured VM maxima/guest MemAvailable не гарантировали RAM физического host.
Slurm и cgroup внутри гостя не резервируют hypervisor RAM. Поэтому host policy, reserves и readback
имеют собственный смысл. Частичная native mutation и потерянный ответ действительно требуют
сохранить charge до reconcile; завершение CLI не доказывает исчезновения remote mutator.

Но это объяснение не делает **каждый** последующий proof универсально обязательным. Уже P20-B28окт
обещал conservative fixed-first lane и одновременно сохранял unknown по output closure/build joins.
Затем значительная часть Source работы закрывала dynamic cleanup/qualification и native custody. Это
показывает фактический механизм роста: одно missing доказательство выделялось в новую owning
boundary, она добавляла новый authenticated input/producer/consumer, тот нуждался в следующем
readback и closure. Каждый локальный шаг мог быть корректен, но сумма prerequisites росла без
завершённого whole route. Это вывод из структуры diffs и записанных Source limitations, не
объяснение скрытых мотивов агента.

Нельзя свести всё к hostile-root threat model: initial native-attempt docs прямо ограничивают
trusted-team domain и отвергают универсальный detector malicious root. PID birth и exact owner нужны
также против обычных races, reuse и неверного join. Вопрос для будущего разбора — где эта
ограниченная модель оправдывала выбранную степень контроля, а где достаточно было поддерживать
меньший operational surface. Ответ «один администратор, значит никаких checks» так же не следует из
evidence, как абсолютная гарантия от другого root.

## 4. Что действительно подтверждено, и чего история не доказывает

Положительный результат истории — native mechanisms сохранены, strict scientific layer действительно
удалён, missing capabilities не выдавались за PASS, а independent reviews обнаруживали double-debit,
identity, lifecycle и cleanup defects. В текущем Source фиксированный путь выделен отдельно, в
qualification проводится различие native settlement и physical capacity. Это не фиктивные названия:
есть реальные функции, state transitions и failure controls.

Ограничение результата — большой объём local Source correctness не дал автоматически связного
installed пути. Из Git не следует, что каждый historical test был запущен, что каждый заявленный
runtime prerequisite был принят или что delay целиком вызван proof code. В исследованной истории
есть честные source-only/needs_guard labels и более поздние реальные failed consumer attempts; их
нельзя суммировать как один одинаковый outcome. Review03/04 сохраняют точные границы последней
стадии; более ранние receipts требуют адресного извлечения для конкретного runtime claim.

Не измерены цена каждого layer, скорость science до/после и время, которое занял бы более простой
маршрут. Текущая история позволяет указать **момент доступного выбора**, но не честный срок
альтернативного успеха: operational relaxation24окт, external-controls ordinary25окт, fixed
fallback27окт и fixed-first implementation intent28окт. Первое useful installed trial могло всё ещё
потребовать реальных fixes input/provenance/readback; это не снимает ответственности координатора за
приоритеты и неподтверждённые сроки.

Урок для будущего анализа конечный: сначала различать invariant и выбранный способ его
доказательства, затем проверять необходимость нового control-plane layer для ближайшего user path.
История поддерживает эти вопросы, а не немедленное переписывание проекта. Нельзя без actual proof
открыть admission, стереть paid journal или назвать fixed поддержанным. Current action остаётся
evidence-only.

## 5. Воспроизводимые локаторы

Ключевые Source paths приведены в таблице; commit links позволяют открыть реальные
additions/deletions. Дополнительные Root документы:
[SCI07 D1](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/a29fe2fb19aba0bab216c520653627316f099cce/docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci07-resource-design.md),
[SCI07 D2 baseline correction](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/a29fe2fb19aba0bab216c520653627316f099cce/docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci07-resource-design-v2.md),
[operational policy24окт](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/4bd1085f037ca004b6d4e306eacf99e2c4f0e67f/docs/implementation/review-closure-2026-10-19/resource-policy-2026-10-24.md),
[P20-B fixed-first при рождении](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/0e7d956c23a02d0c7f9cd3cc947c0210dc7d1130/docs/host-resource-integration.md),
[initial native-attempt limitations](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/83b92fbbe54e51dff3928e79e2db0344e5c1d108/docs/native-attempts.md).

Path histories также включают более узкие pivots: Platform8d48d9b/eeebef3 — local I/O/B0
primitives23окт;4f82051 — storage lifecycle29окт; d1bacfa/1adad52/68ef6ba/46bcfaa —
actor/input/close bindings30окт; fa1d22b/9c1aeaa/12558e2 — technical/durable output joins31окт–1ноя;
de93b3f/430b68c/dda7370 — native Slurm/installer corrections1–2ноя. Их existence и diff direction не
объявляются самостоятельной Native приёмкой. Latest Source/private/installed identities различаются,
как описано в01/02.

| Утверждение                                                    | Свидетельство                                                                  | Ограничение                                                                   | Решение                                                       |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Вся resource complexity возникла после27окт                    | Initial import H01, lifecycle H02/H03, strict H04/H05                          | До26сент внешняя prehistory недоступна                                        | изменить датировку и не приписывать импорт текущей неделе     |
| Слой был буквально новым kernel/Slurm                          | Native config и вызовы сохраняются; custom broker/authorization/proof state    | Дополнительная authority и complexity реальны                                 | сохранить точное описание вместо буквальной метафоры          |
| Упрощение24окт было только словами                             | Policy4bd1085 и ordinary diff7d47035; subsequent removals                      | Actual ordinary readiness из removal не следует                               | сохранить положительное Source evidence                       |
| Новые proofs просто вернули тот же strict allocator            | H07/H08 решают другой host/VM scope                                            | Возможное функциональное дублирование требует call-graph/threat-model анализа | не объявлять тождество; дополнительно анализировать necessity |
| Fixed-first альтернатива появилась только после жалобы3ноя     | Q01 fallback27окт и P20-B0e7d95628окт                                          | Actual fixed route неизвестен                                                 | изменить объяснение critical path; сохранить unknown          |
| Любой новый safety proof был обязательным требованием человека | Последовательность author contracts, operational relaxation, missing producers | Реальные host/foreign/integrity invariants сохраняются                        | отделять invariant от implementation choice                   |
| История доказывает точную долю waste или срок простого решения | Нет matched accepted-workflow/cost comparison                                  | Git metadata не время активной работы и не runtime                            | данных недостаточно                                           |
| Можно немедленно переписать или запустить кластер              | Current user STOP, evidence-only поручение                                     | Новая архитектура и runtime не разрешены этим документом                      | сохранить остановку                                           |
