# DOC04/DOC06 test routing D2 — descriptor counts, base scope, exact child env

2026-10-20. Узкая source-only коррекция frozen D1 после независимого high R.
D1 `/tmp/qcl-docs-test-routing-design.md`, SHA256
`fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270`,
и R `/tmp/qcl-docs-test-routing-design-review.md`, SHA256
`9e16ff7519453db4661833455450da9d83c72b5f76c9eefd4fb27370da812930`,
остаются неизменными. Применять D1 с точными overrides ниже. Product edits,
проверки/imports/parser/build/network/CI не выполнялись. Новый framework,
публичная схема и native readiness claim не вводятся.

## 1. Проверка R и неизменяемые основания

R1 подтверждён: D1§3 запрещает дополнительные fields, но §4 требует expected
counts, которых в whitelist нет. R2 подтверждён: разрешённые «indispensable
native-loader fields» не имеют exact admitted representation; Python child
clearEnv и preflight version evidence также требуют явного определения.

Primary source binding — Root `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`:
`deno.json` содержит составной check через `&&`, а не один engine report;
`ops/ci.ts` сохраняет targeted scopes; `ops/process.ts` передаёт Deno.Command
`env` и `clearEnv` раздельно. Existing unbounded `run` не становится bounded
executor благодаря этому уточнению. Его использование для dedicated receipts
по-прежнему недостаточно. D2 не следует за изменяющимся Root/candidate checkout.

Две точные discovery exceptions, mandatory aggregate из четырёх steps,
workflow routing, no fallback/download, external supervision/admission и sole
final CI условия D1 сохраняются. Никаких изменений test bodies/assertions.

## 2. R1: complete exact descriptor

Заменить exact field list D1§3 следующей формой. Это описание schema, не runnable
JSON. `Ref` означает ровно `{path,sha256}`; существующие retained receipt refs
должны связывать точные байты, а не caller boolean/status. `Count` — обязательное
положительное safe integer без string coercion/default. Никакие дополнительные
keys на любом показанном уровне не допускаются; duplicate JSON members также
refuse. Existing finite path/hash/size and ≤32KiB descriptor bound сохраняются.

```text
{format:'qcl-negf.docs-test-inputs.v1', source_revision,
 source_files:[{path,sha256}],
 tools:{deno:{path,version,sha256,receipt_ref:Ref},
        node:{path,version,sha256,receipt_ref:Ref},
        python:{path,version,sha256,receipt_ref:Ref}},
 loader_env:{},
 units:{
   'doc04-python':{
     test_path:'tests/test_docs_assembly.py', test_sha256,
     expected_tests:Count, report_format:'python-unittest-summary-v1'},
   'doc04-node':{
     test_path:'tests/docs_math_test.mjs', test_sha256,
     expected_tests:Count, report_format:'node-test-tap-v1'},
   'doc06-deno':{
     test_path:'tests/docs_static_slice_test.ts', test_sha256,
     expected_tests:Count, report_format:'deno-test-tap-v1'}},
 katex:{root,version,module_sha256,css_sha256,source_receipt_ref:Ref},
 storage:{owned_tmp_root,attempt_dir,deno_cache_dir},
 admission_ref:Ref,
 limits:{per_step_wall_seconds,per_step_log_bytes,total_log_bytes,
         cpu,ram_bytes,node_tmp_bytes,python_tmp_bytes,doc06_tmp_bytes}}
```

`units` содержит **ровно** три named entries, не arbitrary array/engine selector.
Path literals и report_format literals фиксированы planner, descriptor не может
подменить исполняемый файл, engine, argv или parser. `test_sha256` каждой entry
обязан совпасть с единственной соответствующей source_files entry, с actual
selected source bytes и с reviewed final test contract. Final source graph,
helper/task/adapter closure и before/after equality остаются D1 obligations.

Expected count относится к конкретному test path+SHA и выбранному tool/report
contract. Prepared admitted setup замораживает это source-bound значение до
запуска; helper не выводит expected из observed output и не исполняет файл для
подсчёта. При смене test bytes, регистрации/параметризации или engine semantics
нужен новый reviewed binding; старый count не переносится автоматически.
Отсутствующий count binding блокирует dependent full check. Для Python считать
unittest test methods по его Ran N tests, не iterations внутри subTest; для
нынешних flat Node/Deno suites — зарегистрированные engine tests, включая
развёрнутые literal loops. Число assertions не подменяет count.

На immutable e22 Node SHA
`a3e47d219238e9e0b6be4b64ef42154a7057e4ac79776621f3bca84f58acc6a7`
содержит15 flat `test(...)`; Python SHA
`2207f3bce01e55774b2a4f3a5930fbb5cc880b84fe6e1b38afeafab3a2a548ca`
содержит20 test methods. Это source declarations, не измеренные engine results.
В e22 DOC06 test/adapter не опубликованы, поэтому полного descriptor сейчас нет.
Ранее записанный candidate SHA3714933… не является final source binding.
Текущий candidate при ограниченном чтении имел другой SHA2957b182…; он также
не подставляется за selected source. Final DOC06 expected count устанавливается
по отдельному reviewed final file; никакого guessed/default count для него нет.

Dedicated unit pass требует одновременно exact reviewed test/tool/inputs,
complete captures, guards/source stability, exit0 без signal, один поддержанный
полный summary/plan, observed_tests=expected_tests>0 и все tests passed;
failed/errors/skipped/ignored/cancelled/todo=0 по применимому engine format.
Bailout, only/filter mutation, противоречивые/дублирующие summary, unknown format,
пропавший count или zero count не дают pass. Неприменимые engine counters не
выдумываются как измеренный0: они tagged not_applicable; все применимые counters
обязательны. Report readers сохраняют original bytes; отсутствие данных —
unknown/failure, а не успех. Новые непроверенные engine layouts fail closed.

## 3. R1: base-only имеет отдельный статус

Base не входит в `units` и не имеет synthetic expected_tests. Состав existing
`check:base` остаётся: fmt → lint → typecheck → generic Deno suite с двумя exact
exceptions → transfer:check → restore:check. `&&`-chain и task bytes являются
проверяемой частью source binding. Новый helper не разбирает весь base stdout
как один TAP/unittest и не суммирует его с dedicated unit counts.

Внутренние step receipts различают:

- `kind:'base-task'`, `name:'base'`, `task:'check:base'`: exact bound deno.json
  task/argv/cwd, complete captures, exit0/no signal, guards и before/after source
  equality дают `result:'passed_base'`. При timeout/overrun/incomplete capture/
  source mutation/nonzero — failed; missing prerequisite — blocked. Unit summary
  имеет `status:'not_applicable', reason:'composite-task'`, numeric tests fields
  отсутствуют. Это сохранённая software task semantics, не scientific/native
  acceptance и не доказательство dedicated docs coverage.
- `kind:'dedicated-unit'` для каждого из трёх exact units: own report_format,
  expected/observed и применимые counters; только полный predicate §2 даёт
  `result:'passed_unit'`. Не reuse base result/exit как engine summary.

Aggregate `scope:'full-root-check'` требует base=passed_base плюс все три
units=passed_unit, все четыре steps ровно один раз и D1 shared predicates.
`docs:check` имеет scope docs-units-only; успешный docs-only результат не является
full aggregate. Самостоятельный `check:base`/runner-smoke маркируется base-only
в task/workflow/summary; dedicated units там not_requested, не pass. Отсутствие
unit counts у base — typed not_applicable, не not_measured→pass. Выдача base-only
output как full-root-check запрещена. Full `check` не имеет fallback в base-only.

## 4. R2: точные environments, без admitted arbitrary loader fields

Выбран строго пустой `loader_env:{}`. Любая непустая map, дополнительное поле env,
loader_env внутри tools или произвольное имя/значение из descriptor запрещены.
Ни measured external receipt, ни caller flag не расширяют эту map в рамках D2.
Если свежему actual tool требуется дополнительный loader environment, зависимый
route blocked и требуется отдельный явный reviewed correction; не наследовать
ambient field и не считать tool совместимым по одному retained version label.

Все dedicated executables — exact absolute admitted paths. Deno.Command env
строится из проверенных path inputs и фиксированных literals; helper не читает
Deno.env и не получает allow-env. Child environment задаётся **ровно** так:

| Child | clearEnv | Exact env map |
| --- | --- | --- |
| DOC04 Node | true | `{DOC04_KATEX_ROOT:katex.root, TMPDIR:OWN_NODE_TMP}` |
| DOC04 Python | true | `{TMPDIR:OWN_PYTHON_TMP, PYTHONNOUSERSITE:'1', PYTHONDONTWRITEBYTECODE:'1'}` |
| DOC06 Deno | true | `{DENO_DIR:storage.deno_cache_dir}` |
| Existing base task | false | no env overrides; existing trusted CI job environment/task behavior сохранено только для base |

OWN_NODE_TMP/OWN_PYTHON_TMP — созданные helper exact disjoint children внутри
admitted owned_tmp_root, не env/cwd fallback. DOC06 получает собственный TMP
только уже заданным explicit positional argument и script read/write capability;
DENO_DIR относится к admitted CLI runtime cache и не даёт script allow-env.
Ни HOME/PATH/TEMP/TMP, ни NODE_OPTIONS, PYTHONPATH/PYTHONHOME, ambient DENO_*,
LD_*/DYLD_* или preload fields не копируются dedicated children. Фиксированные
Python literals отключают user-site и bytecode writes; они не являются arbitrary
loader input. Python argv остаётся D1 `-m unittest discover -s tests -p
 test_docs_assembly.py`, Node/DOC06 argv/permissions также без изменений.

Python clearEnv не объявляется OS sandbox или доказательством полного import
closure: фактический interpreter/std-library/global-site identity и допустимые
import effects остаются external tool/admission obligation. Если в этом exact
clean environment запуск не совместим с admitted toolchain, сохраняется failure,
не происходит retry с inherited environment. Base сохраняет прежнее окружение
и capabilities; dedicated isolation claim к нему не приписывается. Base env
не расширяет descriptor env и не распространяется на следующие child steps.

Private step receipt записывает clearEnv, exact set имён, literal values либо
value binding на descriptor digest+field и owned child path; values не выводятся
в public summary. Exact empty loader map также фиксируется. Names-only receipt
не считается достаточной binding для разрешённых derived values. Никакие secret
values/ambient inventory не собираются; inherited base env обозначается явно,
не изображается как очищенное или перечисленное.

## 5. R2: preflight retained identity, а не hidden version execution

`docs:preflight` остаётся helper read/write/run=git, no env/net/ffi, и units не
запускает. Он может читать/хешировать доступные executable/receipt bytes и
проверять согласованность exact tool path/hash/version declaration с retained
identity receipt и внешним admitted handoff. Version label этого шага имеет
`evidence:'retained_receipt_bound'`, measurement здесь отсутствует. Версия не
получает статус freshly_measured только потому, что field совпал со строкой.

Внутри preflight запрещены Node/Python/Deno `--version`, units, loaders/imports
или дополнительные subprocesses кроме existing read-only git source graph.
Initial Deno, которым caller запускает task/helper, не является дочерним version
probe. Required externally measured version/binary identity должна уже иметь
допустимое retained свидетельство; при отсутствии, stale/mismatched receipt,
unknown schema или несовпадении actual executable bytes — blocked. Ref/status
alone не доказывают admission/ownership. Native process-tree enforcement,
actual runtime compatibility и resource evidence остаются отдельными gates D1.

Preflight outcome: ready_for_unit_attempt только при всех required source/input/
retained-evidence predicates; blocked/failed иначе. Это prerequisite readiness,
не test pass, не выполненные version probes и не полный native readiness.
Обычный unit mode выполняет только D1 reviewed argv — дополнительный hidden
version measurement не нужен. CLI/report incompatibility при будущем запуске
сохраняется failure и не инициирует fallback/rerun.

## 6. Узкие source-I controls, delta и stop

Дополнить existing fake-executor/manufactured-report controls D1 следующими:

| Control | Required result |
| --- | --- |
| Missing/extra unit, missing/zero/non-integer count, wrong test path/hash или report_format | descriptor refuse до dedicated spawn |
| Expected N против observed N±1, zero, skipped/TODO/ignored/errors, duplicate/unknown summary | dedicated unit не passed_unit; aggregate не pass |
| Base exit0 + fake TAP text при отсутствующих docs units | максимум passed_base/base-only; full blocked/failed |
| Base nonzero/timeout/capture/source mismatch при всех units green | full aggregate не pass |
| Непустой loader_env, extra tool env field, environment injection | refuse; no ambient loader propagation |
| Child plan capture | точные clearEnv/maps по §4; Python столь же очищен, как Node/DOC06; base явно inherited |
| Preflight fake executor | только allowed git route; ни одного version/unit subprocess; retained version label не measurement |
| Retained receipt mismatch/missing и actual binary hash mismatch | blocked before dedicated spawn, no automatic repair/download |

Ни один control здесь не выполнялся. Source I остаётся finite отдельно порученным
этапом; никакого final CI dispatch или scientific test не было. Original D/R и
ledger не меняются; D2 identity/delta содержат новые hashes и named source reads.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 descriptor и base semantics были неполны | D1§3/§4/§6, R1, primary deno.json && chain | Source-only | изменить |
| R2 child env и version claims теперь определены | Exact maps и retained-only preflight выше; process.ts clearEnv forwarding | Actual clean-env compatibility не измерена | изменить |
| Полный check сейчас готов к запуску | Final DOC06 selected binding/admission inputs отсутствуют | D2 не admission/runtime proof | данных недостаточно |
| Routing/framework/scientific boundaries D1 сохраняются | Узкие overrides §2–§5 | Native/full CI не запускались | сохранить |

STOP для независимого high D_R перед I.
