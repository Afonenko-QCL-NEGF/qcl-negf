# Dispositions требований: 2026-10-19

Sanitized decision appendix DOC01. Это актуальность 59 исторических ID,
а не второй полный план, source lock или журнал научной приёмки.
Полные исходные формулировки/acceptance cells сохранены в
[requirements](requirements.md); ссылка каждого ID ведёт к соответствующей строке.
История не удаляется при новом disposition.

## Источники и epoch

Все locators `Q:Lnn` относятся **только** к неизменённым байтам
`docs/system/requirements.md` на исходном commit
`e0f244d075dd49874ba4f3847f4efa693f3b3622`, SHA256
`aaf01fe9b803a0aa34ba5ae9e71559606482e2ad96c3314388dc6c6667096e0d`.
Это documentary epoch **2026-10-09** для всех 59 строк. Номера не обозначают
строки новой редакции. Original Git blob доступен командой чтения
`git show e0f244d075dd49874ba4f3847f4efa693f3b3622:docs/system/requirements.md`.
Gitlinks остаются authority состава; этот locator фиксирует input DOC01,
не создаёт maintained список component revisions.

| Alias | Первичный доступный документ / точный locator | Граница свидетельства |
| --- | --- | --- |
| Q | Original requirements выше; exact row в каждой строке ledger | Статусы С/Н/П и дата документа; **первичный user message ID/date каждой historical строки — unknown** |
| RV00 | [Historical ledger](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/RV00.md), P01–P14, F00-01–06; [independent review](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/reviews/RV00-review.md) | 2026-10-14, root e48e5b2 + frozen overlay; 59/59 textual coverage, не acceptance текущего source |
| MAP | [PORTABILITY](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/PORTABILITY.md), §Карта путей; [publication receipt](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/publication-receipt.json), `frozen_root_texts` entry `docs/system/requirements.md` | Original RV00/Q bytes не меняются. Frozen sys/README original отсутствует; current файл не подставляется вместо него |
| A | [AGENTS](../../AGENTS.md), названный в ledger раздел, source e0f244d0 | Действующие прямые project instructions; норма не доказательство исполнения |
| H | [Handoff](../implementation/review-closure-2026-10-19/README.md), Goal и Global constraints, source e0f244d0 | Полный scope: findings, cluster, worker distribution/guide, convergence и physical attempt; исторический PLAN header относится к подготовке |
| P1 | [Operator permissions](../implementation/review-closure-2026-10-19/operator-permissions.md), PERM01–18 и §Запись решений, source e0f244d0 | Ответы пользователя 2026-10-19, call `call_20fe81a2d18242509e046a77f78f8b87`, items0/1/2: B/G1/S1 без e–e. Время внутри суток неизвестно |
| EXEC | [Coordination checkpoint](../implementation/review-closure-2026-10-19/execution/checkpoint.json), `operator_authority`, `mode`, `grants` | Отдельное прямое поручение 2026-10-19 активировало EXEC. Checkpoint — sanitized запись coordinator, не primary transcript и не admission/READY |
| DOC | [Documentation cards](../implementation/review-closure-2026-10-19/documentation-instructions.md), DOC01–07, source e0f244d0 | DOC01 dispositions; DOC03 design; DOC07 feature inclusion явно принято PERM14 |
| OPS | [Platform cards](../implementation/review-closure-2026-10-19/platform-worker.md), OPS01–17, source e0f244d0 | Required Proxmox/Linux-libvirt/Windows-Hyper-V и обе Windows machines; exact native inputs/outcomes отдельно |
| S | [Science cards](../implementation/review-closure-2026-10-19/science.md), SCI01–15; P1 §S1 | 0 mV/period, lattice/LO 70 K, e–e none, LO/acoustic/impurity/IFR/alloy; conditional13/936 catalog и byte caps, не physical pass |

Для historical С/Н сохраняется последняя документированная запись, если нет
локализованного противоречия новому поручению. Missing primary provenance не
означает отмены требования и не блокирует current approved design.
P1/EXEC не выдаются за восстановленный primary provenance всех старых строк.

## Семантика ledger

`current` — действующее ограничение/выбор; `target` — обязательная целевая
возможность, исполнение которой ещё надо доказать; `historical` — датированный
контекст/способ, неприменимый как автоматическая новая операция. Метки могут
сочетаться: например, D07 сохраняет cold-source вход и историческое ограничение
clean-install. Они не являются machine outcomes.

Вторая ось — evidence реализации: `implemented` разрешено только при
commit + path/symbol + проверенном свойстве/limits; `unpublished` — лишь при
подтверждённом отсутствии публикации конкретного output; `unknown` — сведения
не установлены. **Для всех 59 строк implementation/native/scientific evidence
в этом docs-only пакете = `unknown`.** Наличие source не property pass;
проверка этих Markdown не доказывает GUI, backend, сходимость или физику.
Отсутствие доказательства публикации не превращается в `unpublished`.

Actions: `preserve` сохраняет принятое требование/историю; `implement` направляет
явно включённый scope owning task без заявления, что он уже реализован;
`conditional` требует указанного design/measurement/BIND/READY;
`needs_operator` касается только конкретного выхода за принятый grant.
Unknown API внутри разрешённой feature решает owning design, не новый опрос.

Во всех строках historical primary decision = **unknown**, epoch = **2026-10-09**,
evidence реализации = **unknown**; таблица даёт exact Q row и доступную current
authority. Ссылки/aliases source-bound к e0f244d0, кроме явно mutable EXEC receipt.

## 59 dispositions

### Научная область

| ID → исходный текст | Historical status / locator | Применимость | Current authority | Action / owning scope и предел |
| --- | --- | --- | --- | --- |
| [S01](requirements.md#s01) | С, уточнено; Q:L15 | `current/target` | P1 PERM15–17, S | `conditional` — Research/Core: цель выбрана, SCI03/READY доказывают критерии и admission. Новый B0 не наследует old S01 acceptance. |
| [S02](requirements.md#s02) | С, уточнено; Q:L16 | `target` | Q, H, P1 PERM15 | `preserve` — Research/Runner/Results: stationary transport/ВАХ остаются областью target release; finite-bias не входит в текущий S1. |
| [S03](requirements.md#s03) | С; Q:L17 | `current` | Q, P1 PERM15 | `preserve` — Core/Portal: исключение мощности, динамики и волновода сохраняется; expert gain не означает эти наблюдаемые. |
| [S04](requirements.md#s04) | С; Q:L18 | `current/target` | Q, A §Владение компонентами | `preserve` — Results: сравнение saved data отдельно от solve; тяжёлая derive-команда требует своего бюджета. |
| [S05](requirements.md#s05) | С, уточнено; Q:L19 | `target` | Q, H | `preserve` — Runner/AiiDA: независимые точки и continuation поддерживаются как разные явные policies; ветка остаётся одной execution. |
| [S06](requirements.md#s06) | С, уточнено; Q:L20 | `current/target` | Q, A §Физическая и численная добросовестность | `preserve` — Runner/Contracts: failed point не seed; предыдущие данные/причины и independent branches сохраняются. |
| [S07](requirements.md#s07) | С, AGENTS; Q:L21 | `current` | A §Физическая и численная добросовестность, P1 PERM18 | `preserve` — Core/Results/Contracts: process/convergence/physics/discretization/validation раздельны; missing не pass. |
| [S08](requirements.md#s08) | С; Q:L22 | `target` | Q, H | `preserve` — Results/Research: предметные figures с axes/units/conditions сохраняются; plot template не scientific criterion. |
| [S09](requirements.md#s09) | С; Q:L23 | `current` | Q, P1 PERM15 | `preserve` — Core/Portal: quantitative gain/absorption spectra отложены; expert API/справка сохранены с ограничениями. |

### API и конфигурация

| ID → исходный текст | Historical status / locator | Применимость | Current authority | Action / owning scope и предел |
| --- | --- | --- | --- | --- |
| [C01](requirements.md#c01) | С; Q:L29 | `current/target` | Q, A §Владение компонентами | `preserve` — Core/Runner: полезные локальные Julia API независимы от YAML/AiiDA/Slurm/Portal; package presence не behavioral proof. |
| [C02](requirements.md#c02) | С; Q:L30 | `target` | Q, H | `preserve` — Core: construction/validation/run/initial state/iteration observer и expert operators; DOC/DEV адресно проверяют API contracts. |
| [C03](requirements.md#c03) | С; Q:L31 | `target` | Q, H, P1 PERM01 | `preserve` — Portal/Runner: короткая предметная форма сохраняется в target; готовность полного GUI не prerequisite B0. |
| [C04](requirements.md#c04) | С; Q:L32 | `target` | Q, H, P1 PERM01 | `preserve` — Portal/Runner: templates/forms/YAML должны иметь один смысл; полная реализация и round-trip здесь unknown. |
| [C05](requirements.md#c05) | С; Q:L33 | `current/target` | Q, H | `preserve` — Research/Runner: named/versioned protocol, explicit variant/diff/resolved inputs; не silent numerical change. |
| [C06](requirements.md#c06) | П; Q:L34 | `current/target` | A §Владение компонентами, P1 PERM01–02, DOC03 | `conditional` — Owning boundaries уже действуют; historical П о конкретном resolver/interface проходит design, не новый operator опрос. |
| [C07](requirements.md#c07) | С; Q:L35 | `target` | Q, H, P1 PERM01 | `preserve` — Portal/Research/Runner: structure editor сохраняется; levels/wavefunctions — отдельная budgeted команда, без обещания optics. |
| [C08](requirements.md#c08) | С; Q:L36 | `target` | Q, H | `preserve` — Research/Core: GaAs/AlGaAs наборы с origins/applicability; другие системы через explicit parameters, вне S1 при смене модели. |
| [C09](requirements.md#c09) | С; Q:L37 | `current` | Q, H | `preserve` — All owners: global scientific research cache не добавляется; explicit initial state не скрытый cache hit. |
| [C10](requirements.md#c10) | С; Q:L38 | `current/target` | Q, A §Владение компонентами | `preserve` — Core/Runner: in-memory solve, сохранение и checkpoint различаются; обязательная регистрация локального solve не вводится. |
| [C11](requirements.md#c11) | Н; Q:L39 | `target` | P1 PERM14, DOC03/07 | `implement` — Core/Research content, Runner adapter, Portal help: содержательный model help включён; exact contract решает DOC03. |
| [C12](requirements.md#c12) | Н; Q:L40 | `current/target` | P1 PERM14, DOC03/07, A §Физическая и численная добросовестность | `implement` — Model/formula, numeric value и effective assigning input различаются; current defaults не origin historical run. |
| [C13](requirements.md#c13) | С; Q:L41 | `current` | Q, P1 PERM14, DOC07 | `preserve` — Unknown origins допустимы как explicitly declared research variant; не published/measured и не основание physical acceptance. |

### Исследование и агент

| ID → исходный текст | Historical status / locator | Применимость | Current authority | Action / owning scope и предел |
| --- | --- | --- | --- | --- |
| [R01](requirements.md#r01) | С; Q:L47 | `target` | Q, H, P1 PERM01 | `preserve` — AiiDA/Portal: goal→variants→attempts→analysis связь сохраняется; существующий каталог сам не requirement acceptance. |
| [R02](requirements.md#r02) | С; Q:L48 | `target` | Q, H, P1 PERM01 | `preserve` — AiiDA/Portal: graph показывает actual dependencies, формы создают stages/variants; произвольный DAG editor не требуется. |
| [R03](requirements.md#r03) | С; Q:L49 | `target` | Q, H | `preserve` — Portal/Results: brief/full saved manifest/slices доступны локальному API; bounded reads без обязательного archive download. |
| [R04](requirements.md#r04) | С; Q:L50 | `current/target` | Q, A §Владение компонентами, H | `preserve` — Runner/Results/Platform: NFS daily payload, archive для переноса/recovery; NFS не backup и не гарантирует staging после kill. |
| [R05](requirements.md#r05) | С; Q:L51 | `current/target` | Q, P1 PERM02/15–18 | `preserve` — Человек/агент имеют одинаковые research admission/budget rules; operator destruction не вытекает из research прав. |
| [R06](requirements.md#r06) | С; Q:L52 | `target` | Q, H | `preserve` — AiiDA/Portal: persisted jobs переживают disconnect внешнего клиента; новые решения после resume, unknown submit сверяется. |
| [R07](requirements.md#r07) | С; Q:L53 | `current/target` | Q, P1 PERM16–18, S | `conditional` — Агент автономно исследует несходимость в scope; science ограничено conditional S1, R slots и stop fingerprints, без arbitrary mixing variants. |
| [R08](requirements.md#r08) | С, уточнено; Q:L54 | `current/target` | Q, P1 §S1, S | `preserve` — Allocated cores×execution time включает failures/idle allocation; actual CPU отдельно. S1 добавляет finite node-hour/wall/byte caps. |
| [R09](requirements.md#r09) | С; Q:L55 | `current` | Q, P1 PERM18 | `preserve` — Integrity checks имеют цель/trust boundary; без дублирующих hashes по привычке, без удаления обязательного provenance/raw. |
| [R10](requirements.md#r10) | П; Q:L56 | `current/target` | Q, H, P1 PERM01–02 | `conditional` — Historical П: минимальные domain templates и existing AiiDA; exact interface проходит owning design, новый универсальный DSL не требуется. |
| [R11](requirements.md#r11) | П; Q:L57 | `target` | P1 PERM14, DOC03/07 | `implement` — Включение human/agent model help принято. DOC03 решает version/source/bounded API; неизвестный API не needs_operator для включения feature. |
| [R12](requirements.md#r12) | С; Q:L58 | `target` | Q, H | `preserve` — Research/Portal: отдельный report связан с вопросом и exact attempts; авторский текст не меняет machine statuses. |

### Платформа и управление

| ID → исходный текст | Historical status / locator | Применимость | Current authority | Action / owning scope и предел |
| --- | --- | --- | --- | --- |
| [I01](requirements.md#i01) | С; Q:L64 | `current/target` | Q, H, P1 PERM01/08 | `preserve` — Platform: основной Proxmox и локальные compute, бесплатные решения; новый cloud/Kubernetes control plane не требуется. |
| [I02](requirements.md#i02) | С; Q:L65 | `current/target` | Q, H, P1 PERM03–05 | `preserve` — GitHub source/CI, локальная эксплуатация ready artifacts; G1 merge conditional, public release требует отдельного решения. |
| [I03](requirements.md#i03) | С; Q:L66 | `current` | A §Полномочия и стоимость, P1 PERM09–12 | `preserve` — Foreign VM/jobs/minima и host reserve защищены; похожее имя не ownership и не разрешение cancel/cleanup. |
| [I04](requirements.md#i04) | С; Q:L67 | `current/target` | A §Полномочия и стоимость, P1 PERM07/09 | `conditional` — Platform/Runner: безопасный maximum CPU/RAM по fresh admission, согласованные slices/Nix/Slurm/Julia; foreign jobs не отменяются. |
| [I05](requirements.md#i05) | С; Q:L68 | `current/target` | Q, H | `preserve` — Platform: стандартные declarative limits владеют policy; adapter обеспечивает guards/ordering, ad-hoc скрипт не второй источник policy. |
| [I06](requirements.md#i06) | С; Q:L69 | `target` | Q, H, P1 §S1 | `conditional` — Runner/Platform: auto resource estimate с confidence/reserves и enforceable guards; unknown capacity блокирует submit, physics не уменьшается. |
| [I07](requirements.md#i07) | С; Q:L70 | `target` | P1 PERM08, OPS11–14/17 | `implement` — Platform: Proxmox, Linux/libvirt, Windows/Hyper-V required; native acceptance на обеих Windows machines. Missing backend = partial release. |
| [I08](requirements.md#i08) | С; Q:L71 | `target` | Q, H, A §Светлая тема веб-интерфейса | `preserve` — Portal/Platform: эксплуатационные панели и research cards сохраняются; fixed light во всех состояниях, конкретная сторонняя панель — design candidate. |
| [I09](requirements.md#i09) | С; Q:L72 | `current` | Q, H | `preserve` — Большой performance aggregator stack отложен; состояния/ошибки и данные admission обязательны независимо от него. |
| [I10](requirements.md#i10) | С; Q:L73 | `current/target` | A §Полномочия и стоимость, P1 PERM07, OPS05 | `conditional` — Four-role NixOS/nginx/executable/flake/builder/ownership preflight до heavy stage; не обещание поймать все scientific errors. |
| [I11](requirements.md#i11) | С; Q:L74 | `target` | P1 PERM08/11, OPS09–14 | `conditional` — Platform: reproducible named install/restore по selected source+inventory; current DB/repository/NFS защищены, полный historical wipe не prerequisite. |
| [I12](requirements.md#i12) | С; Q:L75 | `current/target` | Q, P1 PERM13, H | `preserve` — Platform: trusted publisher/object/recipient/reject semantics проверяются отдельно; checksum не signature и не scientific verdict. |
| [I13](requirements.md#i13) | С, уточнено; Q:L76 | `current/target` | Q, P1 PERM09, OPS02/08 | `preserve` — Platform: separate builder/compute VM, ordinary reclaim только после idle/capacity proof; whole-cluster update отдельно I14. |
| [I14](requirements.md#i14) | С; Q:L77 | `current/target` | Q, P1 PERM09–11, OPS08 | `conditional` — Отдельный operator-step: campaign-only cancel после durable proof, затем updater verify empty/stop/update. Old S01/foreign jobs protected; all enrolled workers учтены. |

### Документы и пересборка

| ID → исходный текст | Historical status / locator | Применимость | Current authority | Action / owning scope и предел |
| --- | --- | --- | --- | --- |
| [D01](requirements.md#d01) | Н; Q:L83 | `current/target` | P1 PERM14, DOC01, A §Независимая проверка и завершение | `implement` — Root/docs owners: один corpus и dispositions, history отдельно; эта правка не доказывает полную миграцию component docs. |
| [D02](requirements.md#d02) | Н; Q:L84 | `current` | Q, H, DOC01 | `preserve` — Root/all owners: requirements→target→actual baseline; source defect не создаёт новое требование сам по себе. |
| [D03](requirements.md#d03) | Н; Q:L85 | `current` | Q, H | `preserve` — Owning design: primary evidence, alternatives/counterexamples/cost; этот пакет не повторяет архитектурный аудит всех tools. |
| [D04](requirements.md#d04) | Н; Q:L86 | `historical` | Q, P1 PERM11–12, A §Полномочия и стоимость | `needs_operator` — Полный wipe existing QCL state не входит в B. Новое destructive действие требует exact target+решения; approved disposable cleanup остаётся PERM12. |
| [D05](requirements.md#d05) | Н; Q:L87 | `historical/target` | Q, P1 PERM06/09, OPS01 | `conditional` — SSD/100GB/swap — historical site request, exact current topology unknown. Сначала inventory/admission; swap не scientific RAM, unknown disk не resize grant. |
| [D06](requirements.md#d06) | Н; Q:L88 | `historical/target` | Q, P1 PERM08/11, OPS09–14 | `conditional` — After-wipe bootstrap сохранён только как historical clean-install scenario. Текущий named install/replacement защищает persistent data и требует backup/restore gates. |
| [D07](requirements.md#d07) | С; Q:L89 | `current/target/historical` | Q, P1 PERM02/08/11/13 | `conditional` — Fresh selected clone/gitlinks+trusted private inputs сохраняются; запрет old-state recovery относится только к historical clean-install, не отменяет current verified restore. |
| [D08](requirements.md#d08) | Н, ориентир; Q:L90 | `historical` | Q, H, P1 §B-envelope/§S1 | `preserve` — Суточный ориентир не deadline/SLA/scientific bound; текущие конечные caps и measured progress действуют отдельно. |
| [D09](requirements.md#d09) | Н, уровень С; Q:L91 | `target` | Q, P1 PERM14, DOC02/04 | `preserve` — Core/Research docs: tutorial-first для QM/semiconductor reader плюс full expert reference; уже принятая аудитория не переопрашивается. |
| [D10](requirements.md#d10) | П; Q:L92 | `target` | P1 PERM14, DOC03–05/07 | `conditional` — Historical П статического docs artifact: pilot/local light/offline help включены; generator/pins/serving API ещё owning design, не новый scope approval. |
| [D11](requirements.md#d11) | Н; Q:L93 | `current/target` | A §Физическая и численная добросовестность, P1 PERM14, DOC02/03/07 | `implement` — Core/Research/Runner владеют formula/value/origin; UI показывает canonical content и used overrides, unknown не скрывается. |

## Существенные решения и локальные остатки

| Пакет | Решение 2026-10-19 / источник | Что остаётся неизвестным или условным |
| --- | --- | --- |
| S01 и scope науки | P1/PERM15–17 закрывает старый F00-02: цель 0 mV/period, 70 K, без e–e; все пять каналов сохранены | SCI03 criterion bounds и READY, actual resources/byte guards, convergence/discretization/physical verdict. Finite-bias/optics/experimental validation вне S1 |
| GUI/domain features | C03/C04/C07/R01/R02/I08 сохраняются target полного scope H/PERM01 | Не объявляются реализованными и не задерживают B0 при закрытых собственных gates |
| Historical П и help | C06/R10 exact mechanisms — owning design; R11/help DOC07 включён PERM14; D10 pilot выбран в DOC03–05 | Новые schema/API/generator/pins не приняты наличием текста; неизвестный API не причина повторно спрашивать включение help |
| Required backend | PERM08 + OPS11–14/17 сохраняют три backend и обе required Windows machines | Missing hardware/native receipts оставляют release partial; отказ от backend требует operator decision |
| D04/D06/D07 clean install | D04 full wipe historical; текущий P1 защищает existing DB/repository/NFS/raw и требует verified backup/restore | `needs_operator` только для нового destructive scope. Named disposable targets/cleanup PERM08/12 не требуют повторного общего разрешения |
| I14 cancellation | Исторический отдельный operator-step сохранён; PERM10 допускает агенту campaign-only cancel после durable proof; updater только проверяет empty/stop | Old S01/foreign/unknown ownership не становятся campaign-owned; unknown cancel outcome сверяется по persisted IDs |
| R07/R08 автономность и бюджет | S1 задаёт конечный conditional catalog, caps/stop fingerprints; no hidden physics change | Arbitrary new method/mixing variant, новые waves, расширение ceilings или second final CI требуют отдельного решения |

Первичные historical message locators неизвестны; это честный provenance gap,
а не общий blocker для DOC/DEV. Ни один новый operator packet не нужен, пока
решение остаётся внутри уже принятого scope и predicates P1. Если понадобится
wipe, смена physics/backend/trust или выход за caps, packet локализует только
это зависимое действие с exact target/evidence/альтернативой.

## Приёмка этого appendix

Denominator — исходный textual set **S01–09/C01–13/R01–12/I01–14/D01–11**.
Требуются exact59/59 без новых/потерянных ID, исходные тексты/статусы/acceptance
cells, явные epoch/unknown primary/current locator/state/action, links/anchors,
Markdown format и independent review. Count не semantic acceptance.
Исходные байты historical bundle не редактируются. Numerical tests, imports,
docs build, browser/native/server и solver в DOC01 не выполняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| 59 ID имеют current disposition | Original Q hash/rows и ledger выше; P1/DOC01 | Primary historical messages unknown; textual coverage не acceptance | сохранить |
| S01/help/backend scope уже выбран | P1/PERM08/14–17 и DOC07/OPS13 | Exact API, native READY и physical outcomes требуют своих evidence | сохранить |
| Полный historical wipe разрешён текущим B | D04 original против P1/PERM11–12 | Existing persistent данные защищены; нового destructive target нет | изменить |
| Реализация и scientific acceptance установлены DOC01 | Только документационный diff и static checks | Для всех59 implementation/native/science evidence здесь unknown | данных недостаточно |
