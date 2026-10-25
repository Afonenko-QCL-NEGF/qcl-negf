# SCI08-R1 production I1 — независимый high C/P/P

**Вердикт: PASS_SOURCE. Блокирующих findings в адресном R1 scope нет.** Actual five-file production diff соответствует accepted D1+D2+D3 и замороженным пяти fixtures. Это source approval для последующего отдельного Root GREEN1 READY, а не GREEN/ENG_READY, S1 admission, release или scientific acceptance. Новых execution grants этот отчёт не выдаёт.

Reviewer независим от sole writer I1. Сначала прочитаны требования и actual production diff/fixtures, затем авторские report/caller-traces; готовый авторский диагноз не использовался как первичное доказательство. Внутренних дополнительных reviewers не было. Runtime/parser/compiler/format/lint/tests/Julia/Pkg/build/solver/native/network/server calls=0. Source/CP/Git changes=0; записаны только review artifacts в /tmp.

## Идентичность

Owning candidate `/tmp/qcl-sci08-r1-runner-worktree`: HEAD `fefaa27f194bfddf85dd51a0e255beef2218c06d`; статус содержит ровно пять изменённых production файлов, три прежних modified fixtures и два untracked fixtures. Recursive submodules пусты. Managed Root HEAD независимо прочитан как `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`; его Git tree содержит Runner fefaa27 и Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`. Начальный cwd имеет другой dirty HEAD e48e5b2; он не источник reviewed candidate. Gitlinks остаются authority состава, hashes ниже — forensic binding diff/evidence.

| Input | SHA256 |
| --- | --- |
| I1 identity | `5c04472b3dda7325d99a4e1eebbc732db869bccde46a3b6f2fd9ffc8dafa82ad` |
| I1 complete production patch | `7c5d0a56dfc56081aa3a3e78e91adae936130482167614dec4867779b520c9e6` |
| I1 report | `4ac96ee72aeb54eec76cf31e8b236d7cbc9d686464d5efddfbf00ce9ecf1fb4e` |
| I1 author caller-traces | `2c5913c00123b3556070f322b53f5795381dc6b4c3d06323944e974676512699` |
| D1 | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| D2 | `5a50afe3ca4014991dcb61d6dfb2879b2fef99e10f18347b5aa5d4eefe54d642` |
| D3 | `373a5da4ca765561e4a3ee46fa9c0bd06959a067ebf9f56c415e33666ad507c7` |
| High D1/D2/D3 reviews | `a68ecf63af984355148b46d4a943cc5ca35adbe9da80102c512858d2b4847d69` / `23e50f07964c441f16b1e121f9d7952cf1bafd737544b81000a56a9da28e32fa` / `7b8108df1708f103a988ca567feb0e50c8b8c8f455ac657217033ed692c0ff46` |
| Engineering plan v3 | `c48d28709fb75a66652d8ca7d884e55a1158c7e9e950b5e8aa0861525db3c13e` |
| Frozen fixture identity | `87981037d559a9461b835a3a4d1c5d99b86c1cce78c3594197010948397bb254` |
| Actual RED2 receipt | `1ae6c4cd1ac24f82dbc43558f9f145654468347e4a9b91ef81563ff2ed59714c` |

All five source SHA256 and all five fixture SHA256 were independently recomputed and agree with I1 identity and plan. Full hashes are repeated in accompanying review identity. The source diff examined directly is the five-file diff represented by complete.patch. There is no new physics, model, configuration/schema, discretization, grid/basis/window, scattering, tolerance or scientific acceptance edit in this diff.

## Адресная корректность

`src/infrastructure/persistence/point_artifacts.jl:528–583` implements one shared non-Bool representable-Int validator through existing `QCLExecutionPolicy._grant_integer`. Positive dimensions/budget and nonnegative reserve/kernel/current bytes remain distinct. The scalar forecast checks every product and sum of unchanged `C+4*(128*NE*Nk*Nb*Nb+ΣK+F)`. Zero empty kernels are known zero; unknown is rejected. Checked budget and free predicates retain separate baselines. Adapter scalar validation precedes storage/disk readers; raw diskstat available is validated before Int conversion, each filesize is validated before checked accumulation. No unknown-to-zero/unlimited conversion is introduced. Forecast remains a heuristic allowance, not a proven HDF5 upper bound.

O1 actual caller: `scientific_execution.jl:449` invokes imported `_scientific_resource_preflight` as the first body statement. `scientific_workflow.jl:29` imports that same root symbol tested in frozen O1. `native_phase_telemetry.jl:237–245` rejects wrong policy, strict missing envelope, and unconditionally strict with envelope pending R2/R3/P1/P2/A1/C1. Refusal precedes plan decode, root mkdir:459, plan writer, attempts, strategy:672, problem construction:687 and cache:694. No bypass Boolean/proof object exists. The typed entry is not itself executed by the tiny fixture; its ordering is established by source trace, separately approved in the companion O1/O2 report.

Envelope entry:447 is explicitly passed to `resolve_execution_strategy(config;envelope)`:672 and reservation:679. `auto_strategy.jl:512–523` forwards it to selection; reservation:175–184 consumes the third argument. The actual entry chain has no second ambient default lookup. Optional two-argument reservation compatibility remains for other standalone callers. Policy entry:446 reaches actual phase constructor:969, then permit. Strict entry currently prevents reaching the strategy's legacy default hardware reader; no claim is made that future strict execution admission has already been integrated.

O2 actual caller: `commit_point_artifacts` validates budget/reserve:816–818, calls shared `_checkpoint_storage_preflight`:825, then budget/free:826–827, generation enumeration:828, staging:846 and HDF5 writer:852. Preflight:554–557 checks reserve, calls real solution adapter:547–552 and the scalar core:532–545, then checked-adds reserve. The same seam is called by tiny O2/O4 fixtures. Invalid dimensions or overflow cannot reach generation/staging/payload writer. `mkpath(root)`:823 intentionally precedes forecast; this is a disclosed directory effect accepted by D1, so no zero-filesystem-effects claim follows.

`linux_resources.jl:1–123` retains strict raw finite/unlimited/unknown/malformed/out_of_range distinctions and rejects incomplete/wrong cgroup membership, traversal, missing/symlink ancestor directories, bad ancestor max and absent finite max. Strict probe validates override integers before use, reads all currents/max/high, process affinity, leaf effective cpuset and every ancestor quota from explicit roots. Missing/malformed CPU paths throw; no host capacity fallback replaces them. CPU ranges are merged as intervals, never expanded over untrusted range length. Integer quota worker floor is exact; observational ratio remains Float64. Legacy `_resource_integer` and old standalone probe body remain unchanged below the strict sibling.

`native_phase_telemetry.jl:139–245` validates width before conversion/permit. Strict mode requires directory, known burst, a complete valid max chain with finite hard bound, and finite current at each applicable finite bound. Known zero burst still requires measurements. Every current+burst is checked before tightest-bound selection and GC; malformed/overflow exits precede pressure writing and continuation. Known insufficient capacity retains GC/resample and then checked required bytes in refusal receipt. Exact fit permits; clean cache credit stays zero. Standalone retains directory/burst/no-finite-bound unavailable branches and legacy readers; common malformed-width/arithmetic tightening is the accepted D1 safety change.

Module visibility was checked from `src/QCLNEGFRunner.jl`: root helper bodies resolve existing `QCLExecutionPolicy._grant_integer` after module initialization; new preflight and ExecutionEnvelope are imported into `QCLScientificWorkflow`. Frozen fixture API names/keywords match implemented helpers; no undefined future helper mismatch was found by source inspection. Package loading and syntax have not been executed.

## Frozen denominator и fake-only coverage

Manual expansion agrees with **349 nominal assertions if all blocks are reached**, not runtime passes: F/B/D file118, S/O file131, application55, Linux26, integration19. F/B/D15 + S/O13 + L3 =31 required logical groups; selected named-file testsets33. Boundary rows remain present: six isolated forecast overflow sites, adjacent literal/BigInt fit, budget/free exact fit and 1byte short, unknown versus known zero, strict bad ancestors/current/CPU overrides, negative continuation and healthy continuation controls. Oracle does not call production forecast/validator. Fixtures are byte-for-byte unchanged from frozen v3; no weakened assertion or added include.

Application width test:142–143 passes both fake roots. Constructor→legacy membership reader uses fake self/cgroup; ancestor chain is fake leaf/slice/root, and directory=nothing returns before memory reads. Attempted/completed counters supplement actual width results. Linux fixtures provide both roots, explicit physical/count/thread/vendor values and nonzero fake MemAvailable or explicit available override; Sys memory fallback is unreachable for these selected calls. Strict fixture phase/probe wrappers both pass fake proc/cgroup plus explicit capacity/count/vendor inputs. Storage tests use scalar or injected tiny readers, not actual diskstat. No selected fixture solves SCBA/Poisson.

D3 chain is actual integration sink:28→recorder:40–45 keyword→journal:20–24 keyword→fake boot file. Lazy get! still uses exactly String directory key; default /proc, strip(read(...,String)), catch boot_unknown, session/PID/time, sequence0, anchors, struct and row construction remain unchanged. Four added provenance/cache checks preserve all old15 integration assertions, count4 events and cache-hit identity after fake A→B. Finally removes only owned journal/admission entries. Production configured sink still omits keyword (`configured_run.jl:41`), preserving original default boot provenance. Fake-only is a source call-path conclusion, not syscall isolation or proof about dependency initialization.

RED2 receipt and original raw log show healthy control pass and known Bool not rejected on baseline:1 pass/1 fail/0 errors/0 broken, not import/missing API failure. Its exact plan/harness and baseline empty production diff are preserved in receipt. This review did not rerun RED. RED1 remains separately consumed; C08 remains exhausted8/8. No GREEN call occurred here.

## Ограничения и решение

No full storage growth enforcement, native ownership/freshness/identity/lease/admission, R2/R3/P1/P2/A1/C1 or runtime GREEN is established. Other unchecked arithmetic (minimum-output/recovery+reserve, counters) is outside reviewed R1 call chains and remains disclosed, not silently claimed safe. No physical CPU/RSS/I/O measurement was performed. Read scope was bounded to named source/docs/receipts and narrow searches, conservatively below6MiB logical reads; repeated full-file read charges and output stay within assigned15min/192KiB envelope. Some batch outputs truncated; acceptance-critical source/contract ranges were read separately. This is logical source accounting, not a sampled OS cap receipt.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| I1 реализует accepted D1+D2+D3 | Five-file diff, matching exact source hashes, traces above | Source-only C/P/P | сохранить |
| O1/O2 actual paths bind tested seam before stated payload effects | Entry449 and commit825→stage846/writer852; companion approval | Early commit root mkdir disclosed; typed entry/commit not executed | сохранить |
|349/31 frozen denominator сохранён | Independent manual expansion + five exact SHA256 matches | Nominal, not runtime passes | сохранить |
| Standalone defaults и D3 provenance/cache сохранены | Separate legacy body; default recorder and lazy directory get! | Regression execution pending separate finite GREEN | дополнительно измерить |
| Full S1/native/science acceptance достигнута | Strict entry unconditional needs_guard/needs_admission | Missing owning guards/runtime evidence | данных недостаточно |

STOP. PASS_SOURCE supports Root binding this exact I1 and approved O1/O2 trace to a fresh GREEN1 READY under the separate accepted finite plan. It does not itself issue READY or authorize a call.
