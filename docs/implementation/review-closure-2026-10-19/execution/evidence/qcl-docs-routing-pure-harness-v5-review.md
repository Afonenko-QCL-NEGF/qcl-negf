# Pure routing v5: независимый узкий high CPP

2026-10-20. Verdict: **PASS_SOURCE_R1B_R2_CORRECTIONS_V5**. R1b/R2 закрыты в exact v5 source; новых блокирующих замечаний в проверенном delta не найдено. **Это не observed runtime, не READY и не execution grant.** Root admission, реальные source calls, format-only/final CPP bindings и единственный GREEN остаются отдельными этапами.

V3/v4 reports/artifacts сохранены. Existing DOC06 E1 unknownFAILED и historical routing RED не переклассифицированы. Reviewer не исполнял/импортировал/парсил/компилировал prepared code, target/helper/runtime/tests/formatter/linter/check/native/network. Записаны только этот report и identity; source/fixture/Root CP не менялись.

## Exact reviewed packet

| Input | Bytes | SHA256 |
| --- | --- | --- |
| /tmp/qcl-docs-routing-pure-guard-v5.py | 53270 | e49cda399947c9ce9a60352c9def75076d8f5bab29d054f16a8d6874837e1372 |
| /tmp/qcl-docs-routing-pure-plan-v5.json | 13320 | 73b79ab73cf2b0702ace55de6f6c0cca6f48106bf0eaa7556221bad4804f9b06 |
| /tmp/qcl-docs-routing-pure-format-v5.py | 1363 | ddb56177a58077e502a1b647b034b590a01ee07d9ccc5de2634a5594c8c1060b |
| /tmp/qcl-docs-routing-pure-lint-v5.py | 1357 | 9c2e13e7f288d2705e12a3dc1378413deb5a045cdfc4b04f67a061a9c893112e |
| /tmp/qcl-docs-routing-pure-check-v5.py | 1366 | e2847a0f69cb470613946be8a9437fe930c1999bb66cca9388c2381d0d003cc9 |
| /tmp/qcl-docs-routing-pure-report-v5.md | 6833 | d3845f06f29720d5ed74c97aa81720884406eca901a666d733d1a07aef90c633 |
| /tmp/qcl-docs-routing-pure-identity-v5.json | 4132 | 5c90ec78c2985fe6f235faf5a5495a01d25d6b9fbbba33aca548fb21cedf83d2 |

Hashes/размеры пересчитаны. Full v4→v5 guard/plan/three-wrapper diffs и актуальные изменённые sections прочитаны отдельно. Preserved v4 review SHA `206731b357638ae735a0b33019108725f4cbe8d329b2009c2f35dce6633791bb`, identity `6adb662dbab01c2cd976fa53ffb8c0589c4dcc62f9614f45738a2d18645dd4e1`, guardc653… и plan4a896… подтверждены unchanged.

## R1b закрыто: unknown construction имеет bounded terminal path

Unit guard`:429–430`, source`:758–759` устанавливают collector_construction_attempted **перед** RawCapture call. Исключение после возможного native thread start не теряет факт неизвестного ownership при capture=None.

Unit finally`:448–466`, source`:776–791` после bounded stop_owned проверяют attempted+captureNone до обычного drain/fallback. Они не читают конкурентно pipe, не закрывают stream неизвестного writer и не выводят complete из fallback EOF. Сохраняются failed consumed identity, raw_capture_complete=false, collector_terminal=null, nullable raw count/SHA и отдельно best-effort stat prefix bytes. Затем os._exit(2) под активным watchdog. Ошибка persistence не создаёт retry и не приводит к Python non-daemon shutdown join.

Для присвоенного collector сохранён v4 lifecycle`:557–564` /`:885–891`: actual thread.is_alive проверяется перед alarm cancel; живой thread получает failed/incomplete receipt и force exit. Terminal-alarm record дополнительно различает attempted/known/unknown ownership. Путь captureNone без попытки construction не выдаётся за успешно построенный reader; source predecessor требует construction_attempted=true и collector_terminal=true.

Это source proof control flow, не измерение termination/fault injection и не абсолютная durability guarantee при отказе всех I/O.

## R2 закрыто: live unknown failure и отдельное pre-proven N/A

Unit observe`:387–402`, source`:718–731` сначала вызывают Popen.poll. Только полученный **до RSS attempt** terminal returncode переводит событие в RSS_NA_after_reap_proofs с PID/returncode/elapsed_seconds; rss_attempts/valid не увеличиваются и peak не подменяется0. При poll=None предпринимается live/unreconciled RSS observation.

None из rss_tree немедленно увеличивает unknown и устанавливает attempted_live_RSS_unknown. Если процесс исчез уже во время чтения, это остаётся failed unknown; поздний reap не снимает reason. Final guards`:521–524` /`:852–855` независимо требуют valid≥1 и unknown=0; exit0/ранний measured peak не отменяют отказ. Финальный observe после stop_owned/wait создаёт самостоятельный N/A proof только потому, что terminal доказан **до** новой попытки.

Source predecessor`:597–605` требует known collector construction, valid≥1, unknown=0, attempted=valid+unknown и exact N/A count/list/shape/PID/returncode/finite time. Unit source_evidence`:201–204` теперь проверяет все3receipt refs через этот gate в FORMAT1/LINT1/CHECK1 порядке, а не только их SHA. Следующий source stage и unit не продвигаются по receipt с attempted-live unknown. Historical DOC06 E1 остаётся failed; v5 predicate к старой telemetry ретроспективно не применяется.

## Отсутствие scope/order/history drift

Inert JSON comparison подтвердил byte-derived equality значений v4/v5: IDs/maximum_calls/expected230/ancestry/isolated base/shared budget/per-attempt limits/runtime/baseline sources/ancestor files/pure closure/child permissions/argv/env. Source commands, config, ordering и counter maps также unchanged.

Wrappers меняют только versioned guard path и pinned SHA. Их exact-buffer verified compile/exec lifecycle из v4 сохранён; shared helper loader source section byte-equal. Новый guard не запускает next stage, не создаёт predecessor/READY, не пишет CP и не расширяет grants.

- Source stages остаются FORMAT1/LINT1/CHECK1, по1call, counters2→3→4→5 при ceiling8. Exact config `a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce`, fmt.width100; commands/caps120s1CPU1GiB32MiBTMP2MiBraw неизменны.
- Sole unit остаётся DOCS-ROUTING-GREEN-1,87→88,230static registrations/observed=null,120s1CPU1GiB16MiBTMP2MiBraw и108s early stop/120s watchdog. Никаких RED/retry/alias/native16/CI/science calls.
- Pure owning files independently rehashed unchanged helper `676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c`, fixture `f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761`. Их ранее независимо проверенная registration expansion227+3=230 сохраняется; это не измеренный engine count и не число assertions.
- Retained CPP `4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea` остаётся whole CHANGES_REQUIRED с explicit positive pure slice. Whole I2B/native PASS не наследуется.
- Historical ANCESTORS и OLD_RAW_LAYOUT byte-equal v4: fixed v2 H/P/04589fixture/2724Breceipt/765Braw, два diagnostics TS2307+TS7006 с exact full normalized layout и original inconclusive. Versioned predecessor path меняется наv5, old artifacts не переписаны.

Global Root SourceRef остаётся late-bound отдельно от isolated2bb base; прежний107… лишь preparation/read anchor. Root обязан независимо установить actual fresh HEAD/status/gitlinks/CP/counters перед handoff. Guard проверяет exact SOURCE_HANDOFF/PURE_HANDOFF values и hashes, не создаёт trust из same-user JSON или CP marker.

## Оставшиеся обязательные gates

Format ownership не перенесено reviewer/author guards: actual FORMAT1 только по отдельному Root admission, потом independent baseline→final format-only review; LINT1/CHECK1 по тому же final source и accepted predecessor evidence. Final pure CPP и substantive approval всех3source receipts обязательны до unit READY. Совпадение refs и best captured verdict не заменяет их смысла.

Combined compiler-only flags/runtime acceptance здесь не измерялись; опционный/typecheck failure должен сохранить потраченный source ID и остановить продвижение без fallback/rerun. Sampled RSS/TMP/output stops не hard transient/cgroup/disk quota. Полный TAP230 names/plan/counters/all-pass/zero skip/ignore/todo/cancel/only/no-filter и source/guard/capture evidence проверяются независимо после единственного разрешённого вызова; guard return0 — не test pass.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Unknown collector construction больше не теряет terminal ownership | attempted-before-call, failed nullable receipt, no competing fallback, active-watchdog force exit | Source-only, без fault injection | сохранить |
| Attempted live RSS unknown блокирует результат/продвижение | Immediate reason + final unknown=0 + прямой predecessor gate всех3refs | Sampling не доказывает transient peak | сохранить |
| Reaped N/A не подменяет unknown нулём | poll proof до sampling, отдельные count/PID/returncode/time | Нет retrospective waiver | сохранить |
| Counters/grants/history/format ownership не расширены | Full diffs + invariant plan/section/hash comparisons | Future Root admission и final bindings ещё нужны | сохранить |
| Runtime/READY/GREEN/native acceptance установлены | Executions0, observed=null | Этот report только source CPP | данных недостаточно |

Finite reviewer budget: conservative logical reads≤1MiB при cap4MiB, wall<600s,1CPU/1GiB, report+identity<128KiB. Physical CPU/RSS/I/O не измерялись; absence не записана0. Prepared target/guard/parser/compiler/runtime/tests/network executions0; Root/CP/source writes0.

**PASS_SOURCE_R1B_R2_CORRECTIONS_V5; STOP_FOR_ROOT_ADMISSION_AND_LATE_BINDINGS.**
