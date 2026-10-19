# DEV24 — independent public rejection audit, first packet

Root c43935567df010d43cab9bcd8d851a9ed976a8d7, selected Portalff1e25f22eed2cb6f48ba11c1ba0a52495e7f363, AiiDA312ed8a6363103d05a971d14ac9cbcca1c782358, Contracts26cacbe1688fee0af300d0949fc6b94e55a29f4a. Reviewer/executor coordinator Sol high, не автор Portal/AiiDA implementation. Read source/test first, then one fresh address-only packet. Product files не изменялись; new service/backend submit/solver/build/fullCI не выполнялись.

## Evidence denominator

14 explicitly selected functions generate50 pytest cases. Actual owning Portal API/AiiDA service/Contracts decoder imports в prepared locked Python3.14.7; external AiiDA repository/submit/process boundary заменён public synthetic objects. Один процесс GREEN-1:50 passed in1.13s pytest,4.992s wall, RSS167157760B sampled, TMP0B sampled, raw99B complete,67samples/no guards/errors/overrun. Cap90s/1CPU/1GiBsampledRSS/16MiBsampledownedTMP/2MiBlog. Zero sampledTMP не доказательство hardquota/transientpeak/explicitpathsoutsideTMP.

| Property | Named negative/control | Observed / boundary |
| --- | --- | --- |
| Missing/wrong bearer | test_authentication_and_private_schema |401 vs200; API auth dependency source api.py192–200. Existing test does not count facade/actor dispatch; exact zero-counter requirement not yet proven |
| Invalid resources/Code/plan | test_submission_rejections_do_not_start_work (6) +test_submission_has_one_owner_and_passes_exact_resources |403/422, service.calls empty for rejected; healthy202 exactlyone fake submit |
| Wrong native capability | test_native_artifact_capability_cannot_open_other_artifacts +test_locator_selection_race_capability_and_range | Valid200 and altered selector401; wrong capability calls==[] before metadata/open in locator case |
| Exact locator errors | test_exact_locator_errors_have_no_payload (11) | GET/HEAD/authorize expected422/404 and no open calls; attempt/path/UUID/inventory/status ambiguity fail closed |
| AiiDA metadata | test_metadata_fail_closed_without_payload (11),test_invalid_paths_before_selection (6) +test_cached_metadata_and_exact_payloads | Errors +zero payload open for malformed cases; healthy exact attempt metadata/payload correct |
| Broker error | test_broker_unavailable_is_not_reported_as_success |503 and no synthetic private-address text; log access/sanitization and actual broker unmeasured |
| Contract JSON/booleans | test_json_boundary_rejects_ambiguous_or_invalid_inputs (7),test_json_budget_and_canonical_encoding,test_single_archive_receipt_validates_unbounded_size_and_confined_filename | NaN/Inf/duplicate/deep/nonUTF8 malformed rejected; bool bytes rejected, valid finite receipt/JSON accepted |
| Composite cache | Existing source test_exports.py375/455 and previous DEV11 exact packet | Not among new50; no new cache runtime claim. Future DEV24 final packet should include these two selected functions with explicit authorization counters |

## Narrow I ticket DEV24-AUTH-COUNTERS

Ready existing handoff acceptance, no new public API/production design. One Portal writer medium on separate codex/review-closure-rejection-controls branch; only tests/test_api.py. Add one parametrized test missing/wrong bearer across selected list/submit/artifact/kill API routes using actual create_app and public synthetic facade wrappers with explicit call-list counters. Invalid bearer must401 and counters remainexactempty. Each healthy control withvalidbearer must reach exact relevant boundary once and produce expected existing status. Fake submit/kill only, no profile/service jobs. Keep existing tests/invariants/production code byteidentical. No call after auth failure can be hidden by a raising stub without countedattempt. No fixture reset between request and negative assertion; independent resets allowed only before separatecontrol. Does not claim a real actor was constructed/executed; witness is request→facade actor boundary.

Independent CP-CODE static review before remainingsecondtargetedcall; final packet onlynewtest +existing test_exports.py::test_export_pins_inventory_plan_payload_status_and_cache and ::test_export_invalid_selectors_precede_preparation (plus chosen positivecontrol ifnotalreadyembedded). Remaining1ofinitialmax2 DEV24calls90s1CPU1GiB16MiBTMP2MiBlog; author/reviewfinite2cycles; failurepreserved/replan, no automaticthird. Full suite/nativeTLS/securityclaim excluded. Scope can return concrete finding ifactualproductionbuguncovered.

## Artifact identity

- `/tmp/qcl-DEV24-GREEN-1/receipt.json` 5792B SHA256 `1a804be7a8d04b53cf2c418dedf5640e3ccd61b52851da4b25dcd95db0448b3e`
- `/tmp/qcl-DEV24-GREEN-1/original.log` 99B SHA256 `ccd9d26d5af2b916b82f6f94841bc4fd578b4c40ed5a7f96ad78bee59c969429`
- `/tmp/qcl-dev24-selected-nodeids.json` 1461B SHA256 `f62cab6f4111b32ac2ab9ab75198b0d0dcc739b7bb1317d43b34e5148f9ed684`
- `components/qcl-negf-aiida/tests/test_artifact_locator.py` SHA256 `ae339e892c9058afc55926203e8ddc4f1daa1106e34f7080f88bee54f814a8c9`
- `components/qcl-negf-contracts/tests/test_contracts.py` SHA256 `0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7`
- `components/qcl-negf-portal/tests/test_api.py` SHA256 `55efd325a3a3c97a8799a6eec8341c6eeaf78e8b0c18a3ec740b23ed1c9ebb9e`

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
|50 public synthetic rejection/control cases pass current source | Exact receipt/raw/source identity | Boundary fakes, не live/native | сохранить |
| Missing/wrong auth has measured zero dispatch | Current status-only assertion insufficient | Narrow I counter/control ticket ready | дополнительно измерить |
| Full security/native scientific accepted | Нет таких измерений | Separate gates protected | данных недостаточно |
