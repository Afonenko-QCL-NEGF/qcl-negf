# SCI06 — независимый source audit stored reader

2026-10-19. Этап: A/R high, чтение исходников, tests и frozen contracts. Реализация, imports и test execution не выполнялись. Первый собственный verdict сформирован до чтения SCI04-D2 independent review; затем проверено только его approval и применимость уже принятого N1.

## Вердикт

**Сохранить existing stored-state reducer как независимый от Julia/Core путь измерения full-matrix FDR, sheet numbers и outward currents. Source и manufactured assertions поддерживают эту роль. Утверждение о восстановлении величин из конкретного exact immutable final сейчас не измерено: финальные массивы/run/attempt не предоставлены. Source audit не заменяет C07 или C08.**

Не обнаружено source-признака diagonal-only FDR, повторного включения embedding в raw или подмены отсутствующего FDR нулём. Обнаружены два явно локализованных отсутствующих measurement/format capabilities: approved D2 final-record cross-check (готовый SCI05-N1 owning ticket) и коэффициенты/absolute represented-current bound SCI03 §5.3. Неполный expected_identity и разрешённый requested≠stored inventory ограничивают stronger identity/model claims; при полном C07 input это не доказанная ошибка reducer.

## Неизменяемые входы

Workspace `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Root HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`.

| Owner | Selected/current commit | Проверка |
| --- | --- | --- |
| Results | e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae | HEAD совпадает с root gitlink, `git status --short` пуст |
| Contracts | 02a564b78dc9c5e19eacf496bc8c891361eafaab | Root gitlink совпадает, status пуст |
| Research | 1eacefcd81a50e245ea9da74a0b717b33818c61e | Root gitlink совпадает, status пуст |

Initial root dirty: `components/QCLNEGF.jl`, `components/QCLNEGFRunner.jl`, execution/checkpoint.json, execution/qcl-targeted-receipt-census.json, docs/single-server-deployment.md; untracked execution evidence/receipts/tests относятся к соседним задачам. Recursive status: Core current `e86ac74c4fe04a8999b889970c5a9f3c65575694` и Runner `9378396a3681c1eddf2c62f16674834fc4465583` отличались от root gitlinks; остальные selected gitlinks совпали. Эти overlays не использовались для численного verdict. Original dirty checkout не читался и не изменялся.

Прочитаны root AGENTS, architecture, канонический agent-review-workflow; Results CONTRIBUTING; P1 science.md:232–278,319–373; применимые qcl-results-analysis и qcl-physics-audit. Using-superpowers прямо исключает dispatched subagent. Дети не создавались.

Ниже пути Results относительно `components/qcl-negf-results`, Research — `components/qcl-negf-research`.

| Файл | SHA256 |
| --- | --- |
| Results/src/qcl_negf_results/equilibrium.py | 3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6 |
| Results/src/qcl_negf_results/state.py | a8e96fc0edcc087aa71126dcbad57bc3ab2acdddbef4630b17c685dcafa7d323 |
| Results/src/qcl_negf_results/native.py | 892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b |
| Results/tests/test_equilibrium_diagnostics.py | ce35954b2503d7a910048d6e95bcc6b6b0c88eea40f8a018dc13bdf8ca4bbad0 |
| Results/src/qcl_negf_results/provenance.py | 50835460bcd1210f19c5f71b093215eb59c20538c7c1ce036b29299ad893f832 |
| Results/tests/source_ownership.py | 95b2a6811c3ea10c77efcc4c64d90bc6d1ef04e529d027f5a65eb7db00d501ea |
| Results/CONTRIBUTING.md | c228613ad22198b125128437aac6047de3c3e22885c5f5bb3ec3c71bb62be48c |
| Contracts/src/qcl_negf_contracts/artifacts.py | 639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa |
| Research/docs/equilibrium-measurement-contract.md | 758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f |
| /tmp/qcl-sci04-design-v2.md | d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c |
| /tmp/qcl-sci04-design-v2-review.md | ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1 |

D2 review: APPROVE bounded implementation contract, отдельно от CP-CODE/runtime/science. Его prose не является evidence нынешней реализации. D2 исторические refs не перенесены на current Results; current source hashes установлены отдельно.

## Цепочка определения и измерения

Owning Research:77–124 определяет orthonormal finite basis, общий μ/T, N=−iGL, P=iGG, A=i(GR−GA), W=gs*wE*wk/(2π), weighted full complex Frobenius norm; physical numbers /L0², current ×J0. В reducer сохраняются эти определения:

- `equilibrium.py:441–460`: q(E)=Σk W ReTr A; одна finite-spectrum μ с bracket. `:227–285` сохраняет endpoint/width/number residual; algorithm tolerance не physical tolerance.
- `:469–493`: GA=GR†, Nraw=−iGRΣLtotalGA, Praw=iGRΣGtotalGA; total складывает enabled scattering и embedding_total один раз. FDR обеих версий использует одну μ и полные комплексные matrices. A не пересчитывается как i(GR−GA); это независимая диагностика сохранённого A, не spectral-consistency check.
- `:494–526`: для каждой стороны `ΣG GL−ΣL GG`, weighted signed sum, ×J0. Minus outward переводится в common-z сменой знака; report отдельно даёт outward sum и max absolute boundary current. Balanced nonzero currents не принимаются за thermal zero.
- `:502–512`: occupied/empty numbers измеряются отдельно; donor residual только occupied. Отрицательное число сохраняется с issue; imaginary trace также сохраняется.
- `:124–135,527–531`: correction 0/0 имеет explicit measured0/reason; nonzero/0 undefined; при unavailable μ весь FDR получает null/inherited reason. Floors не добавляются.

## Property / assertion / independence matrix

Все строки ниже — static reading, ни одна не означает executed pass. Тестовые пути и line numbers относятся к выбранному Results commit.

| Свойство | Source locator | Manufactured assertion | Независимость и граница |
| --- | --- | --- | --- |
| Exact committed owner и receipt | state.py:299–344,131–155; equilibrium.py:306–310 | R34:576–579 corrupt owner; R36:589–593 receipt hash; helper:175–178 проверяет commit hash, identity, SHA bytes | Hash/receipt code — Results, не solver; fixture использует product artifact_row/json_bytes, поэтому не полностью независимый format encoder. Local publication/integrity, не remote durability |
| Run/attempt/plan/state binding | state.py:303–306; provenance.py:59–61; native identity required state.py:327–333 | R35:582–586 wrong attempt; fixture identity:24–25 содержит все 6 полей | При полном expected mapping все поля сравниваются type-strict. Wrong plan/state/sequence не имеют отдельных assertions в этом equilibrium-файле |
| Native schema/role/version | native.py:174–199 | fixture:116 declare_native; R27–29:458–493 проверяют доступ producer layout | Общие native fixture helpers доказывают compatibility с этой synthetic schema; не факт чтения настоящего producer archive |
| Full E,k,a,b real/imag, coordinates, units | equilibrium.py:361–382,435–439; state.py:380–403,432–499 | R05:266–268 wrong a/b labels; R29:479–493 values/axis/coordinates/weights | Static guards сильнее negative coverage: wrong units/coordinate linkage и реальные transposed bytes при неизменных labels отдельно не проверены этим suite |
| Nonnegative nonzero measures | equilibrium.py:409–417,427–433 | R08/R09:315–322 negative wE/wk; R12:338–340 NaN; R06:271–293 изменяет measure с retained target | Literal `math.fsum` :75–85 независимо от product `_Sum/_Norm`; здоровый control имеет неединичные WE/WK |
| Known common μ, number scale | equilibrium.py:227–285,441–460,502–512 | R01:189–222 known μ bracket, physical /1e−16, occupied and complementary empty values; R22:409–416 below bracket; R26:451–455 iteration cap | Fixture inverse2:48–50 и fd:53–54 не импортируют tested `_fit_mu`, `_number`, `_fd`; donor target вычислен literal number. Сам k-dependence fixture вырожден (same matrix на обоих k), хотя weights неединичны |
| Full-matrix normalized FDR | equilibrium.py:83–135,465,489–493 | R02:225–241 чистый off-diagonal Hermitian D с нулевым trace; exact independent numerator² и correction ratios | Healthy scalar trace не видит D; тест действительно требует coherences. Expected norm2 использует np.sum(abs²), не product LASSQ |
| Raw stored Σ matrix orientation | equilibrium.py:471–477 | R03:244–254 defect одного LO; R04:257–263 transpose LO | Expected GR получен closed inverse2; expected raw uses explicit analytic total+mutant и literal weighted sums. NumPy matmul общий численный primitive; это независимость от product reducer, не от BLAS/NumPy |
| embedding_total ровно один раз | equilibrium.py:472–474 | Fixture:133 fractions five×0.1 + total0.5; R01 raw number/FDR; R03/R04 expected explicit total | Если в raw добавить plus/minus (0.25 каждый), здоровый raw изменится; baseline assertions различают double count. Отдельный named mutant product reducer не выполнялся |
| plus/minus отдельно; outward signs и scale | equilibrium.py:494–526 | R02:235–241 nonzero analytic j>0, оба outward=j, minus common-z<0, balance=2j; R01 raw≈0 | J expectation задан literal expression через ΓD и независимый weighted sum. Raw nonzero-current exact value не asserted в R03/R04; это покрытие normalized nonzero J + raw healthy0, не полное raw-J mutation coverage |
| Five requested/stored inventory | equilibrium.py:328–359 | R13:343–345 missing enabled; R14:348–351 extra known; R16/R17:367–376 unknown/duplicate | Source запрещает unknown stored и incomplete embedding; Context enabled и stored должны совпасть, но requested=true не требует stored present (см. ниже R15) |
| Missing context/channel не0 | equilibrium.py:177–203,340–360,527–531 | R18:379–386 missing context→FDR null при measured numbers/J; R13 missing enabled→error | Missing entire context не даёт affirmative model. Partial model keys имеют static status branches, но не каждый branch отдельный test |
| LO thermal / zero drive / e–e none | equilibrium.py:182–203 | R19:389–393 finite drive; R20:396–399 unequal T; R21:402–406 unsupported e–e | Applicability минимального stored contract, не доказательство actual finite_chain4 production model/source |
| Zero denominator и missing μ | equilibrium.py:124–135,238–247,527–531 | R23:419–426 zero spectrum→FDR null и zero corrections; R24:429–440 nonzero/zero→undefined; R25:443–448 occupied/empty statuses независимы | Не превращает empty spectrum в equilibrium pass; direct full-FDR denominator0/nonzero-error branch недостижим при defined μ/positive capacity и не отдельный runtime control |
| Finite data and no acceptance inference | equilibrium.py:53–56,547–554 | R10:325–330 negative spectral q; R11:333–335 NaN GR; helper:174–175 allow_nan=False и отсутствуют pass/scientific_accepted keys | Assertions защищают report vocabulary, но не доказывают scientific success; no criteria evaluator здесь |
| Bounded I/O/workspace | equilibrium.py:146–154,383–405,532–554; state.py IO budget | R30–33:496–573, R27/R29 cap checks | Full-owner SHA обязателен; logical vs actual delivered bytes разделены. Workspace forecast не bound process RSS/OS disk I/O. Runtime данного раунда не измерен |
| SCI03 §5.3 measured current-bound coefficients | equilibrium.py:465–547 inventory | Отсутствует | Existing report не выдаёт Γ-side norms, δS-side norm, отдельные δN/δP FDR absolute norms и ‖δN+δP‖W; нельзя восстановить full bound из одного aggregate FDR ratio |
| D2 final audit portable record | state.py:326–344; native.py:174–199 | Отсутствует в selected paths | Не проверяются record_json↔commit equality/availability/context/state. Existing GR/Σ measurements всё ещё полезны; fresh-map provenance не сертифицируется |

Tests independence: test_equilibrium_diagnostics.py:16–22 импортирует Contracts constants, StateReader и fixture/serialization helpers. Tested equilibrium API загружается через importlib в `api():39–45`; expected arithmetic не импортирует его reducers. `source_ownership.py` проверяет выбранные пути state.py и Contracts artifacts.py, но не commit hashes и не equilibrium.py напрямую. Следовательно будущий C08 обязан отдельно привязать exact imports/env/commits к этой таблице hashes; pathname ownership не равен scientific source closure. Fixture thresholds из assertions не переносимы на full-device accuracy. Bound derivation для исторических test-specific 2e−15/2e−10 здесь не дополнялся новым научным threshold.

## Границы exact-final и all-five утверждений

1. `diagnose_stored_equilibrium:299–300` требует только nonempty expected_identity; StateReader:303–306 сравнивает только supplied keys. README:193–196 показывает лишь execution/point/attempt. Поэтому сама API может принять другой state_sequence/state_id/plan того же run, если caller их не передал. C07 в P1:253 требует все шесть; при таком вводе source exact-check есть. Это caller-precondition/hardening gap, не воспроизведённый сбой полного C07. Не следует ломать общий StateReader partial-selector API под видом audit; достаточно сохранить full-six precondition C07, а отдельный owning ticket может сузить именно diagnostics entrypoint и его example.

2. R15:354–364 намеренно оставляет scattering_alloy requested=true, удаляет alloy из context и storage, перераспределяет остальные stored contributions и ожидает healthy FDR. Это подтверждает actual-dictionary semantics, а не нулевой physical alloy kernel: нулевой kernel в тесте не вычисляется. Code:351–359 не требует равенства requested set и enabled set. Для all-five S1 отдельно проверять frozen model/context/native requested flags и фактические пять stored families; `applicable` не достаточен. При missing context reader вообще допускает неизвестные отсутствующие requested channels для stored numbers/J, сохраняя FDR not_measured.

3. Context hash-bound к commit/receipt, но truth model не установлена. StateReader хеширует physics.full owner, не читает/верифицирует model artifact bytes и frozen plan source. `native_verified` значит format/identity, не физическая корректность metadata. No source/runtime provenance of actual model/revision beyond предоставленного immutable commit не выводится. Exact sources/runtime и finite_chain4/all5/e–e none остаются отдельным BIND/READY gate.

4. Сохранённый A и Σ могут содержать согласованную общую ошибку; FD seed или synthetic equality не доказывает full QCL equilibrium. Reader не строит fresh scattering/embedding map, не измеряет outside-window tails, PSD/sum-rule/density/Poisson/inverse-Jacobian bounds или эксперимент.

5. `_internal_storage`, state.py:506–524, запрещает soft/external links, external и virtual datasets: все значения находятся внутри hashed owner. Owner проверяется через тот же открытый stream до HDF reads. Reader полагается на immutable-publication precondition и не делает файл OS-immutable/не блокирует чужую in-place запись; malicious/concurrent mutation после SHA не проверялась этим заданием. Это граница модели хранилища, не свидетельство наблюдённой гонки.

## Готовые owning dispositions

### SCI05-N1-RESULTS — READY по уже принятому D2; не новая design-сессия

- Вопрос/owner: Results, один implementer и отдельный R high; может ли reader структурно подтвердить exactly same portable final raw measurement record в native owner и commit?
- Входы: Results/Contracts/Research commits и hashes выше; D2 SHA d787… и approved independent review ae57…; owning Contracts validator/schema после его появления.
- Paths: D2:256–263 только `src/qcl_negf_results/native.py`, минимальная private интеграция `state.py` и bounded schema tests. Public string-reader/новый CLI не нужен; equilibrium.py не становится fresh map evaluator.
- Invariants: существующие numeric interfaces, owner SHA/I/O budget/native4 backward compatibility, все physical thresholds/model/grids. Нет scientific evaluator в reader.
- Oracle/acceptance: exact D2 §8.3–8.8. Fixed-width scalar ≤65536 bytes, bounded format before read; present copies match real state identity and all semantic fields exactly (Float64 parsed value); one-sided/contradictory→corrupt. absent+absent final→not_recorded, recovery→not_applicable/not_a_final_state. Healthy measured0, unavailable/null, invalid/vlen/oversize/NaN/duplicate key/wrong state controls по D2 §9.
- Проверка: source review + relevant bounded prepared tests по remaining root-assigned C08. Этот audit не разрешает новый test call и не расходует/увеличивает cap8; root распоряжается остатком.
- Dependency: Contracts pure structural validator/schema и Runner dual transport; пока они отсутствуют, implementing source scaffold не равен completed end-to-end check.
- Budget/stop: отдельная assigned finite I/R envelope до исполнения; no install/build/solve; stop на schema/source drift, missing portable contract/runtime или исчерпании assigned budget.
- Output: owning reviewed commit, hashes/receipts и per-control dispositions. Read-back record не называется fresh recomputation.

### SCI06-MEASURE-J — source-proven missing measurement; отдельный Results ticket

Research:216–246,395 уже задаёт формулу без guessed thresholds. Scope — append-only stored measurement к existing two-pass reducer, без fresh candidate/model changes: для каждой plus/minus и raw/normalized вычислить Γ=−iSL+iSG, δS=−iSL−fΓ, δN=N−fA, δP=P−(1−f)A и absolute weighted norms, включая ‖δN+δP‖W; B=J0[‖(1−f)Γ‖W‖δN‖W+‖fΓ‖W‖δP‖W+‖δS‖W(‖A‖W+‖δN+δP‖W)]. Сохранить measured coefficients/status/units/source binding, не восстанавливать absolute numerators умножением rounded ratio на denominator. При μ unavailable dependent coefficients/B unavailable, существующие numbers/J сохраняются.

Healthy and negative oracle: literal inverse2 и literal weighted sums (D2 §9 fixture допустим как algebra fixture, не thermal fit); noncommuting 2×2, off-diagonal δN/δP, nonzero δS, nonunit weights, wrong transpose/sign/measure, exact zero factors, missing μ. Явно проверить |complex represented J|≤B с объявленным fixture arithmetic error budget; Bmatrix D2 не переносится автоматически на arbitrary new pipeline. Считать coefficient norms measured даже если B слишком велик; εJ/scientific acceptance остаются owning Research unknown. Product `_Norm/_Sum` не используется в expected calculations.

Formula/source scope достаточны для owning D→I ticket; exact report fields и arithmetic bound для расширенного oracle нужно заморозить в этом ticket до code/test, не импровизировать их в SCI06 audit. Final schema D2 касается fresh record и не задаёт output schema этого дополнительного stored-current reducer. Поэтому **не объявляю этот ticket I-READY на несуществующем exact report contract** и не создаю third D2 round. Дешёвый следующий шаг — короткий additive measurement contract от Results на базе SCI03, с последующим independent R; test calls только остаток assigned C08/новый явный envelope.

## Уровни evidence и завершение

| Уровень | Статус этого задания | Почему |
| --- | --- | --- |
| Source/contract | Подтверждены перечисленные control-flow/formula/guard/test-assertion свойства | Pinned clean Results + hashes + точные locators |
| Prepared runtime | Не измерен здесь | Ни imports, ни pytest, ни Julia не запускались; старые import receipts не перенесены |
| Stored final C07 measurements | Данных недостаточно | Нового final commit/owner/receipt/run-state arrays нет; старый S01 не читался |
| Сходимость уравнений | Неизвестна | Stored Σ reconstruction не fresh map; source/test assertions не numerical run |
| Physical gates | Неизвестны | Нет final measurements и finite justified ε/bounds |
| Достаточность дискретизации | Неизвестна | No comparable converged refinements/tail/basis bounds |
| Экспериментальная валидация | Неизвестна | No experimental comparison input |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Full-matrix FDR/numbers/J реализованы в независимом stored reader | Results e2fdeda + matrix выше; literal inverse2/sums не импортируют tested reducers | Source/tests прочитаны, runtime не исполнен | сохранить |
| Actual immutable final успешно прочитан | Нет artifact/run/attempt arrays, C07 не выполнен | Receipt fixture не real final | данных недостаточно |
| Reader success доказывает все пять S1 channels | R15 и equilibrium.py:328–359 | requested≠stored разрешено; модель проверяется отдельно | дополнительно измерить |
| D2 final raw record проверен reader | Отсутствуют record locators/cross-check в native.py/state.py | Legacy readability сохранить | изменить |
| Represented-current bound SCI03 §5.3 измерен | Отсутствует coefficient inventory в equilibrium.py:465–547 | Formula known, exact additive output/oracle contract ещё не frozen | изменить |
| Численная/научная приёмка достигнута | Только source evidence | Нет runtime/final data/finite accuracy and domain bounds | данных недостаточно |

Выполнено только bounded read-only Git/text/hash чтение; создан только этот `/tmp` report. Никаких Python/Julia imports, tests, postprocessing, solver, setup, network/server/Git mutations. Никаких scientific payload reads. C08 calls consumed: 0. STOP: source-audit вопрос завершён; dependent runtime/science claims сохранены unknown, исправления не выполнялись.

Финальная повторная проверка: Results `git status --short` пуст; четыре SHA equilibrium.py/state.py/native.py/test_equilibrium_diagnostics.py совпали с initial manifest. Source drift выбранного Results не обнаружен. Отчёт хранится отдельно от original artifacts.
