# DOC06 schema declaration correction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:subagent-driven-development or superpowers:executing-plans for the separately assigned I stage. This document is D only; it executes no product check.

**Goal:** восстановить принятые direct schema declarations fixed slice и честно сохранить неполноту validation, не изменяя научную задачу.

**Architecture:** Root adapter остаётся fixed source projection. Узкая проверка root `allOf` устанавливает только область применимости к root properties; условия не вычисляются. Direct declarations, partial validation coverage и authored scheduling context представлены отдельно в существующих Fact/Extraction shapes.

**Tech Stack:** существующий TypeScript/Deno adapter и inert fixture bytes; новых dependencies, публичных schema/Bundle/API нет.

**Spec:** frozen `/tmp/qcl-doc06-static-slice-design.md` SHA256 `34b80d4ae1c8b94d23657124f17c9051251cea4763af8f92007d24929aafb2e8`; independent high D review SHA256 `385c2ae4358a7fb296399d6d955eb4d9ac5995c26f8baa2c27526ad11677d5ce`; actual meaning review `/tmp/qcl-doc06-actual-meaning-review.md` SHA256 `4c35b2517718e3b9a137047a45652c4924de7e21ae3ad9041cd8d1e90df56861`.

## Global constraints

- D: только source/metadata reads и собственные report/identity/ledger writes; no target imports/parsers/product/tests/harness/native/network/SCI/build/CI/C08.
- Selected Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; dirty evidence сохраняется. Default cwd e48e5b2 — отдельный protected checkout, не authority.
- Adapter `ops/docs/static-slice.ts` SHA256 `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`; canonical tests `tests/docs_static_slice_test.ts` SHA256 `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69`.
- Exact actual snapshot `/tmp/qcl-DOC06-ACTUAL-2bb05d3-v1/snapshot`, nine files/245338 B; canonical Contracts and packaged Runner schema each54815 B/SHA256 `62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b`.
- Literal direct declaration не является instance validation, effective value/default или causal origin. Scientific equations/model/criteria, loader и owning schema не меняются.
- Existing limits/permissions/symlink protection/source binding/default isolation/sentinel controls сохраняются. Actual status/coverage остаются partial; exit0 и одинаковые SHA не закрывают semantic acceptance.
- Root — единственный будущий writer adapter+tests и executor/count writer. I: максимум2 source rounds. Этот D не создаёт grants. Root предлагает отдельный конечный milestone: максимум3 новых product calls —1 regression unit GREEN и2 новых actual projections; compiler/source checks до них. Старые unit2/2, E1 1/1, actual2/2 исчерпаны и сохраняются.

## Primary observation and exact allOf impact

Selected adapter `schemaProjection`: lines494–627; `allowed(root, objectKeys)` :550 вызывается до `/required` и local-ref traversal; root `allOf` отсутствует в allowlist. Catch :618–625 заменяет constraint/default/description общим failure; rootRequired остаётся изначальным leaf failure. Это объясняет A1 nulls без запуска: `facts.json` SHA256 `ead7c19658478682d9da3b966f5aaec2e0ec9a180a27b7c62442f5796b63e041`, receipt SHA256 `7bd0d68220ec0d37972b2cb25ad20b5f3b99078f95e06f64327727b446f7bd92`.

Схема :179–423 содержит ровно5 root allOf items. В каждом item верхние ключи только `if`,`then`, а каждое clause имеет только `properties`. Точные root scopes:

| JSON Pointer | if root properties / source lines | then root properties / source lines |
| --- | --- | --- |
| /allOf/0 | run :181–194 | algorithms :195–247 |
| /allOf/1 | run :250–260 | algorithms :261–342 |
| /allOf/2 | run :345–355 | run :356–366 |
| /allOf/3 | execution :369–379 | algorithms :380–390 |
| /allOf/4 | scattering :393–403 | physical :404–421 |

Nested `if/then` in /allOf/0/then/properties/algorithms and `anyOf` in /allOf/1/then/properties/algorithms remain within algorithms. Energy/volume refs :412–416 remain inside physical. These nodes do not become selected production constraints merely because nested keywords are unsupported. No condition is evaluated; no conclusion is made that the whole run is valid. This is a scoped source observation, not an assertion that all allOf are irrelevant.

Independent positive locators: root `/required` includes production :8–20; `/properties/production/$ref` :41–43 points to `#/$defs/production`; production required :1423–1435 includes energy_chunk; `/$defs/production/properties/energy_chunk` :1437–1441 has integer/minimum1/literal description/no own default keyword. Route :67 and :82–87 explicitly supplies scheduling context; typed64/example64 remain different source contexts.

## Correction contract

### 1. Scope classifier and failure isolation

Keep `schemaProjection(input: Input)` private and existing public `generateStaticSlice` unchanged. Extend only its private result as needed for `validationCoverage: Observation` and the production required selector. Preserve `{name,status,text,sources}` and receipt extraction fields; multiple rows per fact class remain allowed.

Use two phases after bounded parseData:

1. Validate root object/type and direct required array with current unique-string checks. Record rootRequired at `/required` immediately and independently; missing input points to `/required`, not leaf. A later unhandled composition must not overwrite that literal membership.
2. Check selected context before claiming selected schema facts. `allOf` is removed from generic root rejection **only by calling a narrow scope classifier**, never added to ignored keywords. For this fixed profile the accepted form is a nonempty array; each item is an ordinary object with exactly `if` and `then`; each clause is an ordinary object with exactly `properties`; each properties dictionary is nonempty and every immediate key differs from `production`. Values under other root property names are opaque data under that property scope. Use own-key traversal and existing parse caps; no recursion into unrelated schemas or predicate evaluation.

Classifier returns a literal footprint of `{if:[root property names],then:[root property names]}` in source order for the5 actual items. This footprint supports a separate constraint row `context="schema-validation-coverage"`, status partial, selector `/allOf`, explicit authored-context mode: direct selected declarations are extracted, root conditional predicates and complete validator behavior were not evaluated. It is not a pass/result of those predicates. When root has no allOf, the same coverage limitation remains explicit using root selector.

Any item/clause outside that grammar, `production` in either clause, root-wide keyword (e.g. required/additionalProperties/not/$ref within clause), scalar/boolean item, root anyOf/oneOf/if/not or otherwise unsupported root context produces selected-context failure. Record the first exact offending JSON Pointer deterministically, e.g. `/allOf/0/then/properties/production` or `/allOf/0/then/required`, with reason `unsupported_selected_schema_context` (malformed shapes retain malformed_schema where distinguishable). Do not infer absence of a default/description or an effective minimum from this failure. RootRequired remains known if already read; selected type/constraint/default/description are null+partial/unknown with that context reason. Independent Core/default/example/API facts survive.

Production/leaf combinators and ref siblings remain fail closed as today, with exact selected offending pointer rather than fabricated leaf-location diagnosis. Preserve local-only refs, escapes/hop/cycle checks, malformed/duplicate key and safe number controls. Failure of one supported direct scalar extraction should not fabricate missing data; no fallback to prior/default64. This correction need not become a generic JSON Schema validator or support additional conditional grammars.

### 2. Positive facts and exact selectors

For the actual schema above: schema-type known literal-extraction integer; direct schema-constraint known literal-extraction `{type:"integer",minimum:1,required:true}`; schema-default not_assigned literal-extraction null **with text limited to no own default keyword in the recognized direct leaf**; units known literal quoted description. Root membership known at `/required`; production membership source locator `/$defs/production/required` must be retained alongside the leaf reference for the combined direct constraint (or as an additional direct membership row, with combined row citing both through its sources array). Do not mislabel a leaf pointer as proof of rootRequired.

Add one explicit partial validation-coverage constraint row using existing Fact fields, as above; preserve all ten class names and separate typed/example default rows. Do not raise `coverage.status` to complete or produce application_release/run identity. `additionalProperties:false` and required declarations are reported only as source declarations; an instance is never loaded or validated.

### 3. Reason-aware text and authored mode

At adapter units branch :880–889, absence text is legal only when `reason===description_absent`, meaning recognized direct leaf lacks an own description keyword. Use “В распознанном direct leaf description не объявлено; физические единицы из имени не выводятся.” For any other reason: “Owning description не извлечено (<reason>); физические единицы из имени не выводятся.” Source_missing is unavailable, never absence.

At effects :932–940, successful description permits the partial authored scheduling sentence and “Owning description приведено отдельно”. Failure branch must say description is not extracted and full effects unknown; omit both the quotation promise and unproved scheduling assertion. Explicit authored-context mode on the successful contextual interpretation, dynamic-unknown on failure.

At formula_origin :950–958: if description exists, keep not_applicable text about scheduling count, source exact `.../description`, and pass explicit `authored-context`. It is authored interpretation anchored to an extracted owning description, not literal formula extraction. If description is unavailable, return unknown/dynamic-unknown with the reason; do not retain an unconditional not_applicable assertion or attach a failed description as proof. No new route parser is necessary; independent route :67 remains reviewer support rather than a hidden fallback.

## Review focus and anticipated fixture controls

| Fixture/control | Required assertion |
| --- | --- |
| Root allOf unrelated versus selected target | Paired same schema bytes except then.properties.algorithms→production. Unrelated form restores literal integer/min1/required/defaultabsent/description; selected form gives null+partial/unknown for affected selected contexts, exact failure pointer; root `/required` and Core/example survive. |
| Root-wide/opaque condition | Add then.required or item $ref/boolean; affected contexts unknown, no false absence and no silent allOf ignore. Root anyOf remains unsupported. |
| Unsupported selected leaf/production | Existing leaf anyOf plus production allOf; no known complete constraint/defaultabsent/description claim. Distinguish actual missing description from unsupported context with description still present. |
| Authored interpretation consistency | description success→formula not_applicable/authored-context, effects partial/authored-context with exact source. Failure→unknown/dynamic-unknown and no “description отсутствует/приведено отдельно”. |
| Preserved evidence/capabilities | Packaged mismatch remains explicit while canonical result independent; all ten classes, typed79/example31, null run/effective origin, deterministic facts AND receipt across fresh dirs; existing target sentinels stay inert; no eval/import/run/net capability introduced. |

### Task 1: Root adapter and focused regression fixture patch

**Files:** modify only `ops/docs/static-slice.ts` and `tests/docs_static_slice_test.ts` in selected Root; no harness/product/source-schema edits in this task.

**Interfaces:** consume current `generateStaticSlice({snapshotDir,sourceReceiptPath,outDir})`, existing inert `schema()/sources()/fixture()/extraction()/facts()` test helpers. Produce same public API and output Fact/Extraction shapes; private schema result may carry exact coverage/required observations. Test discovery and harness TMP/symlink fixture contract remain unchanged.

- [ ] Write the paired controls before implementation, using canonical test baseline e825f6... (the /tmp prototype tests ff6f... differ by formatting only in preparedSymlinkFixture; do not replace canonical tests wholesale).
- [ ] Source-read expected failure against frozen3dde28 adapter/A1 evidence; no extra RED execution is required or granted here. Root’s proposed milestone has one GREEN invocation total, not an additional RED.
- [ ] Implement narrow classifier, independent rootRequired, direct projection, explicit partial coverage, reason-aware text and conditional formula/effects mode together. No generic traversal or broad refactor.
- [ ] Source/compiler/format/diff checks and fresh independent source review occur before consuming the proposed product calls. Root binds exact final code/test/harness hashes and all finite limits; stop if outside two source rounds.
- [ ] Only after separate coordinator READY, execute at most the single regression GREEN, then two new actual-source attempts against the same nine-source snapshot; preserve originals/failed logs and new attempt identities. Check positive fact content/modes/locators, both outputs’ determinism, no private paths and retained all10. No automatic retries or reuse of old exhausted counters.
- [ ] Independent high semantic review must inspect primary schema/route before outputs; completion requires meaning, not only byte identity. Then Root can record source/engineering acceptance separately from shared DOC03/render/native/science gates.

## Self-review and limits

Coverage includes M1/M2/M3, exact actual allOf footprint, selected-context negative pair, defaults/origins, mismatch, malformed/ref guards, all10/determinism and no evaluation. No equations/model/criteria changes or public schema additions. No product call, test, Deno/compiler/harness/native execution, target parser, network or solver performed in this D. Available slots were fully occupied; no extra subagent was spawned. Separate high D review is the next requested gate, not proof from agent agreement.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual root allOf относится к другим root properties | schema SHA62df... :179–423, five exact scopes above | Нет predicate/full instance evaluation | сохранить |
| Direct selected facts можно восстановить узко | /required, root ref, production.required, leaf1437–1441 | Условные/неподдержанные selected contexts остаются unknown | изменить |
| Description failure означает отсутствие | A1 units text против literal schema description и receipt reason | Extraction failure не data absence | изменить |
| Formula mode можно согласовать без новой physics | Existing description/route67 and conditional authored mode | No physical formula/runtime origin inferred | изменить |
| Новые checks/полная DOC06 приёмка уже выполнены | D has only source evidence | Old caps exhausted; fresh Root milestone remains separate | данных недостаточно |

STOP after D/report identity/readledger; no product/checkpoint/source mutation.
