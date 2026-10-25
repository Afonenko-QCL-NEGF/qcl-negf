# SCI12 MATH-I1-DYADIC — source I, восемь private helpers

2026-10-20. Авторская source-only реализация; STOP перед fresh independent high CPP. Не заявляется GREEN, CPP approval, runtime rounding proof, native admission или scientific acceptance.

## Неизменяемый вход

Root HEAD по поручению: 107bac5697b37cf0e47c3feb44883a907837645c. Owning Results worktree `/tmp/qcl-sci12-math-results-worktree`, фактический HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`; recursive submodule status пуст. Рабочий status: два untracked файла — новый module и ранее frozen fixture. Fixture не редактирован, SHA256 `995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d`.

Прочитаны owning architecture, TDD skill, OPS design/high review, MAP design и fixture. RED1 принят как исходный факт поручения: 97 cases = 2 PASS + 95 call-phase Assertion FAIL, 0 ERROR/SKIP/XFAIL/XPASS, product counter 89. Автор повторно его не исполнял. Единственный GREEN90 остаётся у Root после fresh high CPP.

OPS SHA `82a2fbc34cbfc2c6d879a160122362e54dc48586dca4153ae5229ff60ce93a3e`; high review `3f0d7aa11fbc66cb3dbc5e66a0604d22eacb2e6705de165a4e1cc89198bd68d3`; MAP D2 `5473c96d80ad44c1b045008c7fa1aa6055502b05681700d4191c54b46f42db17`.

## Изменение и source walkthrough

Единственный изменённый owning файл: `src/qcl_negf_results/_equilibrium_map_math.py`, 356 строк, 14608 bytes, SHA256 `0750ac7b1f74588278a4a6fd468ecf0a8ce739342383d717d719bc4126cfcdaa`. Полный add-file patch `/tmp/qcl-sci12-math-i1-complete.patch`, SHA256 `d7a3308110eace16bb12e41c3a5cb94eb77e6e2f61a53d52d60a2a37471a7c60`.

- Lines 24–131: owning ContractError, finite scalar primitives, exact non-Bool counts, shape/size/nbytes/native float64/C-contiguous checks, output writeability и alias preflight. Array subclasses/coercible objects не принимаются. Finite scans скалярные, без full bool temporary. Inputs могут быть read-only; output должен быть writable. Alias output с любым input и alias real/imag planes отвергается до output writes; одинаковые left/right inputs разрешены для Gram. Фиксированные ceiling Nb7/Nz192 — engineering preconditions, не новый physical plan.
- Lines 133–169: hat intersection без extrapolation; annulus upper-square minus lower-square без radial/pi/spin factor; cell overlap. Hat nonempty left branch: 2 divisions, 2 multiplies, 7 add/sub; right branch на 2 subtract меньше. Annulus: 2 multiplies + 1 subtract. Empty geometry возвращает известный geometric0.
- Lines 172–231: lengths/caps до payload reads, exact positive uniform cells и coincident full domain, signed two-pointer restriction. Не более Ns+Nt−1 nonempty overlaps, каждый subtract/multiply/add; target width subtract + divide один раз/target. No dense T. Только возвращаемый list ≤192 Python floats/slots; scalar sweep state constant. Неравномерные/сдвинутые domains отвергаются, не исправляются.
- Lines 234–263: `_mac`: p=ar*br,q=ai*bi,r=ar*bi,s=ai*br; real=p−q,imag=r+s; два accumulator adds. Итого 4 multiply + 4 add/sub. Square product i,j,k order, 8b³ primitives, literal0 sums.
- Lines 265–287: rectangular Gram z,a,b order после zero initialization output, conjugation left; 8Qab primitives. Rank deficiency/Gram discrepancy не нормализуются.
- Lines 290–321: observable shape/count preflight; scratch vr/vi два b-length Python lists, суммарно ≤14 floats/slots плюс constant live scalar/tuple state. MAC создаёт transient pair tuple, не matrix scratch. Row contraction M·conj(row), затем row·v: 8b²+8b primitives. Численные byte counts не выдаются за total Python RSS.
- Lines 324–334: actual χ density, L0³ как два multiply, reciprocal один divide, одна scale multiply/output. Полная complex contraction, берётся real part; M не symmetrized, PSD не предполагается.
- Lines 337–356: actual Φ internal bonds; h=−cbar*(2/(ml+mr))/(dx*dx), harmonic masses, затем ((−2*J0)*h)*ImR. На h: 1 mass add, 2 multiply, 2 divide; output 3 multiply. No seam, extra dx, charge/radial/spin factor. Nonunit dx companion fixture остаётся n[8,4], sheet3, J−3 как независимый literal expected, не авторское runtime observation.

До allocation/compute validation проходят metadata/count caps, types/finite inputs, physical positive scales/masses и aliases; loop primitives проверяют finite intermediates. На arithmetic failure outputs могут быть частично записаны; atomic rollback contract не задан. Невалидные metadata/inputs/aliases/read-only outputs отвергаются до output writes.

## Явный arithmetic choice

Восемь frozen signatures не имеют event sink. По согласованному Root уточнению выбран разрешённый OPS error branch: nonzero operands multiplication/division → rounded0 вызывает existing `ContractError(code='invalid_data')` с marker `arithmetic_events.underflow_or_zero_rounding=true` в message. Это fail-closed отказ, не finite0 measurement. Новый global registry/carrier/public API не добавлен. General event-carrying finite measurement остаётся future PAIR/N0 contract. Overflow/nonfinite/zero denominator также invalid_data. `arithmetic_error_status=not_measured`, bound=null остаются semantic limitation; module не формирует report/certificate.

Никаких @/einsum/BLAS/coercion/np.asarray/hidden array expression или reassociation; no generic χΦ residual/norm/interval/eigen/projector/native reader/HDF5 pair. Physical model/scattering/criteria не менялись.

## Проверка и ограничения

Выполнены только source/text/Git/hash reads и создание module + трёх /tmp artifacts. No scripts/import/parser/compiler/numerics/tests/probes/formatter/linter/network/native/CP/READY/index mutations/subagents. git diff --no-index /dev/null module сформировал patch с ожидаемым exit1 (различие), не test failure. SHA fixture после реализации совпал. Первое объединённое чтение design было обрезано tool output; необходимые OPS §§2–3/high review и fixture затем прочитаны отдельными ограниченными chunks. Author не заявляет чтение отсутствующих обрезанных fragments как самостоятельное свидетельство.

Консервативно content read <1MiB; output ограничивался tool token caps, полный физический syscall IO/CPU/RSS не измерялся. Runtime source syntax/import/behavior ещё не проверены согласно фазе. Новый package import не исполнен. Author walkthrough не заменяет независимого CPP.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Восемь helpers представлены exact scalar graph | module SHA + line locators выше | Source-only; fresh independent high CPP впереди | сохранить |
| Frozen fixture сохранён | SHA995b364b… повторно совпал | RED/GREEN не повторялись автором | сохранить |
| χ/Φ, mass harmonic factor, unequal dx не подменены | module density/bond + literal frozen fixture | Runtime behavior ещё не измерено | дополнительно измерить |
| При underflow выдаётся доказанный exact0 | Explicit ContractError marker вместо результата | General event carrier не определён | изменить |
| GREEN/primitive enclosure/native READY/science pass получены | Execution0, missing runtime/native proofs | Не подтверждены этим source I | данных недостаточно |

STOP: передать exact module/patch/fixture hashes fresh independent high CPP. Единственный reserved GREEN90 выполняет Root отдельно.
