# Final postboot report: independent scientific review

**APPROVE / GREEN** научного содержания draft
`final-postboot-report.md`, точный SHA256
**ed34d4344cb6d265872e13ce62f47486863c2944421b38667bed60a82665f942**.
Научных blockers не обнаружено. Publication refs следующего snapshot ещё
могут быть добавлены; эта bookkeeping работа сама по себе verdict не блокирует.
Draft reviewer не редактировал. Только чтение малых summaries/CSV/audit JSON/
reviews/source notes и scalar arithmetic; Julia/Pkg/Φ/μ-fit/HDF arrays,
новых performance measurements и продолжения расчётов не было.

Проверенные опоры: coarse `native-bias1mV-result.md`; fine case0 summary
и29rows case1; warm128 result/replay audit; final FD review
`native-bias1mV-FDseed128-max26-result.md`
SHAc3256c15f63b47f02c1fdc2027495deb1a4c4e0f58fdb28a3db8a5a57990a624,
его audit JSON3465881af6edfcec17161435774f1133c4f8a9e5f75873146fe34f97ab17a305;
Core32 benchmark/result и Green-variable future source/docs review.
Большие state hashes в отчёте — pinned declared/runtime witnesses, не
повторное независимое хеширование или eigenscan этим docs reviewer.

Подтверждено:

- Native coarse/fine/warm/FD rows в таблице согласованы с малыми первичными
  источниками; J корректно переведён изA/m² вA/cm² и везде UNCONVERGED,
  без I–V/conductance/transport acceptance. Fine32+29 — user-aborted pair,
  не grid-accuracy test и не принятая matched32 пара.
- Unmodified128 включает parent32 boundary replay:127 новых post-parent
  состояний, nominal159, не160. FD128 использует **другой L/G seed** из
  того же coarse32; первая raw row не parent replay. Draft не приравнивает
  novel-state counts и не заявляет repeated FD projection. Common μ при
  bias — initializer, не доказанное equilibrium/FDR условие.
- FD конечные rΣ ratios к unmodified8,01429495/7,80163787 подтверждены.
  Это finite-budget initialization sensitivity; все256 strict pass flags
  false. Constructed first λ≈1/J≈0 и paired target не заменяют raw gates.
- Source A/8ΓR прошли **native numerical budget**, не exact PSD. Negative
  ΓR embedding minimum−1,33645e−13 явно сохранён, без clipping/repair.
  Свидетельство не переносится в exact-causal/grid/window certificate.
- Финальный max-component rΣ действительно embedding_plus.lesser:
  0mV:0,00243838911116/0,158893069334;
  1mV/period:0,00108025541865/0,165981543572.
  Эти fresh-scale norms далеки от floor1e−14; это unweighted component
  Frobenius ratio, не charge fraction. Локализация не выдана за единственную
  причину nonlinear tail, сеточной ошибки или отсутствия решения.
- Малые rD/rA — stored-state Dyson backward/spectral identity residuals,
  не forward-accuracy bound и не freshΣ/Keldysh convergence. Нормировка
  числа отдельно названа constraint, conservation/current не приняты.
- INFO surrogate/padding результат и residual4 policy разделены. R4
  сохраняет canonical raw measurement на том же Core; FD/unmodified имеют
  разные траектории, поэтому их времена не объявлены чистым end-to-end
  speedup benchmark. Allocation counters не названы RSS leak.
- Coref50/Julia1.13.3, postboot e171/1.13.4, accepted db26/Runner53b и
  отдельный finite-N/M3 equilibrium reference не объединены задним числом.
  Fixed-Hartree U0, Poisson, original native и эксперимент разграничены.
- Green-AA — только FUTURE/UNRUN: history3F против21F, не RSS/speed bound;
  unprojected T−G, λraw и materialized strict native exit обязательны.
  Walker–Ni не представлен как nonlinear/truncated/projected guarantee.
  Будущий raw-capture/hidden-state contract из linked review ещё требуется
  перед любым новым поручением; draft не обещает готовой реализации.

Start/deadline/STOP и публикационная bookkeeping provenance относятся к
owner session/отдельным publication checks; не переизмерялись здесь как
научные данные. Предстоящая вставка commit/manifest links допустима без
нового физического вывода. Любая смена чисел, science identity или acceptance
claims потребовала бы новой адресной проверки, а не переноса этого SHA-verdict.

**STOP сохранён.** Reviewer завершил docs review; никаких дальнейших опытов,
реализаций или новых научных вычислений этим заключением не разрешается.
