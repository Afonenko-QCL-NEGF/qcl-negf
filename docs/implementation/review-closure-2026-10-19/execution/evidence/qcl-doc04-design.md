# DOC04 — один pinned light/offline publication pilot

Дата: 2026-10-19. Этап D, source-only contract для independent CP-DESIGN.
Автор — Sol/ultra по brief координатора. Это не render/build/browser acceptance.
Product edits и CP-DESIGN автором не выполняются. No children.

## 1. Scope, source и результат этапа

Один pilot materializes existing Documenter docs с тремя primary slices:

| Reader journey | Primary source / URL после сборки | Проверяемый вопрос |
| --- | --- | --- |
| Исследователь | Core `docs/src/theory/09_scba.md` → `core/theory/09_scba.html#researcher-scba-route` | Почему малый смешанный шаг не доказывает fixed-point solution; переход к final assessment |
| Разработчик | Runner `docs/src/api/public.md`, `user/configuration.md` → `runner/api/public.html#reader-api-routes`, `runner/user/configuration.html#developer-configuration-route` | configuration_source, energy_chunk, assigning и effective origin, boundaries API/schema |
| Оператор | Новый authored public `docs/public/operator-recovery.md` → `operator/recovery.html#operator-recovery` | Сохранить failed attempt и выбрать acknowledged recovery; явный execute boundary и missing-data outcome |

Root source: `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Selected gitlinks:
Core `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`, Runner
`9378396a3681c1eddf2c62f16674834fc4465583`, Contracts
`12fc26462bbab3df76904c6deb01f8c6596de7be`. Остальная композиция — Git tree,
не дополнительный revision lock. Source receipt содержит все gitlinks и status.
Рабочие foreign execution/checkpoint изменения не являются DOC04 inputs.

Accepted DOC03 owning contract: `docs/system/physics-documentation.md`, SHA256
`4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`.
Discovery receipt `/tmp/qcl-doc04-source-discovery.json`, SHA256
`39fa7266234f4082d8bc6d8b75ade5e87351bb7fa9760e3f0317fa30d08a7433`,
перепроверен по primary source, а не принят за implementation verdict.

Envelope этого D: <=45 min, 1 CPU/2 GiB, source reads <=8 MiB,
report+identity <=96 KiB. Не выполнялись target imports/parsers/tests,
Julia/Nix/render/download/network/browser/server/Git mutations или product edits.
Standard-library metadata/hash processing не загружает код target packages.
Scientific S1/criteria/модель и sole-final-CI сохранены. Public release не разрешён.

Выход D — exact owning recipe/data/receipt contract и explicit readiness gaps.
DEV implementation может продолжаться без native inventory; BUILD/OPS ждут
fresh admission. Source verification не является native toolchain proof.

## 2. Проверенные source facts и архитектурный выбор

Pinned manifest выбирает Julia 1.13.0 и Documenter 1.17.0, UUID
`e30172f5-a6a5-5a46-863b-614d45cd2de4`, tree
`56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`.
Прочитан локальный package source
`.build/local-julia-int01/depot-1/packages/Documenter/AXNMp`.
Его Project version и отдельные hashes совпадают с discovery. Полный фактический
Git tree **не проверен**: 431 file entries, около 4.70 MB, один symlink.
Не считать расположение в depot или Project version доказательством tree pin.
Verified full-tree closure остаётся preflight prerequisite, без следования symlink
за пределы package root. Native executable identity здесь не измерялась.

Primary Documenter locators:

- `src/html/HTMLWriter.jl:507–538`: public constructor поддерживает prettyurls,
  assets, mathengine, analytics, warn_outdated, prerender, disable_git,
  size thresholds. **Нет** kwargs `theme`, `themes`, `offline`, `cdn=false`.
- `:845–880`: copies themeswap; при source/assets/documenter.js skips generated
  runtime bundle; иначе включает RD dependencies и все `assets/html/js/*.js`.
  Все THEMES копируются без public theme restriction.
- `:1006–1065`: settings modal содержит Automatic(OS) и все theme choices.
  `:1068–1143`: head всегда включает RD font/KaTeX CSS, CDN RequireJS,
  inline documenterBaseURL, search index, siteinfo/versions и все theme links.
- `assets/html/themeswap.js` читает `documenter-theme` и OS dark preference;
  `assets/html/js/themes.js` меняет localStorage и stylesheet selection.
- `src/html/RD.jl`: pinned CDN versions RequireJS2.3.6, Lato3.0.0,
  JuliaMono0.050, FontAwesome6.4.2, jQuery3.7.0/jQueryUI1.13.2,
  Headroom0.12.0, highlight.js11.8.0 и KaTeX0.16.8.
- `HTMLWriter.jl:91` выбирает MiniSearch6.1.0. `assets/html/js/search.js:68–71`
  importScripts с jsdelivr; `:459–474` creates Blob Worker. Это не offline/self
  closure и не совместимо автоматически с existing Portal CSP.
- `HTMLWriter.jl:2388–2390` выдаёт display math как p.math-container с `\\[…\\]`,
  inline math как span с `$…$`. Это source-preserved math до browser rendering.
- `src/documents.jl` поддерживает source/build/pages/pagesonly/doctest/linkcheck/
  checkdocs/draft. Это позволяет отдельный pilot profile без изменения normal
  release/documentation defaults.

Existing Portal `api.py` CSP: script-src/style-src/connect-src self, object-src
none, base-uri none. Оно не разрешает CDN, inline page script или blob workers;
KaTeX HTML style attributes также требуют проверки/устранения. Глобальная CSP
не ослабляется ради docs.

| Вариант | Disposition |
| --- | --- |
| Existing Documenter + version-bound source/output presentation adapter + local assets | **Выбран.** Сохраняет authoring, @docs/@ref, anchors и search algorithm; adapter имеет проверяемые pinned input shapes |
| Изменять const THEMES/RD или monkeypatch render_head/render_settings в установленном Documenter | Не выбран: package mutation/internal method replacement и скрытая совместимость |
| Новый framework/React Markdown renderer/global search service | Не выбран: не нужен для трёх journeys и выходит за минимальный route |

Adapter output-specific и явно связан с 1.17.0 hashes. Он не выдаётся за public
Documenter API. Unknown generated shape/version вызывает отказ; нельзя молча
«починить regex» или опубликовать неполную closure.

## 3. Exact owning paths и порядок готовности

Все новые paths — proposed, сегодня отсутствуют/не изменены.

| Владелец | Path | Единственная ответственность |
| --- | --- | --- |
| Core | `docs/make.jl` | Выбрать явный pilot profile; existing default build semantics сохраняются |
| Runner | `docs/make.jl` | Тот же profile с root workspace, не standalone Core v0.2.0 |
| Root | `ops/docs.ts` | SourceGraph gate, finite process orchestration, три render steps и assembly; subprocess argv, no shell evaluation |
| Root | `ops/docs/pilot-plan.json` | Versioned slice/output/transform policy; component pins извлекаются из Git, не дублируются вручную |
| Root | `ops/docs/assemble.py` | Pure bounded HTML/asset transform, closure/allowlist validation, immutable final staging |
| Root | `ops/docs/math-render.mjs` | Build-only static math bridge; exact KaTeX asset/API prerequisites ниже |
| Root | `ops/docs/runtime/` | MIT-derived local Documenter snippets, fixed-light CSS, static worker and no-theme bootstrap; no physical semantics |
| Root | `ops/docs/assets.lock.json` | Exact external presentation asset content pins/redistribution licenses; не component revision registry |
| Root | `ops/docs/schemas/docs-build-receipt.schema.json` | Root build-recipe receipt; не scientific acceptance schema |
| Root | `docs/public/operator-recovery.md` | Authored sanitized public recovery chapter; no private deployment inventory |
| Root | `docs/public/make.jl` | Documenter operator section, modules=[], root locked Julia project |
| Contracts (DOC03 dependency) | `src/qcl_negf_contracts/schemas/model-help.schema.json` | Shared DOC03 bundle/fragment/view format, не независимая копия в root |
| Portal/Platform (DOC05/07) | Existing api.py/module settings | Serve admitted immutable bundle under /docs before catch-all; здесь serving code не пишется |

Отдельный author каждого owning recipe; owning commits/PRs перед root gitlinks.
DOC04 не требует реализовать весь DOC07 run-help endpoint/snapshot. Catalog может
иметь fragments=[] с явной coverage=[] до готовых authored fragments; нельзя
создавать dummy known origin. DOC03 bundle schema PublicRef должен существовать
в выбранном published Contracts до выдачи final bundle.json. Missing shared
schema блокирует только финальную serialization claim; raw HTML pilot не
называется DOC03-conformant bundle без неё.

Root operator chapter содержит сам public recovery route из Runner
`docs/src/user/results.md#operator-recovery-route`: preserve raw/attempt,
current→previous verified selection, new attempt boundary, complete prior closure,
no valid generation outcome и recovery != science. Не копировать private hosts,
usernames, mounted paths, credentials, live measurements, исторические receipts
из большого deployment runbook. CLI grammar сохраняется по owning Runner,
synthetic placeholders PLAN/OUTPUT/ID/N/DIRECTORY явно не выполняются при build.
Chapter связывает canonical Runner/Core/Contracts refs, не копирует формулы,
thresholds или native recovery success claim.

## 4. Recipe phases, public APIs и import-effects gate

### 4.1 Source preparation без target execution

1. `sourceGraph()` из existing ops/git.ts требует clean published root, совпадение
   checked-out component revisions/gitlinks, отсутствие nested submodules.
   Повторный graph после render/assembly должен совпасть. Final build root будет
   новым reviewed composition с recipes; cfc38e1 — baseline дизайна, не будущий
   кандидат с несуществующими recipe files.
2. Verify Project/Manifest hashes, complete Documenter tree, input files,
   assets.lock and licenses. Immutable vendor inputs подаются с named admitted
   cache; source-only phase не делает fetch/install/Pkg.instantiate.
3. Copy exact authored sources и allowlisted docs assets в isolated named staging.
   Symlinks/paths/private payload не проходят public allowlist. No archive script
   execution, no user macros/plugins. Generated sources никогда не canonical.
4. Оба existing docs page graphs сохраняются для @ref/@docs closure. Три slices —
   primary reader acceptance, а не обещание audit всех chapters. Сборка существующих
   Core/Runner страниц обеспечивает cross-reference closure; никакого partial
   @ref rewrite на current GitHub вместо отсутствующей local page. Support pages
   и assets перечислены в receipt по точным paths/hash, не скрыты как «одна глава».

Сохраняем normal `checkdocs=:exports`, warnonly=false и публичные IDs, потому что
в pilot используются existing complete page graphs. Нет ослабления coverage
ради отсутствующих @ref. Operator-only modules=[] имеет checkdocs=:none по
отсутствию package exports; это не scientific acceptance decision.

### 4.2 Import audit, prerequisite до первого render

Source inspection обнаружила:

- Core/Runner recipes импортируют owning packages/Documenter и включают doctest.
  Standalone Runner docs Project source выбирает Core v0.2.0; pilot всегда
  QCL_NEGF_PROJECT=<selected-root>/julia, без standalone instantiate.
- Core module включает `src/composition/precompile_workload.jl`. Workload строит
  tutorial problem без scattering, Hamiltonian/retarded Green/spectral function;
  не вызывает SCBA/Poisson transport solve. Он относится к package-image
  compilation, не обычному import по source contract. Source не доказывает,
  что конкретная будущая среда имеет готовый package cache.
- В Runner есть одноимённый source workload file, но selected
  src/QCLNEGFRunner.jl его не включает. Наличие файла не принимается за import edge.
- Runner `__init__` назначает DEFAULT_CONFIGURATION_SCHEMA через package resource
  path. Transitive imports HDF5/FFTW/Unitful/PrecompileTools/Documenter имеют свой
  эффект/compilation closure; полный transitive import audit не закрыт этим scan.
- Source-only text scan owning docs/src не нашёл executable fenced @example,
  @repl, @eval, @setup, jldoctest. Это наблюдение о прочитанных Markdown sources,
  не доказательство отсутствия executable behavior во всех docstrings/dependencies.
  @meta CurrentModule и @docs symbol resolution сами требуют evaluation/import.

До BUILD I создаёт import manifest `{package, revision/tree, entrypoints,
includes, init_effects, package_image_workload, docs_directives, status, evidence}`.
Каждый compiled/include/@meta/@docs edge либо reviewed allowlisted effect, либо
unknown. Unknown effect останавливает соответствующий render; prepared environment
и missing pins добываются отдельно, не замещаются install latest. Ни наличие
Project hash, ни успешный isolated import не устанавливает scientific validity.

### 4.3 Exact pilot profile

Owning docs/make.jl получают explicit mode `QCL_DOCS_PROFILE=pilot-v1` и target
paths из root orchestrator; generic/default mode не меняется. При неизвестном
profile — error. В pilot Documenter.makedocs использует:

```text
root/source/build = explicit isolated authored staging paths
modules = existing owning module (operator: [])
pages = existing owning page graph (operator: index.md + recovery.md)
remotes = nothing
doctest = false
linkcheck = false
checkdocs = :exports (operator :none)
warnonly = false
draft = false
format = Documenter.HTML(
  prettyurls=false, edit_link=nothing, disable_git=true,
  analytics="", warn_outdated=false, prerender=false,
  mathengine=nothing, assets=["assets/qcl-fixed-light.css"],
  repolink=<selected owning public repository URL>)
```

Эти Documenter kwargs проверены по pinned source. Не используются неподдерживаемые
theme/offline kwargs. Mathengine=nothing выбран потому, что math материализуется
build-only ниже; в final browser runtime нет client math evaluator/CDN. RD.katex_css
в raw head всё равно появится и обязателен к обработке, а не считается устранённым
одним keyword. Никакого deploydocs; version pointer и production serving не
меняются. Отключённые doctests — scope pilot render, не изменение normal owning
test contract или численных критериев. `@example/@eval/@repl` не запрещаются одним
doctest=false: source gate отклоняет их до импорта/render.

Future command chain (не исполнялась): root `ops/docs.ts prepare`, три isolated
Julia process с --startup-file=no, --history-file=no, --project=selected/julia,
then build-only math bridge, pure assemble/verify. Source preparation/root Deno
и Python uses existing locked toolchain. Actual executable paths/version/CLI
support и Julia import/cache policy проверяются по fresh BUILD toolchain receipt;
не выдумываются из $PATH. Environment allowlist: JULIA_PROJECT/LOAD_PATH,
JULIA_DEPOT_PATH (admitted prepared immutable dependency depot + named writable
cache), JULIA_PKG_OFFLINE=true, JULIA_PKG_PRECOMPILE_AUTO=0,
OPENBLAS_NUM_THREADS=1 и admitted Julia/precompile concurrency.
No Pkg.instantiate/precompile/bootstrap скрыто внутри docs command. Если imports
требуют недопустимого package-image build, render остаётся blocked до отдельной
prepared-environment stage; scientific solve не подставляется для warming cache.

## 5. Fixed-light/CSP-safe materialization

### 5.1 HTML policy adapter

Pure `assemble.py` использует locked Python stdlib html.parser в будущей I/BUILD;
никаких target parser imports в этом D. Это version-specific Documenter-output
adapter, не новый scientific/documentation renderer. Guard input hashes/shape
и count per page; unknown shape → fail closed. Оригинальные article text,
headings, id/name anchors, equation text и source links сохраняются. Transform log
связывает each raw page hash → each public page hash и перечисляет операции:

1. Оставить только documenter-light stylesheet. Удалить other themes и их assets,
   data-theme-primary-dark, theme-- classes, .docs-dark-only logo; выбрать
   .docs-light-only. Нет альтернативной theme picker даже скрытой CSS.
2. Удалить #documenter-settings modal и #documenter-settings-button, themeswap
   script и themes.js runtime. Старый localStorage key не читается/не пишется;
   OS preference не вызывает branch. Fixed-light external CSS содержит
   `:root { color-scheme: light; }`, явные светлые surfaces/контраст для generated
   states. Настройки других страниц/пользователя не перезаписываются.
3. Удалить live version selector/versions.js/siteinfo.js/warner references;
   pilot version — immutable URL/source graph, без latest pointer. Никакой
   runtime fetch проверки другого version URL. Датированный buildinfo из modal
   не попадает в public payload; actual timestamps остаются в build receipt.
4. Externalize единственный inline documenterBaseURL assignment в generated
   per-page local script `assets/pages/<page-content-id>.js`; semantic value
   такой же relative base URL. Other unknown inline script/event-handler → fail,
   не добавлять unsafe-inline/unsafe-eval/hash exceptions в CSP.
5. Replace known RD URL-bearing resource nodes with exact local asset URIs.
   Replace RequireJS data-main/runtime references с локальным no-theme runtime.
   External scholarly/source `<a href>` сохраняются как ссылки; они не runtime
   assets и не fetch при чтении страницы.
6. Static math renderer выдаёт presentation nodes; все inline style attributes
   преобразуются в deterministic classes с declarations во внешнем
   `assets/styles/math-generated.css`. Unknown executable/unsafe style URL,
   event handlers/embedded scripts → error. Никакой новой формулы/threshold.
7. Remaining inline styles generated by snippets/search presentation also move
   to local classes (например font-size в result snippets). Runtime CSSOM UI
   behavior остаётся subject DOC05 CSP receipt; исходная CSP не ослабляется.

При документированном supported asset override source/assets/documenter.js
Documenter пропускает bundle generation. Profile подаёт derived local no-theme
runtime. Состав — только MIT snippets из exact pinned Documenter, кроме
themes/settings/version/warner, плюс reviewed static-search bridge. Libraries
paths/shims извлечены из pinned RD/JSDependencies и содержат только local assets.
Публичные Documenter package sources в depot не меняются, const/methods не patch.

### 5.2 Search без CDN/blob worker

Search сохраняет MiniSearch6.1.0 и pinned search scoring/filter/result logic.
Это per-section Documenter search, не DOC03 cross-corpus search adapter.

- `assets/runtime/search-worker.js` — version-bound worker_function из pinned
  source; importScripts только relative local `../vendor/minisearch/6.1.0/index.min.js`.
- Main thread создаёт `new Worker(<same-origin static URL>)`, не Blob/objectURL.
  Init message `{type:'init',docs,baseURL,filters}`, worker reply `{type:'ready'}`;
  затем original query/result messages. Main ждёт ready перед первой query;
  original result categories/limit сохраняются. Worker не принимает URL из query.
- Search index — Documenter-generated search_index.js, local и exact hash в files.
  Validation: expected assignment/schema, locations только existing local pages/
  anchors того же section/version; unknown index format не загружается best-effort.
- Нельзя оставлять unused themes.js/remote import string в исполняемом closure.
  Allowed search bridge touches transport/init, не scientific content/ranking.

Same-origin worker соответствует script-src self fallback без нового blob:
разрешения. Browser CSP/runtime compatibility остаётся отдельным DOC05 gate.

### 5.3 Math: выбранный build-only путь и точный unresolved prerequisite

Сохраняем Documenter raw TeX и его model/equation IDs. Build-only bridge получает
`[{page,selector,tex_sha256,tex,display}]` из exact generated math nodes и
возвращает `[{selector,tex_sha256,html,css_declarations}]`. Params: trust=false,
strict errors, no user macros/plugins/extensions, unsupported TeX → failure,
не текст-заглушка и не исправление формулы. Native text и TeX input fingerprint
сохраняются в private transform receipt; source source-of-truth не меняется.
Final page содержит static math и local font/CSS closure, не Julia/client
math-engine execution. Inline-math capture не ищет dollar delimiters по всему
произвольному тексту: только Documenter math node shapes и checked source mapping.

Выбран external asset family **KaTeX0.16.8**, поскольку именно её задаёт pinned RD.
Bridge expected binding — same local pinned distribution's renderToString export;
Node24 берётся из existing root/platform toolchain. Это **ещё не verified API
binding**: локально найден лишь unrelated vendored KaTeX другой версии, 0.16.8
source/distribution/hash/license closure не предоставлены. Он не переиспользуется.
Exact bridge API/options и style/font closure должны быть сверены с source
именно 0.16.8 **до** implementation этой ветви/BUILD. До этого math bridge input
status=missing_pin; render/closure pass не разрешён. Не вызываем неподтверждённый
API и не скачиваем latest/другую версию ради закрытия пробела.

Это локализованный factual blocker math/asset readiness. Остальные DEV recipes,
schema/sanitized chapter/source fixtures проектируются и реализуются независимо.
Если exact supplied distribution не поддержит этот binding, автор возвращается
к focused design; medium implementer не выбирает новую math/CSP/trust policy.
Документ намеренно не утверждает, что supported 1.17.0 Documenter kwargs решают
отсутствующую math distribution. Не появляется новый live renderer или trust root.

## 6. Asset input contract, pins, licensing и public allowlist

`assets.lock.json` — формат `qcl-negf.docs-assets.v1`, all objects
additionalProperties=false. Exact fields:

```text
{format, generator_tree_sha1, entries[]}
entry = {id, family, version, source_uri, distribution_sha256,
         files[{source_path, destination, bytes, sha256, media_type}],
         license:{spdx, text_file, text_sha256, copyright}, dependencies[]}
```

All hashes/bytes обязательны для admitted lock; null/TODO/zero hash — invalid.
Source_uri — provenance HTTPS URL, не runtime network request. Content comes
from named immutable prepared input directory checked against lock. License
text included в `assets/licenses/<id>.txt` и indexed in public NOTICE. Прямые
и transitively referenced CSS/fonts/images/scripts перечисляются индивидуально;
нет `fetch any url()` или glob vendor-cache publication. Hash pins assets не
заменяют Git gitlinks, Julia manifest или native toolchain receipt.

Required families / selected versions (не готовый asset lock):

| Family | Версия / origin | Readiness и source obligation |
| --- | --- | --- |
| Documenter light CSS/snippets | Documenter1.17.0 tree56e9… | Individual source hashes доступны; полный tree verification pending; MIT license текст прочитан |
| RequireJS | 2.3.6 из RD | distribution/hash/license не provided; prerequisite |
| jQuery / jQueryUI | 3.7.0 / 1.13.2 | Exact distribution/shim/closure/license prerequisite |
| Headroom + jQuery adapter | 0.12.0 | Exact two scripts/license prerequisite |
| highlight.js + Julia/julia-repl and used extra languages | 11.8.0 | Used-language list от actual generated pages; base/language hashes/licenses prerequisite; no prerender auto-download |
| MiniSearch | 6.1.0 из HTMLWriter | UMD file/hash/license prerequisite |
| KaTeX + fonts/CSS/build-only module | 0.16.8 | Source/API/assets/license closure missing; hard math prerequisite §5.3 |
| Lato / JuliaMono | 3.0.0 / 0.050 из RD | Local CSS + **все** referenced font files/license conditions; отсутствуют admitted pins |
| FontAwesome CSS/solid/brands/fonts | 6.4.2 | Разделить licenses по CSS/code/font assets, сохранить notices; не предполагать один MIT на всё |

Lodash объявлен в RD, но не входит initial RequireJS libraries. Он не включается
автоматически «потому что упомянут»; если actual selected runtime edge требует
его, lock должен явно включить 4.17.21 distribution/license. Unused dependencies
не публикуются. Чужой KaTeX из LazilyInitializedFields не считается matching pin.

Public bundle files — DOC03 allowlist: reviewed HTML/CSS/JS, fonts, images,
search index, approved bounded JSON, optional inventory, license texts/NOTICE.
Extensions включают нужные local `.woff/.woff2/.ttf/.txt`; MIME whitelist exact.
No symlinks, .git/.aws/dotfile paths, depots, logs/raw build receipts, HDF5/arrays,
source maps/private source paths, tokens/credentials/private inventory. Raw
Documenter `.documenter-siteinfo.json` retained privately, не public payload.
SVG trusted public authored assets проверяются на external references/scripts;
unknown SVG не очищается молча, а блокирует этот asset до review.

Closure scanner walks only admitted payload tree, file count<=10000,
total logical bytes<=256 MiB/pilot, one file<=16 MiB, bounded JSON согласно DOC03
(manifest<=2 MiB, fragments<=32 KiB, help view<=64 KiB). Превышение — replan,
не silent truncation. Проверяются HTML src/href resource attributes, CSS url/
imports, JS loader/worker resource URLs и all search/DocRef targets; external
article/source anchor links классифицируются отдельно, не скачиваются.
Unknown dynamic loader/URL construction вне approved runtime bridge → stop.

## 7. Exact consumed/produced data и build receipt

### 7.1 Plan и artifacts

`pilot-plan.json` fields:
`{format:'qcl-negf.docs-pilot-plan.v1', profile:'pilot-v1', slices,
support_policy:'existing_owning_page_graphs', source_inputs, assets_lock,
transform_policy:'documenter-1.17-light-self-v1', public_prefix:'/docs',
limits, expected_primary_anchors}`.
Source_inputs — versioned repo-relative paths, не component commit list.
Slices=`[{id,owner,primary_sources,section,primary_urls}]`; limits — caps §6
и builder-supplied attempt envelope. Expected_primary_anchors включают
researcher-scba-route, researcher-final-route, reader-api-routes,
developer-configuration-route, operator-recovery-route, operator-recovery.
Никаких private site paths в plan.

Consumed: existing sourceGraph, selected Project/Manifest, owning recipes/sources,
DOC03 schema, assets lock+immutable bytes/licenses, reviewed import manifest,
fresh BUILD admission and toolchain receipt. Не потребляются scientific results,
production DB/profile, private inventories или full-result hashes для чтения help.

Produced private attempt tree:
`raw/core`, `raw/runner`, `raw/operator`, original stdout/stderr, import/toolchain/
transform/closure receipts и failed outputs. Produced public candidate tree:

```text
<source_revision>/index.html
<source_revision>/core/**
<source_revision>/runner/**
<source_revision>/operator/{index.html,recovery.html}
<source_revision>/assets/{runtime,vendor,styles,fonts,pages,licenses}/**
<source_revision>/NOTICE.txt
<source_revision>/help/fragments/<id>.json   (только available DOC03 fragments)
<source_revision>/bundle.json
```

Hub — source-only root collector с тремя task links и existing per-section
search. No unified search adapter/service. `bundle.json` имеет exact DOC03 fields
format/sources/schema/generator/fragments/files/aliases; generator fields включают
Documenter1.17.0 UUID/tree/Julia1.13.0, Project/Manifest hashes, recipe PublicRefs,
toolchain_lock PublicRef. Output hashes compute after **all** transforms; bundle
does not self-hash. Bundle identity — external SHA256 exact manifest bytes.
App release.json не дописывается задним числом; publication receipt связывает
app release/source graph/bundle SHA. Version pointer не изменяется в DOC04.

### 7.2 Root build receipt schema

Один `qcl-negf.docs-build-receipt.v1` с all objects additionalProperties=false:

| Поле | Exact содержание / producer |
| --- | --- |
| `format`, `attempt_id` | const format, уникальная immutable bounded build attempt identity; не AiiDA UUID |
| `sources` | existing generated sourceGraph, exact equality before/after |
| `plan_sha256`, `assets_lock_sha256`, `schema_sha256` | Input bytes hashes; missing не подменяется 0 |
| `inputs` | `[{owner,revision,path,sha256,bytes}]` source inputs/recipes/import manifest и licenses |
| `toolchain` | `{expected:{julia_version,documenter_version,documenter_tree_sha1,manifest_sha256}, observed:{julia_version,julia_executable_sha256,documenter_tree_sha1,deno_version,deno_executable_sha256,python_version,python_executable_sha256,node_version,node_executable_sha256}, status}`; status verified/unknown/mismatch; native derivation/NAR binding отдельным optional receipt_ref, не выдумывается |
| `admission` | `{receipt_sha256,limits:{cpu,ram_bytes,wall_seconds,output_bytes,log_bytes},status}`; hash trusted private admission, raw inventory не публикуется; unknown blocks BUILD |
| `imports` | `{manifest_sha256,status,unknown_edges}`; status reviewed/unknown; unknown prevents corresponding process |
| `assets` | `[{id,version,distribution_sha256,license_sha256,status}]`; verified/missing/mismatch; final pass требует all verified |
| `steps` | `[{name,argv,environment,started_at,finished_at,exit_code,status,stdout,stderr}]`; normalized public-relative argv/env allowlist; stdout/stderr={bytes,sha256,retained_ref,cap_exceeded}; raw paths/logs private |
| `measurements` | `{wall_seconds,cpu_seconds,max_rss_bytes,read_bytes,write_bytes,peak_output_bytes,status}`; absent=null + not_measured, не zero |
| `transforms` | `[{input_path,input_sha256,output_path,output_sha256,policy,operations}]`; includes math TeX/source preservation and exact removed resource classes |
| `checks` | `{source_binding,toolchain,import_policy,assets_licenses,allowlist,resource_closure,anchors,theme_static,csp_static,browser_offline,browser_light,production_serving,scientific}` с per-check status pass/fail/not_measured/not_applicable + evidence refs |
| `result` | `{status,bundle_manifest_sha256,bundle_bytes,files,reason}`; status candidate/failed/blocked; missing outputs null; build exit не повышает browser/native/science status |
| `parent_attempt` | null или prior immutable failed attempt ID; correction changes source/recipe identity, originals retained |

Raw receipt не входит public DOC03 bundle. Sanitized source/build summary может
ссылаться на recipe/source/toolchain/asset hashes, исключая hostnames, machine
paths, secret env и native inventory. Build-specific timestamps остаются receipt,
не обязаны входить public content. Header/chapter text/anchors не меняются ради
побайтовой воспроизводимости. Этот D задаёт воспроизводимый recipe/input contract,
а не утверждает уже измеренную bit-identical rebuild reproducibility.

## 8. Конечный future BUILD envelope и gates

DOC04 handoff: один build candidate и максимум две corrected attempts, только
при changed reviewed source/recipe, до30 min каждая; не automatic rerun того же
неизвестного outcome. Общий wall<=90 min для этого блока, stdout+stderr<=8 MiB
на attempt. CPU/RAM/disk и concurrency из fresh BUILD admission. Общий grant
не умножается на agents/processes. При cap exit сохранить original failed logs/
receipts и outputs; не обрезать log с последующим pass. Supervisor прекращает
процесс при достижении log/resource cap, записывает cap_exceeded и доступные bytes.

Не запускать full `deno task test`, CI или native solver build как обёртку docs
pilot. Sole final CI остаётся отдельно на final ready source. Нельзя собирать
параллельные attempts «на всякий случай». BUILD admission сейчас отсутствует:
никакой render/native launch из этого D. OPS serving/version activation требует
своего BIND и production receipts; preview/source pass его не наследует.

## 9. Source-only fixtures и future browser acceptance

В этом D fixtures **описаны, но не исполнялись**. I проверяет pure adapters на
synthetic retained source/output shapes без target imports, затем отдельный
BUILD render и DOC05 browser. Healthy control должен отличаться одним фактором.

| Negative | Expected source/static outcome / healthy control |
| --- | --- |
| Wrong generator tree/version/shape | Fail before render/transform; exact verified package source/known generated head принимается. Не сравнивать только Project.version |
| Missing asset/hash/license/font | Missing_pin blocks that closure; matching complete distribution+licenses accepted. Не использовать соседний vendor version |
| CDN/importScripts/blob Worker остаток | Closure/CSP-static fail; same-origin static worker с local MiniSearch control проходит source checks |
| Dark OS/localStorage/theme alternatives | Fixture с themeswap/picker/dark stylesheet/media branch отклоняется; fixed-light no-theme output принимается static check, browser pass не выводится |
| Inline script/event/style residue | Fail CSP-static; known page config externalized, static math/styles separated accepted; никакого unsafe-inline bypass |
| Executable @example/@eval/jldoctest or sentinel target module | Source gate fails до imports; ordinary fenced Julia text и allowlisted @meta/@docs принимаются. Sentinel не импортируется для доказательства |
| Private path/credential/symlink/source map | Allowlist reject, originals retained private; public repo-relative asset/source refs accepted |
| Wrong release / missing primary source | Graph/hash mismatch или absent source rejects required slice; same immutable graph/source accepted; current defaults не fallback |
| Unknown numeric origin | DOC03 fragment remains reference-only/actual unknown; cannot become DOI/0/used pass. Empty catalog explicitly empty, не fake known help |
| Anchor or loader target missing | Exact URL/anchor/worker/font target failure; known target maps to real payload. Не переписывать missing docs URL в Portal index |
| Unsupported math macro/incorrect math-node map | Math gate fails; не менять формулу или подавлять error. Positive supported source TeX roundtrip сохраняет tex_sha256/IDs |

DOC05: три journeys × online/offline (external network blocked, cold cache) ×
light/dark OS при всегда светлом результате. Отдельные retained preferences
documenter-dark/catppuccin/invalid value, reload, initial load/no flash. Проверить
math/font layout, search results/keyboard/worker under **existing Portal CSP**,
mobile/keyboard/focus/contrast/dialog/loading/error, direct URLs/anchors,
asset misses/docs404 до catch-all и preserved authenticated /api/v1 routes.
Source-only fixture pass, build exit, CLI help/version output и preview не являются
browser/production serving pass. Offline означает local HTTP origin без внешней
сети; file:// не обещается. Никакой live Julia при просмотре.

## 10. Readiness / явные ограничения

| Зависимость | Сейчас | Что разблокирует |
| --- | --- | --- |
| Accepted DOC03/DOC02/source composition | Bound к cfc38e1 и exact hashes | DEV recipe/content design и будущий scoped implementation |
| Complete installed Documenter tree identity | Не измерена; individual source verified | Cheap exact Git-tree/package verification в подготовленной среде; не install latest |
| KaTeX0.16.8 source/API/assets | Отсутствуют admitted bytes/pins; unrelated vendor не подходит | Exact immutable source/distribution/license receipt, затем focused API binding verification; блокирует math bridge/BUILD acceptance |
| Остальная local vendor closure/licenses | Versions известны из source; hashes/bytes не supplied | Complete reviewed asset lock/input delivery; no current download |
| Full transitive import/compiled cache effects | Не закрыты | Reviewed import manifest/prepared environment; unknown edge blocks only dependent render |
| DOC03 Contracts schema | Дизайн принят; future published resource нужен для final bundle | Owning Contracts implementation/PR/gitlink; не duplicate schema |
| Fresh builder inventory/admission | Недоступны | Native BUILD resource/toolchain BIND; source/DEV работа продолжается |
| Production serving | Не выполнялось | DOC05/OPS bound serving candidate; version pointer отдельно |

Missing math API/source — конкретный factual gap, не согласование нового scope.
Medium I не получает права на download/install/new CSP policy от этого текста.
Новые научные/UI/доверительные решения не подменяют недостающие bytes. Если
необходим новый renderer/framework/trust exception, нужен focused D/operator
route по действующей policy; сейчас они не выбраны.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing Documenter остаётся generator и предоставляет нужные public recipe kwargs | Pinned HTMLWriter/documents source и selected owning recipes | Full actual package tree/native binary ещё не verified | сохранить |
| Fixed-light/offline нельзя получить одним HTML keyword/CSS override | THEMES/settings/themeswap/RD/search source | Presentation adapters и assets ещё не реализованы/проверены | изменить |
| Три slices имеют canonical source и complete support-page policy | §1/3/4, DOC02 headings/refs | Full corpus coverage/native recovery не доказываются | сохранить |
| Strict-CSP math closure готова | Выбран build-only contract §5.3 | Exact KaTeX0.16.8 API/assets отсутствуют; branch не ready | данных недостаточно |
| Recipe/receipt/negative/browser boundaries определены | §6–9 exact fields/caps/controls | Fixtures/render/browser/native/science не выполнялись | дополнительно измерить |

**STOP: source design frozen для independent review; implementation не начиналась.**
