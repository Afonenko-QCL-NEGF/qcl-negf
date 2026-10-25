# DOC04/DOC06 routing: независимый high RED fixture source review

Вердикт: **REQUEST_CHANGES**, два collated замечания R1–R2. Это проверка исходников fixture до первого RED; она не является результатом выполнения тестов. Нужен один узкий correction cycle. Production/helper/tasks/workflows рецензент не менял.

## Зафиксированный набор

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-docs-test-routing-design.md` | `fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270` |
| `/tmp/qcl-docs-test-routing-design-v2.md` | `bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70` |
| `/tmp/qcl-docs-test-routing-design-v2-review.md` | `939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967` |
| `/tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts` (33358 B) | `f3db415342457e3f05434f5ed5e3c49f83796f6d91eddffdd76846363b64f0c5` |
| `/tmp/qcl-docs-test-routing-red-report.md` | `e0621ad8010399bb7013a35353496ecc6581193c8d0f90ea358ab00985070215` |
| `/tmp/qcl-docs-test-routing-red-identity.json` | `889f52e7dd5b46f96b0b6c9483da587c917ce459dd18e8ad887559fe36942d20` |

Прочитаны D1/D2 и accepted R, затем весь fixture; author packet прочитан после первичных материалов. Worktree HEAD наблюдён как `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`. `git status --short`: только `?? tests/docs_test_routing_test.ts`. Recursive submodule status содержит восемь неинициализированных selected gitlinks, без обновления компонентов. Это не readiness их runtime.

## R1 — P2: отрицательные path fixtures допускают постороннюю причину отказа

Локаторы: fixture:112–157 (`metadata`), 318–332 (особенно326), 378–389; D1:109–117; D2§2.

Все18 storage rows меняют только `d.storage[location]`, передавая прежний `metadata()`. В admission.exclusive_storage остаются исходные TMP/ATTEMPT/CACHE. Directory facts, fresh absent_paths и child paths также относятся к исходным именам. Поэтому row с `/tmp/a,b`, control character, traversal или workspace path может пройти даже у реализации, которая вообще не проверяет соответствующее правило безопасности: достаточно отказать из-за отсутствующей admission для нового пути. Это статический контрпример достаточности oracle, а не утверждение о ещё не написанном helper.

Отдельно `absolute source path` заменяет весь массив source_files одной entry (326), одновременно теряя11 обязательных исходников. Отказ за неполный source closure удовлетворяет assertion и не различает проверку absolute path.

Минимальная коррекция:

- Для parse-level lexical запретов проверять именно `parseInputs` на полной, в остальном здоровой форме; менять одну существующую source entry, сохраняя остальные entries и размер массива. Не считать отказ о missing closure доказательством lexical path predicate.
- Для правил, требующих metadata, явно согласовать с изменённым путём все независимые fake facts: admission storage, directory/canonical facts, fresh attempt/children и прочие зависимые ссылки. Оставить только проверяемое нарушение. Где unsafe path нарушает несколько нормативных правил одновременно, указать это, а не заявлять изоляцию каждого правила.
- Добавить хотя бы healthy relocation пары для TMP/attempt/cache с полностью согласованными manufactured facts: безопасное переименование обязано дать ready. Отрицательная пара затем отличается проверяемым unsafe свойством. Не превращать admission fake в разрешение unsafe path.

Старые18 rows можно сохранить как общей формы rejection controls, но до такой коррекции они не являются независимыми controls отдельных path predicates. Не требуется никакой реальный FS/probe.

## R2 — P2: нет контроля source mutation между preflight и первым execute

Локаторы: fixture:160–163, 212–223, 610–620; D1:96, 218–220; D2:65–68, 112–114.

Существующий source-change control вызывает `executor.setGraph(OTHER)` только внутри уже вызванного execute. Он различает отсутствие after-check, но не отсутствие before-check. Реализация, которая всегда запускает children и сравнивает graph только после них, удовлетворяет этому control и всем healthy cases. Между готовым preflight outcome и runChecks исходники могут измениться; проверяемый контракт требует before/after equality и source binding до dependent execution.

Минимальная коррекция: отдельный async control берёт ready и exact plan, затем устанавливает executor graph=OTHER **до** runChecks. Нужны aggregate non-pass и `executor.calls=[]`; retained outcome не должен объявлять child выполненным/успешным. Положительная пара уже есть в healthy aggregate. Тот же fake seam позволяет без runtime проверить changed revision/dirty graph, если реализация различает их; обязательный узкий минимум — pre-start digest mismatch. Existing after-child mutation control сохранить.

## Что исходники действительно различают

Fixtures не получают expected output из helper. Exact argv/env/base command перечислены literals (41–58,237–274), report streams сконструированы независимо (168–180). `metadata()` берёт отдельный healthy descriptor, поэтому изменения входного descriptor не изменяют наблюдённые facts автоматически. Shared fixture factories остаются общим допущением, а не вторым независимым reader.

Healthy tests требуют four steps ровно один раз, scoped aggregate, base `passed_base` с typed N/A вместо synthetic count, три `passed_unit` с20/15/7 и retained-only version labels (276–294). Docs-only и smoke не выдают full scope. Unit reader controls проверяют expected mismatch, zero, unknown/duplicate/truncated summary, applicable failure/skip/TODO/cancel/error counters (438–527). Exact DOC06 least permissions/one owned argument, clean environments и selected executables имеют literal expectations и changed-plan negatives (255–274,530–575,699–712). Это полезные независимые tests, не просто comparison двух вызовов planner.

Все четыре step names проходят manufactured failure matrix: nonzero, deadline, log overrun, capture/drain incomplete и отсутствующее enforcement evidence (577–608). Сохраняемые stdout/stderr/exit проверяются по оригинальным changed capture, no retry и no cleanup — отдельно. Существуют launch-rejection, total-log и convincing-base-TAP negative controls. Здесь проверяется returned receipt state; физическое сохранение файлов, hard quotas, kill/drain implementation и процессное дерево этим fake executor не доказываются.

На source level подтверждены **207** регистраций: сумма независимых групп `6+8+27+1+3+18+8+20+1+21+20+14+4+1+24+3+1+3+8+3+8+1+3+1`. Циклы конечны; async callbacks возвращают/await promises, включая aggregate/report controls. Прямых skip/only/filter регистраций нет; строка filter используется как запрещённая мутация argv. Это не measured engine count. Исправления могут изменить итог: новый count нужно явно перебиндить, не сохранять207 любой ценой.

Значения20/15/7 намеренно manufactured. В частности7 не является final published DOC06 count. Отдельный reviewed_units mismatch control (732–738) препятствует простому увеличению expected без нового binding. Реальные final source/tool/counts по-прежнему отсутствуют в этом packet.

## Чистота fixture и границы проверки

Fixture импортирует только будущий trusted helper и пользуется Deno.test, обычными JS данными и fake executor; прямых FS/env/process/network/FFI calls нет. Никаких target units/config imports или настоящих tool probes fixture не содержит. Это совместимо с будущим focused harness без script FS/env/run/net/ffi permissions при условии, что helper безопасен при import. Такой harness и target helper в этом review не исполнялись.

Название `preflight and parsing are pure` сильнее отдельного assertion на calls (296–305): созданный executor не передаётся preflight, поэтому его пустой calls не является трассировкой preflight. Успешный healthy preflight под deny-run/env harness будет полезным запретительным контролем, но разрешённый readonly Git CLI adapter и фактическое отсутствие прочих probes всё равно требуют source review. Новый side-effect API ради этого не нужен.

Returned fake retained paths/cleanup flags не доказывают существование TMP или receipt на диске. Capture negative assertions не проверяют byte-for-byte сохранение всех иных metadata полей; они проверяют original streams/exit и terminal aggregate. Эти пределы сохраняются, без ложного native/resource pass.

## Обязательный отдельный source integration gate после production I

`genericCheckPlan`, `parseCiArgs`, `workflowRoute` сами по себе допускают несвязанный helper: возвращать правильные literals можно и при неправильных actual task/workflow bytes. Author report это ограничение признаёт; чистому fixture не добавляется FS privilege. Для будущего production source review требуется конкретно:

1. Сопоставить actual `deno.json` check:base bytes с exact base chain и двумя исключениями, а actual check/docs:check/docs:preflight/test tasks — с единственными helper/CI entrypoints. Проверить отсутствие второго независимого check перед aggregate и recursion CI→check→CI.
2. В actual `ops/ci.ts` пройти от `Deno.args` до call-site общего parser/planner и child spawn: input-only выбирает all; targeted selectors не проглатывают docs input; full передаёт descriptor в ровно один aggregate и сохраняет Python/Julia/infra branches. Не принять один только экспорт неиспользуемого parseCiArgs.
3. В обеих actual `.github/workflows/{ci,release}.yml` сопоставить triggers, required/optional inputs, job mode, step-level env/quoted argv, cancel-in-progress:false и порядок source-graph→docs-preflight→prepare→full-aggregate. Smoke обязан вызывать check:base и не требовать dedicated inputs. Release обязан заменить прежнюю пару check+test одним test aggregate. Не принять неиспользуемый workflowRoute за проверку YAML.
4. В actual helper пройти от import.meta.main/CLI dispatch до этих же production функций, trusted external receipt/admission readers и bounded executor. Проверить отсутствие второй более разрешительной CLI ветки, ambient fallbacks/hidden version probes. Fake normalized-tool-identity не становится accepted persisted receipt schema.
5. Bind final published test/helper/task/workflow source closure, three reviewed unit counts и selected executable/report contract до любого real full route. Root separately authorizes finite RED/GREEN; этот review не выделяет calls и не разрешает full CI.

Это source verification actual integration, отдельная от pure-function GREEN. Нужный факт после будущей реализации — наблюдаемые actual call-sites и configuration bytes, не согласие fake metadata. Native tool compatibility, process supervision/admission и final CI остаются отдельными gates.

## Учёт и решение

Named source reads, включая повторные extracts/hash reads, консервативно444668 B; округлённый bound524288 B <4MiB. Полные underlying files начислялись для каждого grep/sed/nl/hash read, а не только выведенный диапазон. Git metadata читается отдельно; physical I/O/CPU/RSS не измерены. Действий target runtime/import/parser/typecheck/test/format/build/network/commit/checkpoint/product edits:0. Только два requested review artifacts в /tmp.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Path negatives независимо проверяют safety rules | R1, descriptor-only mutations при старой admission; source array заменён одной entry | Сейчас допускают unrelated rejection | изменить |
| До первого child source identity проверяется control | R2; mutation test только внутри execute | Нет pre-start mismatch negative | изменить |
| Exact routing/env/typed counts/failure summaries имеют полезные controls | Literal expectations и fake report/failure matrices выше | Source-only, helper отсутствует | сохранить |
| Pure GREEN доказывает actual tasks/workflows | Только exported decision functions; integration checklist выше | Нужен separate production call-site/config review | данных недостаточно |
| Тесты, native limits или full CI выполнены успешно | Execution0 | Ничего из этого не измерялось | данных недостаточно |

STOP. Root получает collated correction scope R1–R2; независимый reviewer не расходует RED/GREEN и не меняет checkpoint.
