"""One ordinary sandboxed DOC04 producer, invoked only by nix/docs.nix.

Only declared immutable public inputs enter this process. Private admission,
resource inventory and host credentials stay with the CLI. Candidate completion
uses the existing AS1 and owning Contracts C1/C2; it is not publication/science.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import resource
import selectors
import shutil
import subprocess
import sys
import tempfile
import time

MAX_FILE = 16 * 1024 * 1024
MAX_PUBLIC = 64 * 1024 * 1024
MAX_LOG = 8 * 1024 * 1024
OWNERS = (('core', 'components/QCLNEGF.jl'), ('runner', 'components/QCLNEGFRunner.jl'),
          ('operator', 'root'))
STORE = re.compile(r'/nix/store/[0-9a-df-np-sv-z]{32}-[^/]+(?:/[^/]+)*\Z')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode('utf-8')


def decode_json(data):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError('duplicate_json_key')
            result[key] = value
        return result
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))


def fields(value, names):
    if not isinstance(value, dict) or set(value) != set(names):
        raise ValueError('input_shape: ' + ','.join(names))


def store_path(value):
    if not isinstance(value, str) or not STORE.fullmatch(value):
        raise ValueError('immutable_store_path')
    path = Path(value)
    if any(part in ('.', '..') for part in value.split('/')) or str(path) != value:
        raise ValueError('immutable_store_path')
    if not path.exists() or path.is_symlink():
        raise ValueError('missing_store_input: ' + value)
    # Store outputs can contain symlinks internally; public declared file inputs
    # must resolve within the immutable store, never into mutable host paths.
    if not str(path.resolve()).startswith('/nix/store/'):
        raise ValueError('mutable_store_target')
    return path


def read_file(path, maximum=MAX_FILE):
    if not path.is_file() or path.is_symlink() or path.stat().st_size > maximum:
        raise ValueError('file_input_limit: ' + str(path))
    with path.open('rb') as handle:
        data = handle.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError('file_input_limit')
    return data


def record(value, maximum=MAX_FILE):
    fields(value, ('path', 'sha256'))
    if not isinstance(value['sha256'], str) or not re.fullmatch('[a-f0-9]{64}', value['sha256']):
        raise ValueError('input_hash_shape')
    data = read_file(store_path(value['path']), maximum)
    if sha(data) != value['sha256']:
        raise ValueError('input_hash_mismatch: ' + value['path'])
    return data


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def runtime_context(page):
    depth = len(PurePosixPath(page).parts) - 1
    prefix = '../' * depth
    return {'destination': 'assets/runtime-depth-' + str(depth) + '.js',
            'worker_url': prefix + 'assets/search-worker.js',
            'asset_prefix': prefix + 'assets/vendor'}


def bridge_math(raw, page):
    """Pinned Documenter1.17 text-node shapes; assign deterministic page IDs.

    No HTML regex extraction or TeX evaluation. Ambiguous/unbalanced candidate
    math fails; the bridge never silently removes a formula.
    """
    assembly = module('_qcl_bridge_assemble', Path(__file__).with_name('assemble.py'))
    tree = assembly._Tree(raw.decode('utf-8'))
    records, ids = [], set()
    def visit(node):
        attrs = node.attr()
        if attrs.get('id'):
            if attrs['id'] in ids:
                raise ValueError('duplicate_html_id')
            ids.add(attrs['id'])
        classes = attrs.get('class', '').split()
        text = assembly._text(node)
        display = node.tag == 'p' and 'math-container' in classes
        inline = node.tag == 'span' and (text.startswith('$') or text.endswith('$'))
        if display or inline:
            if any(child.tag != '#text' for child in node.children):
                raise ValueError('ambiguous_documenter_math')
            begin, end = ('\\[', '\\]') if display else ('$', '$')
            if not text.startswith(begin) or not text.endswith(end) or len(text) < len(begin) + len(end):
                raise ValueError('ambiguous_documenter_math')
            tex = text[len(begin):-len(end)]
            if not tex or len(tex.encode()) > 16384 or (not display and re.search(r'(?<!\\)\$', tex)):
                raise ValueError('ambiguous_documenter_math')
            identity = attrs.get('id', 'qcl-math-' + str(len(records)))
            if 'id' not in attrs:
                if identity in ids:
                    raise ValueError('math_id_collision')
                attrs['id'] = identity
                ids.add(identity)
                node.attrs, node.changed = list(attrs.items()), True
            records.append({'page': page, 'selector': '#' + identity, 'tex': tex,
                            'tex_sha256': sha(tex.encode()), 'display': display})
        for child in node.children:
            visit(child)
    visit(tree.root)
    return assembly._serialize(tree.root).encode(), records


class Pipeline:
    def __init__(self, inputs, work):
        self.inputs, self.work = inputs, work
        self.start = time.monotonic()
        self.log_bytes = 0
        self.steps = []

    def run(self, argv, env, label, *, timeout=1800):
        """Drain both pipes with combined bound; no shell or buffered fallback."""
        remaining = min(timeout, 1800 - (time.monotonic() - self.start))
        if remaining <= 0:
            raise TimeoutError('producer_deadline')
        before = time.monotonic()
        output = bytearray()
        counts = {"stdout": 0, "stderr": 0}
        usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
        child = subprocess.Popen(argv, env=env, cwd=self.work, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        selector = selectors.DefaultSelector()
        selector.register(child.stdout, selectors.EVENT_READ, sys.stdout.buffer)
        selector.register(child.stderr, selectors.EVENT_READ, sys.stderr.buffer)
        try:
            while selector.get_map():
                if time.monotonic() - before > remaining:
                    raise TimeoutError('producer_deadline: ' + label)
                for key, _ in selector.select(timeout=min(0.2, remaining)):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    counts["stdout" if key.fileobj is child.stdout else "stderr"] += len(chunk)
                    self.log_bytes += len(chunk)
                    if self.log_bytes > MAX_LOG:
                        raise ValueError('combined_log_limit')
                    key.data.write(chunk)
                    key.data.flush()
                    if key.fileobj is child.stdout:
                        output.extend(chunk)
            code = child.wait(timeout=max(0.01, remaining - (time.monotonic() - before)))
            usage = resource.getrusage(resource.RUSAGE_CHILDREN)
            self.steps.append({'step': label, 'argv': argv, 'exit_code': code,
                'wall_seconds': time.monotonic() - before, 'stream_bytes': counts,
                'child_user_seconds': usage.ru_utime - usage_before.ru_utime,
                'child_system_seconds': usage.ru_stime - usage_before.ru_stime,
                'completed_children_maxrss_kib': usage.ru_maxrss,
                'step_peak_memory': None, 'step_peak_memory_status': 'not_measured'})
            if code:
                raise ValueError('render_process_failed: ' + label)
            return bytes(output)
        finally:
            selector.close()
            if child.poll() is None:
                child.kill()
                child.wait()
            child.stdout.close()
            child.stderr.close()


def source_tree(root, relative):
    path = root / relative
    if path.is_symlink() or not path.is_dir():
        raise ValueError('missing_source_graph: ' + relative)
    files = {}
    total = 0
    for item in sorted(path.rglob('*')):
        if item.is_symlink():
            raise ValueError('source_symlink')
        if item.is_file():
            key = item.relative_to(path).as_posix()
            data = read_file(item)
            total += len(data)
            if len(files) >= 10000 or total > MAX_PUBLIC:
                raise ValueError('source_tree_limit')
            files[key] = data
    return files


def put_tree(root, files):
    root.mkdir(parents=True, exist_ok=False)
    for name, data in sorted(files.items()):
        # Same portable path grammar as the final payload.
        if posixpath.normpath(name) != name or name.startswith('/') or any(p.startswith('.') for p in name.split('/')):
            raise ValueError('unsafe_output_path')
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(data)


def validate_tool(name, tool):
    fields(tool, ('store_path', 'executable', 'deriver', 'nar_hash', 'version'))
    base = store_path(tool['store_path'])
    executable = store_path(tool['executable'])
    # Metadata only: an absent physical .drv is not an output dependency.
    deriver = tool['deriver']
    if deriver is not None and (not isinstance(deriver, str) or
            not re.fullmatch(r'/nix/store/[0-9a-df-np-sv-z]{32}-[^/\\\x00-\x1f\x7f]+\.drv', deriver)):
        raise ValueError('tool_deriver: ' + name)
    nar_hash = tool['nar_hash']
    if not isinstance(nar_hash, str) or not re.fullmatch(r'sha256:[0123456789abcdfghijklmnpqrsvwxyz]{52}', nar_hash):
        raise ValueError('tool_nar_hash: ' + name)
    version = tool['version']
    if (base.parent != Path('/nix/store') or executable == base or
            not executable.is_relative_to(base) or executable.resolve() != executable or
            not executable.is_file() or not os.access(executable, os.X_OK) or
            not isinstance(version, str) or not version.strip() or len(version) > 256):
        raise ValueError('tool_identity: ' + name)


def validate_inputs(inputs):
    fields(inputs, ('source_root', 'source_graph', 'plan', 'project', 'manifest',
                    'prepared_depot', 'assets_lock', 'asset_inputs', 'review_inputs', 'tools'))
    root = store_path(inputs['source_root'])
    for name in ('source_graph', 'plan', 'project', 'manifest', 'assets_lock', 'asset_inputs', 'review_inputs'):
        record(inputs[name], 2 * 1024 * 1024)
    for name, filename in (('project', 'Project.toml'), ('manifest', 'Manifest.toml')):
        if Path(inputs[name]['path']) != root / 'julia' / filename:
            raise ValueError('project_source_identity')
    if Path(inputs['assets_lock']['path']) != root / 'ops/docs/assets.lock.json':
        raise ValueError('asset_lock_source_identity')
    if Path(inputs['plan']['path']) != root / 'ops/docs/pilot-plan.json':
        raise ValueError('plan_source_identity')
    fields(inputs['prepared_depot'], ('store_path', 'metadata'))
    store_path(inputs['prepared_depot']['store_path'])
    # Opaque truthful snapshot metadata is retained, never re-labelled as a new
    # root's producer receipt. Its original bytes/hash remain part of this input.
    record(inputs['prepared_depot']['metadata'], 2 * 1024 * 1024)
    fields(inputs['tools'], ('python', 'node', 'julia', 'git'))
    for name, tool in inputs['tools'].items():
        validate_tool(name, tool)
    assets = decode_json(record(inputs['asset_inputs'], 2 * 1024 * 1024))
    if not isinstance(assets, dict) or len(assets) > 10000:
        raise ValueError('asset_inputs_shape')
    data, total = {}, 0
    for key, path in assets.items():
        if not isinstance(key, str) or posixpath.normpath(key) != key or key.startswith('/') or any(x in ('.', '..') for x in key.split('/')):
            raise ValueError('asset_inputs_shape')
        # Distribution caps belong to runtime adapter too; archive bytes may be
        # larger than one public file but remain finite and never extracted here.
        data[key] = read_file(store_path(path), MAX_PUBLIC)
        total += len(data[key])
        if total > 256 * 1024 * 1024:
            raise ValueError('asset_input_total_limit')
    return root, data


def detached_review(root, graph, review):
    fields(review, ('sources', 'public_reviews', 'input_allowlist', 'output_allowlist', 'selector_allowlist'))
    sources = {}
    revisions = {r['path']: r['revision'] for r in graph['components']}
    revisions['root'] = graph['revision']
    for row in review['sources']:
        fields(row, ('component', 'revision', 'path', 'file'))
        component, path = row['component'], row['path']
        if component not in revisions or row['revision'] != revisions[component]:
            raise ValueError('review_source_revision')
        if not isinstance(path, str) or posixpath.normpath(path) != path or path.startswith('/') or any(p in ('.', '..') for p in path.split('/')):
            raise ValueError('review_source_path')
        expected = root / ('' if component == 'root' else component) / path
        data = record(row['file'])
        if data != read_file(expected) or (component, path) in sources:
            raise ValueError('review_source_identity')
        sources[(component, path)] = {'revision': row['revision'], 'bytes': data}
    reviews = []
    for row in review['public_reviews']:
        fields(row, ('source', 'recipe', 'receipt'))
        raw = record(row['receipt'], 2 * 1024 * 1024)
        if not raw:
            raise ValueError('empty_public_review')
        reviews.append({'source': row['source'], 'recipe': row['recipe'],
                        'receipt': {'bytes': raw, 'sha256': sha(raw)}})
    def tuples(rows, length):
        if not isinstance(rows, list) or any(not isinstance(r, list) or len(r) != length for r in rows):
            raise ValueError('review_allowlist_shape')
        return tuple(tuple(r) for r in rows)
    return {'selection': {'sources': graph}, 'sources': sources,
            'input_allowlist': tuples(review['input_allowlist'], 2),
            'selector_allowlist': tuples(review['selector_allowlist'], 4),
            'output_allowlist': tuple(review['output_allowlist']),
            'metadata': {}, 'public_reviews': tuple(reviews)}


def reference(retained, component, path):
    row = retained['sources'][(component, path)]
    return {'component': component, 'revision': row['revision'], 'path': path,
            'selector': {'kind': 'file', 'value': ''}, 'sha256': sha(row['bytes'])}


def coverage_for(assembly, retained, payload):
    rows = []
    for identity, (_, _, sources, urls) in assembly.PRIMARY.items():
        refs = []
        for full in sources:
            component = next((c for _, c in OWNERS if c != 'root' and full.startswith(c + '/')), 'root')
            path = full if component == 'root' else full[len(component) + 1:]
            refs.append(reference(retained, component, path))
        paths = {url.split('#')[0] for url in urls}
        # Include additional required anchors in the exact primary page(s).
        pages = []
        for path in sorted(paths):
            parser = assembly._PayloadHTML(path)
            parser.feed(payload[path].decode())
            parser.close()
            pages.append({'path': path, 'anchors': sorted(parser.ids & assembly.ANCHORS)})
        rows.append({'id': identity, 'sources': refs, 'pages': pages})
    return rows


def source_media_bytes(assembly, root, retained, path, raw):
    """Pre-admission equality: renderer output, actual S and detached source."""
    if path not in assembly.PUBLIC_SOURCE_MEDIA:
        raise ValueError('unreviewed_source_media_path: ' + path)
    component = 'components/QCLNEGF.jl'
    source = 'docs/src/' + path.removeprefix('core/')
    row = retained['sources'].get((component, source))
    if row is None:
        raise FileNotFoundError('missing media source: ' + source)
    if raw != row['bytes'] or raw != read_file(root / component / source):
        raise ValueError('source_media_identity: ' + path)
    return raw


def bind_source_media(assembly, evidence, retained, document):
    """Final authority uses the real retained candidate, never a preflight bundle."""
    paths = {row['path'] for row in document['files']} & assembly.PUBLIC_SOURCE_MEDIA
    if not paths:
        return  # Historical small media-free engineering fixtures stay valid.
    if paths != assembly.PUBLIC_SOURCE_MEDIA:
        raise FileNotFoundError('incomplete reviewed media payload')
    for path in sorted(paths):
        component = 'components/QCLNEGF.jl'
        source = 'docs/src/' + path.removeprefix('core/')
        if (component, source) not in retained['sources']:
            raise FileNotFoundError('missing media source: ' + source)
        data = evidence.source(reference(retained, component, source))
        item = retained['payload'].get(path)
        if not isinstance(item, dict) or item.get('kind') != 'file' or item.get('bytes') != data:
            raise ValueError('source_media_payload_mismatch: ' + path)


def owning_callbacks(root, graph, retained, payload):
    contracts_src = root / 'components/qcl-negf-contracts/src'
    # Exact source priority before importing owning C1/C2; no installed fallback.
    sys.path.insert(0, str(contracts_src))
    import qcl_negf_contracts as contracts
    from qcl_negf_contracts import model_help
    from qcl_negf_contracts.messages import ContractError
    if not Path(contracts.__file__).resolve().is_relative_to(contracts_src):
        raise ValueError('contracts_import_identity')
    import yaml
    import jsonschema
    if not getattr(yaml, '__version__', None) or not getattr(jsonschema, '__file__', None):
        raise ValueError('python_dependency_identity')
    validator = contracts.schema_validator('model-help.schema.json')
    assembly = module('_qcl_bind_media_assembly', Path(__file__).with_name('assemble.py'))
    retained['payload'] = {path: {'kind': 'file', 'bytes': data} for path, data in payload.items()}
    def bindings(document, *, coverage):
        # AS1 already constructed the exact candidate bytes; retaining that one
        # serialization binds C2 to the candidate, not a fabricated review. All
        # source/recipe public-review receipts above remain independent inputs.
        blob = encode(document)
        retained['bundle'] = {'bytes': blob, 'sha256': sha(blob)}
        try:
            model_help._validate_model_help_bindings(document, retained=retained)
            evidence = model_help._Evidence(retained)
            bind_source_media(assembly, evidence, retained, document)
            for row in coverage:
                for source in row['sources']:
                    evidence.source(source)
        except model_help._MissingProof as error:
            raise FileNotFoundError('missing owning retained proof') from error
        except ContractError as error:
            if isinstance(error.__cause__, model_help._MissingProof):
                raise FileNotFoundError('missing owning retained proof') from error
            raise
    return validator.validate, bindings


def math_insert(assembly, html, rendered, page):
    tree = assembly._Tree(html.decode())
    rows = {r['selector'][1:]: r for r in rendered if r['page'] == page}
    found = set()
    def visit(node):
        identity = node.attr().get('id')
        if identity in rows:
            found.add(identity)
            node.children = assembly._Tree(rows[identity]['html']).root.children
            return
        for child in node.children:
            visit(child)
    visit(tree.root)
    if found != set(rows):
        raise ValueError('rendered_math_mapping_mismatch')
    return assembly._serialize(tree.root).encode()


def localize_head(assembly, raw, page, locked, resources, requirejs):
    """Exact Documenter1.17 RequireJS src/data-main head loading shape."""
    tree = assembly._Tree(raw.decode())
    context = runtime_context(page)
    count = 0
    owner = page.split('/')[0]
    expected_main = posixpath.relpath(owner + '/assets/documenter.js', posixpath.dirname(page))
    def visit(node):
        nonlocal count
        attrs = node.attr()
        if node.tag == 'script':
            source = attrs.get('src', '')
            loader = source in resources and resources[source] == requirejs
            if 'data-main' in attrs or loader:
                if not loader or attrs.get('data-main') != expected_main or requirejs not in locked:
                    raise ValueError('documenter_requirejs_data_main_shape')
                count += 1
                attrs['data-main'] = posixpath.relpath(context['destination'], posixpath.dirname(page))
                node.attrs, node.changed = list(attrs.items()), True
            elif posixpath.basename(source) == 'documenter.js':
                raise ValueError('documenter_requirejs_data_main_shape')
        if node.tag == 'link' and posixpath.basename(attrs.get('href', '')) == 'qcl-fixed-light.css':
            attrs['href'] = posixpath.relpath('assets/runtime/qcl-fixed-light.css', posixpath.dirname(page))
            node.attrs, node.changed = list(attrs.items()), True
        if node.tag == 'link' and 'docs-theme-link' in attrs.get('class', '').split() and attrs.get('data-theme-name') == 'documenter-light':
            attrs['href'] = posixpath.relpath(next(p for p in locked if p.endswith('/documenter-light.css')), posixpath.dirname(page))
            node.attrs, node.changed = list(attrs.items()), True
        for child in node.children:
            visit(child)
    visit(tree.root)
    if count != 1:
        raise ValueError('documenter_requirejs_data_main_cardinality')
    return assembly._serialize(tree.root).encode()


def produce(inputs, work, output):
    root, asset_inputs = validate_inputs(inputs)
    assembly = module('_qcl_produce_assemble', root / 'ops/docs/assemble.py')
    runtime = module('_qcl_produce_runtime', root / 'ops/docs/runtime-assets.py')
    plan = assembly.load_pilot_plan(inputs['plan']['path'])
    graph = decode_json(record(inputs['source_graph']))
    assembly.validate_source_binding(graph, graph)
    lock_bytes = record(inputs['assets_lock'])
    lock = runtime.load_lock()
    asset_inputs = runtime.extract_inputs(asset_inputs, lock)
    locked = runtime.verify_inputs(asset_inputs, lock)
    retained = detached_review(root, graph, decode_json(record(inputs['review_inputs'])))
    # Missing prepared Python dependencies fail before any Julia render.
    shape, bindings = owning_callbacks(root, graph, retained, {})
    pipeline = Pipeline(inputs, work)
    (work / 'raw').mkdir()
    (work / 'home').mkdir()
    (work / 'tmp').mkdir()
    (work / 'depot').mkdir()
    env = {'PATH': os.environ['PATH'], 'HOME': str(work / 'home'), 'TMPDIR': str(work / 'tmp'),
           'JULIA_PKG_OFFLINE': 'true', 'JULIA_LOAD_PATH': '@:@stdlib',
           'JULIA_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1',
           'MKL_NUM_THREADS': '1', 'JULIA_DEPOT_PATH': str(work / 'depot') + ':' + inputs['prepared_depot']['store_path'],
           'QCL_DOCS_PROFILE': 'pilot-v1', 'QCL_DOCS_ROOT': str(root), 'QCL_DOCS_ATTEMPT': str(work)}
    # Once, inside the same cap: actual Julia+Documenter import identity. The
    # three owning recipes repeat their own root/project guards independently.
    check = ('using Documenter; using TOML; VERSION == v"1.13.0" || error("Julia identity"); '
             'pkgversion(Documenter) == v"1.17.0" || error("Documenter identity"); '
             'string(Base.PkgId(Documenter).uuid) == "e30172f5-a6a5-5a46-863b-614d45cd2de4" || error("Documenter UUID"); '
             'startswith(realpath(pathof(Documenter)),ARGS[2]*"/") || error("Documenter depot"); '
             'm=TOML.parsefile(joinpath(ARGS[1],"julia","Manifest.toml")); '
             'd=only(m["deps"]["Documenter"]); '
             'd["git-tree-sha1"] == "56e9c37b5e7c3b4f080ab1da18d72d5c290e184a" || error("Documenter tree"); '
             'println("QCL_DOCS_IDENTITY Julia=",VERSION," Documenter=",pkgversion(Documenter))')
    julia = inputs['tools']['julia']['executable']
    pipeline.run([julia, '--startup-file=no', '--history-file=no', '--project=' + str(root / 'julia'),
                  '-e', check, str(root), inputs['prepared_depot']['store_path']], env, 'toolchain-identity')
    for owner, component in OWNERS:
        if owner == 'operator':
            recipe = root / 'docs/public/make.jl'
            # Exact versioned Julia string literal extraction, never evaluate it.
            match = re.search(r'^const QCL_DOCS_OPERATOR_INDEX = ("(?:[^"\\]|\\.)*")$', read_file(recipe).decode(), re.M)
            if match is None:
                raise ValueError('operator_index_literal')
            index = json.loads(match.group(1))
            if '$' in index or not index.endswith('\n'):
                raise ValueError('operator_index_literal')
            files = {'index.md': index.encode(),
                     'recovery.md': read_file(root / 'docs/public/operator-recovery.md'),
                     'capture-runtime-delivery.md': read_file(root / 'docs/capture-runtime-delivery.md'),
                     'solver-build-receipt.md': read_file(root / 'docs/solver-build-receipt.md')}
        else:
            recipe = root / component / 'docs/make.jl'
            files = source_tree(root, component + '/docs/src')
        for name, data in files.items():
            if name.endswith('.md'):
                assembly.validate_authored_source(data.decode())
        files['assets/qcl-fixed-light.css'] = assembly.FIXED_LIGHT
        files['assets/qcl-runtime.css'] = b'.qcl-search-small{font-size:smaller}.qcl-copy-fallback{position:fixed;opacity:0}\n'
        source = work / 'stage' / owner / 'src'
        put_tree(source, files)
        child_env = {**env, 'QCL_DOCS_SOURCE': str(source), 'QCL_DOCS_BUILD': str(work / 'raw' / owner)}
        pipeline.run([julia, '--startup-file=no', '--history-file=no', '--project=' + str(root / 'julia'),
                      str(recipe)], child_env, owner)
    payload, retained_assets, pages, records, contexts = dict(locked), {}, {}, [], {}
    snippets = {name: asset_inputs['documenter/assets/html/js/' + name] for name in runtime.SNIPPETS}
    remote_map = lock['resource_map']
    for owner, _ in OWNERS:
        for name, raw in source_tree(work, 'raw/' + owner).items():
            page = owner + '/' + name
            if name.endswith('.html'):
                bridged, mapping = bridge_math(raw, page)
                context = runtime_context(page)
                contexts[context['destination']] = context
                generated = runtime.build_runtime(snippets, worker_url=context['worker_url'], asset_prefix=context['asset_prefix'])
                payload[context['destination']] = generated.pop('assets/documenter.js')
                payload.update(generated)
                # Pinned local script override is per page depth; Documenter raw
                # runtime stays diagnostic, never a served executable.
                bridged = localize_head(assembly, bridged, page, locked, remote_map,
                    lock['runtime_dependencies']['requirejs'])
                transformed = assembly.transform_page(bridged, page=page, binding=assembly.BINDING,
                    expected_sha256=sha(bridged), math_mapping=mapping, resource_map=remote_map)
                pages[page] = transformed['html']
                records.extend(mapping)
                for path, data in transformed['generated_files'].items():
                    payload[path] = data
                    retained_assets[path] = data
                (work / ('mapping-' + sha(page.encode()) + '.json')).write_bytes(encode({'page': page, 'raw_sha256': sha(raw), 'bridged_sha256': sha(bridged), 'records': mapping, 'operations': transformed['operations']}))
            elif not name.startswith('assets/') or name in ('search_index.js', 'assets/search_index.js'):
                # Search index is data authored by the pinned renderer. Images
                # are retained below; Documenter's bundled JS/CSS are replaced.
                if name.endswith(('.js', '.json')) and name not in ('search_index.js', 'assets/search_index.js'):
                    raise ValueError('unexpected_documenter_payload: ' + name)
                payload[page] = raw
                retained_assets[page] = raw
            elif (owner, name) == ('core', 'assets/physics/data/basis_metrics.csv'):
                payload[page] = source_media_bytes(assembly, root, retained, page, raw)
                retained_assets[page] = raw
            elif PurePosixPath(name).suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico'):
                if page in assembly.PUBLIC_SOURCE_MEDIA:
                    source_media_bytes(assembly, root, retained, page, raw)
                payload[page] = raw
                retained_assets[page] = raw
    # Add runtime/fixed-light and KaTeX styles to EVERY page, with exact ordered
    # context consumed below. Locked fonts CSS is already linked via resource_map.
    css = sorted(path for path in payload if path.endswith('.css'))
    for page, html in list(pages.items()):
        links = ''.join('<link rel="stylesheet" href="' + escape(posixpath.relpath(path, posixpath.dirname(page)), quote=True) + '">' for path in css)
        if html.count(b'</head>') != 1:
            raise ValueError('documenter_head_shape')
        pages[page] = html.replace(b'</head>', links.encode() + b'</head>')
    sheets = [{'path': path, 'text': payload[path].decode(), 'sha256': sha(payload[path])} for path in css]
    katex = next(row for row in lock['files'] if row['source_path'].endswith('/katex.mjs'))
    # Build-only KaTeX ESM may live inside an archive; materialize its verified
    # bytes into the private build directory, never serve the executable module.
    module_bytes = asset_inputs[katex['source_path']]
    module_path = work / 'katex.mjs'
    module_path.write_bytes(module_bytes)
    math_input = {'modulePath': str(module_path), 'moduleSha256': katex['sha256'], 'version': '0.16.8',
                  'stylesheets': sheets, 'completeStylesheets': sheets}
    packet = work / 'math-input.json'
    packet.write_bytes(encode({'records': records, 'inputs': math_input}))
    result_path = work / 'math-output.json'
    # Fixed code imports only the owning renderer, not commands from input JSON.
    js = ('import {readFileSync,writeFileSync} from "node:fs"; '
          'import {renderMathBatch} from ' + json.dumps((root / 'ops/docs/math-render.mjs').as_uri()) + '; '
          'const p=JSON.parse(readFileSync(process.argv[1],"utf8")); '
          'writeFileSync(process.argv[2],JSON.stringify(await renderMathBatch(p.records,p.inputs)));')
    pipeline.run([inputs['tools']['node']['executable'], '--input-type=module', '-e', js,
                  str(packet), str(result_path)], env, 'math', timeout=60)
    math = decode_json(read_file(result_path, 40 * 1024 * 1024))
    if [{k: r[k] for k in ('page','selector','tex','tex_sha256','display')} for r in math['records']] != records:
        raise ValueError('rendered_math_mapping_mismatch')
    payload['assets/qcl-math.css'] = math['css'].encode()
    retained_assets['assets/qcl-math.css'] = payload['assets/qcl-math.css']
    for page, html in pages.items():
        html = math_insert(assembly, html, math['records'], page)
        link = '<link rel="stylesheet" href="' + posixpath.relpath('assets/qcl-math.css', posixpath.dirname(page)) + '">'
        payload[page] = html.replace(b'</head>', link.encode() + b'</head>')
    payload['index.html'] = ('<!DOCTYPE html><html><head><meta charset="utf-8"><title>QCL NEGF docs</title></head><body><main>'
        '<h1>Документация QCL NEGF</h1><a href="core/theory/09_scba.html#researcher-scba-route">Исследователь</a> '
        '<a href="runner/api/public.html#reader-api-routes">Разработчик</a> '
        '<a href="operator/recovery.html#operator-recovery">Оператор</a></main></body></html>').encode()
    if sum(map(len, payload.values())) > MAX_PUBLIC:
        raise ValueError('public_64MiB_limit')
    asset_inputs['runtime-contexts.json'] = encode(list(contexts.values()))
    def assets(lock_raw, source_inputs, *, payload):
        # This full owning render must carry every reviewed media file. The
        # generic bindings adapter also serves historical media-free fixtures.
        if not assembly.PUBLIC_SOURCE_MEDIA.issubset(payload):
            raise FileNotFoundError('incomplete reviewed media payload')
        verified = runtime.validate_assets(lock_raw, source_inputs, payload=payload)
        for path, data in retained_assets.items():
            if path in assembly.PUBLIC_SOURCE_MEDIA:
                source_media_bytes(assembly, root, retained, path, data)
            if path in verified and verified[path] != data or payload.get(path) != data:
                raise ValueError('retained_asset_mismatch')
            verified[path] = data
        return verified
    retained['payload'] = {path: {'kind': 'file', 'bytes': data} for path, data in payload.items()}
    recipes = [reference(retained, c, ('docs/public/make.jl' if c == 'root' else 'docs/make.jl')) for _, c in OWNERS]
    generator = {'name':'Documenter', 'version':'1.17.0', 'uuid':'e30172f5-a6a5-5a46-863b-614d45cd2de4',
        'git_tree_sha1': assembly.BINDING['documenter_tree_sha1'], 'julia_version':'1.13.0',
        'project_sha256':inputs['project']['sha256'], 'manifest_sha256':inputs['manifest']['sha256'],
        'recipes':recipes, 'toolchain_lock':reference(retained,'root','julia/Manifest.toml')}
    result = assembly.finalize_bundle(plan=plan, before=graph, after=decode_json(record(inputs['source_graph'])),
        generator=generator, schema_ref=reference(retained,'components/qcl-negf-contracts','src/qcl_negf_contracts/schemas/model-help.schema.json'),
        coverage=coverage_for(assembly, retained, payload), fragments=[], aliases=[], payload=payload,
        asset_lock=lock_bytes, asset_inputs=asset_inputs, validate_shape=shape,
        validate_bindings=bindings, validate_assets=assets)
    if result['status'] != 'candidate':
        raise ValueError('assembly_blocked: ' + result['reason'])
    if sum(map(len, payload.values())) + len(result['bundle_bytes']) > MAX_PUBLIC:
        raise ValueError('public_64MiB_limit')
    output.mkdir(exist_ok=False)
    put_tree(output / 'public', payload)
    # The AS1 serialization is the final public write; no self hash.
    (output / 'public/bundle.json').write_bytes(result['bundle_bytes'])
    diagnostics = output / 'diagnostics'
    diagnostics.mkdir()
    shutil.copytree(work / 'raw', diagnostics / 'raw')
    for path in work.glob('mapping-*.json'):
        shutil.copyfile(path, diagnostics / path.name)
    shutil.copyfile(result_path, diagnostics / 'math-output.json')
    receipt = {'format':'qcl-negf.docs-producer-receipt.v1', 'status':'candidate',
        'source_graph_sha256':inputs['source_graph']['sha256'], 'inputs_sha256':sha(encode(inputs)),
        'bundle_sha256':result['bundle_sha256'], 'payload_files':len(payload),
        'payload_bytes':sum(map(len,payload.values())), 'elapsed_seconds':time.monotonic()-pipeline.start,
        'steps':pipeline.steps, 'acceptance':{'render':'completed','publication':'not_measured','science':'not_measured'}}
    (output / 'producer-receipt.json').write_bytes(encode(receipt))


def run_attempt(inputs, output, temporary_root):
    # An explicit workspace intentionally survives ALL failure paths. Nix
    # --keep-failed retains its build directory; no Python context manager
    # deletes the primary raw bytes before Nix can retain that directory.
    work = Path(tempfile.mkdtemp(prefix='qcl-docs-', dir=temporary_root))
    try:
        produce(inputs, work, output)
    except BaseException as error:
        failure = {'format': 'qcl-negf.docs-producer-failure.v1',
                   'workspace': str(work), 'raw_directory': str(work / 'raw'),
                   'error_type': type(error).__name__, 'error': str(error)[:4096],
                   'candidate_output_exists': output.exists(),
                   'publication': 'not_published'}
        try:
            (work / 'failure.json').write_bytes(encode(failure))
        except OSError as retention_error:
            sys.stderr.write('QCL_DOCS_FAILURE_METADATA_ERROR=' + type(retention_error).__name__ + '\n')
        sys.stderr.write('QCL_DOCS_FAILED_WORKSPACE=' + str(work) + '\n')
        raise
    return work


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', required=True)
    args = parser.parse_args()
    inputs = decode_json(read_file(store_path(args.inputs), 2 * 1024 * 1024))
    output = Path(os.environ['out'])
    run_attempt(inputs, output, os.environ.get('TMPDIR', '/tmp'))


if __name__ == '__main__':
    main()
