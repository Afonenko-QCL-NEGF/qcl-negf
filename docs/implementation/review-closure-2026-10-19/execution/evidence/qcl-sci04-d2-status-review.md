# SCI04 D2 — независимое review overflow/status interpretation

2026-10-19. **Вердикт: APPROVE только узкую трактовку D2.** Предложенное error+finite0 для ratio с nonfinite normalization совместимо с исходными M fields, enums и equality contract. Новый public format, D3 или физическое решение не нужны. Current conditional C1 этим review не становится CP-CODE accepted: correction и literal controls ещё должны быть выполнены в порученном этапе.

## Inputs, порядок и границы

Сначала независимо прочитан frozen open question и проверена зависимость ratio/absolute norms по source; затем сопоставлена clarification с unchanged D2§8.1/8.4/8.6. Author report прочитан после этой оценки. Применён ранее прочитанный qcl-physics-audit, область — residual-algebra/status source audit.

| Input | SHA256 |
| --- | --- |
| /tmp/qcl-sci05-core-open-question.md | 5d38aa1f6670a9bc39a25d74901856e2ffc35da8b69ff0d37e6c490d5b7b17bb |
| /tmp/qcl-sci04-design-v2.md, unchanged61527 bytes | d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c |
| D2 independent review | ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1 |
| /tmp/qcl-sci04-d2-status-clarification.md,13262 bytes | a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8 |
| /tmp/qcl-sci04-d2-status-clarification-report.md,4210 bytes | 657443d94e20907f964709e91a0a32f0b27595957e7267af102282557d3c836d |
| Frozen conditional /tmp/qcl-sci05-core.patch | 5381c086669da753421e4e2719daa0f3b03944b928e33ec17de0eb5e76da040e |
| Candidate reference/validation.jl | 50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c |
| Candidate reference/final_audit.jl | 2d6a9b904b0249a9efe8b418664aa5120e9b907782fd15f1dd6a1ee80f1fa1f6 |

Root actual HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`; selected Core actual `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`, root gitlink ещё f5. Diff f5→f7 затрагивает CONTRIBUTING.md, review_oracle_contracts.md и final_state_alignment_oracle.jl; production src diff пуст. Portal gitlink2622de5 и прочие concurrent dirty skills/checkpoint/evidence остаются вне этого review.

Protected candidate `/tmp/qcl-sci05-core-worktree` HEAD `f5b73369a96d1225bd96fb34f5262c8dcf965f86`; existing dirty overlay: production_solver/final_audit/poisson/validation и untracked final_audit_evidence.jl. Эти paths не редактировались. Hashes двух consumed candidate sources совпали с clarification.

Envelope20min/1CPU/2GiB/output64KiB. Выполнены только text reads, read-only Git и hashing; sole new output — этот файл. Не выполнялись project imports, tests, Julia, runtime matrix arithmetic, solver/SCBA/Poisson experiments, installation/build, server/native probes, Git mutations или scientific payload reads. OldS01, foreign state и исходные receipts не затронуты. Run/attempt/runtime/admission bindings не созданы; C08 calls0.

## Независимый source вывод

Candidate validation.jl:37–73 вычисляет numerator=norm(D*GR−I), затем D_F/GR_F, denominator=D_F*GR_F+sqrt(Nb), ratio=numerator/denominator, global/max absolute numerator aggregates. Первое nonfinite intermediate сохраняется в first_invalid; оба witness затем указывают его. Это разделяет числовую finite result и пригодность её normalization.

В frozen одном блоке NE=Nk1,Nb2, D=c*ones(2,2), GR=g*I, c=Float64(1e308), g=Float64(1e−308), все input entries finite. В real arithmetic norm(D)=2c превышает representable finite binary64 range. D*GR имеет конечные entries порядка1; residual содержит ненулевые off-diagonal terms. Если actual runtime даёт заявленный phenotype D_F=+Inf, GR_F>0 finite, numerator>0 finite, то old denominator=+Inf и old ratio=+0.0. Это условный source counterexample, а не observed runtime result.

Причина invalid ratio — его nonfinite normalization, а не невычисленный map. Global/max absolute quantities зависят от numerator, а не D_F/denominator. Поэтому их finite собственные вычисления остаются измерениями. Blanket error всех absolute fields потерял бы верное raw evidence. Напротив, finite quotient0 с invalid normalization нельзя обозначать корректно measured только из-за isfinite(ratio).

Current candidate final_audit.jl:420–428 уже умеет error с finite value через invalid_reason, без нового поля. Но _audit_witness_record:460–472 и _final_fixed_point_record:591–596 сейчас вызывают _audit_measure(value) без этой причины для finite ratio; поэтому существующий candidate сохраняет measured0 в aggregate и witness ratios. Whole record уже partial_error из-за D_F/denominator, и одного assertion top-level status для regression недостаточно. Это source finding о ещё не исправленном C1, а не отказ трактовки.

## Совместимость D2 и точный approved mapping

D2§8.4 разрешает M.status=error с finite value и nonfinite=null, controlled reason nonfinite_measurement уже существует. Tag относится к значению конкретного M, а не к любой его dependency. Поэтому перенос +inf tag с denominator на finite ratio был бы ложным описанием scalar result. D2§8.6 требует сохранить finite ratio numeric equality; value0 сохраняется. D2§8.1 запрет скрывать nonfinite block исполняется error-status normalization-dependent ratio и first-invalid witness.

| Field в данном phenotype | Approved mapping |
| --- | --- |
| dyson.ratio и оба witness.ratio | status=error,value=actual finite0,nonfinite=null,reason=nonfinite_measurement |
| dyson.global_abs_F/max_abs_F и оба witness.numerator_F | measured с actual finite значением,null tag/null reason |
| оба witness.D_F и denominator | error,value=null,nonfinite=+inf,reason=nonfinite_measurement |
| оба witness.GR_F/identity_F | measured с actual finite значением,null tag/null reason |
| ratio_witness/absolute_witness overall | error,e_index=k_index=1 |
| whole record | partial_error,reason=measurement_error |

Actual independent nonfinite numerator/sum/sqrt/max, если они возникнут, следуют своим D2 error/tag правилам; report не обещает finite values заранее. Map unavailable здесь неверный статус: измерение выполнено, normalization invalid. Finite raw absolute subfields не противоречат overall witness.error, потому что witness включает normalization fields.

Это существующая status semantics, без изменения schema marker/keys/enum/units, numeric metric/order/API или acceptance thresholds. Новый producer обязан сохранять тот же semantic M object в native/commit; equality по value не отменяет error-status. No guessed tag, no finite0→null подмена и no hidden stable-rescaling arithmetic.

## Required negative и healthy controls

Clarification:119–145 задаёт достаточный узкий regression contract, который обязан войти в correction:

1. Проверить точный overflow phenotype по фактическому prepared runtime. Если phenotype иной, сохранить failure и остановить dependent assertion; не менять constants/criteria для pass.
2. Сопоставить finite numerator с independent literal p=c*g, sqrt(2*(p−1)²+2p²), не импортируя tested residual/norm reducer в expected graph. Frozen gamma64*max(1,a_expected) — fixture-only arithmetic allowance; это не scientific tolerance. Inf/zero/status/tags/coordinates проверяются точно.
3. Проверить каждый M из approved table и оба overall witnesses. Mutants measured0 в dyson.ratio, ratio_witness.ratio и absolute_witness.ratio должны по отдельности проваливать именно status assertion при неизменном partial_error.
4. Mutants forged +inf tag для finite ratio, finite0→null, Inf→finite sentinel и blanket error raw absolute aggregates должны проваливать соответствующие value/tag/status assertions.
5. Healthy companion D=I2,GR=I2 того же shape обязан сохранять measured0 для ratios/absolute norms, finite normalization и measured witnesses. Это проверяет применимость, а не запрет любого нулевого ratio.

Тесты здесь не выполнялись. После implementation нужны отдельные CP-CODE и bounded runtime receipt; текущие conditional sources всё ещё не содержат approved mapping.

## Ограничение и решение

Трактовка касается указанного normalization-overflow phenotype и D2 scalar causality. Она не разрешает новый causal-propagation framework, переписывание norm/quotient/max/order, второй pass/map/solve, стабилизацию arithmetic, новый public format либо перенос schema decision в medium implementation. Другие load-bearing случаи, не выводимые из D2, остаются concrete blocker для координатора.

Legacy ConvergenceReport ratio остаётся0; metadata mapping сама по себе не изменяет old solver verdict. Partial_error не является успешно измеренным final raw audit и не закрывает scientific acceptance. Manufactured singular D не объявляется causal Green function/physical solution; forward error/conditioning, full model accuracy и native/runtime gates не выводятся из этого случая. S1 physics0mV/70K/all5/e–e none, strict thresholds, budgets и protected state сохраняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Finite invalid ratio может сохранить0 и получить error без forged tag | D2§8.1/8.4/8.6; clarification35–58,79–103 | Только указанный dependency/phenotype | сохранить |
| Finite independent absolute numerator aggregates остаются measured | Source validation48–66; clarification81–89 | Actual arithmetic должна подтвердить конечность | сохранить |
| Нужен новый portable format/physical decision | Existing M keys/status/reason полностью выражают mapping | Новые иные causal cases этим не разрешены | сохранить |
| Current C1 correction/CP-CODE/runtime готов | Source ещё сохраняет measured finite ratios без invalid_reason | После review нужны correction, независимый CP-CODE и finite test receipt | изменить |
| Научная/forward acceptance достигнута | Такого evidence нет | No solver/runtime/native data | данных недостаточно |

STOP после отчёта. Никакой implementation correction или test этим reviewer не выполнен.
