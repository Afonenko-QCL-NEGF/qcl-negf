# DEV15 — assigning-source prose и контракт DEV16

Статус: D-candidate v2, второй и последний design round; C1 исправлен для
закрытия CP-DESIGN координатором. Implementation не выполнена.
Авторский этап — чтение исходников и подготовка `/tmp` handoff. Все product
files Runner оставлены без изменения, пока INT01 готовит source-bound Julia.
Ни imports, ни tests/install/build, ни SSH/solver не запускались. Субагенты не
создавались по ограничению данного задания; независимый reviewer назначается
координатором на этот неизменяемый пакет.

## 1. Immutable inputs и фактическое наблюдение

Следующие записи — историческая source epoch первого D-пакета. Round2 rebind
приведён ниже отдельно; первоначальные наблюдения не переписаны задним числом.

- Active root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
  HEAD `eb59809a4e601c9bd1d4859228d68502679b6d93`.
- Runner HEAD `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, clean на начале и
  последней проверке. Его исходники — основание локаторов ниже.
- Canonical DEV14 checkout: Contracts `26cacbe1688fee0af300d0949fc6b94e55a29f4a`,
  clean. `src/qcl_negf_contracts/schemas/run.schema.json` SHA256
  `62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b`.
  Diff этого commit меняет только description `production.energy_chunk` и
  legacy-only README wording. Publication/G1 PR7 проверяет координатор.
- Текущий root HEAD ещё содержит Contracts gitlink
  `e5c056c47fc3bde3e0ca32866692d740ef9b325c`; checkout `26cacbe...` — dirty
  gitlink относительно HEAD. Новый root selection выполняет INT02, не DEV15.
- Root `git status --short` при чтении: изменены gitlinks Contracts/Portal/Results
  и execution/checkpoint; присутствуют чужие evidence/setup. Они не изменялись.
  Полный фактический recursive submodule status прочитан, reset/update не делались.
- Packaged Runner hashes сейчас:
  `run.schema.json=01ebc5aa635ae98d864fda23606d3228efc6020c68066496539227002ada6390`;
  `results-contract-set.json=bd14c6a62d35543b29e9473c8e388a3790524364c52b4d64922a74278c6fb2c1`;
  `PROVENANCE.json=dd7f1256d4f994cc554f53288a63ad299baba3866d465625876f0737fd43ea28`.
  Canonical results-contract-set имеет тот же `bd14...` hash. Совпадение старых
  declared hashes с packaged bytes — наблюдение, не ongoing guard.

### Round2 source rebind (текущее наблюдение)

Фактически прочитаны `git rev-parse HEAD`, `git status --short`,
`git submodule status --recursive` и `git ls-tree HEAD components/qcl-negf-contracts`.
Root теперь `04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6`, уже выбирает Contracts
`26cacbe1688fee0af300d0949fc6b94e55a29f4a` через Git gitlink. Старый root
`eb59809...` и его selected `e5c056c...` выше — честно сохранённая история,
не текущий blocker. Runner остаётся на том же immutable `0c53c6d...`, clean;
tracked diffs Core и Runner пусты. Чужие untracked Core файлы, Results/checkpoint
и evidence не тронуты. Это source receipt наблюдения, не отдельный maintained lock.
Во время правки координатор сообщил об active
`qcl-int01-julia-import-attempt-2.service`; этот D-task не проверял сервис и
не менял source inputs его импорта.

Прочитаны root AGENTS/architecture, handoff README/autonomy/P1, DEV14–16 и
общие envelopes, primary RV07/RV19 и narrow fixcards. Latest active EXEC B/G1/S1
передан координатором и сильнее старой записи PLAN в published handoff.

## 2. Найденное поведение и граница discovery

Проверены `git ls-files` (256 tracked Runner paths), broad `git grep` по всем
tracked paths, затем прочитаны relevant config/runtime/CLI/test/integration/
tools/Nix routes. Поиск включал PROVENANCE.json, run.schema.json,
results-contract-set, schema/hash/drift/canonical и SHA256. Это охватывает
tracked integration paths, а не только `src/` или один символ.

Enforcing verifier packaged schemas в выбранном Runner не найден. Existing
`_runtime_source_files` (`src/composition/production_runtime_adapter.jl:193`)
включает run schema в runtime source identity; он не сравнивает её с declared
hash/canonical Contracts и не заменяет rejection guard. `tools/ci.ts` запускает
native tests/docs/setup, но schema-copy check не содержит. Другой drift framework
не добавляется: DEV16 создаёт один общий verifier с CLI и двумя runtime вызовами.

Доказательная цепочка assigning-source:

| Факт | Первичный локатор в Runner 0c53c6d / Core a8d2c0d | Значение |
| --- | --- | --- |
| Lookup — get/last | `src/application/configuration_types.jl:216–221::configuration_source` | missing/empty history → `nothing`; typed field не читается |
| Recorded assignment merge | `src/infrastructure/config/configuration.jl:214–238::_deep_merge!`; `src/infrastructure/scientific/definitions.jl:387–462` | explicit files записывают filename; generated overrides — assigning identifiers, включая `#generated:`; subtree replacement удаляет displaced history |
| Source order | `src/infrastructure/config/configuration_sources.jl:31–55::validate_configuration_source` | schema load, ordered file merge, schema validation |
| 17/23 fixture | `test/application/configuration_merge_order_and_fail_closed_validation.jl:5–27` | base→first17→second23 даёт 23/second; reverse даёт17 |
| Required chunk | `src/infrastructure/config/configuration.jl:914–935::_parse_production` и canonical schema `$defs.production.required/properties.energy_chunk` | merged input обязателен; schema default отсутствует |
| Typed default | Core `src/numerics/optimized/production_contracts.jl:88–99::ProductionOptions` | `energy_chunk::Int = 64`; не источник явного YAML/JSON присваивания |
| Example64 | `test/fixtures/configurations/base.yaml:163` | здесь64 явно задан в файле, хотя число совпадает с typed default |
| Recorded generated marker | `test/contracts/generated_scientific_configuration_provenance.jl:32–38,100–110` | lookup возвращает `definition_path * "#generated:temperature-axis"`; freeze/load сохраняет recorded histories |
| Semantic boundary | `src/infrastructure/config/configuration_contract.jl:31–41,88–95` и `configuration.jl:1757–1782` | schema validation отдельно от Unitful/cross-field resolution |

## 3. Точные DEV15 изменения prose (будущий writer)

Разрешены только docstring `configuration_source`, guide и новый
`docs/schema-provenance.md`. API signature и function body не меняются.

### 3.1 Replacement docstring

```julia
"""
    configuration_source(configuration, dotted_path)

Return the last assigning-source identifier recorded in the provenance
history for `dotted_path`, or `nothing` when that history is absent or empty.
Explicit configuration leaves record source filenames; generated overrides
may record identifiers containing a `#generated:` marker. Later recorded
assignments override earlier assignments.

This lookup reports an assigning source. It does not infer a schema default,
a typed-constructor default, or the complete origin of an effective value.
It reads provenance only; source loading and validation are performed by
`validate_configuration_source` and `load_configuration_source`.

See [YAML run configurations](@ref yaml-run-configurations).
"""
```

### 3.2 Guide insertion after first paragraph of docs/src/user/configuration.md

```markdown
## Recorded assignments and value origins

`configuration_source(configuration, dotted_path)` returns the last
assigning-source identifier in that leaf's recorded provenance history.
Explicit configuration leaves record source filenames; generated overrides
may record identifiers containing a `#generated:` marker. Later recorded
assignments override earlier assignments. The lookup returns `nothing` when
the history is absent or empty, even if a typed field has a value. It reads
the recorded history; it does not load or validate source files.

The [merge-order fixture](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/0c53c6d0f68e0b25fce79388db831da6fc3ae856/test/application/configuration_merge_order_and_fail_closed_validation.jl)
starts with a base file and applies `first.yaml` with `energy_chunk: 17`, then
`second.yaml` with `energy_chunk: 23`. The resolved value is 23 and the assigning
source is `second.yaml`. Reversing those two overrides gives 17 and `first.yaml`.
These are fixture expectations; the source example is not a production-run receipt.

The merged declarative input requires a positive integer `production.energy_chunk`
and assigns no schema default. It sets the maximum number of energy points per
execution chunk for work scheduling; it does not set energy-grid spacing. The
Core `ProductionOptions` constructor has its own default of 64. The base fixture
also explicitly assigns 64. Equal values do not establish the same assigning
source, and an absent history does not identify that constructor as an origin.
The existing [generated-provenance fixture](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/0c53c6d0f68e0b25fce79388db831da6fc3ae856/test/contracts/generated_scientific_configuration_provenance.jl)
expects `configuration_source(configuration, "physical.lattice_temperature")`
to return `definition_path * "#generated:temperature-axis"`. That recorded
identifier names the generated assigning policy; it does not identify a physical
data source. Freeze/load preserves such recorded histories. The lookup returns
these markers when present; it does not reconstruct the complete effective-value
origin chain, including any further resource-planning decisions.

The owning [schema provenance contract](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/main/docs/schema-provenance.md) defines
packaged-byte verification and comparison with a selected workspace Contracts copy.
```

The guide uses an external source link, matching existing Runner documentation
conventions. Independent review checks its target against the candidate file;
the main-branch URL becomes available after the owning G1 merge. Documenter does
not list this outside-src file. Do not edit `docs/make.jl` under this card or
claim Documenter inclusion. A rendered-site schema-contract page would require
a separate docs-navigation task.

### 3.3 New docs/schema-provenance.md: exact authored prose

```markdown
# Packaged schema provenance

Contracts owns the canonical schema definitions. Runner packages their bytes in
`schema/` and records declared SHA256 digests in `schema/PROVENANCE.json`. Its
source URL and version are descriptive metadata. The selected workspace Git
gitlink identifies the Contracts source; this file is not a second revision lock.

The verification contract below is the DEV16 implementation target. At the
DEV15 baseline, recorded hashes alone do not enforce drift rejection. Update
this status sentence only after the implementation and its negative controls
have been reviewed on the published Runner source.

`tools/verify_schema_provenance.jl` provides one verifier for the CLI and runtime.
It parses the provenance mapping, checks every declared packaged file, and
hashes the exact captured bytes. Workspace mode additionally compares those
bytes with the canonical files below the selected root's
`components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/`. Standalone mode
checks bundled declared digests and needs no sibling Contracts checkout.

From a prepared root workspace, run:

    julia --startup-file=no --project=julia --threads=1 components/QCLNEGFRunner.jl/tools/verify_schema_provenance.jl --mode workspace --workspace-root .

From a prepared standalone Runner environment, run:

    julia --startup-file=no --project=. --threads=1 tools/verify_schema_provenance.jl --mode standalone

These commands need the selected Julia runtime and its existing YAML dependency.
They do not install packages or fetch a remote latest schema. A mismatch, missing
file, invalid provenance mapping, or unsupported mode fails with process status 2.
A successful check exits 0 and identifies the mode and checked-file count.

Runtime verification runs before a configuration schema is used and before
`_resolve_configuration` converts a declarative or frozen-plan mapping to typed
values. The package resolves resources from its loaded installation location.
It detects a source workspace from its component placement and root `.gitmodules`
marker; within a detected workspace, a missing Contracts copy is an error. An
installed standalone runtime uses its bundled files. It does not infer workspace
selection from the caller's current directory. Verification has no success cache.

Configuration APIs report verification failure as `ConfigurationError`; the
existing `qcl-negf` command maps that exception to status 2. The verifier does not
run at package import and does not add a new scientific acceptance condition.
A caller-supplied `schema_path` still undergoes the existing schema validation;
it does not bypass packaged verification or become a canonical packaged schema.

To update a packaged schema, first publish and review the canonical Contracts
change. Select that source through the workspace workflow, copy its schema bytes
without independent edits, and update the existing declared digest from those
bytes. Review the copy, provenance, and negative controls together in Runner.
The root integration owner subsequently publishes the owning gitlink selection.

Byte agreement establishes the checked schema copies' integrity. It does not
establish model adequacy, convergence, discretization sufficiency, experimental
validation, or the complete origin of an effective configuration value.
```

## 4. DEV16 precise enforcing contract

### Scope and accepted internal replan

Original DEV16 paths remain; coordinator additionally approves only
`src/infrastructure/config/configuration.jl::_resolve_configuration` for the
shared verifier call before `_expect_keys`/Unitful resolution. This corrects
the initial coordinator shorthand `src/application/configuration.jl`, which
does not name the actual file. The optional private root keyword described below
is an explicit CP-DESIGN candidate, endorsed for review by the coordinator.
No other function in configuration.jl is in scope. Public positional interfaces,
public loader keywords, schemas' constraints/defaults, model, equations,
discretization and all acceptance criteria remain unchanged.

### One implementation, two invocation forms

New `tools/verify_schema_provenance.jl` defines a small internal
`QCLSchemaProvenance` module. It imports only `SHA` and `YAML`, already direct
Runner dependencies; it never imports QCLNEGFRunner/Core/HDF5. At the bottom,
the direct-program condition invokes its CLI main only when this file is the
executed program. Runtime `configuration_contract.jl` includes that same file
through `_package_path("tools", "verify_schema_provenance.jl")`; inclusion must
not run CLI/main, exit, or verification. This is one verifier, not separate
runtime and CI algorithms. Nix currently copies the entire Runner tree
(`nix/package.nix`), including tools; no Nix edit is required for this contract.

Proposed exact internal API:

```julia
QCLSchemaProvenance.verify_schema_provenance(
    runner_root::AbstractString;
    mode::Symbol = :auto,
    workspace_root::Union{Nothing,AbstractString} = nothing,
)
QCLSchemaProvenance.main(arguments::AbstractVector{<:AbstractString};
    output::IO = stdout, errors::IO = stderr)::Int

QCLNEGFRunner._verify_configuration_schema_provenance(
    runner_root::AbstractString = _package_path(),
)
```

The CLI contract is IO-injectable for in-process assertions, without subprocesses.

`verify_schema_provenance` returns an internal NamedTuple with resolved
`mode`, `runner_root`, `workspace_root` (`nothing` standalone), `provenance_path`,
`hashes::Dict{String,String}`, and captured `files::Dict{String,Vector{UInt8}}`.
Byte snapshots are a local call result; no global registry/cache or emitted lock.
The wrapper converts known `SchemaProvenanceError(path, message)` into existing
`ConfigurationError(path, "schema provenance: ...")`. It does not blanket-catch
interrupts/OOM/programming errors.

### Input parsing, hashes and modes

1. Resolve supplied roots once with `abspath`/`realpath`. Metadata lives only at
   `<runner_root>/schema/PROVENANCE.json`. Read and parse the actual mapping;
   source/version are required nonempty strings; `sha256` is a nonempty mapping
   of string names to 64 lowercase hexadecimal digests, containing at least
   `run.schema.json` and `results-contract-set.json`. Verify every declared entry,
   never ignore unknown entries. A declared name must be a single safe basename:
   reject empty/dot/dotdot, either separator, absolute/drive paths and path escape.
   Each resolved packaged path must be a regular file confined to schema/.
2. Use YAML's safe parsing of the JSON subset with the strict mapping constructor
   already used at `configuration.jl:23–39` (`strict_unique_keys=true`). Reject
   duplicate/non-string keys, scalar/null metadata, missing/ill-typed required
   fields, bad digests and read errors. No new JSON package/dependency. Schema
   parsing remains the existing Draft2020-12/keyword validator. Locked root YAML
   is 0.4.17 (`julia/Manifest.toml:651–656`). Mandatory preimplementation read-only
   checkpoint: I must confirm its in-memory `YAML.load` overload against the
   prepared owning source before coding and record its exact signature/locator
   in the implementation receipt. If unavailable, only dependent parser work/
   runtime checks are blocked; no guessed overload, duplicate-key fallback,
   pathname reread, import/install/build is permitted. A separately inspected
   local YAML0.4.16 source is not execution/version proof for this lock. The shared
   internal helper is `QCLSchemaProvenance._strict_mapping_from_bytes(bytes, path)`:
   parse `String(copy(bytes))` with that strict constructor, preserving captured
   vectors for byte comparison/hash reporting; normalize string keys recursively.
   Runtime schema parsing reuses this helper, translating its parse failure to
   existing ConfigurationError formatting before Draft/keyword checks. Reusing
   this parser is not a second integrity implementation.
3. Capture each packaged file once; compute `bytes2hex(SHA.sha256(bytes))` from
   those bytes and compare with the declared hash. SHA is an existing stdlib
   dependency. Whole-schema semantic equality is not the oracle; whitespace-only
   one-byte drift must reject. Metadata is read each call, and there is no
   success cache or mtime shortcut.
4. `mode=:standalone` verifies bundled metadata/files only. It rejects a supplied
   workspace_root as conflicting input. `mode=:workspace` requires an explicit
   workspace_root and requires its Runner component path, after realpath, to
   equal runner_root. Compare every declared basename against
   `<workspace_root>/components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/<name>`;
   missing/unreadable/outside canonical files reject. Compare bytes (and report
   their hashes); no remote resolution, network, Git subprocess or latest lookup.
5. Runtime uses `mode=:auto`: when runner_root is exactly
   `<candidate>/components/QCLNEGFRunner.jl` and candidate has `.gitmodules`,
   choose workspace with that candidate. If Contracts is missing there, fail;
   do not silently fall back. Otherwise choose standalone. Explicit auto with
   workspace_root is invalid. `cwd`/active Julia project are not mode selectors.
   Nix's installed runtime lacks a root `.gitmodules` and canonical sibling,
   so it uses standalone without changing its present installation layout.
6. Runtime comparison checks the selected on-disk source, not Git cleanliness
   or commit authenticity. CP-SOURCE/INT02 independently bind those files to
   the published Contracts gitlink. No maintained duplicate revision lock and
   no new root edit are introduced by this Runner implementation.

### Exact CLI contract

Allowed options once each: `--mode standalone|workspace`,
`--workspace-root ROOT` (workspace only), `--runner-root ROOT` (optional,
primarily temporary-copy controls; default current script package directory).
Require explicit `--mode`; reject missing values, unknown/duplicate options and
unexpected positional arguments with exit2 and one diagnostic line. Roots may be
relative only when explicitly passed; normalize relative to invocation cwd.
Do not add auto CLI selection, environment bypass, silent refresh or repair mode.

Successful stdout is exactly
`schema provenance verified (mode=workspace, files=N)\n` or standalone equivalent;
stderr empty, return0. Known failure has empty stdout and
`schema provenance error at PATH: REASON\n` on stderr, return2. Wrong CLI syntax
uses `schema provenance usage error: REASON\n`, return2. No stack trace for known
input/mismatch errors; unexpected implementation errors propagate nonzero.

### Runtime enforcement and same-byte use

- `configuration_contract.jl` owns `_verify_configuration_schema_provenance` and
  the shared module inclusion. `_load_configuration_schema(path)` first obtains
  the snapshot from that wrapper, before schema parsing. For packaged
  run.schema.json, parse the captured verified bytes, not a second read of the
  path. Use the strict YAML constructor and preserve `_string_keyed_yaml`,
  Draft declaration and supported-keyword checks. A changed file after capture
  cannot replace the bytes consumed by that call. Caller-supplied schema_path
  remains supported and is parsed from its own captured bytes after package
  verification; its bytes are not falsely reported as canonical.
- Private testability extension to `_load_configuration_schema`:
  `; schema_provenance_root::AbstractString = _package_path()`.
  Public loaders/validators add no keyword and always use the package default.
- `_resolve_configuration(mapping::Dict{String,Any}, provenance;
  schema_provenance_root::AbstractString = _package_path())` gains exactly one
  first executable statement:
  `_verify_configuration_schema_provenance(schema_provenance_root)`.
  All existing positional callers keep their behavior on matching bytes. This
  private keyword is not a YAML field, frozen-plan field, CLI flag, environment
  setting or exported public API. It only selects a temporary-copy fixture for
  testing the actual method. It cannot skip verification.
- Alternative: keep `_resolve_configuration` signature unchanged and assert
  source call order plus verifier-only negatives. That avoids a private keyword
  but cannot directly prove the real method rejects temporary drift without
  touching selected files or using package-root mocks. Choose the private keyword
  for stronger actual-method evidence; reviewer accepts/rejects this choice.
- No verification in `default_configuration_schema`, `__init__`, package import,
  metadata lookup `configuration_source`, or unrelated analysis commands.
  Both `default_configuration_schema()` and exported String behavior stay
  compatible; no InitError is substituted for ConfigurationError.

Supported reachability:

| Entry route | Actual source route | Earliest enforcing boundary |
| --- | --- | --- |
| load_run_configuration, load_configuration_source, validate_configuration_source (string/vector) | `configuration.jl:1856–1860`; `configuration_sources.jl:31–91` | `_load_configuration_schema` before ordered source merge; `_resolve_configuration` before typed conversion |
| validate_configuration_schema | `configuration_contract.jl:88–95` | `_load_configuration_schema` before schema validation |
| qcl-negf plan / resolve_scientific_plan | `cli.jl::_cli_heavy`; `application/scientific/planning.jl::resolve_scientific_plan` | existing load_run_configuration route |
| qcl-negf run-plan / load_scientific_plan | `cli.jl::_cli_heavy`; `infrastructure/scientific/snapshots.jl:1–36` | shared `_resolve_configuration` before Unitful/typed configuration conversion |
| configured runtime consistency | `production_runtime_adapter.jl:130–134::_assert_runtime_configuration_consistency` | same `_resolve_configuration` |
| bin/qcl-negf, scientific_workflow.jl, resource_plan.jl, validate_configuration.jl | source calls above | same actual methods, no duplicated per-script checks |

Frozen-plan JSON/YAML parsing, fingerprints and existing structural reads can
precede `_resolve_configuration`; this contract promises rejection before typed
configuration resolution, solver invocation or configuration-dependent output
mutation, not before every raw dictionary read. Existing frozen semantic checks
are preserved; drift verification is not new schema validation of historical raw
plans. Direct in-memory Core operations and old independent Results readers do
not use this schema-copy contract. Custom typed objects that never enter these
configuration routes are outside its declared reachability.

## 5. DEV16 copy/publication workflow

After coordinator confirms published DEV14 ref and source selection, copy exactly
Contracts `src/qcl_negf_contracts/schemas/run.schema.json` into Runner
`schema/run.schema.json`. Independently recompute bytes/hash; expected canonical
DEV14 hash is `62df4ac2...0e58b` (full hash above). Update only the existing
`PROVENANCE.json` run-schema digest. Preserve source/version and the unchanged
results-contract-set digest unless their actual owning canonical bytes differ.
Do not hand-edit the second description, reformat the schema, add a version lock
or silently regenerate schema semantics. Compare parsed canonical/copy and byte
hashes; independently review the prose-only canonical diff.

At round1 the root selection was older. The round2 `04eecba...` source rebind
above confirms that INT02 has selected Contracts26cacbe through the root gitlink;
do not carry the historical selection mismatch as a present blocker. Canonical
publication/G1 receipts remain coordinator-owned, and a merely local unreviewed
copy is never publication. The Runner copy still requires the reviewed DEV16
owning workflow; no root locks/CI/gitlinks are edited by this D-task or DEV16.

## 6. Exact tests, negative controls, finite budget

New `test/contracts/schema_copy_provenance.jl`, unique suite module,
testset `Packaged schema provenance rejects drift before resolution`.
Existing test discovery (`test/run_group.jl`) includes every .jl in contracts;
no test registry/CI edit needed. Reuse `test/support/common.jl` and current
configuration fixture. No solve/benchmark/profiling/full suite.

All negative cases operate on temporary copies, never selected schemas:

| Assertion | Fixture/control and distinguishing observation |
| --- | --- |
| Exact positive standalone | Copy schema/PROVENANCE to temp Runner; no sibling Contracts; returned two hashes equal independently calculated SHA of temp bytes |
| Exact positive workspace and auto | Temp workspace component layout with .gitmodules marker and copied canonical schemas; compare both files and assert resolved mode/root |
| Packaged one-byte drift | Append a newline to temp run schema without changing manifest; exact-byte digest mismatch although parsed meaning is unchanged |
| Stale provenance | Replace only run digest with 64 zeros; correct file remains unchanged; mismatch |
| Canonical workspace drift | Change only canonical temp file byte; bundled manifest remains consistent; workspace mismatch and standalone success on identical bundled bytes |
| Missing declared payload | Remove results-contract-set temp file; reject (proves check is not run-schema-only) |
| Missing canonical / no fallback | Remove temp Contracts schema under detected workspace; auto/workspace reject, not standalone fallback |
| Invalid provenance | Missing map, non-string/bad hash, missing run/results entry, duplicate key and unsafe name reject before callback/use |
| CLI behavior without subprocess | Call shared main with IOBuffer output/errors; success0, mismatch2 and syntax2; assert empty/single-line streams and no writes to original files |
| Actual schema-loader order | `_load_configuration_schema(temp_run; schema_provenance_root=temp_runner)` rejects corrupted bundled bytes as ConfigurationError with schema-provenance reason before unsupported-schema-keyword parsing |
| Same captured bytes | Unit helper parses snapshot bytes after the underlying temp pathname changes; assert parsed object derives from old verified bytes, then next fresh verification rejects new bytes (no cache). No concurrency threads needed |
| Actual snapshot-to-parse flow | CP-CODE must inspect actual `_load_configuration_schema` → returned snapshot `files["run.schema.json"]` → strict parser argument on the same candidate and record exact source locators. A helper-race assertion alone is insufficient; no packaged pathname reread or fallback may feed parsing |
| Actual typed-resolver order | Load valid base mapping, replace lattice_temperature with `200 eV`; `_resolve_configuration(mapping, base.provenance; schema_provenance_root=corrupt_temp_runner)` reports schema provenance first. Matching temp copy then reports existing wrong-dimension error. No selected-file edits/mock Core/import stubs |
| Frozen-plan reachability | Review exact `snapshots.jl::load_scientific_plan` call to shared `_resolve_configuration`; fixture above exercises that actual conversion method. Full CLI/frozen-plan process execution is not claimed by this bounded direct-method check |

Preserve existing merge fixture assertions. Add explicit reverse-source assertion
ending first.yaml. Add missing history and empty-history assertions using a deep
copy of the loaded config (its provenance.sources dictionary is mutable): removing
the leaf or assigning `String[]` returns `nothing` while production.energy_chunk
still has a typed value. Base configuration explicitly64 still reports base.yaml;
this controls confusion with Core constructor default64. Do not change constructors
or a scientific fixture to manufacture missing schema defaults.

The existing generated-provenance test (`:32–38,100–110`) is an unchanged source
anchor for C1, not a third runtime invocation. Its recorded marker expectation
and freeze/load history preservation were checked statically in this round.

Read-only preflight/`git diff --check`/link checks are L-SOURCE. Runtime only after
INT01 confirms exact Julia1.13.0, locked YAML0.4.17/source-bound package route,
prepared depot and available shared test slot. Set OPENBLAS_NUM_THREADS=1 and
JULIA_NUM_THREADS=1. At most two Julia process invocations total, including any
red/green corrections: each ≤120s, 1CPU/2GiB; combined ≤4min, ≤16MiB temporary,
≤2MiB logs. Apply timeout TERM then kill-after5s and available memory enforcement.
Do not spawn Julia subprocesses inside fixtures. Record original failure/output,
actual executable/version/import ownership and temp/log sizes. Cost limit is an
engineering envelope, not a numerical tolerance. On cap/missing runtime stop the
runtime check and retain source evidence; no hidden Pkg.instantiate or compile loop.

Two maximum invocation commands from selected root, pending runtime owner:

```sh
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/contracts/schema_copy_provenance.jl")'
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/application/configuration_merge_order_and_fail_closed_validation.jl")'
```

These tests do not establish cold package relocation/native Nix installation,
full suite coverage, process-level frozen-plan execution, scientific convergence
or physical acceptance. Existing schema scattering/domain helper remains an
unchanged source anchor; no extra third invocation is implied.

## 7. CP-DESIGN questions and READY I handoff

Reviewer receives immutable Runner0c53c6d, Contracts26cacbe, primary RV07/RV19,
this file and the question before being shown any suggested verdict:

1. Is the assigning-source identifier wording correct for missing/empty provenance,
   base64, merge17/23/reverse, already-recorded generated markers and the boundary
   to the complete effective-value/resource-planning origin chain?
2. Does one shared YAML+SHA implementation with explicit CLI modes and structural
   runtime auto detection correctly cover source-workspace versus installed Nix/
   standalone routes, with no missing-Contracts fallback or cwd selection?
3. Are both approved seams sufficient before schema use/typed configuration
   conversion, including frozen plans, without import-time failure or accidental
   schema/model/default changes? Accept private root injection or state a cheaper
   equally strong actual-method negative control.
4. Are same-byte parsing, no success cache, custom schema_path compatibility,
   diagnostic type/status and declared-file coverage complete and bounded?
5. Does the finite fixture protocol distinguish integrity failures without new
   solver work, source mutation or ungranted root changes? Does the prose link
   remain valid for source readers without claiming Documenter rendering?

READY for I requires independent CP-DESIGN, canonical DEV14 publication check,
source-bound INT01 release of Runner write ownership, and runtime slot readiness
for any tests. Source implementation may proceed without runtime claims if the
runtime is still blocked; tests cannot be called passing until actually executed.
Medium implementer edits only original DEV16 paths plus the precise approved
`_resolve_configuration` seam/private keyword. DEV15 prose is applied by its sole
writer when ownership is released. Any additional root/doc-nav/native integration
change is a separate owning task. No further human approval is required for this
internal compatible design decision within active grants.

## 8. Завершение текущего D этапа

### Round2 response to independent review

Review `/tmp/qcl-dev15-design-review.md` принял shared guard, оба seams,
workspace/standalone modes, private keyword и bounded controls, оставив C1.
C1 принят: lookup читает `last(history)`, а `definitions.jl` уже записывает
generated assigning identifiers. В docstring/guide/source matrix исправлено
universal filename/explicit-only определение; добавлен точный unchanged fixture
пример `#generated:temperature-axis`. Границы typed/schema defaults и полного
effective-origin inference сохранены. Function body/API/scientific fixture values
не меняются. Design guard/seams/modes/private keyword не пересматриваются.

Первый candidate сохранён byte-for-byte в
`/tmp/qcl-dev15-design-round1.md`, SHA256
`662f0bdf5d51df3cf4e907645a56da6d125eb64e99db21429096e74bd8393c82`;
original `/tmp/qcl-dev15-design.md` также не изменён. V2 и отдельный unified diff/
response с hashes передаются координатору для closure на втором design round,
без третьего раунда или повторного human question. YAML source-overload checkpoint
и actual snapshot-to-parse CP-CODE evidence уточнены по review, без снятия условий.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Assigning source — last recorded identifier, включая generated marker; не typed/default origin | Runner0c53c6d configuration_source/definitions/merge и generated-provenance fixtures; Core a8d2c0d ProductionOptions | Runtime fixture не запускался; C1 исправлен статически | изменить prose |
| Packaged schema пока старая | Точные byte hashes и Contracts26cacbe canonical diff | Canonical publish/G1 receipt у координатора | изменить через DEV16 owning copy |
| Tracked Runner enforcing guard не найден | Все256 tracked paths; broad git grep + tools/config/runtime/Nix/test reads | Не утверждение о внешних/untracked CI systems | изменить одним общим verifier |
| Один loader seam не покрывает frozen typed path | snapshots.jl прямой _resolve_configuration; точные локаторы выше | Узкий extension утверждён координатором, CP-DESIGN ещё нужен | изменить shared guard invocation |
| Проверки integrity не scientific acceptance | Explicit byte-only contract и unchanged semantic paths | Native/runtime/численные проверки здесь не выполнялись | сохранить границы; дополнительно измерить fixtures |
| Product tree не изменён этим автором | Runner clean; tracked Core/Runner diffs пусты в round2 | Root dirty foreign work сохранён; /tmp reports не publication | сохранить |
