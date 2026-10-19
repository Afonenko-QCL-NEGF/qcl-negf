# SCI03 — final independent CP-DESIGN R2

2026-10-19. Source/design-only, узкая независимая проверка D2 после R1.

**CP-DESIGN: APPROVED для bounded measurement/pilot design.**
R1-01–03 закрыты. Это утверждение о научном дизайне и его буквальных measurement
semantics; numerical/scientific acceptance, CP-SCI runtime READY и admission
не установлены. Работа R2 frozen и остановлена; третьего design round нет.

## Exact reviewed artifacts

| Артефакт | SHA256 |
| --- | --- |
| D2 `/tmp/qcl-sci03-design-v2.md`, 40 812 bytes | `788ab058f1c52520d79aa621dcecd0d525f2562b7fcf2ea10da2c664989c8018` |
| Diff `/tmp/qcl-sci03-design-v2.diff`, 6 680 bytes | `3011ef89c2618d68145b537869d2a59ec6e670b2793fcc5ccf9d4faa6ccbe104` |
| D2 author report, прочитан LAST | `18eadecad3e240f4055f25e809ca8e2e12c562d6793a798f8ccaba0ecdc105c3` |
| R1 review, baseline rationale/limitations | `f917b3b6fab356dd1972aece21b34f1b4ba967e53303d613c373262b6bd96822` |
| D1 preserved baseline | `ceffa4f2ca941510451f1d28a9f0cbaff7277e10411230c0b1dc8ab26c649509` |

Root HEAD при R2 `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`.
Фактический status прочитан: concurrent untracked Core test, AiiDA/Platform
internals и root checkpoint/evidence/tooling. Они не являются новыми reviewed
source inputs и не включены в этот verdict. **Все14 owning hashes повторно
совпали** с D1/R1/D2; production bytes не изменились. R1 primary/mathematical
проверка сохраняет свои пределы независимости и не повторяется без причины.

## Проверенная дельта и closure

Независимый SequenceMatcher установил ровно3 replace blocks, по одной строке:
D1/D2 lines48,96,140. Removed/added lines точно совпадают с diff artifact;
других изменений нет. Trailing whitespace отсутствует.

- **R1-01 closed:** helper `_ratio(0,0)` отделён от полного FDR. Defined μ и
  applicability обязательны; unavailable μ сохраняет inherited status/reason
  и value=None. При nonnegative q, capacity<=0 и applicable context сохраняется
  `not_measured/empty_represented_spectrum`. Negative q и другие причины не
  перезаписаны. Повторно прочитаны Results `_fit_mu`:237–247,
  fitted/fermi:459–464, full FDR:527–531; текст соответствует actual branches.
- **R1-02 closed:** acoustic paragraph locator исправлен на printed p.4,
  совпадает с проверенными в R1 primary bytes. B1/B2 p.17 не менялись.
- **R1-03 closed:** FJ — prefactored scaled boundary flux, FC — unprefactored
  signed collision integral, FP — prefactored dimensionless channel power;
  max по sides/channels и отдельные channel-C metrics указаны. Повторное чтение
  Core acceptance_metadata.jl:248–263, observables.jl:314–322,390–399 подтверждает
  неизменные branch switch1e-12, multiplier100 и strict threshold1e-10.

Полная остальная дельта отсутствует: §5 bounds, strict norms/thresholds,
0mV/period70K, пять LO/acoustic/impurity/IFR/alloy и e–e none, S1 slots/caps,
H+ΔE/4 и unknown error coefficients остаются ровно reviewed D1.

## Remaining ready actions and blockers

**Готовы к отдельному owning source/design поручению:** публикация точных
reviewed design bytes с provenance; SCI04/O08-03 final-U/G-density audit design;
SCI06 represented-current coefficient reducer contract и независимый literal
oracle; SCI12 gauge/basis/domain mappings, tail/interaction/H exact encoding;
SCI03-ACC derivation finite target basis. Это не разрешение незаявленных
executions и не обход обязательного D→I→independent R для реализации.

**Scientific acceptance blocked:** отсутствуют independently justified finite
εQ, nonlinear conditioning/contraction и required tail/truncation/interaction
bounds. Sensitivity, seed, normalized density и mixed step не заменяют bound.
**Pilot runtime blocked:** SCI07/08 enforceable guards/fresh admission и SCI09
exact frozen plan/identity/budget bindings ещё не установлены. H использует
единственный уже утверждённый slot, до него нужен exact A1 freeze; H не даёт
дополнительной попытки или continuum proof. Эти ограничения не требуют заново
спрашивать уже утверждённые B/G1/S1 permissions.

R2 включал только read-only file/source/hash/diff checks и запись этого отчёта
в /tmp. Product imports, Julia, tests/solver/build/benchmark/install/fullCI,
network retrieval и server probes не выполнялись; current/old attempt arrays
не читались. Научных попыток0. CPU/RSS не измерялись и не объявлены profile.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1-01–03 закрыты | Exact3-line diff + owning branches + R1 primary locator | Source/design evidence | сохранить |
| CP-DESIGN D2 пригоден для finite pilot contract | Exact hash, неизменные bounds/strict policy/S1 и explicit unknowns | Runtime gates отдельны | сохранить |
| Полная physical/discretization acceptance получена | Missing εQ/conditioning/tail/truncation evidence | Дизайн не numerical result | данных недостаточно |
| Pilot/H runtime READY | Missing guards/admission/exact plans | Approved slots не readiness | данных недостаточно |
