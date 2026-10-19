# RV11 independent review

Candidate SHA256 `d80f8b534670fd855aeea000d5e1078f9cf986e3a6e2cd1bfbcb029667ac0ff6`; S/J/U as [blind notes](RV11-blind.md), before candidate read. N=7; native tests/crash/NFS unexecuted.

Source trace independently confirms stage→sync→immutable generation→readback→receipt→pointer→pruning and separate Results internal-HDF5/attempt guards. Candidate accurately distinguishes artifact integrity, resumability and science acceptance; scratch killed-worker/NFS delivery limitation is explicit. Existing wrong-attempt/hash-valid-external fixtures assert independent reader negatives rather than writer self-success.

No actionable contradiction in report. A bounded additional locator check strengthens F11.1: J `filesystem_repository.jl::_immutable_yaml` delegates `_atomic_yaml`, which calls `_atomic_replace_file`; none of these selected helpers invokes fsync. The absence is established for this direct chain, while enclosing native durable guarantees remain unmeasured. Candidate's more cautious «требует отдельной проверки» is not a false positive, so no correction required.

Fault catalogue and independent crash-cut oracle supplied; M04 partial and M09 RPO/RTO not_measured correct. Full pruning correctness beyond selected reader/pointer trace and actual archive completeness remain outside this review, no expanded acceptance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Selected scientific publication/reader chain consistent | J commit helpers and U reader identity/internal storage | Actual power loss/backend not measured | сохранить |
| Generic runtime metadata chain lacks explicit fsync | J save_runtime_checkpoint→_immutable_yaml→_atomic_yaml→rename | No observed loss or enclosing-host claim | дополнительно измерить |
