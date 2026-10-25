# OPS04 Root final assembly

PASS — exact five source/test file hashes from green-source-binding, unchanged after sole GREEN; independent code reviewb59aeca1, D2/CLI-seam reviews12e811ec/626159c6. Actual main delegates use same checked capture/prepare/build seams. Full selected graph and Manifest bind raw JSON capture, deterministic consumed JSON/hash, archive scalar inputs and Nix arguments; no late pathname fallback.

Original RED17fail9pass1.639s preserved; post-formatter soleGREEN26pass1.707s, sampleRSS321,445,888B/TMP651,709B/raw3307Bcomplete. Formatter4files0.104s and pinnedDeno linter4files0.104s passed separately; source parser only, not hidden tests. Unitcap2/2 consumed; no repeats. Actual unit commands lack run/network permissions; fake command callbacks and literal fixtures exercise native-caller order, graph mutation, invalid UTF8, byte bounds, noexec failures and pending-file durability protocol.

Nix expression was source-reviewed, not evaluated/built. No native output/reuse/derivation/content/bootstrap/import/runtime or public-release receipt exists. OPS04.N and OPS03 OS/systemd/Slurm/admission constraints remain open. These units do not establish native durability or privileged reader safety.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact captured/consumed metadata controls both consumers | CPPsource and26boundedcases incl A→B at first app callback | NativeNix assertion not executed | изменить |
| Cache rejects empty password, preserves username | Same literalTS/Python rejection controls | No credential/trust policy expansion | изменить |
| Full release/native gate obtained | None | Admission/builder/systemd/etc missing | данных недостаточно |

Eligible for Root progress commit/PR23 only; sole finalCI/fullrootmerge/public release still pending.
