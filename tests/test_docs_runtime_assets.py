"""Source fixtures; run only in the separately admitted finite packet."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("runtime_assets", Path(__file__).resolve().parents[1] / "ops/docs/runtime-assets.py")
assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assets)

class RuntimeAssets(unittest.TestCase):
    def test_missing_prepared_inputs_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "missing_asset_input"):
            assets.verify_inputs({}, assets.load_lock())

    def test_changed_source_fails_before_transform(self):
        with self.assertRaisesRegex(ValueError, "asset_hash_mismatch"):
            assets.pinned_source("search.js", b"SENTINEL")

    def test_paths_cannot_escape_prepared_inputs(self):
        for value in ("../x", "/x", "a/../x", "a//b", "a\\b"):
            with self.assertRaises(ValueError):
                assets.relative(value)

    def test_runtime_retains_search_protocol_without_blob(self):
        import os
        root = Path(os.environ["DOC04_DOCUMENTER_ROOT"])
        snippets = {name: (root / "assets/html/js" / name).read_bytes() for name in assets.SNIPPETS}
        result = assets.build_runtime(snippets)
        self.assertNotIn(b"new Blob", result["assets/documenter.js"])
        self.assertNotIn(b"createObjectURL", result["assets/documenter.js"])
        self.assertNotIn(b"https://cdn", result["assets/search-worker.js"])
        self.assertIn(b"index.search(query", result["assets/search-worker.js"])
        self.assertIn(b"qcl-init", result["assets/documenter.js"])
        self.assertIn(b"importScripts(\"vendor/minisearch/6.1.0/index.min.js\")", result["assets/search-worker.js"])

    def test_literal_worker_url_accepts_page_depth_but_rejects_remote_targets(self):
        import os
        root = Path(os.environ["DOC04_DOCUMENTER_ROOT"])
        snippets = {name: (root / "assets/html/js" / name).read_bytes() for name in assets.SNIPPETS}
        result = assets.build_runtime(snippets, worker_url="../../assets/search-worker.js", asset_prefix="../../assets/vendor")
        self.assertIn(b'new Worker("../../assets/search-worker.js")', result["assets/documenter.js"])
        for value in ("https://host/worker.js", "//host/worker.js", "data:text/javascript,x", "blob:x", "a/../b"):
            with self.assertRaises(ValueError):
                assets.build_runtime(snippets, worker_url=value)

    def test_complete_prepared_inventory_is_required_and_exact(self):
        import os
        import json
        import copy
        source_map = json.loads(Path(os.environ["DOC04_ASSET_INPUTS_JSON"]).read_bytes())
        inputs = {name: Path(path).read_bytes() for name, path in source_map.items()}
        lock = assets.load_lock()
        self.assertEqual(lock["closure_status"], "complete")
        self.assertEqual(lock["missing_inputs"], [])
        result = assets.verify_inputs(inputs, lock)
        self.assertIn("assets/licenses/katex-fonts.txt", result)
        archive_only = {key: value for key, value in inputs.items()
                        if key not in {entry["source_path"] for entry in lock["files"] if "distribution" in entry}}
        recovered = assets.extract_inputs(archive_only, lock)
        for entry in lock["files"]:
            self.assertEqual(recovered[entry["source_path"]], inputs[entry["source_path"]])
        for entry in lock["files"]:
            if entry["destination"]:
                self.assertEqual(result[entry["destination"]], inputs[entry["source_path"]])
        changed = dict(inputs)
        key = lock["files"][0]["source_path"]
        changed[key] = changed[key] + b" "
        with self.assertRaisesRegex(ValueError, "asset_hash_mismatch"):
            assets.verify_inputs(changed, lock)
        wrong_license = copy.deepcopy(lock)
        wrong_license["licenses"]["katex-ofl"]["spdx"] = "MIT"
        with self.assertRaisesRegex(ValueError, "font_license_mismatch"):
            assets.verify_inputs(inputs, wrong_license)

    def test_actual_worker_result_has_one_class_and_preserves_text_and_external_size(self):
        import json
        import os
        import shutil
        import subprocess
        from html.parser import HTMLParser

        class ResultDOM(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.nodes = []
                self.stack = []

            def handle_starttag(self, tag, attrs):
                node = {"tag": tag, "attrs": attrs, "text": ""}
                self.nodes.append(node)
                self.stack.append(node)

            def handle_endtag(self, tag):
                if self.stack and self.stack[-1]["tag"] == tag:
                    self.stack.pop()

            def handle_data(self, value):
                for node in self.stack:
                    node["text"] += value

        node = os.environ.get("DOC04_NODE") or shutil.which("node")
        self.assertTrue(node, "existing Node executable is mandatory for the actual worker DOM control")
        root = Path(os.environ["DOC04_DOCUMENTER_ROOT"])
        snippets = {name: (root / "assets/html/js" / name).read_bytes() for name in assets.SNIPPETS}
        generated = assets.build_runtime(snippets)
        input_map = json.loads(Path(os.environ["DOC04_ASSET_INPUTS_JSON"]).read_bytes())
        mini = Path(input_map["responses/minisearch-min"]).read_bytes()
        pin = next(entry for entry in assets.load_lock()["files"] if entry["source_path"] == "responses/minisearch-min")
        self.assertEqual(assets.digest(mini), pin["sha256"])
        # One tiny in-memory worker/MiniSearch query. Parent packet supervisor
        # owns aggregate resources; this child has its own finite 5-second cap.
        script = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const input = JSON.parse(fs.readFileSync(0, "utf8"));
const messages = [];
const context = vm.createContext({postMessage: value => messages.push(value)});
context.self = context;
context.importScripts = path => {
  if (path !== "vendor/minisearch/6.1.0/index.min.js") throw Error("unexpected worker import");
  vm.runInContext(input.mini, context, {timeout: 1000});
};
vm.runInContext(input.worker, context, {timeout: 1000});
context.onmessage({data: {type: "qcl-init", base: "..", filters: ["page"], docs: [{
  location: "theory/transport.html", page: "Transport manual",
  title: "Quantum transport", category: "page", text: "Quantum transport evidence"
}]}});
context.onmessage({data: "transport"});
process.stdout.write(JSON.stringify(messages));
"""
        completed = subprocess.run([node, "-e", script],
            input=json.dumps({"worker": generated["assets/search-worker.js"].decode(), "mini": mini.decode()}),
            text=True, capture_output=True, timeout=5, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        messages = json.loads(completed.stdout)
        self.assertEqual(len(messages), 1)
        self.assertEqual(len(messages[0]), 1)
        parser = ResultDOM()
        parser.feed(messages[0][0]["div"])
        matches = [entry for entry in parser.nodes if entry["tag"] == "div" and
                   ("title", "theory/transport.html") in entry["attrs"]]
        self.assertEqual(len(matches), 1)
        target = matches[0]
        classes = [value for name, value in target["attrs"] if name == "class"]
        self.assertEqual(len(classes), 1, "browser DOM must receive a single class attribute")
        self.assertEqual(set(classes[0].split()), {"has-text-left", "qcl-search-small"})
        self.assertFalse(any(name == "style" for name, _ in target["attrs"]))
        self.assertIn("theory/transport.html (Transport manual)", target["text"])
        self.assertIn(b".qcl-search-small{font-size:smaller}", generated["assets/qcl-runtime.css"])

    def test_actual_worker_preserves_cyrillic_search_and_julia_symbols(self):
        import json
        import os
        import shutil
        import subprocess

        node = os.environ.get("DOC04_NODE") or shutil.which("node")
        self.assertTrue(node, "existing Node executable required")
        root = Path(os.environ["DOC04_DOCUMENTER_ROOT"])
        snippets = {name: (root / "assets/html/js" / name).read_bytes() for name in assets.SNIPPETS}
        worker = assets.build_runtime(snippets)["assets/search-worker.js"].decode()
        inputs = json.loads(Path(os.environ["DOC04_ASSET_INPUTS_JSON"]).read_bytes())
        mini = Path(inputs["responses/minisearch-min"]).read_bytes()
        pin = next(x for x in assets.load_lock()["files"] if x["source_path"] == "responses/minisearch-min")
        self.assertEqual(assets.digest(mini), pin["sha256"])
        script = r"""
const fs = require("node:fs"), vm = require("node:vm");
const input = JSON.parse(fs.readFileSync(0, "utf8")), messages = [];
const context = vm.createContext({postMessage: x => messages.push(x)});
context.self = context;
context.importScripts = path => {
  if (path !== "vendor/minisearch/6.1.0/index.min.js") throw Error("unexpected import");
  vm.runInContext(input.mini, context, {timeout: 1000});
};
vm.runInContext(input.worker, context, {timeout: 1000});
context.onmessage({data: {type: "qcl-init", base: "..", filters: ["section"], docs: [
  {location: "theory/scba.html", page: "Теория", category: "section",
   title: "Самосогласованное НЕВЯЗКА учёт ёмкости", text: "Борновское приближение."},
  {location: "api/public.html", page: "Public API", category: "section",
   title: "solve_scba Base.sort! @time α₂", text: "Julia operators"}
]}});
for (const query of input.queries) context.onmessage({data: query});
process.stdout.write(JSON.stringify(messages.map(rows => rows.map(x => x.div))));
"""
        queries = ["Самосогласованное", "самосогласованное", "НЕВЯЗКА", "учёт", "ёмкости",
                   "solve_scba", "Base.sort!", "@time", "α₂", "zzzzmissingzzzz"]
        completed = subprocess.run([node, "-e", script], input=json.dumps({
            "worker": worker, "mini": mini.decode(), "queries": queries}),
            text=True, capture_output=True, timeout=5, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        results = json.loads(completed.stdout)
        self.assertEqual(len(results), len(queries))
        for query, rows in zip(queries[:-1], results[:-1], strict=True):
            with self.subTest(query=query):
                self.assertTrue(rows, "actual worker discarded the query")
                expected = "theory/scba.html" if query in queries[:5] else "api/public.html"
                self.assertTrue(any(expected in row for row in rows))
        self.assertEqual(results[-1], [])
