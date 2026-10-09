# Packages для локального development lab

Этот путь собирает точный private development snapshot. Он не публикует release: production
`ops/git.ts` / `ops/solver.ts` сохраняют GitHub-only source guard. Состав автоматически выводит
`lab:snapshot` из authoritative Gitlinks и clean component HEADs; generated JSON является provenance
одной попытки.

Команды выполняются из root checkout на Linux x86_64. До запуска задайте конечный бюджет и проверьте
свободные RAM/диск с учётом работающих VM. Пример ниже ограничивает каждую package build 3600 s,
двумя Nix jobs и двумя cores. Это конечный пример бюджета, а не обещание времени сборки. После
timeout нужен явный новый бюджет. SCBA/Poisson не запускаются. Nix flags сами не ограничивают число
внутренних Julia subprocesses: owning Runner задаёт `JULIA_CPU_THREADS=2` для upstream install-check
и проверяет `Sys.CPU_THREADS` / `Sys.EFFECTIVE_CPU_THREADS`, сохраняя весь выбранный upstream suite.
Имена ignored каталогов каждой попытки должны быть новыми; snapshot нельзя переносить.

## Snapshot и dependency depot

```sh
set -e
mkdir -p "$PWD/.build/local-lab"
export LAB_CAPTURE="$PWD/.build/local-lab/sources-attempt"
export LAB_PACKAGES="$PWD/.build/local-lab/packages-attempt"
deno task lab:snapshot "$LAB_CAPTURE" > .build/local-lab/snapshot-capture-attempt.json
mkdir -m 700 "$LAB_PACKAGES"
export LAB_EVIDENCE="$LAB_CAPTURE/snapshot.json"
```

Нужен `qcl-negf.julia-depot.v1` metadata file с `julia: "1.13.0"`, SHA-256 native Manifest, URL и
SRI hash архива. Для существующего внешнего dependency depot задайте `LAB_DEPOT_METADATA` на его
проверенный receipt. `juliaManifest` должен совпасть с snapshot; hash архива проверяет
`nix store prefetch-file` ниже. Поле `sources` нового metadata выбирает build graph. Оно не
утверждает, что переиспользованный архив был подготовлен из позднейшего snapshot commit;
происхождение подготовки сохраняйте отдельно.

Для нового depot используйте owning Runner, exact Julia 1.13.0 и snapshot environment:

```sh
set -e
deno task --cwd components/QCLNEGFRunner.jl bootstrap
export JULIA="$PWD/components/QCLNEGFRunner.jl/.build/julia/bin/julia"
export LAB_REPOSITORY="$(python3 -c 'import json,os; print(json.load(open(os.environ["LAB_EVIDENCE"]))["snapshot_root"])')"
export LAB_ARCHIVE="$LAB_PACKAGES/depot.tar.gz"
export LAB_DEPOT_METADATA="$LAB_PACKAGES/prepared-depot.json"
sha256sum "$LAB_REPOSITORY/julia/Manifest.toml" > "$LAB_PACKAGES/preparation-manifest.sha256"
timeout --kill-after=30s 3600s deno run --allow-read --allow-write --allow-env --allow-run \
  "$LAB_REPOSITORY/components/QCLNEGFRunner.jl/tools/ci.ts" prepare-depot \
  "$LAB_REPOSITORY/julia" "$LAB_PACKAGES/depot"
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner \
  -czf "$LAB_ARCHIVE" -C "$LAB_PACKAGES/depot" .
python3 - <<'PY'
import base64, hashlib, json, os, subprocess
from pathlib import Path
root = Path(os.environ['LAB_PACKAGES'])
evidence = json.loads(Path(os.environ['LAB_EVIDENCE']).read_text())
manifest = Path(evidence['snapshot_root']) / 'julia/Manifest.toml'
digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
assert digest == (root / 'preparation-manifest.sha256').read_text().split()[0]
assert subprocess.check_output([os.environ['JULIA'], '--startup-file=no', '-e', 'print(VERSION)']).decode() == '1.13.0'
archive = Path(os.environ['LAB_ARCHIVE'])
with archive.open('rb') as stream:
    sha = hashlib.file_digest(stream, 'sha256').digest()
value = {'format': 'qcl-negf.julia-depot.v1', 'sources': evidence['source_graph'],
         'julia': '1.13.0', 'juliaManifest': digest, 'url': archive.as_uri(),
         'hash': 'sha256-' + base64.b64encode(sha).decode()}
with Path(os.environ['LAB_DEPOT_METADATA']).open('x') as out:
    out.write(json.dumps(value, indent=2) + '\n')
PY
```

Runner проверяет exact Julia, неизменность Manifest и artifact tree hashes; удаляет
compiled/log/scratch caches и сохраняет captured registry. Не используйте receipt неудачной
подготовки. Для готового depot пропустите этот блок, сохранив исходный receipt и архив. Далее новый
binding создаётся одинаково для обоих случаев:

```sh
python3 - <<'PY'
import hashlib, json, os, subprocess
from pathlib import Path
evidence_path = Path(os.environ['LAB_EVIDENCE'])
evidence = json.loads(evidence_path.read_text())
assert evidence['schema'] == 'qcl-negf.local-development-snapshot.v1'
assert evidence['published_release'] is False
repo = Path(evidence['snapshot_root'])
revision = evidence['snapshot_revision']
graph = evidence['source_graph']
assert graph['revision'] == revision
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip() == revision
assert not subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain=v1', '--untracked-files=all'])
manifest_hash = hashlib.sha256((repo / 'julia/Manifest.toml').read_bytes()).hexdigest()
old = json.loads(Path(os.environ['LAB_DEPOT_METADATA']).read_text())
assert old['format'] == 'qcl-negf.julia-depot.v1' and old['julia'] == '1.13.0'
assert old['juliaManifest'] == manifest_hash
output = Path(os.environ['LAB_PACKAGES'])
metadata = {**old, 'sources': graph}
metadata_path = output / 'solver-depot.json'
inputs = {'source': 'git+' + repo.as_uri() + '?rev=' + revision + '&submodules=1',
          'snapshotRevision': revision, 'sourceGraph': graph,
          'preparedManifestSha256': manifest_hash, 'depotManifest': str(metadata_path)}
binding = {'snapshot_evidence': str(evidence_path), 'snapshot_revision': revision,
           'dependency_receipt': str(Path(os.environ['LAB_DEPOT_METADATA'])),
           'semantics': 'external dependency depot reused with identical native Manifest; sources selects build graph',
           'scientific_accepted': False, 'published_release': False}
for path, value in ((metadata_path, metadata), (output / 'package-input.json', inputs),
                    (output / 'depot-binding.json', binding)):
    with path.open('x') as out:
        out.write(json.dumps(value, indent=2) + '\n')
prefetch = subprocess.check_output(['nix', '--extra-experimental-features', 'nix-command flakes',
    'store', 'prefetch-file', '--hash-type', 'sha256', '--expected-hash', metadata['hash'],
    '--name', 'qcl-negf-julia-depot.tar.gz', metadata['url'], '--json'])
with (output / 'depot-prefetch.json').open('xb') as out:
    out.write(prefetch)
PY
```

Verified prefetch использует exact `fetchurl` name: Nix sandbox не читает произвольный host path
архива. Сохраните оригинальный архив для prefetch после garbage collection.

## Сборка и installed integrity

Сначала `--dry-run`, затем actual build для каждой package, последовательно:

```sh
set -e
for LAB_PACKAGE in application solver synthetic; do
  nix --extra-experimental-features 'nix-command flakes' build --dry-run --impure \
    --no-link --max-jobs 2 --cores 2 --file nix/local-lab-packages.nix \
    --argstr inputFile "$LAB_PACKAGES/package-input.json" --argstr package "$LAB_PACKAGE"
  timeout --kill-after=30s 3600s nix --extra-experimental-features 'nix-command flakes' \
    build --impure --no-link --print-out-paths --max-jobs 2 --cores 2 \
    --file nix/local-lab-packages.nix --argstr inputFile "$LAB_PACKAGES/package-input.json" \
    --argstr package "$LAB_PACKAGE" > "$LAB_PACKAGES/$LAB_PACKAGE.path" \
    2> "$LAB_PACKAGES/$LAB_PACKAGE.log"
done
```

Не продолжайте после failed command; перед следующей build повторите RAM/disk admission. Сохраните
`nix path-info --json` outputs для NAR hashes и `nix flake metadata --json` для exact source store
path. Application/synthetic сами не требуют depot fields: для них достаточно автоматически
полученных `source`, `snapshotRevision`, `sourceGraph`.

Из application Python проверьте imports, locked versions, console metadata и factories в свежем
scoped `AIIDA_PATH`:

```sh
export LAB_SOURCE_URL="$(python3 -c 'import json,os; print(json.load(open(os.environ["LAB_PACKAGES"]+"/package-input.json"))["source"])')"
nix --extra-experimental-features 'nix-command flakes' flake metadata --json \
  --no-write-lock-file "$LAB_SOURCE_URL" > "$LAB_PACKAGES/source-store.json"
export LAB_STORE_SOURCE="$(python3 -c 'import json,os; print(json.load(open(os.environ["LAB_PACKAGES"]+"/source-store.json"))["path"])')"
LAB_APPLICATION="$(cat "$LAB_PACKAGES/application.path")"
AIIDA_PATH="$LAB_PACKAGES/installed-aiida-check" "$LAB_APPLICATION/bin/python" - \
  > "$LAB_PACKAGES/installed-application-check.json" <<'PY'
import importlib, json, os, sys, tomllib
from importlib.metadata import distribution
from pathlib import Path
from aiida.plugins import CalculationFactory, ParserFactory, WorkflowFactory
import h5py
source = Path(os.environ['LAB_STORE_SOURCE'])
assert str(source).startswith('/nix/store/') and sys.version_info[:2] == (3, 14)
lock = tomllib.loads((source / 'uv.lock').read_text())
projects = {'qcl-negf-contracts': ('qcl_negf_contracts', 'qcl-negf-contracts'),
    'qcl-negf-results': ('qcl_negf_results', 'qcl-negf-results'),
    'aiida-qcl-negf': ('aiida_qcl_negf', 'qcl-negf-aiida'),
    'qcl-negf-api': ('qcl_negf_api', 'qcl-negf-portal')}
versions = {}
for name in (*projects, 'aiida-core', 'h5py'):
    versions[name] = distribution(name).version
    assert {versions[name]} == {p['version'] for p in lock['package'] if p['name'] == name}
for name, (module, component) in projects.items():
    assert str(Path(importlib.import_module(module).__file__).resolve()).startswith('/nix/store/')
    declared = tomllib.loads((source / 'components' / component / 'pyproject.toml').read_text())
    installed = {e.name: e.value for e in distribution(name).entry_points if e.group == 'console_scripts'}
    assert all(installed.get(k) == v for k, v in declared['project'].get('scripts', {}).items())
for factory, label in ((CalculationFactory, 'qcl_negf.execution'),
    (ParserFactory, 'qcl_negf.execution'), (WorkflowFactory, 'qcl_negf.plan'),
    (WorkflowFactory, 'qcl_negf.execution_restart')):
    factory(label)
print(json.dumps({'status': 'completed', 'scope': 'installed package integrity',
    'scientific_accepted': False, 'versions': versions, 'python': sys.version,
    'hdf5_library_version': h5py.version.hdf5_version, 'source': str(source)}))
PY
```

Controller profile/bootstrap identity проверяется после closure delivery по
[platform handoff](../components/qcl-negf-platform/docs/local-lab.md).

## Application stage: четыре role closures

Public API `nix/local-lab-systems.nix { inputFile, siteFile }` возвращает `systems`, `application`,
`solver` из exact captured snapshot. Application и solver проходят существующий
`local-lab-packages.nix`, включая source graph, prepared Manifest и depot guards, даже при выборе
только storage-роли. `siteFile` — JSON public lab configuration для platform `mkLocalLab`: hosts,
nodes, partitions, SSH public key, service email и optional API resource limits. Secret bytes,
private SSH/Munge keys и API token в этот JSON не входят.

Следующие команды только вычисляют четыре `.drv` и ожидаемые output paths; они не создают image, не
собирают closures и не активируют VM.

Для evaluation четырёх ролей задайте resident `MemoryMax=3GiB`, swap 0 и `CPUQuota=100%` в transient
user scope; перед запуском нужны ≥4GiB MemAvailable и свободного диска. Ограничение virtual address
space отдельно от resident RAM может прервать Nix evaluator до завершения.

```sh
export LAB_SITE_JSON="$PWD/.build/local-lab/private/app-role-site.json"
export LAB_INPUT_FILE="$LAB_PACKAGES/package-input.json"
timeout --kill-after=10s 240s nix --extra-experimental-features 'nix-command flakes' \
  eval --impure --json --file nix/local-lab-systems.nix \
  --apply 'make: let result = make { inputFile = builtins.getEnv "LAB_INPUT_FILE";
    siteFile = builtins.getEnv "LAB_SITE_JSON"; };
    in builtins.mapAttrs (_: system: system.drvPath) result.systems' \
  > "$LAB_PACKAGES/role-derivations.json"
timeout --kill-after=10s 240s nix --extra-experimental-features 'nix-command flakes' \
  eval --impure --json --file nix/local-lab-systems.nix \
  --apply 'make: let result = make { inputFile = builtins.getEnv "LAB_INPUT_FILE";
    siteFile = builtins.getEnv "LAB_SITE_JSON"; };
    in builtins.mapAttrs (_: system: system.outPath) result.systems' \
  > "$LAB_PACKAGES/systems.json"
```

`systems.json` имеет ровно `control`, `storage`, `worker-1`, `worker-2` и подходит существующему
[platform helper](../components/qcl-negf-platform/docs/local-lab-orchestration.md). После отдельно
разрешённых bounded build и signed closure delivery повторный
`prepare --systems "$LAB_PACKAGES/systems.json"` с прежними namespace, image, pool и libvirt URI
обновляет только выбранные role paths. Затем `inventory` передаёт их как `qcl_lab_system`
существующему Ansible playbook. Сохраните protected backing image, disks и private keys; image
replacement для этой стадии не требуется. Cold profile preparation, controller API token и порядок
первого handoff описаны в platform docs. Evaluation этих paths не подтверждает delivery, activation,
application readiness или научную приёмку.

Synthetic package устанавливает `bin/qcl-negf-synthetic-transport-1`: installed application Python
исполняет immutable snapshot `components/qcl-negf-aiida/tests/transport_fixture.py`. Проверьте
actual closure references на application и source, затем доставьте wrapper closure обоим workers.
Это отдельный `SYNTHETIC-` InstalledCode. Controller rehearsal исполняет immutable
`tests/run_transport_acceptance.py` через installed `verdi -p PROFILE run` с внешним deadline.
Production Code allowlist и admission predicates сохраняются.

Приёмка transport требует ровно один owned Slurm attempt, WorkChain 400 / CalcJob 303, unchanged
frozen plan, `converged:false`, `scientific_accepted:false` и измеренный terminal scheduler receipt.
`qcl-negf self-check` — отдельная finite проверка (например, 300 s, 1 CPU, 2 GiB на worker).
Integrity, завершение процесса, сходимость, физические проверки, дискретизация и экспериментальная
валидация остаются отдельными утверждениями.
