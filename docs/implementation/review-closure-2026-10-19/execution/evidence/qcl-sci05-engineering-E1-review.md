# SCI05 engineering E1 — независимый high source review

2026-10-19. **APPROVE CP-SOURCE для exact E1 test candidate; eligible для coordinator C08 call5 после fresh source/intent BIND.** G1/G2 реализованы в пределах ready audit33157fef. Новых load-bearing findings в узком test-only diff нет. Это не runtime GREEN и не scientific acceptance. Further corrective loop данным E1 не разрешён.

Scope≤15 min /1 CPU/2 GiB/read≤2 MiB/output≤32 KiB. Сначала прочитаны actual diff/source и ранее сформулированный ready audit; author report прочитан после независимой оценки. Единственный новый файл — этот review. Проверяющий не запускал Julia/parser/arithmetic processes/imports/tests/build/network/solver/native, не менял продукт/harness/Git, не создавал подагентов. Применён ранее прочитанный `qcl-physics-audit` в source-only границе.

## Identity и authority

Actual owning Core `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`: HEAD `e86ac74c4fe04a8999b889970c5a9f3c65575694`; `git status --short` и `git diff --name-only` содержат только modified `test/numerics/final_audit_evidence.jl`; recursive submodule status пуст. `git diff --check` успешен. Exact candidate — dirty test overlay поверх этого HEAD, поэтому HEAD без after-test SHA недостаточен для runtime binding.

| Артефакт / source | Проверенный SHA256 |
| --- | --- |
| Ready audit `/tmp/qcl-sci05-diagnostic-gap-audit.md` | `33157fef096a7945c68fe1bcaf54477304704be1b60ee9345c1dcd498659580a` |
| E1 checkpoint `/tmp/qcl-checkpoint-SCI05-engineering-E1.json` | `706dff1aaf6c9332da00ad434c314a0cb4591d3ac8ded2460d8ba3f2c5f3eaee` |
| `/tmp/qcl-sci05-engineering-E1-patch.diff` | `87d2180206e1bbb573fa5b654b3e29cbc07c29775d26b2a8a758fc2e1a184993` |
| `/tmp/qcl-sci05-engineering-E1-identity.json` | `ed3f92e5b7ebafb2e6ec2dd3a86cb6422aa9d0233ec3779f8ba353bf76c2103e` |
| `/tmp/qcl-sci05-engineering-E1-report.md` | `9f1796c061e61af5a6ce1a39cd4ea28442b1df728fddc018082803599878a0c7` |
| Before test | `d4ac564013d46021a84b323338635f6860f16d1aa76e4b417c4aaf64debf64c4` |
| Actual after test | `ede25dde26d72c313fb15e8bfcc515e8d29673b41336535c760a6eb0113309e9` |

E1 checkpoint прозрачно сохраняет original corrective cap2, consumed2, additional authorized finite engineering round1, effective max3. Он ограничивает работу G1/G2 этим test path, запрещает production/model/γ/threshold/schema изменения и дальнейший автономный corrective cycle. Этот review не переименовывает E1 в продолжение старых2/2 и не выводит новый grant из числа оставшихся test calls. Latest coordinator указал Contracts call4 уже55pass; это контекст ledger, не самостоятельно пересмотренный здесь Contracts result. E1 author identity с C08 consumed3/remaining5 — исторический before-E1 snapshot; перед call5 координатор использует актуальный общий counter4/8, а не старое число.

## G1: concrete public realness rejection и независимый scalar oracle

**Disposition: closed source-only.** Actual test154–183 сохраняет malformed ordinary-transpose field и прежний scalar real projection `wrong_number`. Дополнительный `wrong_complex` строится из тех же independently formed2×2 entries через explicit trace/scalar weights; он не вызывает tested number/residual/solve reducer для expected value.

- Healthy number comparison133–134, literal inverse2/adjoint fixture, λ masking, off-diagonal coherence, wrong weights/gs и raw-vs-mixed Σ checks сохраняются.
- Новые167–168 проверяют согласованность literal real component с прежним wrong_number и гарантируют нарушение existing realness gate1e−10 даже после **прежнего** `Bmatrix` allowance. Вычитание Bmatrix из imaginary numerator и добавление Bmatrix к правой normalizer bound усиливают необходимый запас, не ослабляют public gate. Применяется прежняя floor1 normalizer semantics.
- Public вызов170 сохраняется actual observed product path. `try` возвращает nothing при отсутствии исключения;176 тогда Fail. Catch173 пропускает только DomainError, другие exceptions rethrow. Нет catch-anything-to-pass.
- После проверки типа178 требует exact reason `number functional is not real`;179–180 сравнивают обе компоненты DomainError value с independent complex scalar в прежнем Bmatrix;181 требует actual offending value нарушать тот же public inequality. Поэтому unrelated DomainError либо непредсказанное value не становятся successful negative control.
- Прежний distinguishing real-projection-vs-healthy assertion183 остаётся; public API не вынужден выдавать число из malformed complex population.

Error ledger оценён source-арифметикой: у target path четыре weighted terms, на каждый блок два explicit2×2 complex matmuls для wrong field, upstream literal inverse2 и bounded trace/scalar operations. Это тот же finite graph и magnitudes frozen D2 matrix fixture; добавление imaginary component weighted sum не требует larger4096-operation envelope или amplification allowance. Ordinary transpose меняет conjugation, а не dimensional scale/operator count. `Bmatrix=2^24*gamma4096` и утверждение `Bmatrix<7.63e−6` не изменены. Новый generic full-device bound не введён.

**Возле нуля:** invariant использует1e−10*max(abs(real N),1), поэтому остаётся absolute при real0; никакой division by population не добавлен. Healthy real zero не объявляется ошибкой только из-за нуля. Этот конкретный complex-transpose control находится на nonzero scale; его Bmatrix не подменяет tighter near-zero A/K/Σ controls.

**Runtime limit:** новый try/message/component oracle пока не исполнен. Source proof не заменяет measured DomainError/assertion result после E1.

## G2: exact projected numerator до reciprocal

**Disposition: closed source-only.** Actual helper249–267 вычисляет:

```text
S = sum(nf)
projected_numerator[j] = 3*nf[j] − S
Uexact[j] = lambda*projected_numerator[j]/(9*q)
```

Это exact real algebra прежнего `lambda/(3*q)*(nf[j]−S/3)`. q/h/ε/λ/ND inputs, sign, gauge, native units, L/b/Q4, inverse4/3 и количество product solves не меняются. Убрано только образование reference interval reciprocal1/3 **до** neutral cancellation; generic PBall division199–201 (ныне219–221) и другие arithmetic methods не редактировались.

Новый directed reference ledger указан непосредственно в source252: exact input points → directed sum S →3n−S →lambda multiplication →division by9q. Для neutral fixture n=(1,1,1) сумма3 и3*n exact в384 bits, projected numerator point0 до reciprocal; multiply/divide0 при positive finite denominator сохраняет point0. Ref создаётся до product call. Neutral assertions335–336 требуют оба endpoints=0 и у numerator, и у exactU — невозможно подменить это «interval содержит0» или product output.

Neutral product assertions338–342 дополнительно сохраняют общий literal predicate и требуют actual Up/ζ/rP/neutrality zeros, RHS/numerator zeros, signed/absolute charge zero, прежний denominator=lambda*delta>0. Это strengthening healthy control, а не special pass branch. Никакой tolerance-based neutral classification, snapping/clipping/epsilon не добавлен.

Для nonuniform near-zero inputs выражение остаётся directed outward algebra над actual rounded Float64 points; nonzero projected numerator не превращается искусственно в ноль. Если actual rounded inputs uniform, нулевой zero-mean компонент следует из данных, а не выбранного physical tolerance. Umap0 не означает raw rU0 при nonzero publishedU; существующая rawU interval construction и public raw-rU checks не редактировались.

Сохранены без ослабления:

- gamma3 b-formation, gamma32 row/dot/norm error, inverse4/3, retained short cap;
- оба forward bounds≤short и component/gauge/ζ comparisons302–305;
- wrong sign, /4 missing-h² analogue, ×1.1, constant shift, altered-density observed mutants327–333;
- positive nonneutral и separate/joint factor2 numerator/ratio mutants345–358;
- actual published-U/public validate_solution raw rU, mixed α=1/8 и changed-density controls, ныне692 и далее;
- independent near-zero additive floors, measured-zero controls, D2 overflow per-field mapping/mutations, history/context/availability tests.

Новых bounds/tolerances не требуется. Новая3-element reference tuple field — только expected intermediate для independent positive assertion; persisted schema/API не меняется. Полный PBall redesign не выполнялся.

## Protected source и целостность scope

Actual production hashes совпали CPP2 и до-E1 состоянию:

| File | SHA256 |
| --- | --- |
| `src/QCLNEGF.jl` | `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| Protected DEV05 `test/numerics/final_state_alignment_oracle.jl` | `81fbb258f86c1760ed2ffb7964e189518fd1ec7608921e42080c969c4a55f852` |

Actual diff ограничен G1/G2 blocks этого одного test. Никаких изменений public number functional/realness invariant, physical model, fixed thresholds, solver/kernel algorithms, Γ/scattering, grids/basis/window, exception production boundary или metadata format нет. Expected values не получают данные от product result для построения здорового oracle.

Author report верно называет новый runtime `not_measured`. Его исторический consumed3 ledger не используется для будущего C08 accounting после сообщённого Contracts call4. Существующий diagnostics275/1/1 остаётся original failed evidence и не переписывается E1 source verdict.

## Следующий gate и STOP

Exact after-test SHA ede25dde... eligible для coordinator call5, после binding этой dirty overlay, actual runtime/admission и общего remaining budget. Этот review сам не выполняет call и не подтверждает будущее GREEN. Только measured targeted receipt может закрыть runtime test result. Если возникнет новый source/semantic defect, E1 требует concrete blocker: дальнейший corrective loop не разрешён этим review. Все S1 experiment caps, declared model, physical strict criteria и final-CI policy неизменны.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| G1 готовый contract реализован без false GREEN path | Typed rejection, exact reason/value и independent complex scalar, retained healthy/mutants | Новый runtime отсутствует | сохранить |
| G2 нейтральный эталон имеет exact cancellation до reciprocal | Equivalent3n−S/9q graph, pre-solve point0 assertions | Исполнение directed graph ещё не измерено | сохранить |
| γ/thresholds/production/PBall generic division/DEV05 сохранены | Single-test diff и actual hashes, unchanged strict predicate lines | Source-only review | сохранить |
| E1 candidate eligible для C08 call5 | Exact patch/test identity; новых load-bearing findings нет | Fresh BIND и actual aggregate counter обязательны | дополнительно измерить |
| Runtime/scientific acceptance получена | Новый запуск не выполнялся | Previous full diagnostic RED не отменён | данных недостаточно |

STOP. Единственный output — этот review; никакой новой реализации или исполнения.
