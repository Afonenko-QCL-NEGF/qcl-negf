# DEV01 applied author packet

Source: root e0f244d075dd49874ba4f3847f4efa693f3b3622, Core 3108150dd1b6b1377470b384b15c26e272fe5c5d.
Author: /root/dev01 gpt-6.1-sol ultra. Independent design: /root/reviewer high, PASS.
Writer branch: codex/review-closure-dev01. Author patch SHA256 b54e1b38b60430b39c0adfeadf7cbcbe6b0ae3c548fc90a673cf7c49b17b2331.

Old author exec approval was interrupted; root reconciled clean Core and git apply --check exit0, then applied exact author bytes via root automatic approval. No coordinator content edit.

Verification from Core cwd:

- git diff --check: exit0, no diagnostics.
- git diff --name-only: exactly docs/src/theory/{05_basis,11_observables,19_production}.md.
- Scoped rg confirmed EQ-CURRENT-001/002 anchors, corrected eg_s/(2pi hbar), physical eV weights, explicit rejected legacy_pzp, and no unilateral post-root rescale.
- Full diff /tmp/qcl-dev01-review.diff SHA256 ddcc4b0013cc3b74213c5e0609566fe770d47dadd54a5cd4a6abdb99cdd24f05.

Numerical tests/imports/docs build/solver not executed for this docs-only task. No production, model, schema, thresholds or test files changed. Existing Core source assertions were read by author/reviewer, not rerun. Full source-to-sentence design evidence: /tmp/qcl-dev01-design-receipt.md.

CP-CODE independent diff review PASS. Reviewer receipt /tmp/qcl-dev01-review.md SHA256 84f3143047a3e08b9aed47c90163728046a44b0c44842ebaad4c44ca87058365. Coordinator corrected an extra leading d in the report diff hash; product bytes unchanged. No commit/push yet.
