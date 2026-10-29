/** DOC04 build-only static math adapter. No CLI, process, fetch, DOM, or font
 * publication. Caller must supply a reviewed source->node mapping and an external
 * supervisor (<=60s, admitted CPU/RAM/log limits); synchronous KaTeX cannot be
 * interrupted by an event-loop timer. Unit results never admit a public bundle.
 */
import { createHash } from "node:crypto";
import { lstat, readFile, realpath } from "node:fs/promises";
import { isAbsolute, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const MODULE_SHA256 = "cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88";
const CSS_SHA256 = "df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e";
const LIMIT = Object.freeze({
  tex: 16384,
  batch: 4194304,
  records: 10000,
  markup: 262144,
  total: 33554432,
  css: 1048576,
  groups: 20000,
});
const sha = (input) => createHash("sha256").update(input).digest("hex");
const bytes = (input) => Buffer.byteLength(input, "utf8");
const fail = (code, detail = "") => {
  const error = new Error(detail ? `${code}: ${detail}` : code);
  error.code = code;
  throw error;
};
const own = (object, field) => Object.prototype.hasOwnProperty.call(object, field);
const plain = (value) =>
  value !== null && typeof value === "object" &&
  Object.getPrototypeOf(value) === Object.prototype;

function recordShape(record) {
  const keys = ["page", "selector", "tex", "tex_sha256", "display"];
  if (
    !plain(record) || Object.keys(record).length !== keys.length ||
    !keys.every((key) => own(record, key)) || typeof record.tex !== "string" ||
    typeof record.display !== "boolean" || typeof record.page !== "string" ||
    !/^[A-Za-z0-9_-][A-Za-z0-9_./-]*\.html$/.test(record.page) ||
    record.page.split("/").some((part) => part === ".." || part === ".") ||
    !/^#[A-Za-z][A-Za-z0-9_.:-]*$/.test(record.selector) ||
    !/^[a-f0-9]{64}$/.test(record.tex_sha256)
  ) fail("record_shape");
  if (sha(record.tex) !== record.tex_sha256) fail("tex_hash_mismatch");
}

export function validateMathMapping(expected, actual) {
  if (
    !Array.isArray(expected) || !Array.isArray(actual) || expected.length !== actual.length ||
    expected.length > LIMIT.records
  ) fail("math_mapping_mismatch");
  const identities = new Set();
  for (let i = 0; i < expected.length; i++) {
    const a = expected[i];
    const b = actual[i];
    recordShape(a);
    recordShape(b);
    const key = `${a.page}\0${a.selector}`;
    if (
      identities.has(key) || ["page", "selector", "tex", "tex_sha256", "display"]
        .some((field) => a[field] !== b[field])
    ) fail("math_mapping_mismatch");
    identities.add(key);
  }
}

const DENY = new Set([
  "def",
  "gdef",
  "edef",
  "xdef",
  "let",
  "futurelet",
  "global",
  "long",
  "newcommand",
  "renewcommand",
  "providecommand",
  "csname",
  "endcsname",
  "catcode",
  "href",
  "url",
  "includegraphics",
  "htmlClass",
  "htmlId",
  "htmlStyle",
  "htmlData",
  "input",
  "include",
  "usepackage",
  "require",
  "read",
  "write",
  "openout",
  "message",
  "errmessage",
  "show",
  // Explicit authored geometry is outside the reviewed V1 layout subset.
  "rule",
  "raisebox",
  "kern",
  "mkern",
  "hskip",
  "vskip",
  "mskip",
  "hspace",
  "vspace",
  "hspace*",
  "vspace*",
  "fontsize",
  "setlength",
  "enlargethispage",
  // Exact KaTeX0.16.8 src/functions/sizing.js::sizeFuncs (SHA 7efd9a5c...).
  "tiny",
  "sixptsize",
  "scriptsize",
  "footnotesize",
  "small",
  "normalsize",
  "large",
  "Large",
  "LARGE",
  "huge",
  "Huge",
  // Exact manual delimiter sizes from pinned delimsizing.js, not auto left/right.
  "bigl",
  "Bigl",
  "biggl",
  "Biggl",
  "bigr",
  "Bigr",
  "biggr",
  "Biggr",
  "bigm",
  "Bigm",
  "biggm",
  "Biggm",
  "big",
  "Big",
  "bigg",
  "Bigg",
]);
function sourceGate(tex) {
  if (bytes(tex) > LIMIT.tex) fail("tex_limit");
  // TeX control token lexer: comments end at real newline; a control symbol
  // consumes exactly one character, so escaped backslashes/percent are inert.
  for (let i = 0; i < tex.length; i++) {
    if (tex[i] === "%") {
      while (i < tex.length && tex[i] !== "\n" && tex[i] !== "\r") i++;
    } else if (tex[i] === "\\") {
      i++;
      let command = "";
      while (i < tex.length && /[A-Za-z@]/.test(tex[i])) command += tex[i++];
      if (command) {
        i--;
        if (DENY.has(command) || command.includes("@")) fail("unsupported_source", command);
      }
    }
  }
}

const TAGS = new Set(("span math annotation semantics mtext mn mo mi mspace mover munder " +
  "munderover msup msub msubsup mfrac mroot msqrt mtable mtr mtd mlabeledtr mrow " +
  "menclose mstyle mpadded mphantom svg path line").split(" "));
const COMMON = new Set(["class", "style", "aria-hidden"]);
const MATH_ATTRS = new Set(("xmlns display encoding mathvariant mathcolor mathbackground " +
  "mathsize scriptlevel displaystyle stretchy symmetric fence separator largeop movablelimits " +
  "accent accentunder minsize maxsize lspace rspace width height depth voffset notation " +
  "linethickness columnalign rowalign columnspacing rowspacing columnlines rowlines " +
  "columnspan rowspan linebreak equalrows equalcolumns side frame framespacing align").split(" "));
const SVG_ATTRS = new Set([
  "xmlns",
  "width",
  "height",
  "viewBox",
  "preserveAspectRatio",
  "d",
  "x1",
  "x2",
  "y1",
  "y2",
  "stroke",
  "stroke-width",
  "fill",
]);
const LENGTH_PROPS = new Set(
  ("height width min-width max-width min-height max-height top bottom left right " +
    "vertical-align margin-left margin-right margin-top margin-bottom padding-left padding-right " +
    "padding-top padding-bottom border-bottom-width border-top-width border-right-width " +
    "border-left-width border-width font-size").split(" "),
);
const NUMBER = "[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)";
const LENGTH = new RegExp(`^(?:${NUMBER})(?:em|ex|px|pt|%|rem)?$`);
const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", "#x27": "'" };
function decode(text) {
  return text.replace(/&(#(?:x[0-9a-f]+|[0-9]+)|[A-Za-z]+);/gi, (_whole, name) => {
    if (own(ENTITIES, name)) return ENTITIES[name];
    if (name[0] === "#") {
      const number = name[1].toLowerCase() === "x"
        ? parseInt(name.slice(2), 16)
        : Number(name.slice(1));
      if (!Number.isInteger(number) || number < 32 || number > 0x10ffff) fail("unsupported_markup");
      return String.fromCodePoint(number);
    }
    fail("unsupported_markup", "unknown entity");
  });
}
function escapeAttribute(value) {
  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(
    />/g,
    "&gt;",
  );
}

function propertyAtoms(property) {
  const sides = ["top", "right", "bottom", "left"];
  const border = sides.flatMap((side) =>
    ["width", "style", "color"].map((kind) => `border-${side}-${kind}`)
  );
  if (property === "all") return ["*"];
  if (property === "border") return border;
  if (/^border-(?:width|style|color)$/.test(property)) {
    const kind = property.slice(7);
    return sides.map((side) => `border-${side}-${kind}`);
  }
  if (/^border-(?:top|right|bottom|left)$/.test(property)) {
    return ["width", "style", "color"].map((kind) => `${property}-${kind}`);
  }
  if (/^border-(?:block|inline)(?:-|$)/.test(property)) return border;
  if (/^(?:margin|padding)(?:-(?:block|inline)(?:-(?:start|end))?)?$/.test(property)) {
    const family = property.split("-")[0];
    return sides.map((side) => `${family}-${side}`);
  }
  if (property === "font") return ["font-size"];
  if (property === "background") return ["background-color"];
  if (property === "inset" || /^inset-(?:block|inline)(?:-|$)/.test(property)) return sides;
  if (
    LENGTH_PROPS.has(property) || ["color", "background-color", "position"].includes(property) ||
    /^border-(?:top|right|bottom|left)-(?:width|style|color)$/.test(property)
  ) return [property];
  return null;
}

// This adapter is for the exact published Documenter 1.17 light theme only.
const DOCUMENTER_LIGHT_SHA256 = "706b5379af688761c9f0168af88e1eaa05495e1cdc7c4a0debbf03621d8923a7";
// Exact ancillary CSS retains the global-important refusal; this only admits
// its reviewed comment/quoted numeric-content grammar, with no selector proof.
const ANCILLARY_CSS_SHA256 = new Set([
  "f8bd27657d5373067aa3e9d8885497855c6284d495706dfb1ccdf0cdc0bc3391", // fontawesome
  "4de6067d6c116b81dd1a4fcd252e3c3e2297ae01c576b63fabac8f8655b4787a", // solid
  "f4ab507a816906136d0ea985f089ee666acd8a10850ec718e67cd98ca23a8081", // brands
  "0ca8befae6dc6607ebb252e15fb00f6482d094b6a0d1771b2e0ee327eacadebe", // Lato3.0.0
]);
const DISJOINT_IMPORTANT = new Set([
  "-ms-high-contrast-adjust",
  "opacity",
  "display",
  "visibility",
  "z-index",
  "text-align",
  "overflow",
  "overflow-x",
  "overflow-y",
]);

function pinnedCSSRules(text) {
  // Consume comments and strings before braces. Escapes are admitted only as
  // numeric glyphs in an entire quoted content value; never selectors or URLs.
  let clean = "", i = 0;
  while (i < text.length) {
    if (text.startsWith("/*", i)) {
      const end = text.indexOf("*/", i + 2);
      if (end < 0) fail("unsupported_style_context");
      clean += " ";
      i = end + 2;
    } else if (text[i] === '"' || text[i] === "'") {
      const quote = text[i++];
      let value = "";
      while (i < text.length && text[i] !== quote) value += text[i++];
      if (i === text.length) fail("unsupported_style_context");
      i++;
      if (value.includes("\\")) {
        if (
          !/(?:^|[;{])\s*content\s*:\s*$/i.test(clean) ||
          !/^(?:\\[a-fA-F0-9]{1,6}\s?)+$/.test(value)
        ) {
          fail("unsupported_style_context", "non-glyph escape");
        }
      }
      // Quoted values contain no declaration/rule delimiters in the lexer view.
      clean += '"quoted"';
    } else {
      if (text[i] === "\\") fail("unsupported_style_context", "escaped identifier");
      clean += text[i++];
    }
  }
  const rules = [];
  const stack = [];
  let start = 0;
  for (let j = 0; j < clean.length; j++) {
    if (clean[j] === "{") {
      stack.push(clean.slice(start, j).trim());
      start = j + 1;
    } else if (clean[j] === "}") {
      if (!stack.length) fail("unsupported_style_context");
      const selector = stack.pop();
      const body = clean.slice(start, j);
      for (const field of body.split(";")) {
        if (!/!\s*important\b/i.test(field)) continue;
        const m = /^\s*([-a-zA-Z]+)\s*:[^{};]*!\s*important\s*$/i.exec(field);
        if (!m) fail("unsupported_style_context", "important grammar");
        rules.push({ selector, property: m[1].toLowerCase() });
      }
      start = j + 1;
    }
  }
  if (stack.length || rules.length !== [...clean.matchAll(/!\s*important\b/gi)].length) {
    fail("unsupported_style_context", "rule grammar");
  }
  return rules;
}

export function selectorMayMatch(selector, tag, classes) {
  // Split only outside functional/attribute selectors. No negative pseudo class
  // supplies a required class. Unsupported syntax always remains may-match.
  let depth = 0, square = 0, quote = "", part = "";
  const alternatives = [];
  for (const c of selector) {
    if (quote) {
      if (c === quote) quote = "";
      part += c;
      continue;
    }
    if (c === '"' || c === "'") {
      quote = c;
      part += c;
      continue;
    }
    if (c === "(") depth++;
    if (c === ")") depth--;
    if (c === "[") square++;
    if (c === "]") square--;
    if (depth < 0 || square < 0) return true;
    if (c === "," && !depth && !square) {
      alternatives.push(part);
      part = "";
    } else part += c;
  }
  if (depth || square || quote) return true;
  alternatives.push(part);
  return alternatives.some((alternative) => {
    let right = "", nesting = 0, brackets = 0;
    for (const c of alternative.trim()) {
      if (c === "(") nesting++;
      if (c === ")") nesting--;
      if (c === "[") brackets++;
      if (c === "]") brackets--;
      if (!nesting && !brackets && /[\s>+~]/.test(c)) right = "";
      else right += c;
    }
    // Only the positive simple prefix can prove disjointness. Everything after
    // a pseudo/attribute is ignored, including classes inside :not/:is/:has.
    const prefix = right.split(/[:\[]/, 1)[0];
    if (!/^(?:[a-zA-Z][a-zA-Z0-9-]*|\*)?(?:[.#][a-zA-Z_][a-zA-Z0-9_-]*)*$/.test(prefix)) {
      return true;
    }
    const type = /^[a-zA-Z][a-zA-Z0-9-]*/.exec(prefix)?.[0];
    if (type && type.toLowerCase() !== tag.toLowerCase()) return false;
    for (const m of prefix.matchAll(/\.([a-zA-Z_][a-zA-Z0-9_-]*)/g)) {
      if (!classes.has(m[1])) return false;
    }
    return true;
  });
}

function stylesheetsContext(stylesheets) {
  if (!Array.isArray(stylesheets)) fail("unsupported_style_context");
  const rules = [];
  let total = 0;
  for (const sheet of stylesheets) {
    if (!plain(sheet) || typeof sheet.text !== "string") fail("unsupported_style_context");
    total += bytes(sheet.text);
    if (total > 4 * LIMIT.css || /@import|expression\s*\(|javascript\s*:/i.test(sheet.text)) {
      fail("unsupported_style_context", "unknown cascade input");
    }
    const actual = sha(sheet.text);
    if (sheet.sha256 !== undefined && actual !== sheet.sha256) fail("stylesheet_hash_mismatch");
    if (actual === DOCUMENTER_LIGHT_SHA256 && sheet.sha256 === actual) {
      rules.push(...pinnedCSSRules(sheet.text));
      continue;
    }
    if (ANCILLARY_CSS_SHA256.has(actual) && sheet.sha256 === actual) {
      rules.push(...pinnedCSSRules(sheet.text).map((rule) => ({ ...rule, selector: null })));
      continue;
    }
    if (/\/\*/.test(sheet.text) || (sheet.sha256 !== CSS_SHA256 && /\\/.test(sheet.text))) {
      fail("unsupported_style_context", "unreviewed CSS grammar");
    }
    let matched = 0;
    for (
      const match of sheet.text.matchAll(/(?:^|[;{])\s*([-a-zA-Z]+)\s*:[^;{}]*!\s*important\b/gi)
    ) {
      matched++;
      rules.push({ selector: null, property: match[1].toLowerCase() });
    }
    if (matched !== [...sheet.text.matchAll(/!\s*important\b/gi)].length) {
      fail("unsupported_style_context");
    }
  }
  // Preserve the former eager global-grammar refusal for every stylesheet
  // outside the exact Documenter selector adapter, even an empty math batch.
  for (const { selector, property } of rules) {
    if (
      selector === null && propertyAtoms(property) === null && !DISJOINT_IMPORTANT.has(property)
    ) {
      fail("unsupported_style_context", "unknown important property");
    }
  }
  return (tag, classText) => {
    const important = new Set(), classes = new Set((classText ?? "").split(/\s+/));
    for (const { selector, property } of rules) {
      if (selector !== null && !selectorMayMatch(selector, tag, classes)) continue;
      const atoms = propertyAtoms(property);
      if (atoms === null) {
        if (!DISJOINT_IMPORTANT.has(property)) {
          fail("unsupported_style_context", "unknown important property");
        }
      } else for (const atom of atoms) important.add(atom);
    }
    return important;
  };
}
// KaTeX0.16.8 accent.js:153-175 (SHA87a5cb4b...7c4f09) derives these
// intrinsic width/margin pairs from character skew. This finite subset is not
// an authored calc grammar; only the verified renderer's private path uses it.
const ACCENT_WIDTHS = new Map([
  ["calc(100% - 0.0556em)", "0.0556em"],
  ["calc(100% - 0.1111em)", "0.1111em"],
]);
function declarations(text, important, intrinsicAccent = false) {
  if (!text || /[\\&<>!]|url\s*\(|expression\s*\(|var\s*\(/i.test(text)) fail("unsupported_style");
  const list = [];
  for (const field of text.split(";")) {
    if (!field.trim()) continue;
    const match = /^\s*([-a-z]+)\s*:\s*([^:;]+?)\s*$/.exec(field);
    if (!match) fail("unsupported_style");
    const [, property, value] = match;
    let valid = false;
    if (LENGTH_PROPS.has(property)) {
      valid = LENGTH.test(value) && Number.isFinite(parseFloat(value));
      if (property === "width" && intrinsicAccent && ACCENT_WIDTHS.has(value)) valid = true;
    } else if (
      property === "color" || property === "background-color" || property === "border-color"
    ) {
      valid = /^(?:#[a-fA-F0-9]{3,8}|[a-zA-Z]+)$/.test(value);
    } else if (property === "position") valid = /^(?:relative|absolute)$/.test(value);
    else if (property === "border-style") valid = /^(?:solid|dashed|dotted|none)$/.test(value);
    if (!valid) fail("unsupported_style", property);
    if (
      important.has("*") ||
      (propertyAtoms(property) ?? [property]).some((atom) => important.has(atom))
    ) {
      fail("unsupported_style_context", property);
    }
    list.push([property, value]);
  }
  if (!list.length) fail("unsupported_style");
  const intrinsic = list.find(([property, value]) =>
    property === "width" && ACCENT_WIDTHS.has(value)
  );
  if (intrinsic) {
    const widths = list.filter(([property]) => property === "width");
    const margins = list.filter(([property]) => property === "margin-left");
    if (
      widths.length !== 1 || margins.length !== 1 ||
      margins[0][1] !== ACCENT_WIDTHS.get(intrinsic[1])
    ) fail("unsupported_style", "intrinsic accent pair");
  }
  return list;
}

export function externalizeStyles(markup, { stylesheets } = {}) {
  return externalizeMathStyles(markup, stylesheets, false);
}

function externalizeEngineStyles(markup, important) {
  return externalizeMathStyles(markup, important, true);
}

function externalizeMathStyles(markup, context, engineGenerated) {
  if (typeof markup !== "string" || bytes(markup) > LIMIT.markup) fail("markup_limit");
  // Raw callers build their own context. The renderer alone supplies its local
  // immutable rule closure, compiled once before the asynchronous ESM import.
  // It still returns a fresh per-node important set for each tag/class pair.
  const important = engineGenerated ? context : stylesheetsContext(context);
  const groups = new Map();
  const stack = [];
  let output = "", position = 0, tokens = 0;
  // This scanner recognizes only KaTeX's closed static markup vocabulary. It is
  // not a permissive browser HTML parser and never repairs unknown/malformed input.
  while (position < markup.length) {
    if (++tokens > 50000 || stack.length > 512) fail("markup_limit");
    if (markup[position] !== "<") {
      const end = markup.indexOf("<", position);
      const text = markup.slice(position, end < 0 ? markup.length : end);
      if (text.includes(">")) fail("unsupported_markup");
      output += text;
      position += text.length;
      continue;
    }
    const end = markup.indexOf(">", position);
    if (end < 0) fail("unsupported_markup");
    const token = markup.slice(position, end + 1);
    const closing = /^<\/([a-zA-Z][a-zA-Z0-9]*)\s*>$/.exec(token);
    if (closing) {
      if (stack.pop()?.tag !== closing[1]) fail("unsupported_markup");
      output += token;
      position = end + 1;
      continue;
    }
    const start = /^<([a-zA-Z][a-zA-Z0-9]*)([\s\S]*?)(\/?)>$/.exec(token);
    if (!start || !TAGS.has(start[1])) fail("unsupported_markup");
    const [, tag, attrText, selfClosing] = start;
    const attrs = new Map();
    const attribute = /\s+([A-Za-z][A-Za-z0-9:-]*)\s*=\s*(?:"([^"<>]*)"|'([^'<>]*)')/gy;
    let offset = 0;
    while (offset < attrText.length) {
      if (!attrText.slice(offset).trim()) break;
      attribute.lastIndex = offset;
      const match = attribute.exec(attrText);
      if (!match || attrs.has(match[1])) fail("unsupported_markup");
      const name = match[1], value = decode(match[2] ?? match[3]);
      const permitted = COMMON.has(name) ||
        (tag === "svg" || tag === "path" || tag === "line"
          ? SVG_ATTRS.has(name)
          : tag !== "span" && MATH_ATTRS.has(name));
      if (!permitted || name.toLowerCase().startsWith("on")) fail("unsupported_markup", name);
      if (name !== "style" && /javascript\s*:|data\s*:|blob\s*:|url\s*\(/i.test(value)) {
        fail("unsupported_markup");
      }
      if (
        name === "xmlns" &&
        !["http://www.w3.org/1998/Math/MathML", "http://www.w3.org/2000/svg"].includes(value)
      ) {
        fail("unsupported_markup");
      }
      if (name === "class" && (!/^[A-Za-z0-9_ .-]*$/.test(value) || /katex-error/.test(value))) {
        fail("unsupported_markup");
      }
      attrs.set(name, value);
      offset = attribute.lastIndex;
    }
    if (attrs.has("style")) {
      const original = attrs.get("style");
      const intrinsicAccent = engineGenerated && tag === "span" &&
        attrs.get("class") === "svg-align" &&
        stack.some((ancestor) => ancestor.classes.has("mord") && ancestor.classes.has("accent"));
      const values = declarations(original, important(tag, attrs.get("class")), intrinsicAccent);
      const className = `qcl-math-${sha(original)}`;
      groups.set(
        className,
        values.map(([property, value]) => `${property}:${value}!important;`).join(""),
      );
      if (groups.size > LIMIT.groups) fail("style_group_limit");
      attrs.delete("style");
      attrs.set("class", `${attrs.get("class") ?? ""} ${className}`.trim());
    }
    output += `<${tag}`;
    for (const [key, value] of attrs) output += ` ${key}="${escapeAttribute(value)}"`;
    output += selfClosing ? "/>" : ">";
    if (!selfClosing) {
      stack.push({ tag, classes: new Set((attrs.get("class") ?? "").split(/\s+/)) });
    }
    position = end + 1;
  }
  if (stack.length) fail("unsupported_markup");
  if (bytes(output) > LIMIT.markup) fail("markup_limit");
  const css = [...groups].map(([name, value]) => `.${name}{${value}}`).join("\n");
  if (bytes(css) > LIMIT.css) fail("math_css_limit");
  return { html: output, css, groups: groups.size };
}

async function verifiedModule(inputs) {
  if (!plain(inputs) || !isAbsolute(inputs.modulePath ?? "")) fail("module_hash_mismatch");
  if (inputs.moduleSha256 !== MODULE_SHA256) fail("module_hash_mismatch");
  const path = inputs.modulePath;
  const stat = await lstat(path);
  if (
    !stat.isFile() || stat.isSymbolicLink() || stat.size > 1048576 ||
    await realpath(path) !== resolve(path)
  ) {
    fail("module_hash_mismatch");
  }
  const raw = await readFile(path);
  if (sha(raw) !== MODULE_SHA256) fail("module_hash_mismatch");
  if (inputs.version !== "0.16.8") fail("module_version_mismatch");
  return path;
}

function renderStyleContext(inputs) {
  const complete = own(inputs, "completeStylesheets");
  const sheets = complete ? inputs.completeStylesheets : inputs.stylesheets;
  const validate = (items) => {
    if (!Array.isArray(items) || !items.length || items.length > 1024) {
      fail("stylesheet_hash_mismatch");
    }
    const paths = new Map();
    let total = 0;
    for (const sheet of items) {
      if (
        !plain(sheet) || typeof sheet.text !== "string" || typeof sheet.path !== "string" ||
        !/^[A-Za-z0-9_][A-Za-z0-9_./-]*\.css$/.test(sheet.path) ||
        sheet.path.split("/").some((part) => !part || part.startsWith(".")) ||
        !/^[a-f0-9]{64}$/.test(sheet.sha256) || sha(sheet.text) !== sheet.sha256
      ) {
        fail("stylesheet_hash_mismatch");
      }
      if (paths.has(sheet.path)) fail("unsupported_style_context", "duplicate stylesheet path");
      paths.set(sheet.path, sheet.sha256);
      total += bytes(sheet.text);
      if (total > 4 * LIMIT.css) fail("unsupported_style_context", "stylesheet context limit");
    }
    if (items.filter((sheet) => sheet.sha256 === CSS_SHA256).length !== 1) {
      fail("stylesheet_hash_mismatch", "required exact KaTeX CSS");
    }
    return paths;
  };
  const primary = validate(inputs.stylesheets);
  const context = validate(sheets);
  for (const [path, hash] of primary) {
    if (context.get(path) !== hash) fail("stylesheet_hash_mismatch", "omitted consumed stylesheet");
  }
  const files = sheets.map(({ path, sha256 }) => ({ path, sha256 }));
  return {
    sheets,
    metadata: {
      complete,
      files,
      sha256: sha(JSON.stringify(files)),
      authority: complete ? "caller_supplied_complete_list" : "private_partial_context",
    },
  };
}

export async function renderMathBatch(records, inputs) {
  // Hash-before-import is deliberately first, including before stylesheet/source
  // validation: wrong-file sentinel code can never be executed as a dependency.
  const path = await verifiedModule(inputs);
  if (!Array.isArray(records) || records.length > LIMIT.records) fail("batch_limit");
  const serialized = JSON.stringify(records);
  if (bytes(serialized) > LIMIT.batch) fail("batch_limit");
  const identities = new Set();
  for (const record of records) {
    recordShape(record);
    const identity = `${record.page}\0${record.selector}`;
    if (identities.has(identity)) fail("math_mapping_mismatch");
    identities.add(identity);
    sourceGate(record.tex);
  }
  const styleContext = renderStyleContext(inputs);
  const important = stylesheetsContext(styleContext.sheets);
  // Import the supported public default ESM only; no named/internal API/plugins.
  // Prepared input directory must remain immutable for the whole admitted attempt.
  const katex = (await import(pathToFileURL(path).href)).default;
  if (katex.version !== "0.16.8" || typeof katex.renderToString !== "function") {
    fail("module_version_mismatch");
  }
  const output = [], cssGroups = new Map();
  let aggregate = 0;
  for (const record of records) {
    let html;
    try {
      html = katex.renderToString(record.tex, {
        displayMode: record.display,
        output: "htmlAndMathml",
        throwOnError: true,
        strict: "error",
        trust: false,
        macros: {},
        maxExpand: 1000,
        maxSize: Number.POSITIVE_INFINITY,
        globalGroup: false,
      });
    } catch (error) {
      if (/Too many expansions|infinite loop|maximum.*expan/i.test(error.message)) {
        fail("expansion_limit");
      }
      fail("unsupported_tex");
    }
    // No fallback colored command text is accepted. The lexical gate blocks its
    // upstream source triggers; closed markup guards also reject active resources.
    if (bytes(html) > LIMIT.markup) fail("markup_limit");
    const transformed = externalizeEngineStyles(html, important);
    aggregate += bytes(transformed.html);
    if (aggregate > LIMIT.total) fail("aggregate_markup_limit");
    for (const line of transformed.css.split("\n").filter(Boolean)) {
      cssGroups.set(line.slice(0, line.indexOf("{")), line);
    }
    if (cssGroups.size > LIMIT.groups) fail("style_group_limit");
    output.push({ ...record, html: transformed.html });
  }
  const css = [...cssGroups.values()].join("\n");
  if (bytes(css) > LIMIT.css) fail("math_css_limit");
  validateMathMapping(
    records,
    output.map((record) => ({
      page: record.page,
      selector: record.selector,
      tex: record.tex,
      tex_sha256: record.tex_sha256,
      display: record.display,
    })),
  );
  return {
    records: output,
    css,
    source_fingerprints: records.map(({ page, selector, tex_sha256 }) => ({
      page,
      selector,
      tex_sha256,
    })),
    license_status: "not_evaluated",
    options_policy_sha256: sha(
      "katex-0.16.8;htmlAndMathml;strict=error;trust=false;fresh-macros;maxExpand=1000;maxSize=Infinity;globalGroup=false",
    ),
    module_sha256: MODULE_SHA256,
    stylesheet_sha256: CSS_SHA256,
    stylesheet_context: styleContext.metadata,
    supervision: { required: true, wall_seconds: 60, cpu_ram: "external_admission" },
  };
}
