# DOC06 schema: независимая format-only проверка

2026-10-20. Verdict: **PASS_FORMAT_ONLY_EQUIVALENCE**. Проверены ровно два owning source paths после sole DOC06-SCHEMA-FORMAT-1. Accepted CPP `2706d0bb54a9e9027ae9cc633bc42fded380501a3ca45bd48400915e35c89be7` сохраняет применимость к этим formatter-equivalent исходникам. Review не устанавливает compiler/type correctness,74-unit GREEN, actual meaning или scientific acceptance и сам не является разрешением следующего запуска.

## Exact binding

Before root `/tmp/qcl-doc06-schema-preformat-v2`; after Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`. Fresh read-only HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc` совпал с formatter receipt observations.

| Path | Before SHA256 | After SHA256 |
| --- | --- | --- |
| ops/docs/static-slice.ts | aa476aabdb044b020040816fdf7c2f7983082d28f6c15b01ccf1cbae307998ee | a852318af5105aaf224913e2264342c4349cb0ed70991842f00ab78e4d6c4b72 |
| tests/docs_static_slice_test.ts | ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04 | 45febb3ccfdd9d641447d5cec6e26bbfc6c9b97f188c2e9a620142794c1a3b31 |

Frozen diff `/tmp/qcl-doc06-schema-format-only-v2.diff`17792B SHA `a645fe4317d061ba713aa084cc0686c9b8df62dde3b7728bd3b8a11e47cfd700` независимо воспроизведён обычным inert text unified_diff из exact before/after files. Получены те же bytes, поэтому review diff не пропускает изменения файлов. Прочитаны все8hunks:3adapter и5tests.

## Почему изменения эквивалентны

Adapter: развёрнут object literal `rootRequired` с той же value/selector; развёрнут вызов allowed с теми же четырьмя аргументами; строковая конкатенация coverage текста перенесена после `+`. Добавленные trailing commas относятся к object/argument syntax. Ни literal text, ни selector, ни условия classifier не изменены.

Tests: параметры функций и аргументы assertions/calls разнесены по строкам; длинные tuples и for-of headers отформатированы с прежним порядком элементов; callback arrow expressions и property access `.map`/`.selector` сохранили те же expressions. String literal `'[]'` заменён на `"[]"` с тем же содержимым. Единственный single-statement `if (absent === "description_absent")` получил braces вокруг прежнего assignment; последующий await fixture остаётся вне if, else отсутствует. В завершающем Deno.test callback перенесён по строкам без изменения return-expression.

Ни predicate/assertion, ни expected value/status/mode/reason/locator, ни fixture string/template contents не заменены. В diff нет import/permission/I/O изменения или добавленной регистрации теста. Tests prefix до комментария M1/M2/M3 —35096B — независимо сравнен byte-for-byte и совпал; baseline controls не затронуты. Новые18 registrations сохраняют source contract74 совместно с принятым baseline56. Это не test discovery и не исполнение.

## Formatter receipt

`/tmp/DOC06-SCHEMA-FORMAT-1/receipt.json`4120B SHA `aaaf0be83c834ba83736959d37025113dc067c306ed0dc9ed4b46736d3be3dcc` независимо проверен. Stage/schema-plan/harness/input/output/CPP hashes соответствуют v2 packet и текущим файлам. Receipt показывает outcome=guarded_pass, exit0,0.719s, raw_capture_complete=true, no stop/guard/capture/overrun errors;2completed/0failed RSS observations и3TMP samples. Guarded source-format outcome не приравнивается к compiler/unit/scientific gates.

Original log189B независимо прочитан и хеширован: `dbd62c13facc85425d25919de4a089675905eb14da7f39fcf404d1c3983005b9`, совпадает с receipt raw_metadata. Вывод перечисляет ровно2source paths и Checked2files. Sampled RSS/TMP остаются ограниченными sampling metrics; transient maximum не доказан.

Записан machine binding `/tmp/qcl-doc06-schema-format-only-review.json` с ровно полями verdict/input_source_sha256/output_source_sha256/formatter_receipt_sha256/accepted_cpp_sha256 для последующего Root READY.

Проверка только читала bytes, Git HEAD и metadata, строила inert text diff. Reviewer не запускал formatter/linter/compiler/parser/typecheck/runtime/harness/helper/tests и не менял Root source/CP/оригиналы. Записаны только этот report, machine binding и identity. Conservative logical reads≤1MiB при cap2MiB; wall<600s; report+JSON+identity<128KiB. Физические CPU/RSS/I/O reviewer не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Accepted CPP source и formatted source эквивалентны | Полный independently regenerated diff; все8hunks рассмотрены | Без compiler/parser execution | сохранить |
| Formatter receipt привязан к exact before/after hashes | Receipt SHA + input/output/CPP maps + raw189B SHA | Только formatter stage outcome | сохранить |
| Baseline controls и74 source contract сохранены | Exact35096B prefix + неизменные assertions/registrations в diff | Unit не выполнялся reviewer | сохранить |
| LINT/unit/actual/science приёмка установлена | Этот review таких executions не содержит | Нужен отдельно разрешённый следующий bounded этап | данных недостаточно |

**PASS_FORMAT_ONLY_EQUIVALENCE; следующий запуск остаётся за Root readiness.**
