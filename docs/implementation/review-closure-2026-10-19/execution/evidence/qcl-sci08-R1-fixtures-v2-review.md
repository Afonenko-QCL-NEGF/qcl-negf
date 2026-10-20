# SCI08-R1 fixture v2 — scoped independent high source review

**Вердикт: PASS_SOURCE_FIXTURE_ONLY, условный относительно будущего production I.** Fixture correction соответствует принятому D3; новых блокирующих замечаний в этом scoped diff нет. Recorder→journal→fake boot path ещё не реализован. ENG_READY, fake-only runtime и GREEN не установлены.

| Frozen input | SHA256 |
| --- | --- |
| V2 report | `fd85b55862a57177d59954196d23871182cf1c0cc9b45559f599bfef602a8928` |
| V2 identity | `87981037d559a9461b835a3a4d1c5d99b86c1cce78c3594197010948397bb254` |
| V2 patch | `e989e733d13a4b96f870358a599c494177703185978aa19d81f4f5568d7819ae` |
| D3 | `373a5da4ca765561e4a3ee46fa9c0bd06959a067ebf9f56c415e33666ad507c7` |
| Accepted high D3 | `7b8108df1708f103a988ca567feb0e50c8b8c8f455ac657217033ed692c0ff46` |
| Separate RED | `c519b715f645de58a27dea3e19cda5ad9142b393347a07dd8e4265edad914028` |

Runner `/tmp/qcl-sci08-r1-runner-worktree` HEAD заново подтверждён `fefaa27f194bfddf85dd51a0e255beef2218c06d`. Status: три modified selected fixtures и два new selected fixture files; recursive submodules пусты. `git diff --exit-code HEAD -- src`0 и `git diff --check`0. Production src сохранён baseline. Четыре прежних fixture SHA256 совпали с v1 и v2 identity; изменился только integration fixture: `63d83e77025c74140cd67af9d9efb2b1bb7df735bebf7ac9c06c4c16e3476a6a`.

Независимо просмотрены полный current integration source и его HEAD diff. Строки 16–21 создают literal boot A под `fake_proc=dirname(proc)` в `sys/kernel/random/boot_id`, с newline. Boot A/B — фиксированные UUID, не копия host observation. Callback:23 получает оба fake roots. Actual event sink:28 передаёт тот же `fake_proc` будущему recorder keyword; реальные phase begin/end:31–48 сохранены. Прямой cache-hit вызов journal:68 тоже явно получает fake root. Есть один fake boot file с последовательной заменой A→B, без preseed journal, global Base.read monkeypatch или real boot probe.

Все прежние 15 integration assertions сохранены в diff без ослабления. Четыре новых на строках64–69 проверяют literal boot prefix A, String directory key, identity `=== journal` после замены файла на B и неизменный cached clock domain. Последнее старое сравнение row1/row4 clock domain остаётся. Новые assertions не создают phase event; прежние count4 и pressure assertions остаются. `try/finally`:22/83–85 удаляет только journal/admission записи exact owned `root` через `pop!(...,root,nothing)` даже при ошибке. Чужие caches не очищаются.

Изменение `let` на `try` внутри существующего mktempdir do-block не переносит fixture variables в глобальное состояние. Производственный journal не создаётся вручную; после принятого I test будет проходить actual lazy initialization. Эти assertions имеют смысл только вместе с source trace: сами по себе они не доказывают отсутствия host reads или корректности default production behavior.

Ручная развёртка количества согласуется с v1 review:249 новых F/B/D/S/O +55 application +26 Linux +19 integration = **349 nominal assertions**, 31 logical groups,33 `@testset` blocks, пять includes. Четыре неизменных file hashes сохраняют исходные matrix rows/oracles; scoped integration diff добавил ровно4 assertions к прежним345, без новой required group. Это source count при достижении всех assertions, не parser/runtime receipt.

Условие source PASS: после отдельного observed behavioral RED owning production writer должен реализовать принятый D3 seam, а независимый I reviewer — проследить integration:28 → `_record_native_phase!(...;proc_root=fake_proc)` → `_native_phase_journal(...;proc_root=fake_proc)` → lazy `read(joinpath(fake_proc,"sys","kernel","random","boot_id"),String))`. Сохранить default `/proc`, strip/read/catch→boot_unknown, String directory-only get! key, first cached clock identity, struct/session/sequence/anchors, early returns и row schema. На текущем baseline keywords ещё отсутствуют: запуск этого integration fixture дал бы неподходящую API error, а не нужный behavioral RED. Поэтому production chain пока **pending**, прежний host-read finding не объявляется закрытым на actual implementation уровне.

Separate RED байты/hash неизменны; прочитанный файл содержит ровно2 assertions existing `_checkpoint_storage_forecast`: healthy literal16777728 и Bool-negative ArgumentError expectation. Он не включает integration, journal или новые helpers и не требует ранних production edits. Source prediction о нужном behavioral failure остаётся прежним; observed RED отсутствует. Missing import/environment/keyword error не заменяет требуемое RED evidence.

O1/O2 actual production caller traces, checked forecast+reserve и explicit envelope/policy propagation остаются prerequisite перед ENG_READY. Fake clock prefix не удостоверяет actual host/boot/process и не является trusted admission BIND. Strict campaign остаётся closed needs_guard/needs_admission; D1/D2/D3, scientific contract, C08 exhausted8/8 и общий SCI08 code-round cap не изменены. Никакого полного SCI/S1 pass из source fixture review не следует.

Выполнены только source/text/Git/hash проверки. Прочитаны v2 report/identity, integration source/diff и RED; bounded patch locator scan и SHA256 остальных selected files связывают unchanged v1 evidence. D3/high D3 hashes перепроверены; их ранее прочитанный contract сохранён. Conservative logical read charge с metadata/output reserve <524288B из лимита1MiB. Physical I/O/CPU/RSS не измерялись. Scope6min/1CPU/1GiB/report≤64KiB. Target parser/import/runtime/tests/build/SCBA/Poisson/native/network/install calls=0; production/CP/Git writes=0. Записаны только этот report и review identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Fixture v2 реализует D3 caller/boot/cache contract | Integration:16–28,64–69,83–85 + exact diff | Future production keyword отсутствует | сохранить |
| Старые15 integration assertions сохранены;349/31 | Diff без удалённых assertions;345+4; unchanged four hashes | Nominal source count | сохранить |
| Production baseline и отдельный RED сохранены | Empty src diff + RED c519… | RED не наблюдался | сохранить |
| Actual boot read уже fake-only | Только future caller binding | Recorder→journal production trace pending | данных недостаточно |
| ENG_READY/GREEN/full SCI/S1 достигнут | Target calls0; separate gates остаются | Нет runtime/admission receipts | данных недостаточно |

STOP. PASS_SOURCE_FIXTURE_ONLY не выдаёт runtime, production, native или science grant.
