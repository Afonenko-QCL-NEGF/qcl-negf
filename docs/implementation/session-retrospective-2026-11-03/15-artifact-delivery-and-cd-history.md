# Доставка артефактов и CD: от первого Git import до собственного протокола

Срез: 2026-11-04. **Evidence-only, Root/privacy review перед публикацией.** Ничего не
устанавливалось, не запускались tests/build/VM/PG, не менялись Git refs или код. Анализ относится к
опубликованной ancestor history Root и Platform и к явно названным operational receipts. История до
первого Git import неизвестна; private scripts вне Git рассмотрены отдельно, без приписывания их
published Source.

## Вывод

У доставки действительно есть небольшое обычное ядро: собрать immutable outputs, передать closures
штатным Nix, выбрать profiles/role generation, активировать службы и проверить health. Эти операции
уже использовали Nix/systemd; проект не написал собственный binary store. Основной рост сложности
произошёл **вокруг** них: согласованная остановка fleet, admission, enrollment/host identity,
physical process-stop evidence, durable unknown outcomes, artifact qualification, historical
Code/source binding и частные cross-store receiver transactions.

Неверно относить всё это к последней неделе. `application_release.py` появился3октября с313строками;
до27октября достиг3224строк. На выбранном опубликованном tip —3805. `bootstrap_build.py` уже
имел595строк и за последнюю неделю побайтно не менялся. Root `ops/release.ts` существовал с первого
import и к27октября уже имел те же98строк, что на final tip. LOC здесь лишь атрибуция происхождения,
не оценка качества или процента ненужного кода. [H01–H04]

Часть поздней сложности была прямо задана approved initial plan27октября: durable controller
service, request/attempt identity, продолжение после отключения клиента и reconciliation после
restart. Другую часть выбрали как конкретную реализацию этих целей. Требование updates при
работающей scientific job затем сузили2ноября, но это не отменяло автоматически независимые
требования interruption/reconciliation. Есть основания пересмотреть толщину адаптера; нет основания
считать любую receipt или весь ранее написанный CD бесполезными.

## Как проверена история

Inventory фиксирует non-shallow Root tip `a29fe2fb19aba0bab216c520653627316f099cce` и Platform tip
`c47097225a4a798e4124e30245c7b5b2063eb32a`. Прочитаны metadata **всех312 и222 ancestor commits**,
включая merges: SHA, author timestamp, subject. Формат census:
`git log --reverse --format=%H%x09%aI%x09%s TIP`; hashes полных metadata streams приведены ниже.
Затем прочитаны полные file histories целевых CD/build/docs paths и выбранные diffs/Source. Это не
line-by-line review всего кода534commits и не census unmerged/private branches. Другие компоненты
покрываются соседним cross-component report13.

Первый Root commit — `1e10299e99f8d9f73a5dc3d3b53141459091d1fa`, Platform —
`66115da942ed46e61fb60e95f33d9d9b5a8137bd`, оба26сентября. Git author date показывает сохранённую
хронологию, не время исполнения или изготовления pre-Git кода. Для сравнения перед программой выбран
snapshot до27октября: Root `d395044ac09b28c2ff573724f8911d625df43bf5`, Platform
`1b1370d2b8e83a267a97c8d49df14db220123478`.

## 1. Что уже было в первом import

Root `ops/release.ts` собирал frontend и четыре Python wheels, фиксировал source graph, проверял его
неизменность после build, хэшировал manifest и публиковал результат через rename. Он отдельно
пояснял, что wheels не включают Julia, NixOS images и внешние Python dependencies. Это assembler
release envelope, а не рабочий cluster deploy command. Название `release` не означает, что одна эта
команда уже выполняла production CD. [H01]

Platform `modules/cache.nix` уже объявлял signed Nix cache через `services.nix-serve`, а
`modules/storage.nix` — отдельный persistent NFS lifecycle, stable disk identity и root-squash. То
есть cache/storage ownership не появились как изобретение программы27октября. Сам
bootstrap/build/qualification protocol того времени из факта наличия modules не следует. [H02]

Проверенные workflow snapshots показывают integration job. Ранний runbook3октября говорил о
существующем build/test/publish/deliver workflow и protected delivery job; это описание не является
receipt такого deployment. К10октября документы и Root assembler явно разделили source CI и
controller-local delivery без production credentials в CI. В историю нельзя переносить обещанный
delivery job как доказанно работавший сервис. [H03, H05]

## 2. Октябрь3–9: небольшая activation и первые реальные границы

Platform commit `c50a771a1ce4fbfc4ece5d4309cda65cb21ed458`3октября создал `application_release.py`,
`modules/release.nix` и initial CD runbook. Основной `activate` был узнаваемым adapter:
`nix-store --verify-path`, два `nix-env --profile ... --set`, регистрация immutable solver в AiiDA,
`service.env`, restart/is-active, затем `ready:true`. Controller-local `deliver_cli` закрывал shared
gate, останавливал API/AiiDA, drain-ил выбранных workers, запрещал непустую Slurm queue, делал
`nix copy`, activate/check и RESUME. Исходный scientific workflow команда сама не отменяла. [H03]

Эта связка имеет доменное основание: новый job не должен попасть на worker со старым solver, а
старый AiiDA Code нельзя переименовать под новый executable. Но это уже более широкий контракт, чем
«передать файл и перезапустить веб-службу». Сам выбранный closed-gate fleet protocol — архитектурное
решение, не обязательное свойство Nix.

Через два часа commit `953d9558d2f8aaa0d65d8bfc72f2ced48d87730b` вынес prefetch и exact NAR-hash
проверку **до** остановки служб/admission mutation. Это исправляло конкретную опасность: bad
cache/missing closure не должны оставить здоровую систему остановленной. Native Nix copy/path-info
оставались исполнителями; новый код проверял manifest и порядок эффектов. [H04]

9октября `7eaa515fcf4a` исправил независимость application и solver profiles. Initial idempotence
проверяла application profile, но могла пропустить потерянный solver GC root при «том же» release.
Это содержательная ошибка lifecycle, а не косметическое расширение спецификации. В тот же день
`587a895fd2df` добавил bounded commands и uncertain admission outcomes; `dcc566cab90c` связал
delivery/startup с protected enrollment. У admission появился дополнительный вопрос: не только
правильный artifact, но и правильный реально наблюдённый узел. [H06]

Публичный local validation report3октября честно ограничивал evidence: Python/Nix evaluation и fake
external commands; server, реальные Slurm/NFS/Windows и production delivery не изменялись. Его
полный suite count не доказывал native rollout. Эти исходные ограничения важны: высокая формализация
ещё тогда опережала end-to-end hardware qualification. [E01]

## 3. Октябрь10–26: основной рост произошёл до новой программы

`368413cd955868cf72794238dcc98656a287faa2`10октября расширил selected pool до полного enrolled
fleet: offline enrolled worker стал blocker; AiiDA workflows/CalcJobs и Slurm queue должны
отсутствовать; worker services и processes должны быть остановлены и затем иметь проверенный healthy
generation. Source diff добавил858строк в application module и1307строк tests. Это не цена одной
команды `nix copy`, а цена выбранного whole-cluster update contract. [H05]

`bc44deb4a522`12октября отделил protected administrative namespace от service-owned state.
Последующие fixes разбирали native Slurm alias/Reason, service cgroups, infinity keeper, effective
runtime masks и NFS mount selection. `6a5d8048cd17e46d0149f529d03bef666276d5ce`19октября добавил
cooperative lifecycle serialization с durable owner identity: shared release/startup/update
mutations больше не координировались одним незафиксированным foreground caller. Эти source changes
содержат полезные race/failure protections; их совокупная необходимость для минимального research
site отдельно не измерена. [H07]

К25октября `cc72bbffbf1b` сохранял solver-build и runtime identity, к26октября появились fixes
исчезающего process и Nix store directory timestamp drift. Так возник слой, который проверял не
только delivery, но и происхождение команды/службы и uncertainty её завершения. Большая часть
монолитного engine существовала до стартового поручения27октября. Формулировка «за неделю заново
написал CD с нуля» исторически неверна.

`bootstrap_build.py` родился5октября (`348fcc415f4e`), менялся6/10октября и остался неизменным в
рассматриваемую неделю. Его preflight/disk/build scope нельзя записывать как новый параллельный CD
продукт27октября. Аналогично `ops/transfer-github.sh` относится к переносу repositories/organization
и не менялся за неделю; это не transport NAR в cluster. [H08]

## 4. План27октября и реализация28–31октября

Initial `69d841fdd0fa84f835803560faf80bcfd682679c`, `project-simplification`§6, уже требовал:

- совместимый management/application/solver/docs descriptor и runtime bindings;
- artifact qualification отдельно от дешёвой mutable health;
- controller systemd service с durable request/attempt identity вне client lifetime;
- reconciliation после restart, без «успеха по исчезнувшему process»;
- soft application/docs при продолжающейся job и отдельные maintenance/OS/resource/restore
  процедуры.

Поэтому28октября не следует описывать как самовольное внезапное изобретение deployment daemon. Это
реализация заранее записанного широкого плана. Как и зачем сам план выбрал эту ширину — другой
вопрос; наличие утверждённого текста не доказывает оптимальность architecture. [H09]

`8d48643827d13e2f7961b785b85e2771e6582b3e`28октября выделил `release_identity`, `release_trust`,
`release_qualification`, `release_health`. Stable artifact proof отделён от boot/service activation
health: неизменный solver больше не должен постоянно выполнять expensive verify/self-check при
health/guard. Qualification key исключает APP release, Root revision и boot/service generation, но
включает собственный artifact/environment/enrollment. Это явная оптимизация повторного использования
evidence с сохранением provenance; metadata proof не равен scientific acceptance. [H10]

`a957e935a6cbe6328129f4843d2b6dcbafde6e02` создал `delivery_requests.py` и `delivery_service.py`,
systemd template и boot/failure reconcile units. Сформировался собственный durable protocol:
immutable request→attempt/operation projection→engine primary receipt→completion witness. Exact
повтор ID/body читает прежний status, не dispatch заново. Unknown требует reconciliation; служба не
делает automatic replay/open-admission. Completion witness сохраняет связь с authoritative engine
outcome, чтобы сбой auxiliary status publication не откатывал уже совершённый success. Это общая
control-plane функциональность поверх Nix/systemd. [H11]

`2e0a0ecf1131a2e8f9d2ccc8249f3af0a692ad22`29октября сохранил original actual-build graph и
historical Code binding. Текущий Root HEAD не подставляется вместо producer source; APP-only update
с прежним solver сохраняет его graph. Эти records сами не являются GC roots; retention closures
остаётся у profiles/native retention owner. Здесь конкретная QCL/provenance потребность, которую
обычный profile switch не описывает. [H12]

`3079f7de1acfa32b260aa21798018442dbd14ca5`31октября исправил `require_controller`: публичная NixOS
config штатно проходит через immutable symlinks, тогда как reader mutable administrative records
запрещал symlinks. Runbook сохранил original native `OSError(40)`: OS generation могла
переключиться, а service reconcile завершиться с ошибкой. Это пример, почему source fixtures
недостаточны и почему «команда failed» не означает «ничего не изменилось». Узкий native store
exception не разрешал произвольные writable targets. [H13]

Отдельный `host_resource_storage.py`29октября добавил owned VM storage capture/import/binding и
trusted topology. Это не artifact CDN/cache. Его controller/broker guarantees относятся к disk
lifetime, QEMU/native identities и resource qualification; он связывает delivery/installation
prerequisites с более широким resource plane. Native N-H0…H8 были объявлены отдельными gates. Полный
storage collector нельзя считать доказанным обычным CD или незаметно включать в его стоимость.
Подробный resource scope разобран в14. [H14]

## 5. Docs и depot: reusable artifacts, но новые joins

Root `ops/application_cd.ts` с3октября был assembler APP+solver manifest;10октября прямо закрепил
controller-local delivery.29октября `993b378d0dfc` добавил compatible depot v2: original producer
graph сохраняется, а reuse разрешается по exact native inputs/Manifest/factory compatibility. Это
решало настоящий недостаток exact-graph v1: docs-only graph change не должен требовать нового depot,
но и не должен ретегировать старое evidence. Цена — candidate/native facts/Source
qualification/finalization protocol. Его hashes связывают assertions, не доказывают смысл review
автоматически. [H15]

Docs producer существовал до новой недели: `ops/docs/assemble.py` с20октября, source-observation
binding с22-го, обычный offline Nix docs package с24-го.29октября `1e65ba2d3ecb` собрал полный
immutable package и **сократил** общую diff-обвязку:2166insertions против6097deletions в commit.
`ops/docs.ts` уменьшился с2545строк pre-week до821 на tip. Следовательно история не монотонно
наращивала wrappers; часть была реально упрощена. [H16]

Тем не менее docs derivation в первой реализации намеренно зависел от полного published source
graph, depot evidence, assets и review receipts. Новый graph давал новый docs derivation даже при
тех же страницах. Это выбранная cache boundary, а не требование Nix. `docs:plan/prepare/build`,
bundle validation, C1/C2 source references, renderer/assets и installed serving стали разными gates.
`docs/cached-documentation.md` прямо отрицал отдельный docs VM/daemon/cache ledger/root admission в
**public build path**. Частная доставка готового package позже добавила собственные operational
steps; их нельзя приписать этому публичному builder. [H16]

## 6. Частный Root receiver: отдельная provenance категория

Named preparation snapshot2ноября фиксирует `receiver.py`, `linux_receiver.py`, `cache_usage.py` по
SHA. Repair scope: native sticky store boundary и strict JSON/finite bounds до dependent IO. READY
имел `NOT_NATIVE`, будущий target ещё требовал Root binding. Это **вне Git**; public ancestor
history не устанавливает first birth, весь первоначальный design или полный source ancestry этих
scripts. [E02]

Последующие exact actual reviews подтверждают software import/content/trust readbacks, retained GC
links, WAL/child reconciliation и durable unlock для отдельных controller/compute/docs operations.
Они отдельно не принимали OS/App activation, backend/admission или science. Compute adaptation
разрешила явное `docs:null`, сохранив обязательный target и строгую membership при наличии docs:
универсальное требование docs к compute closure оказалось слишком широким.45 Source tests и
mutations подтвердили узкий guard change, не Native импорт сами по себе. [E03–E05]

Docs receiver3ноября имел отдельные staging/capacity/GC/socket obligations. Его actual review принял
import/retention/unlock/socket restore, но не OS switch/HTTP. Другой actual review затем принял
**docs-only controlOS и installed HTTP/TLS**:54requests, с закрытым admission. Не были приняты
authenticated backend readiness, full current runtime snapshot, fresh content/trust reverify всех
прежних outputs или scientific acceptance. Это реальный положительный installed результат, а не
только Source; scope всё равно узкий. [E05–E06]

Так стало больше, чем несколько native CD commands: был выбран конкретный bounded cross-store
transaction с staging, hash/signature binding, retained links, WAL и unknown-child reconciliation.
Нельзя приписывать его целиком Platform `delivery_service`: это другой operational route. Нельзя и
объявлять избыточными каждую подпись или GC root без знания trust/store topology. Сравнения с
достаточно простым `nix copy` route при тех же условиях в этих receipts нет; цена и необходимость
всего receiver framework остаются отдельным вопросом.

## 7. Что изменило maintenance-only2ноября

Commit `2ff7baa92ad3b4886646e825d54b61fe4f95339a` после прямого user steering исключил
App/UI/service update и acceptance при работающих jobs. Initial soft-job-continuation case перестал
быть обязательным. Это законное сужение задачи; не следует требовать доказательство concurrent
update по старому тексту. [H09]

Но maintenance engine требовал empty-work barrier ещё с3/10октября, а durable service — отдельно
с27-го. Поэтому утверждение «весь собственный CD вырос только из ненужного zero-downtime требования»
противоречит history. Сужение устраняет часть compatibility/capability cases и позволяет
пересмотреть порядок rollout, но не автоматически решает lost replies, profile identity, shared
admission, returning workers и mutable PG/NFS recovery. APP rollback не равен rollback dataset;
restore hook в P23 оставался явным незавершённым integration gate. [H03, H05, H09, H11]

## 8. Конкретные объекты будущего упрощения

Это карта решений для будущего overhaul, не начатый migration/implementation plan. Сопоставление
возможностей existing tools — в12; их не устанавливали и drop-in equivalence не проверяли.

| Текущий механизм                                         | Что можно делегировать existing owner                                                                | Небольшой site/QCL contract, который остаётся                                                                                   |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `prefetch_controller_closures`, closure transfer/staging | Native Nix copy/store verification; сравнить private receiver с тем же trust/store route             | Выбор exact APP/solver/docs output, trusted publisher и достаточное место; не подмена source graph                              |
| Profile set и role activation в `_activate_owned`        | Nix profiles/systemd; адресно сравнить deploy-rs/Colmena для generic multi-node copy/activate/health | Порядок stop/admission, immutable InstalledCode, выбранный role inventory и критерий health                                     |
| Request/service/process supervision                      | Native systemd unit/cgroup lifetime; существующая deployment operation identity                      | Только требуемая semantics lost-reply/unknown/reconciliation. Не очевидно, что необходимы все собственные projections/witnesses |
| `retain_release_sources` и artifact qualification        | Native closure retention и immutable references как substrate                                        | Минимальная историческая связь actual solver/depot/Code/source; missing proof не создавать задним числом                        |
| Docs recipe/orchestration/serving                        | Обычные locked renderer tools, Nix derivation/cache и static serving                                 | Русские страницы, light theme, source links и проверяемый bundle; полный Root graph в cache key требует отдельного оправдания   |
| `physical_stop_scan`, runtime-mask/Slurm lifecycle logic | Использовать выбранные systemd/Slurm owners, где их contract достаточен                              | Whole-cluster stopped condition и защита чужих jobs; не объявлять process absence по одному exit code                           |

Потенциальное сокращение — границы этих механизмов и поддерживаемого режима, а не новая
general-purpose CD library. deploy-rs/Colmena не обещают QCL dataset consistency, правильность
scientific checkpoint или атомарную distributed rollback. Native copy не даёт scientific acceptance.
Отдельные adapters оправданы там, где остаётся непокрытый domain/site invariant; для каждого
большого слоя нужно показать именно этот gap, а не только наличие многих tests.

## Решения по evidence

| Утверждение                                 | Свидетельство                                                                   | Ограничение                               | Решение                      |
| ------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------- | ---------------------------- |
| Basic delivery может быть короткой          | Initial313-line adapter; native copy/profile/systemd                            | Fleet/unknown/data semantics шире         | сохранить native core        |
| Всё CD изобретено за последнюю неделю       | First imports и pre-week3224-line engine                                        | Pre-Git origins неизвестны                | изменить атрибуцию           |
| Durable service добавлен без требования     | Initial27Oct§6 прямо задаёт service/request/reconciliation                      | Не доказывает минимальность самого плана  | не утверждать                |
| Сложность вызвана только live updates       | Maintenance engine и ownership уже существовали                                 | Concurrent case действительно отменён2Nov | сузить объяснение            |
| Source/tests доказывают установленный CD    | Source docs сохраняют native gaps; actual import/HTTP reviews имеют узкий scope | Полный backend/science не принят          | не утверждать                |
| Existing CD tool гарантированно заменит всё | 12 показывает capabilities, но не semantic equivalence                          | Нет runtime comparison/стоимости перехода | данных недостаточно          |
| Конкретный overhaul можно обсуждать         | Названы функции/native owners/retained invariants                               | Никакой реализации сейчас                 | сохранить как вопросы review |

## Источники и воспроизводимость

Все Git locators относятся к указанным frozen tips, не к текущему dirty checkout. Полные public
ancestor metadata stream hashes: Root
`403ea579bcf123d042cb080c7c20c16575ffd09383a6d266f4faa08539e68eb6`, Platform
`31233c264eda03c2df19d21f852b4c5bb724ae09530a8e87af71ee96bbba2d35`. Private operational receipts
содержат более широкие поля; публикуются только приведённые scope/aggregates и file hashes, без
inputs, IP, home/session/operation identifiers, credentials и научных данных.

| ID  | Repository / commit / path / symbol или раздел                                                                                     | SHA256 Source blob                                                 |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| H01 | Root `1e10299e99f8d9f73a5dc3d3b53141459091d1fa` / `ops/release.ts` / release manifest/source graph                                 | `d7771f108d08b6966205fc81f01b84f892e673239685dc47f644ecb853c50872` |
| H02 | Platform `66115da942ed46e61fb60e95f33d9d9b5a8137bd` / `modules/cache.nix` / nix-serve                                              | `f0a64ef7e1303490bb516e1916e506a400ae5bbb592e0ab84276a25a52e28130` |
| H02 | Platform `66115da942ed46e61fb60e95f33d9d9b5a8137bd` / `modules/storage.nix` / separate NFS lifecycle                               | `1518be74a9c353adaa547047635dc5bbd90cda0374ac50ce08d0631bf44eb0b1` |
| H03 | Platform `c50a771a1ce4fbfc4ece5d4309cda65cb21ed458` / `ops/application_release.py` / activate/check/deliver_cli                    | `f2240de34d5d7fd50ce266676c6fec0725d64dc3444baf6dfbc818823dd14b42` |
| H03 | Root `4341692b0d40e4d7b381b4525cf19dd6750ebf66` / `.github/workflows/ci.yml` / integration workflow                                | `254a8d92d81ab4d31d6a591ddc3d721f567b035a9f03db1ed5958c74e7910059` |
| H04 | Platform `953d9558d2f8aaa0d65d8bfc72f2ced48d87730b` / `ops/application_release.py` / prefetch_controller_closures                  | `860fa1aab7778cb0fe32a967eba043bed99d0739f66473b8835e82e60a4d9406` |
| H05 | Platform `368413cd955868cf72794238dcc98656a287faa2` / `docs/application-cd.md` / whole enrolled fleet/maintenance                  | `3815fe6b86b787c970ccd584e4a267ce0474218793d4b259365c3060b9ceed12` |
| H05 | Root `f8a370dd089de56dada7eecd8c84bef9e0a9a12c` / `ops/application_cd.ts` / assembler/local delivery separation                    | `91989d0171e011f4518e178e247d4f7a466d08bd02b7931308a202c4354ee9ce` |
| H06 | Platform `7eaa515fcf4ad1146d7767b350286814e7c97f70` / `ops/application_release.py` / independent profile repair                    | `8c1645b24057909f28587a6ec541271d69f6afe5e24c2fdaccc87d79bf31933f` |
| H06 | Platform `587a895fd2df0f7273fa9de03aa373ac34f67024` / `ops/application_release.py` / bounded commands/unknown                      | `093abc29f15a3b97adef712b0cc79af85239f356c47a3b967445d920db25cfe8` |
| H06 | Platform `dcc566cab90cb85d12c16c88078193c636aab5f2` / `ops/application_release.py` / enrollment binding                            | `3afdc0751385f6d35cc23a6b931a5609635ec531237cc24cc3d793946ff1dc81` |
| H07 | Platform `6a5d8048cd17e46d0149f529d03bef666276d5ce` / `ops/application_release.py` / LifecycleOwner                                | `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0` |
| H08 | Platform `c47097225a4a798e4124e30245c7b5b2063eb32a` / `ops/bootstrap_build.py` / unchanged pre-week blob                           | `87eebbbfa1b13ffadd15b4e8fc880774e70b26ddd59de3034ccf29ecfd980479` |
| H08 | Root `a29fe2fb19aba0bab216c520653627316f099cce` / `ops/transfer-github.sh` / organization transfer                                 | `9feca2cb0da57d4267a0a392cd5d4901c6b97b584c014dc90f3f6e3d5ad6a746` |
| H09 | Root `69d841fdd0fa84f835803560faf80bcfd682679c` / `docs/implementation/project-simplification-2026-10-27.md` / initial §6          | `ab945b0190548ca4f8f82dd8ea083199af6caf63fe4be2907b96b2ce78b90b99` |
| H09 | Root `2ff7baa92ad3b4886646e825d54b61fe4f95339a` / `docs/implementation/project-simplification-2026-10-27.md` / maintenance-only §6 | `e37f22090c2f93474d66d6c133185a938afe7fbd94a94b0a868779ce547bfa83` |
| H10 | Platform `8d48643827d13e2f7961b785b85e2771e6582b3e` / `docs/artifact-qualification.md` / artifact proof vs health                  | `16ca9bbca406cb7937047765a5f22d2d30c1f46d3469b1e138411f4c77fb8114` |
| H11 | Platform `a957e935a6cbe6328129f4843d2b6dcbafde6e02` / `ops/delivery_service.py` / run_update_service/reconcile/_commit             | `22d0526cc108307facf3bcbc8a3dff838b540ac5d78b5967596fbe2476f46ac3` |
| H11 | Platform `a957e935a6cbe6328129f4843d2b6dcbafde6e02` / `ops/delivery_requests.py` / submit/read binding                             | `6a7ea09325ccfc121da8d286efa7c41e0af741b41d48803d34e4f276146a04a0` |
| H12 | Platform `2e0a0ecf1131a2e8f9d2ccc8249f3af0a692ad22` / `ops/application_release.py` / retain_release_sources                        | `b4aab88833867daa61002d23bcf6a84317acac98d1d77e883d0be836acb5f5eb` |
| H13 | Platform `3079f7de1acfa32b260aa21798018442dbd14ca5` / `ops/delivery_requests.py` / require_controller                              | `90b2fab480338dd9f465ea3f93067d7e06c863168c5d7fe419071e81ed8b51fd` |
| H14 | Platform `4f820511dbe1dc1b613b32a1a3f67b9d3268b769` / `ops/host_resource_storage.py` / storage capture/import/bind                 | `e9ba29079cda35a6c97117f85b89535e5a7b791acad309ee30fae2177ab3a514` |
| H15 | Root `993b378d0dfc918cb4324f5036e3d9eadb834fcf` / `docs/depot-compatibility.md` / v2 qualification/reuse                           | `eefb197696b2de69e62940fc1c049ff188721cf6334346c523040a8e8f810256` |
| H16 | Root `1e65ba2d3ecb78186df5502c37e5257ea61ee7c6` / `docs/cached-documentation.md` / cached docs artifact contract                   | `f13ab05893e6d6fc7e910abf79f40aad48af612e1ba45d593c88583c41342220` |
| H16 | Root `a29fe2fb19aba0bab216c520653627316f099cce` / `nix/docs.nix` / mkDocumentation input binding                                   | `4ef782338a0d0f8a1714e464fba71cf67b63acdf5ad52dd92808780383dc53b5` |

| Evidence ID | Локальный source или published Source locator                                                       | SHA256                                                             |
| ----------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| E01         | Root `a29fe2fb19aba0bab216c520653627316f099cce:docs/implementation/recovery-cd-local-validation.md` | `844b86015d802d4fbea628cf96e64ec0c0ab226f97dcb9bf81bed6d321efe864` |
| E02         | `.build/P17-control-receiver-transaction-repair-preparation-20261102/READY.json`                    | `91f33cf29ea086942bb91a33f674c4f38a152f9294a5e304652f9e01299671c7` |
| E03         | `.build/P17-Root125-compute-receiver-Root-independent-review-20261102/decision.json`                | `dce153fca20189bbd83659111118dc5f000582ad5010cdfde343caa23767ee02` |
| E04         | `.build/P17-Root125-receiver-actual-independent-review-20261102/decision.json`                      | `7ba47e280252959a7ed712bcb8dce31e9e25cbbb7a0c6ca011f02d32c68d9598` |
| E04         | `.build/P17-Root125-compute-receiver-actual-independent-review-20261102/decision.json`              | `bdeabc5dd680c2788e922990019a9b06c7d74172fc08cae3b33b5ebf463f8207` |
| E05         | `.build/P23-Root126-docs-receiver-actual-independent-review-20261103/decision.json`                 | `d06d8d332293c0023be3a3fd838dd087a721d7aa167bfbbf576bd2d595de2cba` |
| E06         | `.build/P23-Root126-docs-OS-actual-independent-review-20261103/decision.json`                       | `54bc7410e2f1dfd9cb6eff7ddc2d30e04ad7eb9be84183ddfc5beee94f06addc` |
| E07         | `.build/session-evidence-followup-20261104/repository-history-inventory.json`                       | `454c42ed40baf7301382b51f850ff3071656aabd5a610138341e95ff922dd763` |
| E08         | `.build/session-evidence-followup-20261104/drafts/12-opensource-references-and-reuse-options.md`    | `ff7b6c506e31d31153f4e475192c76788b45f34ee3ea41919046810fcdbfdb61` |

Read-only подготовка отчёта завершена. Все source/count comparisons — историческое свидетельство, а
не новые тесты. Future options не приняты как design или разрешение реализации; окончательная
публикация — после независимого Root/privacy review.
