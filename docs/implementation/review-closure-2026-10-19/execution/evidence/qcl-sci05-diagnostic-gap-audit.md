# SCI05 — independent diagnostic gap audit, без реализации

2026-10-19. **Оба наблюдённых отказа классифицируются как дефекты независимого теста.** Call3 не даёт свидетельства дефекта production `number_functional` или Poisson solver. Для обоих gaps возможен узкий test-only repair contract без изменения physical model, public API, γ, floor или acceptance thresholds. Ни правка, ни новый запуск этим audit не разрешаются и не выполняются. Original SCI05 corrective cap2/2 исчерпан; необходим отдельный конечный engineering replan координатора.

Применён ранее прочитанный `qcl-physics-audit`, этап source/arithmetic audit существующего результата. Scope≤15 min /1 CPU/2 GiB/read≤2 MiB/output≤32 KiB. Сначала целиком прочитаны call3 raw/receipt; затем immutable test, production preconditions, PBall graph и accepted D2/O08-03 formulas. Единственный новый файл — этот отчёт. Python/Julia arithmetic processes, parser/import/tests/build/install/network/solver/native calls=0; Git/product mutations=0. Подагенты не создавались. Приведённая арифметика — символический разбор формул и уже измеренных чисел, не новое исполнение.

## Исходные свидетельства

Actual owning Core HEAD `e86ac74c4fe04a8999b889970c5a9f3c65575694`, status пуст, recursive submodule status пуст; `git diff --check` успешен. Test `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl/test/numerics/final_audit_evidence.jl` SHA `d4ac564013d46021a84b323338635f6860f16d1aa76e4b417c4aaf64debf64c4` не изменён.

| Первичный артефакт / источник | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-SCI05-C08-DIAGNOSTIC-3/original.log` | `3ea0c064402917a29df4abae74447c4d17078865469fd62ef7d6cbfd3efc0ece` |
| `/tmp/qcl-SCI05-C08-DIAGNOSTIC-3/receipt.json` | `15c50c17b266692734fc58afcb806c0613a0cd7fe67734734f1f3c543328fd93` |
| Diagnostic harness v2 из receipt | `949d2b5d621ac3b23196e61116334731ca3871163411b1ac2a21f277b8de60a0` |
| Core `src/numerics/reference/greens.jl` | `25f476e3ac4f4c282433f55286ded0893994ac9bb1ce8c0ab17fe1c3b288f5b9` |
| Core `src/domain/numerical_invariants.jl` | `9ffa937de68e9acb7e09b4f4029c7a192d60f1c992be274ac79c7997745cadee` |
| Accepted `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| Accepted O08-03 `/tmp/qcl-final-ug-design-v2.md` | `eb9e1a8c39ad08bafa480970392d844c2c9fffdef02d847397ef87c52111bfc9` |
| O08-03 D2 independent review | `53c3e9b4061a6cdb42239d6d42f5b3f7a09b94eb36315b1ec22bfea103c4f55f` |

Receipt: exit1, wall29.377s, sampled peak tree RSS821837824 B, sampled owned TEMP0 B, raw7932 B, raw_capture_complete=true; stop_reason/guard_error/capture_error=null, output_overrun=false. Это successful evidence collection известного RED, не successful test acceptance. По summary все семь sibling testsets достигнуты:

| Набор | Измеренный результат |
| --- | --- |
| Dyson witnesses/nonfinite | 26 Pass |
| Near-zero additive-floor/measured-zero | 24 Pass |
| Complex matrix/number/candidate | 21 Pass +1 Error |
| Poisson literal/gauge enclosure | 16 Pass +1 Fail |
| Overflow finite-ratio0 mapping | 89 Pass |
| Template/availability/charge | 76 Pass |
| Public validation/raw rU/transport | 23 Pass |

Итого275 Pass/1 Fail/1 Error, RED сохранён внешним testset. Такая coverage закрывает прежнюю неизвестность «не дошли до поздних blocks», но не доказывает каждое свойство физической модели или достаточность сетки. Исправление тестовых дефектов и новый полный targeted result пока отсутствуют.

## G1 — test162: precondition публичного number functional

**Категория:** independent-test defect, mismatch negative-control expectation с существующим public domain contract. Product defect не установлен; load-bearing normative ambiguity не требуется.

**Наблюдение:** `test/numerics/final_audit_evidence.jl:154–162` строит
`Gwrong = GR * SigmaL * transpose(GR)` с ordinary `permutedims`, затем162 требует finite числовую разность `number_functional(Gwrong)-Nhealthy`. Raw сообщает DomainError с actual complex value
`0.2582304378268251 - 0.8300177489439131im`, reason `number functional is not real`.

**Формула/контракт:** `greens.jl:99–108` вычисляет

```text
Ncomplex = gs/(2π) Σ_e,k wE[e] wk[k] (-i Tr(GL[e,k,:,:]))
```

и перед return real(Ncomplex) требует
`abs(imag(Ncomplex)) ≤ 1e-10 * max(abs(real(Ncomplex)), 1)`.
Structural limit1e−10 задан owning `numerical_invariants.jl:5`, это существующий invariant, не campaign fit tolerance. Для observed real≈0.258 нормировка равна1, разрешённый imaginary defect≤1e−10, наблюдённый≈0.830. Public function обязана отклонить этот malformed input до числового return. Ordinary transpose не сохраняет требуемую lesser anti-Hermiticity и не обязан давать real population.

**Связь с accepted oracle:** D2 §7/§9 требует отличать wrong transpose от healthy literal result. Он не требует отменять public realness precondition для malformed field. Existing literal `wrong_number` на155–160 берёт real projection; assertion163 проверяет его отличие от healthy number и в call3 проходит. Real projection самостоятельного literal scalar не разрешает product API silently принять большой imaginary part. Поэтому error162 — ошибка способа проверки отрицательного контрола, не противоречие D2 physics/weights/normalization.

**Контраргумент:** можно считать любое thrown exception желательной отрицательной реакцией. Для достаточного negative oracle это слишком слабо: нужно привязать реакцию именно к известному realness contract, не скрывать произвольную ошибку установки/shape/index. Ниже дан узкий проверяемый contract, а не catch-anything-to-pass.

**Поведение около нуля:** floor1 в public normalizer уже делает realness check абсолютным при малом real(N). Нельзя заменить его division by real(N), относительным tolerance при zero или принудительным real projection product result. Для healthy measured zero `Ncomplex=0` invariant проходит; для purely imaginary malformed number с большой imaginary part — отклоняет даже при real0. В текущем control numbers имеют nonzero scales; `Bmatrix` не переносится на near-zero A/K/Σ tests.

### Минимальный ready repair contract G1 — только после отдельного replan

Owner/path: только `test/numerics/final_audit_evidence.jl`, narrow wrong-transpose block154–163. Исходные matrix fixture, weights, gs, transpose mutation и `Bmatrix=2^24*gamma4096` сохранить.

1. Healthy public number assertion и literal inverse2/adjoint/weighted sums сохраняются: валидный input по-прежнему возвращает finite real number с прежним bound.
2. Malformed transpose public path проверяет ожидаемый **DomainError realness contract** вместо невозможного finite return. Unexpected exception не становится pass; production evaluator/structural limit/message не меняются. Не добавлять clipping, `real(...)` внутри public вызова или игнорирование error.
3. Независимый literal complex weighted sum строится из уже замороженных tiny matrix scalars, без `number_functional`/tested reducer. Его real projection должен оставаться тем же existing `wrong_number`, а imaginary part должен с запасом нарушать неизменный public realness inequality. Existing fixture-only arithmetic bound применим к nonzero-scale scalar components; error ledger должен остаться внутри принятого bound, без нового larger gamma. Actual DomainError value/reason можно сверить с этим literal, если capturing применяется; не сравнивать только status «что-то бросилось».
4. Existing assertion163 о различии literal real projection и healthy number, wrong weights/gs, λ masking и raw-vs-mixed controls остаются. Тест не теряет distinguishing power обычного transpose против adjoint.

**Решение:** изменить test expectation в отдельном разрешённом engineering scope. Изменение production realness gate либо scientific tolerance не является допустимым repair этого gap; если оно потребуется автору, это новый blocker, а не ready repair по данному audit.

## G2 — test312: reference interval width при exact neutral zero

**Категория:** independent-test defect в evaluation graph эталона/consumption interval upper bound. Product Poisson defect не установлен. Это не свидетельство недостаточного γ32 и не причина менять normative contract.

**Наблюдение:** raw для neutral input содержит n=(1,1,1), h=2, εr=4, q=1, target6 и product result:

```text
Up=(0,0,0), zeta=0, rP=0, neutrality=0
rhs_F=0, residual_numerator_F=0
denominator=additive_floor=1.8095128179727823e-13
```

Все эти измерения согласуются с exact neutral equations. Одновременно `neutralref.exactU[j]` в raw — outward interval примерно
`[-3.0616e-115, +1.5308e-115]`, а не point0. Test312 сообщает только false общего predicate; место первой ложной проверки выводится из его source ниже, не из нового trace.

**Арифметическая причина:** test229 вычисляет `S=psum(nf)` и `meanN=S/PB(3)`. Для текущих exact inputs S=3, но PBall division199–201 реализовано как умножение на interval reciprocal. Binary floating representation `1/3` не конечна даже при384 bits. Outward `[1/3↓,1/3↑]`, умноженный на3, содержит1 с положительной шириной. Поэтому `nf[j]-meanN` включает0, но не point0; последующее умножение на λ/(3q) даёт именно маленькую ненулевую ширину, которую видно в raw. PBall division остаётся корректным outward enclosure; это dependency/rounding overestimation эталонного выражения.

**Почему predicate отвергает правильный product0:** в `literal_poisson_enclosure:249–258` при actual Up0, literal b0 и zeta0 все expanded LUp−b, meanUp, projected residual и Q4 residual равны point0. Gamma3/Gamma32, умноженные на нулевые norms, дают0. Поэтому оба computed forward bounds имеют upper0; retained short cap положителен (raw≈1.9286e−13), и check278 проходит. Но check279 требует
`abs(PB(0)-neutralref.exactU[j]).hi <= box.forward.hi`.
Левая сторона положительна из-за **ширины independent reference arithmetic**, правая0. Следовательно,279 возвращает false, что объясняет312. Это символический вывод по показанным inputs/source; отдельный diagnostic execution не проводился.

**Формула/применимость:** accepted O08-03 D2 §5 задаёт exact actual-coefficient solution
`Uexact=λ/(3q)*(n−S/3)` и residual-based forward bound
`||P*r||2/(3q)+abs(meanUp)`, с прежним source rounding allowance. D2 neutral case требует b=0, numerator0, denominator=λ*Float64(1e−14). Для exact neutral system product zero не обязан иметь ненулевую допустимую ошибку. High-precision reference enclosure не является дополнительной physical uncertainty и не должна ложно расходовать zero-error solve budget.

**Контраргумент:** увеличить precision или добавить ε к правой стороне. Увеличение precision уменьшит ширину, но reciprocal1/3 останется неexact при любой finite binary precision; bound0 всё равно не удовлетворится положительной шириной. Произвольный ε, `atol`, floor для forward error или larger gamma скрыли бы defect oracle graph и меняли бы строгую проверку ради GREEN. Это не допустимый repair.

### Минимальный ready repair contract G2 — exact cancellation до деления

Owner/path: только literal reference helper в `test/numerics/final_audit_evidence.jl:221–243` и связанные узкие independent reference assertions. Production poisson.jl/validation и PBall generic arithmetic не менять.

1. Вычислять то же exact zero-mean reference через алгебраически эквивалентную форму:

```text
Uexact[j] = λ * (3*n[j] − S) / (9*q),    S=Σ_j n[j]
```

Сначала form projected numerator из exact Float64 input points в directed high precision, затем делить. Для текущего uniform neutral n=1 `3*n−S=0` точно до reciprocal; умножение/деление point0 при positive finite q сохраняет point0. Более общо для трёх одинаковых finite Float64 n sum/3*n требуют значительно меньше384 significant bits, поэтому exact cancellation доказывается по данным, а не подгоняется под observed Up. Reference замораживается **до** product call.
2. Это равенство exact real algebra к прежней формуле, без изменения q/h/ε/λ/ND inputs, gauge, sign, units, L/b/Q4 или числа product solves. Не подставлять product Up вместо эталона и не использовать tested builder/solve для expected numerator.
3. Сохранить outward arithmetic для nonneutral/near-zero n; обновить лишь ledger высокоточных scalar operations для этой эквивалентной reference expression. Float64 product γ3, γ32, inverse4/3, retained short cap и все current thresholds остаются прежними. Ни check278, ни rigorous forward/gauge comparisons279–281 не удаляются и не ослабляются.
4. Явно удержать neutral positive control: literal projected numerator и Uexact — point0, product Up/ζ/numerator/RHS/neutrality0 проверяются прежними meaningful checks, additive denominator λδ>0 сохраняется. Нельзя применять правило `abs(x)<ε ->0`, clipping, tolerance-based neutral classification или особую pass ветку по product result.
5. Retain observed mutants wrong sign, /4 missing-h² analogue, ×1.1, constant gauge shift, altered density; positive nonneutral factor2 numerator/ratio mutants; actual published-U/raw-rU/mixed-step public validation. Новая reference form не должна отключать эти predicates или менять amplitudes.

**Возле нуля:** exact uniform input имеет exact projected numerator0 по структуре задачи; это legitimate measured zero. Непостоянная малая perturbation даёт её actual rounded Float64 projected numerator и outward bound, без snapping к нулю. Если намеренная perturbation округлилась в uniform actual input, reference обязан описывать actual input, не скрыто восстанавливать intended real perturbation. `denominator=||b||+λδ` остаётся положительным, поэтому neutral residual ratio0 определён. Нулевой Umap не означает нулевой raw rU: при publishedU=(1/8,−1/4,1/8) exact raw max defect=1/4; существующая rawU logic и public validation checks должны сохраниться.

**Решение:** изменить только независимый reference evaluation graph в отдельном engineering scope. Полный redesign PBall, relaxation interval comparisons либо gamma/scientific threshold change не нужны для этого воспроизводимого case и не разрешены этим ready contract.

## Достаточность diagnosis и границы

Оба ready contracts адресуют конкретные test defects с независимым объяснением и различающими positive/negative controls. Из этого не следует, что больше ошибок нет:275 passes относятся к данным tiny fixtures, одной Julia/runtime/source комбинации и executed branches. Всё последующее acceptance требует exact new source diff review и отдельного bounded runtime receipt в новом разрешённом engineering этапе. Автор не должен автоматически внедрять предложенные изменения на основании этого audit.

Нормативный scientific contract D2/O08-03 переоткрывать для данных двух gaps не требуется. Неизвестные conditioning/nonlinear contraction/full-device discretization/experimental agreement от этих тестовых repairs не становятся известными. Если конкретная реализация потребует увеличить gamma, criterion, изменить zero semantics, shape/model или public API, ready contract перестаёт применяться и возникает blocker для координатора.

C08 consumed=3/8 по трём существующим receipts; remaining5 — не разрешение на автоматические retries или новую product correction. Исходный corrective cap2/2 остаётся исчерпанным. Следующий шаг возможен только через отдельный finite engineering extension по последнему прямому user development-resource grant, с exact allowed paths/attempts/stop и сохранением всех original failed logs. S1 experiment caps/physics/strict acceptance не затрагиваются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| G1 — независимый test expectation defect | Raw DomainError162, greens99–108, invariant1e−10 | Malformed input, не real healthy population | изменить |
| G2 — независимый reference interval defect | Raw exactU interval width, product0; PBall reciprocal199–201 и predicate279 | First false branch выведена source-арифметикой, новый trace не выполнен | изменить |
| Production number/Poisson defect установлен | Оба measured outcomes согласуются existing domain/equations | Это не общее доказательство solver correctness | данных недостаточно |
| Узкий repair возможен без D2/physics/threshold changes | Public DomainError contract + equivalent projected numerator before division | Только prospective test-only contract, не разрешение реализации | сохранить |
| Поздние blocks исследованы | Call3 summary всех7 наборов,275/1/1 | RED; tiny fixture coverage, не full-device acceptance | сохранить |
| Автоматический третий corrective loop разрешён | Original cap2/2 consumed | Нужен отдельный finite engineering replan | данных недостаточно |

STOP после отчёта. No code change или new execution.
