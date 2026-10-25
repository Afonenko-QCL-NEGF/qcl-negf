"""Focused fixtures; execute only in Root finite packet, no Nix/Julia.

The AMD control uses one bounded existing Node process and actual hash-bound
RequireJS code in a VM with inert timers and no resource loader/network.
"""
import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('docs_producer', ROOT / 'ops/docs/produce.py')
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)
class ProducerControls(unittest.TestCase):
    def test_documenter_math_bridge(self):
        raw = b'<p class="math-container">\\[x &lt; y\\]</p><span>$a+b$</span>'
        bridged, records = producer.bridge_math(raw, 'core/a.html')
        self.assertEqual([x['tex'] for x in records], ['x < y', 'a+b'])
        self.assertEqual([x['display'] for x in records], [True, False])
        self.assertIn(b'id="qcl-math-0"', bridged)
    def test_ambiguous_math_refused(self):
        for raw in (b'<p class="math-container">bad</p>', b'<span>$x</span>', b'<span>$<em>x</em>$</span>'):
            with self.assertRaises(ValueError): producer.bridge_math(raw, 'core/a.html')
    def test_json_refused(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}'):
            with self.assertRaises(ValueError): producer.decode_json(raw)
    def test_runtime_depth(self):
        self.assertEqual(producer.runtime_context('core/theory/a.html'), {'destination':'assets/runtime-depth-2.js','worker_url':'../../assets/search-worker.js','asset_prefix':'../../assets/vendor'})
    def test_store_path(self):
        for value in ('/tmp/a','/nix/store/a/../b','/nix/store/aaa'):
            with self.assertRaises(ValueError): producer.store_path(value)
    def test_failed_render_retains_workspace_without_public_candidate(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temporary_root:
            output = Path(temporary_root) / 'candidate'
            def failed_render(inputs, work, out):
                (work / 'raw/core').mkdir(parents=True)
                (work / 'raw/core/original.html').write_bytes(b'original failed render')
                (work / 'mapping-original.json').write_bytes(b'{"retained":true}')
                raise RuntimeError('injected render failure')
            with patch.object(producer, 'produce', failed_render):
                with self.assertRaisesRegex(RuntimeError, 'injected render failure'):
                    producer.run_attempt({}, output, temporary_root)
            workspaces = list(Path(temporary_root).glob('qcl-docs-*'))
            self.assertEqual(len(workspaces), 1)
            work = workspaces[0]
            self.assertEqual((work / 'raw/core/original.html').read_bytes(), b'original failed render')
            self.assertEqual((work / 'mapping-original.json').read_bytes(), b'{"retained":true}')
            failure = producer.decode_json((work / 'failure.json').read_bytes())
            self.assertEqual(failure['workspace'], str(work))
            self.assertFalse(failure['candidate_output_exists'])
            self.assertFalse(output.exists())

    def test_derivation(self):
        text=(ROOT/'nix/docs.nix').read_text()
        for value in ('builtins.derivation','builtins.storePath','allowSubstitutes = false','preferLocalBuild = true','"-B"','inputsFile'): self.assertIn(value,text)
        for value in ('fetchTarball','fetchGit','nixpkgs','fixedOutput'): self.assertNotIn(value,text)

class ToolIdentityControls(unittest.TestCase):
    """Actual Tool validator, no Nix queries, solver or physical deriver access."""
    def fixture(self, directory):
        from unittest.mock import patch
        base = Path('/nix/store/' + 'a' * 32 + '-tool')
        actual = Path(directory)
        executable = actual / 'bin/tool'
        executable.parent.mkdir()
        executable.write_text('inert executable fixture')
        executable.chmod(0o555)
        tool = dict(store_path=str(base), executable=str(base / 'bin/tool'),
                    deriver=str(base) + '.drv', version='1.0', nar_hash='sha256:' + 'a' * 52)
        calls = []
        def existing_store(value):
            calls.append(value)
            self.assertIn(value, (tool['store_path'], tool['executable']))
            return base if value == tool['store_path'] else base / 'bin/tool'
        # Substitute only immutable filesystem observations. The validator's
        # actual shape, metadata grammar, containment and mode checks still run.
        original_resolve = Path.resolve
        original_is_file = Path.is_file
        original_stat = Path.stat
        original_access = producer.os.access
        def stat(path, *args, **kwargs):
            self.assertNotEqual(str(path), str(base) + '.drv', 'physical deriver queried')
            return original_stat(path, *args, **kwargs)
        def resolve(path, *args, **kwargs):
            self.assertNotEqual(str(path), str(base) + '.drv', 'physical deriver resolved')
            if path == base / 'bin/tool': return path
            return original_resolve(path, *args, **kwargs)
        def is_file(path):
            if path == base / 'bin/tool': return executable.is_file()
            return original_is_file(path)
        def access(path, mode):
            if path == base / 'bin/tool': return original_access(executable, mode)
            return original_access(path, mode)
        return tool, calls, (
            patch.object(producer, 'store_path', existing_store),
            patch.object(Path, 'resolve', resolve),
            patch.object(Path, 'is_file', is_file),
            patch.object(Path, 'stat', stat),
            patch.object(producer.os, 'access', access),
        )

    def validate(self, tool, patches):
        from contextlib import ExitStack
        with ExitStack() as stack:
            for item in patches: stack.enter_context(item)
            producer.validate_tool('python', tool)

    def test_known_absent_and_null_deriver_are_metadata(self):
        import tempfile
        for deriver in ('known', None):
            with tempfile.TemporaryDirectory() as directory:
                tool, calls, patches = self.fixture(directory)
                known = tool['deriver']
                if deriver is None: tool['deriver'] = None
                self.validate(tool, patches)
                self.assertEqual(calls, [tool['store_path'], tool['executable']])
                self.assertNotIn(known, calls)

    def test_tool_shape_and_metadata_refuse_implicit_coercion(self):
        import tempfile
        bad = [('nar_hash', value) for value in (None, '', False,
            'sha256:' + 'a' * 51, 'sha256:' + 'e' * 52,
            'sha512:' + 'a' * 52, 'sha256:' + 'a' * 52 + '\n')]
        bad += [('deriver', value) for value in ('unknown-deriver', 'null', False,
            '', '/tmp/a.drv', '/nix/store/' + 'a' * 32 + '-a.drv/child',
            '/nix/store/' + 'a' * 32 + '-a.drv\n')]
        bad += [('version', value) for value in (False, None, '', ' ', 'v' * 257)]
        for key, value in bad:
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as directory:
                tool, _, patches = self.fixture(directory)
                tool[key] = value
                with self.assertRaises(ValueError): self.validate(tool, patches)
        with tempfile.TemporaryDirectory() as directory:
            tool, _, patches = self.fixture(directory)
            del tool['nar_hash']
            with self.assertRaises(ValueError): self.validate(tool, patches)

    def test_executable_checks_still_apply(self):
        import tempfile
        from unittest.mock import patch
        for attribute, value in (('access', False), ('is_file', False),
                                 ('resolve', Path('/tmp/escaped'))):
            with tempfile.TemporaryDirectory() as directory:
                tool, _, patches = self.fixture(directory)
                if attribute == 'access':
                    patches += (patch.object(producer.os, attribute, return_value=value),)
                else:
                    patches += (patch.object(Path, attribute, return_value=value),)
                with self.assertRaisesRegex(ValueError, 'tool_identity'):
                    self.validate(tool, patches)

    def test_deriver_nix_context_exception_is_narrow_source_guard(self):
        # Supplementary source guard; independent HIGH must assess Nix semantics.
        text = (ROOT / 'nix/docs.nix').read_text()
        self.assertIn('if key == "deriver" then item else bind item', text)
        self.assertIn('then builtins.storePath value', text)
        self.assertIn('else if builtins.isList value then map bind value', text)
        for field in ('source_root', 'tools.python.executable', 'asset_inputs.path', 'review_inputs.path'):
            self.assertIn('inputs.' + field, text)

class MediaCompatibilityControls(unittest.TestCase):
    """Exact public media in the historical full C1/C2 engineering fixture.

    This keeps the fixture's existing graph order/root epoch, and uses actual
    selected Core bytes/revision. Synthetic association receipts here are tests,
    never the independent production review or native acceptance.
    """
    @classmethod
    def setUpClass(cls):
        import os
        import sys
        snapshot = os.environ.get('QCL_DOCS_TEST_SNAPSHOT')
        if not snapshot:
            raise RuntimeError('Root must supply QCL_DOCS_TEST_SNAPSHOT')
        cls.snapshot = Path(snapshot)
        cls.fixture = sys.modules.get('producer_closure_frozen')
        if cls.fixture is None:
            cls.fixture = producer.module('producer_closure_frozen', cls.snapshot / 'tests/test_docs_bundle_closure.py')
        cls.assembly = producer.module('producer_media_assembly', ROOT / 'ops/docs/assemble.py')
        cls.component = 'components/QCLNEGF.jl'

    def case(self):
        kwargs, _, _, retained = self.fixture.frozen_case()
        revision = next(row['revision'] for row in kwargs['before']['components'] if row['path'] == self.component)
        # The actual Core primary files belong to precisely this historical Core.
        self.assertEqual(revision, '5b1cdd458eb07ff8c7c792642eda58d9061e1017')
        source_paths = ['docs/make.jl'] + ['docs/src/' + path.removeprefix('core/')
            for path in sorted(self.assembly.PUBLIC_SOURCE_MEDIA)]
        for path in source_paths:
            retained['sources'][(self.component, path)] = {
                'revision': revision, 'bytes': (self.snapshot / self.component / path).read_bytes()}
        recipe = producer.reference(retained, self.component, 'docs/make.jl')
        kwargs['generator']['recipes'].append(recipe)
        receipt = b'Synthetic media association fixture only; not independent production review'
        rows = tuple({'source': producer.reference(retained, self.component, path),
            'recipe': recipe, 'receipt': {'bytes': receipt, 'sha256': producer.sha(receipt)}} for path in source_paths)
        retained['public_reviews'] += rows
        retained['input_allowlist'] = tuple(retained['sources'])
        retained['selector_allowlist'] = tuple((component, path, 'file', '') for component, path in retained['sources'])
        for output in self.assembly.PUBLIC_SOURCE_MEDIA:
            source = 'docs/src/' + output.removeprefix('core/')
            kwargs['payload'][output] = retained['sources'][(self.component, source)]['bytes']
        retained['output_allowlist'] = tuple(kwargs['payload'])
        kwargs['validate_shape'], kwargs['validate_bindings'] = producer.owning_callbacks(
            self.snapshot, kwargs['before'], retained, kwargs['payload'])
        def assets(lock, inputs, *, payload):
            self.assertEqual(lock, b'{"assets":[],"engineering_fixture":true}')
            self.assertEqual(inputs, {})
            verified = {}
            for path, data in payload.items():
                if path in self.assembly.PUBLIC_SOURCE_MEDIA:
                    verified[path] = producer.source_media_bytes(self.assembly, self.snapshot, retained, path, data)
                elif not path.endswith('.html'):
                    raise ValueError('unreviewed fixture media')
            return verified
        kwargs['validate_assets'] = assets
        return kwargs, retained

    def test_actual_twelve_media_through_real_candidate_and_owning_c1_c2(self):
        kwargs, retained = self.case()
        result = self.assembly.finalize_bundle(**kwargs)
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(retained['bundle']['bytes'], result['bundle_bytes'])
        files = {row['path']: row for row in result['manifest']['files']}
        self.assertEqual(len(self.assembly.PUBLIC_SOURCE_MEDIA), 12)
        for path in self.assembly.PUBLIC_SOURCE_MEDIA:
            self.assertEqual(files[path]['sha256'], producer.sha(kwargs['payload'][path]))
            self.assertEqual(files[path]['media_type'], 'text/csv' if path.endswith('.csv') else 'image/svg+xml')

    def test_actual_bytes_survive_source_stage_raw_and_payload(self):
        import tempfile
        kwargs, retained = self.case()
        files = {path.removeprefix('core/'): data for path, data in kwargs['payload'].items()
                 if path in self.assembly.PUBLIC_SOURCE_MEDIA}
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            producer.put_tree(work / 'stage/core/src', files)
            producer.put_tree(work / 'raw/core', producer.source_tree(work, 'stage/core/src'))
            for name, raw in producer.source_tree(work, 'raw/core').items():
                path = 'core/' + name
                self.assertEqual(producer.source_media_bytes(self.assembly, self.snapshot, retained, path, raw),
                                 kwargs['payload'][path])

    def test_renderer_script_event_external_or_csv_modification_refused(self):
        changes = (b'<script>alert(1)</script>', b'<svg onload="alert(1)"></svg>',
                   b'<image href="https://example.invalid/image.png"/>')
        for extra in changes:
            kwargs, _ = self.case()
            path = 'core/assets/physics/band_dispersion.svg'
            kwargs['payload'][path] += extra
            with self.assertRaisesRegex(ValueError, 'source_media_identity'):
                self.assembly.finalize_bundle(**kwargs)
        kwargs, _ = self.case()
        kwargs['payload'][self.assembly.PUBLIC_SOURCE_CSV] = b'method,state\n=SUM(1),1\n'
        with self.assertRaisesRegex(ValueError, 'source_media_identity'):
            self.assembly.finalize_bundle(**kwargs)

    def test_final_binding_rejects_arbitrary_trusted_map_bytes(self):
        # Bypasses the pre-admission source adapter deliberately: real final
        # evidence.source still prevents a forged map granting new authority.
        for extra in (b'<script>alert(1)</script>', b'<image href="https://example.invalid/x"/>'):
            kwargs, retained = self.case()
            path = 'core/assets/physics/band_dispersion.svg'
            kwargs['payload'][path] += extra
            retained['payload'][path]['bytes'] = kwargs['payload'][path]
            kwargs['validate_assets'] = lambda *args, payload, **kw: {
                path: data for path, data in payload.items() if not path.endswith('.html')}
            with self.assertRaisesRegex(ValueError, 'source_media_payload_mismatch'):
                self.assembly.finalize_bundle(**kwargs)

    def test_changed_source_and_raw_cannot_reuse_old_review(self):
        kwargs, retained = self.case()
        path = 'core/assets/physics/band_dispersion.svg'
        source = 'docs/src/' + path.removeprefix('core/')
        changed = kwargs['payload'][path] + b'<script>alert(1)</script>'
        kwargs['payload'][path] = changed
        retained['payload'][path]['bytes'] = changed
        retained['sources'][(self.component, source)]['bytes'] = changed
        kwargs['validate_assets'] = lambda *args, payload, **kw: {
            name: data for name, data in payload.items() if not name.endswith('.html')}
        self.assertEqual(self.assembly.finalize_bundle(**kwargs)['status'], 'blocked')

    def test_missing_media_review_or_source_blocks_real_candidate(self):
        for missing in ('review', 'source', 'final_source'):
            kwargs, retained = self.case()
            source = 'docs/src/assets/physics/band_dispersion.svg'
            if missing == 'review':
                retained['public_reviews'] = tuple(row for row in retained['public_reviews']
                    if not (row['source']['component'] == self.component and row['source']['path'] == source))
            else:
                del retained['sources'][(self.component, source)]
                if missing == 'final_source':
                    kwargs['validate_assets'] = lambda *args, payload, **kw: {
                        path: data for path, data in payload.items() if not path.endswith('.html')}
            self.assertEqual(self.assembly.finalize_bundle(**kwargs)['status'], 'blocked')

    def test_missing_input_selector_or_output_allowlist_refused(self):
        for missing in ('input', 'selector', 'output'):
            kwargs, retained = self.case()
            source = 'docs/src/assets/physics/band_dispersion.svg'
            if missing == 'input':
                retained['input_allowlist'] = tuple(key for key in retained['input_allowlist'] if key != (self.component, source))
            elif missing == 'selector':
                retained['selector_allowlist'] = tuple(key for key in retained['selector_allowlist'] if key != (self.component, source, 'file', ''))
            else:
                retained['output_allowlist'] = tuple(path for path in retained['output_allowlist'] if path != 'core/assets/physics/band_dispersion.svg')
            with self.assertRaises(ValueError): self.assembly.finalize_bundle(**kwargs)

    def test_old_association_or_missing_payload_refused(self):
        kwargs, retained = self.case()
        source = 'docs/src/assets/physics/band_dispersion.svg'
        for row in retained['public_reviews']:
            if row['source']['component'] == self.component and row['source']['path'] == source:
                row['source']['sha256'] = 'a' * 64
        self.assertEqual(self.assembly.finalize_bundle(**kwargs)['status'], 'blocked')
        for path in ('core/assets/physics/band_dispersion.svg', self.assembly.PUBLIC_SOURCE_CSV):
            kwargs, retained = self.case()
            del kwargs['payload'][path]
            retained['payload'].pop(path)
            self.assertEqual(self.assembly.finalize_bundle(**kwargs)['status'], 'blocked')

    def test_actual_source_retained_and_raw_must_all_agree(self):
        import tempfile
        kwargs, retained = self.case()
        path = 'core/assets/physics/band_dispersion.svg'
        source = 'docs/src/' + path.removeprefix('core/')
        raw = kwargs['payload'][path]
        retained['sources'][(self.component, source)]['bytes'] += b'changed'
        with self.assertRaisesRegex(ValueError, 'source_media_identity'):
            producer.source_media_bytes(self.assembly, self.snapshot, retained, path, raw)
        retained['sources'][(self.component, source)]['bytes'] = raw
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / self.component / source
            target.parent.mkdir(parents=True)
            target.write_bytes(raw + b'changed actual source')
            with self.assertRaisesRegex(ValueError, 'source_media_identity'):
                producer.source_media_bytes(self.assembly, root, retained, path, raw)

    def test_exception_finite_paths_and_exact_evidence_only(self):
        kwargs, _ = self.case()
        svg = kwargs['payload']['core/assets/physics/band_dispersion.svg']
        csv = kwargs['payload'][self.assembly.PUBLIC_SOURCE_CSV]
        for path, data in (('core/assets/new.svg', svg), ('core/assets/physics/data/other.csv', csv),
                           ('runner/assets/physics/data/basis_metrics.csv', csv)):
            with self.assertRaises(ValueError):
                self.assembly.validate_payload({path: data}, verified_assets={path: data})
        with self.assertRaises(ValueError):
            self.assembly.validate_payload({self.assembly.PUBLIC_SOURCE_CSV: csv})
        with self.assertRaises(ValueError):
            self.assembly.validate_payload({'core/assets/physics/band_dispersion.svg': svg})
        with self.assertRaisesRegex(ValueError, 'missing_anchor'):
            self.assembly.validate_payload({'index.html': b'<img src="core/assets/physics/band_dispersion.svg#id"/>',
                'core/assets/physics/band_dispersion.svg': svg},
                verified_assets={'core/assets/physics/band_dispersion.svg': svg})

    def test_authored_diagrams_keep_the_existing_strict_parser(self):
        from unittest.mock import patch
        for name in ('assets/scba_flow.svg', 'assets/diagrams/nested_solver.svg',
                     'assets/diagrams/production_parallelism.svg'):
            path = 'core/' + name
            data = (self.snapshot / self.component / 'docs/src' / name).read_bytes()
            self.assertNotIn(path, self.assembly.PUBLIC_SOURCE_MEDIA)
            with patch.object(self.assembly, '_PayloadHTML', wraps=self.assembly._PayloadHTML) as parser:
                self.assembly.validate_payload({path: data})
                parser.assert_called_once_with(path)

    def test_svg_xml_space_wrong_values_and_nodes_refused(self):
        path = 'core/assets/diagrams/nested_solver.svg'
        raw = (self.snapshot / self.component / 'docs/src/assets/diagrams/nested_solver.svg').read_bytes()
        self.assertIn(b'xml:space="preserve"', raw)
        for attribute in (b'xml:space="default"', b'xml:space="Preserve"', b'xml:space=""',
                          b'xml:space', b'xml:space="preserve "'):
            changed = raw.replace(b'xml:space="preserve"', attribute, 1)
            with self.assertRaisesRegex(ValueError, 'SVG xml:space'):
                self.assembly.validate_payload({path: changed})
        for name, node in (('assets/diagrams/nested_solver.svg', b'<g '),
                           ('assets/scba_flow.svg', b'<marker ')):
            original = (self.snapshot / self.component / 'docs/src' / name).read_bytes()
            self.assertIn(node, original)
            changed = original.replace(node, node + b'xml:space="preserve" ', 1)
            with self.assertRaisesRegex(ValueError, 'SVG xml:space'):
                self.assembly.validate_payload({'core/' + name: changed})

    def test_html_privacy_theme_symlink_and_caps_still_strict(self):
        for data in (b'<p style="color:red">x</p>', b'<svg onload="alert(1)"></svg>',
                     b'<script>alert(1)</script>'):
            with self.assertRaises(ValueError):
                self.assembly.validate_payload({'index.html': data}, verified_assets={'index.html': data})
        path = 'core/assets/physics/band_dispersion.svg'
        for media_path in (path, self.assembly.PUBLIC_SOURCE_CSV):
            for data in (b'/home/private/user', b'prefers-color-scheme', b'\xff'):
                with self.assertRaises(ValueError):
                    self.assembly.validate_payload({media_path: data}, verified_assets={media_path: data})
        with self.assertRaisesRegex(ValueError, 'public_allowlist'):
            self.assembly.validate_payload({}, symlinks=[path])
        with self.assertRaisesRegex(ValueError, 'payload_limit'):
            self.assembly.validate_payload({path: b'x' * (16 * 1024 * 1024 + 1)})

class ProducerClosureControls(unittest.TestCase):
    """Real owning C1+C2, small historical engineering render fixture only.

    Root supplies its initialized immutable read-only snapshot for Contracts;
    this worktree intentionally does not initialize or advance any gitlinks.
    """
    @classmethod
    def setUpClass(cls):
        import os
        import sys
        snapshot = os.environ.get('QCL_DOCS_TEST_SNAPSHOT')
        if snapshot is None:
            raise RuntimeError('Root must supply QCL_DOCS_TEST_SNAPSHOT for real C1+C2 fixtures')
        cls.snapshot = Path(snapshot)
        fixture_path = cls.snapshot / 'tests/test_docs_bundle_closure.py'
        cls.fixture = sys.modules.get('producer_closure_frozen')
        if cls.fixture is None:
            cls.fixture = producer.module('producer_closure_frozen', fixture_path)
        if Path(cls.fixture.__file__).resolve() != fixture_path.resolve():
            raise RuntimeError('cached frozen fixture source identity')
        cls.assembly = producer.module('producer_current_assembly', ROOT / 'ops/docs/assemble.py')

    def case(self):
        kwargs, expected, blob, retained = self.fixture.frozen_case()
        kwargs['validate_shape'], kwargs['validate_bindings'] = producer.owning_callbacks(
            self.snapshot, kwargs['before'], retained, kwargs['payload'])
        return kwargs, retained

    def test_small_render_through_real_c1_c2(self):
        kwargs, _ = self.case()
        result = self.assembly.finalize_bundle(**kwargs)
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(result['manifest']['fragments'], [])
        self.assertEqual(len(kwargs['coverage']), 3)

    def test_missing_independent_review_blocks(self):
        kwargs, retained = self.case()
        retained['public_reviews'] = ()
        self.assertEqual(self.assembly.finalize_bundle(**kwargs)['status'], 'blocked')

    def test_source_identity_mismatch_refused(self):
        kwargs, retained = self.case()
        key = ('root', 'docs/public/make.jl')
        retained['sources'][key]['bytes'] += b'\n# changed\n'
        with self.assertRaises(ValueError):
            self.assembly.finalize_bundle(**kwargs)

    def test_exact_asset_byte_mismatch_refused(self):
        kwargs, _ = self.case()
        kwargs['validate_assets'] = lambda *a, **kw: {'assets/x.css': b'x'}
        with self.assertRaises(ValueError):
            self.assembly.finalize_bundle(**kwargs)

    def test_quoted_glyph_only_for_verified_sheet(self):
        raw = b'.fa:before{content:"\\f000"}'
        with self.assertRaises(ValueError):
            self.assembly._css_edges('assets/a.css', raw.decode())
        self.assertEqual(self.assembly._css_edges('assets/a.css', raw.decode(), verified_bytes=raw), [])
        escaped_url = b'a{background:u\\72l(https://invalid.example/x)}'
        with self.assertRaises(ValueError):
            self.assembly._css_edges('assets/a.css', escaped_url.decode(), verified_bytes=escaped_url)

    def test_actual_core_svg_bytes_and_local_marker(self):
        raw = (self.snapshot / 'components/QCLNEGF.jl/docs/src/assets/scba_flow.svg').read_bytes()
        self.assertEqual(producer.sha(raw), 'b34fbd2868c4b3eca45948c430926771f277132b4c11477518ef90bb1b6e00e4')
        self.assembly.validate_payload({'core/assets/scba_flow.svg': raw})
        # Validation is read-only: neither geometry nor authored labels change.
        self.assertEqual(producer.sha(raw), 'b34fbd2868c4b3eca45948c430926771f277132b4c11477518ef90bb1b6e00e4')
        for changed in (
            raw.replace(b'url(#a)', b'url(https://example.invalid/a)'),
            raw.replace(b'url(#a)', b'url(data:image/svg+xml,a)'),
            raw.replace(b'url(#a)', b'url(javascript:alert(1))'),
            raw.replace(b'url(#a)', b'u\\72l(#a)'),
            raw.replace(b'url(#a)', b'url(#missing)'),
            raw.replace(b'<marker ', b'<marker onload="alert(1)" '),
            raw.replace(b'<text ', b'<foreignObject '),
            raw.replace(b'<text ', b'<script '),
        ):
            with self.assertRaises(ValueError):
                self.assembly.validate_payload({'core/assets/scba_flow.svg': changed})
        # A matching marker in a sibling SVG cannot satisfy this reference.
        with self.assertRaises(ValueError):
            self.assembly.validate_payload({'core/assets/x.svg':
                b'<svg><marker id="a"/></svg><svg><path marker-end="url(#a)"/></svg>'})

    def prepared_runtime(self):
        import os
        runtime = producer.module('producer_amd_runtime', ROOT / 'ops/docs/runtime-assets.py')
        snippets_root = Path(os.environ['DOC04_DOCUMENTER_ROOT'])
        snippets = {name: (snippets_root / 'assets/html/js' / name).read_bytes() for name in runtime.SNIPPETS}
        source_map = producer.decode_json(Path(os.environ['DOC04_ASSET_INPUTS_JSON']).read_bytes())
        loader = Path(source_map['responses/requirejs-min']).read_bytes()
        pin = next(entry for entry in runtime.load_lock()['files'] if entry['source_path'] == 'responses/requirejs-min')
        self.assertEqual(len(loader), pin['bytes'])
        self.assertEqual(producer.sha(loader), pin['sha256'])
        self.assertEqual(producer.sha(loader), 'd5f10f852b112a514a19f2b778eef5d2d1307878757f0a24539c051831cefaf8')
        return runtime, snippets, source_map, loader

    def test_actual_pinned_jquery_public_literal_and_private_negatives(self):
        runtime, _, source_map, _ = self.prepared_runtime()
        # Obtain real exact asset bytes from the complete owning lock verifier;
        # the positive never invents a byte map or empty vendor implementation.
        inputs = {name: Path(path).read_bytes() for name, path in source_map.items()}
        inputs = runtime.extract_inputs(inputs, runtime.load_lock())
        verified = runtime.verify_inputs(inputs, runtime.load_lock())
        destination = 'assets/vendor/jquery/3.7.0/jquery.min.js'
        source = 'vendor/jquery/package/dist/jquery.min.js'
        jquery = verified[destination]
        self.assertEqual(len(jquery), 87462)
        self.assertEqual(producer.sha(jquery), 'd8f9afbf492e4c139e9d2bcb9ba6ef7c14921eb509fb703bc7a3f911b774eff8')
        literal = b'{radio:!0,checkbox:!0,file:!0,password:!0,image:!0}'
        self.assertEqual(jquery.count(literal), 1)
        self.assertIsNotNone(self.assembly.PRIVATE.search(jquery.decode()))
        self.assembly.validate_payload(dict(verified), verified_assets=verified)
        self.assertEqual(verified[destination], jquery, 'public bytes must remain unchanged')
        # Exact public bytes alone cannot replace independent lock authority.
        with self.assertRaisesRegex(ValueError, 'private_content'):
            self.assembly.validate_payload({destination: jquery})
        changed = jquery.replace(b'password:!0', b'password:!1', 1)
        changed_inputs = {**inputs, source: changed}
        with self.assertRaisesRegex(ValueError, 'asset_hash_mismatch'):
            runtime.verify_inputs(changed_inputs, runtime.load_lock())
        with self.assertRaisesRegex(ValueError, 'asset_payload_mismatch'):
            self.assembly.validate_payload({**verified, destination: changed}, verified_assets=verified)
        # Even a deliberately forged caller map cannot apply the literal mask
        # to changed bytes; AS1's real adapter rejects it earlier by hash too.
        with self.assertRaisesRegex(ValueError, 'private_content'):
            self.assembly.validate_payload({destination: changed}, verified_assets={destination: changed})
        for private in (
            b'const value="/home/operator/private";',
            b'const value="/nix/store/private";',
            b'const value="AKIAABCDEFGHIJKLMNOP";',
            b'const value="-----BEGIN RSA PRIVATE KEY-----";',
            b'password="private-value";', b'access_token="private-value";',
            b'secret_key="private-value";',
        ):
            path = 'assets/vendor/unreviewed/private.js'
            with self.assertRaisesRegex(ValueError, 'private_content'):
                self.assembly.validate_payload({path: private})
            with self.assertRaisesRegex(ValueError, 'private_content'):
                self.assembly.validate_payload({path: private}, verified_assets={path: private})

    def test_actual_highlight_css_grammar_literal_preserves_theme_guards(self):
        runtime, _, source_map, _ = self.prepared_runtime()
        inputs = {name: Path(path).read_bytes() for name, path in source_map.items()}
        inputs = runtime.extract_inputs(inputs, runtime.load_lock())
        verified = runtime.verify_inputs(inputs, runtime.load_lock())
        path = 'assets/vendor/highlight/11.8.0/highlight.min.js'
        source = 'responses/highlight-browser'
        highlight = verified[path]
        self.assertEqual(len(highlight), 121107)
        self.assertEqual(producer.sha(highlight), '4499ff936d4fd562adca5a5cbe512dc19eb80942eee8618dafbcebc4f7974bdb')
        self.assertEqual(highlight.count(b'"pointer","prefers-color-scheme","prefers-contrast"'), 1)
        self.assertIsNotNone(self.assembly.THEME.search(highlight.decode()))
        # The subset retains authority from the actual complete lock verifier.
        self.assembly.validate_payload({path: highlight}, verified_assets={path: verified[path]})
        self.assertEqual(verified[path], highlight, 'grammar code bytes must remain unchanged')
        with self.assertRaisesRegex(ValueError, 'theme_alternative'):
            self.assembly.validate_payload({path: highlight})
        changed = highlight + b'\nwindow.matchMedia("(prefers-color-scheme: dark)");'
        with self.assertRaisesRegex(ValueError, 'asset_hash_mismatch'):
            runtime.verify_inputs({**inputs, source: changed}, runtime.load_lock())
        with self.assertRaisesRegex(ValueError, 'asset_payload_mismatch'):
            self.assembly.validate_payload({path: changed}, verified_assets={path: highlight})
        # Adversarial forged map cannot turn a changed active payload into the
        # pinned exception; AS1's real asset adapter would reject it earlier.
        with self.assertRaisesRegex(ValueError, 'theme_alternative'):
            self.assembly.validate_payload({path: changed}, verified_assets={path: changed})
        for active in (b'window.matchMedia("(prefers-color-scheme: dark)");',
                       b'document.body.classList.add("documenter-dark");',
                       b'const theme="catppuccin";', b'const rule="color-scheme:dark";'):
            generic = 'assets/vendor/unreviewed/theme.js'
            with self.assertRaisesRegex(ValueError, 'theme_alternative'):
                self.assembly.validate_payload({generic: active})
            with self.assertRaisesRegex(ValueError, 'theme_alternative'):
                self.assembly.validate_payload({generic: active}, verified_assets={generic: active})
        with self.assertRaisesRegex(ValueError, 'theme_alternative'):
            self.assembly.validate_payload({'assets/unreviewed.css': b'body{color-scheme:dark}'})

    def test_actual_pinned_requirejs_amd_resolution(self):
        import os
        import re
        import shutil
        import subprocess
        from urllib.parse import urljoin
        runtime, snippets, _, loader = self.prepared_runtime()
        cases = []
        dependencies = runtime.load_lock()['runtime_dependencies']
        for page in ('core/index.html', 'core/theory/09_scba.html', 'runner/api/public.html'):
            context = producer.runtime_context(page)
            generated = runtime.build_runtime(snippets, worker_url=context['worker_url'], asset_prefix=context['asset_prefix'])
            config = re.search(rb'^require\.config\((\{[^\n]+\})\);$', generated['assets/documenter.js'], re.M)
            self.assertIsNotNone(config, 'use the actual generated RequireJS config, not an empty require fixture')
            config = producer.decode_json(config.group(1))
            self.assertEqual(config['baseUrl'], '.')
            self.assertTrue(config['paths'])
            self.assertIn(('new Worker(' + __import__('json').dumps(context['worker_url']) + ')').encode(), generated['assets/documenter.js'])
            main = producer.posixpath.relpath(context['destination'], producer.posixpath.dirname(page))
            cases.append({'page': page, 'dataMain': main, 'config': config})
        # Actual pinned RequireJS browser startup consumes data-main. Its timers
        # remain queued/inert; the tiny DOM throws on every script/resource load.
        # Only config/nameToUrl is exercised, never third-party dependencies.
        script = r'''
const fs = require("node:fs");
const vm = require("node:vm");
const packet = JSON.parse(fs.readFileSync(0, "utf8"));
const results = [];
for (const item of packet.cases) {
  const noLoad = () => { throw Error("resource loading forbidden in AMD fixture"); };
  const head = {appendChild: noLoad, insertBefore: noLoad};
  const script = {parentNode: head, getAttribute: key => key === "data-main" ? item.dataMain : null};
  const document = {getElementsByTagName: tag => tag === "script" ? [script] : tag === "head" ? [head] : [],
    createElement: noLoad, createElementNS: noLoad};
  const timers = [];
  const context = vm.createContext({document, window: {document}, navigator: {platform: "Linux"},
    setTimeout: (callback, delay) => { timers.push({callback, delay}); return timers.length; }});
  vm.runInContext(packet.loader, context, {timeout: 1000});
  if (context.requirejs.version !== "2.3.6") throw Error("wrong RequireJS version");
  const api = context.requirejs;
  const inferredBaseUrl = api.s.contexts._.config.baseUrl;
  const broken = {...item.config};
  delete broken.baseUrl;
  api.config(broken);
  const before = Object.fromEntries(Object.keys(item.config.paths).map(name =>
    [name, api.s.contexts._.nameToUrl(name)]));
  api.config(item.config);
  const after = Object.fromEntries(Object.keys(item.config.paths).map(name =>
    [name, api.s.contexts._.nameToUrl(name)]));
  results.push({page: item.page, inferredBaseUrl, baseUrl: api.s.contexts._.config.baseUrl, before, after});
}
process.stdout.write(JSON.stringify(results));
'''
        node = os.environ.get('DOC04_NODE') or shutil.which('node')
        self.assertTrue(node, 'existing admitted Node executable required for AMD control')
        completed = subprocess.run([node, '-e', script],
            input=producer.encode({'loader': loader.decode(), 'cases': cases}),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        self.assertLess(len(completed.stdout) + len(completed.stderr), 65536)
        results = producer.decode_json(completed.stdout)
        self.assertEqual(len(results), len(cases))
        for case, observed in zip(cases, results):
            self.assertEqual(observed['inferredBaseUrl'], producer.posixpath.dirname(case['dataMain']) + '/')
            self.assertEqual(observed['baseUrl'], './')
            document_url = 'https://fixture.invalid/docs/' + case['page']
            for name, target in observed['after'].items():
                self.assertEqual(urljoin(document_url, target), 'https://fixture.invalid/docs/' + dependencies[name])
            worker_url = producer.runtime_context(case['page'])['worker_url']
            self.assertEqual(urljoin(document_url, worker_url), 'https://fixture.invalid/docs/assets/search-worker.js')
            if case['page'] == 'core/theory/09_scba.html':
                self.assertNotEqual(urljoin(document_url, observed['before']['jquery']),
                    'https://fixture.invalid/docs/' + dependencies['jquery'],
                    'negative control must reproduce data-main-derived baseUrl regression')

    def test_actual_requirejs_data_main_nested_page(self):
        page = 'core/theory/a.html'
        cdn = 'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'
        loader = 'assets/vendor/requirejs/2.3.6/require.min.js'
        light = 'assets/documenter-light.css'
        runtime_adapter, snippets, source_map, actual_loader = self.prepared_runtime()
        locked = {loader: actual_loader, light: b'a{color:#123}'}
        raw = ('<!doctype html><html><head>'
            '<link class="docs-theme-link" data-theme-name="documenter-light" href="../assets/themes/documenter-light.css">'
            '<script>documenterBaseURL=".."</script>'
            '<script src="' + cdn + '" data-main="../assets/documenter.js"></script>'
            '</head><body><h1>Fixture</h1></body></html>').encode()
        localized = producer.localize_head(self.assembly, raw, page, locked, {cdn: loader}, loader)
        self.assertIn(b'data-main="../../assets/runtime-depth-2.js"', localized)
        transformed = self.assembly.transform_page(localized, page=page,
            binding=self.assembly.BINDING, expected_sha256=producer.sha(localized),
            math_mapping=[], resource_map={cdn: loader})
        self.assertIn(b'src="../../assets/vendor/requirejs/2.3.6/require.min.js"', transformed['html'])
        generated = runtime_adapter.build_runtime(snippets, worker_url='../../assets/search-worker.js', asset_prefix='../../assets/vendor')
        runtime = generated.pop('assets/documenter.js')
        dependencies = runtime_adapter.load_lock()['runtime_dependencies']
        vendor = {entry['destination']: Path(source_map[entry['source_path']]).read_bytes()
            for entry in runtime_adapter.load_lock()['files'] if entry['destination'] in dependencies.values()}
        assets = {**vendor, **locked, **transformed['generated_files'], **generated,
            'assets/runtime-depth-2.js': runtime}
        payload = {**assets, page: transformed['html']}
        self.assembly.validate_payload(payload, verified_assets=assets)
        for changed in (
            raw.replace(b' data-main="../assets/documenter.js"', b''),
            raw.replace(b'../assets/documenter.js', b'../assets/wrong.js'),
            raw.replace(cdn.encode(), b'https://example.invalid/require.min.js'),
        ):
            with self.assertRaises(ValueError):
                producer.localize_head(self.assembly, changed, page, locked, {cdn: loader}, loader)
        for changed in (
            transformed['html'].replace(b' data-main="../../assets/runtime-depth-2.js"', b''),
            transformed['html'].replace(b'data-main="../../assets/runtime-depth-2.js"', b'data-main="../../assets/runtime-depth-1.js"'),
            transformed['html'].replace(loader.encode(), b'assets/vendor/wrong.js'),
        ):
            with self.assertRaises(ValueError):
                self.assembly.validate_payload({**payload, page: changed}, verified_assets=assets)
        missing_loader_authority = {key: value for key, value in assets.items() if key != loader}
        with self.assertRaises(ValueError):
            self.assembly.validate_payload(payload, verified_assets=missing_loader_authority)

    def test_runtime_depth_not_caller_flag(self):
        runtime = b'require([],function(){});new Worker("../assets/search-worker.js");'
        payload = {'index.html':b'<script src="assets/runtime-depth-1.js"></script>',
                   'assets/runtime-depth-1.js':runtime,'assets/search-worker.js':b''}
        with self.assertRaises(ValueError):
            self.assembly.validate_payload(payload)
        with self.assertRaises(ValueError):
            self.assembly.validate_payload(payload, verified_assets={'assets/runtime-depth-1.js':runtime})

if __name__ == '__main__':
    unittest.main()
