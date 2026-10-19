# RV06-01 — explicit controller activation ownership

Proposed ticket only; owning component Platform P=`4ce214e29b72276157b10a9267e2f30fef4ac66f`, priority P1 for the single-writer lifecycle claim. No product patch or operation performed.

Reproducer contract: `ops/application_release.py::main` 1444–1463 uses `activation.lock` for controller activate, checks only matching closed gate, then calls `activate` (948–1005), which writes profiles/Code allowlist/env/ready and starts services. Concurrent owner in `lifecycle_owner` (683–689) holds `delivery.lock`; update marker only checked by `lifecycle_guard` (663–680), not this CLI branch. Thus public source permits independent controller activation during a common lifecycle owner/update barrier. This is a source counterexample, not observed production incident.

Change proposal: distinguish privileged owned delivery child from standalone controller activation using an explicit authenticated operation binding; standalone requests participate in common guard/owner, child verifies existing parent ownership without reacquiring its flock. Do not naively give remote child the parent lock: parent delivery waits for that child.

Future public fixture (not executed): matching closed gate, delivery owner held or durable update marker; recording activate command boundary must see zero mutations for standalone CLI. Conversely a correctly bound delivery child must progress, wrong/expired operation binding must refuse, and unknown child outcome must retain parent reconciliation evidence. Never delete original intent/receipt to obtain a pass.

Acceptance requires owner×entrypoint catalogue, bounded crash evidence for child handoff, and separately authorized live rehearsal. Inventory/private credentials are not required for this source finding. Scientific model/tolerances unchanged.
