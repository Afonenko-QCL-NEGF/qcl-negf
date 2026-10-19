# RV05 independent review

Candidate SHA256 `5261fee88f115cd9f77e67fbe652b4f49faaef710109766d818229c0f49d50b9`; S/T/A as [blind source notes](RV05-blind.md), written before reading candidate. N=6 selected; read/report only, no tests/profile/HTTP execution.

Independent trace confirms serialized thread/loop/profile/handle ownership, explicit finite-reader disconnect cleanup, cooperative export cancellation and unbounded synchronous Future wait. Candidate states the important limitation correctly: fixture does not prove termination of blocked backend, no production hang claimed. Proposal preserves unknown-submit semantics and refuses unsafe forced thread/profile unload. AiiDA `service.py::open_artifact` repository context also matches the actor handle boundary.

No actionable report/source contradiction found within selected scope. Catalogue, finite negative Event oracle, role actions and M04/M13 partial/not_measured labels are present. The word «доказывает» in discussion of the existing disconnect fixture is constrained by the following source-read/not-run statement; it means the assertion contract, not this session's observed passing result. Future wording can consistently say «asserts» to prevent ambiguity, but no runtime pass is being asserted.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Candidate correctly bounds owner and cleanup claims | T `AiidaService/ClosingStreamingResponse/ExportStore`; A repository context | No blocked-backend/native execution | сохранить |
| Bounded stalled shutdown is not established | `.result()`/shutdown(wait=True), named progress-only fixture | Source inference, not production incident | данных недостаточно |
