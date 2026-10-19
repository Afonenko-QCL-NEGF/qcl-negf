# DEV15/DEV16 implementation candidate — frozen for coordinator GREEN and CP-CODE

## Scope and immutable inputs

Owning Runner branch `codex/review-closure-schema-provenance` from `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, root selected Contracts26cacbe1688fee0af300d0949fc6b94e55a29f4a. Accepted D15v2 `/tmp/qcl-dev15-design-v2.md` SHA25661c07b249740e435b9b4c2e2becfdaf558ad96304e275adcda370f652df9a1c6 and review PASS. No Git mutations after initial authorized local branch creation; no commit/push/merge. Only10 authorized Runner paths changed. Root owns execution/integration/review.

Full intended diff `/tmp/qcl-dev16-full.diff` SHA2568b7d735e6b1026dc921e77e797a437cfd3f21ea1a650443be3b26b07c9a8c22d.
Code+schema+fixtures-before-prose diff `/tmp/qcl-dev16-code.diff` SHA256f9959281c22e934c0f3b499802bf0c0018db5dc269fdb93f52f982c4629b352f.
`/tmp/qcl-dev16-code-hashes.json` SHA25613a0a1310c5c52633459be0210102e86adaf673708e82e9859c116e464df757a.
Verbatim prose mapping `/tmp/qcl-dev15-applied-prose-map.json` SHA256cea5ca69c8ac7010791da330e5c2e2ac430bd40419b6a87a6151f59f021e91c3. All three blocks copied verbatim from accepted section3.1/3.2/3.3; docstring function body unchanged; no new prose design. Root/schema contract status sentence remains accepted DEV16 target wording, pending owning published review.

## Source-confirmed YAML checkpoint

Actual path `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.build/local-julia-int01/depot-1/packages/YAML/M5j6t/src/YAML.jl` SHA25624f6e5c7475945658b3bf8625cacaa7c2443726547e0679acd86ff4584d936cb; Project version0.4.17. Lines142–143 `load(AbstractString,args...;kwargs...) = load(IOBuffer(input),args...;kwargs...)`. Constructor source SHA2564650446782dcdbe53928affe5dd183d0d0643bb07a04bf7ef4d7c6664d0e8f07;183–206 shows strict duplicates skipped after flatten_mapping. Shared parser therefore checks merge-tag keys in metadata constructor before flatten; schema parser retains existing YAML merges. Parser captures `String(copy(bytes))`, never YAML.load_file(path).

## Runtime implementation and actual snapshot flow

`tools/verify_schema_provenance.jl` imports only SHA/YAML, shared module QCLSchemaProvenance; direct-program CLI condition only, no verifier call during inclusion/import. Metadata/files reread each call, no success cache, mtime shortcut, bypass, environment mode or Git/network subprocess.

`configuration_contract.jl:2` includes shared module via loaded package resource. Wrapper:4–13 converts only SchemaProvenanceError to existing ConfigurationError. Actual `_load_configuration_schema:45–75`: obtains verification result49; determines bundled path50; selected bundled branch takes `snapshot.files["run.schema.json"]`52; bytes variable reaches `_strict_mapping_from_bytes(bytes,path)`63 and Draft/keyword checks68–73. There is no packaged content pathname reread or YAML.load_file in this call chain. `isfile/realpath` only classify aliases; custom schemas use their own captured bytes56, after bundled verification, without becoming canonical. Thus helper mutation fixture is supplementary; this actual-method source trace is the required CP-CODE snapshot-to-parse evidence.

`configuration.jl:1757–1762::_resolve_configuration` adds private root keyword and shared verification as first executable statement, before `_expect_keys` and Unitful parsing. Frozen-plan `snapshots.jl:30–33` calls that method; preceding raw mapping/fingerprint/output policy reads remain unchanged. No new frozen-plan JSON-schema validation/default/scientific criterion is introduced. Public loader/validator signatures and `DEFAULT_CONFIGURATION_SCHEMA::String` stay unchanged. No default_configuration_schema/__init__/configuration_source verification.

## Canonical copy and static checks

Canonical run schema and bundled file byte-identical, SHA25662df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b. Existing PROVENANCE run digest only updated; source/version/results digest preserved. Static Python comparison with Runner HEAD confirms removal of the added energy_chunk description makes parsed JSON identical; no constraints/defaults changed. Both declared packaged digests recomputed independently and matched. `git diff --check` passed. Links retain exact accepted source URLs and unchanged source fixture locators; `main/docs/schema-provenance.md` publication availability remains owning G1 concern; no Documenter build/inclusion claim.

## RED and GREEN request

Root reports actual semantic RED2:1failed0errors, absent module availability assertion, `/tmp/qcl-DEV16-RED-2/receipt.json` and original.log;8.631s/RSS772747264/1447B. Prior RED1 cold timeout counted. Writer executed no Julia/import/test/build/install/solver/server action.

After RED, schema fixture was strengthened without removing prior assertions: actual loader with unsupported keyword under mismatching hash, unsafe names with complete valid required metadata, and symlink escape with otherwise matching bytes. Final schema fixture SHA2561d56940eb6202f8b957ed43ce8aa94d1b20a566a80a1d32805ee79ca2c56088f (RED original d81fd3f... retained in frozen RED diff); merge fixture remains09fa7cccc6ec8c701cf86135ce6d50c5ca1881323d8b91e9729846b75f8e9cbb. These are additional controls before sole GREEN; no runtime rerun has happened.

READY FOR ROOT GREEN1 on this exact full diff, one bounded process including only:

```
include("components/QCLNEGFRunner.jl/test/contracts/schema_copy_provenance.jl")
include("components/QCLNEGFRunner.jl/test/application/configuration_merge_order_and_fail_closed_validation.jl")
```

Root owns exact existing prepared Julia1.13.0/depot path, BLAS1/1CPU/2GiB/120s/caps and total max3calls including timeout; no hidden subprocess. Candidate is not claimed passing until measured. Stop writes pending GREEN/review. Full suite, process-level CLI frozen plan, relocation/native Nix, solver convergence/physical acceptance not performed or established.

| утверждение | свидетельство | ограничение | решение |
| --- | --- | --- | --- |
| Shared guard covers declared packaged bytes and selected canonical workspace | Frozen verifier source + independent static SHA checks | Runtime GREEN pending | дополнительно измерить |
| Bundled schema is parsed from verified captured bytes | Actual loader49→52→63, parser String(copy(bytes)); no packaged content reread | No concurrent filesystem/process-level race test claimed | сохранить |
| Metadata merges cannot bypass duplicate rejection | Pre-flatten metadata-only check + valid-hash merge/duplicate fixture | Runtime control pending | дополнительно измерить |
| Frozen typed route reaches guard before resolution | snapshots30–33→resolver1757–1762 + actual wrong-dimension fixture | Earlier raw frozen reads unchanged; no full frozen process execution | сохранить |
| Canonical update changes only description | Exact canonical bytes/hash and JSON structural comparison | Byte integrity is not physical acceptance | сохранить |
| DEV15 exact prose applied | Accepted block hash mapping | No Documenter render/site publication | сохранить |
| Runtime/scientific acceptance complete | No such evidence | GREEN/review and science are separate gates | данных недостаточно |
