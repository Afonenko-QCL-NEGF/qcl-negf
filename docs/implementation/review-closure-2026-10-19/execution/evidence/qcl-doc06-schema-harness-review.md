# DOC06 schema harness v1: независимый source review

2026-10-20. Verdict: **STOP_SOURCE_CHANGES_REQUIRED**. Это проверка текста и identity, не execution grant. Ни один подготовленный harness, helper, Deno, formatter, linter, target parser, compiler, typecheck или selftest не запускался/импортировался. Изменены только этот `/tmp` report и его identity JSON.

## Набор исходников

Проверенные SHA256:

| Артефакт | SHA256 |
| --- | --- |
| format-run-v1.py | 8bbd4a6ea15434188d8ab2c77075549e3a071e99aab0148ad29b005b02ba3ce2 |
| lint-run-v1.py | aad22de63191b5c9357c49fbc5264710dc3e190eab2505e70632162754fa4c94 |
| local-unit-run-v1.py | 5b1c4457fc3955b8691fb9126c636458476ecbe47b7e441c9c1a32ce481fc11e |
| engineering-plan-v1.json | 54f05c78253f5d3037dc71ecde67e131e297c46b5299f69f2d2b0f5d9a9f0342 |
| harness-report.md | a979563443854d7a6e4a0137d9672a791e0665158c4d05acd4ca2b42432e1da4 |
| harness-identity.json | cf12fbd084b8d7c01673dee3a77ba044721726291b4fb8d4d5ec0ca83de8c300 |

Все пути имеют prefix `/tmp/qcl-doc06-schema-`. Accepted CPP SHA `2706d0bb54a9e9027ae9cc633bc42fded380501a3ca45bd48400915e35c89be7` проверен. Current promoted source hashes совпадают с CPP: adapter `aa476aabdb044b020040816fdf7c2f7983082d28f6c15b01ccf1cbae307998ee`, tests `ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04`.

Фактический Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`. `git status --short` показывает modified checkpoint + эти2 source paths, untracked publication/evidence metadata; unrelated files не менялись этим review. `git submodule status --recursive` прочитан: восемь initialized gitlinks без `+`/`U`. HEAD source baselines независимо проверены как adapter `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`, tests `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69`.

## Блокирующие замечания

### R1 — неверный Root HEAD и отсутствие проверки фактического HEAD

Локатор: каждый v1 harness `read_ready():46`, plan `head`, report «Finite stages».

Все3 harness принимают только READY.head=`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; это HEAD author worktree CPP, а current Root уже `b07974b8e46bf8afdf1740947b842669a62a5ccc`. Корректный fresh READY на actual Root будет отвергнут после создания permanent attempt directory. READY со старой строкой, напротив, проходит эту часть gate на новом Root: harness нигде не читает actual Git HEAD, и `prelaunch_bindings`/`terminal_bindings` этого также не делают. Source hashes ограничивают2 paths, но не устанавливают правдивость identity Root.

Требуемое исправление: явно привязать plan/READY к выбранному current Root HEAD и проверить actual Git identity read-only при readiness/prelaunch/terminal (либо эквивалентный проверяемый binding); отдельно сохранить author CPP revision, не подменяя её current Root. Rehash packet. До исправления не создавать READY и не запускать v1, чтобы не сжечь единственный attempt на заведомом mismatch.

### R2 — RSS unknown записывается нулём и может пройти acceptance

Локатор: format/lint `rss_tree():152–165`, `peak=0:171`, polling`:194–198`, receipt`:261`; E1 `rss_tree():221–234`, `peak=0:240`, polling`:279–283`, receipt`:359`.

RSS читается только внутри `while process.poll() is None`. Fast child может завершиться до первой итерации: receipt всё равно получает `sampled_peak_process_tree_RSS_bytes:0`. Даже выполненный sampler при отсутствии VmRSS использует `'0 kB'`, подавляет OSError/ValueError/KeyError и суммирует отсутствующий pid как0. Отсутствуют completed/failed RSS sample counts и status. Таким образом unavailable observation неотличим от measured0; exit0+прочие успешные gates могут дать success. Это противоречит явному контракту measure/unknown, хотя унаследовано от прежнего harness.

Требуемое исправление: nullable peak/status и явные sample counters/errors; не подменять отсутствие VmRSS или unreadable live process нулём. Для нулевого числа измерений честно обозначить unknown и не выдавать RSS acceptance без принятой политики fast-exit evidence. TMP prelaunch/terminal sampling сохранён и эту RSS проблему не решает.

### R3 — error receipt может потеряться после потребления attempt identity

Локатор: E1 `original.log.open:260`, exception handler`:296–301`, finally summary read`:369`, receipt write`:374`; все3 scripts `folder.mkdir:18`, `temporary.mkdir:20` до защищённого `try:67`.

Если открыть original.log не удалось, catch записывает guard_error, но E1 finally затем без защиты читает отсутствующий/недоступный original.log для 74-test summary. Исключение происходит до записи receipt.json, и durable failure receipt теряется. Аналогично ошибка temporary.mkdir после успешного folder.mkdir оставляет потраченную permanent identity без prelaunch-failure.json. Ошибки ожидаемого capture/readback должны фиксироваться, а не обрывать receipt path.

Требуемое исправление: охватить все действия после успешного exclusive creation permanent folder внешним failure-receipt path; чтение summary выполнять только при доступном завершённом original capture, и записывать readback error/status до гарантированной попытки записи receipt. Если запись невозможна физически, вернуть явную внешнюю диагностику с attempt identity. Не объявлять no-child capture measured/complete при невозможном создании лога.

## Сохранённые controls и границы проверки

- `verified_module` проверяет SHA exact bytes buffer и затем compile/exec именно его в свежий ModuleType; `__name__` не `__main__`, поэтому main helper не вызывается. Оригинальные helper/sampler hashes совпали; никаких cached pyc loaders в новых sources нет. Runtime hash здесь прочитан из pinned packet, сам binary не хешировался в source-read budget.
- Exact argv фиксирует stage и2 source paths. Новые stage identities различны; exclusive permanent folder пресекает повторное использование. Fixed child env не наследует caller environment; Deno E1 permissions остаются exact test+adapter+ownedTMP read/ownedTMP write, без env/run/net/FFI. Test имеет единственный static import доверенного adapter; target strings остаются inert fixtures. Source fmt/lint argv запускает только static tools, pinned deno.json содержит fmt width100 без plugins/tasks invocation.
- Candidate→formatter receipt→accepted format-only review→fresh final READY source hash mapping проверяется для lint/E1; final source SHA не зафиксирован навсегда на unformatted candidate. Доказательство независимости format-only review остаётся обязанностью Root. Runtime result отсутствует.
- Seed inventory и `prepare_symlink_seed` отдельно сравнены как inert text с v2: exact equality. Inventory950B SHA `b4d67c005b58d18ec9e6b4c87aa1f86e372567fc70e35523859fa942150cc40d`; preparation3052B SHA `dac1667622549212c153f99ef7120de29368fdc0435a1911bcf51dbabb1a1632`. Сохранены13nodes,10dirs/2links/1zero regular,57B link payload, canonical owned0700 ancestors и explicit backing resolution.
- RawCapture full drain/fallback и final raw-overrun failure сохранены. TMP before_seed/prelaunch/loop/terminal probes сохраняют actual8MiB E1 threshold, source tools32MiB. CPU affinity1 и finite CPU/wall polling есть. RSS/TMP не являются hard cgroup/disk quotas; transient peaks не доказаны.
- План содержит только3 будущих calls: FORMAT1/LINT1≤20s1CPU1GiB32MiBTMP2MiBraw и E1once≤120s1CPU1GiB8MiBTMP1MiBraw. Expected unit count74 заявлен и summary проверяется в source; discovery/execution отсутствуют. Старые unit2/2, E1 1/1, actual2/2 retained, milestone81→87 ceiling и exactly1newunit не расширены. Никаких additional RED/actual/native/scientific calls этим review не разрешено.

Review выполнен чтением, hashes, Git metadata и ограниченным string comparison; candidate source не компилировался, не импортировался и не парсился. Логический source-read conservative upper bound1MiB при cap3MiB; wall<600s; report+identity<96KiB. Физические CPU/RSS/I/O не измерялись и не заявляются0. Ни Root source, ни CP, ни original artifacts не записывались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Root identity правдива и READY применим к current Root | Actual b079… против hardcoded2bb…; нет actual HEAD read | Child не запускался | изменить |
| RSS неизвестность отделена от измерения | missing process/VmRSS→0; counters отсутствуют | Реальная величина RSS неизвестна | изменить |
| Failed attempt всегда имеет receipt | E1 unconditional summary read до receipt; tmp mkdir вне try | Ошибка не инъецировалась | изменить |
| Seed/permissions/helper cache fix сохраняются | Exact source comparison, pinned helpers, argv/env review | Не runtime evidence | сохранить |
| 74unit GREEN/source tools прошли | Executions0 | Нужен отдельно разрешённый bounded этап после исправленного review | данных недостаточно |

**STOP.** Требуется исправленный source packet с новыми hashes и повторная независимая проверка. Этот verdict не разрешает запуск.
