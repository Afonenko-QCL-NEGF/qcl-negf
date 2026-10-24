# DOC06 — full named source ledger

2026-10-20. Source-only D; Root HEAD514cd9707a32cde60c630d60986973a898d35b18.
Initial status observed tracked_dirty3/untracked6; concurrent changes are not
design inputs or author changes. Source authority for components is selected Git
commit, not mutable checkout. All reads used named paths/git show; no target code
or parser was executed. No source/input artifacts were modified.

## Hash and conservative read accounting

Runner revision1acc165650fd4f4c2d49605cc679f90e3f6fcdae;
Contracts12fc26462bbab3df76904c6deb01f8c6596de7be;
Coree431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee.

| Owner | Path | Full source SHA256 | Bytes | Conservative full-file reads |
| --- | --- | --- | --- | --- |
| runner | src/application/configuration_types.jl | `6851ee3d8827912e4542b881ec7014460e5a0f5c83fc4f322b97e1dfce9518f0` | 8663 | 2 |
| runner | src/infrastructure/config/configuration_sources.jl | `bb08a718dd765a15db2a4fba7de0ff2ea79753f29dc516900f67485331dafbb1` | 3381 | 2 |
| runner | src/infrastructure/resources/package_paths.jl | `9296670ff9b4a881ef4a9065e084a5eae682b2c7dba5b9974504252f982373de` | 2527 | 2 |
| runner | src/infrastructure/config/configuration.jl | `b07516d1fa1b9f7918efd4fa9096327be45af5ea32233ba15a9e88bf225daebb` | 71428 | 3 |
| runner | src/infrastructure/config/configuration_contract.jl | `96da51af912890bb001c03c9400f95151c67f630dd248b4263bff4c7b93c710d` | 4635 | 2 |
| runner | src/application/auto_strategy.jl | `810c72af8e4289c3dd61d4f49549a083568472646fa69eb625f41c5702840326` | 19019 | 2 |
| runner | docs/src/user/configuration.md | `5f1fb2243240a957a1d765af0b8dee4f44a7e105dcea35889c725843bacf4cbf` | 10648 | 2 |
| runner | docs/src/api/public.md | `e59e1231197ed92823d691353ddc21dafe0b62252d586cf4018b2f331cda05dd` | 7050 | 2 |
| runner | schema/run.schema.json | `62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b` | 54815 | 2 |
| runner | test/fixtures/configurations/base.yaml | `735c0077cc7c64c901829a5a86bd5bab6c9b78e473d469e3240062aa7bc810b2` | 6973 | 2 |
| contracts | src/qcl_negf_contracts/schemas/run.schema.json | `62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b` | 54815 | 4 |
| core | src/numerics/optimized/production_contracts.jl | `ebb614494b4e58477231dbaf25a5283e8867e1c612859b2e26690c167b61a019` | 15596 | 2 |

Component total including repeated text/hash reads:700158 bytes.
Root canonical physics-documentation.md=97722 bytes, SHA256
fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794,
≤5 full-file-equivalent passes=488610 bytes (hash/targeted text scans/slices).
Root documentation-instructions.md=24800 bytes, SHA256
17fc16b7808ae0e2b29732c65033a5f544bca79577788cbade386870e0246254,
2 reads=49600 bytes. Root AGENTS17383 and architecture5501 bytes each read once.
Total conservative named source payload=1261252 bytes <2097152 cap.
Git object/metadata/kernel physical I/O/RSS not instrumented. Listing explicit
resource/schema paths and cat-file sizes are metadata, not a source/runtime audit.
Failed lookup schema/schema-provenance.json yielded no source bytes; it was not
replaced with invented contents. No broad corpus scan or follow-latest occurred.

## Exact source witnesses

- Runner configuration_types.jl: ConfigurationProvenance doc/type; documented
  configuration_source and typed declaration near end. Sources history ordering,
  last/nothing and lookup-vs-loading/default/effective distinction are explicit.
- Runner configuration.jl:214–235 deep merge records abspath(source_file);
  914–975 requires energy_chunk, converts it through _integer and ProductionOptions.
  _integer excludes Bool and checks representable Int. This is contextual source,
  not a proposal to run the loader or derive actual assigning filenames.
- Runner configuration_sources.jl: ordered source collection/merge/schema validation;
  load_configuration_source converts via _resolve_configuration. Source-only
  adapter never calls any of those routines.
- Contracts run.schema.json: root41–42 local production ref;1420–1441 production
  type/required/energy_chunk integer minimum1/description/no default.
  Exact selector /$defs/production/properties/energy_chunk, required sibling.
- Runner packaged schema byte-identical to Contracts selected schema; no C1
  model-help schema present at selected12fc or made authoritative by pending work.
- Core production_contracts.jl:69–109 documented ProductionOptions and field92
  energy_chunk::Int=64;395–399 positive guard. This is typed constructor context.
- Runner fixture base.yaml162–163 explicitly assigns64; docs configuration route
  has17/23 synthetic override expectations and source-vs-effective distinctions.
- Runner auto_strategy.jl39–66 source marker and conditional policy history;
  69–115 selects chunk from runtime inputs;472–488 sets effective/raw value from
  selected plan. Exact dynamic value/causal chain is not statically extracted.

## Prototype input vs discovery context

Nine future input files are enumerated by D. package_paths.jl,configuration_contract.jl
and API public.md were discovery/context witnesses only, not extra extraction scope.
Full graph/revision/hash table here is an audit receipt, not a maintained composition
lock or replacement for Git gitlinks. Root's private checkout paths are not public
output refs. Known source bytes do not establish an actual run/release binding.

## Scope and limitations

Current work wrote only /tmp design,ledger,identity and tiny erratum candidate.
No imports/parsers/eval/tests/Julia/Nix/Deno/build/network/server/children,
stage/commit/push or checkpoint changes. Skill brainstorming/writing-plans already
used in-session; task is an approved fixed-slice design handoff, no human reapproval.
Historical documents and fixtures retain their dates/semantics. Runtime/static
prototype checks remain future proposed bounded I evidence, not executed results.

