"""Pinned Documenter 1.17 offline runtime and retained asset-byte adapter.

Pure functions only: no fetch, process execution, installation or publication.
Prepared input names are portable relative paths from assets.lock.json. Missing
pins or authoritative licenses block the whole candidate, never become a skip.
"""
from __future__ import annotations

import hashlib
import io
import tarfile
import textwrap
import json
from pathlib import Path, PurePosixPath
import re

SNIPPETS = ("collapse.js", "copy.js", "footnote.js", "headroom.js", "metadata.js",
            "search.js", "shortcut.js", "sidebar.js")
_LOCK = Path(__file__).with_name("assets.lock.json")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    if not isinstance(path, str) or not path or "\\" in path or not re.fullmatch(r"[A-Za-z0-9_.@/-]+", path):
        raise ValueError("asset_path")
    if path.startswith("/") or any(p in {"", ".", ".."} for p in path.split("/")):
        raise ValueError("asset_path")
    return path


def load_lock():
    return json.loads(_LOCK.read_bytes())


def pinned_source(name, data):
    if name not in SNIPPETS or not isinstance(data, bytes):
        raise ValueError("asset_hash_mismatch")
    key = "documenter/assets/html/js/" + name
    entry = next(x for x in load_lock()["files"] if x["source_path"] == key)
    if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
        raise ValueError("asset_hash_mismatch: " + name)
    return data.decode("utf-8")


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("pinned_runtime_shape")
    return text.replace(old, new, 1)


def local_url(value):
    # Page-relative URLs can climb from nested pages; caller's HTML/resource
    # closure resolves them against the actual page and forbids root escape.
    if not isinstance(value, str) or not re.fullmatch(r"(?:\.\./)*[A-Za-z0-9_][A-Za-z0-9_./-]*", value):
        raise ValueError("asset_path")
    relative(value.lstrip("./"))
    return value


def build_runtime(snippets, *, worker_url="assets/search-worker.js", asset_prefix="assets/vendor"):
    """Generate one page-relative runtime, plus the shared assets-relative worker.

    Worker URL and AMD paths are literals. Producer must select their relative
    values for each HTML depth, retaining every generated file in its asset map.
    Query protocol and MiniSearch implementation remain upstream's exact code.
    """
    local_url(worker_url)
    local_url(asset_prefix)
    source = {name: pinned_source(name, snippets[name]) for name in SNIPPETS}
    text = source["search.js"]
    start = text.index("function worker_function(")
    end = text.index("/////// SEARCH MAIN ///////")
    worker = text[start:end]
    worker = replace_once(worker,
        'importScripts(\n    "https://cdn.jsdelivr.net/npm/minisearch@__MINISEARCH_VERSION__/dist/umd/index.min.js",\n  );',
        'importScripts("vendor/minisearch/6.1.0/index.min.js");')
    worker = replace_once(worker,
        'class="has-text-left"\n            style="font-size: smaller;"',
        'class="has-text-left qcl-search-small"')
    worker += '''\nself.onmessage = function (event) {
  const value = event.data;
  if (!value || value.type !== "qcl-init" || !Array.isArray(value.docs) ||
      typeof value.base !== "string" || !Array.isArray(value.filters)) {
    throw new Error("invalid search initialization");
  }
  // worker_function installs the original query handler exactly once. Messages
  // already queued by the main thread run only after this initialization ends.
  worker_function(value.docs, value.base, value.filters);
};
'''
    main = text[end:]
    begin = main.index("  const worker_str =")
    finish = main.index("\n", main.index("  const worker = new Worker(URL.createObjectURL(worker_blob));", begin))
    main = main[:begin] + '  const worker = new Worker(' + json.dumps(worker_url) + ');\n' + '''  worker.postMessage({type: "qcl-init", docs: documenterSearchIndex["docs"],
    base: documenterBaseURL, filters});''' + main[finish:]
    source["search.js"] = main
    source["copy.js"] = replace_once(source["copy.js"],
        'el.style.position = "fixed";\n        el.style.opacity = 0;',
        'el.classList.add("qcl-copy-fallback");')
    paths = {name: asset_prefix + "/" + value.split("assets/vendor/", 1)[1][:-3]
             for name, value in load_lock()["runtime_dependencies"].items()
             if name not in {"requirejs", "minisearch"}}
    # RequireJS data-main infers a base directory from the runtime script URL.
    # These pinned paths are relative to the actual HTML document, so reset that
    # inferred AMD base before any dependency request; Worker URLs stay literal.
    config = {"baseUrl": ".", "paths": paths, "shim": {
        "jqueryui": {"deps": ["jquery"]},
        "headroom-jquery": {"deps": ["jquery", "headroom"]},
        "highlight-julia": {"deps": ["highlight"]},
        "highlight-julia-repl": {"deps": ["highlight"]}}}
    output = '/* Documenter1.17.0 pinned offline adapter; MIT notices retained. */\n'
    output += 'require.config(' + json.dumps(config, sort_keys=True, separators=(",", ":")) + ');\n'
    for name in SNIPPETS:
        if name == "headroom.js":
            deps, args = ["jquery", "headroom", "headroom-jquery"], "$ ,Headroom"
        elif name == "copy.js":
            deps, args = [], ""
        else:
            deps, args = ["jquery"], "$"
        output += 'require(' + json.dumps(deps) + ',function(' + args + '){\n' + source[name] + '\n});\n'
    output += 'require(["jquery","highlight","highlight-julia","highlight-julia-repl"],function($){$(document).ready(function(){hljs.highlightAll();});});\n'
    return {"assets/documenter.js": output.encode(), "assets/search-worker.js": worker.encode(),
            "assets/qcl-runtime.css": b".qcl-search-small{font-size:smaller}.qcl-copy-fallback{position:fixed;opacity:0}\n"}


def _open_distributions(inputs, lock):
    distributions = {}
    for distribution in lock.get("distributions", []):
        key = relative(distribution["input"])
        raw = inputs.get(key)
        if not isinstance(raw, bytes):
            raise ValueError("missing_asset_input: " + key)
        if len(raw) != distribution["bytes"] or digest(raw) != distribution["sha256"]:
            raise ValueError("distribution_hash_mismatch: " + key)
        archive = tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz")
        members = archive.getmembers()
        if len(members) > 10000 or sum(m.size for m in members) > 64 * 1024 * 1024:
            raise ValueError("asset_distribution_limit")
        for member in members:
            relative(member.name.rstrip("/"))
            if not (member.isfile() or member.isdir()) or member.size > 16 * 1024 * 1024:
                raise ValueError("asset_distribution_shape")
        package = archive.extractfile("package/package.json")
        if package is None or json.load(package).get("version") != distribution["version"]:
            raise ValueError("asset_version_mismatch")
        distributions[distribution["id"]] = archive
    return distributions


def extract_inputs(inputs, lock):
    """Materialize only lock-listed regular archive members into a byte map.

    No writes/imports/processes. Exact hashes are checked before tar parsing;
    prepared direct source/metadata inputs remain mandatory. This permits the
    producer to stage build-only katex.mjs and snippets without another unpacker.
    """
    result = dict(inputs)
    archives = _open_distributions(inputs, lock)
    try:
        for entry in lock["files"]:
            if "distribution" not in entry:
                continue
            archive = archives.get(entry["distribution"])
            if archive is None:
                raise ValueError("missing_asset_distribution")
            member = archive.getmember(relative(entry["member"]))
            if not member.isfile():
                raise ValueError("asset_distribution_shape")
            raw = archive.extractfile(member).read()
            key = relative(entry["source_path"])
            if key in result and result[key] != raw:
                raise ValueError("distribution_member_mismatch")
            result[key] = raw
    finally:
        for archive in archives.values():
            archive.close()
    verify_inputs(result, lock)
    return result


def verify_inputs(inputs, lock):
    if not isinstance(inputs, dict) or not isinstance(lock, dict) or lock.get("format") != "qcl-docs-assets-v1":
        raise ValueError("asset_shape")
    verified = {}
    for metadata in lock.get("retained_metadata", []):
        key = relative(metadata["input"])
        raw = inputs.get(key)
        if not isinstance(raw, bytes):
            raise ValueError("missing_asset_input: " + key)
        if len(raw) != metadata["bytes"] or digest(raw) != metadata["sha256"]:
            raise ValueError("asset_metadata_hash_mismatch")
    distributions = _open_distributions(inputs, lock)
    sources, destinations = set(), set()
    for entry in lock["files"]:
        source = relative(entry["source_path"])
        destination = entry["destination"]
        if source in sources:
            raise ValueError("asset_shape: duplicate source")
        sources.add(source)
        if source not in inputs:
            raise ValueError("missing_asset_input: " + source)
        data = inputs[source]
        if not isinstance(data, bytes) or len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError("asset_hash_mismatch: " + source)
        if "upstream_tree_input" in entry:
            tree = json.loads(inputs[relative(entry["upstream_tree_input"])])
            upstream = {item["path"]: item["sha"] for item in tree["tree"] if item["type"] == "blob"}
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if upstream.get(entry["upstream_tree_path"]) != entry["upstream_blob_sha1"] or blob != entry["upstream_blob_sha1"]:
                raise ValueError("asset_upstream_tree_mismatch")
        if "distribution" in entry:
            archive = distributions.get(entry["distribution"])
            if archive is None:
                raise ValueError("missing_asset_distribution")
            member = archive.getmember(relative(entry["member"]))
            if not member.isfile() or archive.extractfile(member).read() != data:
                raise ValueError("distribution_member_mismatch")
        if destination is not None:
            relative(destination)
            if destination in destinations:
                raise ValueError("asset_shape: duplicate destination")
            destinations.add(destination)
            verified[destination] = data
    for license in lock["generated_licenses"]:
        destination = relative(license["destination"])
        data = license["text"].encode()
        if digest(data) != license["sha256"] or destination in destinations:
            raise ValueError("license_hash_mismatch")
        destinations.add(destination)
        verified[destination] = data
    package = json.loads(inputs["responses/lato-upstream-package"])
    if package.get("version") != "3.0.0" or package.get("license") != "(MIT AND OFL-1.1)":
        raise ValueError("asset_version_mismatch")
    readme = inputs["responses/lato-upstream-readme"].decode("utf-8")
    code = textwrap.dedent(readme.split("### Library\n\n", 1)[1].split("\n### Font", 1)[0]).strip() + "\n"
    if verified.get("assets/licenses/lato-code.txt") != code.encode():
        raise ValueError("license_hash_mismatch")
    # Retain the independently extracted primary font evidence and link every
    # TTF to the published triplet. The standard OFL body supplies no attribution.
    evidence = json.loads(inputs["licenses/katex-font-primary-evidence.json"])
    body = inputs["licenses/ofl-standard-body.txt"]
    font_records = evidence.get("fonts", [])
    ttf_inputs = {PurePosixPath(e["source_path"]).name: e["sha256"] for e in lock["files"]
                  if e["source_path"].startswith("katex/dist/fonts/") and e["source_path"].endswith(".ttf")}
    if len(font_records) != 20 or len(ttf_inputs) != 20:
        raise ValueError("font_license_evidence_mismatch")
    notice = "KaTeX 0.16.8 font notices, transcribed from pinned font sfnt name IDs 0/13/14.\n\n"
    seen_fonts = set()
    for font in font_records:
        name = PurePosixPath(font["path"]).name
        names = font["names"]
        if name in seen_fonts or ttf_inputs.get(name) != font["sha256"] or {n["name_id"] for n in names} != {0, 13, 14}:
            raise ValueError("font_license_evidence_mismatch")
        seen_fonts.add(name)
        notice += name + " (TTF SHA256 " + font["sha256"] + ")\n"
        notice += "\n".join(n["text"] for n in names) + "\n\n"
    notice += body.decode("utf-8")
    if verified.get("assets/licenses/katex-fonts.txt") != notice.encode():
        raise ValueError("font_license_evidence_mismatch")
    lato = json.loads(inputs["licenses/lato-font-primary-evidence.json"])
    if len(lato.get("fonts", [])) != 18:
        raise ValueError("font_license_evidence_mismatch")
    notice = "Lato font notices from pinned 3.0.0 distribution WOFF sfnt name IDs 0/5/13/14 (font version is independent of distribution version).\n\n"
    seen_fonts = set()
    for font in lato["fonts"]:
        key = relative(font["input"])
        if key in seen_fonts or key not in inputs or digest(inputs[key]) != font["sha256"] or {n["name_id"] for n in font["names"]} != {0, 5, 13, 14}:
            raise ValueError("font_license_evidence_mismatch")
        seen_fonts.add(key)
        notice += font["source_uri"].rsplit("/", 1)[-1] + " (WOFF SHA256 " + font["sha256"] + ")\n"
        notice += "\n".join(str(n["name_id"]) + ": " + n["text"] for n in font["names"]) + "\n\n"
    notice += body.decode("utf-8")
    if verified.get("assets/licenses/lato-fonts.txt") != notice.encode():
        raise ValueError("font_license_evidence_mismatch")
    for archive in distributions.values():
        archive.close()
    for entry in lock["files"]:
        license = lock["licenses"].get(entry["license"])
        if not license or not license.get("spdx"):
            raise ValueError("missing_license")
        if PurePosixPath(entry["source_path"]).suffix in {".ttf", ".woff", ".woff2"} and license["spdx"] != "OFL-1.1":
            raise ValueError("font_license_mismatch")
        paths = license.get("text_files", [license.get("text_file")])
        if any(path not in verified for path in paths):
            raise ValueError("missing_license: " + entry["license"])
    if any(path not in verified for path in lock["runtime_dependencies"].values()):
        raise ValueError("missing_asset_input: runtime dependency")
    if any(path not in verified for path in lock["resource_map"].values()):
        raise ValueError("missing_asset_input: mapped resource")
    # Explicitly incomplete intermediate inventory cannot admit a publication.
    if lock.get("missing_inputs") or lock.get("closure_status") != "complete":
        raise ValueError("missing_asset_input: pinned distribution/license closure incomplete")
    return verified


def validate_assets(lock_bytes, inputs, *, payload):
    """AS1 adapter: bind the selected source lock, not caller-supplied ready flags.

    Returning this exact destination map is only the assets portion of AS1.
    Existing payload/C1/C2 checks and independent source review still apply.
    """
    if not isinstance(lock_bytes, bytes) or lock_bytes != _LOCK.read_bytes():
        raise ValueError("asset_lock_mismatch")
    lock = json.loads(lock_bytes)
    verified = verify_inputs(inputs, lock)
    raw_contexts = inputs.get("runtime-contexts.json")
    if not isinstance(raw_contexts, bytes) or len(raw_contexts) > 1048576:
        raise ValueError("missing_asset_input: runtime-contexts.json")
    contexts = json.loads(raw_contexts)
    if not isinstance(contexts, list) or not 1 <= len(contexts) <= 1024:
        raise ValueError("asset_shape")
    snippets = {name: inputs["documenter/assets/html/js/" + name] for name in SNIPPETS}
    seen = set()
    for context in contexts:
        if not isinstance(context, dict) or set(context) != {"destination", "worker_url", "asset_prefix"}:
            raise ValueError("asset_shape")
        destination = relative(context["destination"])
        if not destination.startswith("assets/") or not destination.endswith(".js") or destination in verified or destination in seen:
            raise ValueError("asset_shape")
        seen.add(destination)
        generated = build_runtime(snippets, worker_url=context["worker_url"], asset_prefix=context["asset_prefix"])
        verified[destination] = generated.pop("assets/documenter.js")
        for path, data in generated.items():
            if path in verified and verified[path] != data:
                raise ValueError("asset_shape")
            verified[path] = data
    for path, data in verified.items():
        if payload.get(path) != data:
            raise ValueError("asset_payload_mismatch: " + path)
    return verified
