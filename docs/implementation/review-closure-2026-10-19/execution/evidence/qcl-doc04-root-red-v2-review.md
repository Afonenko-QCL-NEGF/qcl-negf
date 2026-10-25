# DOC04 Phase1 RED v2 — независимая corrective source review

**PASS для узкого F1–F4 test-source scope; source eligible для отдельно привязанного bounded RED.** Новых блокирующих замечаний в этом delta не найдено. Это не syntax/runtime/RED/GREEN/public bundle acceptance. Reviewer не выполнял imports/parsers/Python/Node/Julia/tests/render/build/network/Git mutations и не создавал children. Runtime calls=0. Единственные записи — этот report и его identity.

## Identity и порядок проверки

Фактический read-only HEAD `/tmp/qcl-doc04-root-worktree`: `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Status содержит только `?? tests/docs_math_test.mjs` и `?? tests/test_docs_assembly.py`; все восемь submodules не инициализированы. Baseline не подменён более новым root graph. Сначала прочитаны исходное независимое review и actual source/delta v2 против original frozen patch, затем сверены canonical routes accepted D §1 и прочитан авторский v2 report. В этом раунде accepted design/KaTeX binding не пересматриваются.

| Вход | SHA256 |
| --- | --- |
| `tests/test_docs_assembly.py`, 19642 bytes | `ecacc18239241c45ac1ed9c4e7c4935cfd20919cc88ac236a69ffa435bdf038e` |
| `tests/docs_math_test.mjs`, 9405 bytes | `7ae60b15740e7e9790318f8724d364f2a9ce567b2a0480cf13c988172966aef3` |
| `/tmp/qcl-doc04-root-red-v2-patch.diff` | `cd53b2d774fcae5845f8ec97436f177e3fecd61eee1c2eac3a977e999fa17a29` |
| `/tmp/qcl-doc04-root-red-v2-identity.json` | `79f142661285e198e97bdd75a412e33cd78ef9853f8012d2892926673c09bb7b` |
| `/tmp/qcl-doc04-root-red-v2-report.md` | `ec991a9557813386547bc743614a14f77c141f1f54b5465c7f0b3324f555dd63` |
| Original patch | `7ccff023590d62ff8e8959015cb44d1b24fded2276c6074b965e0f8949f0d440` |
| Original author identity | `fda4daaf0b35e8851a437d382ddfafc5e3a4e526b7ee9dda6e7451fc53d5f108` |
| Original author report | `e60d76437fcd1a5070908de22f4db8a5e911cd50d56be8fc05ed124c2f95b87a` |
| Original independent review | `4c7b969ce90fef61e427780edbc84d5b8700189b8a9e4ecc6da4b51698907863` |

Original three artifacts повторно хешированы: сохранены byte-exact. Patch comparison показывает изменения только Python test: stdlib test-observer imports/class, independent literal journey expectations и четыре соответствующих assertion/fixture regions. Node math patch/source byte-identical v1. Production adapters и plan этим delta не добавлены.

## Закрытие всех четырёх замечаний

**F1 CLOSED — Python245–260.** Healthy classic script теперь создаёт `new Worker("assets/worker.js")` из root `index.html`, что согласуется с фактическим `assets/worker.js` inventory при document-relative resolution. Worker `importScripts("minisearch.js")` остаётся относительно worker URL и находит `assets/minisearch.js`; CSS font URL остаётся относительно `assets/a.css`. Positive complete payload предшествует трём single-factor negatives, каждый из fresh dict: font, worker и importScripts dependency. Отдельный прежний `new Worker("worker.js")` negative при неизменном inventory различает ошибочную JS-file-relative базу. Малформированный healthy устранён без ослабления loader policy.

**F2 CLOSED — Python48–73,195–225.** `PRIMARY` и `AVAILABLE_PRIMARY` теперь независимые литералы; Core theory source/URL, две Runner sources/URLs и Root authored operator source/URL совпадают с accepted DOC04 §1. Healthy план обязан буквально совпасть с ними. Existing expected anchors, включая researcher-final-route/operator-recovery-route, сохранены. Каждый slice имеет отдельный source и URL mutant; wrong source добавлен в available set, поэтому `primary_mapping_mismatch` нельзя заменить случайным `missing_primary_source`. Availability negative сохраняется отдельно. Это проверки принятого canonical plan, не новый публичный format или параллельный revision lock.

**F3 CLOSED — Python292–331.** Generic CSS pin/hash/license controls сохранены. Новый private font-shaped positive имеет согласованные `.woff2`, `font/woff2`, `katex-fonts`, byte count/hash и OFL-1.1 notice metadata. Следующий negative меняет только SPDX на MIT; остальные отдельные negatives удаляют notice или меняют его bytes без обновления expected hash. Поэтому blanket rejection всех `katex-fonts` больше не проходит healthy control, а MIT attribution различается от malformed CSS/font family. Synthetic bytes/notice явно названы private validator fixtures; они не реальные font bytes, не полный raw OFL, не admission артефакт и не юридическое доказательство. Public license blocker сохраняется.

**F4 CLOSED — Python76–87,120–145.** Независимый test-only HTMLParser observer читает только external script attributes. Known input `documenterBaseURL="."` должен сохраниться как ровно одно assignment с тем же literal value; regex anchored целиком, допускает только безвредные var/quote/whitespace/semicolon варианты. Каждый script reference должен быть local relative; `urljoin` разрешает его относительно actual page URL. Ровно одна ссылка обязана вести к найденному generated config path. Поэтому wrong BaseURL, orphan generated config и wrong/missing reference нарушают positive assertions. Составной script-only HTML+generated payload проходит closure, удаление config даёт `missing_resource`; unrelated article/CSS fixture edges не маскируют эту причину. Generated filename naming не превращён в новый контракт. Unknown/duplicate inline config и прежние light/CSP assertions сохранены. Helper — исходник наблюдения теста; parser в review не запускался и JS не eval.

## Границы решения

Проверка narrow corrective, не новый полный implementation audit. Не найдено удаления старых controls, смены physics/model/API/schema/CSP/trust policy или расширения scope сверх исходных F1–F4. Runtime source binding всё ещё должен фиксировать exact два test hashes, actual runtime paths/versions/hashes и supplied KaTeX pins. Обсуждённый coordinator plan четырёх unit calls не исполнялся и не подтверждён данным report.

Missing `ops/docs/assemble.py`, `ops/docs/math-render.mjs` и plan по-прежнему означают ожидаемый readiness RED при первой отдельно разрешённой попытке; collection/import failure сам по себе не доказывает behavioral assertions. Syntax, actual RED и subsequent GREEN не измерены. Сохранены ограничения исходного review: это не полная acceptance matrix всех aggregate caps/loader grammar/CSS cascade, не browser proof. Полный raw OFL/публичная asset closure, shared DOC03 schema, actual Documenter/import/native BUILD admission и public serialization остаются отдельными gates. Source PASS не доказывает scientific acceptance, final CI или release-ready graph.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 healthy base/closure исправлен | Python245–260, positive и независимые negatives | Runtime resolver ещё не проверен | сохранить |
| F2 exact journeys независимо связаны | Python48–73,195–225 и D §1 | План/adapter implementation ещё отсутствуют | сохранить |
| F3 font-license control различает policy | Python310–331 healthy + one-factor MIT/notice negatives | Synthetic fixture не public license evidence | сохранить |
| F4 BaseURL value и HTML reference проверяются | Python120–145 + test-only observer76–87 | Syntax/parser/runtime не запускались | сохранить |
| Original artifacts и math source сохранены | Повторные SHA256 и patch comparison | Не runtime proof | сохранить |
| Bounded unit RED/GREEN | Измерений нет | Exact runtime binding и отдельный grant относятся к coordinator | дополнительно измерить |
| Public/build/browser/science closure | Обязательных receipts нет | License/schema/native/admission gates открыты | данных недостаточно |

**STOP. PASS только source F1–F4 closure; execution=0.**
