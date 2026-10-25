# SCI05-C1 v3 — CPP1 correction, frozen source packet

2026-10-19. Один corrective I round по shared max2 code rounds, finite envelope
30 min / 1 CPU / 2 GiB / output128 KiB. Использованы qcl-physics-audit и
receiving-code-review: сначала прочитан полный CPP1 и проверены module/source
locators, затем применены узкие исправления. Julia/runtime/tests не выполнялись.

Baseline isolated Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, worktree `/tmp/qcl-sci05-core-worktree`.
Ровно6 разрешённых путей: src/QCLNEGF.jl, четыре прежних numerics src,
новый test/numerics/final_audit_evidence.jl. Protected main/root/DEV05 не менялись.
Original v2 patch/report/identity и failed CPP1 review сохранены byte-identical;
additional copies `/tmp/qcl-sci05-preserved-CPP1-*` перечислены в identity.

## F1/F2: проверка и исправление связности

Подтверждено, что poisson.jl принадлежит QCLReferenceOperators, validation.jl —
QCLNumerics, а новый private symbol отсутствовал в explicit import. В existing
QCLNumerics import ..QCLReferenceOperators добавлена только строка
`_solve_periodic_poisson_with_diagnostics,`. Public exports/aliases/types/API
не менялись. Это единственный delta src/QCLNEGF.jl и единственное production
изменение относительно v2; SHA четырёх numerics files совпали с frozen v2.

В новом test добавлены явные owning aliases QN=QCLNEGF.QCLNumerics и
QR=QCLNEGF.QCLReferenceOperators. Evidence/record helpers вызываются через QN,
private Poisson helper — через QR. BN оставлен только для существовавших root
aliases _dyson_residual и _solution_validation_limits; public API остаётся прежним.
Никаких private exports ради tests или dynamic namespace lookup не добавлено.

## F3: independent Poisson oracle graph

Полностью удалён широкий factor-two expected band. Повторно использован
accepted O08-03 D2 `/tmp/qcl-final-ug-design-v2.md` §5 и его independent review:
literal M=[2,-1,-1;...], input-side rounded qL, actual rounded n и checked
uniform h/ε/donor/λ coefficients; literal b=λ(n−ND), zero-mean exact U, exact ζ
для frozen v64, Q4=[M/4 v;vᵀ0] и inverse norm4/3. Direct h2/ε4 fixture и actual
source h/ε1 public validation fixture имеют independently checked exact row-sums
4qL; те же Q4 eigenvalues и operation counts сохраняются. Physical acceptance
thresholds не меняются. Generalization — только homogeneous scaling accepted
constant-coefficient3-cell algebra, без нового forward accuracy предположения.

384-bit directed scalar intervals (не product norm/solve) разворачивают literal
L*observedUp−b, independent raw numerator/RHS/additive denominator, signed and
absolute neutrality, gauge и analytic U/ζ. Сохранены γ3 b formation и γ32
row/dot/norm bounds. Full Q4 residual измеряется по returned floats без второго
solve; и zero-mean forward, и Q4 forward обязаны FIT retained γ32 short cap.
Неправильный output не может увеличить residual enclosure и получить pass.
Numerator не восстанавливается через ratio*denominator. Нет guessed LAPACK
accuracy или нового physical tolerance. Около нуля absolute interval применим.

Observed-path mutants меняют returned Up (wrong sign, /4 missing-h² analogue,
*1.1 reviewer counterexample, constant gauge shift), либо получают новый product
output при altered density, сохраняя original expected reference. Nonneutral
positive-residual branch отдельно отвергает factor2 numerator, ratio и совместную
factor2 подмену через тот же literal predicate, чтобы zero cancellation roundoff
не маскировал tampering. Healthy/neutral/nonneutral controls сохранены.

Public validate_solution fixture теперь использует actual published U и
nonconstant positive n. Expected source h получается из принятой binary64
30nm/10nm/3 chain и сверяется с actual grids; ε=1 обеспечивает тот же frozen
qL literal, отдельный guard фиксирует qL hex. Independent reference строится
перед tiny direct Poisson call, затем его measured forward enclosure ограничивает
actual validate_solution report.r_U и record.poisson.rU_max. Mixed step
α*(Up−U) и отдельная public validation с changed density обязаны нарушать тот же
raw-rU enclosure. Это больше не транспорт synthetic r_U=0. Scope остаётся
manufactured functional/source evidence, не aligned device/SCBA solution.

## Проверки и ограничения

Успешен `git diff --check`; exact permitted paths/base/input/file hashes проверены.
Protected src/tests diff к main HEAD пуст; production main diff к f5 пуст;
existing tracked tests в isolated worktree не изменены. Четыре numerics src
byte-identical v2 — old arithmetic/status clarification/metrics не изменились.
Test aggregator auto-discovers новый file. Source bytes/hash proof — в identity.

No Julia/import/runtime/tests/build/setup/solver/native/server/Gitcommit/push.
C08 calls=0. Directed oracle код только написан/прочитан; ни interval graph,
ни source h guard, ни product mutation assertions пока не исполнялись.
F1–F3 addressed source candidate не является independent CPP2 verdict или
runtime GREEN; следующий gate — независимый full CPP2, затем отдельный
coordinator-only bounded runtime grant. Scientific acceptance не установлена.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 private symbol связан с owning module | Один explicit private import | Runtime не измерен | изменить |
| F2 новые tests используют owning namespace | Явные QN/QR calls, без exports | Import/test исполнение не выполнялось | изменить |
| F3 literal raw residual/gauge/rU oracle подготовлен | Accepted Q4/γ derivations + new predicates/mutants | CPP2 и numerical receipt отсутствуют | дополнительно измерить |
| Production arithmetic/schema/physics сохранены | Четыре numerics SHA совпали с v2, module delta только import | Source-only comparison | сохранить |
| Protected state/v2/failed review сохранены | Immutable hashes/status proof | Concurrent root changes вне writer | сохранить |
| CPP2/runtime/scientific acceptance достигнута | Такого evidence нет | Gate остаётся открытым | данных недостаточно |

Patch SHA256 `305675ad283267034a3b3873d1cfb8ff010f7d5a7b7885c523f388e3483ac71e`.
Identity SHA256 `a76ec63745bd73b972a74f3e90bba496240bdad81429c57d716c7a063e40ca3b`.
STOP после freeze. Никакой следующий correction/runtime cycle не начат.
