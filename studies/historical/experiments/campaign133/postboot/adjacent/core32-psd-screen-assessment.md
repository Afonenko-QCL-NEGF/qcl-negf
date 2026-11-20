# Core #32: может ли sign screen прозрачно заменить eigensolve?

Research-only для [issue32](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/issues/32).
Проверен e171/tree742, `optimized/residuals.jl` SHA0f95accf…66404 и
`reference/positivity_diagnostics.jl` SHA796cdde4…d8039; Julia/Pkg/HDF/тестов/
Core edits нет. Измеренные3.33wall/82CPU — уже параллельный residual phase,
не последовательная работа и не цена одних eigenvalues.

**Решение:** дешёвый sufficient zero-residual screen математически возможен
для non-winner blocks. Но Gershgorin/Cholesky **сами по себе ещё не доказывают
точную прозрачность существующему Float64 zheev**, включая INFO/failures.
Ниже — конкретное условие и недостающая предпосылка; blanket skip пока не
обоснован. Это не разрешение ослабить gate или изменить witness.

Фактический PSD metric V3: для уже построенного **тем же порядком операций**
H=Herm(factorX), λhat от zheev, ν=max|λhat|,

`b=64 n eps·max(ν,1)`, `r=max(0,−minλhat−b)/max(ν,floatmin)`.

Keyword floor1e−14 не является этим denominator; construction_scale1
принципиален. Witness содержит также minλhat,ν,absolute/relative defect,
hermiticity defect и budget; min/max bound нельзя выдавать за эти eigenfacts.
Для causality r=max(0,maxλhat(ImΣR))/(opnorm(ΣR)+1e−14), **без PSD budget**.
При нулевом numerator существующий code уже избегает SVD, только если stable
Frobenius norm ΣR конечна; иначе сохраняет reference SVD/failure policy.

**Один bounded sufficient screen.** После прежних finite-X/H checks построить
outward Gershgorin lower bound `g≤λmin(Q)` из real diagonal и upper radii
`Σj≠i |Qij|` (например |Re|+|Im| с upward sums). Q — Hermitian completion
**той же upper triangle**, которую читает zheev; для causality Q=−ImΣR.
Пусть **дополнительно доказано**: old zheev на screened set успешно возвращает
finite eigenvalues с `|λhat_i−λ_i|≤E`. Тогда:

* PSD: `g−E≥−b0`, `b0=64 n eps` ⇒ minλhat≥−b0 и b≥b0 ⇒ old r=0.
  Это certificate нулевого **budget-adjusted residual**, не истинного PSD.
  Более строгий g−E≥0 даёт также нулевой unadjusted negative part.
* Causality: `g−E≥0` ⇒ old numerator0; при прежнем finite-Frobenius условии
  можно вернуть0. Перенос b0 в эту проверку изменил бы raw causality metric.
* Skip допустим лишь когда local chunk witness уже имеет ratio≥0. Возвращённый
  r0 не побеждает strict `>` update; старые winner fields и ties остаются.
  Первый spectral block **каждого chunk** по-прежнему проходит полный eig,
  даже если все blocks safe. Canonical chunk reduction сохраняется.
  Не использовать race-dependent global winner. Raw occupied/unoccupied
  products и их checks не удаляются: normalized GL их не заменяет.

Почему E/успех нельзя предположить: `_PSD_BACKWARD_ERROR_FACTOR=64` —
объявленный allowance acceptance metric, не проверенная bound конкретного
vendor zheev. LAPACK User Guide обозначает свои usual eigenvalue error
estimates как [approximate](https://netlib.org/lapack/lug/node89.html), а
[zheev contract](https://netlib.org/lapack/explore-html/d8/d1c/group__heev_gadbb2b87ce42e51fdaac3228a857a58c8.html)
допускает nonconvergence. Exact-matrix PSD certificate не гарантирует знак
computed near-zero eigenvalue; causality особенно чувствительна, поскольку
её numerator не вычитает allowance. Без qualification этой предпосылки
sound matrix sign screen и сохранение **всех старых machine outcomes** —
разные утверждения. Safe fallback на uncertain блоках обязателен; один
положительный Float Cholesky pivot chain не закрывает этот proof gap.

Validated Cholesky мог бы дать `λmin(Q)≥σmin(L)²−||Q−LL†||` при certified
residual/inverse bounds; просто success/неуспех chol этого не даёт. Даже такой
bound даёт g, но не автоматически E/INFO old eigensolver. Он также дороже
O(n²) Gersh и плохо покрывает semidefinite/rank-deficient blocks. При любой
неопределённости — прежний eig, без clipping/shift/floor changes.

Witness trap: для H=diag(−b0/2,1,1,1,1) ratio0, но minλ и absolute defect
ненулевые. Поэтому даже cert r0 нельзя подставить fake eigenfacts в первый
или выбранный witness. Final per-kind `_scan_positivity_witnesses` имеет
свои first/tie semantics и не входит в предложенный shortcut. Reconstruction
`_scba_physics_witness` должен получать тот же selected matrix/kind/indices.

Возможная стоимость: O(n²) scalar comparisons/abs, без allocation, reuse H;
на miss добавляет проход перед прежним eig. Hit fraction на actual matrices
не измерена; PSD не обязана быть diagonally dominant. Counts6PSD+1causality
на264011 blocks сами по себе не дают wall speedup. До отдельного proof/
qualification и matched evidence сохранять текущие calls; frozen scientific
Core/guards/witnesses не менять ради предполагаемого выигрыша.
