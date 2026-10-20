/** DOC04 phase-1 source only. Requires a separately authorized local Node unit run.
 * No Julia, Documenter, browser, network, npm install, or font publication.
 * Explicit local module identity is mandatory; missing prerequisites never skip.
 */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  externalizeStyles,
  renderMathBatch,
  validateMathMapping,
} from "../ops/docs/math-render.mjs";

const MODULE_SHA256 = "cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88";
const CSS_SHA256 = "df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e";
const sha = (value) => createHash("sha256").update(value).digest("hex");
const record = (tex, display = false, selector = "#eq-sigma") => ({
  page: "core/theory/09_scba.html",
  selector,
  tex,
  tex_sha256: sha(tex),
  display,
});

async function exactInputs() {
  const root = process.env.DOC04_KATEX_ROOT;
  assert.ok(root, "DOC04_KATEX_ROOT must identify the supplied immutable 0.16.8 distribution");
  const modulePath = join(root, "dist/katex.mjs");
  const cssPath = join(root, "dist/katex.min.css");
  // Independent fixture binding before any target import; no source tree fallback.
  assert.equal(sha(await readFile(modulePath)), MODULE_SHA256);
  assert.equal(sha(await readFile(cssPath)), CSS_SHA256);
  return {
    modulePath,
    moduleSha256: MODULE_SHA256,
    version: "0.16.8",
    stylesheets: [{
      path: "assets/vendor/katex/0.16.8/katex.min.css",
      text: await readFile(cssPath, "utf8"),
      sha256: CSS_SHA256,
    }],
  };
}
const codeIs = (code) => (error) => error?.code === code;

// Each assertion catches a bridge policy mutation, not KaTeX's upstream tests.
test("verified default ESM renders static HTML+MathML and retains exact source occurrence", async () => {
  const source = record(String.raw`\Sigma^r(E)=\frac{1}{2}\left(E_i^2+E_j^2\right)`, true);
  const result = await renderMathBatch([source], await exactInputs());
  assert.equal(result.records.length, 1);
  const output = result.records[0];
  assert.equal(output.page, source.page);
  assert.equal(output.selector, "#eq-sigma");
  assert.equal(output.tex_sha256, source.tex_sha256);
  assert.equal(output.tex, source.tex);
  assert.match(output.html, /<math[\s>]/);
  assert.match(output.html, /encoding="application\/x-tex"/);
  assert.match(output.html, /katex-html/);
  assert.doesNotMatch(output.html, /\sstyle\s*=|<style[\s>]|<script[\s>]|\son\w+\s*=/i);
  assert.ok(result.css.length > 0, "fraction/layout styles must be externalized");
  assert.match(result.css, /!important/);
  assert.equal(result.source_fingerprints[0].tex_sha256, sha(source.tex));
  assert.equal(result.license_status, "not_evaluated", "math unit rendering cannot admit fonts");
});

test("module hash mismatch fails before target import and preserves original input", async () => {
  const temporary = await mkdtemp(join(tmpdir(), "doc04-module-"));
  try {
    const modulePath = join(temporary, "wrong.mjs");
    await writeFile(modulePath, 'throw new Error("SENTINEL_IMPORT_MUST_NOT_RUN");');
    const source = record("x");
    await assert.rejects(
      renderMathBatch([source], {
        modulePath,
        moduleSha256: MODULE_SHA256,
        version: "0.16.8",
        stylesheets: [],
      }),
      codeIs("module_hash_mismatch"),
    );
    assert.equal(source.tex, "x");
  } finally {
    await rm(temporary, { recursive: true, force: true });
  }
});

test("wrong claimed version never falls back to another installed KaTeX", async () => {
  const inputs = await exactInputs();
  await assert.rejects(
    renderMathBatch([record("x")], { ...inputs, version: "0.16.9" }),
    codeIs("module_version_mismatch"),
  );
});

test("definition and resource commands fail without colored unsupported fallback", async () => {
  const inputs = await exactInputs();
  const prohibited = [
    String.raw`\def\x{1}\x`,
    String.raw`\gdef\x{1}`,
    String.raw`\edef\x{1}`,
    String.raw`\xdef\x{1}`,
    String.raw`\let\x=y`,
    String.raw`\futurelet\x y`,
    String.raw`\global\def\x{1}`,
    String.raw`\long\def\x{1}`,
    String.raw`\newcommand{\x}{1}`,
    String.raw`\renewcommand{\x}{1}`,
    String.raw`\providecommand{\x}{1}`,
    String.raw`\csname x\endcsname`,
    String.raw`\catcode1=2`,
    String.raw`\href{https://example.org}{x}`,
    String.raw`\url{https://example.org}`,
    String.raw`\includegraphics{x.png}`,
    String.raw`\htmlClass{x}{y}`,
    String.raw`\htmlId{x}{y}`,
    String.raw`\htmlStyle{color:red}{y}`,
    String.raw`\htmlData{x=y}{z}`,
    String.raw`\input{x}`,
    String.raw`\include{x}`,
    String.raw`\usepackage{x}`,
    String.raw`\require{x}`,
    String.raw`\read1`,
    String.raw`\write1`,
    String.raw`\openout1`,
    String.raw`\message{x}`,
    String.raw`\errmessage{x}`,
    String.raw`\show x`,
  ];
  for (const tex of prohibited) {
    await assert.rejects(renderMathBatch([record(tex)], inputs), codeIs("unsupported_source"), tex);
  }
});

test("lexer respects comments and escaped backslashes while preserving original TeX", async () => {
  const inputs = await exactInputs();
  const tex = "x % \\def\\bad{1}\n + y";
  const output = await renderMathBatch([record(tex)], inputs);
  assert.equal(output.records[0].tex, tex);
  assert.equal(output.records[0].tex_sha256, sha(tex));
  // A TeX linebreak control token followed by letters is not a macro definition.
  const escaped = String.raw`\begin{matrix}a\\def\end{matrix}`;
  assert.equal((await renderMathBatch([record(escaped)], inputs)).records[0].tex, escaped);
});

test("unknown TeX, authored sizing and cross-expression macro state are not repaired", async () => {
  const inputs = await exactInputs();
  await assert.rejects(
    renderMathBatch([record(String.raw`\DOC04UnknownCommand`)], inputs),
    codeIs("unsupported_tex"),
  );
  await assert.rejects(
    renderMathBatch([record(String.raw`\rule{100000em}{1em}`)], inputs),
    codeIs("unsupported_source"),
  );
  await assert.rejects(
    renderMathBatch([
      record(String.raw`\newcommand{\x}{1}`),
      record(String.raw`\x`, false, "#eq-next"),
    ], inputs),
    codeIs("unsupported_source"),
  );
  assert.equal((await renderMathBatch([record("x+1")], inputs)).records[0].tex, "x+1");
});

test("UTF-8 bytes and macro expansions are bounded without clamping geometry", async () => {
  const inputs = await exactInputs();
  await assert.rejects(renderMathBatch([record("α".repeat(8193))], inputs), codeIs("tex_limit"));
  await assert.rejects(
    renderMathBatch([record(String.raw`\dots `.repeat(1001))], inputs),
    codeIs("expansion_limit"),
  );
  const valid = await renderMathBatch([record(String.raw`\dots+x`)], inputs);
  assert.equal(valid.records[0].tex, String.raw`\dots+x`);
});

test("record shape/hash/mapping errors cannot select arbitrary HTML or dollar text", async () => {
  const inputs = await exactInputs();
  await assert.rejects(
    renderMathBatch([{ ...record("x"), tex_sha256: "0".repeat(64) }], inputs),
    codeIs("tex_hash_mismatch"),
  );
  await assert.rejects(
    renderMathBatch([{ ...record("x"), trust: true }], inputs),
    codeIs("record_shape"),
  );
  const source = record("x");
  validateMathMapping([source], [{ ...source }]);
  assert.throws(
    () => validateMathMapping([source], [{ ...source, selector: "#price" }]),
    codeIs("math_mapping_mismatch"),
  );
  assert.throws(() => validateMathMapping([source], []), codeIs("math_mapping_mismatch"));
  assert.throws(
    () => validateMathMapping([source], [source, source]),
    codeIs("math_mapping_mismatch"),
  );
});

test("style extraction retains ordered duplicates, units and semantic MathML/SVG", () => {
  const markup =
    '<span style="height:1em;height:2em;margin-right:0.05em"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>x</mi></math><svg viewBox="0 0 1 1"><path d="M0 0 L1 1"></path></svg></span>';
  const result = externalizeStyles(markup, { stylesheets: [] });
  assert.doesNotMatch(result.html, /\sstyle=/);
  assert.match(result.html, /<mi>x<\/mi>/);
  assert.match(result.html, /viewBox="0 0 1 1"/);
  assert.match(result.html, /d="M0 0 L1 1"/);
  assert.match(result.css, /height:1em\s*!important;\s*height:2em\s*!important/);
  assert.match(result.css, /margin-right:0\.05em\s*!important/);
  const same = externalizeStyles(markup, { stylesheets: [] });
  assert.equal(same.html, result.html);
  assert.equal(same.css, result.css);
});

test("important conflicts and unsafe dynamic style grammars fail closed", () => {
  assert.throws(() =>
    externalizeStyles('<span class="katex" style="height:1em">x</span>', {
      stylesheets: [{ path: "fixture.css", text: ".katex{height:2em!important}" }],
    }), codeIs("unsupported_style_context"));
  for (
    const style of [
      "height:1em!important",
      "color:var(--x)",
      "background:url(https://example.org/x)",
      "height:expression(alert(1))",
      "height:NaNem",
      String.raw`height:\31 em`,
    ]
  ) {
    assert.throws(
      () => externalizeStyles(`<span style="${style}">x</span>`, { stylesheets: [] }),
      codeIs("unsupported_style"),
    );
  }
});

test("unknown active/resource markup cannot become static math", () => {
  for (
    const html of [
      "<script>x</script>",
      '<img src="x">',
      '<a href="x">x</a>',
      "<svg><foreignObject>x</foreignObject></svg>",
      '<span onclick="x">x</span>',
      '<span style="height:1em" data-unknown="x">x</span>',
    ]
  ) {
    assert.throws(() => externalizeStyles(html, { stylesheets: [] }), codeIs("unsupported_markup"));
  }
});

test("important shorthands and all cannot change extracted longhand geometry", () => {
  const cases = [
    ["margin:1em", "margin-right:0.05em"],
    ["padding:1em", "padding-left:0.05em"],
    ["border:1px solid red", "border-bottom-width:0.04em"],
    ["border-width:1px", "border-bottom-width:0.04em"],
    ["border-top:1px solid red", "border-color:blue"],
    ["font:20px serif", "font-size:1em"],
    ["background:red", "background-color:blue"],
    ["inset:1em", "top:0.05em"],
    ["margin-inline:1em", "margin-right:0.05em"],
    ["all:initial", "height:1em"],
  ];
  for (const [important, inline] of cases) {
    assert.throws(
      () =>
        externalizeStyles(`<span class="katex" style="${inline}">x</span>`, {
          stylesheets: [{ path: "fixture.css", text: `.katex{${important}!important}` }],
        }),
      codeIs("unsupported_style_context"),
      important,
    );
  }
  const healthy = externalizeStyles('<span class="katex" style="height:1em">x</span>', {
    stylesheets: [{ path: "fixture.css", text: ".katex{opacity:0.5!important}" }],
  });
  assert.match(healthy.css, /height:1em!important/);
  for (
    const text of [
      ".katex{unknown-shorthand:1em!important}",
      String.raw`.katex{mar\67in:1em!important}`,
    ]
  ) {
    assert.throws(() =>
      externalizeStyles('<span style="height:1em">x</span>', {
        stylesheets: [{ path: "fixture.css", text }],
      }), codeIs("unsupported_style_context"));
  }
});

test("render bridge binds a complete supplied stylesheet context beyond pinned KaTeX", async () => {
  const inputs = await exactInputs();
  const light = {
    path: "assets/runtime/light.css",
    text: ".docs-main{background:#fff;color:#111}",
  };
  const completeStylesheets = [...inputs.stylesheets, { ...light, sha256: sha(light.text) }];
  const result = await renderMathBatch([record("x+1")], { ...inputs, completeStylesheets });
  assert.equal(result.stylesheet_context.complete, true);
  assert.deepEqual(
    result.stylesheet_context.files,
    completeStylesheets.map(({ path, sha256 }) => ({ path, sha256 })),
  );
  assert.equal((await renderMathBatch([record("x+1")], inputs)).stylesheet_context.complete, false);
  const conflictText = ".katex{all:initial!important}";
  await assert.rejects(
    renderMathBatch([record("x+1")], {
      ...inputs,
      completeStylesheets: [...inputs.stylesheets, {
        path: "assets/runtime/light.css",
        text: conflictText,
        sha256: sha(conflictText),
      }],
    }),
    codeIs("unsupported_style_context"),
  );
  await assert.rejects(
    renderMathBatch([record("x+1")], {
      ...inputs,
      completeStylesheets: [{ ...light, sha256: sha(light.text) }],
    }),
    codeIs("stylesheet_hash_mismatch"),
  );
  await assert.rejects(
    renderMathBatch([record("x+1")], {
      ...inputs,
      completeStylesheets: [...inputs.stylesheets, { ...light, sha256: "0".repeat(64) }],
    }),
    codeIs("stylesheet_hash_mismatch"),
  );
  await assert.rejects(
    renderMathBatch([record("x+1")], {
      ...inputs,
      stylesheets: completeStylesheets,
      completeStylesheets: inputs.stylesheets,
    }),
    codeIs("stylesheet_hash_mismatch"),
  );
});

test("all eleven pinned KaTeX authored size primitives are unsupported without rewriting", async () => {
  const inputs = await exactInputs();
  const commands = [
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
  ];
  for (const command of commands) {
    const tex = `\\${command} x`;
    await assert.rejects(
      renderMathBatch([record(tex)], inputs),
      codeIs("unsupported_source"),
      command,
    );
  }
  const tex = "x+1";
  const healthy = await renderMathBatch([record(tex)], inputs);
  assert.equal(healthy.records[0].tex, tex);
  assert.equal(healthy.records[0].tex_sha256, sha(tex));
});

test("all sixteen pinned manual delimiter sizes fail while automatic stretch remains supported", async () => {
  const inputs = await exactInputs();
  const commands = [
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
  ];
  for (const command of commands) {
    await assert.rejects(
      renderMathBatch([record(`\\${command} (`)], inputs),
      codeIs("unsupported_source"),
      command,
    );
  }
  const tex = String.raw`\left(\frac{x}{2}\right)`;
  assert.equal((await renderMathBatch([record(tex)], inputs)).records[0].tex, tex);
});
