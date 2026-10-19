# RV19 — заранее фиксированный denominator

Start 2026-10-14T18:09Z; stage static REVIEW/design. Source S + selected RV16 material (predecessor output separately bound in report).
Two finite packets <=20 min each including review, author aim <=12 min, <=1 CPU/1 GiB, extracts <=96 KiB/packet, sections <=8 KiB. No import/evaluation/install/prototype/build.

P19A selected one API boundary through `configuration_contract`/RV16 semantic row (actual API `configuration_source`) and one config assignment boundary `configuration_sources`: signature, units, defaults/constraints, effects/errors, formula origin, value origin, assigning origin, overrides, canonical example, owner = 10 properties. The pre-symbol file-boundary label was not a Julia symbol; clarification does not expand the 10-property denominator. Also trace exported Core API, run schema, Portal route/client, Platform Nix/TF as supporting source surfaces; do not claim full API coverage.
P19B eight generator alternatives: Documenter, Griffe with allow_inspection=False, Sphinx autodoc, OpenAPI, TypeDoc, Nix options docs, terraform-docs, Literate.jl; one prototype READY checklist. Denominator 19 (10+8+1), unseen public API catalogue partial.
