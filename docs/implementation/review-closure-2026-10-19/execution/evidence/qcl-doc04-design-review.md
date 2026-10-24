# DOC04: независимый high CP-DESIGN review

2026-10-19. **PASS — CP-DESIGN для описанного source/recipe/presentation contract с явно blocked math/assets/BUILD ветвями.** Новых blocking противоречий принятому DOC03 или проверенным pinned source facts не найдено. Это не READY на render/publication, не implementation/runtime/browser/native/science PASS и не разрешение установки, загрузки, CSP exception или нового budget.

Этап B выполнен последовательно после отдельного A. No imports/parsers/target tests/Julia/Python target execution/build/network/server/Git mutations/children. C08 reviewer=0. Единственная запись B — этот report; A сохранён отдельным report. Никакой actual documentation artifact не создавался.

## Identity и первичные свидетельства

| Artifact / primary source | SHA256 |
| --- | --- |
| `/tmp/qcl-doc04-design.md` | `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b` |
| `/tmp/qcl-doc04-identity.json` | `924fed8c97da7fa25ad0fe579789d4d8a44b46e5d5bb575bdbf6158bf7a82356` |
| Published root DOC03 `docs/system/physics-documentation.md` at cfc38e1 | `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb` |
| Root `julia/Manifest.toml` | `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47` |
| Pinned Documenter `src/html/HTMLWriter.jl` | `72b261cbef5e06e9edc4159c038d740b5f5372134f9d75db06eeb35b894b29dd` |
| Pinned Documenter `src/html/RD.jl` | `23f894f57a42f1892911b96b06ca15bc2e23f76dd4269484d56198319ea5ce79` |
| Pinned Documenter `src/documents.jl` | `67ded455a9d8881b6fe3cf4a4cfbc97a992e27cd8e31ad3d28de23cbc3578e06` |

Primary package source directory:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.build/local-julia-int01/depot-1/packages/Documenter/AXNMp`.
Manifest selects Documenter1.17.0, UUID `e30172f5-a6a5-5a46-863b-614d45cd2de4`, tree `56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`, Julia1.13.0. Project version и отдельные source hashes сверены; полный установленный package tree и actual executable identity этим review не подтверждены.

Перед чтением авторских выводов прочитаны опубликованный DOC03 (bundle/fragment/allowlist/build/serving/CSP scopes), actual pinned HTMLWriter/RD/themeswap/search sources, owning existing make.jl recipes, Portal CSP и existing root CI/docs composition. Затем прочитан весь proposed design §§1–10. Source discovery receipt не использован как самостоятельное доказательство behavior.

Design baseline root `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; выбранные gitlinks Core7324d98/Runner9378396/Contracts12fc264 сохраняют свою identity. Local Coree431609/Runner1acc165/Results33b1a39 и dirty coordination не становятся новыми published build inputs автоматически. Future sourceGraph требует новый clean published composition с reviewed recipes/dependencies; current dirty checkout не объявлен release-ready.

## Принятое engineering решение и contract trace

### Три slices и научное владение

Дизайн сохраняет existing Documenter и три reader journeys:

- Core SCBA route `core/theory/09_scba.html#researcher-scba-route`, с переходом к final assessment;
- Runner API/configuration routes с existing API/schema/effective/assigning distinctions;
- отдельный authored public Root operator recovery chapter, с canonical Runner recovery route, preserve-failed-attempt/new-attempt/missing-data boundaries.

Primary slices не выдают четыре упомянутые Markdown pages за полный isolated build. Existing Core/Runner page graphs сохраняются явно ради @ref/@docs closure и checkdocs=:exports; support pages/assets входят в input/output manifest. Это честно ограничивает пилот по reader acceptance, сохраняя локальные canonical cross-links. Operator modules=[]/checkdocs=:none обоснованы отсутствием package exports и не ослабляют owning default recipes.

Root chapter не публикует исторический deployment runbook/receipts/private inventory. Model equations/criteria остаются Core, parameter origins Research, effective resolution Runner; presentation adapter не добавляет evaluator, arbitrary run capture или новую scientific authority. Empty fragments=[] допускается лишь как явно пустой catalog, без dummy known origin. Финальный DOC03 bundle требует published shared schema; отсутствие schema блокирует соответствующий serialization claim.

### Pinned Documenter → presentation adapter

Primary source подтверждает необходимость отдельного output adapter:

- HTMLWriter THEMES содержит light, dark и catppuccin variants; render_settings создаёт Automatic(OS) и picker; themeswap читает localStorage и OS preference.
- RD/head содержит versioned remote libraries/fonts/KaTeX CSS, CDN RequireJS; HTMLWriter выдаёт inline documenterBaseURL и версии/themes scripts.
- Search source использует remote importScripts и Blob Worker. Existing Portal policy `default-src/script-src/style-src/connect-src 'self'; object-src 'none'; base-uri 'none'` не разрешает эти default resources/inline scripts/blob.
- Public constructor не имеет `theme/offline/cdn=false` magic kwargs. Design их не выдумывает и не patch-ит installed Documenter consts/methods.

Выбран version-bound source/output presentation adapter с точными hash/shape guards и fail-closed unknown shape. Он удаляет alternate themes/picker/settings/version runtime, externalizes единственный известный page-base script, сохраняет source article/heading/anchors/TeX identity, связывает raw→public transforms и заменяет ресурсы только admitted local closure. Fixed-light не опирается на late CSS concealment или запись user preference. Отказ на unknown script/event/style/resource shape вместо CSP exception соответствует DOC03.

Важное operational условие, уже подразумеваемое design §5.1 и обязательное для I: **admitted source/assets/documenter.js override должен существовать до Documenter render**. В pinned RD исходнике есть `mathengine(::RequireJS,::Nothing)`, тогда как normal generation вызывает `mathengine!`; поэтому один accepted constructor keyword `mathengine=nothing` нельзя считать доказанным standalone normal-bundle path. Предложенный documented override обходит этот normal generation branch (HTMLWriter:850–876), что согласуется с выбранным contract. Missing override/hash должен закрываться input/shape gate, а не best-effort fallback. Это не новое API, не blocker выбранного adapter route и не claim исполненного render.

### Offline search и math

Static same-origin Worker + local MiniSearch6.1.0 сохраняет pinned search ranking/filter/result logic, меняет transport/init вместо Blob/import-CDN. Explicit ready handshake предотвращает query до index init. Worker resource URL не поступает из query; search index locations сверяются с actual version-local targets. Это presentation search, не новый cross-corpus service/evidence store. Runtime CSP/keyboard behavior правильно оставлен DOC05 observation.

Math ветвь **не готова к implementation/render acceptance**: отсутствуют admitted KaTeX0.16.8 source/distribution/hash/license/font closure и проверенная exact API binding. Pinned RD действительно выбирает0.16.8; unrelated vendored version не замена. Expected renderToString binding — условная design target, не установленный source fact. До exact source/API verification допустимы recipe guards/schema/non-math work, но не запуск неизвестного API либо подстановка другой версии/latest.

Build-only static math с trust=false, strict failure и no user macros/plugins не переносит physics evaluator в browser. Source TeX/IDs/fingerprints сохраняются. Inline math в pinned HTMLWriter — обычный span с dollar delimiters, display — p.math-container. Поэтому required checked source→node mapping нельзя заменять global dollar regex: real mapping/selector, preservation и unsupported-case negatives должны быть реализованы/проверены вместе с разблокированием math branch. Design это ограничение явно задаёт. Deterministic style→external-class transform должен сохранить presentation и пройти actual KaTeX source/layout/CSP gate; source review не доказывает такую эквивалентность.

## Assets, import effects, source binding и receipt

`assets.lock.json` выбран как content/redistribution lock **presentation assets**, а не параллельная таблица component revisions. Required families/version из pinned source перечислены с readiness; все hashes/bytes/licenses обязательны при admission. Closure включает CSS imports/url/fonts, JS loaders/worker и actual targets; unknown dynamic resource construction блокируется. FontAwesome CSS/code/font licenses разделены. No network latest/install, no arbitrary cache publication и no source maps/private payload. Bounds filecount10000/total256MiB/file16MiB и DOC03 JSON caps конечны; это предложенные admission ceilings, не measured corpus size или расширение scientific I/O caps.

SourceGraph до/после, exact recipes/Project/Manifest/input hashes, complete Documenter tree, locked toolchain и reviewed import manifest — обязательные gates. Current root/source tuple сам по себе не является builder/native proof. Existing owning recipes импортируют packages и включают doctest; pilot явно отключает doctest/linkcheck, сохраняя normal defaults и coverage. Unsupported executable @example/@eval/@repl/jldoctest отклоняются до render; doctest=false не подменяет этот scan. @meta/@docs и imports/package-image workloads требуют review; неизвестный transitive edge оставляет dependent render blocked. Нет warm-up через scientific solve или full CI.

Proposed exact owning paths разделены: Core/Runner make profiles, Root orchestrator/plan/assemble/runtime/assets lock/receipt schema/public operator chapter, shared Contracts schema, отдельный Portal/Platform serving. Выход public tree содержит hash-listed HTML/assets/licenses/search/approved JSON/bundle, private attempt tree — original logs/failed outputs/import/toolchain/transform receipts. DOC03 bundle exact fields сохранены, self-hash исключён; внешний manifest SHA в receipt, release.json задним числом не меняется, current pointer не активируется.

Receipt отделяет source/toolchain/import/assets/allowlist/theme/CSP/static checks от browser_offline/browser_light/production_serving/scientific. Null+not_measured не подменяется нулём; result candidate/blocked/failed не делает build exit научным или browser PASS. Parent attempt/source correction сохраняет failed originals. Full native derivation binding не выдумывается из executable version.

## Negatives и оставшиеся gates

Planned matrix охватывает wrong tree/version/shape; missing asset/font/license/hash; CDN/importScripts/blob residue; dark OS/saved themes; inline scripts/events/styles; executable directives/sentinel; private paths/symlinks/source maps; wrong release/missing source; unknown origins; missing anchors/loader targets; unsupported math/source-node mismatch. Healthy controls отличаются по одному фактору. Source/static, render и browser receipts разделены.

Необходимые implementation acceptance details без пересмотра design:

- Каждый removed/rewritten known generated shape должен иметь count/hash/source-mapping control; unexpected raw output не исправляется молча.
- Asset closure scanner проверяет actual produced bytes после всех transforms; manifest hashes до transforms не являются итоговым binding.
- Source-only expected pass не переносится на dark-OS/no-flash/offline fonts/math/search/layout/focus. DOC05 проверяет cold-cache local HTTP origin под **existing** Portal CSP, direct URLs/real anchors, docs404 до catch-all и protected API.
- Raw import/build receipts и private inventories не попадают в public payload; same-origin static publication не даёт arbitrary filesystem serving или новой auth boundary.
- Shared DOC03 schema implementation, complete asset pins, package tree/native toolchain/import audit и fresh BUILD admission остаются prerequisite соответствующих ветвей. Какая-либо missing часть не обходится этим CP-DESIGN PASS.

Design §8 описывает конечный proposed BUILD plan (one candidate + max2 changed reviewed corrections, <=90min aggregate), но этот review **не выдаёт** runtime grant. Нужны фактическое действующее разрешение и свежий admission; повтор неизвестного outcome/auto-rerun не разрешён. Sole final CI остаётся отдельным final-ready-source gate. A harness review также не предоставлял новой квоты.

## Итоговое решение / ограничения

CP-DESIGN принят для version-bound minimal presentation/recipe route и exact ownership/data/receipt/negative boundaries. Новый trust/CSP exception или смена scientific contract не требуются выбранным решением. Branch KaTeX0.16.8 API/assets является конкретным blocked prerequisite, а не невысказанным предположением совместимости. Если exact источник не подтвердит выбранную binding/style closure, эта ветвь возвращается на focused D; implementer не выбирает другую trust/math/CSP policy самостоятельно.

Сборка, target imports, browser/native/server checks не выполнялись; полного installed package-tree hashing не было. Наличие source hashes не доказывает фактическую native toolchain или bit-identical rebuild. Static docs не подтверждает сходимость уравнений, physical checks, discretization, experiment либо full S1. Локальные обновления gitlinks/dirty components и данный дизайн не создают release-ready claim.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Минимальный faithful three-journey route сохраняет Documenter/owning sources | Design §§1–4 + DOC03 publication contract | Support corpus/import effects ещё требуют реализации/проверки | сохранить |
| Fixed-light/offline/CSP recipe определена без новой exception | Pinned HTMLWriter/RD/search/themeswap + design §5 | Adapter/runtime/CSP browser behavior не измерены | дополнительно измерить |
| Math API/assets готовы | Нет matching admitted KaTeX0.16.8 source/API/license/font closure | Hard prerequisite; unrelated/latest не замена | данных недостаточно |
| Source/bundle/receipt и allowlist границы достаточны для owning I | Design §§6–9 exact fields/paths/gates | Missing schema/assets/tree/import/admission блокируют зависимые ветви | сохранить |
| Runtime/publication/scientific acceptance выполнены | Ни render, ни browser/server/solver execution нет | CP-DESIGN не закрывает эти gates | данных недостаточно |

**B STOP.** All findings/implementation conditions собраны выше; новых blocking design findings нет. PASS только design scope, current math/BUILD branches blocked. Sole output B — этот report.
