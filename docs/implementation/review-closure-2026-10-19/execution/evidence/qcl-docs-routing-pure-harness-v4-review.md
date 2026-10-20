# Pure routing v4: независимый high source review

2026-10-20. Verdict: **STOP_SOURCE_CHANGES_REQUIRED**. V4 реализует три source stages и исправляет старый R1 для уже присвоенного collector. Остались два блокирующих paths: ownership collector может потеряться в constructor; attempted live RSS unknown не переводит guard в failure. **READY не выдан**, execution grant отсутствует. Старые reports/RED и DOC06 E1 unknownFAILED не пересматривались.

Проверка только source/metadata: prepared Python/TS/helper modules не исполнялись/импортировались/парсились/компилировались; Deno/formatter/lint/check/tests/native/network calls0. Root/CP/product/fixture edits0. Записаны только этот report и identity.

## Exact inputs

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| /tmp/qcl-docs-routing-pure-guard-v4.py | 47309 | c6534b6f1cf129877cd80482ebaddce7664dc179ff7f03760acef37f0f7a820c |
| /tmp/qcl-docs-routing-pure-plan-v4.json | 11825 | 4a8966be6c6bc5a3e4dfc1765b31b16be66355427af2b971e3d1c3bfd42646b6 |
| /tmp/qcl-docs-routing-pure-format-v4.py | 1363 | 4805b0be5aaf9e46c787f2ad43edaf0a57a35c522b52e24a91352fd947b9da70 |
| /tmp/qcl-docs-routing-pure-lint-v4.py | 1357 | 5c80d3c4d11c00809ae6e29316ce0d320373a1d9f85fd27851b4e19d1d90bb3c |
| /tmp/qcl-docs-routing-pure-check-v4.py | 1366 | 61be9d6f59b49856a1d4a0b3d85c194b4c00646efbf1a7f2bb32c4e91ca00463 |
| /tmp/qcl-docs-routing-pure-report-v4.md | 9731 | d0d3d51adb47082c5b7fe95bb778c8f20029406542d714e7b58a6f9a305dbabd |
| /tmp/qcl-docs-routing-pure-identity-v4.json | 3871 | 7403734acba6a513e7d5521dded926bf0e54d47af8fad244159e492c113e8240 |

Hashes/размеры независимо пересчитаны, source прочитан. Preserved v3 review SHA `85a8f8930b94824b07e9d46dc66240fc30e98a0e8499fac45cf95a9f928319ec`, v3 guard750fc… и plan9863… подтверждены неизменными.

Actual read-only metadata: isolated `/tmp/qcl-docs-test-routing-worktree` HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; coordinator `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` HEAD `107bac5697b37cf0e47c3feb44883a907837645c`. Это разные identities. Root перед каждым handoff должен заново проверить actual metadata/status/gitlinks/counters; source guard Git сам не вызывает. Exact SOURCE_HANDOFF/PURE_HANDOFF сравниваются с fresh READY, не выводятся из существования CP file.

## R1a: закрыта прежняя проблема для известного collector

Guard unit`:519–529` и source`:810–817` после receipt явно проверяют `capture.thread.is_alive()`. Живой известный thread сохраняет failed incomplete receipt и приводит к os._exit(2), alarm на этом пути не отключается. Неуспешная запись также приводит к terminal exit. Это исправляет указанный v3 path, где finish(timeout) мог оставить живой non-daemon thread, а timer безусловно отменялся. Thread не daemonized; EOF/error не переименованы в success.

## R1b — блокирующий остаток: collector construction не имеет раннего владельца

Локатор: unit `capture = raw_module.RawCapture(...):409`, source аналог`:705`, nullable initialization`:342/634`, ветки captureNone`:440–457/726–742`, terminal predicates`:514/520–529` и`:805/811–817`. Pinned `/tmp/qcl-local-julia-guard-v2.py:51–54`, SHA `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`.

RawCapture.__init__ создаёт non-daemon thread и вызывает thread.start **до возврата объекта**. Assignment capture происходит лишь после constructor return. Local Python3.14 source `/usr/lib/python3.14/threading.py:1003–1011` подтверждает: native thread запускается, затем start ожидает `_started.wait()`. BaseException/interrupt после native start, но до constructor return, оставляет caller capture=None при потенциально живом reader. Это именно path внутри объявленного BaseException failure handling, не выполненная fault injection.

Тогда fallback может читать тот же pipe параллельно неизвестному reader; отсутствие capture трактуется как collector_terminal=True, live-thread branch пропускается и alarm отменяется. Возвращающийся guard снова способен зависнуть на shutdown join неизвестного non-daemon thread. Fallback EOF также не доказывает sole-reader complete capture в этом construction-unknown состоянии.

Требуемое исправление: владение collector/его lifecycle до side effect start либо явное construction_attempted/construction_unknown состояние. При неизвестном исходе constructor после best-effort сохранения consumed failed receipt/prefix должен оставаться bounded terminal exit/deadline; нельзя использовать captureNone как доказательство отсутствия reader. Completeness остаётся false/unknown, не выводится из fallback EOF, если конкурирующий reader не исключён. Shared helper hash менять/ослаблять для этого не требуется. После исправления — source re-review новых exact hashes, без runtime calls.

## R2 — блокирующее: attempted live RSS unknown не fail closed

Локатор: unit observe`:384–391`, source observe`:671–678`; финальные predicates unit`:490–502`, source`:781–794`; source predecessor gate`:562–565`.

Когда rss_tree возвращает None, observe только увеличивает rss_unknown. Stop reason/error не устанавливается. При хотя бы одном более раннем valid sample итоговый good может остаться true; `sampled_with_gaps` и counter честнее нуля, но **не являются failure gate**. Source predecessor reader также требует лишь RSS_valid_samples≥1 и measured peak<cap, поэтому передаёт receipt с неизвестным live interval дальше в LINT/CHECK. Это не выполняет порученный контракт «unknown metrics fail».

Важно отделить два состояния. В текущем finally после stop_owned/process.wait все observe снова пытаются читать reaped PID и обычно добавляют unknown. Это **не** основание обнулять counters или ретроспективно объявлять live error harmless. Нужен явный predicate:

1. RSS call, предпринимаемый для live/unreconciled процесса, при None/malformed/read error сохраняет unknown/error и даёт failed/NotCapable outcome; хотя бы1valid sample всё равно обязателен.
2. Только доказанный terminal/reaped **до попытки sampling** процесс получает отдельный N/A-after-reap/gap record, без fabricated0/valid RSS sample. Если процесс исчез в ходе attempted live sample, историческая причина остаётся unknown.
3. Final acceptance и source_receipt_ref запрещают хотя бы1attempted-live-unknown; aggregate counts/phases/status сохраняют все gaps и измеренные lower bounds. Нельзя открыть следующий source stage или unit по одному measured peak и exit0.

DOC06 E1 historical29valid+1unknownFAILED остаётся неизменным. Ни этот source review, ни future policy correction не переклассифицируют старую ошибку.

## Три source stages: реализованы, finite scope сохранён

Wrappers полностью прочитаны: каждый проверяет canonical owned regular bounded guard, SHA **того же buffer**, затем future compile/exec(...dont_inherit=True,optimize=0) в fresh non-main ModuleType без pyc/SourceFileLoader. Wrapper передаёт fixed FORMAT1/LINT1/CHECK1, caller argv не выбирает stage. Shared source_main повторно проверяет wrapper/guard/plan exact bytes из READY; target code Python не импортируется. Эти compile/exec statements здесь не выполнялись.

- FORMAT1: exact baseline helper676a…/fixturef02f…, один fmt exact2paths.
- LINT1: independent format-only baseline→final ref плюс exact fmt receipt/raw.
- CHECK1: те же final hashes, fmt+lint receipts; только compiler command двух TS files, без test execution/registration.

Source ready fields, distinct exclusive attempt folders и shared_source_budget требуют2→3→4→5 при ceiling8, по1reserved call. Predecessor gate проверяет stage/argv/cwd/env/limits/rawSHA/size/exit/capture/collector/source hashes. Stages не вызывают следующий stage, retries/aliases/extra RED нет. Unit identity неизменна DOCS-ROUTING-GREEN-1, budget87→88 и solecall1. Failed phase не возобновляется удалением attempt directory.

Все commands source используют actual isolated deno.json SHA `a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce`, strict=true, fmt.lineWidth100; config прочитан полностью, plugins/import maps отсутствуют. Они не выполняют tasks из config и не меняют config. Raw argv фиксирует offline check flags; их runtime option support новым probe не измерялся — unsupported option должен расходовать CHECK1 и остановить продвижение, без fallback flag changes.

Future source receipt лучший verdict — CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW, observed_engine_tests=null/test_registration_performed=false. После источников остаются обязательны substantive independent approvals all3receipts, format-only baseline→final review, exact final CPP и fresh unit handoff. Unit source_evidence хеширует3distinct receipt refs, но trusted Root обязан проверить их смысл/стадии/команды/лимиты, а не приравнять same-user JSON или hash к authority.

## Pure-only CPP и230 denominator

Retained `/tmp/qcl-docs-routing-impl-i2b-review.md` exact SHA `4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea` прочитан. Его whole verdict CHANGES_REQUIRED сохраняется. Прямо выделенный positive pure slice разрешает отдельную prospective pure проверку; он не означает native/source integration PASS. Source READY requires pure_only_slice=true/PURE_CPP; unit требует тот же slice плюс отдельный exact final formatted closure review. Такое разделение корректно.

Baseline pure files независимо перехешированы: helper `676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c`, fixture `f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761`. Они совпадают с fully read v3 audited closure: only fixture→helper, no helper imports/Deno API/process/env/FS, fake executor только manufactured captures. Native16/CLI/environment/git imports не нужны; grant-free unit и private empty HOME/DENO_DIR/TMPDIR остаются обоснованы. Config selected для source tools, unit остаётся no-config.

Static230 registrations подтверждены прежним независимым полным callsite/loop audit34groups на exact f02f… source:227первых+3sourceGraph failures. Hash identity сохраняет применимость этого подсчёта; это не assert count и не measured engine count. Final format-only review должен сохранить registrations/names/loop bounds. Future result acceptance требует полного TAP230 unique names/plan/counters/all-pass/zero skip/ignore/todo/cancel/only и nofilter; exit0 либо captured verdict не равен passed tests.

## Historical RED и remaining safety limits

OLD_RAW_LAYOUT v4 byte-equal сохранённому v3 и independently normalized original raw:765originalB,604B после только ANSI CSI stripping, TS2307+TS7006 exact order/URI13:8/311:36/marker/info/hint/finalLF. Fixed historical v2 H/P/04589fixture/receipt2724B/raw765B/erratum+review refs не смешаны с current v4/final hashes. Original inconclusive classification и observed=null сохраняются, predecessor-v4 record ещё не создан и не ACCEPTED_RED.

Nullable peaks/attempted-valid-unknown counters, TMP all-entry+regular metrics, prelaunch/terminal TMP samples и bounded raw/prefix/original retention реализованы. Capture/raw/hash/terminal-source errors не превращаются в semantic pass, initial consumed receipt и best-effort terminal receipts остаются. Конкретные residual lifecycle/RSS acceptance defects описаны выше. Sampled caps не являются hard RAM/disk/cgroup/OS isolation; deadlined receipt persistence не может гарантировать durability при полном I/O отказе. Runtime hash preflight streaming и terminal source/H/P/helper/review/READY refs есть; terminal executable measurement не заявлено.

Reviewer только перечитал local Python stdlib source для ownership path; Python threads/RawCapture/guards не исполнялись и fault injection не делалась. No product calls/source calls/counter updates. После правок Root должен получить новый source verdict и только затем делать отдельные fresh admitted calls; этот report не READY и не permission flow.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Старый R1 для известного collector исправлен | is_alive→failed receipt+os._exit перед timer cancel | Не покрывает потерянный constructor owner | сохранить |
| Все constructor failure paths bounded | Assignment-after-start, captureNone bypass terminal check | Source path; fault не исполнялся | изменить |
| Live unknown RSS не проходит ресурсный gate | None увеличивает counter без reason; good требует только≥1valid | Gaps честно видны, но gate не закрыт | изменить |
| Source fmt/lint/check finite supervisors реализованы | Fixed wrappers/stages/config100/counters2→5≤8 | Пока source-only; R1b/R2 блокируют admission | сохранить |
| Pure CPP/230/historical identity сохранены | Exact4903slice,676a/f02f, fixed old two-diagnostic layout | Whole I2B CHANGES_REQUIRED; observed=null | сохранить |
| Runtime/unit/native/CI/science приёмка достигнута | Executions0 | Этот review не даёт исполнения или приёмки | данных недостаточно |

Review limits: conservative logical reads≤3MiB при cap8MiB, wall<900s,1CPU/1GiB, report+identity<192KiB. CPU/RSS/physical I/O reviewer не измерялись. Начальные combined outputs были truncated; все необходимые guard sections/CPP header/config затем перечитаны отдельно. Старые reports сохранены; source/CP/product writes0.

**STOP_SOURCE_CHANGES_REQUIRED: R1b collector-construction ownership и R2 live-RSS unknown gate.**
