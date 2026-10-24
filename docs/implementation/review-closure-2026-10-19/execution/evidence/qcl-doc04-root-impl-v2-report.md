# DOC04 corrective source-only cycle1 — v2

F1–F5 из `/tmp/qcl-doc04-root-code-review.md` (SHA256 `5d196aa4…`) получили
source corrections и дополнительные healthy/negative regressions. Execution,
imports/parser, Python/Node/Deno/tests, formatter/lint, render/build/network,
children и Git mutations executor не выполнял. **Syntax, lint и GREEN не
измерены.** Старый LINT failure не переименован в pass; original log/receipt
сохранены с прежними SHA256.

Checkout прежний: `/tmp/qcl-doc04-root-worktree`, ветка
`codex/review-closure-docs-presentation`, HEAD
`cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Правки только в разрешённых двух
product adapters и двух tests; plan побайтово прежний. Main, other ops/solver,
owning recipes, shared docs, schema/asset lock, source-freezes не менялись.
Новая identity относится к source correction; прежние impl/format/review
артефакты остаются неизменяемыми.

## Точный delta и добавленные controls

| Finding | Код | Различающие controls |
| --- | --- | --- |
| F1 CSS/ESM loader closure | `_css_edges` разбирает только полные unqualified literal `@import` directives: quoted или url(). Остаточные media/layer/supports/escaped/unknown формы отвергаются, а не считаются отсутствием edge. Supported directives маскируются линейно до отдельного url() scan. `_js_edges` явно rejects static ESM import/export grammar; dynamic imports по-прежнему запрещены. | Positive local quoted/url-quoted/url-bare imports; для каждой supported формы missing-local target; external literal targets; unsupported media с external/local URL, url+print, layer, escaped keyword. Module script без imports healthy; side-effect/import-from/export-from формы с local/missing/external targets reject. Старые CSS font/classic Worker/importScripts healthy сохранены. |
| F2 !important/context | `propertyAtoms` раскрывает shorthand overlap для all, margin/padding, border/side/width/style/color, font, background, inset и logical aliases; неизвестная important property/grammar fail closed. Extra !important tokens не игнорируются. `completeStylesheets` позволяет передать весь конечный private page stylesheet context с path/bytes/SHA/order binding, exact KaTeX CSS обязателен. | 10 conflicts: margin, padding, border, border-width, border-top vs aggregate color, font, background, inset, logical margin-inline, all. Disjoint opacity-important healthy не допускает blanket-reject mutant. Unknown shorthand/escaped context negative. Полный KaTeX+light context healthy; conflict в extra stylesheet; отсутствующий KaTeX pin, bad extra hash, omitted consumed sheet negative; старый private вызов явно complete=false. |
| F3 self-closing bypass | Оба HTMLParser callbacks вызывают один `_start_node`: одинаковые duplicate attrs/node count/depth checks, различается только stack push для self-closing/void. Caps не подняты. | Under-cap `<br/>` healthy; duplicate self-closing attrs;100001 self-closing nodes; over-depth markup. Для mutated raw fixture обновляется expected source hash, поэтому hash mismatch не маскирует shape/cap failure. |
| F4 authored sizing | В DENY literal все11 `sizeFuncs` exact pinned sizing.js и16 manual delimiter-size primitives exact delimsizing.js. Automatic `left/right` не являются manual size commands и сохраняются. Формулы/длины не переписываются, maxSize по-прежнему Infinity. | Negative для каждой из11 case-sensitive font-size primitives и16 manual delimiter forms; ordinary expression/TeX hash healthy; automatic left/right fraction healthy. |
| F5 two unused bindings | Callback `whole` переименован `_whole`; unused `html` destructure заменён явной projection пяти occurrence fields. `validateMathMapping` не удалён/ослаблен. | Nonfunctional source correction. Lint повторно не запускался; Root выполняет отдельную конечную source-tool revision. |

Pinned primary source фактически прочитан и хеширован:
`sizing.js` → `7efd9a5c2e07fc65499d5142182ea3812e5bd3dc13b298f5ef26c3a7c65736f1`,
`delimsizing.js` → `1594085127352d6881d94f0d41ad5d83863cba47c570abdd90d6db1d48a46c1e`.
Названия взяты из owning registration lists, не из предположения о strict mode.
Это source/API evidence, не выполненный KaTeX render.

## Граница stylesheet context и прежние gates

`completeStylesheets` — routine internal argument, не новый public schema или
CSP/trust policy. Это ordered array actual caller-supplied `{path,text,sha256}`;
каждый hash проверяется, paths уникальны/relative, list<=1024 и bytes<=4MiB,
обязательный exact KaTeX CSS pin присутствует ровно один раз, все primary consumed
stylesheets входят в complete list с теми же hashes. Результат связывает ordered
files/hash и явно указывает authority `caller_supplied_complete_list`.

Проверка **того, что list действительно исчерпывает ссылки final HTML**, остаётся
у owning final materializer; этого этапа ещё нет. Отсутствие complete argument
сохраняет old private units и отмечается `complete=false`,
`private_partial_context`, без public equivalence claim. No final publication API
не добавлен. Неизвестные CSS escapes/important semantics и unsupported runtime
module/media-import grammar останавливаются; поддержка таких форм не имитируется.
Возможен консервативный отказ harmless неизвестного CSS/JS input, а не partial pass.

Все прежние source policies и controls сохранены: fixed-light, same CSP,
hash-before-KaTeX-import, raw TeX/model IDs, fresh macros/trustfalse/strict errors,
finite caps, no public font license assumption. Math-only license_status остаётся
not_evaluated. Full OFL403/license authority, DOC03 shared-schema serialization,
complete vendor/runtime closure, Documenter/import/native BUILD admission и
browser/layout/CSP/offline acceptance по-прежнему blocked/not_measured.
Новых public assets/license/schema approvals нет.

## Frozen v2 identity

| Файл | Bytes | SHA256 |
| --- | ---: | --- |
| `ops/docs/assemble.py` | 33127 | `58d47789da8af18a66136676228c7398fcd50c8797838e8614c8aa07f3d64fda` |
| `ops/docs/math-render.mjs` | 20534 | `9069974229f5c7923725c6d16be9d7cbe57a35d5c069b1380141aa326edb82e3` |
| `ops/docs/pilot-plan.json` | 2120 | `cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50` |
| `tests/test_docs_assembly.py` | 22976 | `2207f3bce01e55774b2a4f3a5930fbb5cc880b84fe6e1b38afeafab3a2a548ca` |
| `tests/docs_math_test.mjs` | 14072 | `ebdecfa1910a03d1c86dd2783c1634b185f324c1473620a2938e0def8f31169d` |
| `/tmp/qcl-doc04-root-impl-v2-patch.diff` | 95710 | `55d7bb4529db0eb39266bb3f7f859c1ec477b6864534197404dc14786e1438a3` |

Patch — все пять additions относительно exact baseline, включая unchanged plan;
precise functional delta относительно formatted parent описан выше. Форматирование
нового кода executor не выполнял. Source-only `git diff --no-index --check` не дал
whitespace findings; exit1 no-index — additions, не execution verdict. Node old
formatted prefix9799bytes имеет прежний SHA `ca055653…`, новые tests только appended.
Python старые test methods не ослаблены, новые методы inserted перед прежними.

Envelope этой correction:35min/1CPU/2GiB/read<=5MiB/output<=128KiB;
executor runtime calls=0. Общий DOC04 unit budget остался used2/4: два retained
readiness RED (missing modules, behavioral assertions тогда не исполнялись),
remaining один PY-GREEN и один NODE-GREEN только Root после отдельных source gates.
Нет autorerun, full CI, scientific run или скрытого profiling/build.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все замечания имеют source correction/causal controls | V2 exact paths/hashes и delta выше | Независимый approval и runtime отсутствуют | сохранить |
| Lint и functional GREEN подтверждены | Нет новых execution receipts | Исправлены только известные source bindings | дополнительно измерить |
| Original failed/frozen evidence сохранено | Старые impl/format identity и lint log/receipt hashes в v2 identity | Новая correction — отдельная identity | сохранить |
| Public/native/browser/science ready | Required receipts отсутствуют | Прежние gates остаются открыты | данных недостаточно |

**STOP: отдельный CPP; Root finite format/lint revision и final CPP до двух GREEN.**
