# QCL-NEGF results

Scientific result inspection and export for QCL-NEGF. The package validates immutable artifact inventories, HDF5 payloads and Parquet telemetry, then creates checksummed snapshots suitable for analysis and transfer. It can run independently of the solver and AiiDA.

## Installation

Python 3.14 is supported. The distribution includes the boundary validation and schema resources formerly supplied by `qcl-negf-contracts`; no separate contracts package is required.

```console
uv venv
uv pip install '.[test]'
.venv/bin/python -m pytest tests contracts-tests
```

The migrated sources are Results `cefffb3460545410e3e5f17c74ade999efc76cf7` and Contracts `bd1270d00502120b37377e8522a0bf4eb3926401`. The reader remains independent of the solver and retains its own scientific calculations. Its bundled contract resources are the current copy for this distribution; runner and analysis must eventually consume a single shared schema source in the application. The Runner and Contracts copies of `results-contract-set.json` match; their `run.schema.json` files differ, including the `human_every` field. Reconcile that schema against the actual Runner configuration and validate consumers before choosing one authoritative copy. Until then, schema changes must be checked against both copies.

## Inspect and export

```console
.venv/bin/qcl-negf-results preview /data/calculation --profile science
.venv/bin/qcl-negf-results export /data/calculation /data/exports --profile science --status completed
.venv/bin/qcl-negf-results render /data/calculation/point/artifacts /data/figures
.venv/bin/qcl-negf-receive --help
```

The command prints a JSON receipt. `preview` inspects committed metadata; `export` opens and verifies the payloads. Supply the status recorded by AiiDA. The default is `running`, which does not claim the calculation has finished.

```python
from pathlib import Path
from qcl_negf_results.export import export_snapshot

receipt = export_snapshot(
    Path("calculation"), Path("exports"), profile="science", job_status="completed"
)
```

| Profile | Contents |
| --- | --- |
| `science` | Analysis arrays, scalar histories, selected diagnostic witnesses, model, plan and compacted telemetry |
| `full-state` | Science contents plus full physics and recovery state |

Exports preserve native values and provenance. Compaction validates logical payloads, including NaN bit patterns and signed zero. Diagnostic witness selection keeps per-attempt boundary and extremum records with an explicit selection proof; full scalar history remains available. Source files are not rewritten.

Telemetry identifies CPU intervals by `allocation_id` (for example, a Slurm job/step identity), with separate execution and process identities. Missing counters remain unknown. `TelemetryWriter` is a library for producers; it does not run a background machine sampler.

Every archive part is at most 200,000,000 decimal bytes. Receipts describe all parts and hashes. The receiving command verifies the complete part set before restoring objects. Archive metadata and paths are checked; incomplete, altered or unsupported input fails explicitly. Disk usage includes a temporary captured snapshot in addition to the published archive.

Scientific series v4 and committed point records declare `scientific_status`
with six independent fields for the process, iterative convergence, the
stationary physical candidate, discretization, the operator check and the
campaign verdict. Each unmeasured scientific field is recorded as `unknown`.
A valid artifact can contain a failed operator check or an unresolved campaign
verdict. The analysis layer preserves both outcomes in its views and exports.
The nullable `converged` field mirrors the solver's joint convergence and
final validation flag. The iterative field reports the iteration assessment.
Payloads use the `qcl-negf.results.v1` contract set and native HDF5 `4.0`.

## Modules

- `export`, `multipart`, `diagnostic_archive`: verified snapshots and transport.
- `native`, `model`, `history`, `witnesses`: native payload validation and provenance.
- `telemetry`, `catalog`, `compaction`: durable typed performance records.
- `render`, `progress`, `presentation`: derived local diagnostic views. Scientific source arrays remain authoritative.

The package uses no scheduler queue or deployment service. Artifact file replacement is a durability mechanism for scientific data, not an application update mechanism.

## Tests

```sh
julia --startup-file=no --project=../runner -e 'using Pkg; Pkg.instantiate()'
uv run --extra test pytest tests contracts-tests integration
```

The integration suite runs Julia SCBA while Python exports its published result.
It uses the application’s `runner/` environment. To select a different installed
Julia executable or project, set `JULIA` or `QCL_NEGF_SOLVER_PROJECT`. Unit tests
include analytical and synthetic states. MIT licensed. [License](LICENSE)

Для независимого расчёта тока на внутренних связях и двух швах передайте
каталог артефактов научной точки. Команда проверяет SHA-256 полного состояния
и возвращает координаты в нанометрах и ток электронов вдоль +z в А/м².

```sh
qcl-negf-results current-profile POINT/artifacts
```
