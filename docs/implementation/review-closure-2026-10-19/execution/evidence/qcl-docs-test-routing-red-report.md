# DOC04/DOC06 routing — RED fixture source packet

Подготовлен только `tests/docs_test_routing_test.ts` в `/tmp/qcl-docs-test-routing-worktree`, ветка `codex/review-closure-docs-test-routing`, immutable base e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b. Worktree уже существовал чистым и был повторно использован. Попытка `worktree add -b` сообщила existing branch и ничего не изменила. Submodules не initialized:8 selected gitlinks наблюдены со знаком `-`; owning state не изменялся.

Frozen D1 fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270 + D2 bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70 и accepted high R939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967 применены совместно. Production helper/tasks/CI/workflows не создавались и не менялись. Existing Node/Python/DOC06 bodies не изменены.

## Exact future pure API

Fixture импортирует следующие именованные exports из будущего `../ops/docs_tests.ts`. Файла helper сейчас нет. API ниже — внутренний injection/control contract для source I, не новая публичная/shared JSON schema и не признание native receipt format.

| Export | Signature / observation |
| --- | --- |
| genericCheckPlan | `() -> {command:string,excluded:string[]}`; exact bound base chain и две discovery exceptions |
| parseInputs | `(text:string) -> Descriptor`; exact D2 whitelist, duplicates включая escaped keys, finite32KiB, literals/counts/paths/limits; malformed throws |
| preflightInputs | `(Descriptor,MetadataFacts) -> PreflightOutcome`; pure; ready result literal `ready_for_unit_attempt`, иначе blocked/failed + nonempty reasons; ready содержит input digest, bound descriptor/source context, versions и license_status |
| planChecks | `(mode:'check'/'docs',PreflightOutcome/null) -> Plan`; requires ready; null/blocked throws; scope full-root-check/docs-units-only, mutable steps и input_sha256 |
| validatePlan | `(Plan,ReadyOutcome) -> void`; rejects changed steps/order/count/source/input/tool/argv/env/caps before execute |
| runChecks | `async(Plan,ReadyOutcome,FakeExecutor) -> AggregateReceipt`; validates plan, invokes only exact plan steps, observes source graph, retains captures and finite failure states, no retry/cleanup |
| parseUnitReport | `(format:string,stdout:string,stderr:string,expected:number) -> UnitSummary`; supported literals D2; malformed either throws or non-passed result; complete healthy reports yield passed_unit |
| parseCiArgs | `(args:string[]) -> {all:boolean,scopes:string[],docsInputs:string/null}`; strict selectors/options and missing-input rejection |
| workflowRoute | `(mode:'full'/'application-release'/'runner-smoke',input:string/null) -> WorkflowRoute`; pure argv/order contract for later actual workflow/source binding |

`Descriptor` — exactly D2§2. `MetadataFacts` is constructed by local `metadata()` in the fixture and passed by value: workspace; source_graph{revision,digest,clean}; actual selected source_files hash map; base_task bytes; files map{kind,canonical,sha256}; directories map{kind,canonical,symlink_ancestors}; absent_paths; retained_tools; retained_katex; independent reviewed_units; admission facts from the trusted-reader double. The internal retained_tools.schema literal normalized-tool-identity denotes already normalized reader output, **not** a new persisted external receipt schema. Unknown normalized identity/ref/schema/hash/version blocks. Production must bind its actual external receipt parser/admission authority separately and must not accept a caller status label as that reader. No metadata double provides real ownership/native evidence.

Independent `reviewed_units` prevents changing positive expected counts while retaining test hashes. Synthetic fixture uses20/15/7 for Python/Node/DOC06 with fabricated source hashes. The7 is intentionally a manufactured DOC06 report count; it does not fill the missing final DOC06 published binding. Actual source-bound counts require future reviewed final bytes as D2 specifies.

`ReadyOutcome.versions[tool]` exposes evidence=retained_receipt_bound, measurement=null; license_status=not_evaluated. Preflight has no executor parameter or side-effect hook, uses no target imports or probes, and never returns passed. Its actual future module must remain safe to import under the no-env/no-run focused harness; import.meta.main gating and actual CLI integration remain production obligations.

Each mutable `Step` has name,kind,executable,args:string[],cwd,clearEnv,env:Record<string,string>,input_sha256,source_graph_digest,limits{wall_seconds,log_bytes}. Base is kind=base-task, task=check:base, inherited environment (`clearEnv:false`, env:{}); dedicated units are kind=dedicated-unit. Exact command paths/argv/maps are asserted independently from descriptor. Empty loader_env is mandatory; Node only KaTeX/TMPDIR, Python only own TMPDIR plus two fixed literals, Deno only its explicit CLI DENO_DIR. DOC06 script sees exactly one owned TMP arg after -- and exact3 read paths/one write path; no env/run/net/ffi/workspace privilege.

`FakeExecutor` has sourceGraph()->{revision,digest,clean} and async execute(Step)->Capture. Capture includes original stdout/stderr, exit_code:number/null,signal:string/null,started_at,ended_at,capture_complete,drains_complete,stop_reason:string/null,supervision{process_tree_owned,limits_enforced,evidence_ref}. These are synthetic observations, not measured physical quotas. No real executor, filesystem adapter or clock is present. Executor rejection is a terminal retained failure, not retry. AggregateReceipt contains result,scope,required_steps,steps,source_stable and retained{attempt_dir,owned_tmp_root,cleanup_attempted:false}. All4 required full step receipt names remain represented after failure (unexecuted obligations cannot become passed). Step receipts contain name,result,summary and executed capture; base summary is {status:not_applicable,reason:composite-task}, without numeric expected count. Dedicated summary contains exact expected/observed/passed/failed plus applicable engine counters; inapplicable counters use {status:not_applicable}. Failed raw captures are retained byte-for-byte; no native TMP retention or process-tree termination is claimed by synthetic controls.

`WorkflowRoute` has cancelInProgress:false, preflight and aggregate argv arrays, aggregateExecutions,standaloneCheckExecutions,order; smoke instead exposes scope=base-only,base argv,dedicatedUnits=not_requested,preflight:null,aggregateExecutions:0. These assertions check the future pure routing decision. They do not substitute for high review of actual deno.json/ops/ci.ts/workflow integration or prove shell quoting. Actual step-local env quoting, manual dispatch, preflight before heavy stages, and no duplicate full check still require source verification in production I.

## Controls, count and bounds

Source declaration arithmetic gives **207** Deno.test registrations (literal table/loop expansion), not an observed engine count. Group arithmetic is recorded in identity. These are routing contract tests, not repeated scientific runs. Healthy report counts20/15/7 are distinct from the207 fixture registrations and from assertion counts.

Coverage: exact old base chain/two exclusions; all4steps once; scoped docs-only/smoke; strict nested fields/duplicates/source/counts; dangerous storage spellings; all8 budget fields; retained source/tool/binary/receipt/admission mismatches; independent reviewed count binding; three supported healthy report formats; count±1/zero/skip/TODO/cancel/error/duplicate/unknown/truncated/bailout/filter summaries; DOC06 capability/argv/env mutations; Python/Node clean-env mutations; every step nonzero/deadline/log-cap/incomplete-drain/missing-supervision; source change; total log cap; executor launch rejection; retained original captures/TMP references; strict CLI scope and workflow dispatch decisions. No future mjs glob exception is introduced.

Future focused execution needs **no filesystem/env/run/net/ffi permissions**: only static import of future pure helper and Deno.test registration. It accepts no TMP argument and allocates no filesystem payload. The fake paths are data. A manufactured log-overrun string is1,048,577 characters;other finite controls/objects remain in ordinary JS memory. Assertion rendering clips actual/expected to300 chars each, so an assertion does not dump the log body. Root must separately bind its own finite RED/GREEN wall/log envelope and count contract before execution. No real base/full suite, Node/Python/Julia/Nix tool or --version probe may run in this fixture.

## Performed source checks / limitations

Only Git metadata and source/text authoring checks ran. `git status --short` contains exactly one untracked fixture. `git diff --no-index --check /dev/null tests/docs_test_routing_test.ts` emitted no whitespace diagnostics (new-file diff exit1 is expected). Source/patch hashes are frozen in identity. No Deno or other target parser/typecheck/formatter/test/build ran; fixture registration arithmetic is not runtime validation. RED is expected to fail because helper import is absent, but **RED has not been executed or measured**. No completion/pass claim is made for tests, CLI, real units, CI, rendering/native/science. Formatting/type availability remain independent review/execution limits of this source-only stage.

Named read bound conservatively≤1MiB<2MiB including full-file charges for extracts/repeated fixture reads and512KiB reserve; no recursive payload scan. Envelope≤25min/1CPU/2GiB/output96KiB. Physical I/O/RSS not instrumented. Original D/R and earlier resource failures are unchanged.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED fixture подготовлен без production drift | One new source path, hashes, independent manufactured expectations | Не запускался, helper отсутствует | изменить |
| Все required route obligations можно проверить без target execution | Fake executor/metadata/report tables и finite loops | Injection contract ещё требует high fixture R | дополнительно измерить |
| Expected counts/admission являются реальными | Только synthetic test data | Final descriptor/DOC06/native bindings отсутствуют | данных недостаточно |
| Full CI/units/native готовы или выполнены | Execution0, no actual production helper | Source fixture не admission/pass | данных недостаточно |

STOP для independent high fixture R; только затем Root bounded RED. Production implementation — отдельный этап.
