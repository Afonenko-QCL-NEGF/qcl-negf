# RV08 — объявленный denominator и свойства

Статический этап, Core `3108150dd1b6b1377470b384b15c26e272fe5c5d` (S).
Root overlay: `../source-receipt.json`; источник overlay — frozen `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Шесть initial пакетов и их properties заданы scope-карточкой до чтения symbols:

| Пакет | Выбранные properties | Применимость |
|---|---|---|
| D | обращение Dyson; причинный scalar pole; bounded residual | ортонормированный базис, Hermitian h, dissipative ΣR |
| K | adjoint/anti-Hermitian; scalar Keldysh limit; positivity | Σ< anti-Hermitian и −iΣ< PSD; отсутствие отдельного initial-source term |
| S | raw candidate residual до mixing; fresh resonant gate; общий final U/G | фиксированный Hartree внутри SCBA; stationary final state |
| P | compatible source; mean-zero gauge; finite-volume stencil | uniform periodic grid, εr>0, положительная donor sheet density |
| L | Fröhlich dimensions/normalization; LO pair signs; equilibrium number/energy balance | thermal LO, общий T/μ, zero drive; finite-window tails отдельно |
| J | outgoing sign/units; resolved-current integral; finite-basis reconstruction | stationary field-periodic embedding; local basis truncated |

Supplemental fixtures выбирать конечным расширением, с явным именем в отчёте.
Selected denominator = 6 packets, 18 declared properties; fixture execution = 0.
Remaining initial queue = 22 reference symbols из RV08-scope; production queue =
6 PROD traceability contracts (каждый отдельный пакет), пока partial/unreviewed.
Численные данные запуска: frozen plan/model/run/attempt/raw S01 arrays отсутствуют;
numeric verdict для всех properties = `not_measured`.

Секции-кандидаты: `../RV08.md`; независимый reviewer пишет `../reviews/RV08-*.md`.
Один writer для RV08 report/cards/fixes; продуктовый код не изменяется.
