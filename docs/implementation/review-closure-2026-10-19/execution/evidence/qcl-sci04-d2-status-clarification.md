# SCI04-D2 — нормативная трактовка конечного ratio при overflow нормировки

2026-10-19. **Узкая интерпретация принятого D2, не D3 redesign.** Она относится
к frozen source case ниже и его существующим measurement fields. D2 bytes,
schema marker/keys/status enums, public API, numeric evaluator, thresholds,
physics и budget не изменяются. Independent high review этой трактовки ещё
нужен до размораживания C1 correction/CP-CODE; author не закрывает review сам.

## Входы и доказательная граница

Принятый D2 `/tmp/qcl-sci04-design-v2.md`: SHA256
`d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`;
его independent review SHA256
`ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1`.
Frozen question `/tmp/qcl-sci05-core-open-question.md`: SHA256
`5d38aa1f6670a9bc39a25d74901856e2ffc35da8b69ff0d37e6c490d5b7b17bb`.
Baseline Core HEAD в `/tmp/qcl-sci05-core-worktree`:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`.

Прочитаны D2 §8.1/8.4/8.6 и C1 candidate source: validation.jl:37–73,
final_audit.jl:417–437,461–477,586–599. Candidate — незакоммиченный frozen
engineering source, не approved/runtime evidence. Actual hashes:
validation.jl `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c`;
final_audit.jl `2d6a9b904b0249a9efe8b418664aa5120e9b907782fd15f1dd6a1ee80f1fa1f6`.
Git status: изменены четыре production files final_audit/validation/poisson/
production_solver и untracked test/numerics/final_audit_evidence.jl; ничего из
этого данной работой не редактировалось. Submodules в Core отсутствуют.

Это source analysis и нормативная трактовка. Julia/imports/tests/solver/native
arithmetic/runtime не запускались. Описанные Float64 outcomes ниже — условие
различающего будущего literal control, а не выполненный test receipt.

## Решение и основание в D2

**Условное предложение question принимается в следующем точном смысле:**
конечный ratio0 сохраняет value0, но имеет status=error, reason=
nonfinite_measurement, nonfinite=null, поскольку его фактически использованная
нормировка nonfinite. Global/max absolute numerators остаются measured, если
их собственные scalar вычисления конечны. В обоих witness ratio получает тот
же error finite0; D_F и denominator сохраняют собственные +inf tags.

Это уже выражается типом M и closed reason enum D2. §8.4 разрешает finite
invalid measurement с error и finite value; пример negative target не
ограничивает этот случай только donor constraint. §8.1 требует не скрывать
nonfinite block в соответствующем aggregate. В этом case нормировке зависит
dyson.ratio; global_abs_F/max_abs_F вычисляются из a_b без D_F/denominator.
§8.6 сохраняет valid finite subfields; здесь finite absolute numerator valid,
а finite normalized quotient имеет invalid normalization. Finite числовое
равенство record ratio и existing report ratio поэтому сохраняется **по value**,
при отличном от measured статусе. Число0 само по себе не делает эту нормировку
измеренной корректно.

Слова D2 «error с tag» не разрешают придумать +inf для конечного ratio. Tag
описывает nonfinite **значение данного M.value**, а не всю его dependency chain.
Actual +inf находятся в D_F/denominator и там выражаются tagged null. Error
ratio с finite0 использует существующий nullable nonfinite field без тега.
Вариант error/null/invalid_prerequisite для ratio здесь не используется:
вычисленное finite0 известно и должно сохраняться по §8.6.

## Exact source case и per-field mapping

NE=Nk=1, Nb=2, E=0, h=zeros(2,2); D=c*ones(2,2), c=Float64(1e308);
ΣR=−D, GR=g*I2, g=Float64(1e−308). Входные entries конечны. Это manufactured
residual-algebra case; D singular, никакая physical solution/causal Green
function не утверждается.

Пусть actual old arithmetic вернула finite a=norm(D*GR−I)>0,
qG=norm(GR)>0, qI=sqrt(2), D_F=+Inf, denominator=+Inf и ratio=+0.0;
sum_abs2=a² остаётся finite. Значения a/qG/qI берутся из выполненного scalar
pass без guessed replacement. В точной real арифметике c,g дают p=c*g,
a²=2(p−1)²+2p²; математическая нормировка конечна после произведения
(2c)*(sqrt(2)g)+sqrt(2), но intermediate norm(D)=2c не помещается в Float64.
Это объясняет invalid normalization. **Стабилизировать/переставлять произведение
в evaluator здесь не разрешается:** исходный Float64 ratio0 сохраняется.

Все M по таблице имеют ровно D2 keys status,value,nonfinite,reason; null — JSON
null, не отсутствие key. В new record/native/commit mapping один и тот же.

| Field | status | value | nonfinite | reason |
| --- | --- | --- | --- | --- |
| dyson.ratio | error | actual old finite +0.0 | null | nonfinite_measurement |
| dyson.global_abs_F | measured | actual sqrt(sum_abs2), finite | null | null |
| dyson.max_abs_F | measured | actual max_abs=a, finite | null | null |
| оба witness.numerator_F | measured | actual a, finite | null | null |
| оба witness.D_F | error | null | +inf | nonfinite_measurement |
| оба witness.GR_F | measured | actual qG, finite positive | null | null |
| оба witness.identity_F | measured | actual qI, finite positive | null | null |
| оба witness.denominator | error | null | +inf | nonfinite_measurement |
| оба witness.ratio | error | actual old finite +0.0 | null | nonfinite_measurement |

ratio_witness.status=absolute_witness.status=error; их e_index=k_index=1.
Существует единственный block, который одновременно first-invalid и оба
witness: иной выбор/tie этим уточнением не вводится. Record.record_status=
partial_error, Record.reason=measurement_error; map доступна, поэтому
unavailable/map_unavailable здесь неверны. Остальные record fields сохраняют
свои actual independent measurements/statuses; данное решение не превращает
их в zero/error без проверки их собственных scalar цепочек.

В частности, absolute_witness содержит normalization fields и потому имеет
overall status=error, хотя его numerator_F и оба absolute aggregates measured.
Это не противоречие: witness object шире одного numerator. Если a либо его
global sum/sqrt/max сами nonfinite, соответствующий M следует исходным D2
error/tag правилам; finite значения не объявляются заранее и не имитируются.

## Минимальная граница correction и независимый negative control

Разрешён только existing D2 measurement-status mapping в C1 allowed paths.
Reuse actual first-invalid witness/scalar diagnostics того же pass для отметки
nonfinite normalization. Existing _audit_measure(value;invalid_reason=...)
уже выражает error finite0 без нового portable field или public argument.
Не менять old quotient/max/loops/order, не добавлять повторные norms/arrays,
fresh map, stable-rescaling solve или fallback measurement. Эта трактовка
не является новым общим causal propagation framework; иные load-bearing
случаи, не выводимые из D2, возвращаются координатору как concrete gap.

Будущий bounded C1 test обязан различать следующие варианты. В этом task он
не выполняется; C08 calls0 и aggregate cap не пополняется.

1. Frozen one-block literal выше. Сначала явно проверить phenotype: finite
   entries, D_F=+Inf, qG finite positive, a finite positive, denominator=+Inf,
   ratio exactly +0.0 и finite absolute aggregates. Если platform/runtime
   даёт иной phenotype, сохранить failure; не менять constants/criteria ради
   pass. Observed старый numeric API и record.ratio.value равны0.
2. Expected numerator строится независимой scalar формулой:
   p=Float64(c*g), a_expected=sqrt(2*(p−1)^2+2*p²), без tested residual/norm
   reducer. Для finite absolute values достаточно fixture-only absolute
   rounding bound gamma64*max(1,a_expected), u=2⁻⁵³,
   gamma64=64u/(1−64u): одна nonzero multiply на entry, ≤4 entry terms,
   squaring/sum/sqrt и scalar global sqrt. Никакой full-device tolerance
   здесь не выводится. Отдельные +Inf/zero/status/coordinate/tag assertions
   точные, без tolerance.
3. Проверить **каждый M из таблицы**, оба witness.status/coordinates и
   record partial_error. Один лишь record_status assertion недостаточен:
   текущий candidate уже становится partial_error из-за witness fields.
4. Mutation «ratio M measured0» в aggregate и отдельно в каждом witness.ratio
   обязана провалить status assertion, даже когда overall partial_error
   остаётся прежним. Mutation «перенести +inf tag на finite ratio» или заменить
   finite value0 на null обязана провалить exact value/tag/equality assertion.
5. Mutation «все raw aggregates error из-за D_F» обязана провалить measured
   assertions для global_abs_F/max_abs_F/numerator_F. Mutation, скрывающая
   actual +Inf у D_F/denominator finite sentinel-ом, обязана провалить tags.
6. Healthy companion: D=I2,GR=I2 при тех же shape. Все normalization fields
   конечны, numerator/ratio/global/max=0. Ratio M и оба witness.ratio имеют
   measured0,null tag,null reason; witness overall measured. Это отличает
   legitimate measured zero от overflow-induced zero и не запрещает measured0.

Native/commit future serialization использует ровно эти M objects и D2 exact
semantic equality. Никаких новых status/reason codes, schema version, units,
tag encoding или acceptance thresholds эта трактовка не вводит. Numeric
ConvergenceReport ratio остаётся0: не заявляется, что одной metadata correction
уже изменён old solver verdict. Partial_error нельзя представить как успешно
измеренный final raw audit; полная scientific acceptance требует остальных
frozen gates/артефактов и здесь не установлена.

## Решения и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Finite ratio0 с overflow нормировки может быть error без потери value | D2 §8.1/8.4/8.6; existing M shape/reason enum | Source interpretation, independent high review pending | изменить |
| Absolute norms сохраняют собственную valid finite measurement | Их formulas зависят от a_b, не D_F/denominator | Измеренность зависит от actual собственной конечности | сохранить |
| Трактовка сохраняет D2 schema/physics/API/thresholds | Existing error finite mapping полностью выражает case | За пределы указанной трактовки новые решения не разрешены | сохранить |
| CPP/runtime green уже получен | Тесты/Julia не запускались; C1 frozen conditional | Следом independent review, затем разрешённая correction/test phase | данных недостаточно |

STOP. D2 original bytes и все original source/receipts сохранены.
