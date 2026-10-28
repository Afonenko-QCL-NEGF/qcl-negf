"""Create tiny source-only Nix fixtures explicitly; no build or dependency bootstrap."""
import argparse
from pathlib import Path
import shutil


def create(output):
    repo = Path(__file__).resolve().parents[1]
    output.mkdir()  # never overwrite an earlier attempt
    recipes = ['nix/depot-compatibility.nix', 'nix/depot-project.nix', 'ops/depot_producer.ts',
               'components/QCLNEGFRunner.jl/tools/ci.ts',
               'components/QCLNEGFRunner.jl/tools/prepare_depot.jl',
               'components/QCLNEGFRunner.jl/tools/depot_native_facts.jl']
    metadata = ['julia/Project.toml', 'julia/Manifest.toml',
                'components/QCLNEGF.jl/Project.toml', 'components/QCLNEGF.jl/Manifest.toml',
                'components/QCLNEGFRunner.jl/Project.toml']
    for name in ('a', 'docs', 'source', 'project', 'selector', 'prefs', 'alias'):
        root = output / name
        root.mkdir()
        for rel in recipes + metadata:
            src = repo / rel
            if not src.exists():
                continue
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        for rel in ('components/QCLNEGF.jl/src/example.jl', 'components/QCLNEGF.jl/LICENSE',
                    'components/QCLNEGFRunner.jl/src/example.jl', 'components/QCLNEGFRunner.jl/LICENSE',
                    'components/QCLNEGFRunner.jl/schema/example.json',
                    'components/QCLNEGFRunner.jl/tools/verify_schema_provenance.jl',
                    'components/QCLNEGFRunner.jl/scripts/scientific_workflow.jl',
                    'components/QCLNEGFRunner.jl/examples/config/example.yaml'):
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text('# manufactured source-only fixture\n')
    (output / 'docs/README.md').write_text('docs graph changed\n')
    (output / 'source/components/QCLNEGF.jl/src/example.jl').write_text('# changed runtime source\n')
    with (output / 'project/components/QCLNEGF.jl/Project.toml').open('a') as stream:
        stream.write('\n# Project bytes changed\n')
    (output / 'selector/components/QCLNEGF.jl/.pkg').mkdir()
    (output / 'selector/components/QCLNEGF.jl/.pkg/select_artifacts.jl').write_text('error("unqualified")\n')
    (output / 'prefs/julia/LocalPreferences.toml').write_text('[MPIPreferences]\nbinary="system"\n')
    (output / 'alias/julia/JuliaArtifacts.toml').write_text('# native alias addition\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    create(parser.parse_args().output)
