# DOC04/DOC06 — точный маршрут Root checks и full CI

2026-10-20. Source-only D ultra; независимый high R перед I. Root published
`e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, worktree clean, все8 gitlinks
совпали. Product edits, target imports, tests/build/network и full CI dispatch=0.
Единственный final full CI остаётся неиспользованным; этот design не разрешает
его запуск или automatic rerun.

## 1. Подтверждённая проблема и выбор

Pinned Deno2.8.3 help явно включает *_test.mjs в directory discovery и задаёт
`[files]... [-- [SCRIPT_ARG]...]`. Existing Root check запускает directory tests
с read/write/run=git, без env и без KaTeX binding. Поэтому Node-owned
tests/docs_math_test.mjs попадает в неверный runner; добавление env privilege
не исправило бы отсутствие exact source input. Future DOC06 test требует ровно
один explicit harness-owned /tmp аргумент и не может запускаться этой командой.

Выбран один минимальный маршрут: **сохранить имена/тела существующих unit files,
две точные discovery exceptions и обязательный отдельный запуск каждого unit в
полном aggregate check**. Не переименовывать frozen tests, не переводить Node
unit в Deno, не исключать все mjs или каталог docs. Исключение из base discovery
не означает skip: aggregate требует свои dedicated receipts перед pass.

Действующий DOC04 Python tests/test_docs_assembly.py также не входит в Root
check/test routes; включить его существующий unittest command в тот же mandatory
docs unit group. Новые assertions/framework не нужны. Это покрытие того же DOC04,
не расширение научной программы или запуск docs BUILD.

## 2. Owning I paths и default semantics

Изменять только Root deno.json,ops/ci.ts,.github/workflows/ci.yml,
.github/workflows/release.yml; добавить маленький Deno helper ops/docs_tests.ts
и focused routing controls tests/docs_test_routing_test.ts. Existing Node/Python/
DOC06 test bodies и adapter semantics остаются своими owning frozen inputs.
DOC06 adapter/test ещё не published в e22; их отсутствие блокирует full check,
а не разрешает пропустить unit. Candidate test SHA указан в source ledger,
но будущий final root должен связать собственные actual published bytes.

Task definitions, сохраняющие existing framework:

- `check:base`: прежняя цепочка fmt/lint/check, generic Deno suite,transfer:check,
  restore:check; у Deno test добавить **только**
  `--ignore=tests/docs_math_test.mjs` и
  `--ignore=tests/docs_static_slice_test.ts`. Existing read/write/run=git
  сохраняются; env/net/ffi/global run suite не получает.
- `check`: `deno run --allow-read --allow-write --allow-run ops/docs_tests.ts check`.
  Через `deno task check --inputs FILE` это обязательный aggregate base+docs.
- `docs:check`: тот же helper, mode=docs; только explicit docs group с inputs.
- `docs:preflight`: тот же helper, mode=preflight, read/write/run=git only;
  проверяет binding/prerequisites, **не запускает units** и не выдаёт test pass.

Helper не получает allow-env/net/ffi и не импортирует environment.ts. Его trusted
process-launch capability нужен для existing task/Node/Python/Deno subprocesses;
внутренний argv allowlist ограничен ниже. Он не распространяется на дочерние
Deno permission flags. Новых permissions generic suite нет. Не использовать -A.
Helper экспортирует pure plan/receipt functions и guarded import.meta.main,
чтобы generic routing test мог импортировать tooling без CLI side effect.

`check` без inputs выдаёт nonzero blocked/usage с объяснением exact prerequisite.
Он больше не является успешным неполным aggregate. `check:base` остаётся явной
командой для доступной независимой проверки; её receipt/title говорит base-only.
Никакого скрытого fallback из check в base, поиска cache/depot/latest или
skip-on-missing. Список mandatory aggregate steps фиксирован:
base,doc04-python,doc04-node,doc06-deno. Любой missing/blocked/failed/unknown
step препятствует full aggregate pass.

## 3. Prepared inputs: небольшой private harness descriptor

FILE —≤32KiB JSON от **уже admitted CI setup**, не runtime secret/config/plugin.
Это локальная metadata одного unit attempt, не DOC03 schema, asset lock, shared
API или новый generator. Exact fields:

```text
{format:'qcl-negf.docs-test-inputs.v1', source_revision,
 source_files:[{path,sha256}],
 tools:{deno:{path,version,sha256,receipt_ref},
        node:{path,version,sha256,receipt_ref},
        python:{path,version,sha256,receipt_ref}},
 katex:{root,version,module_sha256,css_sha256,source_receipt_ref},
 storage:{owned_tmp_root,attempt_dir,deno_cache_dir},
 admission_ref:{path,sha256},
 limits:{per_step_wall_seconds,per_step_log_bytes,total_log_bytes,
         cpu,ram_bytes,node_tmp_bytes,python_tmp_bytes,doc06_tmp_bytes}}
```

Additional fields refuse; scalar/path/size/hash validation finite. References
bind retained exact receipt bytes, not booleans claiming approval. External fresh
builder inventory/admission establishes who owns tools/dirs/process-tree budget;
the helper checks consistency with that trusted handoff and exact source graph.
It does not invent native proof from a JSON status label. Actual interpreter
version/hash/cache identities are prerequisites, not claimed measured here.

Required source_files: the helper/routing/task files, Node test+math bridge,
Python test+assembler, DOC06 test+adapter at this exact final source revision.
No byte-for-byte reuse across a changed test/helper/source contract without
rebinding. Root sourceGraph before/after checks remains authoritative; no second
manual component revision lock. Descriptor/input/outputs live outside source tree.

KaTeX source-only unit input is exact0.16.8 local distribution with module SHA
cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88 and CSS SHA
df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e,
matching frozen Node unit/accepted binding. Preflight hashes bytes before any
target module import. Node unit independently binds them again. No npm install,
fetch, latest/depot fallback, live CDN or full font-publication assertion.
Public OFL/full DOC04 asset closure is **not** silently passed by this unit;
its license_status remains not_evaluated. It need not block this private software
unit once its actual consumed source input is admitted.

storage.owned_tmp_root is an explicit pre-created unique owned /tmp descendant,
not /tmp itself, a symlink or workspace path; visible in the actual CI job mount
namespace. Helper creates separate node/python/doc06 children beneath it.
DOC06 gets exactly its own child capability. attempt_dir is a fresh owned retained
output directory, disjoint from snapshot/workspace/tmp/cache. deno_cache_dir is
explicit admitted runtime cache: Deno's CLI cache behavior is separately budgeted,
not assumed to fit inside DOC06's8MiB fixture allowance. No implicit HOME/TMPDIR
or cache-path fallback. Canonical paths containing separators/control characters
that would alter comma-separated Deno permission lists are refused.

Node24/Python3.14/Deno are already in selected platform runner extraPackages;
Root devShell also has nodejs_24. Platform checks.operations is a component-local
check inherited by Root flake, not Root's tests directory. Do not add native
asset fetching, Root docs units or another Node package to those Nix checks.
Deno2.8.3 is required; exact patch/binary/NAR evidence comes from fresh setup.
No Nix/server/runner-module change is needed for this routing fix.

## 4. Exact child routes and least-capability split

All executable paths come from admitted tools and argv arrays, no shell eval.

1. Base: selected Deno executes `task check:base` in Root using the existing base
   environment/task behavior. Its existing permissions are unchanged.
2. DOC04 Python: selected Python executes
   `-m unittest discover -s tests -p test_docs_assembly.py` in Root. Uses existing
   trusted local assembler and literal fixtures, no package sync/Julia/docs build.
3. DOC04 Node: selected Node executes
   `--test --test-reporter=tap tests/docs_math_test.mjs` in Root. Environment is
   cleared and rebuilt only for this child with DOC04_KATEX_ROOT and its own
   explicit TMPDIR plus any measured indispensable native-loader fields admitted
   for this executable. Never pass NODE_OPTIONS/preload injection or global job
   secrets. Node remains the Node test runner.
4. DOC06 Deno: exact logical argv:

```text
test --no-config --no-lock --cached-only --no-npm --no-remote --reporter=tap
 --allow-read=ABS_TEST,ABS_ADAPTER,OWN_DOC06_TMP
 --allow-write=OWN_DOC06_TMP ABS_TEST -- OWN_DOC06_TMP
```

No allow-env/run/net/ffi, no workspace-wide read/write or temp/env inference.
Trusted test/adapter closure must be exactly bound; any additional tooling import
requires updating/reviewing the explicit allowlist. Child environment is cleared,
with only admitted DENO_DIR/native-loader fields needed by CLI. DENO_DIR does
not grant script env permission. The argument separator is pinned-help-supported;
test sees Deno.args=[OWN_DOC06_TMP]. Type checking stays enabled; no --no-check,
--permit-no-files, filter, only or ignored-tests shortcut.

The source descriptor records each expected unit test count from its reviewed
frozen test contract. Captured engine reports must have a positive expected count,
all passed,zero failed,zero skipped/ignored/todo; unknown summary format/count is
not pass. Node/Deno TAP formats and Python unittest summary are bound to selected
tool versions; source I tests their strict readers with manufactured reports.
Unsupported Node reporter/tool CLI is a native preflight incompatibility, not
an excuse to use Deno for Node or ignore coverage. No real unit is run in D.

## 5. ops/ci default and workflow routing — no duplicate docs execution

Extend ops/ci.ts strict parser with `--docs-inputs FILE` as data, independently
of scope flags. **all = no scope selectors**, even when input option is present.
Default/full mode requires it and first calls
`deno task check --inputs FILE` exactly once, then existing component Python/
Julia/infra branches. Outer sourceGraph before/after remains. Targeted --python,
--julia or --infra keep their prior targeted meaning and do not claim full Root
coverage; reject ignored --docs-inputs in a targeted invocation. No recursive
ops/ci→check→ops/ci path: helper check calls check:base and its dedicated units.

Integrated workflow keeps manual dispatch and cancel-in-progress:false.
Add optional string dispatch input docs_test_inputs (full requires it, smoke
does not). Bind it through a step-local environment value and quote it as one
CLI argument; never interpolate user text directly into shell command syntax.

- Full: after source graph, run docs:preflight with that FILE **before** heavy
  bootstrap/prepare. This is a prerequisite result, not unit pass. After the
  existing prepared environments stage, invoke
  `deno task test --docs-inputs "$DOCS_TEST_INPUTS"`. ops/ci performs the only
  Root aggregate check; remove the redundant full-mode standalone check step.
- runner-smoke: explicitly run `deno task check:base`, with a base-only step
  name, then existing account/routing/shared-slice checks. It does not require
  KaTeX/DOC06 inputs and is not a full-check/docs/native/scientific pass.
- Application-release workflow: required docs_test_inputs dispatch input;
  docs:preflight before bootstrap; replace the old check+test pair by the single
  full `deno task test --docs-inputs ...` call. Remaining release/build steps
  and their separate gates are unchanged.

Missing/unpublished DOC06 file, assets, tools, permissions, owned storage or
admission blocks the dependent full route before target execution. CI setup
must provide actual prepared inputs; design does not pretend such setup exists
or add automatic downloads. Run cheap local admitted source/unit validation
before the sole final CI is dispatched. A workflow failure still consumes its
actual attempt and does not authorize an automatic rerun.

## 6. Finite receipts and failure retention

Trusted helper uses bounded spawn with concurrent stdout/stderr drains, deadline,
byte caps and retained original streams; existing unbounded process.run helper
is not adequate for these dedicated unit receipts. No retry/fallback. External
admitted process-tree unit owns CPU/RAM/descendant termination; direct-child kill
alone is not proof. Input source/asset/descriptor/tool/admission hashes, argv,
scoped environment names and exact capability binding are captured privately.

Proposed per dedicated unit maxima:120s,1CPU/1GiB,each log≤1MiB,total≤4MiB;
DOC06 fixture TMP≤8MiB,Node/Python TMP≤32MiB each, separate admitted runtime-cache
budget. Actual grant can be smaller. These are software unit caps, not science
allowance changes or measured hard quotas. If supervision cannot enforce/capture
the required predicate, block or record failure rather than asserting measured0.

Per step receipt: name,source hashes,tool identity,attempt/input digest,argv,
start/end,exit/signal,expected/observed tests+failed/skipped,stdout/stderr SHA/bytes,
capture-complete,guards/stop/drain status,resource evidence/limitations and result.
Aggregate receipt declares the exact four required steps, each terminal status,
source before/after equality and pass only when all obligations are met. Missing
measurements=null/not_measured. A test command exit0 is software evidence only;
it does not establish docs rendering/browser/serving/native/restore/science.

Keep original failed streams/receipts and available owned TMP; no finally-delete
of failed aggregate artifacts. Existing Node tests clean some inner fixtures in
their own finally blocks; route receipts do not claim those files survive.
DOC06 already retains failed fixture directories. Sanitized summary may be linked
publicly, but raw private paths, environment values and inventories are not copied
into public docs. Context missing before a safe output path is established emits
bounded blocked stderr retained by caller, without fabricating an on-disk receipt.

## 7. Meaningful I controls and stop

Focused source I≤30min,1CPU/2GiB,read≤2MiB,output≤96KiB. High source review before
any separately bound pure RED/GREEN routing harness; no full CI for development.
Tests use injected fake executor/metadata and generated TAP/unittest reports,
not real Node/Julia/Nix/network. No test-body skip or permission weakening.

| Control | Required observable result |
| --- | --- |
| Generic plan | Exactly two dedicated exclusions; no env grant; existing base checks retained; a different future *_test.mjs is not silently excluded |
| Aggregate happy route | Base+Python+Node+DOC06 each exactly once; correct source/inputs,Node scoped env,DOC06 single argv and exact permissions; all four receipts required |
| Missing/wrong KaTeX hash/test/adapter/tool/context/capability | Block before dedicated spawn; no download/latest/fallback/all-pass summary |
| DOC06 argv/permission mutation | Missing/extra argument or env/run/net/ffi/workspace-wide grant rejected by planner/control before unit pass |
| Removed dedicated step or zero/ignored/TODO tests | Aggregate cannot pass even if remaining processes exit0 |
| Fake child failure/timeout/log overrun/drain error/source change | Original partial logs and TMP retained, proper nonzero aggregate, no rerun |
| CLI scopes | Input-only invocation remains all; targeted flags stay targeted; full workflows dispatch aggregate once,smoke explicitly base-only |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing directory discovery reaches Node file without its inputs | Pinned Deno help + current deno.json + Node env accessor | Reproduced as source fact; this D executes nothing | изменить |
| Dedicated route preserves both frameworks and DOC06 least capabilities | Explicit argv/inputs/aggregate contract above | Implementation and fresh unit receipts pending | изменить |
| Nix/runner modules need new tools/global privileges | Selected runner already includes Node24/Deno/Python; Root checks inherit component checks | Native identities still require fresh setup | сохранить |
| Full CI/docs BUILD/science ready now | DOC06 unpublished adapter and admitted test input descriptor missing | Source routing design is not readiness evidence | данных недостаточно |

STOP for independent high CP-DESIGN. No product/checkpoint/runtime/full-CI changes.
