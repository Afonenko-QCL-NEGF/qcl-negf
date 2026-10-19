# SCI03-M1 Phase1 RED source v2 — R1 correction

2026-10-19. Source-only corrective cycle1. **STOP: separate independent R, then coordinator sole RED.** Ни imports/parsers/tests/pytest/HDF/Julia/solver/build/install/network/server/stage/commit/push не выполнялись. M1 calls0/2; SCI05/08 C08 exhausted8/8 сохранён. Production/README не изменены.

Input review `/tmp/qcl-sci03-M1-red-review.md`, SHA256 `ba228b23c4d9e17f0c1b35fb171b38cad0d6e75feba2efd9903cedce306299fc`, прочитан полностью. R1 математически обоснован: при fitted binary64 f сумма вычисленных полных defects может иметь rounding residue даже для literal raw N+P=A. Проверка exact runtime zero была сильнее утверждения accepted measurement contract. Новый tolerance/обнуление defect не вводится.

Единственная дельта v1→v2, `tests/test_equilibrium_diagnostics.py:716`:

```diff
-    assert bound['state_defects']['raw']['sum_norm'] == 0
+    m1_close(bound['state_defects']['raw']['sum_norm'], 0)
```

Используется существующий accepted engineering `M1_ROUNDOFF=512*2^-53`; не physical tolerance/libm certificate. Остальные literal exact dyadic controls M1_09, exact boundary-zero M1_03, positive n/p и nonzero normalized c сохранены. Это по-прежнему различает c=n+p, без ложного требования floating cancellation0. Separate all-row finite-t norm assertions также не менялись.

Worktree `/tmp/qcl-sci03-M1-results-worktree`, branch `codex/review-closure-current-bound-measurements`, HEAD/base `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`. Root batch8 при read — `d4113f43cddf02d46025434eb3a9dd8e110e90d6`; root не редактировался. Исходные v1 report/identity/patch сохранены побайтно. Дополнительно восстановлен v1 test source из v2 обратной единственной строкой: `/tmp/qcl-sci03-M1-red-v1-source.py`; hash совпал с frozen v1 `7d2a9d69a0d4cb02334b9b4617a09a9cb3746247eba17f7ebff364eb62ab8921`.

| Объект | SHA256 |
| --- | --- |
| v2 test source | `d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79` |
| `/tmp/qcl-sci03-M1-red-v2-patch.diff` (base→v2) | `c599065fd8e38d5e165693b091a075cee1ac9f128601f3a1b748ac47dcc45acc` |
| `/tmp/qcl-sci03-M1-red-v2-delta.diff` (v1→v2) | `5ed2c20740d13b4c35c6b545337d59c669985f7463f8c248c68a03072d343ec1` |
| unchanged production | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| unchanged README | `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9` |

Проверено только source: single-line delta, baseline full29322-byte prefix через cmp, `git diff --check`, hashes. Overall base diff остаётся append-only +324/−0, только test file. Collection не выполнялась: source forecast51cases/13REDfail/38pass не изменён; runtime assertion ниже missing-namespace signal и не меняет ожидаемый baseline RED mechanism. Original input contract identities и preparation failure/success receipts остаются в неизменённом v1 report/identity; owning Research publication-before-consumer gate не изменён.

Source-author corrective envelope≤10min,1CPU,2GiB,read1MiB,output32KiB; targeted text/hashes only, resource telemetry не инструментировалась. Coordinator runtime envelope прежний:≤2calls по90s/1CPU/1GiB RSS/TMP32MiB/raw2MiB, без automatic third call. Scientific caps/model/tolerances/H/εJ_abs/native admission не менялись. Scope не включает проверку runtime/physical accuracy.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 устранён ровно одной строкой | v1→v2 delta, accepted existing m1_close | Separate R и RED ещё не выполнены | изменить |
| Literal controls/base36/prod/README сохранены | Single-line delta, prefix cmp, unchanged SHA | Source-only verification | сохранить |
| Numerical/scientific acceptance установлена | Нет runtime/final arrays/admission/H/εJ_abs | Engineering fixture correction | данных недостаточно |
