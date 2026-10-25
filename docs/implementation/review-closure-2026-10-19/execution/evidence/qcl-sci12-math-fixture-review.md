# SCI12-MATH-I1 F — independent high fixture source review

2026-10-20. **Нужен узкий F2 до Root RED:** per-test call-phase NEW_API_MISSING assertion и legitimate len-only Sequence no-read count control. Блокирующих ошибок в проверенных literal expected values или восьми-helper scope не найдено. Это fixture source review,не observed RED/PASS,не implementation approval,не all-guards coverage и не scientific verdict. До Root RED никакой code/import/test в данном review не запускался.

## Frozen inputs и фактический scope

Worktree `/tmp/qcl-sci12-math-results-worktree`,actual Results HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`; единственный status entry — untracked `tests/test_equilibrium_map_math.py`. Module `_equilibrium_map_math.py` отсутствует по filesystem existence check. Product source не создан.

Fixture16161B,SHA256 `5e30ef6337374f281681e80e9dc94512043d7f4ee87890f2107d8973f003e1ce`;author report SHA `076d761054386ebbd223f89b79032144237f245d36bc7f362416b6d37dd64efa`;identity SHA `b0a96b213fff49b7514ee1267ab6a1ce10feafd11225b5e92f446eb1c4f29699`;patch SHA `3f69757c5187913c636c35e601004fe4b2ffa9b32d4e2ab7cbc6512f6ef84e36`. Accepted primary authority: MAP D2 `5473c96d80ad44c1b045008c7fa1aa6055502b05681700d4191c54b46f42db17`,OPS D1 `82a2fbc34cbfc2c6d879a160122362e54dc48586dca4153ae5229ff60ce93a3e`,independent OPS review `3f0d7aa11fbc66cb3dbc5e66a0604d22eacb2e6705de165a4e1cc89198bd68d3`. Применены сохранённые qcl-physics-audit/AGENTS/source-stage rules.

## Номинальный состав и будущий RED

Ручной подсчёт decorators/source подтверждает **26 test functions,96 prospective cases:2 independent literal controls+94 api-dependent**. Parametric groups дают8 hats,7annuli,4overlaps,4restrictions,6bad-domain,5density/bond variants,14scalar invalid,8invalid planes,8matrix outputs,7density invalid,10bond invalid;остальные singleton functions дают оставшиеся cases. Collection не выполнялась,поэтому это nominal source count,не pytest-collected count.

Fixture:23–37 проверяет actual selected Results package file до find_spec,exact prospective module origin и imported candidate origin после import. Package `src/qcl_negf_results/__init__.py` на выбранном source содержит только docstring/version; API не импортируется на module collection. Module lookup возвращает explicit NEW_API_MISSING только если spec=None;missing helper также явно assertion NEW_API_MISSING. Broad except,skip,xfail,stub/sys.path mutation отсутствуют. Package path mismatch,missing dependency или candidate import exception остаются отдельными реальными errors,не маскируются как absent API. Standard pyproject `testpaths=["tests"]` обнаруживает файл.

**Уточнение receipt classification:** NEW_API_MISSING возбуждается внутри pytest `api` fixture setup,а не test-call body. При корректном prepared runtime/выбранных package sources и отсутствующем новом module прогноз — **94 per-case setup ERROR с NEW_API_MISSING и2 literal controls**,не94 доказанных behavioral failures. Это не collection crash и не pre-existing physics regression. Author слово «failures» следует понимать только как общий прогноз non-green;Root receipt обязан сохранить actual pytest stage/status и не переписать setup ERROR как numerical behavioral RED. До исполнения ни setup outcome,ни2PASS здесь не заявляются.

## Primary assertions и независимость oracle

| Assertion locators | Независимое expected и различаемая ошибка | Оценка |
| --- | --- | --- |
| 60–70 | Dyadic normalization/sign/partition controls без api | Контроль expected arithmetic,не product test |
| 73–101 | Hat coefficients0.125/0.375,clips,full/partial signed integral0.75+3+2.25=6 | Drop strips/endpoint misuse/extrapolation различимы |
| 104–124,369–383 | Annulus squared areas27/16,13/16,weighted numerator53/8;overlap17/4 и uncovered strips | Extraπ/dropped partial cells различимы;weights factor намеренно вне helper |
| 127–155 | Signed2→1 cell restriction,zero/cancellation,sheet6;changed domain/nonuniform/empty/missing invalid | Uniform same-period applicability сохранена |
| 158–180 | A=[[1,i],[0,2]],B=[[2,0],[i,1]];AB=[[1,i],[2i,2]],A†A=[[1,i],[-i,5]],Gram diag1,4 | Product order,conjugation,coherence,renormalization различимы |
| 183–193,349–360 | Rectangular S=[I2,0],retained density1/2/3;rank1 Gram ones;3×3 known0 | Не объявлены inverse/projector/outside-basis proof |
| 196–228 | Coherence J−3/conjugate+3/offdiag0J0;complex unitary;dx1/4 n8/4,J−3 иwrongχ J−12/wrongΦ sheet3/4 | Φ/χ normalization теперь различима |
| 341–346 | χ rows(1,±i),M given,L0=2:forms4,2 divided by8→0.5,0.25 | Conjugation иL0³ scaling различимы |
| 231–338,363–366 | Invalid scalar/plane/output/finite-overflow cases | Refusal ожидается;atomic output rollback не обещан |

Матрицы AB,A†A,unitary covariance,density row contractions иbond signs адресно перепроверены вручную в source/prose. Никакой arithmetic code не запускался. Expected side — written literals и elementary dyadic checks;`plane`/`output` только создают prospective inputs/buffers. Нет expected через tested helper/Core/reference/optimized kernel,BLAS,@,einsum,norm/eigen/sqrt/pi/exp. Composition helper calls в actual-side hat/annulus/overlap totals не делает expected shared oracle. Matrix input snapshots158–165 проверяют ownership/nonmutation.

Strict package/module origins являются source-selection guard,не арифметическим oracle и не доказательством отсутствия будущих forbidden imports. Actual implementation import graph остаётся отдельной source-I review obligation.

## Negative guards: что покрыто и что остаётся неизвестным

Covered source assertions:Bool geometry/scales/cbar,negative radii/scales/masses,nonfinite inputs/intermediates,zero width/denominator context;invalid dtype/object/list/noncontiguous/shape/empty planes;input-output alias,real/imag component alias,readonly output,wrong output length;finite overflow in product/density/bond. Все prospective constructed numerical arrays не больше3×3,нет поддельных огромных ndarray shape или большого payload. Никаких new count/weight API fixture не требует.

**Count/shape-product guard не покрыт executable case.** Author report честно сохраняет это gap. У этих восьми API нет scalar count/weight arguments;negative quadrature weights относятся к future weighted/native adapter,а не доказываются negative radius/mass test. Нельзя назвать эти branches passing по96cases. Readonly/alias guards проверяют отказ,не transactional rollback partially written outputs.

Самый дешёвый дополнительный count control без нового helper API и без большого array возможен через legitimate `Sequence` для `_restrict_cells`:source-edge length194 иvalues length193 уже превышают accepted192cells cap;target edges length2. Metadata-only Sequence возвращает этот valid bounded `__len__`,а `__getitem__`/iteration имеет sentinel AssertionError. Expected — ContractError **до первого element read**. Можно также применить valid __len__=sys.maxsize,не вне Python length range;это проверяет ранний cap отказ,не требует materializing values. Не запускалось и не добавлено данным review;после изменения fixture нужен новый SHA/nominal count.

Такой case не докажет overflow всех ndarray shape products. До GREEN/source-I acceptance требуется primary source predicate actual implementation:dimensions изreal ndarray shapes и Sequence lengths;Python-int products;comparison с owning shape/cell cap иmin(sys.maxsize,limit) **до allocation/range/element read**;no int64 wrap/implicit copy. Его можно проверить source без невозможной legitimate огромной C-contiguous array. Не вводить validator API только ради теста и не приписывать counterfeit ndarray evidence.

До Root RED зафиксировать **минимальный F2 ticket**,без product edits/stubs/нового API: (1) добавить existing `_restrict_cells` count-cap negative с len-only194edges/193values и sentinel запретом любого element read; (2) перенести NEW_API_MISSING presence/callable assertion из fixture setup в assertion,вызываемый явно test-call body каждого API-dependent test. Fixture по-прежнему проверяет selected package/module origin и import dependencies в setup;wrong package,dependency/import/context mismatch остаются ERROR/blocked. При genuinely absent new module fixture может сохранить только факт отсутствия,а per-test assertion обязан FAIL с NEW_API_MISSING,не имитируя product object или callable. Existing literals/guards не ослаблять,skip/xfail/broad catch не добавлять.

F2 должен получить новые hashes и независимый source recheck/nominal count до Root invocation. Номинальная цель после F2:2literal controls плюс API-dependent assertion FAIL при отсутствующем новом API;число API cases надо пересчитать по фактическому F2,а не автоматически оставить94. Actual collected/pass/fail/error count остаётся будущим measured receipt. Это engineering structural new-API RED,не pre-existing behavioral/physics defect. Молчаливое изменение fixture между review иRED недопустимо.

## Граница результата

Scope ровно accepted8helpers;generic χ/Phi residual/norm/interval/projector,PAIR-I2/N0/native/source/criteria bindings не добавлены. Идеальные dyadic equalities не являются scientific tolerances или outward enclosure. Model0mV/70K,all5,noe–e,finite_chain4,13/936/P1 caps иC08=8/8 сохранены. Product87 counter не изменён этим review;никакого нового product/test invocation нет.

Только named source/text/read-only Git/hash/size и два /tmp review outputs;no subagents,scripts/parser/compiler/imports/math execution/numerics/HDF5/tests/Julia/solver/network/source/CP edits. Source content conservative≤1MiB при cap3MiB,outputs≤96KiB;CPU/RSS/syscall IO не измерены. No source mutation вResults илиRoot. Module/test syntax иpytest collection не проверялись исполнением,поэтому any runtime issue остаётся actual future receipt,не ложный PASS.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Literal fixture имеет независимые различающие controls | Primary assertions60–383 иaccepted8helper contract | Executed cases0 | сохранить |
| Номинальный состав96cases корректен | Manual decorators26functions,2+94 | Collection count ещё не измерен | сохранить |
| Missing API даёт structural RED route | Per-test fixture23–37,module absent | Prospective setup ERROR,неexisting physics failure | дополнительно измерить |
| Все count/negative-weight/native guards verified | Count/weight APIs отсутствуют,source predicate ещё будущий | Не covered/non-PASS;valid Sequence control возможен | данных недостаточно |
| Scientific/native readiness достигнута | Новых scientific/native artifacts нет | Только fixture source approval | данных недостаточно |

STOP. Следующая работа — только narrow medium F2 по двум пунктам выше,затем frozen source recheck и отдельно authorized Root RED;implementation пока не создана.
