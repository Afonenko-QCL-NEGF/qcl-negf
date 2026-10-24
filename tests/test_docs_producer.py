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

class ProducerClosureControls(unittest.TestCase):
    """Real owning C1+C2, small historical engineering render fixture only.

    Root supplies its initialized immutable read-only snapshot for Contracts;
    this worktree intentionally does not initialize or advance any gitlinks.
    """
    @classmethod
    def setUpClass(cls):
        import os
        snapshot = os.environ.get('QCL_DOCS_TEST_SNAPSHOT')
        if snapshot is None:
            raise RuntimeError('Root must supply QCL_DOCS_TEST_SNAPSHOT for real C1+C2 fixtures')
        cls.snapshot = Path(snapshot)
        cls.fixture = producer.module('producer_closure_frozen', cls.snapshot / 'tests/test_docs_bundle_closure.py')
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
