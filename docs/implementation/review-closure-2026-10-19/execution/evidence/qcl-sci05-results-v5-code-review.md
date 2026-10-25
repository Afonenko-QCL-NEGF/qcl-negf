# SCI05 N1 Results v5 — independent coordinator/high source review

2026-10-19. **PASS / source eligible for binding, runtime pending.** Reviewer: `/root`, selected Sol/high; writer `/root/sci05_results_impl` is separate and stopped. This is an incremental review of the exact E4 correction against the preserved v4 REQUEST_CHANGES, plus the actual producer field and consumer call graph. No target imports/parser/pytest/HDF5/Julia/solver/build/network/server actions were executed. Hash/Git/text inspection only; C08 consumed by reviewer=0.

## Source identity and independent checks

Owning base `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`, worktree `/tmp/qcl-sci05-results-worktree`. Root selected source `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; Contracts selected12fc264 and Runner selected9378396. The candidate is not yet the root gitlink. Actual source hashes and full patch SHA were recomputed; `git diff --check` passed. Source was read before the v5 author's conclusions.

| Exact input | SHA256 |
| --- | --- |
| v5 identity | 4d9eb0f0e6a533023d5d0a52a7e4574f0e63c4560142d9b29d090f29926f6daf |
| v5 patch | 7be93766f021e2e8a3a4c4afc5a4d56f1302d5317c001d36c108408c9d2034c1 |
| native.py | 532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5 |
| state.py | 335e67678120fd0c8e222fcb5e937b277ccadac35303fca2250c9f345983b477 |
| new test | 45111262df9b7744ca9f7397a887af4133ee602d9b6e325af2d3ee4a5e12f95a |
| preserved v4 review | 91e1ab77033d3c95f2cd03cb4efa7aeb7a9216c6d49b6260bac9c112b83da198 |

## F1 role binding and distinguishing controls

Primary Runner `save_analysis_physics` writes native4 role `physics.analysis` and `metadata/identity_json` (point_artifacts.jl304–317); full-owner metadata uses `point_identity_json`. D2 requires binding native role identity, not a uniform invented dataset name.

Actual v5 `state.py::_validate_final_audit_sidecar`201–218 now reads only `metadata/identity_json` after present native/commit record validation. Missing raises; strict recursive type equality against the complete commit identity rejects all six stale fields. There is no fallback to `point_identity_json`. The full-owner helper185–198 is unchanged. A fresh full-owner alias therefore cannot substitute for a stale/missing analysis identity. This closes the source counterexamples of the original and v4 reviews.

The sidecar caller221–236 verifies its declared SHA and then passes the same retained `_BudgetStream`/HDF5 handle under the shared `_IOBudget`. The new native identity read does not reopen a filename or use another unaccounted reader. Recovery role with a present record rejects before analysis identity handling, independent of enclosing archive storage_class. Absent analysis record returns without imposing a new identity requirement. `_commit_final_audit` distinguishes a present-null nested key from absence.

Prepared tests now model the real role layout: `publish` chooses identity_json for analysis; the native fixture helper receives that selector and does not fabricate a second full-owner alias. Healthy control verifies both actual field presence and alias absence. Negative controls change missing/all six stale actual fields, update owner bytes/SHA and receipt commit digest, and repeat with a fresh alias present. They require the identity-specific error and unchanged canonical bytes, so an unrelated checksum failure is not sufficient. No linked recovery.json dependency is declared by these literal two-HDF fixtures; the refreshed owner+receipt proof has no hidden stale nested reference of the kind found separately in Runner copied fixtures.

I compared frozen v4/v5 full patches: production delta is only the analysis selector/error text. Test delta is only role-correct fixture plumbing plus alias controls. native.py is byte-identical to independently reviewed profile A source. Full wire parsing, same AttrID/type cleanup, bounded fixed-width attrs, exact JSON/pair policy and canonical/equality/legacy behavior retain their prior source review. No numerical formula, gate, tolerance, schema, equilibrium reducer or public API changed.

## Actual producer control and limits

The explicit-env transport test only reads `ROOT/archive/final/commit.json`; supplied missing output fails, absent env is explicitly skipped/not_run. It does not generate substitute Python bytes. It asserts actual writer detail/shape, full+analysis owner roles, audit identity, owner SHA accounting and finite4MiB physical-stream cap. Its externally supplied selector has four known fields; the actual generated state_id/sequence are checked internally and must be captured by the coordinator's retained producer manifest before call8. This is transport evidence, not the full-six independently supplied C07 scientific selection contract.

Actual Runner output does not exist yet. Runner v2 is separately under review, including recovery-role handling and public negative-control integrity. This Results source PASS neither accepts Runner nor authorizes consuming the Results slot before a successful bound call7 and immutable producer manifest. The sole remaining Results C08 invocation should include the new file and the existing equilibrium fixtures in one pytest process, with explicit producer env; a skip is not round-trip evidence. C08 cap8 and used6 remain unchanged. No automatic rerun is authorized by this report.

Source budgets are bounded text/Git reads well below the assigned4MiB input scale; OS CPU/RSS/I/O totals were not instrumented and are not claimed as measured. Prior profile-A limits remain: whole-process hostile HDF metadata allocation, all dataset low-ID lifetime paths and historical verify_recovery_bundle aggregate I/O are not proven. Existing synthetic fixtures are not S1 all-five physical measurements. No full CI, native build or scientific submit occurred.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Analysis native identity соответствует реальной роли | Primary Runner field + v5 selector, no fallback, refreshed controls | Runtime pending | сохранить |
| Profile A/pair/legacy/recovery source semantics сохранены | Exact v4/v5 diff and unchanged native hash, caller graph | No linked HDF runtime in this review | сохранить |
| Producer-to-reader roundtrip уже доказан | Explicit test prepared only | Call7/8 and producer hashes absent | дополнительно измерить |
| S1/native/full-release acceptance достигнута | Нет новых измерений | Separate required gates remain open | данных недостаточно |

STOP source review; no product edits by reviewer.
