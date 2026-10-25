# DOC04 — KaTeX 0.16.8 source/API binding addendum

Дата: 2026-10-19. Focused D ultra, один source-only round. No children.
Это дополнение к принятому DOC04 contract, а не новая реализация или новый build.

## 1. Immutable inputs и граница закрываемого gap

Сохранены неизменными:

- DOC04 D `/tmp/qcl-doc04-design.md`, SHA256
  `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b`;
- source identity `/tmp/qcl-doc04-identity.json`, SHA256
  `924fed8c97da7fa25ad0fe579789d4d8a44b46e5d5bb575bdbf6158bf7a82356`;
- independent CP-DESIGN PASS `/tmp/qcl-doc04-design-review.md`, SHA256
  `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164`.

Новый exact input — source distribution
`/tmp/qcl-doc04-katex-0.16.8/source/package`. Root fetch receipt
`/tmp/qcl-doc04-katex-0.16.8/receipt.json`, SHA256
`4493f9d81a9b9ab0c09d5cd82e4849748f673d1af620d7389e2328ea7e36baa4`.
Receipt фиксирует official npm registry0.16.8 metadata, exact tarball,
SHA512 integrity verification и no install/scripts/import/render. Это receipt
получения source, не native toolchain, package-tree или rendering evidence.
Автор дополнения не выполнял запросов в сеть и не повторял download.

Source identity содержит exact hashes consumed code/CSS/fonts/licenses и URL
reference edges. Distribution/receipt не изменялись. Не запускались Node/module
imports, target parser, render, Julia, tests/build/server/Git mutations/solver.
25 min, 1 CPU/2 GiB, read<=6 MiB, report+identity<=64 KiB. Только `/tmp` outputs.

Устанавливается public API binding и наличие exact KaTeX code/CSS/font bytes.
Это закрывает прежнее factual отсутствие **этих** source/API inputs. Полная
public font license closure, остальные RD assets, полный Documenter tree,
native binaries/import audit/admission и actual CSP/layout/browser acceptance
этим дополнением не закрываются.

## 2. Подтверждённый public API

Primary `package.json`: name=katex, version=0.16.8, exports["."].import=
`./dist/katex.mjs`, require=`./dist/katex.js`. ESM file заканчивается
`export { katex as default };`; katex object version=0.16.8 и содержит
renderToString. **Named ESM export renderToString отсутствует.**

Выбранная future build-only binding:

```javascript
// Текст контракта, в этом D не исполнялся.
import katex from "<verified-local-distribution>/dist/katex.mjs";
const markup = katex.renderToString(tex, options);
```

`dist/katex.mjs:18245–18248`: renderToString вызывает
renderToDomTree(expression,options).toMarkup(). В source нет потребности в DOM
для этого пути; функция render(expression,baseNode,…) — другая, DOM-writing API,
она не выбирается. Source feasibility не доказывает уже выполненный Node import.
Не использовать internal __parse/__renderToDomTree, global __defineMacro,
auto-render, contrib plugins или CLI.js. Commander из package dependencies не
нужен direct prebuilt ESM file; npm/yarn install/build не выполняется.

Source/API witness paths: `dist/katex.mjs`, `src/Settings.js`, `src/buildTree.js`,
`src/Parser.js`, `src/parseTree.js`, `src/MacroExpander.js`, `src/Namespace.js`,
`src/functions/{def,html,href,includegraphics}.js`, `src/macros.js`,
`src/domTree.js`, `src/mathMLTree.js`. Их чтение не выполняет код.

## 3. Exact options и finite input contract

Bridge принимает только DOC04 mapped math records
`{page,selector,tex_sha256,tex,display}`. Selector проверен against source→node
mapping; arbitrary HTML/DOM selector, delimiter regex по всему тексту, custom
options object от пользователя не принимаются. Tex exact UTF-8 bytes/hash и
equation IDs не переписываются. JSON/schema additionalProperties=false.

Future options на **каждый отдельный** renderToString вызов:

```text
displayMode = record.display                 # boolean
output = "htmlAndMathml"                    # exact supported enum
throwOnError = true
strict = "error"                           # string, не callback
trust = false                              # boolean, не callback
macros = {}                                # новый mutable plain object на вызов
maxExpand = 1000
maxSize = Number.POSITIVE_INFINITY          # library default, не silent clamp
globalGroup = false
```

Settings поддерживает перечисленные names/types; buildTree выбирает HTML+MathML
для htmlAndMathml. Не применять Object.freeze/null-prototype к macros: Namespace
использует current.hasOwnProperty и может записывать внутренние scoped значения.
Fresh object не разделяется между формулами, pages или attempts. Остальные
defaults остаются exact pinned defaults; receipt связывает options policy hash.

`strict="error"` заставляет reportNonstrict throw для соответствующей категории;
useStrictBehavior для другой категории выбирает strict branch, а не обязательно
throw. Поэтому «strict» не объявляется универсальным запретом расширений/макросов.
throwOnError=true запрещает renderError fallback для ParseError; обычный source
failure не подменяется красным текстом как успешным equation rendering.

Finite presentation input guards, не scientific tolerances:

- tex<=16 KiB UTF-8 на expression; batch JSON<=4 MiB, records<=10000;
- maxExpand=1000 соответствует supported finite expansion limit source;
- markup<=256 KiB/expression, aggregate generated math markup<=32 MiB/pilot;
- generated style sheet<=1 MiB и <=20000 distinct style groups;
- каждый math batch имеет external supervisor wall<=60 s и остающийся DOC04
  attempt budget; CPU/RAM не превосходят fresh admitted process limits.

Synchronous JS render нельзя прервать обычным setTimeout в том же event loop;
при wall/RAM/output cap supervisor завершает весь isolated batch process,
сохраняет failed input/hash/log receipt, без automatic rerun. Это будущий
BUILD behavior, здесь не исполнялся. Caps не суммируются сверх DOC04 envelope.

maxSize в KaTeX **ограничивает/clamps геометрию**, а не гарантирует ошибку при
превышении. Поэтому finite arbitrary maxSize не ставится ради pass: он мог бы
молча изменить presentation. Default Infinity не отменяет finite bytes/expansion/
process caps. Explicit authored sizing constructs и oversized layout остаются
unsupported до reviewed source/layout checks; bridge не исправляет lengths
ради fit. Full browser layout/contrast/overflow проверяется DOC05.

## 4. Что означает no-user-macro/extensions

`trust=false` относится к trusted HTML/resource commands. `src/functions/def.js`
явно реализует \def/\gdef/\edef/\xdef/\let/\futurelet/global prefixes;
`src/macros.js` — \newcommand/\renewcommand/\providecommand. Пустой options.macros,
strict и globalGroup=false **не запрещают inline определения**. Это отдельный
предварительный source gate, а не несуществующая KaTeX disableMacros option.

V1 принимает только TeX из reviewed owning source mapping. Caller не может
передать macro maps/functions, plugins, extension packages, JS snippets или
вызвать __defineMacro. Source lexer gate рассматривает control tokens, comments
и escaped backslashes; это bounded lexical policy, не запуск KaTeX parser.
Literal policy rejects:

```text
definition/namespace: \def \gdef \edef \xdef \let \futurelet \global \long
                     \newcommand \renewcommand \providecommand
                     \csname \endcsname \catcode
resource/HTML:       \href \url \includegraphics
                     \htmlClass \htmlId \htmlStyle \htmlData
file/extension:      \input \include \usepackage \require \read \write \openout
diagnostic output:   \message \errmessage \show
```

Unknown dynamic definition/alias/sizing construct → unsupported_source; не
пропускать через regex rewrite. Стандартные built-in KaTeX macros остаются частью
самой pinned библиотеки. Их internal scoped implementation не называется
пользовательским macro injection. Если authored equation требует inline macro,
сохраняется original source и fragment возвращается на focused review; агент
не разворачивает/переписывает формулу сам ради совместимости.

Причина explicit resource deny: `isTrusted` returns false, но href/includegraphics
handlers могут вызвать formatUnsupportedCmd, который строит цветной text node
**без исключения**. Таким образом trust=false+throwOnError=true не доказывают,
что любой trusted-only command даст hard failure. Source gate устраняет эти
inputs, output guard отвергает resource/unsupported shapes. Никогда не разрешать
trust callback или отключение strict, чтобы карточка отобразилась.

## 5. Static markup и CSS extraction под existing CSP

`domTree.js:89–121` toMarkup переносит ordered style declarations в escaped
`style="…"`; SymbolNode отдельно добавляет italic margin-right. MathML содержит
semantic attributes и TeX annotation; HTML ветвь может включать inline SVG paths.
Следовательно raw renderToString output нельзя сразу объявить CSP-clean.

Выбранный existing DOC04 assembly contract уточняется:

1. Запретить script/iframe/object/foreignObject/img/a/resource-loading nodes,
   on* attributes, external href/src/style URL, javascript:/data:/blob: URL.
   Разрешить только known KaTeX HTML spans, static MathML/SVG/path vocabulary
   из pinned output; unknown shape → failure. Namespace URI и TeX annotation
   являются inert metadata/text, не fetch. Scalar source text/attributes escaping
   сохраняются; он не проходит eval/innerHTML live execution в build.
2. Retain semantic MathML/SVG attributes и aria structure. Нельзя удалить math
   attributes как «inline styling» и потерять meaning/accessibility. Сопоставить
   output equation occurrence с исходным page/selector/tex_sha256.
3. Extract **все** inline style attributes, including SymbolNode italic correction,
   в generated external CSS. Classes идентифицируются SHA256 exact ordered
   declarations; не сортировать duplicate properties, не округлять числа и не
   менять units. Исходный style удалён; значения проверены на finite numeric/
   allowed property grammar и отсутствие URL/expression/var()/CSS escapes либо
   других неизвестных executable/dynamic forms.
4. Inline specificity нельзя заменить одним слабым class selector без проверки.
   Для закрытого admitted stylesheet set выбран generated rule с !important
   для extracted declarations; **до этого** guard обязан доказать отсутствие
   конкурирующих !important rules, применимых к тому же math element/property.
   При конфликте → unsupported_style_context, не silent cascade change. В этом
   ограниченном контексте rule wins над normal stylesheet так же, как исходный
   inline normal style; selector/ordering сохранены. Input inline !important
   либо непроверенный CSS context не принимается. Эта достаточная source policy
   ещё требует implementation tests и actual computed-style/layout comparison.
5. Generated math CSS загружается локальным `<link>` из immutable bundle после
   KaTeX CSS; no style elements/attributes остаются. No browser KaTeX JS,
   auto-render, fonts/math CDN или unsafe-inline/unsafe-eval CSP exception.

Source pin доказывает свойства generator source, но не эквивалентность ещё не
написанного CSS rewriter. Browser/equation layout, accessibility, initial light
theme/no-flash и existing Portal CSP остаются DOC05 measurements. Unknown output
не публикуется с «частично красиво» или fallback текущей версии.

## 6. Exact consumed/public files и licensing

Source identity JSON содержит индивидуальный path/size/SHA256/media/license
каждого файла и 60 CSS reference edges. Это machine-readable **candidate inventory**,
не admitted assets.lock с пропущенными лицензиями.

| Файл | Роль / destination / media |
| --- | --- |
| package.json | Source version/export witness, private build input; не browser payload |
| dist/katex.mjs | Build-only ESM module, SHA/size в identity; application/javascript, не публикуется и не импортируется здесь |
| dist/katex.min.css | Public `assets/vendor/katex/0.16.8/katex.min.css`, text/css, SHA256 `df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e` |
| dist/fonts/*.woff2 / *.woff / *.ttf | **Ровно 60** файлов из url() original CSS, destinations `assets/vendor/katex/0.16.8/fonts/<same-name>`; font/woff2, font/woff, font/ttf; all byte hashes в identity |
| LICENSE | Software/CSS MIT notice, public `assets/licenses/katex-0.16.8-MIT.txt`, text/plain; SHA256 `766ccc1f306c885aa45542a9846bbd0a505b27a0374f146778171c2254ce18e3` |
| Full font license notice | Required `assets/licenses/katex-fonts-OFL-1.1.txt`, text/plain; **полный текст пока не предоставлен**, hash не выдумывается |

CSS source содержит 60 unique local url() references, no @import. Все referenced
files существуют, total font bytes=1,076,572. Relative CSS→fonts layout сохраняется
без subsetting/перекодирования/font rebuild. Не включаются unused katex.js,
katex.min.js, auto-render/contrib scripts, src/fonts build tools или source maps.
ESM source bundle self-contained для выбранного direct import, никакого CLI
Commander/npm install. Source/API files в identity не обязаны стать public files.

**Лицензии нельзя свести к package.json license=MIT.** Package LICENSE/README
объявляют KaTeX software MIT. Но Main-Regular.ttf содержит embedded copyright
Design Science2009–2010/Khan Academy2014–2018 и явное `SIL Open Font License,
Version 1.1` с URL. Поэтому fonts не помечаются MIT по соседству. Identity
фиксирует embedded OFL observations соответствующих TTF files. Нужны полный
OFL1.1 text и retained notices для public font closure; tarball не содержит
отдельного OFL file. Missing notice блокирует font-publication/license pass,
а не отменяет подтверждённый source/API binding. Новых web requests здесь нет.

`src/fonts/Makefile` имеет Apache2.0 header, но не consumed/public runtime asset
и не запускается. Это не основание произвольно назвать Apache2.0 лицензией всех
готовых fonts. Сохранять byte-exact distribution fonts и embedded notices;
никаких модификаций font names или implicit relicensing.

DOC04 asset lock для этих inputs может стать admitted только после полного
license closure. Missing OFL artifact остаётся в candidate inventory как missing,
не null/TODO hash в final admitted lock. Остальные RD assets — RequireJS,
jQuery/UI, Headroom, highlight.js, MiniSearch, Lato/JuliaMono/FontAwesome —
по-прежнему требуют собственные pins/bytes/licenses; KaTeX не закрывает их.

## 7. Planned controls и acceptance boundary

Ниже future controls, не выполненные tests:

| Negative | Healthy control / expected observation |
| --- | --- |
| Named `import {renderToString}` | Direct default import; source binding проверяется до execution; нет fabricated named export |
| Wrong module hash/version/asset | Exact 0.16.8 bytes; mismatch rejected до import/render, без latest fallback |
| Inline \def/\newcommand, shared macro object | Plain existing equation + fresh object; definition rejected до target parser, no cross-expression state claim |
| \href/\includegraphics/HTML command при trust=false | Resource-free equation; запрещённый command rejected, colored unsupported text не pass |
| Recursive expansion/oversized input/output | Valid bounded fixture; finite maxExpand/process caps stop failed batch, retained raw/source unchanged |
| Unknown sizing/clamp/style/important conflict | Known static style context; fail без изменения числа/формулы и без CSP exception |
| CSS font missing/hash wrong/OFL notice missing | Exact 60 fonts + both complete license notices; source/API success не поднимает license status |
| Inline style/script/blob/CDN residue | Only external local CSS/static math, existing CSP unchanged; source-static checks отдельно от browser |
| Math source→node mismatch | Exact selectors/TeX hash/IDs/MathML annotation roundtrip; global dollar regex не принимается |

Future comparison должен проверить original renderer markup semantics и
externalized class layout на representative inline/display, fractions,
sub/superscripts, stretch delimiters/SVG и Unicode/MathML accessibility. Browser
при cold cache/offline, OS dark/light и stored theme всегда показывает светлый
сайт, локальные fonts/math, ноль CSP violations. Никакого solver в build/view.
Tests/render/import require их assigned scope/admission; этот source addendum
сам по себе их не запускает и не выдаёт новый grant.

## 8. Disposition

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact KaTeX0.16.8 public ESM binding установлена | package.json, default export, renderToString source и hashes | Node import/render не выполнялся | сохранить |
| Options/macro/resource semantics определены по source | Settings/def/macros/Namespace/handlers | Input gate и bridge ещё не реализованы/проверены | изменить |
| CSS/fonts bytes доступны | 60 reference edges и hashes в identity | Full OFL notice/public license closure пока отсутствует | данных недостаточно |
| Strict-CSP static math реализована и эквивалентна | Пока только precise transform contract | CSS rewriter/layout/browser proof отсутствуют | дополнительно измерить |
| DOC04 native/publication/science ready | Таких свидетельств нет | Остальные assets/tree/import/admission/browser gates сохраняются | данных недостаточно |

**STOP: exact D addendum для отдельного independent high review; math I не начиналась.**
