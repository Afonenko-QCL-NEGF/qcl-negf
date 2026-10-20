# Pure routing v3: независимый high source review

2026-10-20. Verdict: **STOP_SOURCE_CHANGES_REQUIRED**. Static denominator230 и pure two-file closure подтверждены; historical RED/current GREEN pins разделены корректно. Найден один блокирующий terminal-path defect:120s alarm отключается при потенциально живом non-daemon RawCapture thread. До source correction/re-review GREEN READY не выдавать. Prospective fmt/lint/check тоже ещё не имеют реализованного source supervisor и не являются готовыми calls.

Никакой подготовленный guard/helper/product/runtime/parser/compiler/test/formatter/linter/native/network не исполнялся и не импортировался. Только reads, hashes, read-only Git metadata и bounded inert text/log comparisons. Записаны только этот report и identity; Root/CP/product/old receipts не менялись. Это source verdict, не execution grant.

## Exact identities и разделение checkout

| Input | Bytes | SHA256 |
| --- | --- | --- |
| /tmp/qcl-docs-routing-pure-guard-v3.py | 26935 | 750fc342884b2f47372912c538d7cfd47d60c8aa6f2ac9ee37aee02373976c0a |
| /tmp/qcl-docs-routing-pure-plan-v3.json | 8181 | 9863ffb52c44f9d3ab95ff1165233132ebbca965338883a7c2724e8b9cbde742 |
| /tmp/qcl-docs-routing-pure-report-v3.md | 7665 | f45d28da3cc4aae41e5094301f354b1fff967954305ed36e1170e97b4e05eb0d |
| /tmp/qcl-docs-routing-pure-identity-v3.json | 2497 | 3ee980db931a3ce1ba6777921e8e639531117aae8e95a7cfd8a162bcfe4e9a00 |
| isolated ops/docs_tests.ts | 25884 | 676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c |
| isolated tests/docs_test_routing_test.ts | 40125 | f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761 |

Hashes/sizes независимо проверены. Product isolated Root `/tmp/qcl-docs-test-routing-worktree` HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; status содержит dirty I2B overlay и8uninitialized gitlinks, сохранён. Coordinator `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` при readback уже HEAD `107bac5697b37cf0e47c3feb44883a907837645c`, а не preparation c5ef. Это допустимо по late Root policy; нельзя записать isolated2bb как global current HEAD.

Guard проверяет spelling40hex Root HEAD и SHA Root handoff ref, но сам Git не вызывает и содержимое handoff record не интерпретирует. Поэтому обязательное действие Root — независимо проверить фактические HEAD/status/gitlinks/CP/call87→88 и source handoff после публикации, привязав это к свежему READY. Данный snapshot review не является будущим admission.

## R1 — блокирующее отключение deadline при живом collector

Локатор: guard `/tmp/qcl-docs-routing-pure-guard-v3.py:428–430,485–486,509–514`; pinned helper `/tmp/qcl-local-julia-guard-v2.py:49–72`, SHA `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`.

RawCapture использует `threading.Thread(...,daemon=False)`. Его finish(timeout) делает join(timeout) и возвращает complete/error boolean; false не доказывает, что thread завершён. Если reader остаётся жив после finish(2), guard честно устанавливает incomplete_capture и сохраняет failed receipt, но затем **безусловно** отменяет ITIMER_REAL на510 и возвращает1. На shutdown Python ожидает non-daemon thread, так что зависший reader/writer может удерживать guard без120s terminal alarm. Наличие failed receipt не исполняет обещанный finite terminal stop.

Source correction: сохранять deadline до подтверждённого завершения collector либо завершать процесс ограниченным terminal path после сохранения failed receipt/cleanup при живом thread. Нельзя назвать incomplete capture complete или daemonize reader ради скрытой потери original evidence. Требуется source re-review exact revised hash; runtime fault injection/новый product call этим review не разрешаются. Это воспроизводимый source path, а не заявление о наблюдавшемся hang.

## Expected230 — именно registrations, не assertion counter

В fixture все Deno.test calls на top level либо внутри конечных top-level registration loops. Ни один Deno.test не находится внутри callback другого Deno.test. Обход source выполнен вручную по callsites/array entries; только арифметика суммирования вынесена в inert postprocessing. Fixture/TypeScript не парсились и не исполнялись.

| Registration source lines | Expansion | Count |
| --- | --- | --- |
| 251–332 initial standalone | 6 | 6 |
| 342–364 descriptorMutations | 8entries | 8 |
| 365–386 unit invalid count/binding | 3×(6+3) | 27 |
| 387 strict JSON | 1 | 1 |
| 397–407 tool contracts | 3 | 3 |
| 408–424 unsafe storage | 3×6 | 18 |
| 425–435 limits | 8fields; inner2values execute within each callback | 8 |
| 436–469 metadataMutations | 20entries | 20 |
| 477 healthy readers | 1; inner summaries не регистрации | 1 |
| 500–522 report expectation/layout | 3×(3+4) | 21 |
| 523–537 Node report mutations | 9 | 9 |
| 538–548 Deno report mutations | 5 | 5 |
| 549–561 Python report mutations | 6 | 6 |
| 562–582 DOC06 plan mutations | 14 | 14 |
| 583–598 removed required steps | 1base+3units | 4 |
| 599 duplicate/base-only | 1 | 1 |
| 609–642 capture failure matrix | 4steps×6mutations | 24 |
| 643 source drift | 1 | 1 |
| 655 zero/skipped output | 1; inner2bad values не регистрации | 1 |
| 665 aggregate log | 1 | 1 |
| 677 CI args | 1; inner3scopes не регистрации | 1 |
| 691–702 workflow routes | 2 | 2 |
| 703 runner smoke | 1 | 1 |
| 713–724 nested keys | 8 | 8 |
| 725–731 missing units | 3 | 3 |
| 732–746 Python/Node propagation | 2×4 | 8 |
| 747 executor rejection | 1 | 1 |
| 766–773 unit expected counts | 3 | 3 |
| 774 default full route | 1 | 1 |
| 781–790 lexical storage | 3×4 | 12 |
| 796–828 healthy/unsafe relocation | 3×2callsites | 6 |
| 829 TMP itself | 1 | 1 |
| 837 prestart mismatch | 1 | 1 |
| 857–883 sourceGraph rejection | 3observations | 3 |
| Total | prior227 +3new registrations | **230** |

Поэтому expected230 обоснован как prospective Deno registered-test denominator для exact f02f… source, а не как число assert/equal/reject invocations. Observed_engine_tests остаётся null до исполнения/независимого raw review; static count не доказывает runtime registration/typecheck или pass.

Guard не интерпретирует test TAP как success: лучший capture verdict только CAPTURED_REQUIRES_INDEPENDENT_TAP230_REVIEW. Future independent result review должен сверить230unique expected names, complete plan, actual counters/all-pass и отсутствие skip/ignore/todo/cancel/only/filter, а не один exit0 или guessed synthetic layout. Нет права подменять observed count nominal230.

## Pure closure и permissions

Полностью прочитаны helper и fixture. Fixture импортирует только `../ops/docs_tests.ts`; helper не имеет imports и Deno API/dynamic import/eval/process/env/filesystem calls. Exported functions работают с caller metadata/strings, а child submissions внутри runChecks идут только через injected fake executor. Synthetic paths/tool commands — данные; fixture fakeExecutor.execute не spawn. Native16/CLI/process/environment/git modules не импортируются. Поэтому grant-free pure Deno run, private empty HOME/DENO_DIR/TMPDIR и отсутствие seed обоснованы для этих exact2files. Это не OS isolation proof и не native I2B acceptance.

Prospective final formatted closure нужно проверить снова: новый import/behavior не является format-only и блокирует baseline ancestry. Baseline helper676a…/fixturef02f… — не guessed final SHA.

## Historical RED проверен exact, без retroactive pass

Fixed v2 harness `0061c27ec61bf8ca15d6e94d304db695072b12adc3fe6ca8ddef2ee254df82e7`, plan `5147cab0a8df1d50fb908b3c247e8c7b0e11852ee01a990f8a35228b3e70157a`, historical fixture `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3`, receipt2724B `e874825467896121a89e7c0d31272ed5b923da8b0cc08e30846adca56c6806b0`, original raw765B `6b044ed571751341f215353d5dafd384dcf009a70c4b471595ebdcb53b8589ad` независимо перехешированы.

ANSI CSI stripping existing raw даёт604B, exact byte-equal source OLD_RAW_LAYOUT, включая TS2307+TS7006, URI13:8/311:36, marker spacing,2errors/info/hint/finalLF. Это не substring matcher и не проигрывание predecessor verifier. Erratum/review и design2/review hashes из ANCESTORS также независимо подтверждены. Функция predecessor сохраняет command/cwd/env/limits/source/runtime/capture/status/observed=null и inconclusive classification; fixed old H/P не сравниваются с new self/plan SHA. Eligibility record не создавался этим review, не ACCEPTED_RED и не результат227executed tests.

## Сохранённые controls и необходимые late gates

Exact-buffer helper loading проверяет тот же buffer и compile(...dont_inherit=True,optimize=0) в fresh non-main ModuleType, без SourceFileLoader/pyc; исходники target Python не импортируются. Historical/CPP/format/source/READY/H/P/helper refs перепроверяются terminally. Pinned runtime SHA проверяется streaming перед submission; terminal runtime hash не заявлен. Root отвечает за immutable Nix executable/prelaunch provenance.

Permanent folder и initial consumed receipt, full RawCapture и честный bounded-prefix fallback сохранены; missing EOF не complete. Independent terminal steps не выдают отсутствующие source/hash observations за исходные known hashes. Raw≤2MiB нужен complete/hash, overrun fail; failures оставляют consumed ID и failed/reconciliation metadata. Это сохраняется, кроме R1deadline gap выше.

RSS nullable, attempted/valid/unknown counts отдельны; минимум1valid обязателен, unknown не записывается0. Terminal observation после cleanup может быть unknown и отражается aggregate counter, не доказывает причины/полноты RSS sampling. RSS_status sampled при valid>0 означает наличие samples, не отсутствие gaps. TMP all-entry lstat bytes и regular payload отдельно; prelaunch+terminal observations обязательны. Sampled caps не hard quotas/transient peak proof; полный resource review остаётся по фактическим counters/gaps.

**Prospective source tools ещё не готовы:** plan содержит3future exact2file commands и limits120s1CPU1GiB32MiBTMP2MiBraw, но никакого source-tool supervisor не реализует/не запускает. До их calls Root нужен отдельный bounded guard/authority с exact argv/config/env/caps/capture/attempt identities; нельзя приписывать их контроль этому pure GREEN guard. После реальных fmt/lint/check нужны все3distinct accepted receipts, independent format-only baseline→final binding и CPP exact final source. Green READY source_evidence проверяет hashes/схемы refs, но не читает смысл receipt/review approvals: Root обязан проверить их substantive acceptance/status/commands/limits/provenance. Same-user JSON не создаёт authority.

После source correction R1 и этих gates требуется новый accepted guard review с exact H/P и свежий global Root handoff. Sole product call87→88,120s1CPU1GiB16MiBTMP2MiBraw остаётся неизменным; нового RED/retry/alias/native16/CI/science не возникает. Предыдущие source calls и old inconclusive RED не сбрасываются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
|230 — static Deno registered denominator | Все callsites/finite registration loops, explicit total227+3 | Observed=null, без execution/parser | сохранить |
| Pure closure допускает zero script grants/seed-none | Exact2files fully read, fake executor, helper imports/API absent | Final formatted source требует CPP | сохранить |
| Historical RED/current GREEN identities разделены | Fixed old H/P/04589/raw full layout vs fresh v3 READY | Inconclusive не принят как RED/pass | сохранить |
|120s termination действует при incomplete live collector | Non-daemon reader + finish timeout + unconditional alarm cancel | Runtime fault не воспроизводился | изменить |
| Source fmt/lint/check guards/late READY готовы | План prospective, supervisor/receipts/CPP отсутствуют | Отдельные Root gates до handoff | данных недостаточно |
| Runtime230/native/fullCI/science установлены | Executions0 | Данный source packet этого не доказывает | данных недостаточно |

Review budget: conservative logical reads≤2MiB при cap6MiB; wall<720s; report+identity<128KiB;1CPU/1GiB request. Physical CPU/RSS/I/O не измерялись. Начальный combined source output был truncated; необходимые guard/helper/fixture sections затем reread отдельно, выводы не основаны на скрытом truncated остатке. Prepared-code/parser/compiler/runtime/tests/network execution0; Root/CP/product writes0.

**STOP_SOURCE_CHANGES_REQUIRED: R1deadline correction; затем source supervisors и exact late bindings.**
