# DOC04 recipes D3 — две точные API-коррекции

2026-10-20. Source-only correction к frozen D1+D2 после independent R2
`/tmp/qcl-doc04-recipes-design-v2-review.md`, SHA256
`759039e4040d54652d288b4bc100fd238b2da679127a49b73be66a873583c017`.
Замечания сверены с primary pinned Documenter и selected owning make sources.
Оба подтверждены. Julia/imports/tests/render не запускались; это исправление
контракта будущей реализации, а не runtime failure/pass.

Применять D1+D2 с двумя overrides ниже. Все исходные D1/D2/reviews/ledgers/identity
остаются byte-exact неизменными; исторически неверные literals не переписываются.
Никакого дополнительного scientific/UI/trust/BUILD решения здесь нет.

## 1. Operator modules — только typed empty vector

Во всех operator recipe clauses D1/D2 literal `modules=[]` и placeholders,
означавшие untyped empty vector, заменяются инструкцией:

```julia
modules = Module[]
```

Pinned AXNMp `src/documents.jl:420` объявляет
`modules::Union{Module, Vector{Module}} = Module[]`. Literal `[]` имеет
неподходящий Vector{Any}; typed empty vector удовлетворяет заданному контракту.
Operator не импортирует Core/Runner owner module; checkdocs=:none и две страницы
index.md/recovery.md сохраняются. Явное значение не оставляется на усмотрение I.

Core/Runner сохраняют существующие modules=[QCLNEGF]/[QCLNEGFRunner]. Ни default
branch, ни page/module namespace этим уточнением не меняется.

## 2. Каждый pilot задаёт непустой sitename

Добавить обязательный `sitename` к точному набору makedocs kwargs D1§3 и
применить в D2 executable profile contract:

| Recipe owner | modules | Exact sitename |
| --- | --- | --- |
| Core | `[QCLNEGF]` | `"QCLNEGF"` |
| Runner | `[QCLNEGFRunner]` | `"QCLNEGFRunner"` |
| Operator | `Module[]` | `"Документация оператора"` |

Core/Runner literals уже стоят в selected docs/make.jl:6; default branch
сохраняет их. Operator literal совпадает с заголовком frozen generated index
из D1§4 и не содержит host/release/user-specific interpolation.
Все три значения фиксированы recipe, не выводятся из private environment/cwd.

Pinned documents.jl:427 по умолчанию даёт пустой sitename; HTMLWriter.jl:825
явно отказывает при пустом `doc.user.sitename`:
`!isempty(doc.user.sitename) || error("HTML output requires `sitename`.")`.
Поэтому поле обязательно именно в полном pilot kwargs contract, а не только
в неформальном описании. Новый operator recipe не наследует его автоматически.

## 3. Primary binding и unchanged boundaries

Documenter expected version1.17.0/tree56e9c37b5e7c3b4f080ab1da18d72d5c290e184a;
actual named source witnesses:

- documents.jl SHA256
  `67ded455a9d8881b6fe3cf4a4cfbc97a992e27cd8e31ad3d28de23cbc3578e06`;
- html/HTMLWriter.jl SHA256
  `72b261cbef5e06e9edc4159c038d740b5f5372134f9d75db06eeb35b894b29dd`;
- selected Coree431/Runner1acc docs/make.jl modules/sitename lines reread via
  immutable git show. Их новые commit identities не выдумываются.

Полный installed tree/native/cache identity остаётся непроверенным. Все остальные
D2 границы приняты R2 и сохраняются: default doctest=true; explicit pilot before-
import guards; complete pages; byte-exact operator mapping; fixed light;
bounded argv/drains/receipts; no schema/framework/dependency/CSP change.
Nested/dynamic-docstring/import/assets/license/cache/fresh-admission evidence
остаётся обязательным BUILD prerequisite. Source I может реализовывать профиль
и blocked preflight; BUILD/release не разрешены этой коррекцией.

Original broad source scan5,523,762B против4MiB остаётся FAILED_RESOURCE_CAP.
Отдельная D2 continuation сохраняет собственные1,142,390B и grant. Этот D3 —
ещё один отдельный ограниченный source-only correction envelope≤10min,
1CPU/1GiB,read≤512KiB,output≤48KiB; не retroactive PASS предыдущих этапов.
Названные D3 чтения: documents47,497B×2,HTMLWriter113,880B×2,
R2report15,636B×2, prior artifacts47,233B×1, два маленьких owner make с
консервативным reserve8KiB:≤409,451B. Physical I/O/RSS не инструментированы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Operator modules должен быть Module[] | Pinned documents.jl:420, R1 | Source type contract, без runtime | изменить |
| Exact pilot kwargs нуждаются в фиксированном sitename | HTMLWriter825, documents427, selected owner make6 | Render не запускался | изменить |
| Остальные D2 границы/failed resource history сохраняются | R2 и immutable D1/D2 hashes в delta receipt | BUILD prerequisites всё ещё missing | сохранить |

STOP: frozen D3/delta/identity для отдельного high recheck перед medium I.
