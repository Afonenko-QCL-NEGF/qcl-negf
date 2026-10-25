# SCI12-MATH-I1-DYADIC F2 — независимый source-only review

2026-10-20. **F2 принят в узком fixture scope: блокирующих замечаний не найдено.** Обе correction прежнего F review выполнены без изменения literal oracle и product source. Это статическая оценка frozen fixture, не результат collection/RED/GREEN и не разрешение запуска, implementation, native/scientific READY.

Применён `qcl-physics-audit`: отдельно рассмотрены исходный контракт, численные literal controls, plumbing регистрации и граница наблюдаемого свидетельства. Сначала прочитаны вопрос, F2 fixture и первичный OPS/D2 contract; прежний F review и exact F snapshot прочитаны после самостоятельной оценки. Дочерних агентов нет по поручению родителя.

## Неизменяемые входы

Рабочий каталог всех shell calls: `/tmp/qcl-sci12-math-results-worktree`. Фактический Results HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`. Начальный и финальный `git status --short`: только `?? tests/test_equilibrium_map_math.py`; tracked и staged diff пусты. Recursive submodule status этого owning repository пуст. Новый product module отсутствует в source inventory.

| Артефакт | SHA256 |
| --- | --- |
| F2 fixture, 17308 B, 421 lines | `995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d` |
| F2 report | `64f569373d61b7bfa18cae4bd54825655868f355d572e851cc1f416542298e3d` |
| F2 identity | `29ac3e7f4f1d4df7dbfe70cf64280af88df39ed00c29be792d72cc4c3f862243` |
| F2 full new-file patch | `dfaecb1d1a0b194cfa6979a4ca88ed60c516a548513c55bace9c43cc80ea00f4` |
| OPS D1 | `82a2fbc34cbfc2c6d879a160122362e54dc48586dca4153ae5229ff60ce93a3e` |
| OPS independent review | `3f0d7aa11fbc66cb3dbc5e66a0604d22eacb2e6705de165a4e1cc89198bd68d3` |
| MAP D2 | `5473c96d80ad44c1b045008c7fa1aa6055502b05681700d4191c54b46f42db17` |
| Previous F review | `5e59fd2f62500da9de877c601127c9262f310381ff883985300445150d34f0ce` |
| Exact F snapshot | `5e30ef6337374f281681e80e9dc94512043d7f4ee87890f2107d8973f003e1ce` |

## Ответы на вопросы review

**1. Независимые literal controls и ровно восемь helpers — сохранить.** Fixture:18–21 называет только `_hat_area`, `_annulus_square_area`, `_overlap_cell`, `_restrict_cells`, `_complex_matmul`, `_gram`, `_density_from_integrated`, `_bond_from_integrated`, совпадающие с OPS:24–32 и accepted narrow review §2. Нет generic residual/norm/interval/projector, file reader, Core/reference/optimized kernel либо нового validator API. `plane`/`output` создают inputs/buffers; `assert_plane` сравнивает actual с написанными expected. Actual-side композиция hat/annulus/overlap не используется как expected-side oracle.

Адресная ручная проверка сохраняет OPS/D2 конвенции: clips hat 1/8 и3/8; signed partitions3/4+3+9/4=6; annulus partial27/16 и13/16, weighted numerator53/8; spatial17/4 с полосами1/4 и3/2; restriction[2,4] и signed cancellation; AB=[[1,i],[2i,2]], A†A=[[1,i],[-i,5]]; Gram diag(1,4), rank1 и rectangular missing-subspace controls. Density rows(1,±i) дают forms4,2 и при L0=2 outputs1/2,1/4. Coherence/conjugation/unitary и unequal-dx companion различают J−3/0/+3, χ-density[8,4], sheet3, wrong χ bond−12 и wrong Φ sheet3/4. Expected values не вычисляются tested helpers, BLAS, `@`, compiler или arithmetic script. Приёмка всех возможных численных inputs из этих примеров не следует.

**2. Missing API отделён от import/source failures — сохранить.** Fixture:39–51 проверяет actual package origin, найденный spec origin и imported candidate origin в setup; `import_module` и `find_spec` не окружены broad catch. Wrong package/path, dependency и module import exceptions остаются setup ERROR. Отсутствующий spec возвращает только `_CallPhaseAPI(None)`. В `__getattr__`:30–36 нет fabricated result/callable: возвращается настоящий imported helper либо named AssertionError `NEW_API_MISSING` во время test-call attribute lookup. Отсутствующий callable при успешно импортированном module также даёт call-phase assertion. Это test gateway, product stub отсутствует.

В negative tests `pytest.raises(contract_error)` не поглощает missing-API AssertionError: существующий primary source `components/qcl-negf-contracts/src/qcl_negf_contracts/messages.py:17` определяет `ContractError(ValueError)`, не AssertionError. Никакие missing dependency errors не переименовываются в API absence. Неожиданное исключение будущего module-level `__getattr__` при lookup тоже не перехватывается; фактический traceback должен сохраняться. Static source selection не доказывает будущий runtime import graph.

**3. Legitimate cap-before-read Sequence control — сохранить.** OPS:19,27,51 задаёт Sequence inputs, максимум192 cells и dimension/count checks до allocation/range/read. Fixture:400–421 реализует finite legal `__len__`194/193, `Sequence` ABC с требуемыми `__len__`/`__getitem__`; нет counterfeit ndarray shape или больших allocations. Получается193 source cells при одном target cell: cap можно отвергнуть только по metadata. `__getitem__` считает любой payload доступ и поднимает sentinel AssertionError; default Sequence iteration также идёт через него. Ожидаемый ContractError плюс оба нулевых counter не позволяют скрыть прочитанный payload даже если реализация перехватит sentinel и затем откажет.

Control обосновывает один early cell-cap guard. Он не покрывает все ndarray shape-products, target-only cap branches, Python integer multiplication, общий RSS/allocator или все allocations реализации. Эти свойства остаются отдельным source-I obligation: Python-int counts/products, owning cap и `min(sys.maxsize,limit)` до allocation/range/read, без int64 wrap/implicit copy. Sentinel object легитимен именно для этой metadata-first отрицательной проверки; его payload намеренно недоступен, это не положительный numerical input.

**4. 97=2+95 и ожидаемые стадии — статически правдоподобно, runtime неизвестен.** Ручной source census:27 test functions. Parametric functions дают8+7+4+4+6+5+14+8+(4×2)+7+10=81 cases;16 singleton functions дают16. Из97 два singleton literal controls не зависят от `api`, остальные95 обращаются к API из тела test-call. При absent module и корректном prepared runtime каждый из95 должен остановиться AssertionError `NEW_API_MISSING`;2 literal controls должны пройти. Прогноз **2 PASS +95 assertion FAIL +0 setup ERROR** условен: правильные selected packages, установленные совместимые зависимости/pytest/NumPy и нормальные collection/setup нужны. При missing contracts package, foreign Results, dependency/import/source error или иных environment failures setup ERROR ожидаем и не должен переписываться в structural API RED. Collection/count/status здесь не измерены.

## Регрессия относительно exact F

Текстовый `diff -u` F→F2 содержит только import `Sequence`, новый `_CallPhaseAPI`, перенос присутствия API из setup в attribute lookup и новый cap case. Старые inputs/expected literals/assertions/negative predicates не изменены. Полный patch имеет заголовок нового файла421lines и тот же новый footer. Source-only review не применял patch и не вызывал Python parser.

Два прежних blocking request закрыты на уровне исходника. Статических blockers для frozen F2 нет. Это не all-guards coverage: будущая implementation/source review и отдельно порученное инженерное исполнение сохраняют собственные gates.

## Учёт и границы

Только read-only Git, чтение текста, SHA/size/source inventory и два новых `/tmp` review outputs. Tests/imports/parsers/compiler/math/runtime/scripts/network/solver/HDF5/benchmarks/native/CI0; product/index/CP/source writes0. Прочитаны архитектура, skill и owning CONTRIBUTING/pyproject; поиск contracts path дал harmless missing-directory diagnostic для несуществующего `packages`, затем найден primary class в `components`. Это не test failure. Консервативный source-content charge меньше1MiB, deliverables меньше64KiB; CPU/RSS/physicalIO не измерялись и hard resource enforcement не заявлен. Текущие model/criteria/C08 или scientific readiness данным review не меняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F2 закрывает две source corrections F | Exact F→F2 diff; fixture30–51,400–421 | Исполнение0 | сохранить |
| Oracle независим и ограничен accepted8helpers | HELPERS18–21, literal assertions74–397, OPS/D2 | Не полный proof implementation | сохранить |
| Len cap проверяется до payload | Sequence metadata194/193 и sentinel counters | Только source-cell-cap branch; не ndarray overflow/RSS | сохранить |
| RED2PASS/95FAIL/0ERROR уже наблюдён | Только manual97case census и stage reasoning | Runtime/collection не запускались | данных недостаточно |
| Full guards/native/scientific READY получены | Новых runtime/science artifacts нет | Отдельные source/runtime/native/science gates | данных недостаточно |

STOP после source-only review. Никакого разрешения Root RED или implementation этот отчёт не выдаёт.
