# SCI08-R1 — fixture-first SOURCE candidate

Статус: **READY_FOR_INDEPENDENT_FIXTURE_SOURCE_REVIEW**, не production I, не ENG_READY.
Owning Runner worktree `/tmp/qcl-sci08-r1-runner-worktree`, branch
`codex/review-closure-sci08-r1-checked-resources`, HEAD
`fefaa27f194bfddf85dd51a0e255beef2218c06d`.
Production `src` byte-exact HEAD: `git diff --exit-code HEAD -- src` завершён0.
Target Julia/import/parser/test/runtime/build/solver/native/network/install/commit/push=0.
Существующие C08=8/8 exhausted не использованы. Root владеет execution counters/grant.

Прочитаны D1, D2, оба high source review (финальный PASS_SOURCE), architecture,
owning point_artifacts/linux_resources/native_phase_telemetry/scientific_execution
ranges, пять selected fixtures/support common/resource_probe. Источник API — Runner
fefaa27; current initial cwd Root e48e5b2… и его dirty files не inputs реализации.
Root Git HEAD/status/submodule status и Runner HEAD/status/submodule status сняты.
Ничего в Root или компонентах исходного checkout не записано.

## Изменённые owning paths и точная selection

1. Новый `test/contracts/checked_storage_forecast.jl`: F1–F6/B1–B5/D1–D4.
2. Новый `test/infrastructure/strict_campaign_resource_admission.jl`: S1–S9/O1–O4.
3. `test/application/execution_resource_contract.jl`: только D2 correction L2.
4. `test/infrastructure/linux_process_resource_probe.jl`: только требуемые L3
   legacy malformed-current/max assertions, explicit fake roots/overrides.
5. `test/integration/native_phase_resource_contract.jl`: байты baseline сохранены.

31 — logical required property groups, не число @testset blocks. L1 охватывает
existing managed/manual/default-envelope assertions двух application testsets;
L2 — application width/unavailable + integration actual begin/end/missing burst;
L3 — Linux legacy controls. Всего в пяти files33 @testset blocks,31 logical groups.
Никаких skip/broken/filter/only либо исчезнувших parameter rows нет.
Предполагаемые counts при достижении всех assertions: новые249, application55,
Linux26, integration15, итого345. Это ручная source развёртка loops, **не runtime
assertion receipt**; independent reviewer обязан перепроверить до grant.
RED tiny subset содержит отдельно2 assertions, не заменяет full31-group GREEN.

| Group | Inputs / independent expected binding | Assertions |
| --- | --- | ---: |
| F1 | 2/3/5,[7,11],13 → literal16854140 |1|
| F2 | 1/1/1,[],0 и [0,0],0 → literal16777728 |2|
| F3 | 3 dimensions × true/0/−1/1.0/nothing/M+1 → ArgumentError |18|
| F4 | K entry/F independently × true/−1/1.0/nothing/M+1 → ArgumentError |10|
| F5 | Nb²,128NE,sumK,A+K,4(A+K),C+scaled → BigInt boundary checks + OverflowError |14|
| F6 | k=fld(M−C,4)−128 → BigInt exact fit; k+1 rejects |4|
| B1 | used17,budget25,reserve3,additional5 →17 |1|
| B2 | only budget24 →ArgumentError |1|
| B3 | 0/1/0/0 →0;26/25/0/0 rejects |2|
| B4 | four pure args×5 bad; budget0; adapter three args×5 bad+budget0 before read; healthy reader fires |40|
| B5 | M+1+0; (M−1)+1+1 →OverflowError at separate additions |2|
| D1 | available25,required25 →25 |1|
| D2 | available24,required25 rejects |1|
| D3 | 0/0 →0; each arg×5 malformed refuses |11|
| D4 | malformed required×5 before reader; healthy25; unknown/throwing disk reader |10|
| S1 | fake max/100/max,current90,burst10 →exact fit; bounded pool; continuation1 |2|
| S2 | only bound99 →pressure, continuation0 |2|
| S3 | 3 ancestors×blank/broken/negative/>M/missing max →refusal |15|
| S4 | all max; no groups; missing/legacy/traversal/relative/absent membership →refusal |7|
| S5 | each ancestor made finite ×blank/max/broken/negative/>M/missing current →refusal |18|
| S6 | absent burst; nothing/Bool/negative/float/>M burst; directory=nothing →refusal |7|
| S7 | burst0 known current →permit; same burst unknown current refuses |2|
| S8 | width Bool/0/negative/float/>M; currentM+burst1 →checked refusal, continuation0 |8|
| S9 | finite probe; raw max/finite0/unknown/malformed/out_of_range distinct; affinity4,quota21,cpuset4,override16,count-zero2,membership1 →refuse |55|
| O1 | missing envelope/wrong policy/remaining guards missing →closed actual preflight seam, continuation0 |4|
| O2 | Bool forecast or forecast+M reserve →actual checkpoint preflight seam refuses before continuation |3|
| O3 | real strict phase callback absent burst →continuation0/no successful admission/no phase row |4|
| O4 | real tiny phase permits continuation1; healthy checkpoint seam literal; standalone entry preflight |4|
| L1 | default envelope nothing/manual envelope nothing/managed controls retained |existing|
| L2 | four real callback widths + D2 attempted/completed3/3 then4/3; integration unchanged |existing|
| L3 | legacy max/malformed sentinels and malformed current fallback0 retained; strict S5/S9 refuses counterparts |existing|

M=typemax(Int), C=16777216. Exact integer counts/bytes; tolerance0. F oracle uses only
literal formula and test-local BigInt. No production forecast/validator computes RHS.
F5 identifies six independently constructed unsafe intermediate boundaries, but
throws alone do not prove the implementation used a particular checked primitive;
independent source review must verify every actual intermediate and conversion.
No arrays are allocated from manufactured dimensions. Tiny UInt8[] payloads are known
zero actual sizes, not normalization of missing observations.

## Precise private API/signature handoff for production writer AFTER observed RED

D1 names three scalar helpers; D does not fix all adapter/seam names. This candidate
binds the following signatures for a coherent implementation/review, without modifying
production before Root behavioral RED. Types must permit invalid test inputs to reach
explicit ArgumentError validation; typed dispatch MethodError is not the oracle.

| API | Contract used by fixtures |
| --- | --- |
| `_checkpoint_storage_forecast_bytes(ne,nk,nb,kernel_sizes,f_size)` | dimensions positive non-Bool Int-representable; sizes nonnegative; return Int forecast; checked all intermediate arithmetic |
| existing `_checkpoint_storage_forecast(solution)` | gather actual sizeof and delegate to same scalar helper; tiny NamedTuple uses existing duck-typed baseline API |
| `_storage_budget_used(used,budget,reserve,additional)` | validate all; budget>0; checked used+reserve+additional≤budget; return used |
| `_storage_free_permit(available,required)` | validate known nonnegative bytes; required≤available; return available |
| existing `_check_storage_budget(paths,budget,reserve,additional; storage_reader=_storage_bytes)` | validate caller args before reader; delegate used validation/predicate; reader called once only for valid caller args |
| existing `_check_storage_free(path,required; available_reader=...)` | default adapter returns raw diskstat.available without lossy preconversion; validate required before reader; unknown rejects, reader error propagates; delegate scalar validation |
| `_checkpoint_storage_preflight(solution,reserve)` | same forecast adapter plus checked validated forecast+reserve; return `(forecast_bytes=F,required_bytes=F+reserve)`; actual commit must use seam before generation/HDF5 writer |
| `_strict_resource_integer(raw::AbstractString)` | NamedTuple with `.status` :finite/:unlimited/:unknown/:malformed/:out_of_range; finite `.value` exact Int; max distinct from unknown0 |
| existing `_native_phase_request(directory;proc_root,cgroup_root,resource_policy=:standalone)` | strict refuses missing path/unknown estimate/bounds/current; validates width before Int; known pressure existing _NativePhasePressure; checked current+burst |
| existing `_native_phase_memory_permit!(directory,groups,request;resource_policy=:standalone)` | strict empty groups refuses; same helper is actual callback memory seam |
| existing `probe_hardware(;...,resource_policy=:standalone)` | strict raw CPU/count/override/path validation, no fallback from unknown; all fixture calls give roots and capacities/vendor explicitly |
| `_scientific_resource_preflight(resource_policy,envelope)` | unknown policy/missing strict envelope refuse; :campaign_strict always ArgumentError needs_guard/needs_admission until owning guard integration; standalone nothing returns nothing |
| existing `execute_scientific_plan(...;resource_policy=:standalone,envelope=default_execution_envelope())` | call same entry preflight before mkdir/plan/attempt/problem allocation; propagate selected envelope/policy, no second ambient default read |

These seams are engineering mechanics, not physical policy, authority tokens,
private portable schemas, lease ledgers or S1 admission. Standalone defaults remain.
Probe keyword count/capacity validations must be explicit even for Float/Bool/>M;
current typed override signatures may need widening to reject with ArgumentError.
Strict CPU range parser must not enumerate arbitrarily large intervals into Sets.

## Ordering evidence and remaining source obligations

D2 actual caller trace now:
`execution_resource_contract.jl` local fake_proc/fake_cgroup →
`_native_phase_request(nothing;proc_root=fake_proc,cgroup_root=fake_cgroup)` →
`_process_cgroup_path(fake_proc)` → `joinpath(fake_proc,"self","cgroup")`.
Literal membership normalizes to `fixture.slice/solver.scope`; `_cgroup_ancestors`
constructs fake leaf → fake slice → fake root, inside temporary root. Existing
standalone directory=nothing permit returns before memory reads. Both explicit
roots and source trace establish intended fake path; counters alone do not prove it.
Only four width invocations remain; attempted/completed checks3/3 then4/3.

All five selected fixture files' `_native_phase_request` calls pass both fake roots.
Existing Linux calls use fake proc/cgroups, fixture meminfo, explicit physical/thread/
vendor inputs. Added legacy call also binds available override. No global Base.read
monkeypatch or production read observer introduced. All new disk adapters use explicit
reader fakes and never actual diskstat. New strict callbacks/probe receive both roots.

**Design gap / STOP before ENG_READY:** O1/O2 currently bind actual future private seams,
with continuation sentinels and positive controls; baseline has neither seam. They do
not instantiate ScientificPlan/NEGFSolution or execute scientific entry/commit.
Therefore source trace on the later production candidate is mandatory to prove that
actual execute_scientific_plan/commit_point_artifacts call these same seams before
root/plan/problem or generation/HDF5 respectively. Without that source trace, these
sentinels prove only seam ordering and cannot close actual entry ordering. This is an
explicit review obligation, not a claim that toy thunks closed O1–O2. O3 uses actual
production callback; its actual allocator caller propagation also requires source
trace. Campaign entry must remain closed regardless of helper controls passing.

## RED handoff and source checks

`/tmp/qcl-sci08-R1-behavioral-red.jl` calls only baseline `_checkpoint_storage_forecast`.
Healthy tiny NamedTuple dims1/1/1 with empty byte kernels expects literal16777728;
negative same object except NE=true expects ArgumentError. Existing fefaa27 multiplies
Bool as1, so source predicts behavioral assertion failure. **No failure was observed.**
It imports no undefined future helper and does not read host or call solver/writer.
Exact source/candidate/environment/harness/combined budget/stop must be separately
bound by Root before RED execution. Production writer waits for behavioral RED receipt.
Full five-file GREEN follows only a separately accepted finite plan after implementation.
No automatic rerun, no C08 allowance, no target process called by this fixture task.

Completed source checks: `git diff --check`0; production src diff empty0; source-only
SHA256/Git inspection. No parser/import/runtime syntax validation; no numerical tests.
Source work bounded by4MiB read proposal/15min/1CPU/1GiB/report128KiB; no claimed
measured RSS/CPU or runtime fit. Output report+patch+identity well below128KiB each.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
|31 groups prepared with literal/BigInt oracles | two new source files + table above | not executed or parsed | дополнительно измерить |
| production baseline preserved until RED | empty git diff HEAD -- src | no observed RED yet | сохранить |
| selected D2 callback reads fake membership | explicit two roots + constructor/read path | source trace, no runtime read log | сохранить |
| actual O1/O2 entry ordering closed | future seam fixtures only | later production caller source trace mandatory | данных недостаточно |
| strict full campaign admitted | preflight expected always closed | other owning guards absent | данных недостаточно |

STOP for independent high fixture review. No runtime/production permission inferred.
