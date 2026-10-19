# Targeted Python harness v2 — independent source review

**Verdict: CHANGES_REQUESTED before OPS03 use**, two concrete raw-evidence/output-envelope gaps. No helper execution, target imports, tests, child process or synthetic probe run by reviewer. AST/source/hash inspection only. Comparison with previously accepted harness is supplementary; inherited defects do not become validated by equality.

Exact proposed `/tmp/qcl-python-targeted-run-v2.py` SHA256 `9726bc355f0fd762cc382c69c23940112b0bf19659045dc49214c5fa44d6df8b`; compared Julia targeted v2 `23555092332f5a93d378bbedf4eb1f21dbae2de6ba6acc50926238ac703221d9`, helper `/tmp/qcl-local-julia-guard-v2.py` `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`. Hashes match.

## R1: collector-construction exception loses drain and receipt

In proposed try/finally, Popen is followed by `capture = lib.RawCapture(process.stdout, stream)`. If RawCapture construction raises after Popen, e.g thread.start failure, process exists but capture remains None. Finally sets completeFalse, kills process group, then unconditionally calls `capture.finish(5)` inside that branch. This raises AttributeError on None; child pipe is never drained and receipt code is skipped. Accepted e88 full guardian has an explicit capture-is-None fallback using communicate/write/close; targeted harness omitted it.

Required narrow fix: preserve the original launch/monitor exception; stop only own process group; if collector exists drain it, otherwise communicate/read the pipe after stop into already opened exclusive raw file, preserve all bytes and close stream. Failure/incomplete/unknown capture must produce non-success receipt and outer nonzero. Popen failure with no child must close stream and retain original guard diagnostic. Source-only/AST review is sufficient to inspect correction; no actual tests required for this review.

## R2: successful fast burst can exceed output envelope without failure

Output threshold is checked only in while process.poll() is None. A process can emit >2MiB and exit before the next50ms sample. Finally records exact captured bytes, but no post-drain maximum predicate exists. If process return0/reasonNone/completeTrue, final sys.exit returns0 despite output_bytes limit2MiB. This is not sampled-peak uncertainty: collector has the exact byte count after EOF.

Required narrow fix: after drain mark honest output_envelope_overrun when bytes>2MiB, preserve full raw and return nonzero regardless of child exit. Threshold1.875MiB remains an early-stop planning margin, not proof final bytes≤2MiB. Never truncate output. An overshoot receipt is failure, not pass with disclaimer.

## Confirmed design and limits

- Selected fixtures resolve to actual files below root/components, supporting pytest node IDs by splitting :: only for file identity. Command executes fixed selected Python/.venv pytest with explicit fixture args; no install/solver/fullCI command.
- Unique attempt directory mkdir(exist_ok=False) and exclusive original.log prevent accidental reuse. Task/attempt are not path-validated: confinement currently assumes coordinator supplies safe single-basename IDs such as OPS03/RED-1. Do not advertise generic arbitrary-CLI confinement; enforce basename validation if broader input is intended.
- TMPDIR points to owned attempt/tmp, and pytest basetemp is inside it. Standard tempfile.TempDirectory normally uses TMPDIR; explicit filesystem paths elsewhere remain unmeasured. Existing checkpoint correctly preserves legacy caveat: old basetemp-only zero did not measure all temporary data. No retrospective rewrite.
-1CPU affinity, per-process CPU90/95s,90s monitored wall, process-tree1GiB sampledRSS,16MiB sampled ownedTMP; no hard cgroup/disk/transient peak guarantee. Fixture and harness hashes are recorded at receipt time, not a before/after source-drift proof; coordinator must freeze sources and shared packet identity. Helper SHA is verified before import.
- Continuous non-daemon e88 RawCapture preserves byte writes, consumes pipe immediately after Popen, and normal/monitored-stop path drains. Tail printed for UI does not replace full original.log. R1 corrects exceptional construction path; R2 corrects post-drain success classification.
- No native runtime/process termination/global-budget acceptance follows from read-only source review. Root retains finite attempt counters and validates actual harness exit, receipt, raw hashes and source binding.

| Claim | Evidence | Limitation | Decision |
| --- | --- | --- | --- |
| Normal output preserved | Exact accepted RawCapture helper hash, exclusive raw file, drain path | Construction-error path R1 incomplete | изменить |
| Output overrun cannot pass | Exact post-drain bytes available | Final envelope predicate absent R2 | изменить |
| Standard tempfile routes owned | Explicit TMPDIR and basetemp | Explicit external paths/sample peaks unknown | сохранить |
| Legacy temp accounting honest | Checkpoint caveat1689–1690 | Not retrospective all-temp measurement | сохранить |
| OPS03 harness ready | Two concrete source gaps | No runtime executed | данных недостаточно |
