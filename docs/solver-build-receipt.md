# Solver build receipt and release assembly

`ops/solver.ts::buildSolver` returns the existing depot binding extended as `SolverBuildResult`. It
captures the stdout returned by the actual `nix build --json --no-link` invocation, requires exactly
one `drvPath` and one `outputs.out`, and retains the exact consumed depot JSON and its digest. The
returned graph digest uses recursively ASCII-sorted object keys, compact UTF-8 JSON without a
newline, and unchanged array order. Unknown graph fields, duplicate component paths, duplicate
captured JSON keys and non-ASCII graph values are refused. Captured depot component array order must
match the selected source graph; changing object key order is harmless to the graph digest.

`ops/application_cd.ts::runApplicationCdCli` uses that returned output directly. Before publishing
it hashes the installed `${output}/share/qcl-negf/julia/Manifest.toml` with a 1 MiB read limit and
obtains actual closure NAR hashes through `nix path-info --json`. Its existing returned
`depotBinding` contains the extended build receipt. `deploymentManifest` accepts an optional sixth
`SolverAssemblyReceipt` argument containing that result, the selected source Manifest digest and the
installed Manifest digest. It rejects contradictions between consumed source/Manifest metadata,
captured build JSON, selected output, and any known local deriver. The resulting optional
`solver_build` contains exactly `source_graph_sha256`, `julia_manifest_sha256`, `drv_path`, and
`output_path`; the existing `closures` carry the actual NAR hashes. The historical
`release_id = SHA256(JSON.stringify({sources, closures}))` remains unchanged. The derivation path is
an observation, not an additional deployment closure; a substituting destination need not retain its
`.drv` file.

A trusted native builder may already have performed the exact build outside this CLI. Its existing
command adapter can supply that captured stdout through the normal `buildSolver(..., execute)`
callback only after matching the original invocation's pinned source URI, exact consumed depot
JSON/digest, selected Julia Manifest, and resource/test arguments to the requested command. The
callback returns the original captured JSON; it must reject a different invocation or missing
receipt. Prefetch callbacks retain their normal independent contract. Pass the resulting
`SolverBuildResult` to `deploymentManifest` with independently read installed Manifest SHA and
actual `path-info` NAR evidence for the selected application and solver. Do not manufacture
`drvPath`, infer it from a store name, substitute a source label for command provenance, invent NAR
hashes, or mark an absent receipt as verified. This adapter is a trusted publisher boundary, not a
browser, request, or arbitrary client input. The API's structural checks cannot prove the origin of
a deliberately forged command adapter.

Legacy direct `deploymentManifest` callers that omit the receipt still produce the existing manifest
without `solver_build`; no empty proof or verified boolean is generated. Such a manifest remains
compatible with ordinary delivery but cannot provide the quantum runtime binding. Platform validates
and preserves this additive metadata and checks NAR/output/Manifest at delivery. Runner checks its
immutable source and active environment before quantum work. Source review, focused tests, native
delivery qualification, and scientific acceptance remain separate gates.
