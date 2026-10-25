# DOC04 KaTeX0.16.8: independent high CP-DESIGN review

2026-10-19. **PASS — precise source/API binding addendum.** Новых blocking design findings не найдено. Exact code/API input gap закрыт по прочитанному source; **font license admission/full public asset closure, native BUILD/import/render и browser/CSP/layout остаются blocked/unmeasured gates**. Никакой runtime/native/publication PASS этим review не выдан.

No network/download, Node/module import, parser, render/test/Julia/build, server/Git mutations/children. Optional font metadata проверена bounded raw UTF-16BE string scan одного TTF, без font parser. Sole output — этот report. Ранее accepted DOC04 D/R не изменены.

## Primary evidence и порядок

Сначала прочитаны actual verified distribution package exports, renderToString/default export, Settings/buildTree/domTree/namespace/macro/resource handlers, CSS references, LICENSE и font raw metadata; затем авторский addendum и candidate inventory. Receipt source delivery принят как предоставленная первичная цепочка загрузки, его hash и selected source hashes проверены. Повторной сетевой SHA512-delivery процедуры reviewer не запускал.

| Artifact / primary file | SHA256 |
| --- | --- |
| `/tmp/qcl-doc04-katex-binding-design.md` | `c65c38f74b5fd8168c9ed5ee2fc79649e2d7bafa5655a9248aee4aa81dca25a2` |
| `/tmp/qcl-doc04-katex-binding-identity.json` | `fad374dfd6cf69772cc1bdf7e6816e6d409f18faba361def15e0bb1618af9e9e` |
| Exact npm source delivery receipt | `4493f9d81a9b9ab0c09d5cd82e4849748f673d1af620d7389e2328ea7e36baa4` |
| `katex-0.16.8.tgz` | `7547e6a4088c2bbf0edb82510aa88822396fb39bf14b4e35ed491182b0e89c73` |
| `package/package.json` | `df6fe85c3ecfe46ea791087f689f1206fcfb5e3db265f4a0a9ef20f79cfd19d2` |
| `package/dist/katex.mjs` | `cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88` |
| `package/src/Settings.js` | `2d574dc1e5f245d114871e788b8843d7527a5cc84c2529bbdf3385afe00f781c` |
| `package/dist/katex.min.css` | `df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e` |
| `package/LICENSE` (software MIT) | `766ccc1f306c885aa45542a9846bbd0a505b27a0374f146778171c2254ce18e3` |
| `/tmp/qcl-doc04-ofl-source-receipt.json` | `e8903e46e2528b042567648491606da1f33f9d21d049b7027e81849555c77ddc` |

Source root `/tmp/qcl-doc04-katex-0.16.8/source/package`. Parent DOC04 D SHA `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b`, accepted review `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164` остаются первичными boundary contracts. Root cfc38e1/local component drift не превращается в новый clean release binding.

## Принятые точные решения

### API и effects

`package.json` exports["."].import указывает на `dist/katex.mjs`; file заканчивается `export { katex as default }`. Object version0.16.8 содержит renderToString. Named ESM export renderToString отсутствует. Выбранный `import katex from <exact local file>; katex.renderToString(tex, options)` соответствует source (`dist/katex.mjs:18245–18248,18308+`), не inferred latest API.

Путь renderToString → renderToDomTree → toMarkup выбирает static string production; DOM-writing render/toNode — другой путь. Direct prebuilt ESM не имеет top-level import edges/CLI Commander requirement. Source содержит DOM helpers и guarded `typeof document` check; их наличие не означает, что выбран render-to-string требует браузер, и не даёт право назвать actual Node import already passed. Internal __parse/__renderToDomTree/__defineMacro, CLI/contrib/auto-render/plugin APIs не используются. Package manager scripts/build/install не нужны и этим addendum не разрешены.

### Options и finite scope

Exact supported settings сохранены: displayMode — mapped boolean; output="htmlAndMathml"; throwOnError=true; strict="error"; trust=false; fresh mutable macros={}; maxExpand1000; maxSize=default Infinity; globalGroup=false. Settings types/enums и buildTree branches подтверждены. Namespace действительно обращается к current.hasOwnProperty и может писать scoped values, поэтому freezing/null-prototype macro object не является безопасной «оптимизацией». Fresh object на expression исключает намеренное shared-state use; actual absence cross-expression effects ещё проверяется implementation tests.

Addendum корректно не обещает, что strict всегда throws: reportNonstrict и useStrictBehavior имеют разные source semantics. throwOnError=true исключает ParseError красный fallback как успешную формулу. maxSize конечное значение **clamps** геометрию вместо reject; сохранение default Infinity не выдаётся за resource bound. Explicit sizing/unknown layout остаются unsupported до focused review, CSS nonfinite guard и DOC05 layout. Нельзя менять lengths/формулу ради fit.

Finite input/output contract конкретен:16KiB/expression,4MiB batch JSON,≤10000 records, maxExpand1000,≤256KiB markup/expression/32MiB aggregate, CSS≤1MiB/20000 groups, external process supervisor≤60s в остатке DOC04 attempt. Однопоточный synchronous render не прерывается same-event-loop setTimeout; failed batch должен быть остановлен внешним supervisor, raw/source preserved. Это proposed implementation behavior, не доказательство фактической native RAM/time stop. Supervisor/cleanup обязаны оставаться внутри fresh admitted total envelope; rerun/новый grant не выводится из этих caps.

### Public authored TeX и macro/resource boundary

V1 input — reviewed owning-source mapping с exact selector/TeX hash/IDs, не arbitrary user TeX/options/HTML ingress. Control-token/comment/escape lexer — source gate; macro maps/functions, inline definitions, namespace mutation, file/resource/HTML/diagnostic commands и unknown dynamic constructs запрещаются до KaTeX parser. Standard pinned built-ins не переименовываются в пользовательскую injection. Не требуется global dollar regex или преобразование исходной формулы.

Это существенно: def.js/macros.js действительно поддерживают inline определения, которые не выключаются пустым macros/globalGroup=false/strict. href/url/includegraphics handlers при trust=false возвращают formatUnsupportedCmd; это может дать colored text без exception. Явный source deny + post-output shape/resource guard не позволяет объявить такой результат принятой формулой. trust callback/strict-off ради green не допускаются.

Лексический gate не следует продавать как general-purpose security proof для враждебного TeX. Scope остаётся доверенный публичный authored corpus с fail-closed unsupported source/output. Неоднозначный alias/expansion/sizing или новая extension возвращаются на focused review, а не молча допускаются. Это соответствует принятому DOC04 trust boundary.

### Static markup / CSS и unchanged CSP

Primary domTree.toMarkup выводит inline style attributes, включая SymbolNode italic correction; MathML annotation и static SVG — часть output. Raw renderToString поэтому ещё не CSP-clean. Addendum сохраняет semantic MathML/aria/SVG attributes, но отвергает resource nodes, on* handlers и unsafe URLs/unknown shapes; namespace URIs и TeX annotation не ошибочно считаются network fetch.

Style extraction сохраняет exact ordered declarations/duplicate-property order/numeric values/units, content-addressed class identity, затем удаляет все style attrs. Grammar/finite-value/resource guards обязательны. Выбранный sufficient cascade contract ясен: generated declarations !important разрешены только при доказанном отсутствии competing applicable !important rule для element/property и отсутствии inline !important/unknown context. В этом закрытом stylesheet set они сохраняют приоритет исходного inline-normal над normal stylesheet. При конфликте нужен unsupported_style_context, а не попытка угадать cascade.

Этот контракт не доказывает эквивалентность ещё не написанного rewriter, selectors/media/namespace handling или actual computed style. Tests должны проверять именно admitted stylesheet set и representative inline/display/fraction/sub/sup/stretch SVG/Unicode/MathML cases, включая конфликтный negative. Source→node mismatch и residual style/script/CDN/blob — fail. Нельзя ограничиться удалением атрибута или weak class rule. Static local generated CSS после KaTeX CSS, no browser KaTeX JS и отсутствие unsafe-inline/unsafe-eval exception сохраняют исходную CSP policy. Fixed-light/offline/no-flash/layout/accessibility остаются DOC05 observations.

## Exact CSS/font inventory и license boundary

Непосредственно проверены60 url(fonts/…) occurrences и60 unique local refs в exact katex.min.css; в dist/fonts60 regular asset files, суммарно1,076,572 bytes. CSS не содержит @import или remote/data/blob URL. Candidate identity перечисляет source/destination/bytes/SHA/MIME/license состояния всех60 refs. Public destination сохраняет относительное CSS→fonts layout и byte-exact original names/types (20families×woff2/woff/ttf), без subset/re-encode/rebuild. Software ESM/private source не обязан публиковаться; unused browser KaTeX JS/contrib/build tools/maps исключены.

Связка receipt официального exact distribution, hash code/CSS и candidate per-file inventory достаточна для source-design binding; это **не admitted assets.lock** и не claim отдельного выполненного full asset-admission validator. Финальная I/BUILD admission обязана сверить все individual bytes/hashes/refs и licenses, не только total/count. Не требуется повторять Node/render, чтобы признать правильный выбор исходного API.

Package LICENSE — MIT software notice Khan Academy/contributors; package-level MIT нельзя автоматически перенести на fonts. Bounded raw UTF-16BE scan Main-Regular.ttf подтверждает отдельные Design Science/Khan Academy copyrights, Reserved Font Name KaTeX_Main и SIL Open Font License1.1. Это font metadata observation, не font execution/parser и не полный юридический аудит каждого файла. Unmodified font bytes/embedded notices сохраняются. Apache header font-build Makefile не relicenses готовые font binaries.

**Full raw OFL1.1 artifact пока unadmitted.** Receipt фиксирует HTTP403/no raw license admitted, original failure trace retained, response body/headers unavailable, official web text/link available отдельно. Web availability или MIT file не заменяют missing exact raw artifact hash/notice closure. В final assets.lock null/TODO hash недопустим; candidate missing license status не повышается до verified. Нужны полный license text и retained distribution-specific copyright/RFN notices, без template placeholders или догадок. Это конкретный publication/license blocker, не опровержение source/API binding. Reviewer не повторял сеть, не создавал license replacement и не вносил новый trust root.

Остальные RD presentation assets/licenses, full Documenter tree, toolchain/import audit и fresh native BUILD admission остаются незакрытыми, как в original DOC04 design. Этот addendum их не наследует от готового KaTeX source.

## Findings / gates / STOP

Новых blocking design findings нет. Implementation acceptance обязана сохранить все уточнённые negative/healthy controls, особенно unsupported resource colored fallback, macro lexical gate, changed/hash-mismatched file, style-important conflict, missing font/license, source→node mapping и no CSP residue. Ни один из этих tests не выполнялся reviewer. No render/native/browser/prod/public/scientific PASS, no solver и no cache warming/build loop.

CP-DESIGN PASS разблокирует разработку source-bound bridge/gates в ранее разрешённом scope. Он **не** разблокирует full public font closure, asset-lock admission/render/publication при missing license/pins, native imports без fresh admission, новый grant/corrective loop или public release. Исходные delivery/addendum/parent artifacts и HTTP403 failure остаются неизменяемыми evidence.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact default ESM renderToString API установлена | package exports + dist default object/path/hash | Node import/render не выполнялся | сохранить |
| Options/macro/resource policy faithful source | Settings/Namespace/def/macros/handlers | Lexer/bridge/output guards ещё не реализованы/проверены | сохранить |
| CSS/font candidate set имеет exact scoped closure |60local unique refs/files, names/types/count/total, candidate inventory | Full individual asset admission ещё впереди | сохранить |
| Public font/license closure готова | MIT code notice и отдельные OFL font markers | Полный raw OFL/notice artifact unadmitted,403 retained | данных недостаточно |
| Static CSP math/CSS эквивалентны | Precise extraction/cascade contract | Нет computed-style/layout/browser proof | дополнительно измерить |
| DOC04 native/publication/science ready | Таких receipts нет | Остальные assets/tree/import/admission/browser gates открыты | данных недостаточно |

**STOP.** PASS только source/API CP-DESIGN addendum; лицензии/full BUILD/publication остаются blocked. Sole output — этот report.
