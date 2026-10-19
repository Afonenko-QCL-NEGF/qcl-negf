# Coverage: каждый результат review имеет маршрут закрытия

**Статус: план, не выполненная remediation.** Таблицы связывают первичные
findings с карточками, владельцами и будущим различающим свидетельством.
Назначение task не закрывает finding. Исходные verdict сохраняются отдельно
от нового outcome; source proof, synthetic fixture, native receipt и scientific
evidence не взаимозаменяемы.

Основной вход — [README](README.md), permissions — [autonomy](autonomy.md).
Tasks определены в [development](development.md), [platform-worker](platform-worker.md),
[science](science.md), [documentation-instructions](documentation-instructions.md).

## Источники и denominator

Обозначение **A** ниже — published primary public review
`docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/`.
Все148 original campaign files и2 frozen overlays входят в Git. Их hashes,
неизвестные private/native inputs и исторические пути описаны в
[PORTABILITY](../comprehensive-review/2026-10-14-e48e5b2-01/PORTABILITY.md).
External `REVIEW_BUNDLE_DIR` и локальный путь компьютера автора не требуются;
publication receipt — immutable artifact evidence, не maintained source lock.

Полнота сопоставления: 20 отчётов RV00–19, семь SI proposals внутри RV17,
28 individual fixcard files в `A/fixes/`; `index.md` — навигация, не 29-я задача.
59 textual requirements и 34 selected operator packets/102 properties —
исторические denominators review. Их количество не доказывает выполнение,
корректность или исчерпывающее покрытие всех свойств модели.

Новый task denominator: **75 уникальных карточек** = 25 DEV + 17 OPS + 15 SCI
+ 7 DOC + 7 SI + 4 INT. Task ID — координационная единица, а не число будущих
PR, новых алгоритмов или scientific attempts. Accepted proposal может быть
реализован; уже корректный boundary сохраняется и проверяется; альтернативы
получают disposition. Требование «отработать всё» не означает внедрить все
взаимоисключающие alternatives или повторить уже вошедший fix.

## RV00–19 → owning work → свидетельство

| Report | Фактический предмет и граница вывода | Owner / задачи | Необходимый выход и оставшийся уровень проверки |
| --- | --- | --- | --- |
| RV00 | Ledger 59 requirements; исторический текст и implementation не заменяют primary operator decision | Root/Research: DOC01, SI01, INT01–04; SCI02/09 | 59 dispositions с authority/epoch/unknown, только существенные conflicts оператору; scientific selection отдельно от requirements cleanup |
| RV01 | Паспорт saved S01, не live state и не итог решения | Research/AiiDA/Results: SCI01, SCI04/06/10/15; OPS01/17 | Exact model/plan/run/attempt/CalcJob + completeness; старый terminal/raw только при доступных originals. Новый run не восстанавливает старую историю |
| RV02 | Exact Results PR6 owning imports; старый PR head не равен current gitlink | Results/integration: DEV21–22, INT02 | Проверить актуальный base/head/diff существующего PR, продолжить его; owning import/installed route и independent controls на новом source. Source чтение не pass тестов |
| RV03 | Actual dependency/context/job/deployment views и сохранённые owners | Root + затронутые owners: DOC01–03, DEV09/12/15/17/19, OPS02/04 | Обновить только реально изменённые edges, ownership и source bindings. Dynamic graph или массовый refactor из review не следуют |
| RV04 | Core/Runner call/mutation owners, expert API effects | Core/Runner: DEV02–08/15/17–18, DOC02/06 | Прозрачные формулы, side effects и assigning source, малые различающие assertions. Existing cohesion сохранить; API redesign только при конкретной необходимости |
| RV05 | Actor caller deadline, remote mutation outcome и close/export lifecycle | Portal/AiiDA: DEV12–13/23; OPS14 | Accepted semantics до кода, bounded response/unknown/reconciliation/close fault receipts; synthetic actor control не доказывает native AiiDA shutdown |
| RV06 | Controller activation ownership: source counterexample, native incident не установлен | Platform: OPS02–03/08–09/14 | Один controller owner и owned child без deadlock/reentrant loophole; crash/retry/standalone controls и затем native receipt на identified targets |
| RV07 | Composite attempt pin, legacy size description scope и packaged schema drift | Contracts/Runner/AiiDA/Portal: DEV09–11/14–16; DEV24 | Frozen exact child для bytes/plan/status/cache, canonical description/copy provenance и drift rejection; public rejection не подменяет научную приёмку |
| RV08 | Operator cards, D08 prose и шесть независимых oracle gaps | Core: DEV01–08; Research/Results: SCI03–06/14; DOC02 | Три точечных docs corrections, шесть property passports и independent assertions; current normalization/seed/basis code не менять только по ошибке prose |
| RV09 | Что реально различают existing tests и где oracle зависим от implementation | Core/Results/Contracts: DEV02–08/21/23–25; SCI03–06/14 | Oracle independence и negative controls; existing CR05/single-file CR01 не внедрять повторно. Совпадение двух несошедшихся states не solution verification |
| RV10 | Scientific question, model/value origins, seven unknowns и finite next gate | Research/Core/Runner/Results: SCI01–15; OPS17 | Primary-source reconciliation, justified criteria, frozen finite catalog, convergence studies и independent physical verdict; экспериментальная validation отдельна |
| RV11 | Immutable scientific publication/raw protocol и более слабый generic checkpoint contract | Runner/Results: DEV17–18, SCI04/06–08; Platform: OPS10 | Preserve сильный scientific путь; определить generic durability scope, barriers и independent crash reader. fsync mocks не доказывают NFS/power loss |
| RV12 | Finite attempts, submit ambiguity, cancel propagation и deadline | AiiDA/Portal/Runner/Platform: DEV12–13/23, OPS08–09/14, SCI09/13 | Persisted owned IDs, reconciliation, no duplicate/no orphan; unit/source доказательства плюс native faults. Disconnect не означает remote stopped |
| RV13 | Coordinated backup/restore и public/private boundary | Platform/operator: OPS01/10–15 | Fresh private inputs, isolated restore, verified generations, measured RPO/RTO, tested backend receipts. Старый site не fresh admission; live restore требует CP-OPS |
| RV14 | Source/build/import/runtime identity, stale assets и route differences | Portal/Results/integration: DEV19–22/25; Platform: OPS04–07/16; DOC04–06 | Exact source→derivation→contents→imports→assets chain и deliberate wrong/stale source controls; package version или old pass недостаточны |
| RV15 | Public trust/rejected paths и redaction | Portal/AiiDA/Contracts: DEV11/24; Platform: OPS04–05/09; DOC05 | Независимые invalid locator/auth/path/schema/unknown controls, secret-free outputs; native TLS/nginx/SSH trust проверяется отдельно, границы сохраняются |
| RV16 | Evidence inventory и три reader routes | Root/Core/Runner: DOC02/05; DEV01 | Inventory сохранить как evidence appendix; адресно улучшить researcher/developer/operator материалы и пройти три reader journeys. Inventory не новый implementation scope |
| RV17 | Семь независимых instruction proposals | Root/skills/owners: SI01–07; DOC01, INT01/03 | Реальные AGENTS/references/skills/UI paths, одна authority и task policy, static/formal/tabletop/forward результаты раздельно; число файлов не behavioral proof |
| RV18 | Один docs hub/pilot, light/offline/source binding | Docs/Portal/Platform: DOC03–05/07; OPS05/15 | Existing stack preserve, один pinned pilot и browser journeys; direct `/docs/`/offline/light checks. Optional UI help зависит от accepted scope |
| RV19 | Source-of-truth, authored scientific meaning и безопасная генерация | Contracts/Runner/Core/Docs: DEV14–16, DOC02–07 | Один API+config prototype, truthful static facts и separate meaning/value/assigning origins; generation не выводит физический смысл и не запускает target imports |

## Все 28 original fixcards

Имена ниже буквально соответствуют `A/fixes/`. Эта таблица нужна, чтобы
проверить полноту handoff относительно конкретного архива, а не поддерживать
второй issue tracker. Execution status/receipts ведутся в одном coordination
checkpoint; в этой таблице при закрытии оставляется ссылка на его решение.

| Original fixcard | Карточки handoff / владелец | Disposition и будущая проверка |
| --- | --- | --- |
| `RV00-requirement-provenance.md` | DOC01, SI01, INT03 / Root | Authority/epoch ledger, primary conflicts без повторного опроса принятого scope |
| `RV00-scientific-selection.md` | SCI01–03/09, DOC01 / Research | Separate selection/model/criteria packet, CP-SCI |
| `RV00-scope-and-proposals.md` | DOC01/03/07, SI01 / Root | implement/preserve/conditional/needs_operator; mutually exclusive alternatives не все внедряются |
| `RV02-selected-check.md` | DEV21–22, INT02 / Results | Existing PR6 exact current candidate и owning route controls |
| `RV05-actor-deadline.md` | DEV12–13/23, OPS14 / Portal/AiiDA | Design → fault fixtures → native outcome/close evidence |
| `RV06-01-controller-activation-ownership.md` | OPS02–03/09/14 / Platform | Owned lifecycle helper/capability по accepted design, no standalone overlap/deadlock |
| `RV07-attempt-export.md` | DEV09–11/24 / AiiDA/Portal | Immutable exact child на всём composite export, deliberate moving-publication case |
| `RV07-legacy-doc-scope.md` | DEV14/16, DOC06 / Contracts/Runner | Description cap только применимому legacy scope; consumer/package copy согласованы |
| `RV07-schema-drift.md` | DEV15–16, DEV24 / Runner/Contracts | Canonical source/provenance и enforcement при deliberately stale schema |
| `RV08-doc-and-oracle-handoff.md` | DEV01–08, SCI03–06 / Core | D08 three prose fixes, six independent property passports/assertions |
| `RV09-oracle-gaps.md` | DEV02–08/21/23, SCI03–06/14 / Core/Results | Независимый oracle и различающие отрицательные случаи; no redundant CR05/CR01 rewrite |
| `RV09-selected-check.md` | DEV03–08/21/24–25 / Core/Results/Contracts | Selected controls с actual invocation/source receipts и limitations |
| `RV10-next-gate.md` | SCI01–15, OPS17 / Research | Seven unknowns, justified finite convergence/physical attempt и separate report |
| `RV11-runtime-durability.md` | DEV17–18, SCI07–08, OPS10 / Runner/Platform | Generic scope/barriers, independent reader и isolated native fault evidence |
| `RV13-01-bounded-restore-evidence.md` | OPS01/10–15 / Platform | Private inventory/admission, verified recovery, RPO/RTO и tested targets |
| `RV14-asset-contract.md` | DEV19–22, OPS04–07/16, DOC04–05 / Portal | Accepted asset/source contract, stale controls, native/static routes отдельно |
| `RV16-inventory.md` | DOC02, INT03 / Root | **Preserve evidence appendix**; не самостоятельная rewrite/implementation задача |
| `RV16-selected-materials.md` | DEV01, DOC02/05 / Core/Runner/Root | Три точечных reader routes и независимая reader acceptance |
| `RV17-SI01-claims.md` | SI01, DOC01 / Root | 7 claim dispositions с authority и epoch |
| `RV17-SI02-contract.md` | SI02, INT01 / Root | Один nine-field contract, без второго процесса или approval каждого ticket |
| `RV17-SI03-routing.md` | SI03 / Root/components | Action routing + eight owning contribution instructions, invariants preserved |
| `RV17-SI04-references.md` | SI04 / skills | Четыре existing references, current/archive/standalone lookup |
| `RV17-SI05-skills-ui.md` | SI05 / skills | Четыре skills + четыре UI files, actual path/name/behavior checks раздельно |
| `RV17-SI06-engineering-route.md` | SI06 / Root/skills | Existing engineering route preserve, новый skill только при подтверждённом repeated gap |
| `RV17-SI07-validation.md` | SI07, INT03 / independent reviewer | Formal/tabletop/forward split, фиксированный sample envelope, no hidden execution |
| `RV18-pilot.md` | DOC03–05/07 / Docs/Portal | Один pinned publication pilot и light/offline/direct route checks |
| `RV19-prototype.md` | DOC03/06, DEV14–16 / Docs/Contracts/Runner | Static one-API/one-config prototype, imports запрещены в extractor route |
| `RV19-source-meaning.md` | DOC02–03/06–07, DEV15 / Research/Core/Runner | Формула/value/assigning/effective source различаются; unknown остаётся unknown |

## Семь SI proposals: отдельные решения и свидетельства

| Proposal | Primary report/карточка | Работа и effort | Критерий закрытия |
| --- | --- | --- | --- |
| SI01 | RV17 SI01 / claims | SI01 D ultra + R high | Семь claim dispositions привязаны к authority, epoch, source и текущему scope |
| SI02 | RV17 SI02 / contract | SI02 D ultra + R high; narrow accepted edits I medium | Один nine-field task contract включает grants/stop/evidence; routine technical CP не human approval |
| SI03 | RV17 SI03 / routing | SI03 D ultra + R high | Routing в AGENTS/owning instructions точен; физические/admission/light/CI-once constraints сохранены |
| SI04 | RV17 SI04 / references | SI04 D ultra + R high | Четыре references открывают current/historical/archive/standalone маршруты и missing-source handling |
| SI05 | RV17 SI05 / skills-ui | SI05 D ultra + R high | Четыре SKILL.md и UI metadata согласованы; имена/units/permissions не испорчены, source-only analysis доступен |
| SI06 | RV17 SI06 / engineering | SI06 D ultra + R high | Preserve/conditional disposition; новый skill имеет реальный recurring use case и owner либо не создаётся |
| SI07 | RV17 SI07 / validation | SI07 R high, focused redesign D ultra | Validator receipt, manual metadata checks и восемь read-only fresh forward samples раздельны; no product/server/solver execution |

## Уровни закрытия и передача между направлениями

1. **Software:** exact component/root refs + meaningful controls, CP-CODE/
   CP-RELEASE. DEV25 не является обязательным глобальным gate для каждого
   exploratory SCI или независимой OPS task; нужна только релевантная closure.
2. **Native/build:** fresh identity/admission, four-role/nginx preflight, immutable
   build и isolated tests. BUILD не разрешает production mutation.
3. **Cluster/worker:** CP-OPS на конкретных candidate/targets и native receipts,
   выдаваемый distribution + walkthrough. Required missing Windows/другой backend
   оставляет full release partial, но не останавливает независимые исследования.
4. **Science:** CP-SCI на justified frozen contract и finite conditional catalog,
   immutable raw arrays и independent five-level verdict. B0/E1/P1/K1 могут дать
   отрицательный результат; missing convergence не маскируется pass.
5. **Experimental validation:** только применимые independent experimental data,
   соответствующая модель и uncertainty. Её отсутствие не мешает честно завершить
   convergence/physical attempt report, но запрещает заявить validated device.

Сервер сейчас недоступен; OPS read/native и cluster SCI остаются pending.
Слова пользователя «после review работ не было» — контекст, не live admission,
не terminal state и не подтверждение отсутствия чужих jobs.

## Формат итогового решения

INT03 заполняет строку для каждого существенного claim и unresolved finding:

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Требуется либо сохраняется конкретное поведение | commit + path/symbol; fixture receipt либо artifact hash + HDF5 path/sample | Applicable route/model/source, unknown/native/primary gaps | сохранить / изменить / дополнительно измерить / данных недостаточно |

До execution все tasks имеют состояние **planned**, кроме текущих проверок
самого текста handoff. Ни один planned output в этих таблицах не считается
existing artifact, исправленным кодом, работающим кластером или physical pass.
