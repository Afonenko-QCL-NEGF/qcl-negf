"""Bounded DOC04 presentation adapters; no processes, imports of owning packages,
network, publication, or writes. Returned HTML is an intermediate until math,
asset/license, shared-schema and BUILD gates independently admit a final bundle.
"""
from collections import defaultdict
import copy
import hashlib
from html import escape, unescape
from html.parser import HTMLParser
import json
from pathlib import PurePosixPath
import posixpath
import re
from urllib.parse import unquote, urljoin, urlsplit


class DocsError(ValueError):
    def __init__(self, code, detail=""):
        self.code = code
        super().__init__(f"{code}: {detail}" if detail else code)


def _fail(code, detail=""):
    raise DocsError(code, detail)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


BINDING = {"documenter_version": "1.17.0",
           "documenter_tree_sha1": "56e9c37b5e7c3b4f080ab1da18d72d5c290e184a",
           "policy": "documenter-1.17-light-self-v1"}
PRIMARY = {
    "researcher": ("core", "core", ["components/QCLNEGF.jl/docs/src/theory/09_scba.md"],
                   ["core/theory/09_scba.html#researcher-scba-route"]),
    "developer": ("runner", "runner", ["components/QCLNEGFRunner.jl/docs/src/api/public.md",
                  "components/QCLNEGFRunner.jl/docs/src/user/configuration.md"],
                  ["runner/api/public.html#reader-api-routes",
                   "runner/user/configuration.html#developer-configuration-route"]),
    "operator": ("root", "operator", ["docs/public/operator-recovery.md"],
                 ["operator/recovery.html#operator-recovery"]),
}
ANCHORS = {"researcher-scba-route", "researcher-final-route", "reader-api-routes",
           "developer-configuration-route", "operator-recovery-route", "operator-recovery"}
PLAN_LIMITS = {"files": 10000, "total_bytes": 268435456, "file_bytes": 16777216,
               "manifest_bytes": 2097152, "fragment_bytes": 32768, "help_view_bytes": 65536,
               "tex_bytes": 16384, "math_batch_bytes": 4194304, "math_records": 10000,
               "math_markup_bytes": 262144, "math_total_markup_bytes": 33554432,
               "math_css_bytes": 1048576, "math_style_groups": 20000, "math_batch_wall_seconds": 60}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
PRIVATE = re.compile(r"(?:/(?:home|Users|tmp|root)/|/nix/store/|(?:AKIA|ASIA)[A-Z0-9]{16}|"
                     r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|"
                     r"\b(?:password|access_token|secret_key)\s*[:=]\s*[^\s<]+)", re.I)
THEME = re.compile(r"documenter-(?:theme|dark)|catppuccin|themeswap|themepicker|"
                   r"prefers-color-scheme|matchMedia\s*\([^)]*color-scheme|"
                   r"color-scheme\s*:\s*(?:dark|light\s+dark)|theme--|docs-dark-only|"
                   r"documenter-settings", re.I)
FIXED_LIGHT = (b":root{color-scheme:light;}body,.docs-main,.docs-sidebar,.docs-navbar{"
               b"background:#fff;color:#17212b;}a{color:#075ca8;}"
               b"input,select,textarea,button,dialog{color:#17212b;background:#fff;}"
               b":focus-visible{outline:2px solid #075ca8;outline-offset:2px;}"
               b"[role=alert],.admonition.is-danger{background:#fff2f2;color:#721515;}"
               b"[aria-busy=true],.docs-search-results{background:#fff;color:#17212b;}\n")


def _relative(path, code="public_allowlist"):
    if not isinstance(path, str) or not path or len(path) > 2048:
        _fail(code, "invalid path")
    decoded = unquote(path)
    if decoded != path or "\\" in path or any(ord(c) < 32 for c in path):
        _fail(code, path)
    parts = PurePosixPath(path).parts
    if path.startswith("/") or any(p in (".", "..") or p.startswith(".") for p in parts):
        _fail(code, path)
    if posixpath.normpath(path) != path or "//" in path:
        _fail(code, path)
    return path


def _object(value, fields, code):
    if not isinstance(value, dict) or set(value) != set(fields):
        _fail(code, "unexpected/missing fields")


def _decode(data):
    try:
        return data.decode("utf-8", errors="strict")
    except (UnicodeError, AttributeError):
        _fail("invalid_encoding")


def validate_source_binding(before, after):
    if before != after:
        _fail("source_graph_mismatch")
    if not isinstance(before, dict) or before.get("format") != "qcl-negf.git-graph.v1":
        _fail("source_graph_mismatch")
    _object(before, {"format", "revision", "components"}, "source_graph_mismatch")
    if not re.fullmatch(r"[a-f0-9]{40}", before["revision"]):
        _fail("source_graph_mismatch")
    seen = set()
    for item in before["components"]:
        _object(item, {"path", "revision", "url"}, "source_graph_mismatch")
        _relative(item["path"], "source_graph_mismatch")
        if item["path"] in seen or not item["path"].startswith("components/"):
            _fail("source_graph_mismatch")
        if not re.fullmatch(r"[a-f0-9]{40}", item["revision"]):
            _fail("source_graph_mismatch")
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", item["url"]):
            _fail("source_graph_mismatch")
        seen.add(item["path"])
    if not seen:
        _fail("source_graph_mismatch")


def validate_primary_sources(plan, available):
    slices = plan.get("slices", [])
    if not isinstance(slices, list) or len(slices) != 3:
        _fail("primary_mapping_mismatch")
    seen = set()
    for item in slices:
        identity = item.get("id")
        if identity not in PRIMARY or identity in seen:
            _fail("primary_mapping_mismatch")
        owner, section, sources, urls = PRIMARY[identity]
        if (item.get("owner"), item.get("section"), item.get("primary_sources"),
                item.get("primary_urls")) != (owner, section, sources, urls):
            _fail("primary_mapping_mismatch", identity)
        seen.add(identity)
    for _, _, sources, _ in PRIMARY.values():
        if not set(sources).issubset(available):
            _fail("missing_primary_source")


def _json_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("duplicate_json_key", key)
        result[key] = value
    return result


def load_pilot_plan(path):
    with open(path, "rb") as source:
        raw = source.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        _fail("plan_limit")
    try:
        plan = json.loads(_decode(raw), object_pairs_hook=_json_pairs)
    except (ValueError, TypeError) as error:
        if isinstance(error, DocsError):
            raise
        _fail("plan_shape")
    return _validate_pilot_plan(plan)


def _validate_pilot_plan(plan):
    """Shared in-memory plan contract; the file loader alone owns IO."""
    _object(plan, {"format", "profile", "slices", "support_policy", "source_inputs", "assets_lock",
                   "transform_policy", "public_prefix", "limits", "expected_primary_anchors"}, "plan_shape")
    if (plan["format"], plan["profile"], plan["support_policy"], plan["transform_policy"],
            plan["public_prefix"]) != ("qcl-negf.docs-pilot-plan.v1", "pilot-v1",
            "existing_owning_page_graphs", BINDING["policy"], "/docs"):
        _fail("plan_shape")
    if set(plan["expected_primary_anchors"]) != ANCHORS or len(plan["expected_primary_anchors"]) != len(ANCHORS):
        _fail("primary_mapping_mismatch")
    _object(plan["limits"], PLAN_LIMITS, "plan_shape")
    for key, maximum in PLAN_LIMITS.items():
        if type(plan["limits"][key]) is not int or not 0 < plan["limits"][key] <= maximum:
            _fail("plan_limit", key)
    if not isinstance(plan["source_inputs"], list) or len(plan["source_inputs"]) > 10000:
        _fail("plan_shape")
    for path in [*plan["source_inputs"], plan["assets_lock"]]:
        _relative(path, "plan_shape")
    for item in plan["slices"]:
        _object(item, {"id", "owner", "primary_sources", "section", "primary_urls"}, "plan_shape")
    validate_primary_sources(plan, {p for values in PRIMARY.values() for p in values[2]})
    return plan


def validate_authored_source(source):
    if not isinstance(source, str) or len(source.encode()) > 16 * 1024 * 1024:
        _fail("source_limit")
    # Inspect fence information strings, not occurrences in prose or literal code.
    fence = None
    for line in source.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if not match:
            continue
        marker, info = match.groups()
        if fence is not None:
            if marker[0] == fence[0] and len(marker) >= len(fence) and not info.strip():
                fence = None
            continue
        directive = info.strip().split(maxsplit=1)[0] if info.strip() else ""
        if directive in {"@example", "@eval", "@repl", "@setup", "jldoctest"}:
            _fail("executable_docs_directive", directive)
        if directive.startswith("@") and directive not in {"@meta", "@docs", "@autodocs", "@index", "@contents"}:
            _fail("unsupported_docs_directive", directive)
        fence = marker


class _Node:
    def __init__(self, tag, attrs=(), raw="", text=""):
        self.tag, self.attrs, self.raw, self.text = tag, list(attrs), raw, text
        self.children = []
        self.changed = False

    def attr(self):
        return dict(self.attrs)


class _Tree(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.root = _Node("#root")
        self.stack = [self.root]
        self.nodes = 0
        self.feed(text)
        self.close()
        if len(self.stack) != 1:
            _fail("unsupported_generated_shape", "unclosed element")

    def _start_node(self, tag, attrs, *, self_closing):
        self.nodes += 1
        if len(self.stack) > 512 or self.nodes > 100000:
            _fail("page_limit", "HTML depth/nodes")
        if len({k for k, _ in attrs}) != len(attrs):
            _fail("unsupported_generated_shape", "duplicate attribute")
        node = _Node(tag, attrs, self.get_starttag_text())
        self.stack[-1].children.append(node)
        if tag not in VOID and not self_closing:
            self.stack.append(node)

    def handle_starttag(self, tag, attrs):
        self._start_node(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._start_node(tag, attrs, self_closing=True)

    def handle_endtag(self, tag):
        if len(self.stack) < 2 or self.stack[-1].tag != tag:
            _fail("unsupported_generated_shape", "unbalanced element")
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(_Node("#text", text=data))

    def handle_entityref(self, name):
        self.handle_data("&" + name + ";")

    def handle_charref(self, name):
        self.handle_data("&#" + name + ";")

    def handle_decl(self, decl):
        if decl.lower() != "doctype html":
            _fail("unsupported_generated_shape", "declaration")
        self.stack[-1].children.append(_Node("#text", text="<!" + decl + ">"))

    def handle_comment(self, text):
        self.stack[-1].children.append(_Node("#text", text="<!--" + text + "-->"))


def _text(node):
    return unescape("".join(child.text for child in node.children if child.tag == "#text"))


def _serialize(node):
    if node.tag == "#root":
        return "".join(_serialize(c) for c in node.children)
    if node.tag == "#text":
        return node.text
    start = node.raw
    if node.changed:
        start = "<" + node.tag + "".join(" " + k + ("" if v is None else '="' + escape(v, quote=True) + '"')
                                         for k, v in node.attrs) + ">"
    closed = node.raw.rstrip().endswith("/>")
    if closed and node.changed:
        start = start[:-1] + "/>"
    return start + "".join(_serialize(c) for c in node.children) + ("" if node.tag in VOID or closed else "</" + node.tag + ">")


def transform_page(raw, *, page, binding, expected_sha256, math_mapping, resource_map=None):
    """Transform one known Documenter page, returning private intermediate data.

    resource_map is an exact admitted remote-resource -> relative local path map;
    absent pins fail closed. No assets are fetched or licensed by this function.
    """
    if binding != BINDING:
        _fail("generator_mismatch")
    if not isinstance(raw, bytes) or len(raw) > 16 * 1024 * 1024:
        _fail("page_limit")
    if _sha(raw) != expected_sha256:
        _fail("input_hash_mismatch")
    _relative(page)
    tree = _Tree(_decode(raw))
    generated, operations = {}, []
    config_count = light_count = 0
    resources = resource_map or {}
    mapping, observed = {}, []
    if not isinstance(math_mapping, list) or len(math_mapping) > 10000:
        _fail("math_mapping_mismatch")
    for record in math_mapping:
        _object(record, {"page", "selector", "tex", "tex_sha256", "display"}, "math_mapping_mismatch")
        if not isinstance(record["tex"], str) or len(record["tex"].encode()) > 16384:
            _fail("math_mapping_mismatch")
        if record["page"] != page or not re.fullmatch(r"#[A-Za-z][A-Za-z0-9_.:-]*", record["selector"]):
            _fail("math_mapping_mismatch")
        if type(record["display"]) is not bool or _sha(record["tex"].encode()) != record["tex_sha256"]:
            _fail("math_mapping_mismatch")
        if record["selector"] in mapping:
            _fail("math_mapping_mismatch")
        mapping[record["selector"]] = record

    def visit(parent):
        nonlocal config_count, light_count
        kept = []
        for node in parent.children:
            attrs = node.attr()
            classes = attrs.get("class", "").split()
            identity = attrs.get("id", "")
            remove = identity in {"documenter-settings", "documenter-settings-button", "documenter-version-selector"}
            remove = remove or "docs-dark-only" in classes
            if node.tag == "link" and "docs-theme-link" in classes:
                if attrs.get("data-theme-name") not in {"documenter-light", "documenter-dark", "catppuccin-latte",
                                                        "catppuccin-frappe", "catppuccin-macchiato", "catppuccin-mocha"}:
                    _fail("unsupported_generated_shape", "unknown theme")
                if attrs.get("data-theme-name") == "documenter-light":
                    light_count += 1
                else:
                    remove = True
            if node.tag == "script":
                source = attrs.get("src")
                if source:
                    if posixpath.basename(urlsplit(source).path) in {"themeswap.js", "themes.js", "versions.js", "siteinfo.js", "warner.js"}:
                        remove = True
                    elif urlsplit(source).scheme or source.startswith("//"):
                        if source not in resources:
                            _fail("missing_pin", source)
                        attrs["src"] = posixpath.relpath(_relative(resources[source]), posixpath.dirname(page))
                        node.attrs, node.changed = list(attrs.items()), True
                    elif not remove and posixpath.basename(urlsplit(source).path) not in {"search_index.js", "documenter.js"}:
                        if source not in resources:
                            _fail("unsupported_generated_shape", "unknown head script")
                        attrs["src"] = posixpath.relpath(_relative(resources[source]), posixpath.dirname(page))
                else:
                    # Exact pinned render_head assignment; only a path literal, no JS evaluation.
                    match = re.fullmatch(r'\s*documenterBaseURL="([A-Za-z0-9_./-]*)"\s*;?\s*', _text(node))
                    if not match or node.children and any(c.tag != "#text" for c in node.children):
                        _fail("unsupported_generated_shape", "unknown inline script")
                    config_count += 1
                    if config_count != 1:
                        _fail("unsupported_generated_shape", "duplicate page config")
                    value = match.group(1)
                    if value.startswith("/") or any(p not in {"..", "."} for p in value.split("/")):
                        _fail("unsupported_generated_shape", "base URL")
                    content = ('documenterBaseURL=' + json.dumps(value) + ';\n').encode()
                    destination = "assets/pages/" + _sha(page.encode() + b"\0" + raw) + ".js"
                    generated[destination] = content
                    node.attrs = [("src", posixpath.relpath(destination, posixpath.dirname(page)))]
                    node.children, node.changed = [], True
                    attrs = node.attr()
                    operations.append("externalize_page_config")
            if remove:
                operations.append("remove:" + (identity or attrs.get("src", attrs.get("data-theme-name", "dark-logo"))))
                continue
            if node.tag == "link" and attrs.get("href"):
                target = attrs["href"]
                if urlsplit(target).scheme or target.startswith("//"):
                    if target not in resources:
                        _fail("missing_pin", target)
                    attrs["href"] = posixpath.relpath(_relative(resources[target]), posixpath.dirname(page))
            filtered = [(k, v) for k, v in attrs.items() if k not in {"data-theme-primary-dark", "data-theme-primary", "data-theme-name"}]
            filtered = [(k, " ".join(c for c in v.split() if not c.startswith("theme--")))
                        if k == "class" else (k, v) for k, v in filtered]
            if filtered != node.attrs:
                node.attrs, node.changed = filtered, True
            if any(k.lower().startswith("on") for k, _ in node.attrs):
                _fail("inline_event")
            if "style" in node.attr() or node.tag == "style":
                _fail("inline_style")
            selector = "#" + identity
            if selector in mapping:
                record = mapping[selector]
                expected = ("\\[" + record["tex"] + "\\]") if record["display"] else "$" + record["tex"] + "$"
                if node.tag != ("p" if record["display"] else "span") or _text(node) != expected:
                    _fail("math_mapping_mismatch")
                if record["display"] and "math-container" not in classes:
                    _fail("math_mapping_mismatch")
                if any(child.tag != "#text" for child in node.children):
                    _fail("math_mapping_mismatch")
                observed.append(copy.deepcopy(record))
            elif node.tag == "p" and "math-container" in classes:
                _fail("math_mapping_mismatch", "unmapped display math")
            visit(node)
            if node.tag == "head":
                destination = "assets/runtime/qcl-fixed-light.css"
                generated[destination] = FIXED_LIGHT
                relative = posixpath.relpath(destination, posixpath.dirname(page))
                node.children.append(_Node("link", [("rel", "stylesheet"), ("href", relative)],
                                           '<link rel="stylesheet" href="' + escape(relative, quote=True) + '">'))
            kept.append(node)
        parent.children = kept

    visit(tree.root)
    if config_count != 1 or light_count != 1:
        _fail("unsupported_generated_shape", "required head cardinality")
    if len(observed) != len(mapping):
        _fail("math_mapping_mismatch")
    output = _serialize(tree.root).encode()
    if THEME.search(_decode(output)):
        _fail("theme_alternative")
    return {"html": output, "generated_files": generated, "math": observed,
            "input_sha256": _sha(raw), "output_sha256": _sha(output), "operations": operations}


def _resolve(base, value, *, article=False):
    if not isinstance(value, str) or len(value) > 4096 or "\\" in value:
        _fail("external_resource")
    value = unescape(value)
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if article and parsed.scheme in {"https", "http", "mailto"}:
            return None
        _fail("external_resource", value)
    if value.startswith("/") or parsed.query:
        _fail("external_resource", value)
    resolved = urlsplit(urljoin(base, value))
    path = resolved.path or base
    _relative(path)
    return path, unquote(resolved.fragment)


class _PayloadHTML(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page, self.ids, self.edges, self.scripts = page, set(), [], []
        self.in_script = False
        self.data_main = []
        self.svg_depth = 0
        self.svg_scopes = []
        self.nodes = 0

    def handle_starttag(self, tag, pairs):
        self.nodes += 1
        if self.nodes > 100000:
            _fail("payload_limit", "HTML node count")
        if len(dict(pairs)) != len(pairs):
            _fail("unsupported_generated_shape")
        attrs = dict(pairs)
        if tag == "svg":
            self.svg_depth += 1
            self.svg_scopes.append({"markers": set(), "references": set()})
        if self.svg_depth and tag not in {"svg", "g", "path", "line", "rect", "circle", "ellipse",
                                          "polyline", "polygon", "title", "desc", "defs", "marker", "text"}:
            _fail("unsupported_generated_shape", "unreviewed SVG vocabulary")
        if self.svg_depth and tag in {"marker", "text"}:
            common = {"id", "class", "x", "y", "fill", "stroke", "stroke-width", "stroke-linecap",
                      "stroke-linejoin", "font-family", "font-size", "font-weight", "text-anchor",
                      "transform", "role", "aria-label", "aria-hidden"}
            allowed = common | ({"markerwidth", "markerheight", "refx", "refy", "orient"}
                                if tag == "marker" else set())
            if not set(attrs).issubset(allowed):
                _fail("unsupported_generated_shape", "unreviewed SVG marker/text attribute")
            if tag == "marker":
                identity = attrs.get("id", "")
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", identity) or identity in self.svg_scopes[-1]["markers"]:
                    _fail("unsupported_generated_shape", "SVG marker identity")
                self.svg_scopes[-1]["markers"].add(identity)
        if any(PRIVATE.search(value) for value in attrs.values() if value is not None):
            _fail("private_content", self.page)
        for key, value in attrs.items():
            if value is None:
                continue
            marker = self.svg_depth and key in {"marker-start", "marker-mid", "marker-end"}
            if marker and value != "none":
                match = re.fullmatch(r"url\(#([A-Za-z][A-Za-z0-9_.:-]*)\)", value)
                if match is None:
                    _fail("external_resource", "SVG marker requires literal local fragment")
                self.svg_scopes[-1]["references"].add(match.group(1))
            elif re.search(r"url\s*\(", value, re.I):
                _fail("external_resource", "unreviewed attribute URL")
        if tag == "script":
            if not attrs.get("src"):
                _fail("inline_script")
            self.in_script = True
            source, fragment = _resolve(self.page, attrs["src"])
            self.scripts.append(source)
            if re.fullmatch(r"assets/runtime-depth-[0-9]+\.js", source):
                _fail("unsupported_generated_shape", "runtime requires pinned RequireJS data-main")
            requirejs = "assets/vendor/requirejs/2.3.6/require.min.js"
            if "data-main" in attrs or source == requirejs:
                if source != requirejs or fragment or not attrs.get("data-main"):
                    _fail("unsupported_generated_shape", "RequireJS data-main loader")
                main, anchor = _resolve(self.page, attrs["data-main"])
                depth = len(PurePosixPath(self.page).parts) - 1
                if (anchor or main != "assets/runtime-depth-" + str(depth) + ".js"
                        or attrs["data-main"] != "../" * depth + main):
                    _fail("unsupported_generated_shape", "RequireJS data-main context")
                self.data_main.append((main, source))
        elif "data-main" in attrs:
            _fail("unsupported_generated_shape", "data-main outside script")
        if tag == "style" or "style" in attrs:
            _fail("inline_style")
        if any(k.startswith("on") for k in attrs):
            _fail("inline_event")
        if tag in {"base", "iframe", "object", "embed", "foreignobject"}:
            _fail("unsupported_generated_shape")
        if tag == "meta" and attrs.get("http-equiv", "").lower() in {"refresh", "content-security-policy"}:
            _fail("unsupported_generated_shape")
        for key in ("id", "name"):
            if attrs.get(key):
                self.ids.add(attrs[key])
        for key in ("src", "href", "poster", "action", "xlink:href", "data-main"):
            if key in attrs:
                edge = _resolve(self.page, attrs[key], article=tag == "a" and key == "href")
                if edge:
                    self.edges.append(edge)
        if "srcset" in attrs:
            _fail("unsupported_generated_shape", "srcset requires explicit reviewed mapping")

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        if tag == "svg":
            self._close_svg()

    def _close_svg(self):
        if not self.svg_scopes:
            _fail("unsupported_generated_shape", "unbalanced SVG")
        scope = self.svg_scopes.pop()
        if not scope["references"].issubset(scope["markers"]):
            _fail("missing_anchor", "SVG marker outside local scope")
        self.svg_depth -= 1

    def close(self):
        super().close()
        if self.svg_scopes:
            _fail("unsupported_generated_shape", "unclosed SVG")

    def handle_data(self, data):
        if PRIVATE.search(data):
            _fail("private_content", self.page)
        if self.in_script and data.strip():
            _fail("inline_script")

    def handle_startendtag(self, tag, pairs):
        if tag == "script":
            _fail("unsupported_generated_shape", "self-closing script")
        self.handle_starttag(tag, pairs)
        if tag == "svg":
            self._close_svg()


def _css_edges(path, text, *, verified_bytes=None):
    if re.search(r"expression\s*\(|javascript\s*:|behavior\s*:|-moz-binding", text, re.I):
        _fail("unsafe_css")
    # Escaped resource identifiers/URLs require a separately reviewed grammar;
    # they must not evade a scanner for literal url()/@import tokens.
    if verified_bytes is not None:
        if not isinstance(verified_bytes, bytes) or verified_bytes != text.encode():
            _fail("asset_payload_mismatch", path)
        # Exact retained stylesheet bytes may contain upstream comments and
        # quoted numeric icon/content glyphs. Never decode selectors, properties,
        # url/import identifiers or resource values as an escape shortcut.
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        def glyph(match):
            value = match.group(0)
            return re.sub(r"\\[0-9a-fA-F]{1,6}(?:[ \t\r\n\f])?", "G", value)
        text = re.sub(r"\bcontent\s*:\s*(?:\"(?:[^\"\\]|\\[0-9a-fA-F]{1,6}[ \t\r\n\f]?)*\"|'(?:[^'\\]|\\[0-9a-fA-F]{1,6}[ \t\r\n\f]?)*')", glyph, text, flags=re.I)
    if "\\" in text:
        _fail("dynamic_loader", "unreviewed CSS escape grammar")
    edges = []
    pieces, cursor = [], 0
    imports = list(re.finditer(r"@import\b", text, re.I))
    for start in imports:
        if start.start() < cursor:
            _fail("dynamic_loader", "overlapping CSS import tokens")
        end = text.find(";", start.start())
        if end < 0:
            _fail("dynamic_loader", "unterminated CSS import")
        directive = text[start.start():end + 1]
        # Only the closed, unqualified literal import forms are supported.
        # Media/layer/supports suffixes are unsupported, never invisible edges.
        match = re.fullmatch(
            r'''@import\s+(?:"([^"\n]+)"|'([^'\n]+)'|url\(\s*(?:"([^"\n]+)"|'([^'\n]+)'|([^\s)'";]+))\s*\))\s*;''',
            directive, re.I)
        if not match:
            _fail("dynamic_loader", "unreviewed CSS import qualifier/grammar")
        edges.append(_resolve(path, next(g for g in match.groups() if g is not None)))
        pieces.extend((text[cursor:start.start()], " " * (end + 1 - start.start())))
        cursor = end + 1
    pieces.append(text[cursor:])
    remaining = "".join(pieces)
    for match in re.finditer(r'url\(\s*(?:"([^"\n]*)"|\'([^\'\n]*)\'|([^\s)]+))\s*\)', remaining, re.I):
        edges.append(_resolve(path, next(g for g in match.groups() if g is not None)))
    # Unknown or dynamic url()/import grammar is never silently ignored.
    if len(edges) - len(imports) != len(re.findall(r"\burl\s*\(", remaining, re.I)):
        _fail("dynamic_loader")
    return edges


def _js_edges(path, text, document):
    if re.search(r"\b(?:Blob|eval|Function)\s*\(|createObjectURL|(?:unsafe-inline|unsafe-eval)", text):
        _fail("dynamic_loader")
    # Browser static module imports/re-exports are outside the admitted classic
    # script/Worker bridge. Reject the keywords even with comments/qualifiers;
    # absence of an import(...) call is not a closed module dependency graph.
    if re.search(r"\b(?:import|export)\b", text):
        _fail("dynamic_loader", "unadmitted ESM grammar")
    edges, spans = [], []
    patterns = [
        (r'new\s+Worker\s*\(\s*(["\'])([^"\'\n]+)\1\s*\)', document),
        (r'importScripts\s*\(\s*(["\'])([^"\'\n]+)\1\s*\)', path),
    ]
    for pattern, base in patterns:
        for match in re.finditer(pattern, text):
            value = match.group(2)
            # Check absolute URL even for an orphan script, before contextual base admission.
            if urlsplit(value).scheme or value.startswith("//"):
                _fail("external_resource", value)
            if base is None:
                _fail("dynamic_loader", "worker constructor has no document context")
            edges.append(_resolve(base, value))
            spans.append((match.start(), match.end()))
    rest = text
    for start, end in sorted(spans, reverse=True):
        rest = rest[:start] + " " * (end - start) + rest[end:]
    if re.search(r"\b(?:Worker|importScripts|fetch|XMLHttpRequest|WebSocket|EventSource|import)\s*\(|"
                 r"\brequire\s*\(|\bdefine\s*\(|\.(?:src|href)\s*=|"
                 r"setAttribute\s*\(\s*['\"](?:src|href)|createElement\s*\(\s*['\"]script", rest):
        _fail("dynamic_loader", "unadmitted loader grammar")
    return edges


def _private_scan_text(path, data, verified_data=None):
    """Mask one public selector literal only for its independently verified pin.

    jQuery3.7 declares supported input types in an object whose boolean property
    `password:!0` is public code, not a credential assignment. Never alter the
    payload or relax path/key/credential detection for any changed/unverified
    asset. Whole-lock byte authority is obtained by AS1 before this scanner.
    """
    text = _decode(data)
    if (path == "assets/vendor/jquery/3.7.0/jquery.min.js"
            and isinstance(verified_data, bytes) and verified_data == data
            and _sha(data) == "d8f9afbf492e4c139e9d2bcb9ba6ef7c14921eb509fb703bc7a3f911b774eff8"):
        literal = "{radio:!0,checkbox:!0,file:!0,password:!0,image:!0}"
        if text.count(literal) != 1:
            _fail("asset_payload_mismatch", "pinned jQuery input-type literal")
        text = text.replace(literal, literal.replace("password:!0", "public_input_type:!0"), 1)
    return text


def _theme_scan_text(path, data, verified_data=None):
    """One inert CSS grammar keyword in exact verified Highlight.js11.8 code.

    The media-feature name is grammar data later passed to the syntax keyword
    classifier, not a matchMedia call or a stylesheet/theme selector. Preserve
    public bytes and all other theme matches, including every changed asset.
    """
    text = _decode(data)
    if (path == "assets/vendor/highlight/11.8.0/highlight.min.js"
            and isinstance(verified_data, bytes) and verified_data == data
            and _sha(data) == "4499ff936d4fd562adca5a5cbe512dc19eb80942eee8618dafbcebc4f7974bdb"):
        literal = '"pointer","prefers-color-scheme","prefers-contrast"'
        if text.count(literal) != 1:
            _fail("asset_payload_mismatch", "pinned Highlight CSS grammar literal")
        text = text.replace(literal, literal.replace("prefers-color-scheme", "public_media_feature"), 1)
    return text


def validate_payload(files, *, symlinks=(), verified_assets=None):
    """Static intermediate closure only; never a browser, license, or build verdict."""
    if symlinks:
        _fail("public_allowlist", "symlinks")
    if not isinstance(files, dict) or len(files) > 10000:
        _fail("payload_limit")
    verified_assets = {} if verified_assets is None else verified_assets
    if (not isinstance(verified_assets, dict) or any(
            not isinstance(data, bytes) or files.get(path) != data
            for path, data in verified_assets.items())):
        _fail("asset_payload_mismatch")
    total = 0
    html, texts, edges, script_documents = {}, {}, [], defaultdict(set)
    allowed = {".html", ".css", ".js", ".json", ".woff", ".woff2", ".ttf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".txt"}
    for path, data in files.items():
        _relative(path)
        if path not in {"index.html", "bundle.json", "NOTICE.txt"} and not path.startswith(
                ("core/", "runner/", "operator/", "assets/", "help/")):
            _fail("public_allowlist", path)
        suffix = PurePosixPath(path).suffix.lower()
        if PurePosixPath(path).name in {"themeswap.js", "themes.js", "versions.js", "siteinfo.js", "warner.js"}:
            _fail("theme_alternative", path)
        if suffix not in allowed or path.endswith(".map") or any(p in {"logs", "depot", "depots", "raw", "results"} for p in PurePosixPath(path).parts):
            _fail("public_allowlist", path)
        if suffix == ".txt" and path != "NOTICE.txt" and not path.startswith("assets/licenses/"):
            _fail("public_allowlist", path)
        if not isinstance(data, bytes) or len(data) > 16 * 1024 * 1024:
            _fail("payload_limit", path)
        total += len(data)
        if total > 256 * 1024 * 1024:
            _fail("payload_limit")
        if suffix in {".html", ".css", ".js", ".json", ".svg", ".txt"}:
            text = _decode(data)
            texts[path] = text
            if PRIVATE.search(_private_scan_text(path, data, verified_assets.get(path))):
                _fail("private_content", path)
            # The selected complete light CSS includes inert settings/theme
            # selectors. The exact locked sheet is admitted by the owning asset
            # verifier; HTML controls and unverified styles remain strict.
            if (THEME.search(_theme_scan_text(path, data, verified_assets.get(path)))
                    and not (suffix == ".css" and path in verified_assets)):
                _fail("theme_alternative", path)
            if suffix in {".html", ".svg"}:
                parser = _PayloadHTML(path)
                parser.feed(text)
                parser.close()
                html[path] = parser
                edges.extend(parser.edges)
                for script in parser.scripts:
                    script_documents[script].add(path)
                for main, loader in parser.data_main:
                    if loader not in verified_assets or main not in verified_assets:
                        _fail("asset_validation_evidence", "unverified RequireJS data-main dependency")
                    script_documents[main].add(path)
            elif suffix == ".css":
                edges.extend(_css_edges(path, text, verified_bytes=verified_assets.get(path)))
            elif suffix == ".json":
                cap = 32768 if path.startswith("help/fragments/") else 2097152
                if len(data) > cap:
                    _fail("payload_limit", path)
                try:
                    json.loads(text, object_pairs_hook=_json_pairs,
                               parse_constant=lambda value: _fail("invalid_json", value))
                except (TypeError, ValueError):
                    _fail("invalid_json", path)
    for path, text in texts.items():
        if path.endswith(".js"):
            contexts = script_documents.get(path) or {None}
            reviewed = path in verified_assets
            if reviewed and path.startswith("assets/vendor/"):
                # Immutable distribution code: runtime adapter checked complete
                # named AMD dependencies and license/distribution bytes first.
                continue
            if reviewed and re.fullmatch(r"assets/runtime-depth-[0-9]+\.js", path):
                workers = re.findall(r'new\s+Worker\(\s*("[^"\n]+")\s*\)', text)
                if len(workers) != 1 or None in contexts:
                    _fail("dynamic_loader", "reviewed runtime worker shape")
                for document in contexts:
                    depth = len(PurePosixPath(document).parts) - 1
                    expected_script = 'assets/runtime-depth-' + str(depth) + '.js'
                    if path != expected_script or json.loads(workers[0]) != '../' * depth + 'assets/search-worker.js':
                        _fail("dynamic_loader", "runtime/page depth mismatch")
                    target = _resolve(document, json.loads(workers[0]))
                    if target != ("assets/search-worker.js", ""):
                        _fail("dynamic_loader", "runtime/page depth mismatch")
                    edges.append(target)
                continue
            if reviewed and path == "assets/search-worker.js":
                imports = re.findall(r'importScripts\(\s*("[^"\n]+")\s*\)', text)
                if len(imports) != 1:
                    _fail("dynamic_loader", "reviewed worker import shape")
                target = _resolve(path, json.loads(imports[0]))
                if target != ("assets/vendor/minisearch/6.1.0/index.min.js", ""):
                    _fail("dynamic_loader", "reviewed worker dependency")
                edges.append(target)
                continue
            if reviewed and path.endswith("/search_index.js"):
                match = re.fullmatch(r"\s*(?:var|const)\s+documenterSearchIndex\s*=\s*(\{.*\})\s*;?\s*", text, re.S)
                if match is None:
                    _fail("dynamic_loader", "Documenter search data shape")
                try:
                    value = json.loads(match.group(1), object_pairs_hook=_json_pairs,
                        parse_constant=lambda value: _fail("invalid_json", value))
                except (ValueError, TypeError):
                    _fail("invalid_json", path)
                if not isinstance(value, dict) or not isinstance(value.get("docs"), list):
                    _fail("dynamic_loader", "Documenter search data shape")
                continue
            for document in contexts:
                edges.extend(_js_edges(path, text, document))
    for path, anchor in edges:
        if path not in files:
            _fail("missing_resource", path)
        if anchor and (path not in html or anchor not in html[path].ids):
            _fail("missing_anchor", path + "#" + anchor)


def validate_asset_entry(entry, inputs):
    """Check an entry's local byte/metadata closure, not upstream license authority.

    An admitted whole lock, verified distribution and complete license provenance
    remain separate prerequisites. Synthetic unit inputs do not publish assets.
    """
    _object(entry, {"id", "family", "version", "source_uri", "distribution_sha256", "files", "license", "dependencies"}, "asset_shape")
    if not re.fullmatch(r"[0-9a-f]{64}", entry["distribution_sha256"]) or entry["distribution_sha256"] == "0" * 64:
        _fail("missing_pin")
    if not entry["source_uri"].startswith("https://"):
        _fail("asset_shape")
    license = entry["license"]
    _object(license, {"spdx", "text_file", "text_sha256", "copyright"}, "asset_shape")
    if entry["family"] == "katex-fonts" and license["spdx"] != "OFL-1.1":
        _fail("font_license_mismatch")
    _relative(license["text_file"], "asset_shape")
    if license["text_file"] not in inputs:
        _fail("missing_license")
    if not license["copyright"] or not license["spdx"]:
        _fail("missing_license")
    if _sha(inputs[license["text_file"]]) != license["text_sha256"]:
        _fail("license_hash_mismatch")
    if not isinstance(entry["files"], list) or not entry["files"]:
        _fail("missing_pin")
    seen = set()
    for file in entry["files"]:
        _object(file, {"source_path", "destination", "bytes", "sha256", "media_type"}, "asset_shape")
        source = _relative(file["source_path"], "asset_shape")
        destination = _relative(file["destination"], "asset_shape")
        if destination in seen:
            _fail("asset_shape")
        seen.add(destination)
        if source not in inputs:
            _fail("missing_pin")
        data = inputs[source]
        if _sha(data) != file["sha256"] or len(data) != file["bytes"]:
            _fail("asset_hash_mismatch")
        if type(file["bytes"]) is not int or not 0 < file["bytes"] <= 16 * 1024 * 1024:
            _fail("asset_shape")
        if entry["family"] == "katex-fonts":
            mime = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf"}
            if mime.get(PurePosixPath(source).suffix) != file["media_type"]:
                _fail("asset_shape")
    return {"status": "bytes_verified", "license_authority": "not_evaluated"}


def prepare_catalog(*, fragments, coverage, shared_schema):
    """Never synthesize DOC03 origins or a root-owned alternative schema.

    Serialization is intentionally unavailable until the owning schema and its
    validation binding are admitted. Merely passing a schema object is not proof.
    """
    if not isinstance(fragments, list) or not isinstance(coverage, list):
        _fail("catalog_shape")
    return {"fragments": copy.deepcopy(fragments), "coverage": copy.deepcopy(coverage),
            "status": "blocked", "reason": "missing_shared_schema" if shared_schema is None
            else "shared_schema_validation_required", "bundle_bytes": None}


_MEDIA_TYPES = {
    ".html": "text/html", ".css": "text/css", ".js": "application/javascript",
    ".json": "application/json", ".woff": "font/woff", ".woff2": "font/woff2",
    ".ttf": "font/ttf", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
    ".svg": "image/svg+xml", ".ico": "image/vnd.microsoft.icon", ".txt": "text/plain",
}


def _bundle_coverage(plan, graph, coverage, payload):
    """Bind PRIMARY refs to their exact output paths/ids, not global id presence.

    Retained source bytes/reviews are checked by the trusted owning C2 adapter;
    this pure projection cannot create those proofs from a source status flag.
    """
    if not isinstance(coverage, list) or len(coverage) != len(PRIMARY):
        _fail("coverage_mismatch")
    revisions = {item["path"]: item["revision"] for item in graph["components"]}
    revisions["root"] = graph["revision"]
    seen, available, locations = set(), set(), {}
    for row in coverage:
        _object(row, {"id", "sources", "pages"}, "coverage_mismatch")
        identity = row["id"]
        if identity not in PRIMARY or identity in seen:
            _fail("coverage_mismatch")
        seen.add(identity)
        if (not isinstance(row["sources"], list)
                or len(row["sources"]) != len(PRIMARY[identity][2])
                or not isinstance(row["pages"], list) or len(row["pages"]) > len(payload)):
            _fail("coverage_mismatch")
        source_paths = []
        for reference in row["sources"]:
            _object(reference, {"component", "revision", "path", "selector", "sha256"},
                    "coverage_source_mismatch")
            component, path = reference["component"], _relative(reference["path"])
            if (component not in revisions or reference["revision"] != revisions[component]
                    or reference["selector"] != {"kind": "file", "value": ""}
                    or not isinstance(reference["sha256"], str)
                    or not re.fullmatch(r"[a-f0-9]{64}", reference["sha256"])):
                _fail("coverage_source_mismatch")
            source_paths.append(path if component == "root" else component + "/" + path)
        if source_paths != PRIMARY[identity][2]:
            _fail("coverage_source_mismatch", identity)
        available.update(source_paths)
        routes = set()
        for page in row["pages"]:
            _object(page, {"path", "anchors"}, "coverage_mismatch")
            path = _relative(page["path"])
            if (path not in payload or not path.endswith(".html")
                    or not isinstance(page["anchors"], list)
                    or len(page["anchors"]) > 10000):
                _fail("coverage_mismatch", path)
            parser = _PayloadHTML(path)
            parser.feed(_decode(payload[path]))
            parser.close()
            for anchor in page["anchors"]:
                if not isinstance(anchor, str) or not anchor or anchor not in parser.ids:
                    _fail("missing_anchor", path)
                route = path + "#" + anchor
                if route in routes:
                    _fail("coverage_mismatch", "duplicate route")
                routes.add(route)
                if anchor in ANCHORS:
                    if anchor in locations:
                        _fail("coverage_mismatch", "ambiguous primary anchor")
                    locations[anchor] = path
        if not set(PRIMARY[identity][3]).issubset(routes):
            _fail("primary_mapping_mismatch", identity)
    validate_primary_sources(plan, available)
    if set(locations) != set(plan["expected_primary_anchors"]):
        _fail("missing_anchor", "primary coverage")


def finalize_bundle(*, plan, before, after, generator, schema_ref, coverage,
                    fragments, aliases, payload, asset_lock, asset_inputs,
                    validate_shape, validate_bindings, validate_assets):
    """Pure, fail-closed completion seam; candidate is not publication acceptance.

    Root supplies trusted adapters over detached retained bytes: shape(document)
    calls owning Contracts C1; bindings(document, coverage=...) calls owning C2
    and validates every coverage source against the same retained source layout.
    Missing owning proof must be translated to FileNotFoundError by the adapter;
    contradictory evidence must raise. No target imports/fetch/IO occur here.

    assets(lock_bytes, inputs, payload=...) verifies whole lock, distributions,
    licenses and dependency closure using independently retained Root evidence,
    then returns the exact verified non-HTML/non-fragment destination->bytes map.
    None means unavailable proof; a boolean/status flag is never byte evidence.
    An explicit empty closure is valid only when there are no such payloads.
    This private callback seam does not add a public manifest/receipt format.
    """
    def blocked(reason):
        return {"status": "blocked", "reason": reason, "manifest": None,
                "bundle_bytes": None, "bundle_sha256": None}

    validate_source_binding(before, after)
    if any(not callable(adapter) for adapter in
           (validate_shape, validate_bindings, validate_assets)):
        return blocked("missing_validation_adapter")
    if any(value is None for value in (schema_ref, generator, coverage, payload,
                                        asset_lock, asset_inputs)):
        return blocked("missing_validation_evidence")
    plan = _validate_pilot_plan(copy.deepcopy(plan))
    if (not isinstance(payload, dict) or not isinstance(asset_lock, bytes)
            or not asset_lock or len(asset_lock) > PLAN_LIMITS["manifest_bytes"]
            or not isinstance(asset_inputs, dict)):
        _fail("bundle_shape")
    if "bundle.json" in payload:
        _fail("manifest_self_hash")
    limits = plan["limits"]
    if (len(payload) > limits["files"]
            or any(not isinstance(data, bytes) or len(data) > limits["file_bytes"]
                   for data in payload.values())
            or sum(len(data) for data in payload.values()) > limits["total_bytes"]):
        _fail("payload_limit")
    if (len(asset_inputs) > PLAN_LIMITS["files"]
            or any(not isinstance(data, bytes) or len(data) > PLAN_LIMITS["file_bytes"]
                   for data in asset_inputs.values())
            or sum(len(data) for data in asset_inputs.values()) > PLAN_LIMITS["total_bytes"]):
        _fail("asset_limit")
    # Detach containers; bytes themselves are immutable and need not be copied.
    payload, asset_inputs = dict(payload), dict(asset_inputs)
    coverage = copy.deepcopy(coverage)
    # Obtain exact whole-lock evidence before selecting the narrowly admitted
    # runtime path. No caller boolean changes CSS/JS validation.
    try:
        verified_assets = validate_assets(asset_lock, dict(asset_inputs), payload=dict(payload))
    except FileNotFoundError:
        return blocked("missing_validation_evidence")
    if verified_assets is None:
        return blocked("missing_asset_evidence")
    if not isinstance(verified_assets, dict) or any(
            not isinstance(data, bytes) for data in verified_assets.values()):
        _fail("asset_validation_evidence", "exact verified bytes required")
    validate_payload(payload, verified_assets=verified_assets)
    _bundle_coverage(plan, before, coverage, payload)
    if not isinstance(fragments, list) or len(fragments) > 256 or not isinstance(aliases, list):
        _fail("catalog_shape")
    fragment_paths, fragment_documents = set(), []
    for descriptor in fragments:
        _object(descriptor, {"id", "file", "sha256"}, "catalog_shape")
        path = descriptor["file"]
        if (not isinstance(descriptor["id"], str)
                or path != "help/fragments/" + descriptor["id"] + ".json"
                or path in fragment_paths or path not in payload):
            _fail("fragment_payload_mismatch")
        fragment_paths.add(path)
        if (len(payload[path]) > limits["fragment_bytes"]
                or _sha(payload[path]) != descriptor["sha256"]):
            _fail("fragment_payload_mismatch")
        try:
            fragment_documents.append(json.loads(_decode(payload[path]), object_pairs_hook=_json_pairs,
                parse_constant=lambda value: _fail("invalid_json", value)))
        except (ValueError, TypeError):
            _fail("invalid_json", path)
    if {path for path in payload if path.startswith("help/fragments/")} != fragment_paths:
        _fail("fragment_payload_mismatch", "unregistered fragment")
    files = [{"path": path, "media_type": _MEDIA_TYPES[PurePosixPath(path).suffix.lower()],
              "bytes": len(data), "sha256": _sha(data)}
             for path, data in sorted(payload.items())]
    manifest = {"format": "qcl-negf.docs-bundle.v1", "sources": copy.deepcopy(before),
                "schema": copy.deepcopy(schema_ref), "generator": copy.deepcopy(generator),
                "fragments": copy.deepcopy(fragments), "files": files,
                "aliases": copy.deepcopy(aliases)}
    try:
        bundle_bytes = json.dumps(manifest, sort_keys=True, separators=(",", ":"),
                                  ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, UnicodeError):
        _fail("bundle_shape")
    if len(bundle_bytes) > limits["manifest_bytes"]:
        _fail("manifest_limit")
    try:
        validate_shape(copy.deepcopy(manifest))
        for document in fragment_documents:
            validate_shape(copy.deepcopy(document))
        validate_bindings(copy.deepcopy(manifest), coverage=copy.deepcopy(coverage))
    except FileNotFoundError:
        return blocked("missing_validation_evidence")
    expected_assets = {path: data for path, data in payload.items()
                       if not path.endswith(".html") and path not in fragment_paths}
    if verified_assets != expected_assets:
        _fail("asset_payload_mismatch")
    # Recheck against the detached manifest as well as each other: mutating both
    # caller graphs identically during validation must not reset the source epoch.
    validate_source_binding(manifest["sources"], before)
    validate_source_binding(manifest["sources"], after)
    return {"status": "candidate", "manifest": manifest,
            "bundle_bytes": bundle_bytes, "bundle_sha256": _sha(bundle_bytes)}
