# SCI03-M1: независимое high CP_CODE source review

2026-10-19. **CP_CODE APPROVED на production SHA256
`bb3d204378fd7d95691cfd9b58360afc6f48ede1b37fe7a0f6d2a6ff06944915`
с frozen tests `d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79`.**
Блокирующих source findings нет. Это code/source verdict до sole coordinator
GREEN, не утверждение о его результате, native readiness или scientific accuracy.
STOP после report/identity; новых запусков или косвенных grants не создано.

## 1. Sources, RED и фактический diff

Применены принятый D `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7`,
его independent R `fa1311a4bf16f08f6e417590b77b7e6179aa9320907934fbd4496ebc059ca4a9`
и Research owning contract at `3ed8a9f`, file SHA
`61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c`.
До implementation artifacts сверены primary theorem/fields/status/resource
sections, baseline Results33b1 source и frozen literal tests. Затем прочитаны
implementation source/patch/report/identity и original RED evidence. Предыдущие
D/test reviews не заменены текущим code review; новых scientific требований нет.

Owning worktree `/tmp/qcl-sci03-M1-results-worktree`, HEAD/base
`33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`.
Actual status: modified `src/qcl_negf_results/equilibrium.py` и ранее frozen
`tests/test_equilibrium_diagnostics.py`; README unchanged. Production diff
**+86/−5**, tests **+324/−0**. `git diff --check` без сообщений. Actual production
diff SHA совпал с frozen patch. Ни source files, ни Git state рецензент не менял.

| Файл/артефакт | Проверенный SHA256 |
| --- | --- |
| Baseline production at33b1 | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| Candidate production,36563 bytes | `bb3d204378fd7d95691cfd9b58360afc6f48ede1b37fe7a0f6d2a6ff06944915` |
| Candidate tests | `d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79` |
| Production-only patch | `b9eb4c0000597dc725a14dbc8c947e7e0d232378447edb6f18ecd0a4c59df805` |
| Implementation report | `d00f63211e5c38a20ff8df1a279caea279ec4ce4041fd7782fc3c33a50186f53` |
| Implementation identity,5015 bytes | `f795263b4140bb9ae7728fef124959170adc527cb64f948acf5c9ebb0d4fd08d` |
| Unchanged README | `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9` |
| RED receipt | `f685a7460f8c0747b73e5559fb36af44b5a3f7a956f36db38ee18d5dec718fa4` |
| RED original.log | `bc72a87f5cdab8374d7ac719905f10df75ff0ab2699512baea285a1526620e53` |

Author identity отсутствовал при первом чтении и был получен позже; его contents
и SHA сверены до решения. Production/test SHA повторно совпали после чтения.
Local coordinator RED commit `d6e1f18` через `git show` содержит baseline
production3f8e…42e6 и testsd4bb…f79. Receipt непосредственно фиксирует fixture и
harness hashes, command/cwd и resource metrics; этот source check не является
новой проверкой imported producer/runtime. Exact GREEN binding остаётся root.

## 2. Формула → reduction → report

**Наблюдение:** новые accumulators в `equilibrium.py:526–529` — ровно12:
три на raw/normalized state и три на plus/minus side. Existing A/correction
norms переиспользованы, aggregate FDR retained. Никакой новой μ construction,
normalization, replacement stored A или guessed model defaults нет.

| Accepted quantity | Actual symbol/строки | Source verdict |
| --- | --- | --- |
| n,p,c каждого варианта | `delta_n=occupied-f*a`, `delta_p=empty-(1-f)*a`, `sum_norm.add(delta_n+delta_p)`553–565 | Full complex matrices, c не n+p и не forced0 |
| g−,g+,d каждой side | `sn=-1j*sl`, `gamma=sn+1j*sg`; norms `(1-f)*gamma`, `f*gamma`, `sn-f*gamma`569–575 | Sn=−iΣ<, Γ=Sn+Sp; only corresponding side |
| Raw N/P | unchanged539–542 | Stored enabled dictionary+embedding_total ровно один раз, GR†; не fresh map |
| Signed outward flux | unchanged576–580 и current report | Ordered `SG*G<−SL*G>`; signed integral до real/abs; common-z minus сохраняет знак |
| RHS terms/B | `_represented_current_bound`138–188 | J0[g−n+g+p+d(a+c)] отдельно для4 side/variant pairs |

Все новые norms идут через existing `_Norm.add` с той же W, что и прежние
FDR/numbers/flux: `gs/(2*pi)*wE*wk`. Full real+imag entry traversal, никакого
trace-only/diagonal projection нет. W≥0 проверяется существующим guard; wk
не получает второй radial/spin factor. Persisted positive J0 даёт A/m² для
трёх terms и B; norm fields имеют units1. Common relative μ/f один для обеих
versions и sides, E_ref presentation/FD gauge не меняется.

Алгебра:
`SpN−SnP=(1-f)ΓδN−fΓδP−δS(A+δN+δP)`.
Те же ordered products дают source bound через Frobenius+Cauchy. Ни код,
ни report не требуют PSD, Hermiticity, commutation, N+P=A или Σ-FDR. Отдельное
измерение δS сохранено. Производственный signed current не заменён B/abs
integrand; equilibrium не выводится из balance двух сторон.

Implementation совпадает с независимо проверенным noncommuting 2×2/finite-t
oracle. M1_01/02 проверяют сами coefficients/terms, а не только |J|≤B;
off-centered fixture различает f/(1−f), imaginary mutation различает full
complex norm/ImJ. R1 runtime exact-zero fragility устранена testsv2 и код её
не маскирует: вычисляет реальные полные defects, без closure shortcut.

## 3. Статусы, zero и finite arithmetic

`_represented_current_bound:147–180` определяет available μ по existing
`mu.value_relative_eV is not None`; current `_fit_mu` устанавливает value
только на measured applicable path. При missing/unavailable μ helper наследует
её exact status/reason. Dependent norm scalars и все bounds/terms остаются
None; `.magnitude()` для пустых dependent accumulators не вызывается.
Это предшествует любому zero handling. A/correction absolute rows measured
независимо от μ и не подменяются relative ratio. Empty spectrum/missing context/
finite drive/unequal LO/e–e unsupported/algorithm_limit не превращаются в pass0.

При defined μ literal zero side matrices дают g−=g+=d=0 и finite products/B0,
без division/J, denominator floor или donor normalization. Нулевой rounded
norm не выдаётся за certified exact/scientific zero. Existing correction ratio
numerators/denominators и zero/undefined branches не изменены.

Guard chain покрывает каждый новый scalar intermediate: finite magnitudes
от `_Norm`, g*n, g*p, a+c, d*(a+c), каждую J0 conversion и compensated sum
через `_finite`/`_Sum`. Matrix-derived nonfinite defects/coefficients
отвергаются `_Norm.add`. Поэтому ни overflow, ни nonfinite sum не дают measured
Inf/null success. M1_06 имеет конечные signed currents при переполнении RHS,
и actual helper должен отвергнуть именно новый overflowing term; source chain
это предусматривает. Исполненное подтверждение ещё впереди.

Namespace/keys/status/units/scope точно соответствуют accepted A.3. Поле
arithmetic_error_status=not_measured, arithmetic_error_bound=None и scope
`represented exact-arithmetic complex trace; no acceptance` сохранены. Код
не создаёт outward-rounded enclosure и не утверждает rigorous error bound
Float64 trace. Нет нового pass/accepted/threshold/εJ_abs/H/criteria registry.

## 4. Allocation census, I/O и compatibility

Новая работа встроена в pass2; actual diff не содержит новых `read_complex`,
StateReader selections, `blocks()` проходов, `@`/GEMM или дополнительных
persisted datasets. Side matrices читаются для прежних signed currents и
переиспользуются для coefficients. State defects освобождаются до side reads,
Sn/Γ до existing current GEMMs. Public signature/imports и old fields/schema
не менялись; новый helper private, новый namespace additive.

**Независимый incremental numeric-buffer census:** пусть C=16·tile·Nb² bytes.

| Фаза | Дополнительный peak поверх прежнего пути |
| --- | --- |
| State norms | δN+δP плюс product либо D temporary:≤3C; затем explicit del |
| Side norms | Sn+Γ и fΓ/subtraction temporaries:≤4C; затем explicit del |
| Common f/1−f | f view existing fermi;≤два 8·tile vectors при reassignment,≤C при Nb≥1 |
| `_finite`/norm scratch | Boolean finite array≤C/16 и bounded real-plane ravel copy≤C/2; укладываются в оставшийся margin |

Следовательно extra8C allowance source-консервативен для добавленных numeric
arrays. Baseline24C не объявляется заново независимо измеренным total RSS.
Новые `_Norm`/dict objects имеют конечное число; reserve4KiB+8KiB — documented
scratch/report accounting, не точный Python heap/RSS certificate. HDF caches,
OS I/O и transient RSS по-прежнему вне numerical workspace scope.

Forecast до vector/matrix payload reads сохраняет старые fixed terms,
добавляет12288 bytes и увеличивает24→32complex slots. Full-plane minimum/tile
selection и logical byte forecast используют новые значения; недостаточная
workspace отвергается до полного plane, а не diagonal fallback. Limits,
single-read/chunk caps и maximum_io_bytes не повышены. При меньшем tile растёт
coordinate/read-call overhead; physical callback guard остаётся authority.

12 norms означают O(12NE·Nk·Nb²) дополнительных entry visits; Python loop
wall cost не измерен и не объявлен несущественным. Постобработка не хранит
unbounded terms list, новых scientific datasets/solve нет.

Fixed report namespace конечен; existing entire-report JSON allow_nan=False
и64KiB default cap сохранены. Runtime overflow/cap fail до возврата отчёта,
без truncation. Literal tests проверяют namespace≤8KiB и entire report≤64KiB,
M1_07 — refusal на old-size cap; их новый GREEN результат ещё не известен.
Full old semantic compatibility требует того же sole GREEN; последние биты/
budget counters при изменении tile не обещаны битово идентичными.

README не изменён этим этапом и зарезервирован отдельному writer. Описание
additive namespace/Research link остаётся publication documentation gate
координатора; его выполнение этим code review не заявляется.

## 5. Sole RED evidence и границы проверки

`/tmp/qcl-SCI03-M1-RED-1/receipt.json`/`original.log` hashes выше совпали.
Raw35438bytes, capture complete, no guard_error/stop_reason/overrun; exit1,
wall12.212s, pytest11.51s, sampled RSS89419776B, ownedTMP15534234B.
Это сохранённый coordinator execution; reviewer ничего не запускал. Sampling
метрики не hard quota/transient peak certificate.

| Cases в raw | Причина | Что подтверждено |
| --- | --- | --- |
| M1_01 False/True, M1_02, M1_03 | Missing namespace at test614 | New feature отсутствовала; предшествующие known-μ/defined-μ checks пройдены |
| M1_04 все6 mutations | Missing namespace at614 | Exact μ status/reason/None checks до namespace пройдены |
| M1_05 и M1_07 | Missing namespace at614 | Новые read-count/cap assertions ещё не достигнуты |
| M1_06 | DID NOT RAISE ContractError at183 | Old implementation не проверяла overflowing bound |

12+1=13 expected failures,38passes из51. Полный failure-summary/trace text
согласуется с source classification; unexpected mechanisms не обнаружены.
Passes включают baseline36 и M1_08/09 healthy controls в этом RED. Это не
pass новых coefficient rows, overflow rejection/read-count/cap enforcement.

Все новые rows/oracles, status branches, guards и old regression поведения
должны получить evidence единственным уже разрешённым root GREEN после exact
source binding. Этот R не расходует оставшийся call и не разрешает третий.
Campaign M1 used1/2, remaining1; SCI05/08 C08 remains8/8. Fresh SCBA/Poisson,
native final data/admission, physical accuracy и S1 scientific acceptance
не входят в этот verdict.

## 6. Scope и итоговая таблица

Source-only shell/Git text/hash/diff reads по explicit paths. Применены
qcl-physics-audit/results-analysis. Imports/parsers/collection/tests/HDF/Julia/
solver/build/install/network/server/source edits/Git mutations/children=0.
Записаны только этот report и identity; root/checkpoint не изменялись.
Envelope≤25min/1CPU/2GiB/read4MiB/output96KiB. С повторными полными inputs
sed/rg/diff/hash conservative logical text reads<2MiB; physical/kernel/Git
object I/O не инструментирован. Broad root execution search отсутствует;
ровно названные RED log/receipt читались как нужные primary evidence.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| 12norm implementation соответствует SCI03 RHS | Source526–575, helper138–188, accepted theorem/literal table | Source verdict, GREEN ещё нет | сохранить |
| Common μ/full complex/W/J0/signs сохранены | Existing raw/flux paths unchanged; separate norms/source mapping | Stored Σ-only, не fresh map | сохранить |
| Missing/overflow/zero не дают ложного pass | Null inheritance, finite product/conversion/sum guards | Runtime подтверждение впереди; arithmetic enclosure unknown | сохранить |
| Не добавлены datasets/pass/GEMM/unbounded arrays | Exact patch + source lifetime census, workspace32slots+12KiB | Source forecast не total-RSS measurement | сохранить |
| Actual RED различил missing feature | Exact receipt/log13fail38pass и all13 classification | Новые rows/readcounts/caps пока не испытаны | дополнительно измерить |
| Feature scientific/native acceptance установлена | Нет final arrays/run/plan/admission/εJ_abs/H | Stored measurement и synthetic tests недостаточны | данных недостаточно |

**CP_CODE APPROVED exact bb3d2043…6944915/tests d4bb720f…f87f79. STOP перед
root sole GREEN; execution/acceptance сверх существующего finite scope нет.**
