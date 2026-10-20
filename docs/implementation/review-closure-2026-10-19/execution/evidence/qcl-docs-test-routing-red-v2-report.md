# Routing RED fixture v2 — один collated correction pass

Исправлены только R1–R2 из frozen high review `/tmp/qcl-docs-test-routing-red-review.md`, SHA705bea4364bbaf6053fd51cb7ea7acb48a2776d19e8f6002f9dddbd7e6302eb7. Source-only; та же isolated Root branch/basee22, один permitted product path `tests/docs_test_routing_test.ts`. D1+D2, exported API и production/config файлы не менялись. Runtime/import/parser/typecheck/format/test/build/network/commit/CP=0.

## R1: что именно устранено

Absolute source path row теперь изменяет только path первой entry; assertions проверяют сохранение размера12 и byte-equivalent остальных11 entries. Прежняя подмена массива одной entry устранена. Refusal по-прежнему проверяется напрямую в parseInputs, без filesystem/admission adapter.

Все прежние18 storage rows сохранены, но теперь используют `relocatedStorage`: перепривязаны descriptor storage, admission.exclusive_storage, directory keys/canonical facts, absence facts attempt/children и три стороны synthetic admission digest (descriptor ref, observed file hash, normalized admission ref). Source revision/graph и source_files не менялись, поэтому их прежний source digest остаётся согласованным. Descriptor/input digest вычисляется будущим parse/preflight из новых bytes; stale готовый ready не переиспользуется. OTHER является fabricated retained-byte hash в fake metadata, не вычисленным hash настоящего admission и не technical BIND.

Добавлены12 отдельных parser-only lexical controls:3 storage locations × relative/comma/control-character/traversal. Они подают полный иначе healthy descriptor прямо parseInputs; metadata adapters не вызываются и не могут маскировать отсутствие lexical rejection своим отказом.

Добавлены3 healthy relocation controls: TMP→/tmp/routing-relocated-fixture, attempt→/fixture/retained/attempt-relocated, cache→/fixture/cache/deno-relocated. Каждый требует ready при согласованных metadata/admission/digest; проверяет независимые storage refs, canonical/absent facts и TMP child names. Отдельные3 workspace relocation negatives используют тот же rebound fact mechanism; admission включает новый путь, а отказ обязан сохраняться. TMP под workspace нарушает одновременно /tmp-descendant и workspace-disjoint predicates; fixture/comment не объявляет это изоляцией одного правила. Для attempt/cache изолирована workspace-disjointness при существующих parent facts и соответствующих existing/absent leaf facts.

Добавлен отдельный owned_tmp_root=/tmp negative с согласованной canonical directory/admission и свежими /tmp/node,/tmp/python,/tmp/doc06 child facts. Он отличается от healthy TMP пары запретом использовать /tmp целиком.

Старые18 broad controls не объявлены независимыми доказательствами каждого отдельного safety predicate: traversal/relative spelling не могут представлять правдивый canonical absolute filesystem fact, а attempt/cache=/tmp могут одновременно нарушать overlap/existence правила. Их назначение — общей формы refusal. Независимую lexical проверку дают12 parser-only cases; metadata-dependent свойства подтверждаются healthy/unsafe paired controls выше. Никакой fake admission не разрешает unsafe path.

## R2: до первого execute отдельно от after-check

Новый async test создаёт ready и exact plan, затем меняет executor source digest на OTHER **до** runChecks. Требует executor.calls=[], aggregate non-pass, source_stable=false, retained attempt/TMP/no-cleanup и отсутствие passed_base/passed_unit/исполненного capture у всех возвращённых step receipts. Нулевое число calls отличает before-check от реализации, проверяющей graph лишь после child. Старый after-child mutation control сохранён побайтно и по-прежнему проверяет другой момент изменения. Healthy aggregate остаётся положительной парой.

## Count, frozen artifacts и предел

Source declaration count:207 прежних registrations +12 lexical +3 healthy relocation +3 workspace negatives +1 /tmp root +1 pre-start = **227**. Это арифметика исходников, не measured engine result. Synthetic unit counts20/15/7 и их ограничения не менялись;7 не является final published DOC06 count.

Immutable v1 source сохранён отдельно `/tmp/qcl-docs-test-routing-red-v1-test.ts`, SHA f3db415342457e3f05434f5ed5e3c49f83796f6d91eddffdd76846363b64f0c5. V1 report/identity/base patch неизменны. Новый `/tmp/qcl-docs-test-routing-red-v2-delta.patch` применим поверх v1 fixture; полный новый base patch здесь намеренно не дублирован. V2 source/delta hashes и bytes — `/tmp/qcl-docs-test-routing-red-v2-identity.json`. Original historical paths в v1 identity описывают прежнее состояние; snapshot выше сохраняет те exact source bytes.

Git status содержит только requested untracked fixture. `git diff --no-index --check /dev/null ...` не выдал whitespace diagnostics, new-file diff exit1 ожидаем. Это не formatter/parser/runtime проверка. После коррекции RED не запускался. Файлы metadata/admission, actual storage и executable tools не создавались и не исследовались. Read bound консервативно≤786432B<2MiB (full-file charges для extracts/repeated reads с reserve); finite≤15min/1CPU/2GiB/output128KiB; physical I/O/RSS not_measured.

## Отдельный actual integration gate после будущего production I

Pure-function GREEN не докажет actual tasks/workflows. До integration claim независимый source review должен отдельно:

1. Сопоставить actual deno.json check:base chain/ровно2exceptions, check/docs:check/docs:preflight/test entrypoints; исключить duplicate check и CI→check→CI recursion.
2. Проследить actual ops/ci.ts Deno.args→shared parser/planner→spawn: input-only all; targeted selectors не поглощают docs inputs; полный aggregate ровно1 и прежние owning branches сохранены.
3. Проверить actual ci.yml/release.yml triggers, optional/required inputs, modes, step-local env и quoted argv, cancel-in-progress:false и порядок source-graph→preflight→prepare→aggregate; smoke base-only; прежняя release check+test пара заменена единственным aggregate.
4. Проследить actual helper import.meta.main/CLI→те же tested functions→trusted external receipt/admission readers→bounded executor; отсутствие parallel permissive path, hidden probes и ambient fallbacks. normalized-tool-identity в fake не является accepted persisted schema.
5. Bind actual final published source closure, reviewed3 unit counts и selected executable/report contracts до real full route. Actual hard supervision/storage/admission/tool compatibility и sole CI — отдельные gates.

Здесь это только plan/source-review gate: перечисленные production/config paths не менялись, их verification ещё не выполнена. Этот пункт не добавляет FS/env/run privileges fixture и не расходует RED/GREEN/full CI.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Masked path oracle исправлен | Full source entry array,12 parse-only cases, rebound facts и healthy pairs | Только source I; broad multi-rule cases явно ограничены | изменить |
| Before-first-execute source check различается | Новый pre-start control с calls=[]; after-child control byte-exact | Runtime не выполнялся | дополнительно измерить |
| D1+D2/API и existing controls сохранены | Delta только2corrected regions+helper+20 registrations | Same high R ещё впереди | сохранить |
| Actual integration/native/tests готовы | Production0, execution0 | Отдельные integration/runtime/admission gates не закрыты | данных недостаточно |

STOP: тот же high fixture R; затем только Root separately bounded RED.
