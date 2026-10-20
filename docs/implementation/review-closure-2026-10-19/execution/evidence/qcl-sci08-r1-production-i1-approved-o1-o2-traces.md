# SCI08-R1 I1 — independent actual O1/O2 caller approval

**status: PASS_SOURCE.** Candidate Runner HEAD `fefaa27f194bfddf85dd51a0e255beef2218c06d`, exact I1 identity SHA256 `5c04472b3dda7325d99a4e1eebbc732db869bccde46a3b6f2fd9ffc8dafa82ad`, complete five-file production patch SHA256 `7c5d0a56dfc56081aa3a3e78e91adae936130482167614dec4867779b520c9e6`. Independently traced from primary production sources before reading author traces; no target execution.

O1: `src/composition/scientific_execution.jl:436–449` actual typed `execute_scientific_plan` captures resource_policy and envelope and calls `_scientific_resource_preflight(resource_policy,envelope)` first. `scientific_workflow.jl:29` imports exactly the root symbol called by frozen O1. `native_phase_telemetry.jl:237–245` permits return only standalone; strict missing envelope rejects needs_admission, strict explicit envelope unconditionally rejects needs_guard/needs_admission pending R2/R3/P1/P2/A1/C1. This precedes plan decode:452, root mkdir:459, plan writer:469, execution mkdir:667, strategy:672, problem:687 and cache:694. No helper-test thunk is substituted for the actual ordering evidence. Tiny fixture tests seam while this source trace supplies real entry ordering; neither typed production execution nor solver was run.

Envelope: entry:447→preflight:449; entry captured argument→strategy:672→auto_strategy:512–523→select_execution_plan; same argument→reservation:679→175–184. No second ambient envelope lookup on actual entry chain. Reservation optional default supports omitted-argument legacy callers only. Policy:entry446→phase constructor969→native149–151→permit156ff; strict entry stays closed before this continuation. Legacy hardware default under strategy is not promoted to strict admission.

O2: `src/infrastructure/persistence/point_artifacts.jl:787–827` actual typed commit validates budget/reserve816–818 and calls `_checkpoint_storage_preflight(solution,reserve_bytes)`:825. Same root seam called by frozen O2/O4 is defined554–557: validate reserve→adapter547–552→pure scalar core532–545→checked forecast+reserve. On invalid scalar/overflow no return to budget/free826–827, generation enumeration828, stage846 or checkpoint/HDF5 writer852. This meets stated writer boundary. `mkpath(root)`:823 remains an explicitly accepted earlier directory effect; no general no-write claim.

Storage budget adapter568–572 validates known budget/reserve/additional before reader; scalar559–566 validates used and checked additions. Free adapter581–583 validates required before diskstat/injected reader; scalar574–578 validates available. There is no fabricated unknown zero/unlimited. Forecast is unchanged heuristic, not proven capacity. This approval does not cover all HDF5 slab growth, R2/R3/P2 resident budgets, unreviewed counters or scientific recovery arithmetic.

Required supporting source hashes: scientific_execution `52aded550f1362b67f7c3781e2d45daac0e001a6dd0248a730f29299d443645f`; scientific_workflow `b391a455247208a4293ea1aa000b4a288c097a70c23abd45f59e9f1b29a01337`; native_phase_telemetry `aba27f8c873b28f4b3f99d7736c9bedf40368ca4154e7c0af0ab592fc7ece216`; point_artifacts `18bcd0fe2c6ff42050c500b57f17678b06a38f14871a9a3de437841cb5f8d1ad`.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| O1 actual entry ordering accepted | Shared imported seam first at449 | No runtime invocation | сохранить |
| O2 actual checkpoint ordering accepted | Shared seam825 before stage846/HDF5852 | Earlier mkdir823 disclosed | сохранить |
| GREEN/S1 admission reached | No execution; strict closed | Root fresh READY and separate finite call still required | данных недостаточно |
