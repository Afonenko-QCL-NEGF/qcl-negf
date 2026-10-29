"""DOC04 pure adapters: literal fixtures, no Julia/Documenter/build/network.

Phase 1 source only: this file has not been executed. The proposed test seams
are local pure functions, not a second DOC03 serialization contract.
"""
import copy
import hashlib
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("docs_assembly", ROOT / "ops/docs/assemble.py")
assembly = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assembly)


def digest(data):
    return hashlib.sha256(data).hexdigest()


# Synthetic known-shape excerpt; not claimed to be actual Documenter output.
RAW = b'''<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" class="docs-theme-link" data-theme-name="documenter-light" href="assets/themes/documenter-light.css">
<link rel="stylesheet" class="docs-theme-link" data-theme-name="documenter-dark" href="assets/themes/documenter-dark.css">
<script src="assets/themeswap.js"></script>
<script>documenterBaseURL=".."</script>
</head><body data-theme-primary-dark="documenter-dark">
<a id="documenter-settings-button" href="#documenter-settings">Settings</a>
<div id="documenter-settings"><select id="documenter-themepicker"><option>Automatic (OS)</option><option>Dark</option></select></div>
<article id="documenter-page"><h1 id="researcher-scba-route">SCBA</h1>
<p id="model-gaas">Small mixed step does not establish a fixed point.</p>
<a href="final.html#researcher-final-route">Final assessment</a>
<p class="math-container" id="eq-self-energy">\\[\\Sigma^r(E)\\]</p>
<pre><code>price = "$5"</code></pre></article></body></html>'''
BINDING = {
    "documenter_version": "1.17.0",
    "documenter_tree_sha1": "56e9c37b5e7c3b4f080ab1da18d72d5c290e184a",
    "policy": "documenter-1.17-light-self-v1",
}
MATH_MAPPING = [{
    "page": "core/theory/09_scba.html", "selector": "#eq-self-energy",
    "tex": r"\Sigma^r(E)", "tex_sha256": digest(br"\Sigma^r(E)"), "display": True,
}]

# Independent root-relative source/URL expectations from accepted DOC04 section 1.
PRIMARY = {
    "researcher": {
        "section": "core",
        "primary_sources": ["components/QCLNEGF.jl/docs/src/theory/09_scba.md"],
        "primary_urls": ["core/theory/09_scba.html#researcher-scba-route"],
    },
    "developer": {
        "section": "runner",
        "primary_sources": ["components/QCLNEGFRunner.jl/docs/src/api/public.md",
                            "components/QCLNEGFRunner.jl/docs/src/user/configuration.md"],
        "primary_urls": ["runner/api/public.html#reader-api-routes",
                         "runner/user/configuration.html#developer-configuration-route"],
    },
    "operator": {
        "section": "operator",
        "primary_sources": ["docs/public/operator-recovery.md"],
        "primary_urls": ["operator/recovery.html#operator-recovery"],
    },
}
AVAILABLE_PRIMARY = {
    "components/QCLNEGF.jl/docs/src/theory/09_scba.md",
    "components/QCLNEGFRunner.jl/docs/src/api/public.md",
    "components/QCLNEGFRunner.jl/docs/src/user/configuration.md",
    "docs/public/operator-recovery.md",
}


class ScriptReferences(HTMLParser):
    """Test-only observation of external script attributes; never evaluates JS."""

    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            source = dict(attrs).get("src")
            if source is not None:
                self.sources.append(source)


class DocsAssemblyTests(unittest.TestCase):
    def transform(self, raw=RAW, binding=None):
        return assembly.transform_page(
            raw, page="core/theory/09_scba.html",
            binding=BINDING if binding is None else binding,
            expected_sha256=digest(RAW),
            math_mapping=copy.deepcopy(MATH_MAPPING),
        )

    def rejected(self, call, reason):
        with self.assertRaises(assembly.DocsError) as caught:
            call()
        self.assertEqual(caught.exception.code, reason)

    def test_known_head_externalizes_only_config_and_preserves_article_ids_and_tex(self):
        result = self.transform()
        html = result["html"].decode()
        self.assertIn('id="researcher-scba-route"', html)
        self.assertIn('id="model-gaas"', html)
        self.assertIn('id="eq-self-energy"', html)
        self.assertIn('Small mixed step does not establish a fixed point.', html)
        self.assertIn('final.html#researcher-final-route', html)
        self.assertIn('price = "$5"', html)
        self.assertEqual(result["math"], [{
            "page": "core/theory/09_scba.html", "selector": "#eq-self-energy",
            "tex": r"\Sigma^r(E)", "tex_sha256": digest(br"\Sigma^r(E)"),
            "display": True,
        }])
        self.assertEqual(result["input_sha256"], digest(RAW))
        self.assertEqual(result["output_sha256"], digest(result["html"]))
        self.assertTrue(result["generated_files"])
        config_files = {path: content for path, content in result["generated_files"].items()
                        if b"documenterBaseURL" in content}
        self.assertEqual(len(config_files), 1)
        config_path, config_bytes = next(iter(config_files.items()))
        self.assertEqual(config_path, 'assets/pages/6cb63afa59ff8389372f824c5f23b2257cecdeab6953440423f8c6501125707a.js')
        self.assertEqual(config_bytes, b'documenterBaseURL="..";\n')
        scripts = ScriptReferences()
        scripts.feed(html)
        resolved = []
        for source in scripts.sources:
            parsed = urlsplit(source)
            self.assertFalse(parsed.scheme or parsed.netloc)
            self.assertFalse(source.startswith("/"))
            resolved.append(urljoin("core/theory/09_scba.html", source))
        self.assertIn(config_path, resolved, "generated config must be loaded by the output page")
        self.assertEqual(resolved.count(config_path), 1)
        # Isolate script closure from the unrelated article/css fixture references.
        config_source = scripts.sources[resolved.index(config_path)]
        config_payload = {"core/theory/09_scba.html":
                          f'<script src="{config_source}"></script>'.encode(),
                          config_path: config_bytes}
        assembly.validate_payload(config_payload)
        del config_payload[config_path]
        self.rejected(lambda: assembly.validate_payload(config_payload), "missing_resource")
        for forbidden in ('themeswap', 'documenter-dark', 'data-theme-primary-dark',
                          'documenter-settings', 'Automatic (OS)', '<script>'):
            self.assertNotIn(forbidden, html)

    def test_wrong_generator_binding_and_changed_raw_bytes_fail_closed(self):
        for field, value in (("documenter_version", "1.18.0"),
                             ("documenter_tree_sha1", "1" * 40)):
            binding = {**BINDING, field: value}
            with self.subTest(field=field):
                self.rejected(lambda: self.transform(binding=binding), "generator_mismatch")
        self.rejected(lambda: self.transform(RAW + b"\n"), "input_hash_mismatch")

    def test_unknown_or_duplicate_inline_head_node_is_not_silently_stripped(self):
        for addition in (b'<script>alert(1)</script>',
                         b'<script>documenterBaseURL=".."</script>'):
            raw = RAW.replace(b"</head>", addition + b"</head>")
            self.rejected(lambda: assembly.transform_page(
                raw, page="core/theory/09_scba.html", binding=BINDING,
                expected_sha256=digest(raw), math_mapping=MATH_MAPPING), "unsupported_generated_shape")

    def test_config_identity_is_page_and_canonical_assignment_not_article_bytes(self):
        original = self.transform()
        changed = RAW.replace(b'Small mixed step', b'A different article')
        updated = assembly.transform_page(changed, page='core/theory/09_scba.html',
            binding=BINDING, expected_sha256=digest(changed), math_mapping=MATH_MAPPING)
        self.assertEqual(updated['generated_files'], original['generated_files'])
        self.assertNotEqual(updated['input_sha256'], original['input_sha256'])
        self.assertNotEqual(updated['output_sha256'], original['output_sha256'])
        self.rejected(lambda: assembly.transform_page(changed, page='core/theory/09_scba.html',
            binding=BINDING, expected_sha256=digest(RAW), math_mapping=MATH_MAPPING), 'input_hash_mismatch')

    def test_config_vectors_and_invalid_page_paths(self):
        vectors = (
            ('operator/index.html', '.', 'a7c9b4631206fa4d149ec937a2cf290193dff35c0790137839d5cbb80760d174'),
            ('operator/capture-runtime-delivery.html', '.', '6cae3f7d445a8cc1be74951d6c355a857e905b4035e1baa01a0d19d14037b901'),
            ('core/a/b/c.html', '../..', 'cc083dd2fdf34e27d50757a365c5f0a9803d465890051a58c530b7358e830ba1'),
        )
        for page, base, identifier in vectors:
            raw = (b'<html><head><link rel="stylesheet" class="docs-theme-link" '
                   b'data-theme-name="documenter-light" href="assets/themes/documenter-light.css">'
                   b'<script>documenterBaseURL="' + base.encode() + b'"</script></head><body></body></html>')
            result = assembly.transform_page(raw, page=page, binding=BINDING,
                expected_sha256=digest(raw), math_mapping=[])
            config_files = {name: data for name, data in result['generated_files'].items()
                            if name.startswith('assets/pages/')}
            self.assertEqual(config_files, {
                'assets/pages/' + identifier + '.js': b'documenterBaseURL="' + base.encode() + b'";\n'})
        for page in ('index.html', 'other/a.html', 'core/a.md', 'core/../a.html',
                     '/core/a.html', 'core\\a.html', 'core/%61.html'):
            with self.subTest(page=page):
                self.rejected(lambda: assembly.transform_page(RAW, page=page, binding=BINDING,
                    expected_sha256=digest(RAW), math_mapping=[]), 'public_allowlist')

    def test_wrong_or_missing_base_assignment_is_rejected(self):
        for value in (b'.', b'../../', b'../.', b'', b'/'):
            raw = RAW.replace(b'documenterBaseURL=".."', b'documenterBaseURL="' + value + b'"')
            self.rejected(lambda: assembly.transform_page(raw, page='core/theory/09_scba.html',
                binding=BINDING, expected_sha256=digest(raw), math_mapping=MATH_MAPPING),
                'unsupported_generated_shape')
        raw = RAW.replace(b'<script>documenterBaseURL=".."</script>', b'')
        self.rejected(lambda: assembly.transform_page(raw, page='core/theory/09_scba.html',
            binding=BINDING, expected_sha256=digest(raw), math_mapping=MATH_MAPPING),
            'unsupported_generated_shape')

    def test_only_exact_documenter_math_nodes_are_captured(self):
        result = self.transform()
        self.assertEqual(len(result["math"]), 1)
        self.assertNotIn("price", result["math"][0]["tex"])

    def test_wrong_source_node_mapping_is_rejected_without_formula_rewrite(self):
        wrong = [{**MATH_MAPPING[0], "tex": "x", "tex_sha256": digest(b"x")}]
        self.rejected(lambda: assembly.transform_page(
            RAW, page="core/theory/09_scba.html", binding=BINDING,
            expected_sha256=digest(RAW), math_mapping=wrong), "math_mapping_mismatch")

    def test_plain_span_inline_math_requires_explicit_reviewed_source_mapping(self):
        raw = RAW.replace(b'<p class="math-container" id="eq-self-energy">\\[\\Sigma^r(E)\\]</p>',
                          b'<span id="eq-self-energy">$\\Sigma^r(E)$</span>')
        mapped = [{**MATH_MAPPING[0], "display": False}]
        result = assembly.transform_page(
            raw, page="core/theory/09_scba.html", binding=BINDING,
            expected_sha256=digest(raw), math_mapping=mapped)
        self.assertEqual(result["math"], mapped)
        self.assertIn(b'price = "$5"', result["html"])

    def test_source_gate_rejects_executable_directive_without_importing_sentinel(self):
        for directive in ("@example", "@eval", "@repl", "@setup", "jldoctest"):
            source = f'```{directive}\nerror("DOC04_SENTINEL_MUST_NOT_RUN")\n```\n'
            self.rejected(lambda: assembly.validate_authored_source(source),
                          "executable_docs_directive")
        assembly.validate_authored_source('```julia\nerror("literal only")\n```\n')
        assembly.validate_authored_source('```@meta\nCurrentModule = QCLNEGF\n```\n```@docs\nsolve\n```\n')

    def test_source_gate_accepts_only_static_cross_graph_navigation(self):
        source = ('```@raw html\n<ul>\n<li><a href="../runner/user/results.html#operator-recovery-route">'
                  'Runner</a> и <a href="https://example.org/reference">reference</a>.</li>\n</ul>\n```\n')
        assembly.validate_authored_source(source)
        # Actual authored chapter must pass the same producer preflight.
        assembly.validate_authored_source((ROOT / 'docs/public/operator-recovery.md').read_text())

    def test_source_navigation_rejects_code_attributes_and_malformed_fragments(self):
        bad = [
            '<script>sentinel()</script>', '<ul onclick="sentinel()"><li>x</li></ul>',
            '<ul><li><a href="x" style="color:red">x</a></li></ul>',
            '<ul><li><a href="javascript:sentinel()">x</a></li></ul>',
            '<ul><li><a href="data:text/html,x">x</a></li></ul>',
            '<ul><li><a href="//example.org/x">x</a></li></ul>',
            '<ul><li><a href="/absolute">x</a></li></ul>',
            '<ul><li><a href="https://user:password@example.org/x">x</a></li></ul>',
            '<ul><li><a href="https://@example.org/x">x</a></li></ul>',
            '<ul><li><a href="x" href="y">x</a></li></ul>',
            '<ul><li><a href="x"><img src="x"></a></li></ul>',
            '<ul><li><a href="x"/></li></ul>', '<ul><li>x</ul>',
            '<ul><li><!-- hidden -->x</li></ul>', '<!DOCTYPE html><ul><li>x</li></ul>',
            '<ul><li>x</li></ul><ul><li>second root</li></ul>',
            'non-list text<ul><li>x</li></ul>', '<ul><a href="x">outside li</a></ul>',
            '<ul><li><a href="x"><a href="y">nested</a></a></li></ul>',
            '<ul><li><a href="x?query=1">x</a></li></ul>', '<ul><li><a href="x">x</a></li></ul>' + ' ' * 32769,
        ]
        for html in bad:
            with self.subTest(fragment=html[:90]):
                self.rejected(lambda: assembly.validate_authored_source(
                    '```@raw html\n' + html + '\n```\n'), 'unsupported_navigation_fragment')
        for info in ('@raw latex', '@raw HTML', '@raw html extra'):
            self.rejected(lambda: assembly.validate_authored_source(
                '```' + info + '\n<ul><li>x</li></ul>\n```\n'), 'unsupported_docs_directive')
        self.rejected(lambda: assembly.validate_authored_source(
            '```@raw html\n<ul><li><a href="x">x</a></li></ul>\n'),
            'unsupported_navigation_fragment')

    def test_source_navigation_rejects_discarded_closing_syntax(self):
        for end in ('</a onclick="sentinel()">', '</a garbage>', '</a/>', '</>'):
            with self.subTest(end=end):
                fragment = '<ul><li><a href="x">x' + end + '</li></ul>'
                self.rejected(lambda: assembly.validate_authored_source(
                    '```@raw html\n' + fragment + '\n```\n'),
                    'unsupported_navigation_fragment')

    def test_source_navigation_rejects_tolerated_malformed_opening_syntax(self):
        for fragment in ('<ul / ><li><a href="x">x</a></li></ul>',
                         '<ul><li><a/href="x">x</a></li></ul>'):
            with self.subTest(fragment=fragment):
                self.rejected(lambda: assembly.validate_authored_source(
                    '```@raw html\n' + fragment + '\n```\n'),
                    'unsupported_navigation_fragment')
        assembly.validate_authored_source(
            '```@raw html\n<UL ><LI><A href=x>x</A ></LI></UL>\n```\n')

    def test_source_navigation_validates_https_ports_and_control_bytes(self):
        for href in ('https://example.org:nope/x', 'https://example.org:70000/x',
                     'https://example.org:-1/x', 'https://example.org:/x',
                     'https://example.org/x\x7f', 'https://example.org/x%7F',
                     'https://example.org/x&#127;'):
            with self.subTest(href=repr(href)):
                self.rejected(lambda: assembly.validate_authored_source(
                    '```@raw html\n<ul><li><a href="' + href +
                    '">x</a></li></ul>\n```\n'), 'unsupported_navigation_fragment')
        for href in ('https://example.org:443/x', 'https://[::1]:443/x',
                     'https://example.org/x', '../runner/user/results.html#operator-recovery-route'):
            with self.subTest(valid_href=href):
                assembly.validate_authored_source(
                    '```@raw html\n<ul><li><a href="' + href +
                    '">x</a></li></ul>\n```\n')

    def test_source_navigation_validates_literal_authority_before_percent_decoding(self):
        bad = ('https://example.org:%34%34%33/x', 'https://example.org:44%33/x',
               'https://example.org:%30%30%34%34%33/x', 'https://example.org%3A443/x',
               'https://example.org%2Fother/x', 'https://example.org%23fragment/x',
               'https://%5B::1%5D:443/x', 'h%74tps://example.org/x',
               'https://example%zz.org/x')
        for href in bad:
            with self.subTest(href=href):
                self.rejected(lambda: assembly.validate_authored_source(
                    '```@raw html\n<ul><li><a href="' + href +
                    '">x</a></li></ul>\n```\n'), 'unsupported_navigation_fragment')
        for href in ('https://example.org&#58;443/x', 'https://example.org:&#52;43/x',
                     'https://example.org/path/%D0%B0', 'https://[::1]:443/x'):
            with self.subTest(valid_href=href):
                assembly.validate_authored_source(
                    '```@raw html\n<ul><li><a href="' + href +
                    '">x</a></li></ul>\n```\n')

    def test_three_primary_slices_require_exact_sources_and_anchors(self):
        plan = assembly.load_pilot_plan(ROOT / "ops/docs/pilot-plan.json")
        slices = {item["id"]: item for item in plan["slices"]}
        self.assertEqual(set(slices), {"researcher", "developer", "operator"})
        for identity, expected in PRIMARY.items():
            with self.subTest(slice=identity):
                self.assertEqual(slices[identity]["section"], expected["section"])
                self.assertEqual(slices[identity]["primary_sources"], expected["primary_sources"])
                self.assertEqual(slices[identity]["primary_urls"], expected["primary_urls"])
        self.assertEqual(set(plan["expected_primary_anchors"]), {
            "researcher-scba-route", "researcher-final-route", "reader-api-routes",
            "developer-configuration-route", "operator-recovery-route", "operator-recovery",
        })
        assembly.validate_primary_sources(plan, AVAILABLE_PRIMARY)
        available = AVAILABLE_PRIMARY - {"components/QCLNEGF.jl/docs/src/theory/09_scba.md"}
        self.rejected(lambda: assembly.validate_primary_sources(plan, available),
                      "missing_primary_source")

    def test_primary_source_and_url_mutants_do_not_redefine_the_accepted_journeys(self):
        plan = assembly.load_pilot_plan(ROOT / "ops/docs/pilot-plan.json")
        for identity in ("researcher", "developer", "operator"):
            for field, wrong in (("primary_sources", ["docs/unrelated.md"]),
                                 ("primary_urls", ["index.html#unrelated"])):
                changed = copy.deepcopy(plan)
                target = next(item for item in changed["slices"] if item["id"] == identity)
                target[field] = wrong
                # Extra available wrong path prevents an availability error masking binding.
                with self.subTest(slice=identity, field=field):
                    self.rejected(lambda: assembly.validate_primary_sources(
                        changed, AVAILABLE_PRIMARY | {"docs/unrelated.md"}),
                        "primary_mapping_mismatch")

    def test_graph_change_does_not_inherit_old_source_acceptance(self):
        before = {"format": "qcl-negf.git-graph.v1", "revision": "a" * 40,
                  "components": [{"path": "components/QCLNEGF.jl", "revision": "b" * 40,
                                  "url": "https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl.git"}]}
        assembly.validate_source_binding(before, copy.deepcopy(before))
        after = copy.deepcopy(before)
        after["components"][0]["revision"] = "c" * 40
        self.rejected(lambda: assembly.validate_source_binding(before, after), "source_graph_mismatch")

    def test_local_resource_anchor_closure_accepts_real_target(self):
        files = {"index.html": b'<a href="core/final.html#done">Final</a>',
                 "core/final.html": b'<h1 id="done">Done</h1>'}
        assembly.validate_payload(files)
        files["core/final.html"] = b'<h1 id="other">Other</h1>'
        self.rejected(lambda: assembly.validate_payload(files), "missing_anchor")
        del files["core/final.html"]
        self.rejected(lambda: assembly.validate_payload(files), "missing_resource")

    def test_resource_scanner_checks_css_and_static_worker_edges(self):
        files = {"index.html": b'<link rel="stylesheet" href="assets/a.css"><script src="assets/search.js"></script>',
                 "assets/a.css": b'@font-face{font-family:k;src:url("font.woff2")}',
                 "assets/font.woff2": b'synthetic font, not licensed public data',
                 "assets/search.js": b'new Worker("assets/worker.js");',
                 "assets/worker.js": b'importScripts("minisearch.js");',
                 "assets/minisearch.js": b'/* synthetic closed dependency */'}
        assembly.validate_payload(files)
        for missing in ("assets/font.woff2", "assets/worker.js", "assets/minisearch.js"):
            changed = dict(files)
            del changed[missing]
            with self.subTest(missing=missing):
                self.rejected(lambda: assembly.validate_payload(changed), "missing_resource")
        # Classic script's Worker URL is document-relative, not relative to assets/search.js.
        changed = {**files, "assets/search.js": b'new Worker("worker.js");'}
        self.rejected(lambda: assembly.validate_payload(changed), "missing_resource")

    def test_css_import_closure_tracks_supported_literals_and_rejects_media_grammar(self):
        files = {"index.html": b'<link rel="stylesheet" href="assets/a.css">',
                 "assets/a.css": b'@import "base.css";',
                 "assets/base.css": b'body{color:#111;background:#fff}'}
        assembly.validate_payload(files)
        missing = {key: value for key, value in files.items() if key != "assets/base.css"}
        self.rejected(lambda: assembly.validate_payload(missing), "missing_resource")
        for directive in (b'@import url("base.css");', b'@import url(base.css);'):
            assembly.validate_payload({**files, "assets/a.css": directive})
            self.rejected(lambda: assembly.validate_payload(
                {**missing, "assets/a.css": directive}), "missing_resource")
        for resource in (b'"https://cdn.example/x.css"', b'url("https://cdn.example/x.css")'):
            changed = {**files, "assets/a.css": b'@import ' + resource + b';'}
            self.rejected(lambda: assembly.validate_payload(changed), "external_resource")
        for directive in (b'@import "https://cdn.example/x.css" screen;',
                          b'@import "missing.css" screen;',
                          b'@import url("missing.css") print;',
                          b'@import "base.css" layer(pilot);',
                          br'@im\port "missing.css";'):
            with self.subTest(directive=directive):
                self.rejected(lambda: assembly.validate_payload(
                    {**files, "assets/a.css": directive}), "dynamic_loader")

    def test_static_esm_import_export_forms_fail_closed_for_local_and_external_targets(self):
        files = {"index.html": b'<script type="module" src="assets/a.js"></script>',
                 "assets/a.js": b'const answer = 1;', "assets/local.js": b'const value = 1;'}
        assembly.validate_payload(files)
        for source in (b'import "https://cdn.example/x.js";',
                       b'import x from "https://cdn.example/x.js";',
                       b'export {x} from "https://cdn.example/x.js";',
                       b'export * from "https://cdn.example/x.js";',
                       b'import "missing.js";', b'import x from "local.js";',
                       b'export {x} from "missing.js";', b'export * from "local.js";'):
            with self.subTest(source=source):
                self.rejected(lambda: assembly.validate_payload(
                    {**files, "assets/a.js": source}), "dynamic_loader")

    def test_self_closing_nodes_share_shape_and_count_caps_with_start_tags(self):
        def transformed(addition):
            raw = RAW.replace(b'</article>', addition + b'</article>')
            return assembly.transform_page(
                raw, page="core/theory/09_scba.html", binding=BINDING,
                expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING))
        healthy = transformed(b'<br/>')
        self.assertIn(b'<br/>', healthy["html"])
        self.rejected(lambda: transformed(b'<br title="x" title="y"/>'),
                      "unsupported_generated_shape")
        self.rejected(lambda: transformed(b'<br/>' * 100001), "page_limit")
        self.rejected(lambda: transformed(b'<div>' * 513 + b'<br/>' + b'</div>' * 513),
                      "page_limit")

    def test_pinned_table_alignment_moves_to_external_css_without_changing_cells(self):
        for direction in ('left', 'center', 'right'):
            with self.subTest(direction=direction):
                table = ('<table><tr><th class="kept" style="text-align: ' + direction +
                         '">Header</th></tr><tr><td style="text-align: ' + direction +
                         '">-2 &amp; 3</td></tr></table>').encode()
                raw = RAW.replace(b'</article>', table + b'</article>')
                result = assembly.transform_page(raw, page='core/theory/09_scba.html',
                    binding=BINDING, expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING))
                self.assertNotIn(b'style=', result['html'])
                self.assertIn(('class="kept qcl-table-align-' + direction + '"').encode(), result['html'])
                self.assertIn(('class="qcl-table-align-' + direction + '"').encode(), result['html'])
                self.assertIn(b'>Header</th>', result['html'])
                self.assertIn(b'>-2 &amp; 3</td>', result['html'])
                css = result['generated_files']['assets/runtime/qcl-fixed-light.css']
                self.assertIn(('#documenter-page th.qcl-table-align-' + direction + ',#documenter-page td.qcl-table-align-' +
                               direction + '{text-align:' + direction + '}').encode(), css)
                parser = assembly._PayloadHTML('core/theory/09_scba.html')
                parser.feed(result['html'].decode())
                parser.close()

    def test_table_alignment_does_not_admit_other_inline_css_or_tags(self):
        for tag, style in (('p', 'text-align: right'), ('table', 'text-align: right'),
                           ('td', 'text-align: right; color:red'), ('th', 'text-align: right;'),
                           ('td', 'text-align: justify'), ('td', 'TEXT-ALIGN: right'),
                           ('td', 'text-align: url(x)'), ('td', 'text-align:right')):
            with self.subTest(tag=tag, style=style):
                addition = ('<' + tag + ' style="' + style + '">x</' + tag + '>').encode()
                raw = RAW.replace(b'</article>', addition + b'</article>')
                self.rejected(lambda: assembly.transform_page(raw, page='core/theory/09_scba.html',
                    binding=BINDING, expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING)),
                    'inline_style')

    def test_pinned_article_toggle_becomes_native_button_without_javascript_url(self):
        toggle = (b'<a id="documenter-article-toggle-button" '
                  b'class="docs-article-toggle-button fa-solid fa-chevron-up" '
                  b'href="javascript:;" title="Collapse all docstrings"></a>')
        raw = RAW.replace(b'</article>', toggle + b'</article>')
        result = assembly.transform_page(raw, page='core/theory/09_scba.html',
            binding=BINDING, expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING))
        self.assertIn(b'<button id="documenter-article-toggle-button"', result['html'])
        self.assertIn(b'class="docs-article-toggle-button fa-solid fa-chevron-up"', result['html'])
        self.assertIn(b'title="Collapse all docstrings" type="button"></button>', result['html'])
        self.assertNotIn(b'javascript:', result['html'])
        parser = assembly._PayloadHTML('core/theory/09_scba.html')
        parser.feed(result['html'].decode())
        parser.close()

    def test_article_toggle_adapter_rejects_unknown_shapes_and_preserves_url_veto(self):
        toggle = (b'<a id="documenter-article-toggle-button" '
                  b'class="docs-article-toggle-button fa-solid fa-chevron-up" '
                  b'href="javascript:;" title="Collapse all docstrings"></a>')
        variants = (toggle.replace(b'fa-chevron-up', b'fa-chevron-down'),
                    toggle.replace(b'javascript:;', b'javascript:sentinel()'),
                    toggle.replace(b'javascript:;', b'#'),
                    toggle.replace(b'title=', b'data-extra="x" title='),
                    toggle.replace(b'></a>', b'>unexpected</a>'),
                    toggle.replace(b'<a ', b'<p ').replace(b'</a>', b'</p>'))
        for addition in variants:
            with self.subTest(addition=addition):
                raw = RAW.replace(b'</article>', addition + b'</article>')
                self.rejected(lambda: assembly.transform_page(raw, page='core/theory/09_scba.html',
                    binding=BINDING, expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING)),
                    'unsupported_generated_shape')
        raw = RAW.replace(b'</article>', b'<a href="javascript:;">other</a></article>')
        result = assembly.transform_page(raw, page='core/theory/09_scba.html',
            binding=BINDING, expected_sha256=digest(raw), math_mapping=copy.deepcopy(MATH_MAPPING))
        parser = assembly._PayloadHTML('core/theory/09_scba.html')
        self.rejected(lambda: parser.feed(result['html'].decode()), 'external_resource')

    def test_runtime_csp_residue_and_theme_alternatives_are_rejected(self):
        cases = [
            ("index.html", b'<script src="https://cdn.example/x.js"></script>', "external_resource"),
            ("index.html", b'<script>alert(1)</script>', "inline_script"),
            ("index.html", b'<p onclick="alert(1)">x</p>', "inline_event"),
            ("index.html", b'<p style="color:red">x</p>', "inline_style"),
            ("assets/a.js", b'new Worker(URL.createObjectURL(new Blob(["x"])));', "dynamic_loader"),
            ("assets/a.js", b'importScripts("https://cdn.example/x.js");', "external_resource"),
            ("assets/a.js", b'localStorage.getItem("documenter-theme");', "theme_alternative"),
            ("assets/a.css", b'@media (prefers-color-scheme:dark){body{background:black}}', "theme_alternative"),
            ("index.html", b'<select id="documenter-themepicker"><option>Dark</option></select>', "theme_alternative"),
        ]
        for path, content, reason in cases:
            with self.subTest(path=path, content=content):
                files = {"index.html": b'<p>Light</p>', path: content}
                self.rejected(lambda: assembly.validate_payload(files), reason)
        assembly.validate_payload({"index.html": b'<link rel="stylesheet" href="assets/light.css">',
                                   "assets/light.css": b':root{color-scheme:light}body{background:#fff;color:#111}'})

    def test_private_files_paths_maps_symlinks_are_never_public_payload(self):
        for path in (".git/config", ".aws/credentials", "assets/x.js.map", "logs/stdout.txt",
                     "depot/packages/x.jl", "results/data.h5", "../escape.txt", "/tmp/private.txt"):
            with self.subTest(path=path):
                self.rejected(lambda: assembly.validate_payload({"index.html": b"ok", path: b"x"}),
                              "public_allowlist")
        self.rejected(lambda: assembly.validate_payload({"index.html": b'<p>/home/operator/private/run</p>'}),
                      "private_content")
        self.rejected(lambda: assembly.validate_payload({"index.html": b"ok"}, symlinks={"assets/font.woff2"}),
                      "public_allowlist")

    def test_missing_pin_license_or_wrong_hash_cannot_admit_assets(self):
        payload = b"literal synthetic asset"
        notice = b"SYNTHETIC TEST LICENSE; no real font license claim"
        entry = {"id": "fixture", "family": "fixture", "version": "1", "source_uri": "https://example.org/fixture",
                 "distribution_sha256": digest(payload), "files": [{"source_path": "a.css",
                 "destination": "assets/a.css", "bytes": len(payload), "sha256": digest(payload), "media_type": "text/css"}],
                 "license": {"spdx": "LicenseRef-Test", "text_file": "NOTICE.txt",
                 "text_sha256": digest(notice), "copyright": "Test fixture"}, "dependencies": []}
        inputs = {"a.css": payload, "NOTICE.txt": notice}
        assembly.validate_asset_entry(entry, inputs)
        for mutation, reason in (("missing", "missing_pin"), ("changed", "asset_hash_mismatch"),
                                 ("license", "missing_license")):
            supplied = dict(inputs)
            if mutation == "missing": del supplied["a.css"]
            if mutation == "changed": supplied["a.css"] += b"!"
            if mutation == "license": del supplied["NOTICE.txt"]
            self.rejected(lambda: assembly.validate_asset_entry(entry, supplied), reason)

    def test_font_license_policy_accepts_matching_private_fixture_and_rejects_only_mit_attribution(self):
        # These bytes are private validator fixtures, not real fonts or admitted OFL artifacts.
        payload = b"SYNTHETIC PRIVATE WOFF2 FIXTURE"
        notice = b"SYNTHETIC PRIVATE OFL-1.1 POLICY NOTICE; NOT A PUBLIC LICENSE ARTIFACT"
        entry = {"id": "fixture-font", "family": "katex-fonts", "version": "0.16.8",
                 "source_uri": "https://example.org/private-font-fixture",
                 "distribution_sha256": digest(payload), "files": [{
                     "source_path": "font.woff2", "destination": "assets/fonts/font.woff2",
                     "bytes": len(payload), "sha256": digest(payload), "media_type": "font/woff2"}],
                 "license": {"spdx": "OFL-1.1", "text_file": "OFL-NOTICE.txt",
                             "text_sha256": digest(notice), "copyright": "Synthetic test fixture"},
                 "dependencies": []}
        inputs = {"font.woff2": payload, "OFL-NOTICE.txt": notice}
        assembly.validate_asset_entry(entry, inputs)
        mit = copy.deepcopy(entry)
        mit["license"]["spdx"] = "MIT"
        self.rejected(lambda: assembly.validate_asset_entry(mit, inputs), "font_license_mismatch")
        self.rejected(lambda: assembly.validate_asset_entry(entry, {"font.woff2": payload}),
                      "missing_license")
        self.rejected(lambda: assembly.validate_asset_entry(
            entry, {"font.woff2": payload, "OFL-NOTICE.txt": notice + b" changed"}),
            "license_hash_mismatch")

    def test_missing_doc03_schema_blocks_serialization_but_empty_catalog_is_valid(self):
        result = assembly.prepare_catalog(fragments=[], coverage=[], shared_schema=None)
        self.assertEqual(result["fragments"], [])
        self.assertEqual(result["coverage"], [])
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "missing_shared_schema")
        self.assertIsNone(result["bundle_bytes"])
        self.assertNotIn("origins", result)


if __name__ == "__main__":
    unittest.main()
