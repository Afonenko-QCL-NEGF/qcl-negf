# RV19 — narrow owning descriptions

Proposal only. Runner0c53c6d… `src/application/configuration_types.jl::configuration_source` docstring replacement:

> Return the last explicit configuration-source filename recorded in the provenance history for dotted_path, or nothing when that history is absent or empty. Later explicit leaves override earlier leaves. This is an assigning-source lookup, not a schema-default or complete effective-value-origin lookup. It reads provenance only; source loading and validation occur in validate_configuration_source/load_configuration_source.

Runner guide after source order: linked explanation from existing merge-order fixture base→first17→second23 selects second; reversed last source gives17. Test is executable specification, not executed receipt. API keeps @docs, no copied signature. Absence of assigning history is explicit, not invented production observation.

Contracts923e0c6… additive `$defs.production.properties.energy_chunk.description`:

> Positive integer execution chunk count for energy work scheduling. Required in the merged declarative configuration; no schema default is assigned here. The Core typed constructor has its own default, which must not be inferred as configuration-source provenance. This option does not define energy-grid spacing.

No constraints/default/model change. Update packaged Runner schema through owning workflow after Contracts PR, not independently edited contract. Future schema/docs check budget assigned before execution.

Portal future route/model prose distinguishes KiB/bytes/seconds and declared/effective defaults, coordinated TS client. Adding response_model is a separate API change, not implicit generator step. Platform conditional defaults retained as expressions, actual private overrides unknown/unpublished. Current output only proposals.
