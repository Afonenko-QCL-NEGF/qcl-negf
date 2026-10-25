# DOC04 Root — Phase2 pure adapter implementation

Подготовлены три product source файла в isolated `/tmp/qcl-doc04-root-worktree`
на exact HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, ветке
`codex/review-closure-docs-presentation`. **Тесты не изменены; executor не запускал
код, parser, imports, tests, render/build, Julia/Node/Python, сеть или children.**
Syntax/GREEN не измерены. Результат заморожен для independent high CPP; два
оставшихся GREEN-вызова принадлежат Root и в этой фазе не расходовались.

## Изменения и границы

`ops/docs/assemble.py` — stdlib-only pure transforms/validation. Входной page
byte hash и exact Documenter1.17.0/tree/policy проверяются до разбора. Известная
head config externalized с тем же relative BaseURL, local HTML reference и
content-derived path. Generated external fixed-light CSS задаёт light surfaces,
focus/form/error/loading states; другие темы, settings/version runtime nodes
удаляются по известным identifiers. Unknown inline script, duplicate config,
unknown theme/head script, inline style/event или missing asset map блокируют
преобразование; remote bytes не скачиваются. Resource rewrites принимают только
явную exact prepared mapping, admission этой mapping остаётся у owning caller.

Math extraction использует reviewed records с exact TeX/hash/page/ID selector,
проверяя raw Documenter p.math-container display или plain span inline shape.
Ни dollar regex по произвольному тексту, ни исправления формул нет. Неизвестный
или неполный mapping даёт failure. Текущий узкий adapter принимает ID selectors;
raw generated страницы без соответствующего reviewed occurrence mapping ещё не
готовы к full pilot. `transform_page` возвращает **intermediate** raw TeX nodes +
math records, не выдает их за final static rendered math или public bundle.

Static payload validation проверяет version-local allowlist, private paths,
symlinks, text credentials, HTML/CSS references, page anchors, script-local
importScripts и **document-relative** classic Worker URLs, отсутствие CDN/blob/
неизвестного loader grammar, inline CSP residue и theme alternatives. Это
ограниченный static scanner для закрытой admitted asset set, не общий JavaScript
interpreter/security oracle. Unknown loader grammar отказывает; existing
RequireJS/runtime bytes не объявлены готовыми. Public asset licensing и complete
runtime closure нужны отдельно. SVG vocabulary ограничен inert reviewed forms.

`pilot-plan.json` содержит три canonical journeys, root-relative source paths,
URLs/anchors, complete owning support-page policy, expected source inputs и
finite caps. Component revisions в plan не дублируются: source graph остаётся
существующим `ops/git.ts` контрактом. Changed source graph rejects; draft plan не
утверждает существование пока отсутствующих owning recipes/schema/assets.lock.

Asset entry validator различает local byte/hash/notice metadata и полномочия
лицензии: возвращает `bytes_verified`, `license_authority=not_evaluated`, требует
OFL-1.1 attribution для KaTeX fonts. Private synthetic font test не превращается
в admitted public OFL artifact. Full asset lock не создан и не подменён fake
hashes/licenses. `prepare_catalog` сохраняет supplied fragments/coverage и всегда
fail-closed до owning shared-schema validation binding; missing schema явно
`blocked`, `bundle_bytes=null`, без fake origins или root DOC03 schema.

`ops/docs/math-render.mjs` проверяет supplied exact local module bytes/SHA до
любого target import, фиксирует версию0.16.8 и exact CSS hash; затем использует
**public default ESM** `renderToString`, без internal API/CLI/plugins/install.
Перед render все records проходят closed shape/hash/identity и bounded TeX
lexer: comments/control-symbols учитываются, definition/resource/file/diagnostic
commands и unreviewed authored geometry отвергаются. На каждую формулу новый
plain `macros={}`, `trust=false`, `strict='error'`, `throwOnError=true`,
`htmlAndMathml`, `maxExpand=1000`, `globalGroup=false`, `maxSize=Infinity`.
Finite maxSize не используется для silent geometry clamp.

Markup scanner принимает закрытые static span/MathML/SVG tags/attributes,
сохраняет semantic attributes и source occurrence, rejects active/resources/
unknown shapes. Все inline declarations, включая SymbolNode italic margin,
переносятся в SHA256 classes и external CSS с сохранением ordered duplicates,
чисел и units. !important context proof консервативен: любой competing property
с !important в закрытых supplied stylesheets блокирует extraction независимо от
selector; unknown/escaped unreviewed context также отвергается. Нормальный
stylesheet не заменяет browser computed-style/layout comparison.

CSS/math output caps считаются и после externalization; никакого fallback
unsupported colored text или частичного успешного batch результата нет.
`license_status=not_evaluated`: private math units не публикуют fonts. Immutable
prepared module directory — precondition всей попытки; adapter не управляет
окружением. Wall/CPU/RAM/log supervisor остаётся внешним, явно требуется в
возвращаемой metadata. Синхронный KaTeX не выдаётся за прерываемый setTimeout.

## Frozen source / evidence

| Источник | Bytes | SHA256 |
| --- | ---: | --- |
| `ops/docs/assemble.py` | 31656 | `4c665bc22c1375e51815f6b229bfc9b9030204e7c9bd7284fee49dcec9437270` |
| `ops/docs/math-render.mjs` | 15765 | `11a4c1381d88e071ecbae89f1727a1d63b3d5e9d0fecfded6bc189b0d5fc54b5` |
| `ops/docs/pilot-plan.json` | 2120 | `cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50` |
| `/tmp/qcl-doc04-root-impl-patch.diff` | 51080 | `9dd6022c325a4fcc7b19b0eadf6fe9e87263abf12680f39ecd9453af45edfc57` |

Tests побайтово прежние: Python `ecacc18239241c45ac1ed9c4e7c4935cfd20919cc88ac236a69ffa435bdf038e`,
Node `7ae60b15740e7e9790318f8724d364f2a9ce567b2a0480cf13c988172966aef3`.
Exact accepted D/R и test-source review SHA перечислены в identity.
`git diff --no-index --check` для трёх новых файлов не выдал whitespace findings;
exit1 no-index означает additions, не test failure/pass. Проверки syntax/import
не выполнялись. Main/protected original не записывался. Core/Runner recipes,
shared docs, ops/solver, assets lock и schemas не менялись; Git stage/commit/push
отсутствуют. Patch включает только три product additions относительно baseline.

## RED classification и конечные allocations

Retained Root evidence прочитано, не переисполнялось:

| Вызов | Наблюдение | Классификация |
| --- | --- | --- |
| `/tmp/qcl-DOC04-PY-RED-1` | exit2,0.747s, FileNotFoundError assemble.py при collection; raw841bytes, guards none | **Readiness RED**, поведенческие assertions не исполнялись |
| `/tmp/qcl-DOC04-NODE-RED-1` | exit1,0.152s, ERR_MODULE_NOT_FOUND math-render.mjs; raw1455bytes, guards none | **Readiness RED**, поведенческие assertions не исполнялись |

Receipt/log SHA256 приведены в identity. Это не numeric/scientific failure и не
доказательство behavioral RED. Root явно разрешил переход к implementation на
этом readiness свидетельстве; executor не расходовал дополнительный RED.

Текущая source-only allocation: до40min,1CPU,2GiB RAM, reads<=5MiB,
outputs<=128KiB; собственных runtime calls=0. Unit budget общий: used2/4,
remaining **один PY-GREEN и один NODE-GREEN только Root после CPP**, без autorerun.
Retained local-unit envelope: каждый <=90s,1CPU affinity, sampledRSS<=1GiB,
ownedTEMP<=32MiB, stdout/stderr<=2MiB. RSS/TEMP sampling50ms не является hard
quota/transient-peak proof; complete byte capture/raw receipts сохраняются.

В adapters: TeX<=16KiB, JSON batch<=4MiB/10000records, output<=256KiB/expression,
aggregate<=32MiB, CSS<=1MiB/20000groups. Payload<=10000files/256MiB,
file<=16MiB; manifest<=2MiB/fragment<=32KiB. HTML depth<=512,
nodecount<=100000/page. Math isolated supervisor wall<=60s и остающийся admitted
CPU/RAM/log budget — внешний required gate, не внутренняя гарантия.

Public full OFL/license closure, DOC03 shared serialization/schema, complete
Documenter tree/import manifest/native BUILD admission и browser acceptance
**остаются blocked/not_measured**. Recipes/orchestration/final materialization не
притворяются сделанными этими тремя pure adapters. CI-once, scientific S1,
production/publication не расходованы и не объявлены accepted.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure adapter source реализован | Exact cfc38e1 + три path/hash/symbol groups выше | Syntax/tests не запускались | сохранить |
| Immutable controls сохранены | Повторные Python/Node SHA256 | Ещё нет behavioral GREEN | дополнительно измерить |
| Readiness RED наблюдался | Два retained Root raw logs/receipts | Не behavioral assertion evidence | сохранить |
| Local math источник связан с exact KaTeX | Hardcoded module/CSS pins + hash-before-import source | Import/render не выполнены executor | дополнительно измерить |
| Public/native/browser/science готовы | Таких receipts нет | OFL/schema/assets/import/admission gates открыты | данных недостаточно |

**STOP: independent high CPP на frozen source; затем Root sole два GREEN-вызова.**
