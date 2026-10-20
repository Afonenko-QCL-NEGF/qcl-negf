# I2H / B3a: normal slots, failed debits, domain/path и source facts

**Partial source candidate; STOP для fresh high CPP. Не whole B3 PASS и не
native READY.** Worktree `/tmp/qcl-docs-test-routing-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.

## Frozen input и scope

I2G high review SHA256
`497f6d9840040d1d5e4eef4b9c0bcf1579b33af4440a0848f32f83c45506b0cd`,
review identity `19050d562f528ae3557467a18f08b0b9b9d3eb97850238a2656a42092f95237b`
сверены. Exact четыре I2G файла сохранены до правок в
`/tmp/qcl-docs-routing-i2g-frozen-before-i2h`, manifest.sha256:4 OK.
D4/D5/D6 и source closures I2G сохранены. Прочитаны узкие owning sourceGraph
участки ops/git.ts; pure pair не менялся. Root подтвердил существующий C/G
caller contract и trusted component order; новая архитектура не вводилась.

Изменены только ops/docs_tests_native.py и tests/test_docs_test_native.py;
оба TS файла unchanged. Config/workflows, Git index, CP, gitlinks, сервер,
provider и scientific code не менялись. Восемь gitlinks остались uninitialized.

## Реализованный normal contract

C — fixed NATIVE_PATHS16×[ls-tree,cat-file],32 reads. G — owning sourceGraph,
36 reads. `source_read_events` строит native-owned ordered events, а
`SourceReadSchedule` требует exact owner/root/argv/ordinal и control markers.
Неправильный owner/root/argv, skip, reorder, extra read или marker poisoning
не возвращает slot и не разрешает продолжение. Перед command dispatch slot
необратимо потребляется. Per-batch snapshot принадлежит native scheduler.

Normal sequences:

- preflight: C → Ginitial → finish → C,100 reads;
- check: C → Ginitial → prepare → Gstart →
  [execute_i → C → unit_i → Gafter_i]×4 → Gterminal → finish → C,
  444 reads;
- docs: тот же contract с3 units,376 actual normal reads; прежний444 upper
  reservation остаётся консервативным, padding reads не добавлены.

Components используют exact trusted request.expected_source.components order.
Python locale/sort не имитирует JS localeCompare. Если registration не имеет
actual owning graph order, healthy execution не доказан и BIND должен отказать.
Существующие16 failure reserve,512 calls/8MiB/60s per phase, snapshot128calls/
2MiB/20s и global metadata2MiB не увеличены. Новых retry/reset/refund нет.

`source_read_binding` связывает registered source, actual native16 bytes/size/
SHA и существующие Git metadata observations: config/attributes, gitdir/common
pointer и .gitmodules. Existing noexec metadata reader теперь отдаёт fingerprint
прочитанных bytes и проверяет stat stability внутри чтения. Baseline получается
до первого C; проверка вызывается перед driver construction и before/after
каждого зарезервированного Git read, включая failed reads. Nodes count не
используется как source identity: создание обычного output не меняет fingerprint.

Это selected payload/config binding по выборкам. Он **не доказывает** atomic
immutable lease для всех tracked working files или отсутствие transient change
между выборками. Такой BIND/inventory proof остаётся B3b; широкий inventory,
новый provider/service не добавлены.

## Failed debits и независимые source facts

`git_read.finally` учитывает actual command ledger streams даже при exception,
elapsed time включая before/after binding, consumed call и snapshot slot.
Known partial bytes сохраняются в git_raw/snapshot.bytes. Если actual stream
неизвестен, raw_complete=false, а отдельный charged counter консервативно
удерживает полный slot cap; неизвестные bytes не объявляются измеренным нулём.
Debit/guard failure отравляет schedule; исходный command exception сохраняется
при secondary postcheck failure. Уже израсходованные counters не возвращаются.

DriverPipe stdout path теперь строится из storage.roots[stdout_domain], где
domain выбирается protocol при его наличии, иначе raw. Charge и actual physical
path совпадают; caps24MiB stdout/262144stderr не увеличены.

Native `validate_graph_read` независимо проверяет actual G stdout/stderr:
expected HEAD, clean status, section set, component URL, flat gitlink set и
component revisions. Completed validated G batch устанавливает измеренный
source fact до unit/report acceptance. Final native source validation отдельно
предшествует unit validation. Поэтому failed unit/report не стирает уже
измеренные source observations; это исторический факт измерения, не утверждение
неизменности source после последующей ошибки. Overall failed/partial result не
становится positive из-за measured label. Ref-exists shortcut не используется.

## Source controls и проверка

Расширены существующие8 Python methods, nominal Deno8 сохранены. Fixtures:
literal100/444/376 counts и check marker positions; trusted component order;
wrong owner/root/argv, premature marker, extra read и poisoned retry; actual
git_read finally с healthy/failed/unknown-partial/before/after guard cases и
сохранением original exception; actual driver initialization path/domain;
native graph positive/negative pairs; native/config binding changes;
actual git_read G36 batch measured только после36-го validated read;
failed unit-report при успешно измеренном source в existing phase seam.

Scheduler/debit fixtures добавлены до основной production correction;
последующие guards и controls расширялись source-only. RED/GREEN не наблюдались.
Некоторые focused seams изолируют другой upstream boundary (например binding
reader в debit test); это не full manufactured C8 route. Existing retention/
publisher controls не переписывались и не объявляются повторно исполненными.

Выполнены text/hash/Git reads, frozen manifest4 OK и diff --check двух changed
files без whitespace diagnostics. Scripts/parser/compiler/import/tests/runtime/
native/network/server/CI/science0. Product89/source8 unchanged; MathGREEN90
reserved и не использован. Новых дочерних агентов нет.

## Точные remaining boundaries

1. **B3a failure-abort transition.** Нормальная последовательность определена;
   допустимая terminal sequence после первого failed Git/unit prefix здесь
   не определена. Current scheduler fail-closed: не перепрыгивает unused normal
   slots, не pads reads и не запускает remainder/retry. Минимальный follow-up
   contract должен указать, какие existing Gterminal/Cfinish допустимы после
   exact failure ordinal, какие unused slots permanently skipped без refund,
   и какие children относятся к16 failure reserve. Пока этого нет, cannot claim
   complete accepted failed-run terminal route; raw/failure/phase evidence
   сохраняются существующими cleanup/fallback paths. Никакой новый broker или
   provider API для этого не нужен.
2. **B3b complete global physical upper trace.** Включить pending hard-link
   aliases и failed publications, actual driver stdout originals в protocol/raw,
   stderr, producer/participant raw, command/settlement/index/fallback receipts,
   samples, directory metadata и все domain/global reservations; metadata ceiling
   остаётся2MiB. Existing reservation estimate оставлен как necessary legacy
   estimate и так назван в source; это не full admission proof. Новые repeated
   source/config hash/census reads требуют CPU/I/O/wall учета в этом же finite
   trace. Не заявляется, что healthy allocation сейчас всё вмещает.
3. **Immutable full-source BIND.** Selected native/config fingerprints и
   observed G facts не заменяют actual immutable inventory/lease или доказательство
   отсутствия arbitrary working-file/exec race. Missing inventory/BIND остаётся
   blocker зависимых claims; fake JSON/booleans или новый trust root не добавлены.
4. **B4/full C8 и native parser conformance.** Root отдельно сообщил следующий
   concrete ticket: Python validate_unit_report ещё должен независимо принять
   exact reviewed Deno selected PATHS2 header и запретить result SKIP/TODO
   directives согласно уже исправленному pure contract, с literal +/- pairs.
   Этот parser в I2H не менялся. Потом отдельные finite DEV/compiler/native
   admissions; nominal counts не доказывают execution/coverage.

## Ledger и exact delta

Поручение20min/1CPU/2GiB/read≤4MiB/output≤128KiB; conservative source/hash/diff
read estimate3MiB. Начальное identity чтение и два небольших bounded selections
имели truncation; exact aggregate transcript byte counter не снимался, поэтому
строгое соблюдение output cap не сертифицируется. CPU/RSS/physical I/O отдельно
не измерялись. Никакого target execution ради измерения не добавлено.

Complete I2G→I2H delta35774bytes, SHA256
`35bd0a7cd6859c6e7124a0e88fea3f674fca4439405ec61975c8ef5dce81ed3b`.
Companion identity содержит exact four-file manifest. STOP fresh high CPP.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Normal source reads имеют exact native slots | source_read_events/Schedule, protocol markers, literal counts/positions | Source-only; registration order требует actual BIND | дополнительно измерить |
| Failed calls сохраняют partial/time/slot debit | git_read.finally и positive/negative controls | No execution; physical full trace ещё B3b | дополнительно измерить |
| Driver stdout charge совпадает с path | storage.roots[stdout_domain], initialization fixture | Нет runtime allocation observation | сохранить |
| Failed unit не стирает измеренный source | native G reader/batch fact, separate final source criterion, phase fixture | Измеренный факт не равен terminal source stability | сохранить |
| Полный B3/failure terminal/native READY закрыт | Явные remaining1–4 | Не получен full trace/immutable BIND/C8 | данных недостаточно |
