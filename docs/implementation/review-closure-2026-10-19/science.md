# SCI01–SCI15: автономный scientific handoff

2026-10-19: **PLAN; S1 без e–e согласован, approved_standby; EXEC не активирован**.
[P1](operator-permissions.md) фиксирует прямой ответ оператора и имеет приоритет
по разрешениям и caps. Solver/imports/tests/install/
benchmark/build/серверные действия здесь не выполнялись. Пользователь подтвердил:
сервер недоступен, работ после review не было. Цель будущего этапа — closure
RV01/08/09/10 и конечная попытка physical acceptance; положительный исход не обещан.
Cluster/worker gates — в [общем плане](../review-closure-2026-10-19.md).
Использовать существующие Runner/AiiDA/Results wrappers, без нового registry/service.

## Источник и общий контракт карточек

Прочитан root `93880c23bca889ddcb8b98edb995080b332dd99f`, gitlinks сверены;
начальный status: untracked общий план. При activation снять C00 на source S,
проверить locators/dirty overlay; gitlinks — состав, не второй ручной lock.
Не обновлять submodules до latest и не повторять весь аудит 34 operators.

Входы: [архитектура](../../architecture.md),
[entrypoint](../../system/implementation-entrypoint.md),
[role policy](../../system/release-roadmap.md#политика-ролей-и-координации),
[milestone](../../system/scientific-milestone.md),
[RV01/08/10](../../system/autonomous-review-formal-science.md),
[RV09](../../system/autonomous-review-engineering.md#rv09--tests-свойства-и-независимость-oracle),
четыре QCL skills. Grants из `autonomy.md`: PLAN, DEV, PUBLISH, READ_NATIVE,
BUILD, OPS, SCI различаются; CP-NATIVE технический, не scientific pass.

**P наследует каждая карточка:** S+gitlinks+overlay hash; producer/runtime/imported
source отдельно; model/scattering/algorithm identity; ordered config sources,
assigning histories/typed defaults; exact plan bytes/SHA256/plan_fingerprint,
реальные configuration/problem/physics fingerprints с семантикой; run/WorkChain,
execution/variant/point/CalcJob UUID, attempt/state_id/state_sequence; commit/receipt/
payload hashes, schema/profile/completeness. Design run=not_created; missing=null+
reason, не 0. Source/seed/grid/plan change — новая identity+causal predecessor;
resume сохраняет plan/consumed iterations. Evidence: commit+symbol либо hash+HDF5
path+slice+units+transform/source hash+read budget.
Роли: **D scientific design Sol ultra; A/R audit/coordination/independent review
high; I ready code contract medium**. Actual Sol ID/ultra support фиксировать
при activation. Frozen D→I→новый независимый R; сейчас всё PLANNED.

| Owner / prefix путей | Адресные источники |
| --- | --- |
| Research R=`components/qcl-negf-research/` | `config/{equilibrium.yaml,studies/equilibrium-0-70.yaml,model/reference-2019-70k.yaml,policies/analytical-diagnostic.yaml}`; `docs/{equilibrium-s01,scientific-inputs}.md`; `literature/reference-2019/{source.yaml,structure.csv,negf_iv_digitized.csv}` |
| Core C=`components/QCLNEGF.jl/` | `src/numerics/reference/{final_audit,acceptance_metadata,validation,poisson}.jl`; `src/numerics/optimized/{production_solver,physics_markers,production_cache}.jl`; `src/physics/observables.jl` |
| Runner N=`components/QCLNEGFRunner.jl/` | `src/{cli.jl,application/auto_strategy.jl,application/resource_contract.jl,application/scientific/planning.jl,infrastructure/persistence/physics_diagnostics.jl}`; `docs/src/user/{configuration,resources,results}.md` |
| Results V=`components/qcl-negf-results/` | `src/qcl_negf_results/{equilibrium,state,native,model,cli}.py`; `tests/test_equilibrium_diagnostics.py` |
| AiiDA/Platform | `components/qcl-negf-aiida/src/aiida_qcl_negf/{service,workflow,recovery,parser}.py`; deployment runbook |

## Declared model и происхождение

Default initial CP-SCI candidate — existing ordinary `equilibrium-0-70`,
research/stationary, independent **0 mV/period, lattice/LO70 K**, не 48 mV bundle.
Preset56 mV/Core200 K не effective inputs. Сохраняются:

- Структура 3.26/7.99/1.90/8.40/2.90/5.16 nm, Al0.25, doped2.90 nm,
  sheet4.5e14 m^-2, ionization1/spin2; thermal LO/fixed screening/parabolic/e–e none.
- Все 5 scattering: LO/acoustic/impurity/IFR/alloy, alloy0.60 eV/cell4.5168e−29 m³.
- Явное решение оператора: **electron–electron scattering = none** для всего
  каталога, repairs и H. Это сохраняет baseline; e–e не является одним из пяти
  перечисленных каналов и не добавляется автономно.
  До submit каждой variant проверить effective `electron_electron=none` в
  resolved plan/runtime model identity; missing/необъяснённый mode блокирует
  submit, а не принимается как неявное отсутствие рассеяния.
- Nb5/basis periods3/Nz96, NE30721/[−0.30,0.90] eV/trust80 meV,
  Nk11/kmax0.60 nm^-1, angular32/qz81/max10 nm^-1.
- Production auto_exact/full self-energy/resolved k/sparse_plan/FFT/paired_convex;
  finite_chain embedding4; SCBA2048/Poisson128, mixing0.2/0.15/adaptive_working,
  existing strict thresholds/confirmations; seed1.25 meV.
- Full final/projections/optical=false; recovery1800 s/retain2/8 GiB/reserve64 MiB,
  telemetry256. Iteration limits не compute grant.

Seed/normalized number/нулевой J не stationary solution. Elastic acoustic/static+
LO transfers не доказывают thermalization произвольного initial. Seed linewidth
не физическая. Adaptive inner return не strict final convergence.

**Unresolved provenance:** review `R/RV10.md` U04 и
`reviews/paper-unit-visual-check.md` сообщали cm^-2 main p.3 vs cm^-3 caption p.4;
primary PDF отсутствует, screenshot failed/cache-miss. Это secondary finding,
не доказанная physical error. Паспорт DOI10.1063/1.5110305/arXiv1911.06582 проверить
по actual primary version/metadata. 4.5e10 cm^-2=4.5e14 m^-2 верно при sheet
interpretation, конфликт не решает. Declared dose сохранять с caveat; изменение
модели — human decision. Material/scattering values имеют own origins/assumptions.

## Нормы и основания до acceptance

Каждая карточка: **question→assumptions/equation→discretization/function→observable
→norm/weights/units/near-zero→criterion basis→evidence**. SCI03 выводит thresholds
из error budget, затем R high; universal1e-4, FD seed/голос оператора не основание.
Existing strict tolerances не ослаблять, archived Core assessment не переписывать.

Первичные formulas проверить адресно, здесь contents не проверялись:
[FD2.30–31](https://www.iue.tuwien.ac.at/phd/smirnov/node25.html),
[FDR42](https://www.acsu.buffalo.edu/~hffotso/MyPapers/FrontiersPhys_FDT.pdf),
[Lee–Wacker B2/II.A](https://arxiv.org/pdf/cond-mat/0212059),
[Wacker2–3](https://arxiv.org/pdf/0706.4202),
[Baym](https://doi.org/10.1103/PhysRev.127.1391),
[Bosco](https://arxiv.org/pdf/1911.06582).
Receipt URL/version/hash/page/formula/applicability; inaccessible source=gap.

| Observable | Norm/units/near-zero и criterion basis |
| --- | --- |
| Fresh SCBA | `fresh_fixed_point_metrics`: r_D_candidate/r_A_candidate/r_K/max-family r_Σ/raw/candidate λ. Actual unweighted block/array norms+floors из C acceptance_metadata; candidate не нормировать λ. Unmixed scattering+embedding map того же final U/G; backward residual не forward-error bound |
| Outer/Poisson | r_U=max abs(Umap−Ufinal), physical r_U·E0(eV); r_n=∥Δn∥wZ/(NDsheet/√Lp), bordered r_P/gaugeζ, neutrality abs(ΣwZ(ND−n))/NDsheet. Одна published density/U/G, positive target, missing/zero invalid без guessed floor |
| FD/FDR | A=i(GR−GA), N=−iGL,P=iGG; W=gs/(2π)wEwk native dimensionless, без двойного spin/2π. η²=(∥N−fA∥W²+∥P−(1−f)A∥W²)/∥A∥W²; full matrix, raw/normalized, одна μ70 K. Denominator0/error0 explicit zero, error≠0 undefined; fit μ не acceptance |
| Charge/corrections | Stored/candidate raw/normalized occupied+empty; sheet /L0²(m^-2), λ−1 dimensionless, occupied/empty matrix corrections отдельно. Donor residual только occupied; empty null/not_applicable с measured number |
| J=0 | max(abs J±), abs(Jplus+Jminus), imaginary parts в A/m²; outward electron-flow/common-z signs явны. Absolute εJ_abs из propagation/quadrature/tail/basis resolution, без division/J. Balanced ненулевые fluxes не zero-current |
| Spectrum/balances | Hermitian PSD A,−iGL,iGG; ΣwE A/(2π)→I по k; signed collision integral до модуля, active power/boundary terms. Tail≠quadrature; finite basis/local current. Не требовать J(z,E)=const, gain>0, monotonic I–V/bias symmetry без вывода |
| Sensitivity | μ(eV), n(z)(m^-3), sheet(m^-2), U(eV), J(A/m²), FDR/corrections/tails; gauge/basis mapping/common-domain+tail. Только individually converged same-model states, labels без mapping не populations comparison |

SCI03 задаёт target Q/error budget εiter+εenergy+εwindow+εk+εbasis/z+
εquadrature+εroundoff. Квадратичное сложение uncertainty — только при доказанной random
independence; discretization bias не random. Unknown coefficient→provisional
bound/конкретный measurement, full accuracy unknown; pilot по frozen strict
contract возможен. Richardson order не из 2 точек. После pilot новые criteria
version требуют held-out confirmation, не retroactive pass.

## Initial CP-SCI и finite waves

**CP-SCI policy approval уже получен:** S1 без e–e, полный finite catalog и caps
из P1. После отдельного EXEC author+independent reviewer закрывают технический
READY: frozen model/assumptions/criteria hash либо pilot unknowns, transitions,
attempts/recovery/CPU/RAM/wall/bytes/guards/stop. Фактические bindings и выведенный
обоснованный criterion не требуют нового human approval в пределах P1.
**CP-SCI-RESULT** — technical independent review immutable P, не human vote.
Новый model/boundary, weaker criteria/unknown physical interpretation/cap overrun
→человек с concrete proposal. Same-physics approved fixes/variants автономны
в remaining slots; большой денежный бюджет не infinite attempts.

| Slots | Delta к B0, отдельный frozen plan | Cap |
| --- | --- | --- |
| W1 B0 | Existing equilibrium | 1≤72 h |
| W1 E1 | NE61441=2(30721−1)+1, same [−0.30,0.90] eV | 1≤72 h |
| W1 P1 | [−0.29998046875,0.90001953125] eV/NE30721; half-cell19.53125 μeV, sameΔE39.0625 μeV | 1≤72 h |
| W1 K1 | Nk21/same kmax0.60 nm^-1 | 1≤72 h |
| W2 W/Z/B/A/Q | По одной оси: window[−0.45,1.05]/NE38401 sameΔE; Nz192; Nb7; angular64; qz161/max10 | До 5≤360 node-hours |
| W3 C | kmax0.9/Nk16 same radial step; energy_max1.2/NE38401 для coverage. Coupled cutoff/window, compare отдельный W | До 1≤72 h |
| R | Cause-specific reviewed corrected source/approved variant | До 2≤144 node-hours |
| H | Frozen final candidate/criteria, заранее held-out initial/phase protocol | До 1≤72 h |

W1 **4 attempts/288 execution node-hours**, без automatic retries; весь каталог
при initial approval **13/936**, не прогноз сходимости. B0 первым; failure blocks
accuracy refinements до cause review. Один node/threaded Julia process, BLAS1;
fresh CPUs/RAM, allocated core-hours=Σallocated CPUs×charged wall, actual CPU/queue
отдельно. CP задаёт deadline/concurrency/reserves; parallelism grant не умножает.
Принят весь conditional S1, а не только W1; для него обязательны P1 concurrency≤2
и byte ceilings. Combined final config не возникает из «лучших»
чисел автоматически. H не для подбора thresholds; unmeasured axis unknown.
Embedding4→8 — boundary-model sensitivity вне numerical pass/default cap,
новое human model decision.

## Admission/guards

Fresh host/VM/cgroup/cpuset/quota/allocation/foreign reserves, Code/release/storage
даёт platform линия; four roles/nginx/native worker/trust/staging/restore/CI
свои gates. Одна B0 ComplexF64 array16×30721×11×5²=135172400 bytes≈129 MiB.
Rough B0 **12–13 GiB**, E1 **24–26 GiB**, не measured RSS/request. Exact estimator+
Julia/native/allocator/HDF5/fresh-audit headroom обязательны; calibration имеет
отдельный finite cap. Auto_exact меняет equivalent chunks/workers, не physics.

Recovery8 GiB нельзя считать достаточным: pending generation/receipt/pointers
до prune при 2 retained; finals/logs/attempt/retrieval/export отдельно. SCI07:
uncompressed inventory×cadence1800 s×72 h, peak resident и duplicates per filesystem,
early durable-stop reserve; cumulative writes/reads/hashes/logs/telemetry/common
allocation accounting через existing jobs/receipts. Quota≠cumulative writes,
io.stat может не покрывать NFS — coverage/storage-side guard. Guard перед growth/
phase и external log enforcement; нет counter→needs_guard, не READY. Raw/failures
не удалять, ENOSPC/OOM не штатный stop, grid/basis/channels ради RAM не урезать.

Утверждённые resource ceilings — **P1/S1**, не measured capacity: W1 per execution
resident128 GiB/writes2 TiB/reads4 TiB/log1 GiB; W2/W3/R/H resident256 GiB/
writes4 TiB/reads8 TiB/log1 GiB. Shared campaign resident2 TiB/writes44 TiB/
reads88 TiB/logs13 GiB, включая retrieval/export duplicates. SCI07/08 доказывают
достаточность и enforceability до READY. W1-only 1 TiB/8 TiB proposal не выбран;
молчаливое изменение caps либо capacity assumptions запрещены.

## Будущие команды/API: сейчас не выполнять

Variables из P/admission, outputs fresh, private UUID вне Git. C00 root:
`git rev-parse HEAD`, `git status --short`, `git submodule status --recursive`,
`git ls-tree HEAD components/`; server read-only `GIT_OPTIONAL_LOCKS=0`.

**C01** root planning; variant meta ещё создаётся owning Research:

```sh
qcl-negf plan components/qcl-negf-research/config/equilibrium.yaml --max-runs 1 > "$SCI_WORK/B0.plan.json"
qcl-negf plan "$SCI_VARIANT_META" --max-runs 1 > "$SCI_VARIANT_PLAN"
```

Effective inputs/fingerprints/controlled_paths проверить; plan exit0 не solve.
**C02** runtime-only `qcl-negf self-check --directory "$SCI_CHECK_DIRECTORY"`:
three-node PV+tiny HDF5, не SCBA/Poisson/physical acceptance.

**C03** actual AiiDA `service.submit_plan`; один submit, не duplicate C04:

```python
from aiida import load_profile
from aiida_qcl_negf.service import submit_plan
load_profile()
run = submit_plan(plan_bytes, code_uuid=code_uuid, resources=resources,
    label=label, release_id=release_id, max_attempts=1,
    retry_backoff_seconds=0, archive_byte_budget=archive_verify_bytes)
```

Python inputs выше — exact frozen/admission fields P, не defaults; сохранить returned UUID.

Resources: machines1/task1, fresh CPUs/RAM/wall≤259200 s. Explicit attempts1;
timeout unknown→найти CalcJob, не resubmit. Recovery direct durable output;
wave transitions — existing Codex wrappers.

**C04** backend run/resume, не обход AiiDA:

```sh
qcl-negf run-plan "$SCI_PLAN" "$SCI_OUTPUT" --execution-id "$SCI_EXECUTION_ID" --attempt "$SCI_ATTEMPT" --archive-byte-budget "$SCI_ARCHIVE_VERIFY_BYTES"
qcl-negf run-plan "$SCI_PLAN" "$SCI_NEW_OUTPUT" --execution-id "$SCI_EXECUTION_ID" --attempt "$SCI_NEW_ATTEMPT" --recovery-bundle "$SCI_VERIFIED_RECOVERY" --archive-byte-budget "$SCI_ARCHIVE_VERIFY_BYTES"
```

Verified compatible whole generation, unchanged plan/runtime, new attempt>source,
consumed iterations сохраняются. submit_plan не имеет external recovery-bundle
аргумента: доказанный WorkChain route либо узкий owning handoff ticket до resume,
без выдуманного API. Independent new UUID/attempt1+causal link тоже тратит slot.

**C05** exact наш attempt:

```sh
qcl-negf pause "$SCI_OUTPUT" --execution-id "$SCI_EXECUTION_ID" --attempt "$SCI_ATTEMPT"
qcl-negf verify-pause "$SCI_OUTPUT" --execution-id "$SCI_EXECUTION_ID" --attempt "$SCI_ATTEMPT" --archive-byte-budget "$SCI_ARCHIVE_VERIFY_BYTES"
qcl-negf verify-stop "$SCI_OUTPUT" --execution-id "$SCI_EXECUTION_ID" --attempt "$SCI_ATTEMPT" --archive-byte-budget "$SCI_ARCHIVE_VERIFY_BYTES"
```

Stop proof: scheduler terminal/receipt/dependencies, только наши jobs;
no final→explicit absence. **C06**, actual status:

```sh
qcl-negf-results preview "$SCI_OUTPUT" --profile full-state --status "$SCI_JOB_STATUS"
qcl-negf-results export "$SCI_OUTPUT" "$SCI_EXPORT" --profile full-state --status "$SCI_JOB_STATUS" --byte-budget "$SCI_EXPORT_BYTES" --reserve-bytes "$SCI_EXPORT_RESERVE"
qcl-negf-receive verify "$SCI_ARCHIVE" --receipt "$SCI_RECEIPT"
```

Preview metadata≠payload; export отдельный I/O grant, лишняя копия не нужна.
Historical multipart — compatible reader.

**C07** existing API, CLI diagnose отсутствует:

```python
from qcl_negf_results.equilibrium import EquilibriumReadLimits, diagnose_stored_equilibrium
report = diagnose_stored_equilibrium(final_commit,
    expected_identity=identity,
    limits=EquilibriumReadLimits(**approved_read_limits))
```

Inputs из P/read admission; JSON report сохранять derived отдельно, allow_nan=False.

Expected identity execution/point/attempt/plan_fingerprint/state_id/state_sequence.
I/O mandatory owner hash+2passes, не selected bytes. Defaults NE65536/Nk128/Nb16/
channels5/workspace32 MiB/read+chunk1 MiB/report64 KiB; axis cap не RSS/I/O grant.
Stored Σ reconstruction **не fresh map**/acceptance; context defaults не придумывать.
HDF5 `/state_dimensionless/{GR,GL,GG,A}`,
`/selfenergy_dimensionless/{LO,acoustic,impurity,IFR,alloy,embedding_total,embedding_plus,embedding_minus}/{SL,SG}`,
`/grids_dimensionless/{energy,wE,k,wk,state_index}`, inputs/numerical_inputs/scales;
real/imag, E,k,a,b, units/coordinate linkage проверить.

**C08** future selected tests, source-bound prepared environment:

```sh
julia --startup-file=no --check-bounds=yes --project=components/QCLNEGF.jl/test components/QCLNEGF.jl/test/numerics/fresh_candidate_residual.jl
julia --startup-file=no --check-bounds=yes --project=components/QCLNEGF.jl/test components/QCLNEGF.jl/test/physics/analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl
julia --startup-file=no --check-bounds=yes --project=components/QCLNEGF.jl/test components/QCLNEGF.jl/test/physics/production_lo_equilibrium_discretization.jl
python -m pytest components/qcl-negf-results/tests/test_equilibrium_diagnostics.py
julia --startup-file=no --check-bounds=yes --project=components/QCLNEGFRunner.jl/test components/QCLNEGFRunner.jl/test/infrastructure/bounded_portable_recovery.jl
julia --startup-file=no --check-bounds=yes --project=components/QCLNEGFRunner.jl/test components/QCLNEGFRunner.jl/test/contracts/archive_dependency_budget_preflight.jl
```

C08: prepared source-bound runtime, missing deps=stop без install/build. Existing
portable PR6 до Results tests; anchors не QCL acceptance. Общий SCI05/08 cap8
процессов≤10 min/2 CPU/4 GiB/log8 MiB. **C09** actual `qcl-negf compare CATALOG.csv
OUTPUT --reference-id ID` / `qcl-negf analyze RESULTS OUTPUT`: bounded derive,
coordinate atol не accuracy, full-matrix reducers SCI12 отдельно.

## Карточки

Каждая наследует P/declared model/5channels/norm table/command contracts.
A/D read-only default≤1 h/1 CPU/2 GiB/64 MiB metadata/64 KiB report; литература≤128 MiB.
Numerical/derived work только SCI07/CP-SCI. Test cap общий, агенты его не умножают.

### SCI01 — отделить историю старой попытки от нового опыта

**A/R high; owners Results/Research.** Вход P, RV01, receipt
`canonical-update-ROOT-recovery-attempt4/ROOT-result.original.json`, reported SHA256
`4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3`;
run `dfb75b38-6019-4861-b868-f51648c71f02`, plan hash
`4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9`,
saved status hash `d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90`.
Вопрос: что именно известно о terminal/final/raw старого run? C00 и bounded
metadata/hash inventory, без submit/распаковки. Нормировка здесь identity equality,
units bytes/status timestamps; missing не 0. Сверить primary bytes либо отметить
secondary-only; разделить installed `qcl-5d779b52-s01-20261012`, producer и `S`.
Positive: complete exact receipt/attempt; negative: старый RUNNING, missing part,
другой attempt. Выход — паспорт с locator каждого поля и gaps, пять уровней verdict.
Без primary terminal/raw локально: `данных недостаточно`, не «solver failed».
Один повтор чтения после появления новых данных; polling недоступного
сервера и новый run вместо утраченного receipt запрещены.

### SCI02 — publication/value origins и объявленная модель

**D Sol ultra; owner Research, review high.** P, declared input table, U04,
`literature/reference-2019/source.yaml` и `structure.csv`; Core `docs/src/theory/02_reference2019.md`.
Вопрос: какие параметры действительно задаёт первичный источник, какие assumptions?
Адресно получить official/author primary paper/версии, DOI metadata и нужные
pages/figure; сверить title/authors/DOI/arXiv, dose sheet/volume, слой и units.
Цепочка для dose: printed quantity → dimensional interpretation → donor profile
normalization → `build_profiles` → integrated sheet m^-2. Positive: verified primary
locator и корректная conversion; negative: wrong DOI, caption ambiguity, secondary
copy/failed screenshot. Выход: model passport с formula/value/assigning origins,
resolved conflict либо explicit assumption/gap для CP-SCI. Менять Research values
или silently «исправлять» dose запрещено; новый model choice — человеку.
Admission: bounded primary downloads≤128 MiB,≤1 h/1 CPU/1 GiB; без расчёта.
Если primary недоступен — сохранить declaration и предел attribution, не выдумывать.

### SCI03 — error budget и frozen scientific acceptance contract

**D Sol ultra; owner Core/Research, independent R high.** P, SCI02, primary
FD/FDR/DOS/current sources и `acceptance_metadata.jl`. Вопрос: какое численное
свидетельство достаточно именно этому равновесному утверждению? Вывести таблицу
выше, target observables/accuracy, uncertainty allocation, actual floors/weights,
units, near-zero и validity. Positive: ошибки
независимо ограничены/измеримы; negative: малый mixed step, normalized number,
FD seed, universal1e-4. Выход: version/hash criteria с unresolved coefficients,
pilot-vs-acceptance границей и заранее заданным H. Design≤2 h/1 CPU/2 GiB, без solve;
нужный measurement назначить конкретной approved variant. При неизвестном bound
приёмка blocked, допустим finite pilot по явно принятой части контракта.
Не менять threshold по результату; новая версия требует held-out evidence.

### SCI04 — контракт свежего финального raw audit

**D Sol ultra; owner Core, persistence Runner.** P, SCI03;
`reference/final_audit.jl::{fresh_fixed_point_metrics,_reference_audit_candidate}`,
`optimized/production_solver.jl` final_audit и `physics_diagnostics.jl`.
Вопрос: доказывает ли реальный final audit raw fixed point одного U/G?
Проследить unmixed scattering/embedding candidate, `r_D_candidate/r_A_candidate/
r_K/r_Σ`, λ/raw numbers, Poisson map и final histories до serialized owner.
Positive: свежий map на frozen final U/G; negative: predicted U+старое G,
stored Σ-only, α-scaled small step, final audit error с process0. Выход — exact gap/ticket либо reuse disposition, required dataset/metadata locator,
независимый literal oracle и regression contract для SCI05. Общий production kernel в fresh map не независимый oracle, это явное ограничение.
Если уже достаточно — SCI05 skip с evidence, не создавать новый сервис/API.

### SCI05 — реализовать только доказанные audit/oracle gaps

**I medium; отдельные owning Core → Runner/Contracts PR, затем R high.**
Вход: frozen SCI04/03 contract, P и утверждённый bounded test cap C08;
Paths точного ticket из SCI04,
existing `test/numerics/fresh_candidate_residual.jl` и выбранные analytic anchors.
Вопрос: может ли fixture отличить stored-good/fresh-bad и U/G mismatch?
Literal resonant scalar/2×2 matrix и manufactured Poisson independent helper graph;
thresholds tiny fixture относятся roundoff/oracle, не full-device accuracy.
Positive: exact oracle; negative: mutate candidate Σ, sign/weights/normalization,
audit unavailable; assertion должен действительно упасть. Если solver algorithms/acceptance meaning должны измениться — вернуть SCI04 D,
не расширять I. Максимум 2 corrective code rounds и 8 test calls общий на SCI05/08;
после лимита issue/gap, без install/full CI. Выход reviewed owning commit/logs,
independent R, gitlink после публикации.

### SCI06 — независимость stored reader и граница измерения

**A/R high; owner Results.** P, SCI03/04, `equilibrium.py::diagnose_stored_equilibrium`,
`state.py::StateReader`, manufactured `test_equilibrium_diagnostics.py`, existing PR6.
Вопрос: восстановлены ли full-matrix FDR/numbers/J из exact immutable final?
Проверить axis/coordinate/units, five requested/stored families, embedding_total
ровно один раз для raw; plus/minus отдельно для outward flux. C07 при наличии
final, C08 только после portable exact-source contract. Positive: known μ/nonunit weights;
negative: off-diagonal defect, transpose, wrong attempt, negative weights, bad
receipt, zero denominator, missing context/channel. Их literal sums/inverse2
не должны импортировать проверяемый reducer. Выход: independence/property/assertion matrix и report source binding; discovered
code gap уходит owning I medium с готовым контрактом, не исправляется под видом audit.

### SCI07 — измеримый resource/storage admission contract

**D Sol ultra; owners Runner/Platform/AiiDA, R high.** P, SCI04, resource section,
`auto_strategy.jl::_configured_production_estimate`, Core `estimate_production_memory`,
Runner resources/results docs. Вопрос: помещаются ли attempt, audit и durable stop
в реально выделенный envelope без изменения модели? Получить fresh host/cgroup
и storage facts, оценить 2 retained+pending+final/retrieval/export peak, 1800 s
cadence×72 h и cumulative bytes/logs. Positive: estimates+reserve+enforceable limits;
negative:8 GiB pre-prune, OOM, NFS counter blind spot, quota без writes limit.
Выход: finite signed admission inputs для CP-SCI и exact guard tickets SCI08;
caps всех conditional waves, shared concurrency и campaign deadline. Design≤90 min,
≤1 CPU/2 GiB; fresh server read только после доступа в platform scope.
Без input/guard — `needs_admission`, не fallback к меньшему Nb/window/channels.

### SCI08 — реализовать и fault-check недостающие guards

**I medium; owning Runner/Platform, R high; Contracts только если нужен формат.**
Вход frozen SCI07 contract/P, existing checkpoint/recovery/staging paths и C08.
Вопрос: отказ произойдёт до uncontrolled write с сохранением последнего verified
generation? Implementation locator сначала найти по current results docs/producer;
не заменять enclosing atomic/fsync contract новым параллельным writer.
Наблюдаемая — resident/cumulative bytes, early-stop reserve и receipt ownership;
переполнение integer/unknown counter fail-closed, units bytes, near-zero budget
означает refusal, не unlimited. Positive: exact-fit/new-generation publish;
negative: one-byte-short до prune, temp pointer/receipt overhead, external log
growth, failure/cancel mid-write, retained finals. C08 existing recovery и archive
preflight плюс новые named owning regressions из ticket; quotas/NFS/LAN/powerloss
требуют отдельного native infrastructure evidence. ≤2 code rounds в общем cap.
Выход: candidate, logs, guard coverage/gaps; no runtime attempt до закрытия
обязательных gaps. Нельзя понизить archive.full_final или удалить failure arrays.

### SCI09 — frozen catalog/CP-SCI

**D Sol ultra, Research/Runner; R high.** P+SCI02/03/04/07/12 design.
Вопрос: какие finite variants различают ошибки? Owning Research studies/meta
с C01, новыми IDs/controlled_paths и exact deltas wave table; equality model/
scattering, fingerprints/attempt membership; norms SCI03. Positive one promised
axis; negative inherited56 mV/alloy off/unlabelled coupled cutoff/window.
Historical plans не менять,48 mV каталог не выдавать за 0 mV.
CP-SCI: criteria hashes, caps/stop/H, code/review readiness+fresh admission;
можно сразу conditional waves. Planning≤30 min/2 CPU/4 GiB/output8 MiB;
missing runtime/слишком дорогой resolver=blocker, не solve. Выход — reviewable
technical READY/BIND packet по уже принятому S1 без e–e, не fake READY и не
повторный вопрос об одобрении каталога.

### SCI10 — B0 и разбор пяти отдельных уровней результата

**A/coordination high; scientific execution через существующий Runner/AiiDA.**
Вход P+CP-SCI, закрытые mandatory SCI05/06/08 gaps, release/worker admission,
C02 и exact B0 plan. C03 один раз с max_attempts1; C04 — backend, не второй submit.
Вопрос: достигнута ли raw thermal self-consistency declared модели? Сохранять
весь outcome, включая nonconverged full final; C05/06/07 и fresh audit по SCI04.
Positive: raw coupled fixed point+FD/FDR+absolute J с confirmed final U/G;
negative: budget stop, nonfinite, returned adaptive approximate, normalization
masking, final audit exception. ≤1 attempt/72 h внутри W1; мониторить CPU/RAM/I/O
и ожидаемое evidence минимум по фазовым переходам и без блокирующих длинных waits.
Выход — immutable report P и CP-SCI-RESULT. При failure не запускать refinements
для accuracy; SCI13 разбирает причину в оставшемся grant. Missing terminal —
первичная retrieval задача, не предположение об успехе/сбойной физике.

### SCI11 — E1/P1/K1 sensitivity

**A/R high, Research/Results; existing wrappers.** P каждого run+B0
CP-SCI-RESULT+initial grant, C01/03/05/07. Вопрос: step/phase/radial errors?
Те же baths/channels/boundary; μ/n/U/J/FDR/tails/raw residuals, gauge/basis/
common-domain mapping и absolute ΔJ из SCI03. Positive individually converged
states/differences внутри derived budget; negative agreement двух unconverged,
phase aliasing/tail loss/сменившийся state label. Cap3/216 node-hours после B0,
parallel только fresh reserves; нового human approve каждой точки нет.
Двух ΔE недостаточно для measured asymptotic order. Выход sensitivity/error
table с unknown axes; exceedance→SCI12/13, не tolerance edit.

### SCI12 — последующие finite waves и held-out contract

**D Sol ultra; owner Research/Core, независимый R high.** P, SCI03/07; initial
design W2/W3/H нужен до включения их в CP-SCI, execution может ждать SCI11.
Question: какой unresolved член error budget ограничивает физический вывод?
Для W/Z/B/A/Q/C задать точные changes/порядок, ожидаемый distinguishing signal,
масштаб n/U/J/tails, basis/gauge mapping и comparison slices. Final candidate: exact source/plan и feasibility. Basis change —
представление той же модели, требует сопоставления projectors/local current;
embedding change — отдельная boundary model. Positive: локализованный error term
и заранее defined H; negative: одновременная смена всего, post-hoc thresholds,
cutoff неверно назван energy-step. Выход: finite criteria/attempt predicates и
derived reducer ticket I medium при необходимости; новые reducers сначала literal
oracle/R high. Если новую variant нельзя выразить approved каталогом — запросить scoped решение,
не дописывать executions. Непроверенные направления остаются unknown.

### SCI13 — finite cause → patch → review → новый run

**D Sol ultra для гипотезы; I только SCI05/08 medium; R high отдельно.**
Вход immutable failed P, raw/telemetry, strict SCI03 contract и остаток grant.
Различать implementation/oracle defect, iterative instability, representation
error, resource/durability failure, model limitation и insufficient evidence.
Формулировать одну причинную гипотезу, её counterexample и самый дешёвый check;
сначала source/analytic/fixture, затем только оставшийся approved run. Наблюдаемая
и norm не меняются под гипотезу. Positive: mutation reproduces cause и corrective
patch проходит независимый oracle; negative: blind mixing/tolerance roulette,
seed→FD→pass, rerun из-за «на этот раз получится». Каждый cause/source/plan/attempt
сохраняет original failed logs/arrays; fixes получают owning PR, Root gitlink позже.
Code fix той же физики/approved numerical variant разрешён автономно внутри
R slots; arbitrary solver-method variant не считается заранее разрешённой.
**Два последовательных одинаковых failure fingerprints** останавливают затронутую
волну: решать ресурсный/причинный blocker, не тратить третий идентичный attempt.
В пределах grant можно продолжать независимый D/I/oracle и незатронутые пакеты;
после resolution run только из оставшихся slots. Нет slots/данных — конечный gap.

### SCI14 — independent result review и confirmation H

**R high; reviewer не writer/автор финального диагноза.** P всех used/failed runs,
SCI03 criteria freeze, sensitivity table, H frozen protocol и actual cap.
Reviewer получает question/assumptions/raw primary artifacts без готового verdict;
независимо C06/07 в bounded read envelope и проверяет fresh audit lineage.
Question: следует ли заявленный уровень из конкретных измерений, а не consensus?
Positive: full raw/normalized FDR и J checks на согласованном final, достаточный
набор refinements, H не использовался при выборе criteria. Negative: stored
selfenergy reconstruction назван fresh map, changed U, incomplete raw, другой
attempt/producer, postselection only pass. H выполняет wrappers через SCI10,
≤1 attempt/72 h из отдельного frozen slot; review не расходует незаявленный solve.
Derived read proposal≤32 GiB I/O/attempt, ≤1 CPU/2 GiB/30 min, report≤64 KiB;
сначала inventory и mandatory hash-size estimate, иначе bounded отказ/новая admission.
Выход CP-SCI-RESULT с разногласиями и cheapest resolution. Согласие агентов не
доказательство; незакрытый существенный counterexample препятствует acceptance.

### SCI15 — report/external validation

**A/R high, Research/Results.** P+SCI01–14, actual cost/criteria versions/sources.
Вопрос: что доказано? Сохранить report existing AiiDA `service.save_agent_report`
с exact used run refs, plots units/residual/correction/sensitivity; массивы не
копировать в Markdown/Git. Verdicts execution/equations/physical gates/
discretization/external validation отдельно; unknown/fail/N/A с причиной.
Negative outcome — legitimate endpoint, не infinite rerun.
`negf_iv_digitized.csv`: calculated NEGF200 K/40–60 mV/period,
digitization-only uncertainty/calibration56 mV, не эксперимент/S01 oracle.
Future transport validation — отдельные comparable conditions/model/held-out
data/error bars/finite grant; agreement не доказывает terminal voltage/405 periods/
gain/power/threshold. Этот каталог не включает finite-bias/optics.
Выход report≤1 h/1 CPU/2 GiB, reads ранее admitted, claims P+hash+dataset+slice.

## Зависимости и closure

01/02/06 параллельно; 02→03→04→05; fresh resources+04→07→08;
03/07→12 design→09→CP-SCI→10→14 baseline review→11→approved W2/W3→H/14→15.
SCI13 адресно при failure; frozen D до I. Historical gap01 ограничивает старый
run, не source design. Platform обеспечивает runtime/admission, не физику.

Stop affected execution/wave: nonfinite/unrecoverable PSD/causality, bad identity/
completeness, missing required audit/criterion, OOM/storage reserve, wall/attempt/
bytes cap, ambiguous submit,2 identical failure fingerprints. Evidence не
перезаписывать. Resume после stop proof/fresh admission, без reset iterations;
новая model/weaker criteria/cost scope — human proposal.

| Утверждение | Свидетельство | Ограничение | Решение сейчас |
| --- | --- | --- | --- |
| RV01 old history | SCI01 primary passport | Terminal/raw локально missing; новый run не восстановит | данных недостаточно |
| RV08 physics | SCI02–04 formula→symbol→criterion | Не reaudit34, provenance conflict открыт | дополнительно измерить |
| RV09 independence | SCI05/06/08 assertions/mutations/import logs | Fixture/старый pass не new execution | дополнительно измерить |
| RV10 finite contract | SCI02/03/07/09/12+CP-SCI | S1 без e–e approved_standby; criteria/admission ещё не установлены | изменить |
| Equilibrium | SCI10 fresh final U/G+C07+14 | Seed/exit0/normalized number/J0 отдельно недостаточны | данных недостаточно |
| Discretization | SCI11/W2/W3/H vs frozen budget | W1 не все axes, embedding отдельно | дополнительно измерить |
| External validation | Отдельные comparable data | 200 K calculated curve не эксперимент/S01 | данных недостаточно |
| Negative outcome легитимен | SCI13–15 failures/cost/gaps | Не положительная приёмка | сохранить |
