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
    def test_exact_raw_root_ancillary_selection_preserves_original_bytes(self):
        import tempfile
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            raw_root = work / 'raw/core'
            raw_root.mkdir(parents=True)
            originals = {
                '.documenter-siteinfo.json': b'{"timestamp":"original"}',
                'objects.inv': b'\x00raw inventory\xff',
                'index.html': b'<html></html>',
                'search_index.js': b'var index = [];',
                'nested/objects.inv': b'nested is public candidate',
                'nested/.documenter-siteinfo.json': b'nested is public candidate',
            }
            for name, data in originals.items():
                path = raw_root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            readback = producer.source_tree(work, 'raw/core')
            selected = producer._documenter_payload_candidates(readback)
            self.assertEqual(set(selected), set(originals) - {'.documenter-siteinfo.json', 'objects.inv'})
            self.assertEqual(readback, originals)
            diagnostics = work / 'diagnostics/raw/core'
            shutil.copytree(raw_root, diagnostics)
            for name, data in originals.items():
                self.assertEqual((diagnostics / name).read_bytes(), data)

    def test_other_raw_json_and_js_remain_public_candidates(self):
        files = {'unexpected.json': b'{}', 'unexpected.js': b'x',
                 'assets/search_index.js': b'var index = [];',
                 'other/objects.inv': b'x', 'other/.documenter-siteinfo.json': b'x'}
        self.assertEqual(producer._documenter_payload_candidates(files), files)

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
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":1e999}', b'\xff'):
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
                (work / 'raw/core/.documenter-siteinfo.json').write_bytes(b'{"original":true}')
                (work / 'raw/core/objects.inv').write_bytes(b'\x00original\xff')
                (work / 'mapping-original.json').write_bytes(b'{"retained":true}')
                raise RuntimeError('injected render failure')
            with patch.object(producer, 'produce', failed_render):
                with self.assertRaisesRegex(RuntimeError, 'injected render failure'):
                    producer.run_attempt({}, output, temporary_root)
            workspaces = list(Path(temporary_root).glob('qcl-docs-*'))
            self.assertEqual(len(workspaces), 1)
            work = workspaces[0]
            self.assertEqual((work / 'raw/core/original.html').read_bytes(), b'original failed render')
            self.assertEqual((work / 'raw/core/.documenter-siteinfo.json').read_bytes(), b'{"original":true}')
            self.assertEqual((work / 'raw/core/objects.inv').read_bytes(), b'\x00original\xff')
            self.assertEqual((work / 'mapping-original.json').read_bytes(), b'{"retained":true}')
            failure = producer.decode_json((work / 'failure.json').read_bytes())
            self.assertEqual(failure['workspace'], str(work))
            self.assertFalse(failure['candidate_output_exists'])
            self.assertFalse(output.exists())

    def test_derivation(self):
        text=(ROOT/'nix/docs.nix').read_text()
        self.assertIn('project.lib.mkDocumentation', text)
        self.assertIn('capturedMetadata = raw.depot_capture_json', text)
        factory = (ROOT / 'flake.nix').read_text()
        self.assertIn('mkDocumentation =', factory)
        self.assertNotIn('allowSubstitutes = false', factory[factory.index('mkDocumentation ='):])
        self.assertNotIn('preferLocalBuild = true', factory[factory.index('mkDocumentation ='):])

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
        tool = dict(output=str(base), executable=str(base / 'bin/tool'),
                    drv=str(base) + '.drv', expected_version='1.0')
        calls = []
        def existing_store(value):
            calls.append(value)
            self.assertIn(value, (tool['output'], tool['executable']))
            return base if value == tool['output'] else base / 'bin/tool'
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
                known = tool['drv']
                if deriver is None: tool['drv'] = None
                self.validate(tool, patches)
                self.assertEqual(calls, [tool['output'], tool['executable']])
                self.assertNotIn(known, calls)

    def test_tool_shape_and_metadata_refuse_implicit_coercion(self):
        import tempfile
        for value in (None, '', False, '/tmp/tool'):
            with self.assertRaises(ValueError): producer.store_path(value)
        bad = [('drv', value) for value in ('unknown-deriver', 'null', False,
            '', '/tmp/a.drv', '/nix/store/' + 'a' * 32 + '-a.drv/child',
            '/nix/store/' + 'a' * 32 + '-a.drv\n')]
        bad += [('expected_version', value) for value in (False, None, '', ' ', 'v' * 257)]
        for key, value in bad:
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as directory:
                tool, _, patches = self.fixture(directory)
                tool[key] = value
                with self.assertRaises(ValueError): self.validate(tool, patches)
        with tempfile.TemporaryDirectory() as directory:
            tool, _, patches = self.fixture(directory)
            tool['nar_hash'] = 'unexpected old DTO field'
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
        # Supplementary source guard; the pure Nix fixture checks the constructor.
        text = (ROOT / 'flake.nix').read_text()
        self.assertIn('builtins.unsafeDiscardStringContext output.drvPath', text)
        self.assertIn('builtins.storePath value', text)
        for field in ('source_root', 'prepared_depot', 'asset_inputs', 'review_inputs'):
            self.assertIn(field, text)


def published_callbacks(graph, retained, payload):
    """Actual published public API, isolated from the historical fixture package.

    Only historical inputs/media/oracles belong to the snapshot. No private API
    compatibility fallback and no fabricated qualification of that old graph.
    """
    import sys
    from contextlib import contextmanager
    prefix = 'qcl_negf_contracts'
    @contextmanager
    def selected(modules=None):
        saved = {k: v for k, v in sys.modules.items() if k == prefix or k.startswith(prefix + '.')}
        saved_path = sys.path[:]
        for key in saved: del sys.modules[key]
        if modules is not None: sys.modules.update(modules)
        try:
            yield
        finally:
            for key in list(sys.modules):
                if key == prefix or key.startswith(prefix + '.'): del sys.modules[key]
            sys.modules.update(saved)
            sys.path[:] = saved_path
    with selected():
        shape, binding = producer.owning_callbacks(ROOT, graph, retained, payload)
        modules = {k: v for k, v in sys.modules.items() if k == prefix or k.startswith(prefix + '.')}
        assert hasattr(modules[prefix + '.model_help'], 'validate_documentation_bundle')
        assert Path(modules[prefix].__file__).resolve().is_relative_to(ROOT / 'components/qcl-negf-contracts/src')
    def adapt(callback):
        def invoke(*args, **kwargs):
            with selected(modules): return callback(*args, **kwargs)
        return invoke
    return adapt(shape), adapt(binding)

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
        kwargs['validate_shape'], kwargs['validate_bindings'] = published_callbacks(
            kwargs['before'], retained, kwargs['payload'])
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
        kwargs['validate_shape'], kwargs['validate_bindings'] = published_callbacks(
            kwargs['before'], retained, kwargs['payload'])
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

    def test_real_c2_requires_exact_config_output_entry_and_bytes(self):
        import copy
        kwargs, retained = self.case()
        baseline = self.assembly.finalize_bundle(**kwargs)
        self.assertEqual(baseline['status'], 'candidate')
        manifest = copy.deepcopy(baseline['manifest'])
        path = 'assets/pages/6cb63afa59ff8389372f824c5f23b2257cecdeab6953440423f8c6501125707a.js'
        data = b'documenterBaseURL="..";\n'
        manifest['files'].append({'path': path, 'media_type': 'text/javascript',
                                  'bytes': len(data), 'sha256': producer.sha(data)})
        retained['payload'][path] = {'kind': 'file', 'bytes': data}
        bundle = self.fixture.raw(manifest)
        retained['bundle'] = {'bytes': bundle, 'sha256': producer.sha(bundle)}
        with self.assertRaisesRegex(Exception, 'outside output allowlist'):
            self.fixture.model_help._validate_model_help_bindings(manifest, retained=retained)
        retained['output_allowlist'] = (*retained['output_allowlist'], path)
        retained['payload'][path]['bytes'] = b'documenterBaseURL=".";\n'
        with self.assertRaisesRegex(Exception, 'inventory size or digest mismatch'):
            self.fixture.model_help._validate_model_help_bindings(manifest, retained=retained)
        retained['payload'][path]['bytes'] = data
        self.fixture.model_help._validate_model_help_bindings(manifest, retained=retained)

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
        node = os.environ.get('DOC04_NODE')
        self.assertTrue(node, 'explicit DOC04_NODE executable required for AMD source control')
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

class NativePrimaryCoverageControls(unittest.TestCase):
    """Actual owning routes are spread over six pages, not four role entries."""
    def case(self):
        assembly = producer.module('producer_native_primary_assembly', ROOT / 'ops/docs/assemble.py')
        graph = {'format': 'qcl-negf.git-graph.v1', 'revision': 'a' * 40,
                 'components': [{'path': 'components/QCLNEGF.jl', 'revision': 'b' * 40},
                                {'path': 'components/QCLNEGFRunner.jl', 'revision': 'c' * 40}]}
        sources = {
            ('components/QCLNEGF.jl', 'docs/src/theory/09_scba.md'): {'revision': 'b' * 40, 'bytes': b'scba'},
            ('components/QCLNEGFRunner.jl', 'docs/src/api/public.md'): {'revision': 'c' * 40, 'bytes': b'api'},
            ('components/QCLNEGFRunner.jl', 'docs/src/user/configuration.md'): {'revision': 'c' * 40, 'bytes': b'configuration'},
            ('root', 'docs/public/operator-recovery.md'): {'revision': 'a' * 40, 'bytes': b'operator'},
        }
        # Literal routes independently observed in retained native Documenter HTML.
        payload = {
            'core/theory/09_scba.html': b'<h1 id="researcher-scba-route">SCBA</h1>',
            'core/theory/12_validation.html': b'<h1 id="researcher-final-route">Final</h1>',
            'runner/api/public.html': b'<h1 id="reader-api-routes">API</h1>',
            'runner/user/configuration.html': b'<h1 id="developer-configuration-route">Configuration</h1>',
            'runner/user/results.html': b'<h1 id="operator-recovery-route">Recovery</h1>',
            'operator/recovery.html': b'<h1 id="operator-recovery">Operator</h1>',
        }
        return assembly, graph, {'sources': sources}, payload

    def test_all_six_actual_owning_routes_survive_primary_coverage(self):
        assembly, graph, retained, payload = self.case()
        coverage = producer.coverage_for(assembly, retained, payload)
        pages = {row['id']: {p['path']: p['anchors'] for p in row['pages']} for row in coverage}
        self.assertEqual(pages, {
            'researcher': {'core/theory/09_scba.html': ['researcher-scba-route'],
                           'core/theory/12_validation.html': ['researcher-final-route']},
            'developer': {'runner/api/public.html': ['reader-api-routes'],
                          'runner/user/configuration.html': ['developer-configuration-route']},
            'operator': {'operator/recovery.html': ['operator-recovery'],
                         'runner/user/results.html': ['operator-recovery-route']},
        })
        plan = assembly.load_pilot_plan(ROOT / 'ops/docs/pilot-plan.json')
        self.assertIsNone(assembly._bundle_coverage(plan, graph, coverage, payload))
        self.assertEqual([len(row['sources']) for row in coverage], [1, 2, 1])

    def test_unrelated_page_cannot_supply_missing_support_anchor(self):
        assembly, graph, retained, payload = self.case()
        payload['core/theory/12_validation.html'] = b'<h1>No final route</h1>'
        payload['core/unrelated.html'] = b'<h1 id="researcher-final-route">Unrelated</h1>'
        coverage = producer.coverage_for(assembly, retained, payload)
        self.assertNotIn('core/unrelated.html', [p['path'] for row in coverage for p in row['pages']])
        with self.assertRaisesRegex(assembly.DocsError, 'missing_anchor'):
            assembly._bundle_coverage(assembly.load_pilot_plan(ROOT / 'ops/docs/pilot-plan.json'),
                                      graph, coverage, payload)

    def test_missing_support_page_refuses_before_candidate(self):
        for missing in ('core/theory/12_validation.html', 'runner/user/results.html'):
            with self.subTest(missing=missing):
                assembly, _, retained, payload = self.case()
                del payload[missing]
                with self.assertRaises(KeyError):
                    producer.coverage_for(assembly, retained, payload)

    def test_coalesced_legacy_fixture_cannot_replace_owning_support_pages(self):
        assembly, _, retained, payload = self.case()
        payload['core/theory/09_scba.html'] += payload.pop('core/theory/12_validation.html')
        payload['operator/recovery.html'] += payload.pop('runner/user/results.html')
        with self.assertRaises(KeyError):
            producer.coverage_for(assembly, retained, payload)


if __name__ == '__main__':
    unittest.main()

class AuthoredHelpControls(unittest.TestCase):
    def fixture(self):
        import os
        fixture = Path(os.environ['P10_HELP_FIXTURE'])
        component = 'components/QCLNEGFRunner.jl'
        revision = '1' * 40
        graph = {'revision': '2' * 40, 'components': [{'path': component, 'revision': revision}]}
        names = ['docs/help/fragments.json', 'docs/src/user/results.md',
                 'src/infrastructure/scientific/model_help.jl']
        sources = {(component, n): {'revision': revision, 'bytes': (fixture / n).read_bytes()} for n in names}
        selectors = [(component, names[0], 'json_pointer', f'/0/inputs/{i}') for i in range(8)]
        selectors += [(component, names[1], 'file', ''),
                      (component, names[2], 'symbol', '_model_help_inputs')]
        return graph, {'sources': sources, 'input_allowlist': tuple(sources),
                       'selector_allowlist': tuple(selectors)}

    def test_authored_fragment_uses_selected_bytes_and_public_schema(self):
        import json
        from qcl_negf_contracts import schema_validator
        graph, retained = self.fixture()
        descriptors, payload = producer.authored_fragments(graph, retained, 32768)
        self.assertEqual(len(descriptors), 1)
        document = json.loads(payload[descriptors[0]['file']])
        schema_validator('model-help.schema.json').validate(document)
        self.assertEqual(document['source_revision'], graph['revision'])
        self.assertEqual(len(document['inputs']), 8)
        self.assertTrue(all(i['reference_value_origin'] is None for i in document['inputs']))
        self.assertTrue(all(i['schema_source']['revision'] == '1' * 40 for i in document['inputs']))
        self.assertTrue(all(f['status'] == 'unknown' and f['sources'] == []
                            for i in document['inputs'] for f in i['facts'] if f['text'] is None))

    def test_missing_or_unapproved_source_fails_closed(self):
        graph, retained = self.fixture()
        retained['selector_allowlist'] = ()
        with self.assertRaises(ValueError):
            producer.authored_fragments(graph, retained, 32768)

    def test_corrupt_missing_wrong_revision_and_byte_limits_fail_closed(self):
        import copy
        import json
        graph, retained = self.fixture()
        component = 'components/QCLNEGFRunner.jl'
        template = (component, 'docs/help/fragments.json')
        for mutation in ('missing_template', 'corrupt_template', 'wrong_revision',
                         'missing_source', 'missing_input', 'oversized_template', 'output_limit',
                         'excess_facts', 'fabricated_reference', 'injected_revision'):
            with self.subTest(mutation=mutation):
                case = copy.deepcopy(retained)
                limit = 32768
                if mutation == 'missing_template': del case['sources'][template]
                if mutation == 'corrupt_template': case['sources'][template]['bytes'] = b'[{}]'
                if mutation == 'wrong_revision': case['sources'][template]['revision'] = '3' * 40
                if mutation == 'missing_source': del case['sources'][(component, 'docs/src/user/results.md')]
                if mutation == 'missing_input': case['input_allowlist'] = ()
                if mutation == 'oversized_template': case['sources'][template]['bytes'] += b' ' * 32768
                if mutation == 'output_limit': limit = 100
                if mutation in ('excess_facts', 'fabricated_reference', 'injected_revision'):
                    template_doc = json.loads(case['sources'][template]['bytes'])
                    if mutation == 'excess_facts': template_doc[0]['inputs'][0]['facts'].append({})
                    if mutation == 'fabricated_reference': template_doc[0]['inputs'][0]['reference_value_origin'] = {}
                    if mutation == 'injected_revision': template_doc[0]['meaning_source']['revision'] = '1' * 40
                    case['sources'][template]['bytes'] = producer.encode(template_doc)
                with self.assertRaises((ValueError, KeyError)):
                    producer.authored_fragments(graph, case, limit)

    def test_full_candidate_through_actual_public_contract(self):
        """Synthetic graph/reviews; exact Runner inputs and selected Contracts bytes."""
        import copy
        import os
        import sys
        from contextlib import contextmanager
        snapshot = Path(os.environ['QCL_DOCS_TEST_SNAPSHOT'])
        contract_src = Path(os.environ['P10_CONTRACTS_SRC']).resolve()
        prefix = 'qcl_negf_contracts'
        saved = {k: v for k, v in sys.modules.items() if k == prefix or k.startswith(prefix + '.')}
        saved_path = sys.path[:]
        for key in saved: del sys.modules[key]
        try:
            historical = producer.module('_p10_historical_fixture', snapshot / 'tests/test_docs_bundle_closure.py')
            kwargs, _, _, retained = historical.frozen_case()
            for key in list(sys.modules):
                if key == prefix or key.startswith(prefix + '.'): del sys.modules[key]
            sys.path.insert(0, str(contract_src))
            import qcl_negf_contracts as contracts
            from qcl_negf_contracts import model_help
            self.assertTrue(Path(contracts.__file__).resolve().is_relative_to(contract_src))
            assembly = producer.module('_p10_contract_assembly', ROOT / 'ops/docs/assemble.py')
            graph = kwargs['before']
            component = 'components/QCLNEGFRunner.jl'
            runner_revision = 'c8ac293798b8bd2505fe59063d79077f14d32018'
            contract_component = 'components/qcl-negf-contracts'
            # Detached engineering graph: Runner is published; candidate Contracts
            # revision is deliberately synthetic until its owner publishes it.
            candidate_revision = '4' * 40
            for selected_graph in (kwargs['before'], kwargs['after'], retained['selection']['sources']):
                for row in selected_graph['components']:
                    if row['path'] == component: row['revision'] = runner_revision
                    if row['path'] == contract_component: row['revision'] = candidate_revision
            for (owner, _), row in retained['sources'].items():
                if owner == component: row['revision'] = runner_revision
                if owner == contract_component: row['revision'] = candidate_revision
            for coverage in kwargs['coverage']:
                for ref in coverage['sources']:
                    if ref['component'] == component: ref['revision'] = runner_revision
            for review in retained['public_reviews']:
                if review['source']['component'] == component:
                    review['source']['revision'] = runner_revision
            schema_path = 'src/qcl_negf_contracts/schemas/model-help.schema.json'
            schema = retained['sources'][(contract_component, schema_path)]
            schema['bytes'] = (contract_src / 'qcl_negf_contracts/schemas/model-help.schema.json').read_bytes()
            kwargs['schema_ref'] = producer.reference(retained, contract_component, schema_path)
            for review in retained['public_reviews']:
                if (review['source']['component'], review['source']['path']) == (contract_component, schema_path):
                    review['source'] = copy.deepcopy(kwargs['schema_ref'])
            fixture = Path(os.environ['P10_HELP_FIXTURE'])
            names = ('docs/help/fragments.json', 'docs/src/user/results.md',
                     'src/infrastructure/scientific/model_help.jl')
            for name in names:
                retained['sources'][(component, name)] = {'revision': runner_revision,
                                                           'bytes': (fixture / name).read_bytes()}
            retained['input_allowlist'] += tuple((component, name) for name in names)
            retained['selector_allowlist'] += tuple((component, names[0], 'json_pointer', f'/0/inputs/{i}')
                                                      for i in range(8))
            retained['selector_allowlist'] += ((component, names[1], 'file', ''),
                                                (component, names[2], 'symbol', '_model_help_inputs'))
            recipe = kwargs['generator']['recipes'][0]
            for name in names:
                source = producer.reference(retained, component, name)
                retained['public_reviews'] += ({'source': source, 'recipe': recipe,
                    'receipt': {'bytes': b'synthetic review', 'sha256': producer.sha(b'synthetic review')}},)
            descriptors, help_payload = producer.authored_fragments(graph, retained, 32768)
            kwargs['fragments'] = descriptors
            kwargs['payload'].update(help_payload)
            kwargs['payload']['runner/user/results.html'] = (
                b'<html><head></head><body><h1 id="solver-input-help">Actual input</h1></body></html>')
            retained['output_allowlist'] += tuple(help_payload) + ('runner/user/results.html',)
            kwargs['validate_shape'] = contracts.schema_validator('model-help.schema.json').validate
            def bindings(document, *, coverage):
                blob = producer.encode(document)
                retained['bundle'] = {'bytes': blob, 'sha256': producer.sha(blob)}
                retained['payload'] = {path: {'kind': 'file', 'bytes': data}
                                       for path, data in kwargs['payload'].items()}
                model_help.validate_documentation_bundle(document, retained=retained,
                    required_sources=[r for row in coverage for r in row['sources']])
            kwargs['validate_bindings'] = bindings
            kwargs['validate_assets'] = lambda lock, inputs, *, payload: {}
            result = assembly.finalize_bundle(**kwargs)
            self.assertEqual(result['status'], 'candidate')
            self.assertEqual(result['manifest']['sources']['revision'], graph['revision'])
            path = descriptors[0]['file']
            cases = ('wrong_source_hash', 'missing_review', 'missing_selector', 'wrong_revision',
                     'missing_page_anchor', 'changed_fragment_bytes', 'missing_output_allowlist')
            for mutation in cases:
                with self.subTest(mutation=mutation):
                    saved_retained, saved_payload = copy.deepcopy(retained), dict(kwargs['payload'])
                    if mutation == 'wrong_source_hash': retained['sources'][(component, names[1])]['bytes'] += b'x'
                    if mutation == 'missing_review': retained['public_reviews'] = ()
                    if mutation == 'missing_selector': retained['selector_allowlist'] = ()
                    if mutation == 'wrong_revision': retained['sources'][(component, names[0])]['revision'] = '3' * 40
                    if mutation == 'missing_page_anchor': kwargs['payload']['runner/user/results.html'] = b'<html><head></head><body></body></html>'
                    if mutation == 'changed_fragment_bytes': kwargs['payload'][path] += b' '
                    if mutation == 'missing_output_allowlist': retained['output_allowlist'] = ()
                    try:
                        with self.assertRaises((model_help.ContractError,
                                                model_help.DocumentationProofMissing, assembly.DocsError)):
                            assembly.finalize_bundle(**kwargs)
                    finally:
                        retained.clear(); retained.update(saved_retained)
                        kwargs['payload'].clear(); kwargs['payload'].update(saved_payload)
        finally:
            for key in list(sys.modules):
                if key == prefix or key.startswith(prefix + '.'): del sys.modules[key]
            sys.modules.update(saved)
            sys.path[:] = saved_path

class RunnerHelpSourceProjection(unittest.TestCase):
    def test_only_authored_template_is_added_to_existing_runner_projection(self):
        import re
        source = (ROOT / 'nix/docs-sources.nix').read_text()
        match = re.search(r'runner\s*=\s*select\s*\(root\s*\+\s*"/components/QCLNEGFRunner.jl"\)\s*\[([^]]+)\]', source)
        self.assertIsNotNone(match)
        paths = re.findall(r'"([^"]+)"', match.group(1))
        self.assertEqual(paths, ['docs/make.jl', 'docs/Project.toml', 'docs/src', 'docs/help/fragments.json'])
        flake = (ROOT / 'flake.nix').read_text()
        self.assertIn('runnerDocs = selected.runner;', flake)
        self.assertIn('cp -a "$runnerDocs"/. "$out/components/QCLNEGFRunner.jl/"', flake)
        self.assertIn('source_root = workspace;', flake)

    def test_actual_nix_fileset_includes_exact_bytes_and_excludes_sibling(self):
        import hashlib
        import json
        import os
        import shutil
        import subprocess
        import tempfile
        nix = shutil.which('nix-instantiate')
        lib = os.environ.get('P10_NIX_LIB')
        fixture = os.environ.get('P10_HELP_FIXTURE')
        if not (nix and lib and fixture):
            self.skipTest('requires existing nix-instantiate, P10_NIX_LIB and frozen P10_HELP_FIXTURE')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / 'components/QCLNEGFRunner.jl/docs'
            (docs / 'help').mkdir(parents=True)
            (docs / 'src').mkdir()
            (docs / 'make.jl').write_bytes(b'fixture')
            (docs / 'Project.toml').write_bytes(b'fixture')
            (docs / 'src/page.md').write_bytes(b'fixture')
            original = (Path(fixture) / 'docs/help/fragments.json').read_bytes()
            (docs / 'help/fragments.json').write_bytes(original)
            (docs / 'help/unselected.txt').write_bytes(b'unselected')
            def path(value):
                return '(/. + ' + json.dumps(str(value), ensure_ascii=False) + ')'
            expression = '''let
              lib0 = import (LIB);
              lib = lib0 // { fileset = lib0.fileset // {
                toSource = { root, fileset }: lib0.fileset.toList fileset;
              }; };
              selected = import (SOURCE) { inherit lib; root = ROOTPATH; };
              paths = selected.runner;
              help = HELPPATH; extra = EXTRAPATH;
              in { hash = builtins.hashFile "sha256" help;
                   included = builtins.elem help paths;
                   excluded = !(builtins.elem extra paths); }
            '''
            for key, value in {'LIB': path(lib), 'SOURCE': path(ROOT / 'nix/docs-sources.nix'),
                               'ROOTPATH': path(root), 'HELPPATH': path(docs / 'help/fragments.json'),
                               'EXTRAPATH': path(docs / 'help/unselected.txt')}.items():
                expression = expression.replace(key, value)
            result = subprocess.run([nix, '--eval', '--strict', '--json', '--expr', expression],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {'included': True, 'excluded': True,
                'hash': hashlib.sha256(original).hexdigest()})
