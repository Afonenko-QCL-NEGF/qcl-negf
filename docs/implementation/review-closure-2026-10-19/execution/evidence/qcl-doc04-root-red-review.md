# DOC04 Phase1 RED: независимый high test-source review

2026-10-19. **REQUEST_CHANGES — четыре коллированных test-source finding.** Есть один malformed healthy closure fixture и три пробела различающей силы assertions. Missing adapter modules — ожидаемый readiness RED; он ещё не наблюдался и не подтверждает поведенческие assertions. Никаких imports/parsers/Python/Node/Julia/render/tests/build/network/server/Git mutations/children или product/test source edits reviewer не выполнял. Runtime calls=0.

## Frozen identity / первичные входы

Root worktree `/tmp/qcl-doc04-root-worktree`, HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, branch `codex/review-closure-docs-presentation`. Status содержит только два untracked test files; implementation отсутствует. Submodules по authored phase1 identity не инициализированы, реальные source/native imports через них не выполнялись.

| Артефакт | SHA256 |
| --- | --- |
| `tests/test_docs_assembly.py` | `4c0f3f10d952be0e38c3c3c3caa098af14e0e126720428dd16ae574dc3106422` |
| `tests/docs_math_test.mjs` | `7ae60b15740e7e9790318f8724d364f2a9ce567b2a0480cf13c988172966aef3` |
| `/tmp/qcl-doc04-root-red-patch.diff` | `7ccff023590d62ff8e8959015cb44d1b24fded2276c6074b965e0f8949f0d440` |
| `/tmp/qcl-doc04-root-red-identity.json` | `fda4daaf0b35e8851a437d382ddfafc5e3a4e526b7ee9dda6e7451fc53d5f108` |
| `/tmp/qcl-doc04-root-red-report.md` | `e60d76437fcd1a5070908de22f4db8a5e911cd50d56be8fc05ed124c2f95b87a` |

Accepted primary D/R прочитаны/сверены до test source и авторского отчёта:
DOC04 D `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b`, R `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164`; exact KaTeX binding D `c65c38f74b5fd8168c9ed5ee2fc79649e2d7bafa5655a9248aee4aa81dca25a2`, R `b599846a0bf40f45a9834a84b61d280d64500a625c6fc3fda0cce4e3feee5e28`.

## Findings — полный набор

### F1 — P2: healthy Worker closure fixture разрешает URL относительно JS file вместо документа

Локатор `tests/test_docs_assembly.py:164–171`:
index.html загружает `assets/search.js`; этот classic script создаёт `new Worker("worker.js")`; inventory содержит только `assets/worker.js`.

Worker constructor разрешает relative URL в контексте документа, а не автоматически относительно src classic script. Для данного index.html требуемый worker — `worker.js` в root. В fixture его нет. `importScripts("minisearch.js")`, напротив, разрешается относительно worker URL; это другой base rule. Корректный closure scanner должен отвергнуть нынешний initial positive на171 ещё до намеренного удаления font/miniSearch.

Это unrelated malformed fixture RED, не требуемая регрессия продукта. Более того, scanner, ошибочно считающий Worker URL относительно `assets/search.js`, будет rewarded green этим test.

Минимальный repair: сделать document-relative Worker URL и actual inventory согласованными (например assets/worker.js от root index), сохранив worker-relative importScripts edge. Добавить различающий missing-root-worker negative либо equivalent base-resolution control; healthy должен проходить до каждого single-factor missing target. Никакого browser/network запуска или новой loader policy для исправления не требуется.

### F2 — P2: three-slice test не фиксирует exact primary sources/URLs

Локатор `tests/test_docs_assembly.py:129–144`. IDs/sections/anchor names сравниваются с literal expectations, но available sources строятся из самого plan (`available={path ... primary_sources}`), а затем один self-derived path удаляется.

Если plan поменяет researcher/developer/operator primary_sources на посторонние paths, сохранив IDs/sections/anchor list, test по-прежнему передаст exactly those same paths как available и пройдёт. primary_urls вообще не проверяются. Поэтому assertion name «require exact sources» и требование DOC04 canonical three journeys сейчас не различают wrong source/URL mutation.

Минимальный repair: независимый literal expected mapping canonical primary source paths и primary URLs/anchors по принятому D, включая Root authored operator chapter и Runner routes. Отдельные source/URL one-field mutants должны отклоняться; healthy available set не извлекать целиком из проверяемого изменяемого plan. Это не новая schema/policy, а проверка уже принятого plan contract. Существующий missing-source negative оставить как отдельный availability test.

### F3 — P2: MIT-font negative не имеет matching healthy font control и смешивает категории

Локатор `tests/test_docs_assembly.py:208–228`. Healthy entry — a.css/text-css, family fixture и LicenseRef-Test. Font negative меняет family на katex-fonts и license на MIT, оставляя CSS source/MIME/data; positive licensed-font-shaped entry отсутствует.

Такой test допускает implementation mutant «reject every katex-fonts family» с тем же font_license_mismatch: все имеющиеся assertions останутся green, хотя корректно licensed future font inputs не допускаются. Он также не отличает отказ по malformed family/file category от отказа по MIT attribution настоящего font-shaped input.

Минимальный repair: добавить private synthetic healthy font-shaped entry (consistent extension/MIME/family/size/hash/notice metadata, с явно синтетическими bytes и без public license claim), затем менять только license attribution на MIT. Missing notice/hash должен проверяться отдельно при том же healthy shape. Если реальная OFL artifact admission отсутствует, private unit fixture не объявлять admitted public license: проверяется validator policy/shape, а не юридическая/production font closure. Generic synthetic CSS-license tests остаются полезными и не требуют настоящих fonts.

### F4 — P2: externalized config может иметь wrong BaseURL или быть orphaned, и transform test останется green

Локатор `tests/test_docs_assembly.py:61–82`, особенно generated_files checks77–79. Проверяется лишь непустое множество файлов и наличие bytes documenterBaseURL где-нибудь в них, а inline script удалён из HTML.

Accepted DOC04 §5.1 требует сохранить **то же значение** relative base URL и подключить generated per-page config как local script. Mutant может записать documenterBaseURL с другим значением или оставить правильный generated file, не добавляя ссылку из output HTML; нынешние assertions не заметят ни одно нарушение. Output/input SHA assertions лишь хешируют фактически выданный результат и не доказывают его семантику. Generic closure tests не объединяют transform result с generated_files, поэтому тоже не закрывают orphan branch.

Минимальный repair: независимая проверка preservation известного input config value и соответствия output script reference существующему generated file в том же version-local payload; unknown/duplicate config negatives сохранить. Подойдут static assertions по known assignment shape и ссылкам, без eval/target parser. Wrong value и missing/wrong reference mutations должны провалить ту же positive проверку. Generated path/hash naming не нужно превращать в новый public contract.

## Что уже является meaningful causal test source

Python controls используют отдельные expected error codes и обновляют expected raw hash там, где изменяют generated shape. Это позволяет отличить intended shape reject от hash mismatch. Wrong version/tree, changed raw bytes, duplicate/unknown inline config, wrong math source mapping, inline-vs-display explicit mapping, executable directive sentinel, source graph component drift, page/anchor absence, private payload/maps/symlinks, generic asset missing/hash/license и missing shared schema имеют понятные observable assertions. RAW явно synthetic excerpt, не fabricated retained Documenter output. Price dollar text сохраняется без global math regex.

Пропонованные local pure seams/result/error codes routine и не создают второй DOC03 schema/API или новый trust policy. prepare_catalog с отсутствующей shared schema возвращает blocked/bundle_bytes=null и не выдаёт empty fragments за готовую serialization. Не требуется для private units отложить все math tests до public OFL/schema gate.

Node test source использует exact supplied local ESM/CSS SHA и обязательный DOC04_KATEX_ROOT; missing input не превращается в skip. Direct public default export KaTeX0.16.8 контракт соблюдён в expected bridge; actual target import должен выполняться реализацией только после verification. Sentinel wrong-module test ловит его преждевременный import по expected error code. No source-tree/latest fallback предусмотрен.

Private math positive требует HTML+MathML, source occurrence identity, отсутствие inline styles/scripts/events, external CSS и license_status=not_evaluated. Macro/resource lexical deny имеет полный literal set accepted addendum, код ошибки unsupported_source не даёт засчитать upstream colored unsupported command как success. Unknown TeX/sizing, UTF8 bound, finite expansion negative, shape/hash/mapping/multiplicity, ordered duplicate styles, deterministic CSS, semantic MathML/SVG и !important/unsafe markup controls полезны и не требуют browser/native pass.

Comments/backslash fixture проверена чтением literal source bytes: JS line98 содержит обычный newline escape `\n`, который создаёт newline в строке, а не ошибочно double-escaped literal backslash+n. String.raw matrix case имеет две TeX backslashes перед letters def и не является literal \def macro. Здесь unrelated malformed escaping не найдено. Python bytes/raw TeX fixture также не объявлялся исполненным parser proof.

## Ограничения покрытия и RED readiness

Frozen baseline не содержит ops/docs/assemble.py, ops/docs/math-render.mjs и pilot-plan.json. Python loader15 и ESM import11–13 первоначально остановят collection/import при отсутствии реализации. Это **ожидаемый, но ещё не наблюдавшийся** readiness RED. Ни один behavioral assertion, parser или runtime этим review не исполнялся; авторская формулировка не выдаёт его за executed RED.

F1 нужно исправить до расхода конечного unit invocation: оно заставило бы корректную реализацию краснеть по посторонней причине. F2–F4 нужны, чтобы future green подтверждал заявленные contracts, а не позволял конкретные приведённые mutants. Reviewer ничего не исправлял; новый frozen test hash/source binding обязателен после owning changes. Routine seam implementation может быть отдельным finite DEV stage; данный report не выдаёт разрешение запуска/импорта или новый corrective loop.

Это не полная acceptance matrix: aggregate markup/batch/CSS/group caps, все shape/property boundaries, весь loader grammar, полный source→node/artifact assembly и actual CSS cascade/layout не закрыты двумя файлами. Existing explicit tests не доказывают exact expansion boundary для всех builtin costs, свежесть macros object во всех будущих implementations или general hostile-TeX security. Эти вопросы остаются CPP/implementation/bounded unit/build/browser scope; не следует расширять phase1 green claim до них.

Font admission отсутствует, raw OFL403 original evidence сохраняется; private render license_status not_evaluated — правильная граница. Schema/public asset lock/complete vendor closure/Documenter tree/import manifest/native BUILD admission остаются отдельно. Ни C08, ни sole final CI, ни new release/full S1/scientific acceptance не расходованы и не объявлены passing. Весь UI должен оставаться фиксированно светлым под существующей CSP; browser proof остаётся DOC05.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED соответствует отсутствующим adapters | Exact baseline + top-level imports/loaders | Не выполнялся; assertions ещё не исполнялись | дополнительно измерить |
| Healthy closure fixture корректен | Worker URL/inventory164–171 | F1 document-vs-script base mismatch | изменить |
| Exact slice binding различается тестом | Plan test129–144 | F2 self-derived sources/unchecked URLs | изменить |
| Font-license policy имеет healthy/negative pair | Generic CSS positive и family/license mutant | F3 no matching healthy font shape | изменить |
| Config externalization сохраняет runtime semantics | Generated files contains key + no inline script | F4 wrong/orphaned BaseURL не обнаружен | изменить |
| Остальные pure math/light/CSP guards имеют полезные witnesses | Source assertions выше | Not_run; не full public/browser/science acceptance | сохранить |

**STOP.** REQUEST_CHANGES limited to test source F1–F4. Report+identity — единственные outputs; execution/source writes/Git mutations отсутствуют.
