# RV06 selected denominator (frozen before symbol reading)

Root S=`e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; Platform P=`4ce214e29b72276157b10a9267e2f30fef4ac66f`; root overlay receipt `../source-receipt.json`. Stage: source review only. Component has no AGENTS.md found by `rg --files -g AGENTS.md`.

Finite selected properties, N=7:

1. L1 — shared lifecycle owner/lock for release delivery and worker transitions; declared writers versus unmeasured live drift.
2. L2 — desired immutable release and observed runtime/ready/admission checks across profile/environment/allowlist/ready crash cuts.
3. L3 — durable delivery/admission intent and unknown remote outcome retain reconciliation barrier.
4. L4 — shutdown pending job scope requires per-job proof when a job disappears.
5. L5 — startup ready/resume/admission order and receipt ownership on interruption.
6. L6 — initial cold activation and stale/missing admission fail-closed boundaries.
7. L7 — bootstrap finite preflight/build admission and failure receipts; source checks do not imply four-role runtime acceptance.

Selected role×scenario catalogue: controller release delivery × success/crash/admission failure; worker shutdown × active/disappeared/unconfirmed job; worker startup × health failure/resume interruption; cold controller/worker × missing or mismatched gate; builder × stale preflight or resource rejection. All native execution cells `not_measured`. Unseen scenarios remain partial, not included in N.

Budget per direction: author ≤12 min, reviewer reserve ≤8 min; extracts ≤96 KiB, section ≤8 KiB, ≤1 CPU/≤1 GiB/process. No tests/build/eval/network/server. Acceptance: unknown outcome never counts as positive admission evidence. Stop after dispositions for L1–L7 or cap; coordinator appoints independent reviewer.
