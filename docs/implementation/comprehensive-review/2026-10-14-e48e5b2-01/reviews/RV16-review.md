# RV16 — независимое review трёх atomic packets

Статус: **static candidate допустим с двумя адресными P3 corrections**; no blocking science/runtime overclaim. Blind findings/questions сохранены до candidate в [RV16-blind.md](RV16-blind.md).

Inputs: root frozen README SHA256 fffa603593e830a81a22c9e5b1807be930509cb9c7569b15a33381cf9725e525, source receipt S e48e5b2… + eight gitlinks; Core 3108150dd1b6b1377470b384b15c26e272fe5c5d numerical-policy/12_validation/make; Runner 0c53c6d0f68e0b25fce79388db831da6fc3ae856 api/public, configuration_types::configuration_source, configuration_sources::validate_configuration_source, T024 merge-order/fail-closed test source, user/results/make; root+8 source filenames/build configs; frozen methodology и M14–M17.

Reviewed candidate SHA256 `8e9c4db459d20b59f7a15a5609502ef7fc3f0a28899d449be65c6db6b4a56915`, inventory `04f07c4816659d916d89ca82801208d35d3c178ab7b03a5d24dfadd13ceb14cb`, proposed materials `793dfec8b95f1d8728779b12fa77e15f2a279cd2d8d74cf2efde882d98c81ca8`. Эти identities относятся к прочитанной версии, не будущим исправлениям writer.

Общий conservative reviewer envelope: 2026-10-14 17:52:30 UTC → 2026-10-14 17:59:34 UTC; <8min. Он включает shared source discovery двух reviews и не суммируется по пакетам. Isolated packet CPU/peak RAM/time не измерены; lightweight sequential text reads/stdlib, без numerical payloads. Writer isolated timings отсутствуют; author+review ≤20min нельзя назвать измеренным, coordinator ведёт общий wall grant. Это ограничение не блокирует статический findings verdict. Tests/build/install/import/solver/browser/server/PR/comments не выполнялись.

## P1 — inventory/denominator/source/delivery

Независимо воспроизведены document counts root68/Core36/Runner11/AiiDA5/Contracts2/Platform22/Portal3/Research6/Results3 =156; target configs учитывают test/fixtures, не public option count. Runner generated build:20 files/2591034 bytes совпал. Git tracked filenames + frozen root overlay исключают текущий campaign. 9/9 segments — lexical inventory; all-symbol/semantic/full docs denominator неизвестен и candidate не объявляет его измеренным. Source-file counts и role public surfaces отделены от doc readability. Core/Runner make.jl pages и строгий checkdocs/doctest — config, не build log; deploydocs отсутствует; приложение Portal не scientific docs generator. Dark/light assets existence не утверждение активной dark темы.

**P3/R16-01 — неоднозначный filter native locks.** Locator fixes/RV16-inventory.md:5, root Config N18/hash da69ebaed84126e99860aab9e68689d40318171fe833677c172adf30ceb0881b и Core N5/hash6ba0efdc5f0b62c4b2da93dd1bd4d4dca0005de9ac28035ca2a07dd886c82334. Counts/hashes воспроизвелись при сохранении `julia/Manifest.toml` root и `Manifest.toml` Core, хотя prose говорит «без lock-файлов». С исключением этих Julia native locks — root17/Core4 и иные hashes. Остальные семь config hashes совпали. Минимальная коррекция — явно retained Manifest.toml и exact exclude names + sorted path list + trailing newline SHA256 recipe; либо единообразно пересчитать исключив их. Severity P3: воспроизводимость lexical denominator, scientific criteria не меняются. Writer уведомлён напрямую.

Blind observation dated README/local publication/S01 подтвердился; candidate уже сохраняет distinction source versus current clone/publication. Не требуется corpus rewrite. Document historical labels не отменяют пользовательские правила/согласования.

## P2 — selected chapter/reference/goal runbook и three journeys

Researcher: numerical-policy объясняет raw versus mixed/fresh U/G; самостоятельный scalar example proposal α=.01/.5 и S=100meV корректен при одной norm/positive fixed scale и явно не переносится автоматически на Anderson/Pulay/state-dependent scale. Blind после truncated первичного extract оставлял вопрос registry; адресная проверка `12_validation.md:13–64` затем подтвердила passport: applicability/weights/units/norm/floor, pass/fail/not_measured/not_applicable/error, strict iteration `<` против final `<=`, tolerance policy и source registry. Candidate не выдаёт theoretical numeric example за current run evidence. Artifact/receipt/HDF5 raw selection не входил в RV16, поэтому R16-G1 допустимый exact gap, без generic dataset invention.

Operator: user/results recovery prerequisites совпали: whole generation+prior finals, identity/new attempt/used budget, pending not resumable, corrupt latest→verified previous, both lost→error; local_filesystem receipt не LAN durability. Proposed goal path сохраняет эти guards, scientific acceptance не следует из publication. R16-G2 обоснован как presentation improvement, не найденный corrupted recovery implementation.

Developer: configuration_source source:209–222 returns last history или nothing. Loader source:24–59 supplied order/schema/provenance; T024 case base,A=17,B=23 →23/sourceB, reversed→17, fail-closed invalid units/key/path/duplicate/incomplete/missing документирован исходниками. `energy_chunk` unitless; lookup return filename без physical units. Missing assigning history не schema default. Нет execution claim/универсальной guarantee origin. Проposed 17/23 example корректно требует full base и source/code/test owner.

**P3/R16-02 — неверный selected subsection.** RV16.md:33,54 отсылает configuration_source к §Extension contracts. На exact Runner `docs/src/api/public.md:7,34` он в §Types and operations; §Extension contracts:78,90 содержит validate_configuration_source. Минимальная коррекция: два точных subsection locators для lookup и loader; symbol/code locators верны. Это навигация, не ложный API behavior. Writer уведомлён.

Методологический rule→predict→reason→single-change→boundary сохранён в трёх proposals; firsthand Java read missing явно назван. Frozen QCL adaptation не объявлена самостоятельно прочитанным Java source, пять course projects/Quarto не перенесены. Source-only research/operator/developer journeys имеют exact gaps; delivered/browser/offline/search/light acceptance не выводится из этого.

## P3 — metrics/role actions/caps/refactoring handoff

M14/M15 по одной selected boundary не заявляют full N; M16 9/9 inventory не drift score; M17 3/3 addressed static tasks не completed role×light/offline/search runtime matrix (0 executed, readability/time not_measured). Три роли получают действия и prerequisite gaps; code/model/artifact/runtime evidence разделены. Proposals R16-C1–C4 явно docs-edit/design scope, не исполненные patches или grant builds/browser/solver. Broad authoring/RV18 pilot требует отдельного назначения; карточка передаёт current high-value static facts.

Report P1/P2/P3 sections independently measured 6110/5716/6910 bytes <8KiB; total20k report разрешён aggregated packets. Inventory subsections bounded, report/source hashes отдельно. Reviewer сохранил blind findings, не менял candidate/fixes/source/progress/index. Writer timings нет в reviewed candidate: not_measured; это budget-accounting limit, не blocker статического verdict. Coordinator timing bounds может добавить writer, без fabricated isolated clocks.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| 9/9 source segments и selected roles рассмотрены | Git+overlay filename recount; source chapter/API/recovery read | Не all-symbol/current browser delivery acceptance | сохранить |
| Config lexical recipe нуждается в уточнении | Reproduced N18/N5 содержит Manifest.toml; inventory says no locks | Counts корректны для фактического retained set, prose filter неполон | изменить |
| API subsection locator требует коррекции | api/public:7/34 vs78/90; RV16:33/54 | Symbols/signatures/semantics верны | изменить |
| Science/raw/result и native recovery unknown сохранены честно | Candidate G1–G3, M14–17, proposals boundaries | Нет artifact source/run/raw selection/browser/native execution | дополнительно измерить |
| Пакет timing измерен лишь conservative reviewer envelope | Review wall clock; author isolated clocks отсутствуют | Author+review sum не measured | данных недостаточно |

## Round1 — scoped recheck двух текстовых corrections

Только изменённые строки, без повторной inventory/symbol/native/browser проверки. Current reviewed RV16.md SHA256 `5fa75c3a40c95a7c7be736c68f28f1ae33aafd622eb8485c0f4d9e637fcde3b7`; fixes/RV16-inventory.md SHA256 `568add375555d9bbd6e4b2b2d04822b1285653feb98c41af12e7e9dc1b3ad429`. Чтение 2026-10-14 18:04:01–18:05:05 UTC входит в общий boundedreview; новое isolated timing не выдумано.

P3/R16-01: inventory:5 теперь явным текстом исключает filenames с lock case-insensitive, но сохраняет root julia/Manifest.toml/Core Manifest.toml. Это устраняет противоречие retainednative locks с прежним «без lock-файлов»; counters/hashes намеренно не пересчитывались в этом recheck. P3/R16-02: RV16:33/54 разделяет §Types(configuration_source) и §Extension contracts(validate_configuration_source/loader); exactsource locations api/public:34 и90 соответствует исправлению. Полное heading в source «Types and operations», сокращённое Types однозначно.

Оба requestedtext corrections приняты; прежний staticcandidate verdict сохранён. Runtime/source delivery/metrics unknown и writer-isolatedtime limit остались; recheck не закрывает их. Дальнейшее broad authoring/полный docs build не входит в этот scope.
