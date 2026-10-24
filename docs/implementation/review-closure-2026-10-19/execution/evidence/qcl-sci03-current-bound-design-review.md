# Независимое SCI03-5.3 CP-DESIGN review

2026-10-19. Роль R high, source-only. **APPROVED для представленного additive measurement design. Блокирующих замечаний к математике и измерительному контракту не обнаружено.** Это решение о проекте измерения, а не разрешение на I, C08, scientific/native execution, CP-SCI READY или scientific acceptance. После записи отчёта — STOP.

Проверяемый проект: `/tmp/qcl-sci03-current-bound-design.md`, 39159 bytes,
SHA256 `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7`.
Companion identity SHA256
`0f464d53d206ea168e5f723ffc1b011644e1902d79a3e58dcaa4d1bca9e1f7bf`.
Проект и identity прочитаны после первичных owning формул и Results reducer;
готовый диагноз других рецензентов не использовался. Дочерние агенты не создавались.

## 1. Исходники, порядок проверки и границы

Рабочий root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`.
`git ls-tree HEAD` выбран как composition authority, не индекс:

| Owner | Gitlink root HEAD | Фактический checkout при начале R |
| --- | --- | --- |
| Core | `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c` | `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee` |
| Runner | `9378396a3681c1eddf2c62f16674834fc4465583` | `1acc165650fd4f4c2d49605cc679f90e3f6fcdae` |
| Research | `1eacefcd81a50e245ea9da74a0b717b33818c61e` | совпал |
| Results | `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae` | `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`, component clean |

Root `git status --short` показал изменённые Core/Runner/Results gitlinks,
`execution/checkpoint.json` и concurrent untracked reports/identities/tests
DEV07/SCI05/DOC04/OPS04. Они не менялись рецензентом. Старый source snapshot
автора, в котором Core/Runner ещё совпадали с root gitlinks, сохраняется как
исторический receipt. Owning файлы, нужные этому review, совпали по SHA с D;
изменённый состав root не выдаётся за опубликованный/научно принятый release.

До чтения D: прочитаны AGENTS, architecture, применимый workflow и навыки
qcl-physics-audit/results-analysis; P1 `science.md` SCI03/SCI06 и S1 permissions;
published Research §§2–3, 5.3; actual Results `equilibrium.py`:
`_Norm`, `_ratio`, `_applicability`, `_fit_mu`, scales, W и оба streaming passes.
Затем прочитаны D/identity, native StateReader guards, existing synthetic tests,
Core grids/scales/current definitions и contributing rules. В компонентных
Results/Research корнях AGENTS.md отсутствуют; CONTRIBUTING применены.

| Источник | SHA256, проверен в R |
| --- | --- |
| `docs/architecture.md` | `8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7` |
| `docs/implementation/review-closure-2026-10-19/science.md` | `0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a` |
| `docs/implementation/review-closure-2026-10-19/operator-permissions.md` | `4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0` |
| Research `docs/equilibrium-measurement-contract.md` | `758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f` |
| Results `src/qcl_negf_results/equilibrium.py` | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| Results `src/qcl_negf_results/state.py` | `335e67678120fd0c8e222fcb5e937b277ccadac35303fca2250c9f345983b477` |
| Results `tests/test_equilibrium_diagnostics.py` | `ce35954b2503d7a910048d6e95bcc6b6b0c88eea40f8a018dc13bdf8ca4bbad0` |
| Core `src/physics/observables.jl` | `b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f` |
| Core `src/numerics/reference/grids.jl` | `71c4cff98cbefb834eea818067549dc150cb0cd18141854f27dfbd549862d18e` |
| Core `src/domain/scaling.jl` | `2049ea6638da871c406718dad9f1aa4eb5cee68f4ce8941a8270e050dd7eb9f0` |

Нет immutable input arrays, archive hash, run/attempt/frozen-plan bytes. Новый
numeric coefficient, B, source-data consistency или scientific result не измерен.
Первичные статьи в этом R не загружались/парсились: attribution используется
из опубликованного Research contract с этим SHA. Сам bound проверен независимым
элементарным выводом, не ссылкой на авторитет статьи или согласие рецензентов.

## 2. Математика и конвенции: сохранить

**Наблюдение.** Results `diagnose_stored_equilibrium` определяет
`Nraw=-i GR SLtotal GR†`, `Praw=i GR SGtotal GR†`,
`Nnorm=-i GL`, `Pnorm=i GG`, а boundary trace равен
`Tr(SG GL-SL GG)`. Stored scattering dictionary плюс `embedding_total` входит
в raw ровно один раз; plus/minus читаются отдельно. Полная матрица A остаётся
stored reference, её не подменяют повторно вычисленной матрицей.

**Независимый вывод.** При `SL=i Sn`, `SG=-i Sp`, `GL=iN`, `GG=-iP` trace
равен `Tr(Sp N-Sn P)`, без дополнительного i или минуса. Для scalar f и
`Sn=fΓ+δS`, `Sp=(1-f)Γ-δS`, `N=fA+δN`, `P=(1-f)A+δP` произведения дают

```
Sp N-Sn P = (1-f)ΓδN - fΓδP - δS(A+δN+δP).
```

Сокращаются одинаково упорядоченные ΓA. Ни Hermiticity/PSD, ни коммутирование,
ни `N+P=A`, ни Σ-FDR здесь не требуются. Для любых complex X,Y:
`|Tr XY| <= ||X||F ||Y||F`; transpose второго набора элементов сохраняет
Frobenius norm. Triangle и Cauchy для неотрицательного W дают точно
published §5.3 и D §2:

```
|J_s,v^complex| <= J0*(g_s^-*n_v + g_s^+*p_v + d_s*(a+c_v)),
c_v=||δN_v+δP_v||W.
```

Это верно для каждой raw/normalized стороны отдельно. Real/imag части также
ограничены этим B. Minus common-z меняет знак текущего outward тока, а модуль
и B сохраняются. Balance двух ненулевых потоков не используется как J=0.

**Единицы/мера.** Actual reader W=`gs/(2π)*wE*wk`; Core annular wk уже имеет
radial factor. Ни второй spin, ни второй radial factor не добавлены. Все
новые нормы — dimensionless (`1`), три SI terms и B — `A/m^2` с positive
persisted J0. Raw reconstruction и эти scalar/norm reductions не требуют
нового matrix product. Две версии используют одну existing fitted relative μ.

**Минимальность.** 12 новых norms достаточны для точного измерения выбранной
RHS: по n,p,c на вариант и g−,g+,d на сторону; a и absolute correction norms
уже имеются. Aggregate FDR даёт n²+p², но не отдельные n,p; он не заменяет их.
Минимальность относится к опубликованной факторизации, а не к единственной
возможной математической оценке: например `||N+P||W` позволила бы иную, более
тесную третью оценку. Это не требуется текущим ticket и не повод менять RHS.

## 3. Статусы, near-zero, округление: сохранить

D §5 правильно наследует точные μ status/reason до любых zero shortcuts.
Missing context, finite drive, unsupported e–e closure, unequal/nonthermal LO,
negative spectral-number weights, empty spectrum и algorithm_limit не дают
measured B=0. Null-gated values включают все terms. A и normalization corrections
μ не требуют и могут оставаться measured. Это согласуется с `_fit_mu` и
existing unavailable FDR rows, а не с локальным `_ratio(0,0)` convention.

При defined μ и finite factors literal zero term допустим; B=0 не требует
division/J, floor или donor normalization. Rounded zero, underflow и малый B
не объявляются сертифицированным zero-current/physical error. Все overflow
product/sum/conversion должны оставаться invalid_data; measured Inf недопустим.

RHS — bound exact-arithmetic trace на фиксированном represented domain при
том же f. Float64 `_Norm`, exp, reconstruction products и scalar accumulation
не дают outward-rounded enclosure. D явно оставляет arithmetic_error_bound=null,
status=not_measured и не выдаёт fixture engineering tolerance за scientific
accuracy. Finite εJ_abs, tails/domain/basis, fixed-point/nonlinear conditioning,
native truth и эксперимент остаются неизвестными. Это достаточное ограничение
силы утверждения; новых thresholds/source-acceptance rules не введено.

## 4. Независимая ручная проверка 2×2 oracle

В D §7.1 `X²=Y²=I`, `Tr X=Tr Y=Tr XY=0`, `||X||F²=||Y||F²=2`.
Прямое суммирование entries даёт:

```
Tr Γplus = Tr Γminus = 3/4
||Γplus||F²=11/32; ||Γminus||F²=21/64
Tr(Γplus X)=0; Tr(Γplus Y)=1/4
Tr(Γminus X)=Tr(Γminus Y)=1/8.
```

Γplus/X и Γminus/Y не коммутируют. Поэтому этот пример не опирается на
diagonal/commuting simplification. При `M=3/(8π)`,
`L=(7/4)Mε`, `R=(13/4)Mε²`, ε=1/128 получены независимо:

| Величина при f=1/2 | Проверенное literal expectation |
| --- | --- |
| a² | 8M |
| g−²=g+² | plus 11M/128; minus 21M/256 |
| d² | 2R на обеих сторонах |
| nraw²=praw², craw² | 4R, 0 |
| nnorm²=pnorm², cnorm² | 10R, 20R |
| occupied/empty correction² | 2R, 18R |
| raw outward J на обеих сторонах | J0 L/4 = J0 M·7/2048 |
| normalized plus outward J | J0(−L/8−2R)=−J0 M·69/32768 |
| normalized minus outward J | J0(L/8−6R)=J0 M·17/32768 |

Ток получен как `Γ(N−P)/2−ΔS(N+P)`, с trace после ordered products. Это
также непосредственно проверяет правильный знак Σ-FDR term. Нормы D §7.1
и обе упрощённые формулы Braw/Bnorm согласуются с этими entries.

При `t=f(μhat)−1/2` independently проверены nraw²=praw²=4R+8t²M,
nnorm²=pnorm²=10R+8t²M, c/corrections неизменны,
dplus²=2R+t²(11/32)M,
dminus²=2R−tL/4+t²(21/64)M и g±²=(1/2±t)²gM.
Cross term в dminus следует из `Tr(YΓminus)=1/8`; он не пропущен.
Поэтому finite fitted μ можно учитывать без искусственного ослабления fit.

D §7.2 отдельно различает swap f/(1−f) off-centered f=1/4 control; основной
симметричный f=1/2 пример один этот swap не обнаруживает. При imaginary
`Nnorm += iρI` direct trace даёт `Im J=J0·3ρM/8`, а n²/c² растут на
2ρ²M. Контроль complex modulus поэтому нужен и математически корректен.

Required negative matrix покрывает zero boundary vs missing boundary,
missing μ/context, off-diagonal/imaginary loss, omitted d, replaced c=n+p,
false c=0, wrong W/f powers, unequal k planes/weights, side reuse/transposition,
raw embedding double count, invalid provenance/axes/weights, overflow и budgets.
Проверка exact scalar terms, а не одной inequality, защищает от ошибочно
завышенного B. Expected arithmetic не импортирует product `_Norm`/FD/builder;
shared encoding/provenance остаётся явно признанным пределом независимости.

## 5. Стоимость и совместимость: допустимый дизайн, implementation ещё не проверена

Actual pass2 уже читает A/GR/GL/GG и обе side SL/SG, необходимые для всех
новых scalar norms. D не добавляет dataset inventory, третий проход, новый μ
fit или O(Nb³) product. 12 streaming norms дают O(12 NE Nk Nb²) entries;
finite workspace/report защищены existing limits, цена Python loops не названа
пренебрежимой. Source-only evidence этого достаточно для выполнимого design.

Forecast 24→32 complex tile slots и bounded fixed reserve — проектирование,
не доказанная allocation census. D уже требует проверить actual liveness,
O(tile) f vectors, scalar metadata и full-plane minimum до I completion.
Уменьшение tile увеличивает coordinate/read-call overhead: D сохраняет total
physical I/O guard и пересчёт logical forecast, а не обещает byte-identical I/O.
Report cap не повышается; нехватка cap должна завершаться budget_exceeded.

Один additive namespace с собственной version, прежней public signature и
сохранённой семантикой old rows соответствует просмотренному source. Поиск
в owning Results/Contracts не обнаружил strict schema именно для
`qcl-negf-stored-equilibrium-diagnostics-v1`; закрытые schemas fresh audit и
native payload не являются schema этого derived report.

Неблокирующие implementation clarifications, не новые scientific условия:

1. Формулировку D §5 «existing keys/values/schema остаются» читать как сохранение
   полей и смысла. Изменившаяся tile длина может изменить порядок existing
   aggregate FDR LASSQ и последние биты; budgets закономерно меняются. Не
   обещать побитовую инвариантность всех old values. Проверить old assertions
   с их прежним engineering scope, без расширения допуска под сбой.
2. При known-μ fixture проверять вместе с bracket inclusion его stop_reason,
   width/adjacent-endpoint условие и status. Expected norms при μ из report
   проверяют арифметику выбранного f, а сами по себе не доказывают точность
   μ algorithm. Existing R01 FDR assertion следует сохранить, как уже требует D.
3. 512u max(1,|expected|) в D — предложенная fixture regression policy, не
   доказанный libm bound. В I/R нужна actual operation-chain оценка каждой
   scalar row, finite-t μ accounting и независимые sign/zero controls. Это
   уже включено в D; право поднимать scientific tolerance из него не следует.

Эти пункты не требуют нового математического D: они уточняют проверку будущего
кода в пределах уже записанных D obligations. Implementation approval, actual
workspace/I/O/runtime и mutation-sensitive assertions здесь не заявляются.

## 6. Коллированное решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SCI03 bound корректен без PSD/commutation | Независимое matrix expansion и weighted Cauchy, §2; owning Research §5.3 | Exact represented arithmetic при общем f | сохранить |
| Existing sign/units/weights сохранены | Results 3f8e…42e6 `_Norm`, blocks, boundary trace; Core current/scaling hashes выше | Не physical/native measurement | сохранить |
| 12 новых norms измеряют выбранную RHS отдельно raw/norm, plus/minus | D §§2,5,6 и available pass2 matrices | Не утверждение уникальной глобальной минимальности | сохранить |
| Near-zero/missing/rounding не превращены в pass | D §5 и existing `_fit_mu`/unavailable branches | Arithmetic error enclosure неизвестен | сохранить |
| Literal noncommuting oracle и finite-t table корректны | Ручные entries/traces/norms §4 | Ничего не исполнялось; libm/encoding/runtime остаются checks будущего I | дополнительно измерить |
| Дополнение можно выполнить без нового read pass/product/API argument | Actual streaming loops и fixed-size reducers | Allocation census, external consumer compatibility и exact guards нужны на code review | дополнительно измерить |
| Поле B доказывает thermal/zero-current accuracy устройства | Нет εJ_abs, native arrays и остальных error bounds | Scientific acceptance неизвестна | данных недостаточно |
| Данный R закрывает implementation/native/science READY | Выполнено только source-only review | Не было I/C08/final data/admission | данных недостаточно |

Envelope поручения R: ≤30 min, 1 CPU, 2 GiB, reads≤4 MiB/report≤96 KiB;
фактически не было imports/parsers/HDF reads/Julia/tests/solver/build/network/
server/Git mutations/children. C08 consumption=0. Единственный записанный файл
— этот отчёт в /tmp. Чтение исходников делалось shell cat/sed/rg и SHA; точная
filesystem-byte telemetry отсутствует. Один ранний rg захватил весь execution
subtree шире нужных sections и выдал truncated search results; поэтому фактический
read-byte cap не сертифицирую по размеру показанного текста. Scientific arrays
или архивы не открывались, поиск и чтение ограничились source/evidence corpus.
Это ограничение ресурсного receipt, не научное evidence.

**STOP REVIEW.** Принято только mathematical/source measurement design с exact
D SHA выше. Иного grant этот отчёт не создаёт.
