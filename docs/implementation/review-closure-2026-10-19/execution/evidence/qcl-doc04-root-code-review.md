# DOC04 formatted adapters — независимый high CP-CODE source review

2026-10-20. **REQUEST_CHANGES: F1–F4 — четыре contract findings; F5 — уже наблюдавшийся nonfunctional lint failure.** Не расходовать два оставшихся unit calls на known source gaps. Это не разрешение очередной corrective loop: owning coordinator определяет конечный replan/точный новый frozen source, затем независимое review. Reviewer продукт/тесты не менял и ничего не исполнял.

Разрешённый этап — только source review. Imports/parsers/Python/Node/Deno/Julia/tests/render/build/network/server/Git mutations/children=0. Использованы read-only shell text/Git/hash operations; outputs только этот report и identity. Formatter/lint receipts ниже — первичные **coordinator** measurements, не reviewer execution и не functional GREEN. Cumulative CPU/RAM/read telemetry reviewer не инструментирована;25min/1CPU/2GiB/read5MiB/output128KiB — предел поручения.

## 1. Frozen source / порядок

До кандидатского author conclusion сверены accepted DOC04 D/R, exact KaTeX addendum D/R и test-source v2 review; затем прочитаны все три actual product files, test controls, formatter delta, exact pinned Documenter head/math source и KaTeX API/style/sizing source. Author impl report прочитан после primary source assessment. Отдельно прочитаны предоставленные raw/receipt FORMAT-1 и LINT-1. Ни target parser, ни formatter/linter повторно не запускались.

Actual isolated root `/tmp/qcl-doc04-root-worktree`, HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Status — untracked ops/docs/ и два tests; все восемь gitlinks не инициализированы. Они соответствуют frozen root graph, а не более новым main component candidates. Review не создаёт release-ready/native source binding.

| Файл/артефакт | Проверенный SHA256 |
| --- | --- |
| `ops/docs/assemble.py`,31656B | `4c665bc22c1375e51815f6b229bfc9b9030204e7c9bd7284fee49dcec9437270` |
| `ops/docs/math-render.mjs`,16207B | `cc44314b063213a8d9bb478f9d53e165c562169121ffdde22b5e89834964309b` |
| `ops/docs/pilot-plan.json`,2120B | `cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50` |
| `tests/test_docs_assembly.py`,19642B | `ecacc18239241c45ac1ed9c4e7c4935cfd20919cc88ac236a69ffa435bdf038e` |
| `tests/docs_math_test.mjs`,9799B | `ca055653d7946bd077db69447455aa74e476ce8d37543baaa40b75e082dc11d4` |
| `/tmp/qcl-doc04-root-formatted-identity.json` | `9c74aed0ee5a8d47f11ccb20bb5e76fbe16bc9b555a4c4a13dfaecbd16110393` |
| `/tmp/qcl-doc04-root-formatted-patch.diff`,81481B | `e7dd232373d3d08c2f3df4bae98cb3b037c4cefee380f1dc290f5a64a5c56f7d` |
| `/tmp/qcl-doc04-root-format-delta.diff` | `f7e27acf204aa8234614834739c9a41c6c8290b16c9307ca955b0e7e1568a659` |
| Pre-format `/tmp/qcl-doc04-root-impl-identity.json` | `870989b44732b1f252a70608d67e611ec65b11567b435424ef36747db92e1b8b` |
| Pre-format `/tmp/qcl-doc04-root-impl-report.md` | `e3bdb5aa91563b6e99f8ad0103509107d0cfd9944cb5c0b836876c0757bbbe31` |
| Pre-format `/tmp/qcl-doc04-root-impl-patch.diff` | `9dd6022c325a4fcc7b19b0eadf6fe9e87263abf12680f39ecd9453af45edfc57` |

Primary accepted inputs: DOC04 D `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b`, R `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164`; KaTeX D `c65c38f74b5fd8168c9ed5ee2fc79649e2d7bafa5655a9248aee4aa81dca25a2`, R `b599846a0bf40f45a9834a84b61d280d64500a625c6fc3fda0cce4e3feee5e28`; test R2 `f6d437e7f6e875643baaf374c96e6d04ab2b1c718892e40741a9bcf06700c79b`.

Formatter delta меняет layout/quotes/import ordering MJS и formatted test; literal prohibited TeX set, comment/newline/escaped-backslash witnesses и assertions сохранены по source comparison. Python и plan hashes неизменны. Old impl report не выдаётся за actual formatted identity. FORMAT-1 receipt SHA `54a2fad4ae10bf982998780105b0006e4e6aef1a6de42669e070bec197af239a`: explicit три paths, exit0,0.053s, raw complete; это formatting evidence, не test/render proof.

## 2. Findings — полный коллированный набор

### F1 — P1: static closure принимает неотслеживаемые CSS/ESM network imports

Локаторы `assemble.py::_css_edges:497–510`, `_js_edges:513–538`, `validate_payload:582–597`.

**CSS witness:** admitted intermediate files с index.html→assets/a.css и bytes `@import "https://cdn.example/x.css" screen;` в a.css. URL matcher501 не видит url(...); quoted-import matcher506 требует semicolon сразу после closing quote и не видит media suffix. Последний guard508 сравнивает только число syntactic prefixes: оба count=1, поэтому не отвергает и не добавляет edge. Следовательно remote import остаётся незамеченным; local missing x.css с тем же media suffix также не образует missing-resource failure. Это прямое нарушение DOC04 §6: unknown import grammar должна fail closed, external runtime assets запрещены.

**JS witness:** index.html загружает `<script type="module" src="assets/a.js"></script>`, a.js содержит `import "https://cdn.example/x.js";` (аналогично `import x from "..."`). HTML parser не запрещает module type, `_js_edges` проверяет import только как function-call `import(`; static ESM syntax не traced/rejected. Raw content может пройти remaining theme/private predicates, оставив external module fetch в closure.

Это source-derived counterexamples, **не исполненные tests/network calls**. Достаточный narrow repair: распознавать только конкретно поддержанные closed import forms, а неподдержанный CSS media/import или static ESM import/export-from явно отвергать. Не нужен общий JS/CSS interpreter или новый CDN/CSP exception. Добавить independent missing-local и external negatives, сохранив healthy literal CSS/font/Worker/importScripts controls. Unknown grammar не должна считаться безопасной лишь из-за отсутствия regex match.

### F2 — P2: !important cascade proof неполон и не принимает полный stylesheet context

Локаторы `math-render.mjs::stylesheetsContext:188–210`, `declarations:212–231`, `renderMathBatch:352–357`.

**Shorthand witness:** supplied closed stylesheet `.katex{margin:1em!important}` и markup `<span class="katex" style="margin-right:0.05em">x</span>`. Scanner собирает important property `margin`, но проверяет только `important.has("margin-right")`, поэтому принимает extraction. Исходный inline-normal margin-right проигрывает stylesheet-important shorthand и effective right margin=1em. Generated late `.qcl-math-HASH{margin-right:0.05em!important}` теперь выигрывает по equal specificity/later order; geometry изменена. Аналогично `all:initial!important` против height и border/font shorthands против longhands. Accepted addendum §5 требует доказанного отсутствия **competing** important declarations, не только одинакового spelling property. Conservative rejection здесь допустим, silent cascade change — нет.

**Context witness:** renderMathBatch требует stylesheets.length===1 и exact KaTeX CSS. Полный Documenter page также имеет light/fixed-light/other admitted stylesheets; caller не может передать их в выбранный bridge для проверки, не получив stylesheet_hash_mismatch. Успешная private math unit поэтому не устанавливает тот closed stylesheet set, на котором extraction заявляет достаточный cascade proof. Требуется отдельно связать все consumed stylesheet bytes/hashes/context; один pinned KaTeX CSS не заменяет его. Отсутствие final public materialization снижает текущую deployment опасность, но не делает promised transform faithful.

Narrow repair: сохранить required exact KaTeX pin как обязательный элемент, допустить/связать полный finite admitted stylesheet context либо явный prevalidated complete context token; fail closed для all/shorthand conflicts и неизвестной CSS cascade grammar. Не угадывать computed style и не ослаблять important guard ради GREEN. Нужны independent shorthand/all conflict negatives и healthy full-context control. Browser layout/CSS equivalence всё ещё DOC05.

### F3 — P2: self-closing HTML tokens обходят page node cap и duplicate-attribute guard

Локаторы `assemble.py::_Tree.handle_starttag:221–230`, `handle_startendtag:232–234`, `transform_page::visit:314–372`.

Обычный start tag увеличивает nodes, проверяет100000/depth и duplicate attrs; startend tag просто создаёт node. Page с reviewed known head/body и более100000 `<br/>` (в пределах16MiB) не попадает в declared node cap. Это конкретный обход budget predicate, а не доказательство реального RSS превышения. Self-closing duplicate-attribute token также пропускает rejection: node.attr() превращает attrs в dict, после чего visit может пересериализовать дедуплицированные attributes вместо требуемого unknown-shape fail.

Narrow repair: единый bounded start-node/attribute validation для обоих callbacks; сохранить разницу stack push для void/self-closing. Controls: over-cap self-closing nodes и duplicate attrs в self-closing token с refreshed raw expected hash, чтобы input-hash mismatch не маскировал shape failure. Under-cap healthy self-closing void markup должен оставаться допустимым. Не повышать caps и не запускать native renderer ради проверки.

### F4 — P2: explicit authored size commands обходят V1 unsupported-sizing gate

Локаторы `math-render.mjs::DENY:100–115`, `sourceGate:116–133`; exact KaTeX `src/functions/sizing.js::sizeFuncs` и htmlBuilder/mathmlBuilder. Прочитанный sizing.js SHA `7efd9a5c2e07fc65499d5142182ea3812e5bd3dc13b298f5ef26c3a7c65736f1`.

Accepted addendum §3 и собственный комментарий к DENY объявляют explicit authored geometry/sizing unsupported до focused review. DENY блокирует rule/fontsize/kern/... но не зарегистрированные upstream `\tiny`, `\small`, `\large`, `\Large`, `\LARGE`, `\huge`, `\Huge` и остальные sizeFuncs. Например mapped `\Huge x` проходит lexical gate; upstream поддерживает его и выдаёт sizing classes/mathsize, разрешённые output scanner. Он не unknown TeX и не превратится в error через strict/throwOnError. Следовательно source gate не соблюдает заявленный V1 subset.

Narrow repair: связать finite literal authored-sizing reject set с actual pinned public size primitives и добавить controls с ordinary expression healthy; либо отдельное focused design решение, что конкретные sizing constructs уже review/admitted. Не заявлять, что strict автоматически запрещает их, и не clamp/переписывать geometry. Этот review сам не переоткрывает принятую policy и не предлагает менять формулы.

### F5 — P2/nonfunctional: сохранённый source lint имеет два no-unused-vars failures

Root предоставил `/tmp/qcl-DOC04-LINT-1/original.log` SHA `3c314a42fb584b69e473183745401f1d1dd41b20b4087c9b4d542911e38ab82e`, receipt SHA `7a473ea2d38a5772f48c378a9335cbc53c6c1b8ea6e8f23b4fec35c0b2aee871`. Прочитаны сначала raw, затем receipt. Exit1,0.053s,852 bytes, raw complete/no guards, exact formatted MJS/test hashes совпадают с reviewed candidate. Это coordinator lint evidence, не functional failure.

Локаторы math-render.mjs169 callback `whole` и400 destructured `html`. Их unused status соответствует source. Достаточна nonfunctional owning correction names/binding без удаления mapping validation или ослабления lint rule; хранить original failed raw/receipt. Не повторять lint/tests автоматически за счёт этого report.

## 3. Подтверждённые стороны / цепочка contract→source→tests

Plan точно содержит три canonical slice IDs/owners/source paths/URLs, expected six primary anchors и maximum caps. Revisions не дублируются в plan. load_pilot_plan читает bounded bytes, rejects duplicate JSON members, закрывает поля и не позволяет поднять maxima. validate_primary_sources сравнивает canonical literals, не self-derived mutated plan; validate_source_binding сохраняет existing graph equality/shape check. Эти pure functions не устанавливают сами fresh complete Git tree/build trust; graph authority остаётся ops/git.ts и coordinator binding.

transform_page проверяет exact Documenter version/tree/policy и supplied expected raw SHA до parse. Primary pinned HTMLWriter.jl1119–1143 действительно использует double-quoted documenterBaseURL, theme identifiers и site/version scripts;2388/2390 выдаёт p.math-container `\[...\]` и plain span `$...$`. Source mapping в Python сверяет exact page/selector/TeX hash/display/cardinality, не ищет dollars в price/code. ID-only mapping остаётся declared narrow intermediate subset; фактические generated pages без reviewed IDs/occurrence map не ready. Не найдено переписывания формулы или thresholds.

Known config externalizes то же relative base value в content-derived generated file и local page-relative script reference. Old test F4 проверяет exact assignment/reference/closure. Known themes/settings/version/OS runtime nodes удаляются, external fixed-light CSS создаётся; unknown inline script/event/style/unknown theme/missing map fail. No solver/owning package import/network/process/publication выполняется adapter source. Выход честно intermediate raw-TeX HTML, не final static public page. RequireJS/data-main/runtime replacement и complete admitted runtime assets ещё не готовы; это явно disclosed blocked integration scope, не доказанный полный DOC04 implementation.

Math inputs bound exact ESM/CSS bytes/version: lstat regular/no symlink/size, realpath, SHA до dynamic target import; wrong-file sentinel не импортируется. Immutable prepared input directory — precondition, не hostile concurrent mutation proof. Direct default export katex.renderToString используется без internal APIs/install/plugins. Options per expression: htmlAndMathml, strict error, trustfalse, throwOnErrortrue, fresh plain mutable macros{}, maxExpand1000, maxSizeInfinity/no clamp, globalGroupfalse. Lexical comment/control-symbol handling и literal definition/resource/file/diagnostic reject set соответствуют accepted scope, кроме F4 sizing omission. Trustfalse не объявлен единственным ресурсным запретом.

Markup scanner ограничивает span/MathML/SVG vocabulary/attrs, escaping и shape; сохраняет annotation/source occurrence, отказывает active/resource/event markup. CSS declaration order/duplicate properties/units сохранены, class hash deterministic; output/css/group/aggregate caps проверяются. Перенос всех inline styles выполняется до return. F2 препятствует заявлению cascade equivalence, не опровергает остальные byte/shape checks. External60s/CPU/RAM/log supervisor честно required metadata/precondition: synchronous render не выдаётся за interruptible timer.

validate_asset_entry даёт только bytes_verified/license_authority=not_evaluated; synthetic OFL-shaped fixture не объявлен public font license admission. Actual whole lock/distribution/license authorities не fabricated. prepare_catalog всегда blocked/bundle_bytesNone до owning schema validation binding, не создаёт second DOC03 schema/origins. Full OFL403/raw source history, shared schema, assets.lock, Documenter import/toolchain/native BUILD admission и browser/publication остаются open. Ни short source unit, ни future GREEN не снимают эти gates.

Existing reviewed Python tests unchanged hash; formatted Node test сохраняет assertion смыслы. Они meaningful для covered policy, но не ловят F1–F4 witnesses. Добавление различающих controls должно сохранять все old healthy/negative controls; «сделать существующие fixtures зелёными» не заменяет causal contract closure. Current overall test-source coverage не доказана execution, не general hostile JS/TeX/CSS security oracle.

## 4. Выход / бюджет / ограничения

Root сообщает unit used2/4 (два retained missing-module readiness RED), remaining один PY и один Node GREEN. Reviewer не подтверждает новые runtime результаты и не расходует calls. FORMAT/LINT отдельные coordinator source-tool attempts не называются unit GREEN или full CI. Новых autorerun/engineering/scientific grants этот report не даёт. После owning correction нужна новая immutable identity и source review до sole remaining calls; если budget/contract не позволяет — concrete blocker, не скрытый retry.

Native BUILD/full public font/license closure/shared schema/complete runtime assets/browser/CSP/layout/offline journeys и source graph release acceptance остаются отдельны. Scientific authority остаётся Core/research; этот presentation adapter не physics oracle и не scientific acceptance. Public UI должен оставаться светлым; dark alternate/CSP exception не предлагаются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Static closure исключает все поддержанные import edges | _css_edges/_js_edges и actual witnesses | F1 media CSS/static ESM пропускаются | изменить |
| CSS extraction сохраняет inline-normal semantics | Ordered declarations/hash/output guards | F2 shorthand/all и incomplete full stylesheet context | изменить |
| Page node/shape caps едины для HTML tokens | _Tree callbacks | F3 startend обход | изменить |
| Explicit authored sizing unsupported | DENY и pinned sizing.js | F4 known size primitives разрешены | изменить |
| Formatter/lint source gates green | FORMAT0 и LINT1 retained receipts | F5 two unused vars; functional execution отсутствует | изменить |
| Exact API/source/math/three-slice/blocked gates faithful в остальной части | Actual files, primary pins, reviewed tests, disclosures | Source only; не complete public/native proof | сохранить |
| Unit/native/public/browser/science acceptance получены | Новых таких receipts reviewer нет | Known findings + missing public/build prerequisites | данных недостаточно |

**STOP. REQUEST_CHANGES F1–F5; reviewer executions=0.**
