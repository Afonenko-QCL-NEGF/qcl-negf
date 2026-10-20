# DOC07 C2 semantic implementation — independent high CPP

**REQUEST_CHANGES. Шесть collated findings F1–F6.** Новый private helper содержит существенную проверку source/context/hash/origin связей, но не выполняет весь принятый C2 contract. Ни один runtime не выполнялся; приведённые outcomes — воспроизводимый source trace и contracts для независимых regressions, не измеренный failure/pass. Sole GREEN до owning correction расходовать не следует.

## Неизменяемый вход

Actual worktree `/tmp/qcl-doc07-c2-worktree`, HEAD `d791dea33f4628cf23c0b8552ebee9e51d7dd605`. Read-only Git status: только два untracked файла — новый module и прежний C2 test; submodules отсутствуют.

| Артефакт | SHA256 |
| --- | --- |
| `src/qcl_negf_contracts/model_help.py`,46827 B | `ca2c6656484fd99a2a58815ba97f0eb85369591f287368ffe05109764b014d1a` |
| Frozen C2 test,40274 B | `72240eab26305f63aeeec06197a7f64802c111a83cd3ef8aae603c5e89ae71f9` |
| Frozen D2 | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| Frozen canonical DOC03 | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Author report | `b0a98a45ce6b63f0769c23542017b887cac099dbeb4c9e775222daf049f6dd1f` |
| Author identity | `9e480cb66f354f7117bc6d8c719b4e2dd9d130460530e2232fd03532b7f3e6a6` |
| Author full patch | `480ff73c43ffe0a6393404e453efd613939aa8f4a364f81d47a1a013d747d112` |

Authority: D2 R6 private routines/checked detached inputs:131–145; R2 ordered reasons:178; R3 exact known identity scalars:181–197; R4 exact requested mapping/independent phases:201–212; R5 exact public-source review:219. Canonical origin proof:452–475, assigning/causal/Evidence:510–538, Snapshot:556–574, Index:615–636. Known pointer-only DOC06 erratum733b does not change these norms. Primary authority, frozen test and all module branches were read before author report. No new public schema or repeated handwritten C1 validation is requested.

## F1 — P1: Bundle validation bypasses fragment public-content/source semantics

**Locator:** `_bundle`:720–727 versus `_fragment`:673–695, `_reference`:421–426 and `_origin`:416–418.

The Bundle branch resolves each declared fragment payload, but checks only its id/source_revision. It never checks that payload's public refs/URI, actual source selector/allowlist, keyed input/reference/API/equation identities or document/anchor relationships. Those checks exist only in the separate Fragment branch. `_validate_model_help_bindings(bundle, ...)` therefore accepts a hash-consistent bundle containing a C1-valid fragment with a forbidden query-bearing locator. The selected View branch calls `_fragment` for its one retained requested fragment; that does not protect other public fragments in the bundle either.

**Reproducible source control:** start from `case()`. Preserve the safe original as healthy. Change the authored reference locator to `https://example.org/paper?token=synthetic`, reauthor synthetic annotation/claim/review refs using the existing fixture helper and repack all docs hashes. Call validation for `bundle`. Its path is :698→720→726→728 and never reaches `_uri`. All public bytes and outer hashes can remain internally consistent. The expected result under D2 R5 is ContractError, even when the owning review association exists. Repeat with a second, unselected fragment carrying the same semantic defect to prevent a selected-fragment-only repair.

**Cheapest correction:** apply the existing fragment semantic checks to every decoded bundle fragment in its own exact descriptor/payload context. Separate reusable static fragment checks from selected requested-mapping checks where necessary; do not add I/O, a new format or a public registry. Retain the same public-source/URI policy, rather than changing it to match this implementation. Add paired Bundle controls for a safe fragment, query-bearing fragment, and invalid source/selector in an unselected fragment; all outer hashes must be freshly correct.

## F2 — P2: Unbound View can erase verified retained identity scalars

**Locator:** `_view`:818–849, especially `if binding[field] is not None` at848.

The method establishes known release/source/manifest/bundle identity values but compares them only when the emitted field is nonnull. A C1-valid unknown/unavailable View may set one or all of these known values to null and still pass. D2 R3 explicitly requires each scalar to remain its exact retained value when known, and null only when unavailable. Non-bound status does not erase verified identity.

**Reproducible source control:** take `case()` and the already accepted docs-unavailable View pattern (`binding.status=unavailable`, reason=bundle_missing, fragment=null). Keep the original complete retained mapping/receipt; this pattern has an existing healthy control. Set each emitted `release_id`, `source_revision`, `release_manifest_sha256`, `bundle_sha256` to null in turn. :848 skips the comparison and later checks do not restore it. Expected: ContractError. Also preserve a healthy truly missing-evidence case in which the corresponding scalar is null.

**Cheapest correction:** enforce exact known/null projection according to D2 R3 for every scalar, independently of documentation availability. Do not fabricate unavailable identities and do not require a missing public HTML tree just to preserve retained identity.

## F3 — P2: Assigning Evidence is not bound to the target leaf's last assignment

**Locator:** `_assigning`:793–811; `_view` calls it at889. Contrast `_last_assignment`:490–497, which is used only by origin resolution.

The assigning validator accepts any metadata selector resolving to a dict with equal kind/rule/source. It does not establish that this is the selected input leaf's last recorded assignment. Matching an unrelated producer step is therefore sufficient to label the target's assigning provenance known, even though its actual snapshot last assignment differs. Exact bytes establish what a record says, not that the record assigns this leaf.

**Reproducible source control:** retain the healthy `case()` snapshot, where height has the config-file assignment. Change only its View assigning projection to known/execution_strategy/source=null/rule=`fixed_strategy`, with Evidence pointing to the existing exact `execution_strategy:/steps/0`. That dict has the matching kind/rule/source, so :799–811 accepts it. The target height's retained assigning record has not changed. Expected: ContractError. Use a second leaf with a different valid source/rule as an additional unrelated-record control if needed; all selected context/bytes remain correct.

**Cheapest correction:** bind assigning projection and its allowed Evidence location to the actual selected leaf/phase assignment or explicit checked owning assignment mapping, not arbitrary metadata equality. Keep the already accepted frozen-plan assignment healthy case and valid selected snapshot assignment case. Producer rules still require their owning allowlisted record; this does not add scientific inference or a new public field.

## F4 — P2: Known effective chain permits unrelated Evidence outside owning scope

**Locator:** `_effective`:774–790; known branch uses only `required <= supplied` at782, while partial branch separately restricts `supplied <= required` at790.

Full required coverage is checked, but a known chain can additionally emit arbitrary valid metadata selectors not in the source-bound applicable step list. Canonical Evidence selectors are allowlisted, and D2 requires source-bound causal steps. The known branch should not grant a larger selector scope than the partial branch merely because every required step was also supplied.

**Reproducible source control:** use the healthy complete two-step known chain. Append a correctly hashed Evidence for `execution_input:/context` (or another existing unrelated selector) while keeping both genuine required steps and the genuine requirements source. Every selector resolves and :782 still succeeds. Expected: ContractError; the exact original two-step chain must continue to pass. This is distinct from the existing same-cardinality replacement negatives, which test missing required coverage.

**Cheapest correction:** verify both required coverage and emitted Evidence membership in the checked applicable causal scope. Do not count evidence or infer causal applicability from a dict's presence. No new requirement that an unrelated extra record becomes an accepted step; the source-owned universe already supplies the scope.

## F5 — P2: Index branch rejects ordinary multi-point indexes of one selected child

**Locator:** `_index`:747–771, especially760–770.

Every entry is required to have the endpoint selection's `point_id`, and every valid entry is compared with the same one `execution_input` record. A complete index with P-1 and P-2 entries for the same child/execution/attempt is consequently rejected even when both belong to the frozen plan and each has valid bytes/hash/context. Canonical Index is an execution/attempt inventory with up to the plan point count, not an endpoint-specific single-point list. The actor later selects exactly one entry for the endpoint (canonical retrieval step3). The author's explicit single-point limitation is a narrowing of an accepted public branch, not an approved contract override.

**Cheapest correction:** distinguish index-wide child/execution/attempt and frozen point-membership checks from selected endpoint matching. Associate each valid indexed file with its own checked bounded retained payload/passport/inventory evidence, supplied by the owning in-memory boundary; do not compare siblings to the selected point's sole payload. Missing required entry evidence may fail closed, but a different valid member point must not itself be considered contradictory. Do not truncate a genuine complete index or invent a new public index format to evade this requirement.

**Independent regressions:** healthy complete two-point index with different Atom values, correct point passports and individually correct digest/size records; selected P-1 and P-2 lookups; wrong attempt/execution; nonmember point; cross-associated sibling hash/payload; duplicate path; aggregate/count limits. Bind exact per-entry owner evidence before claiming complete validation. Keep one-point controls. No filesystem read or extra runtime grant is implied by this correction contract.

## F6 — P2: Snapshot declared Atom may contradict its frozen point passport

**Locator:** `_snapshot`:733–744 and `local_context`:281–297.

Snapshot validation checks the context configuration hash against the frozen point hash, equality with its retained snapshot bytes, keyed identities and claim receipt context. It never compares a known RawInput.declared Atom to the corresponding frozen selected point leaf. Thus a snapshot can retain the correct passport hash while declaring a different value/unit/kind. This contradicts the defined declared source; hashing the context does not bind its per-leaf declared payload automatically.

**Reproducible source control:** start from the healthy `case()` Snapshot. Change only height RawInput.declared.atom from0.10nm to0.15nm; keep frozen point/configuration_hash unchanged, then reissue the exact snapshot bytes/digest and index size/hash. Validate the Snapshot branch itself. The context still matches the true frozen passport and :738 matches the freshly retained snapshot, so the altered declared Atom is accepted by this source. Expected: ContractError. Pair with declared unit/kind mismatch and a healthy distinct used value: used is runtime evidence and must not be forced equal to declared.

**Cheapest correction:** for known declared raw leaves with exact frozen point mapping, require the same strict kind/value/unit equality used by View declared projection. Preserve unknown declarations when proof is unavailable; never fill used from plan and never convert units. This is a binding check against existing retained evidence, not numerical/physics validation or another C1 validator.

## Completed source trace and retained useful work

All five dispatch branches and resolver were inspected. `_bytes` verifies byte budgets/digests before decode; metadata uses existing finite JSON boundary. Graph/source owner revision, sorted/unique components, explicit path/selector allowlists and exact opaque public-review source+recipe associations are implemented. `_resolve` separates `_MissingProof` from contradictions; preflight phase/context/hash checks precede missing reasons, then source follows D2:178 broadly in the accepted target/override/condition/claim/source/assignment/conditions order. Declared and used construct distinct Evidence, compare kind/value/unit without conversion, and require retained claim/source/last-assignment/context proofs before bound. This inspection is not an exhaustive proof of every unknown/exception path; F1–F6 are the frozen confirmed gaps.

Existing F1–F5 fixture improvements remain unchanged. They cover source id/revision/mapping witnesses, nonempty review association, same-cardinality missing chain members, claim/source precedence and healthy declared binding. Findings here concern additional implementation paths, not permission to weaken those fixtures. Add regression witnesses alongside preserved originals in the sole allocated owning correction; do not alter tolerances or public C1 schema.

The module remains private/in-memory: no owning target import, filesystem/network scan, unit conversion, public export or new serialized receipt observed. Source-review trust, source extraction allowlists, raw file-kind observations and selected child remain owning preconditions; agreement of synthetic byte records is not independent scientific attribution. No native/public/full-release/science claim follows.

## Read ledger, actions and stop boundary

Named reads: complete module in contiguous numbered ranges, changed/frozen test portions (cached prior full fixture review), selected frozen D2/canonical clauses, existing messages encode/decode source, selected C1 Evidence/assigning/effective/index shapes; author identity/report after primary code; exact hashes and read-only Git identity. Conservative source-read charge for this independent review is 2 MiB, below6MiB; prior task caches are evidence reuse, not new target execution. Physical CPU/RSS/I/O not instrumented; no claim of measured hard enforcement. Output below256KiB. Target runtime/import/parser/typecheck/tests/build/network/solver/server/children/Git mutation/product/checkpoint edits:0. Writes only this review and companion identity.

Engineering source cycle7/8 and DOC07 runtime used3/4 are coordinator provenance; this review consumes neither and does not reset either cap. Root confirmed sole GREEN is held pending the collated correction. Cycle8, if undertaken, must address this full frozen list; further automatic correction/rerun is not authorized. Historical RED/raw artifacts remain immutable.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact C2 candidate has meaningful source/hash/origin checks | Full source trace, immutable source/test hashes | Six confirmed semantic gaps | сохранить |
| Candidate satisfies complete accepted C2 contract | F1–F6 with exact locators and distinguishing controls | Source-only diagnosis, no runtime claims | изменить |
| Sole GREEN is ready to consume | Known gaps remain before cycle8 | Root owns final finite call | данных недостаточно |
| Native/public/scientific acceptance achieved | No such evidence | Private synthetic semantic binder only | дополнительно измерить |

STOP — REQUEST_CHANGES, six frozen collated findings, no execution or product repair by reviewer.
