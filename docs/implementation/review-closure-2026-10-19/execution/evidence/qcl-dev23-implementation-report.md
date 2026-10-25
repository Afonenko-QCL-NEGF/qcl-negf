# DEV23 cancellation error repair — candidate for root GREEN1

Owning AiiDA base `5579d55684939495230241f446b7ea07c8ae0224` in managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`. Root authorized narrow production repair after semantic RED1: 7 passed / 2 failed / 0 errors, daemon and refresh OSError escaped the safe RuntimeError contract. Root executor receipt: wall3.891s / RSS147005440 / complete raw3494 bytes; `/tmp/qcl-DEV23-RED-1/original.log`, SHA256 `01195ffe706ed1c7f612961a2cba4daffe09c6cb23e0c9942bec19e93feada99`.

## Change

`src/aiida_qcl_negf/service.py::kill_run` now catches exceptions during daemon client lookup/property access and emits existing generic cancellation RuntimeError. The existing dispatch exception boundary now includes the single post-dispatch `_node` refresh. Private backend error remains an internally chained cause; public `str` is safe. Initial `_node(identifier)` input admission/lookup semantics, already-terminal behavior, daemon-down message, unconfirmed message, timeout10 and single dispatch are unchanged. No retry, new submit, idempotency mechanism, native process operation or scientific change added. README untouched pending separate ultra design.

The existing ten attempt_decision cells and submission marker/no-requeue/executable tests remain unchanged. All nine candidate cancellation cases and three additional scientific terminal cells from tests-first packet are byte-identical to the RED packet. Full old tests-first report: `/tmp/qcl-dev23-red-report.md`.

## Frozen candidate hashes

| Artifact | SHA256 |
| --- | --- |
| service.py | `5f7e9b28f9007255e3de319fff43e48143d4c23a9c9487164ecda92ebac8c762` |
| tests/test_restart.py | `eaf3b5e78cce5e8dc1ca7a919b299a76443bb5dab3fed584010b523a65c1ad70` |
| tests/test_cancellation_contract.py | `8b276505d190811526bd6d308acb09bf0b00317c36be14a92861236141204809` |
| /tmp/qcl-dev23-full.patch | `dd30d5e29b648ee122d035ef75f2a09cb3a7351db53c6b6cb07cd4d1945c61a3` |

Full patch includes tracked service/restart changes and new cancellation file. Author `git diff --check`: exit0, output0. Author performed no runtime/import/test/Git mutations. Root GREEN1 remains required; root owns L-PY attempt count and bounded integration profile fixture execution. No claim of GREEN, native stopped state, full-release acceptance or scientific acceptance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Safe exception boundary covers two observed RED paths | reviewed service.py diff + original RED log hash | candidate GREEN1 not yet measured | изменить |
| Existing truth/dispatch/submit boundaries preserved | unchanged RED fixture hashes; single kill and refresh source | synthetic backend fixture, not native process-stop proof | сохранить |
| Full remaining numerical budget proved by event60 | read-only Runner gap in tests-first report | positive remaining-loop cap unmeasured | данных недостаточно |

STOP before root GREEN1; no further edit without coordinator release.
