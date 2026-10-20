# DOC04 I-Root — independent high source review

**PARTIAL / NOT_READY.** Operator recipe соответствует принятому source contract в проверенных ниже частях. Полная source-I приёмка orchestration не закрыта. Два конкретных исправимых source замечания приведены ниже; отсутствующие integration APIs и внешние BUILD evidence перечислены отдельно. Общего PASS, runtime/test/build/native/scientific verdict нет.

## Frozen source

Проверен `/tmp/qcl-doc04-root-recipe-worktree`, HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`. Начальный и конечный `git status --short` содержат ровно три untracked файла: `docs/public/make.jl`, `ops/docs.ts`, `tests/docs_recipe_orchestration_test.ts`. Gitlinks сохранены; submodules в review worktree не инициализированы. Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`. Их files/default branches не входят в patch; новый независимый полный review owning profiles этим заключением не подменяется.

Проверенные SHA256:

| Артефакт | SHA256 |
| --- | --- |
| `docs/public/make.jl`, 4134 B | `b673bf4e2ba53179bccd7dcff631c8c1fe03893944cf2add868155e133705c8b` |
| `ops/docs.ts`, 12923 B | `1ab9df1f6b43df745500e176a7125f482105131e1581be5c9205282b99406db0` |
| `tests/docs_recipe_orchestration_test.ts`, 7799 B | `c3f10ffeeb3149c4439a8c2d786da4393a44d76d792e9104c40b31586b0d6ae5` |
| `/tmp/qcl-doc04-root-recipe-impl-complete.patch` | `6f2e25ab81a25223f957d92edee7fab6ea34400bd22eb46ec92bda16156a0b81` |
| `/tmp/qcl-doc04-root-recipe-impl-report.md` | `dbcb6dbb7463839d95bda76b70b989ba90c6787444cf025d4d7bfaa7c34c3f1f` |
| `/tmp/qcl-doc04-root-recipe-impl-identity.json` | `4320cfcaa0a7f5962c046b2ef81ea517e43ecf2a4d91d1afe54a13911135a006` |
| `docs/public/operator-recovery.md` | `8f05ff4cced8579b09cccd4b4315101e861e1896b87321b42e597374da79de49` |
| `ops/docs/assemble.py` | `58d47789da8af18a66136676228c7398fcd50c8797838e8614c8aa07f3d64fda` |

Сверены frozen D1 `008650e7…c2505`, D2 `ce582cc3…65610`, D3 `960a639d…59aee`, path contract `ec771749…5a935`, соответствующие high reviews. Полные hashes находятся в companion identity. Чтение ограничено исходниками и metadata; архивные execution payloads не использованы.

## Исправимые source findings

**R1 — P2: ограничение размера не ограничивает фактическое чтение.** `ops/docs.ts:223–228` (`boundedFile`) сначала проверяет `stat.size`, затем вызывает `Deno.readFile` и лишь после полного выделения/чтения проверяет `data.length`. В `inventoryTree:207–214` тот же шаблон. Если обычный файл вырастает после stat, заявленный cap не останавливает чтение и выделение памяти. Это касается уже blocked CLI preflight: `preflight:242–247` вызывает `boundedFile`, хотя внешняя exclusivity ещё не установлена. То, что после чтения результат будет отклонён, не устанавливает finite read/RAM contract. Допущенный exclusive namespace может исключить race для будущего BUILD, но текущий helper не принимает и не проверяет такой binding.

Минимальная правка: ограниченный reader, читающий максимум remaining-cap+1 byte и прекращающий чтение сразу при превышении, с закрытием handle на каждом выходе; `inventoryTree` использует общий оставшийся byte budget. Сохранить reject-on-change и symlink/special-file правила. Дешёвый различающий fixture source: инъецируемый reader с metadata маленького файла и фактическим более длинным потоком; проверить предел реально запрошенных/полученных байтов и отсутствие зависимого dispatch. Runtime этого fixture здесь не выполнялся.

**R2 — P2: retention control допускает потерю всех partial logs, а byte receipt смешивает reserve и успешную запись.** `tests/docs_recipe_orchestration_test.ts:69–79` записывает только длины и проверяет сумму `<=9`. Если убрать `save` полностью из `runFinite:163`, assertions по caps/reason/exit по-прежнему допускают результат с нулём сохранённых байтов. Все fixture bytes равны нулю, stream identity и точный сохранённый prefix также не проверяются. Поэтому это пока cap/deadline source control, а не meaningful retention control.

Дополнительно `ops/docs.ts:160–163,188` увеличивает `stdout_bytes`/`stderr_bytes` **до** успешного `await save`. При rejecting sink счётчики могут быть ненулевыми при отсутствии сохранённых данных. При hanging sink после drain deadline `runFinite:176–184` возвращает результат, хотя outstanding `save` не отменён/не завершён; callbacks могут продолжить запись или изменение общего массива `errors` после возврата. Это согласуется с авторским признанием missing production sink/cancellation binding, но такой helper ещё нельзя подключать к terminal immutable receipt как доказательство сохранённых логов.

Минимальная правка контракта: различить observed/reserved/retained bytes либо однозначно назвать их; retained увеличивать только после успешного save. Определить finite sink completion/cancellation и snapshot terminal result. В source fixture использовать разные ненулевые stdout/stderr последовательности, проверять точные префиксы/stream tags и ожидаемый полный доступный prefix (для текущего cap — 9 B), отдельно sink rejection, hanging sink и неизменность возвращённого snapshot. Не приписывать descendant termination, если внешнего доказательства нет.

Эти findings не требуют нового Julia/render/сервера. Они относятся к текущим Root helper/fixtures и закрываются отдельным bounded source ticket; исполнение fixture остаётся отдельным порученным этапом.

## Что подтверждено source inspection

`docs/public/make.jl:3–4` допускает только explicit pilot-v1. Base-only path checks `10–52`, VERSION `53`, ordinary nonsymlink Project/Manifest checks `54–66` и exact `Base.active_project()` `67` предшествуют первому `using Documenter:69`. Проверяются ancestors, normalized Linux spelling, два направления overlap, literal operator tuple и absent BUILD, включая dangling symlink. Recipe не очищает output. Containment использует компоненты splitpath, поэтому lexical prefix trap не становится ancestor relation. ROOT/ATTEMPT `/` отвергается явным trailing-slash guard. Это source/API observation; реальный Julia sentinel harness отсутствует и не исполнялся.

Typed `modules=Module[]:74`, exact `sitename="Документация оператора":76`, `checkdocs=:none:86`, две exact pages `82`, supported D1–D3 kwargs и отсутствие runtime math в recipe сохранены. CSS указан как обязательный reviewed input; наличие/полнота asset bytes этим не доказаны. Fixed-light browser/native gate не измерен.

`operatorSources:63–75` сверяет exact8f05 canonical chapter hash и извлекает один ограниченный recipe-owned LF literal без Julia evaluation. Это in-memory mapping; реального stage write/readback, до/после-render recovery hash, staging manifest и immutable candidate нет. Fixture `46–57` проверяет изменённый chapter и index literal, но также не выполняет filesystem mapping. Название test не следует трактовать как свидетельство выполненного staging.

`parseDocsArgs:78–95` допускает только заданные modes/options и canonical absolute values, отклоняет duplicates/unknown/missing fields. `buildBlockers:100–110` нельзя удалить caller marker. `preflight:237–258` всегда blocked, admission остаётся null, steps пусты. Caller-authored JSON не читается как разрешение. `mkdir` fresh attempt и createNew receipt исключают обычный повторный reuse; filesystem fixture `132–152` проверяет сохранность existing receipt. Наличие fixture source не является его execution pass.

`ops/docs.ts` импортирует лишь `workspace` из `ops/process.ts`; старый `sourceGraph` не вызывается. `ops/git.ts:33–39` вызывает `ops/process.ts:run`, а тот использует buffered `Deno.Command.output()` без конечного deadline/caps. Отказ от его вызова здесь правильный. `sources=null` — честный integration blocker; это не проверенный clean graph.

## Integration API gaps и внешние prerequisites

Нельзя свести незавершённость I-Root только к отсутствию внешнего BUILD grant.

| Категория | Конкретный незакрытый контракт | Локатор / следующее свидетельство |
| --- | --- | --- |
| Owning source API | Полный assembly entrypoint/transport/serialization и shared-schema validation binding | `assemble.py:145` уже имеет `load_pilot_plan`; `679–689` всегда blocked и bundle_bytes=None. Нужен принятый owning API, не Root fallback/schema copy |
| Root source integration | Bounded Git runner seam и sourceGraph before/after с теми же identity checks | `ops/git.ts:42–84` сейчас привязан к unbounded run; `docs.ts:239–241` оставляет null |
| Root source integration | Plan/effect/input validation, actual owner staging/readback, owner argv/env и dispatch, full input recheck, terminal receipt | `docs.ts:249–258` явно только hashes/blocked; helpers не связаны в orchestration |
| Root source controls | Actual recipe sentinel source harness, source-change orchestration control, production finite runner/sink failure controls | TS fake-import counter не исполняет Julia guards; before/after source-change control отсутствует |
| Внешний evidence | Complete nested/dynamic docstrings и transitive imports/cache, installed Documenter/toolchain identity, full assets/licenses/CSS bytes | Нужен отдельный bound source/effect/asset evidence; marker path не закрывает его |
| Внешний BUILD admission | Fresh inventory, ownership/exclusive namespace, process-tree/network/CPU/RAM/wall/log/output/scratch budget | Отдельные admission/measurements; path guard, child.kill и source review не являются доказательством |

Дешёвый следующий source contract — **I-Root finite I/O/retention seam**, закрывающий R1/R2 с meaningful pure fixture source, без target execution. Затем узкий owning `sourceGraph` runner seam: default callers сохраняют текущую совместимость, docs получает argv-based capped/deadline runner; fake Git отвечает на существующую последовательность команд, а before/after graph/input mismatch сохраняет original attempt и не создаёт candidate. Это можно сделать при неизменном blocked BUILD, без final assembler и без расширения научного scope. Изменение `ops/git.ts` требует явно добавить этот owning path к следующему ticket; текущий разрешённый patch его не меняет.

Параллельно нужен отдельный interface brief владельцу assembly/schema: точный complete entrypoint + finite JSON/bytes transport + validator binding + typed blocked/error/success result. Pure `load_pilot_plan` уже существует: отсутствие final serialization не отменяет возможность подготовить его будущую binding/validation seam. Нельзя выполнять parser сейчас или выдумывать новый API в Root. Полная staging integration и source-change wrapper также source work, а не недостающий внешний inventory.

## Ограничения и ledger

Только чтение named source, Git/path metadata, hashes и text searches. Запуск target code, Deno/Julia/Python/JS runtime, parser/compiler/formatter/linter/tests, render/build/native/network/science, server/CP, source/Git edits — **0**. Записаны только этот review и companion identity в `/tmp`. Не создавались subagents или новые attempts. Default Core/Runner сохранён по границе трёхфайлового patch и gitlinks; их owning implementation не переисполнялась.

Named content inventory с дополнительными designs/reviews/report находится значительно ниже 512 KiB за один полный проход; для repeated cat/search/extract/hash консервативно зарезервировано **4 MiB** из 6 MiB grant. Это accounting upper reserve, не измеренные disk I/O/RSS. Один ошибочно широкий `rg --files /tmp` перечислил metadata paths; содержимое найденных execution/архивных файлов не читалось. Он не используется как source evidence. Некоторые большие combined tool outputs были усечены; ключевые recipe/TS/path/adapter passages перечитаны отдельно. Точный transport-output meter отсутствует; размер созданных review artifacts измеряется отдельно. Формальный resource/enforcement PASS не заявляется.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Operator guards/Module[]/sitename соответствуют accepted D1–D3/path | make.jl:3–89, exact hash выше | Source only, sentinel/render не выполнялись | сохранить |
| Canonical recovery bytes bound к mapping | exact8f05 input; operatorSources:63–75 | Нет stage write/readback/after-render evidence | дополнительно измерить |
| Caller marker не допускает BUILD; старый buffered sourceGraph не вызван | preflight:237–258; imports/source null | Это blocked skeleton, не finished orchestration | сохранить |
| Finite reads и partial-log retention достаточно проверены | R1/R2 locators и различающие source fixtures выше | Runtime controls отсутствуют | изменить |
| Полная source-I orchestration завершена | Missing API bindings/staging/recheck/runner/sentinels | Внешние BUILD receipts не заменят source gaps | изменить |
| BUILD/native/public/scientific acceptance выполнены | Execution evidence отсутствует | Все соответствующие этапы не запускались | данных недостаточно |

STOP. Принять как честный partial handoff; не маркировать CP-SOURCE READY или общий PASS.
