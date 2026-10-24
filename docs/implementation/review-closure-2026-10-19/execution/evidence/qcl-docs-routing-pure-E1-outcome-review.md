# Независимый outcome review DOCS-ROUTING-CORRECTION-E1

**Software verdict: PASS_TAP232_QUALIFIED. Resource gate: FAILED_UNKNOWN_RSS. Итог попытки: STOP_RECONCILE_NO_RERUN, consumed, без waiver и повторного запуска.**

Полный существующий TAP разобран независимо metadata-only Python regex/JSON/SHA; проверяемые scripts/import/compiler/tests/network/solver не исполнялись. Чтение controller не означало его исполнение. Новых CP/READY/product/index изменений и дочерних агентов нет; созданы только этот отчёт и identity в `/tmp`.

## Software evidence

Receipt `/tmp/qcl-DOCS-ROUTING-CORRECTION-E1/receipt.json`:8519B SHA256 `2accfd34c74b0e48f2f73f194531f88dbbde8eaeea9e123618749eac68cdecf4`. Original raw15889B SHA256 `3b3b8dd81b11ada11829b07399b4c0138e5c0177c806c5ca329d579eea835006`; прочитаны все bytes, сохранённый raw не менялся.

Полный raw имеет235 строк: `TAP version 14`, единственный source comment,232 результатов и финальный `1..232`. Независимый разбор подтвердил ровно232 `ok`,0 `not ok`, ID строго1…232 без дублей/пропусков/перестановок,232 уникальных имён, единственный plan на последней строке235. Все строки классифицированы, неизвестных/diagnostic/error/bailout строк0. SKIP/TODO/XPASS directives0. Упоминания skipped/todo в названиях негативных controls не являются directives. Номинальный source registration232 и наблюдаемый полный TAP232 согласуются. Child exit0 проверен отдельно, сам по себе он не был критерием принятия.

Точные frozen sources before=after=actual files: `ops/docs_tests.ts` SHA `12fbb1d8c754536135e7b919ca14a465532bd3910bdff7f68ef6fdb129376bab`; `tests/docs_test_routing_test.ts` SHA `a629e366cdebacc9d6ffbef1458990cf00232d99ca3cb1668696c169fc4a1164`. Config actual SHAa637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce неизменён. Accepted H/P e02576c6…/e32f4b53… совпадают с receipt/READY; source closure и mixed FORMAT3(v8)/LINT3(v8)/CHECK4(v9) остаются привязаны к предыдущим independent reviews, не заменяются exit0 E1.

Подтверждены actual passing results:

| ID | Control/regression | Что доказывает в frozen pure fixture |
| --- | --- | --- |
| 2 | full plan executes exactly base Python Node DOC06 once with finite caps | структура плана четырёх logical children |
| 4 | healthy fake aggregate requires four typed receipts and retained-only versions | healthy fake route и typed receipts |
| 179 | source change after a healthy child fails binding and retains available evidence | failed binding после сохранённого capture |
| 205 | executor rejection retains completed base and terminal failed attempt without retry | сохранение terminal aggregate при rejection |
| 229 | pre-start source mismatch retains failure with zero child submissions | новый paired regression:0 child/captures при исходном mismatch |
| 230,231,232 | sourceGraph rejection at observation1,2,6 retains terminal aggregate | новый paired regression: source not_measured, failed aggregate,0/1/4 сохранённых capture и столько же submissions |

Source locator `ops/docs_tests.ts:789–843`: healthy route наблюдает source6 раз: до children, после каждого из4 children, затем final. `tests/docs_test_routing_test.ts:1145–1179` прямо инъецирует отказ только в observations1,2,6; observations3–5 находятся в прошедшем healthy route, отдельной fault injection в них нет. Полный TAP не содержит внутренних traces всех6 reads; прохождение healthy route и размещение calls — software/source evidence, а не отдельная инструментированная телеметрия каждого source read. Fixtures используют fakeExecutor и synthetic captures, поэтому этот verdict не является выполнением реальных Python/Node/DOC06/base children, full CI или научного solve.

## Resource gate и наблюдаемая причина sample

Receipt: target_calls1, consumedtrue, child exit0, guard verdict STOP_RECONCILE_NO_RERUN и stop_reason attempted_live_RSS_unknown. RSS attempted45=valid44+unknown1; valid≥1 выполнено, unknown==0 **не выполнено**. Отдельный N/A1 имеет proof Popen.poll_returncode_before_RSS_attempt, PID3107322, returncode0, elapsed2.195821158005856s. Этот более поздний отдельный N/A не отменяет уже attempted-live unknown. Нельзя ретроспективно считать неизвестный RSS нулём либо N/A.

`receipt.json/RSS_failure_diagnostics/0`: ровно1 captured event reasonVmRSS_shape_or_unit, stepVmRSS_shape, `/proc/3107322/status`; root_pid=pid=child_pid3107322, tidnull, errno/errornull. Полный status1177B сохранён hex без усечения; SHA decoded bytes `f20cdf53a7a70274ac8ccd0dec906f774f3b9d4824ff769e80773efed36a777b`. Он содержит Name deno, State Z(zombie), Pid/Tgid3107322, PPid3107321, Threads2 и не содержит VmRSS. Именно отсутствие ожидаемой VmRSS строки в этих прочитанных bytes объясняет возврат None по VmRSS_shape данного sample E1.

Это наблюдаемое kernel state во время одного чтения. Оно не устанавливает более широкую причину/порядок завершения, состояние descendants, полную lifecycle/PIDbirth identity, hardpeak, установленный race или причину исторического CHECK3. Birth identity явно null/not_read; task census/children для этого event не читались и остаются null. CHECK3 не имел такого snapshot и сохраняет cause UNKNOWN. Diagnostic state: events_seen1,dropped0,capture_errors0,truncatedfalse.

Другие наблюдаемые gates: wall2.2041144980466925s<120s; sampled RSS343982080B<1GiB, ownedTMP609109B<16MiB, raw15889B<2MiB. TMP47samples, initial220/final609109B. Raw capture complete, collector construction attempted и terminaltrue; raw_capture_error/guard_errornull, rawoverrunfalse. Эти величины не восстанавливают startup/междусэмпловый peak и не доказывают hard quota. Exact limits120s/affinity1CPU/RLIMIT_CPU120s/1GiBRSS/16MiBTMP/2MiBraw. Одно нарушение unknown RSS достаточно для FAILED при действующем неизменённом критерии, независимо от остальных caps и TAP232.

## Root binding и счётчики

READY actual SHA `f2ae5dc2f154cb86c9cd93a5366f2b4b104966afba2e49528b8e1ce6c8957afc` совпадает с receipt; handoff SHA `e84ec4500590b6b3c0278b1b7b09c3733a0d50964edaed60c7663a8b0d169557` совпадает с READY. Handoff/READY/receipt совпадают по frozen source и product90→91cap91/no_rerun. Whole fixture argv: pinned deno test, no-config/no-lock/cached-only/no-npm/no-remote/no-prompt/reporter=tap, exact fixture path, без filter/only/script grants. Cwd exact isolated worktree; environment_clear=true, только CHECK E1 private owned-tmp DENO_DIR/TMPDIR/HOME.

Outer SHA `36973ad2258bef0cbdc0f2c8d4a52a1af10dce35c88f814c1962e5ed4b226f18`: wrapper_returncode1, outer_failure=null, stdout/stderr empty, outerwall2.5958025379804894s — известное завершение failed guard. Controller SHA `14062cce38970c7927b38ba1e6b94035a67e94945ff284a46c1669c922d01365`; прочитан как source, execution не повторялось.

Root фактический HEAD107bac5697b37cf0e47c3feb44883a907837645c, все8 recursive gitlinks прочитаны, совпадают с предыдущим immutable set. CP snapshot SHA `ecfbb241e3b83ded267395637b6243fd26f6c6a8844fc6d8a321ccfc84774ed8`: product91/91 и source12/12 EXHAUSTED; targeted_test_active/source_tool_active/native_build_active=null, unknown_outcomes=[]. SCI05_08_C08 cap8 неизменён; этот запуск не создаёт fullCI/science evidence или новый бюджет. Legacy pure/v9 preunit summaries подлежат Root reconciliation: ссылаться следует на actual complete failed attempt, software/resource вердикты раздельно. Возможность дальнейшего engineering решения не является разрешением автоматического rerun/изменения criteria.

Физические CPU/RSS/I/O рецензента не измерены; output budget compliance не заявляется. Runtime binary повторно не хешировался; его frozen digest проверен по metadata, а source/config/raw проверены по actual bytes.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Frozen pure software232/232 passed | полный raw3b3b8dd8, строгий разбор всех235 строк | fake controls, не реальные children/CI/science | сохранить |
| E1 resource gate FAILED | receipt2accfd34:44valid1unknown | не подлежит waiver по действующему критерию | сохранить |
| VmRSS отсутствовала при StateZ в sample E1 | полный status1177B SHA f20cdf53 и diagnostic VmRSS_shape | birth/descendants/exit ordering/CHECK3cause неизвестны | сохранить |
| Общая причина устранена | доказательства отсутствуют | rerun и criteria change не поручены | данных недостаточно |
| Counters исчерпаны, outcome известен | CP91/91,12/12,nullactive,unknown_outcomes[] | старые summaries требуют reconciliation Root | изменить |

STOP review-only. Не выдавать общий PASS для попытки; original failed receipt/raw сохранить точно.
