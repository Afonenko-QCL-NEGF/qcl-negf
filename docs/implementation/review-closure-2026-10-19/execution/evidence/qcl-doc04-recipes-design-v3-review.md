# DOC04 recipes D3 — narrow independent high review

**PASS_SOURCE — R1 и R2 закрыты.** D3 достаточно конкретен для medium I source profiles и blocked preflight. Новых блокирующих замечаний в двух поправках нет. BUILD/render/import/release этой проверкой не разрешены.

## Frozen inputs и primary API

| Input | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc04-recipes-design-v3.md`, 5828 B | `960a639dd281d7a5b99c582f2c9dc8b17e816715753557791460ebcef1159aee` |
| `/tmp/qcl-doc04-recipes-design-v3-delta.json`, 1874 B | `592d72646cfea012ed399f739d990b7e95af9f5ff37cd0e6230f652cb4784ccd` |
| `/tmp/qcl-doc04-recipes-design-v3-identity.json`, 2086 B | `67724abb737b2004b1a6282e96916c2e8f8db38ddb46f75b441a5c1f1f4f6f39` |
| D1 `/tmp/qcl-doc04-recipes-design.md`, 19393 B | `008650e7c9ff98bdaf38a3450d2b3b13818409795c92738d0a9dbddaba2c2505` |
| D2 `/tmp/qcl-doc04-recipes-design-v2.md`, 6646 B | `ce582cc394d7dd70971c2a25929bf9362aad7d829403f1e2e0fba68a8ff65610` |
| Prior R `/tmp/qcl-doc04-recipes-design-v2-review.md`, 15636 B | `759039e4040d54652d288b4bc100fd238b2da679127a49b73be66a873583c017` |
| Actual `components/QCLNEGF.jl/docs/make.jl`, 1553 B | `edafb4e03b0fd9982039267dc24ba7c6332551f7e3770fca20b35fc8dae9380f` |
| Actual `components/QCLNEGFRunner.jl/docs/make.jl`, 744 B | `0749b9989ce07c34034dddac2fe8127a9ecca72d43105425928f7468dae16cbc` |
| Pinned AXNMp `src/documents.jl`, 47497 B | `67ded455a9d8881b6fe3cf4a4cfbc97a992e27cd8e31ad3d28de23cbc3578e06` |
| Pinned AXNMp `src/html/HTMLWriter.jl`, 113880 B | `72b261cbef5e06e9edc4159c038d740b5f5372134f9d75db06eeb35b894b29dd` |

Root HEAD повторно наблюдён: `514cd9707a32cde60c630d60986973a898d35b18`. Core gitlink/actual HEAD `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee`, Runner `1acc165650fd4f4c2d49605cc679f90e3f6fcdae`; их `docs/make.jl` без изменений. Root dirty coordinator-owned work сохранён. Contracts actual HEAD уже отличается от root gitlink; это unrelated состояние не используется как источник DOC04 и не исправлялось. Gitlinks остаются source authority, новый lock не создавался.

Pinned API path: Root `.build/local-julia-int01/depot-1/packages/Documenter/AXNMp`. Проверены фактические type/default/render guards и hashes; полная installed tree/cache/toolchain identity не сертифицирована.

## Два замечания и отсутствие drift

**R1 CLOSED.** D3§1 явно перекрывает все старые operator `modules=[]` и untyped placeholders инструкцией `modules=Module[]`. Параметр selected Documenter `src/documents.jl:420` принимает `Union{Module,Vector{Module}}` с таким же default `Module[]`. Типизированный пустой vector корректен. Owner module не импортируется; operator `checkdocs=:none` и две страницы остаются. Core/Runner retain `[QCLNEGF]`/`[QCLNEGFRunner]`.

**R2 CLOSED.** D3§2 добавляет `sitename` именно к полному pilot kwargs contract, с тремя фиксированными непустыми literals:

| Owner | Exact sitename | Primary witness |
| --- | --- | --- |
| Core | `"QCLNEGF"` | actual Core make:6 |
| Runner | `"QCLNEGFRunner"` | actual Runner make:6 |
| Operator | `"Документация оператора"` | previously frozen generated index heading |

В selected `documents.jl:427` default пустой; `HTMLWriter.jl:823–825` требует непустой `doc.user.sitename`. Все три literals удовлетворяют этому source guard. Они задаются самим recipe, без host/private/environment/cwd interpolation. Core/Runner default branch сохраняет существующие значения. Это source/API correction, не новый измеренный render result.

D3 целиком прочитан. Он является двухпунктовым override к неизменным D1+D2, а не заменой их большого контракта. Независимо пересчитанные D1/D2/prior R hashes совпадают с исходным packet. Delta JSON перечисляет только Module[] и три sitename; его declared unchanged boundaries согласованы с текстом D3. Ни third API choice, ни bypass/admission flag, ни изменение page graphs, default doctest=true, pilot guards до imports, fixed light, operator byte/anchor mapping, deadlines/drains/receipts или trust policy не добавлены.

D2 nested/dynamic-docstring и import/include/extension/cache closure остаётся неизвестной до полного review evidence; наличие `@docs` не выдаётся за отсутствие execution effects. Assets/fonts/licenses/CSS bindings, complete Documenter/toolchain/cache identity, final dependent adapter contract и fresh external admission остаются условиями BUILD. Исторические широкое чтение 5,523,762 B при4MiB — FAILED_RESOURCE_CAP — и отдельная D2 continuation 1,142,390 B сохраняются, не превращаясь в retrospective PASS. Этот narrow R не переаудирует их содержимое или общий runtime.

**Path alias erratum сохранён явно:** в prior R table использованы ошибочные каталоги `components/Core` / `components/Runner`. Реальные primary пути — **`components/QCLNEGF.jl/docs/make.jl` и `components/QCLNEGFRunner.jl/docs/make.jl`**, с приведёнными выше hashes. Старый report не переписывался; исправление локатора не меняет два API findings и их закрытие.

## Собственный read ledger и действия

Envelope этого R: ≤10min, 1CPU, 1GiB, source reads≤4MiB, output≤32KiB. Source payload консервативно предзаряжен по полному размеру файла для каждого чтения, включая early-quit extracts; metadata inventory/Git отдельно, physical I/O/RSS не измерены.

| Read group | Upper bound B |
| --- | ---: |
| Full D3 text | 5828 |
| SHA pass D3+D2+D1 | 31867 |
| Delta+identity full text | 3960 |
| Both owner make full text | 2297 |
| API extracts, charged as complete documents+HTMLWriter | 161377 |
| SHA pass delta+identity+prior R+owner makes+pinned API | 183270 |
| **Total source-read upper bound** | **388599** |

Это консервативная source-byte граница, а не измерение disk sectors/kernel cache. Проверки новых review artifacts не входят в product/source reads. Запуск target code/import/parser/tests/render/build/network/server, product edits, children, Git mutations и checkpoint writes — **0**. Новых C08/science calls нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Operator Module[] закрывает R1 | D3§1; pinned documents.jl:420 | Source-only type check | сохранить |
| Три fixed sitename закрывают R2 | D3§2; actual make:6; documents427/HTMLWriter825 | Render не выполнялся | сохранить |
| Остальной accepted D1/D2 contract не изменён | Full D3/delta и unchanged frozen hashes | Узкий recheck, без global re-audit | сохранить |
| Medium I source profiles готов | Два API blockers устранены, fail-closed boundaries сохранены | Product implementation ещё впереди | сохранить |
| BUILD/native/release готов | Required import/assets/toolchain/admission evidence отсутствует | Source PASS этого не доказывает | данных недостаточно |

**STOP. PASS_SOURCE exact D3 correction; только medium I исходников, все BUILD prerequisites conditional.**
