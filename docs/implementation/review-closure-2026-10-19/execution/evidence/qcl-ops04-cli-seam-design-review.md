# OPS04.S — независимый source-only review CLI seam addendum

2026-10-19. **APPROVE на уровне source design: блокирующих технических замечаний к addendum не найдено.** Решение координатора, CP-CODE и разрешённое исполнение fixtures остаются отдельными gates. Это не проверка реализации, Nix evaluation, native/scientific acceptance или новый runtime grant.

## Identity, scope и ограничение независимости

Проверен candidate `/tmp/qcl-ops04-cli-seam-design.md`, SHA256 `93ffbbcdd50770295f2f21e1a9befc47acc63231279b1ff79aebf48e7cc69a7f`; identity SHA256 `1979f183b9035f891c2296687aba2944b8628a084c1c73b6c0b8c7e7e5d4949f`. Принятые parent D2 и его high review имеют SHA256 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147` и `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`.

Checkout `/tmp/qcl-ops04-root-worktree`, фактический HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Начальный и конечный `git status --short` содержат только frozen изменения `tests/application_cd_test.ts` и `tests/solver_test.ts`. `git submodule status --recursive` показывает восемь неинициализированных selected gitlinks; они не обновлялись. Targeted `git diff --exit-code HEAD -- ops/solver.ts ops/application_cd.ts nix/solver.nix ops/git.ts ops/process.ts` пуст и завершился с exit 0. Их прочитанные product sources соответствуют root HEAD.

Review выполнен отдельным от автора агентом. **Ограничение процедуры:** при первом batched read candidate был прочитан раньше primary `ops` files; затем выполнена проверка по ним. Это не blind source-first review. Ограничение было сообщено координатору до результата; этот report не выдаёт иной порядок за выполненный. Технические выводы ниже привязаны к primary sources, а не к согласию с автором.

Разрешённый envelope: ≤20 min, 1 CPU, 2 GiB RAM, reads≤3 MiB, report≤64 KiB. Cumulative CPU/RAM/read/tool-output telemetry не инструментировалась; пределы не выдаются за измеренные значения. Выполнялись только текстовые чтения/поиск, Git metadata/diff, SHA256 и записи review artifacts в `/tmp`. Target imports/parsers/tests, Deno, Nix, Julia, build/install, network/server, source edits, Git mutations, children и checkpoint writes: **0**. Независимый reviewer не запускал автора или дочерних агентов.

## Техническое сопоставление

Primary `ops/solver.ts::solver:124–136` сейчас читает JSON через `Deno.readTextFile` внутри private orchestration. `buildSolver:44–110` имеет callback seam, но допускает independent object/path inputs; `nix/solver.nix:2–9` повторно читает pathname. `ops/application_cd.ts:63–107` держит сборку в `import.meta.main`, а `.#application` на 69–76 предшествует metadata capture на 77. Поэтому одни direct helper fixtures не доказывают production capture или assembly-before-command. Новые именованные orchestration exports адресуют именно этот gap.

1. **Single capture и byte bound заданы исполнимо.** `captureDepotMetadata` имеет один opener и один descriptor с `stat` перед data read, циклом short reads в оставшуюся часть 65537-byte buffer, sentinel rejection без следующего read и reject нулевого progress. Ровно 65536 bytes требуют EOF на попытке прочитать sentinel. `finally` закрывает каждый успешно открытый descriptor при success/stat/read/decode/size failure. Raw NUL/BOM, fatal decode и byte roundtrip проверяются до JSON preparation. Неограниченного read с последующей проверкой нет.

2. **Фактически потреблённый input остаётся единым.** Addendum сохраняет D2 API `buildSolver(metadataJson, expectedGraph, expectedManifest, execute, options?)`, без unchecked object/path overload. Общая preparation routine валидирует полный graph и Manifest, нормализует один parsed input и связывает exact produced UTF8 JSON с SHA256; archive URL/hash для prefetch берутся из того же значения. Оба operational callers названы и обновляются вместе. Search по root `ops`, `tests`, `nix`, `flake.nix` подтвердил эти два TS callers; отдельный `nix/local-lab-packages.nix:14` route не получает нового consumption claim. Nix JSON/SHA assertion и удаление late pathname остаются обязательным D2 изменением.

3. **Порядок application assembly достаточен.** Capture → graph snapshot → Manifest hash → общий полный preflight предшествуют любому `execute`. Поздний `buildSolver` повторно проверяет тот же immutable string, без нового pathname access. Graph recheck после path-info остаётся и блокирует публикацию до cache copy/pending/rename. Изменение файла A→B на первом application callback не влияет на уже captured A. Подмена до capture должна проверять фактически captured B; валидный B не обязан отвергаться только из-за отличного archive URL/hash.

4. **DI не подменяет проверяемую логику.** Разрешены низкоуровневый opener, readonly identity reads и command dispatch; запрещены injection готового captured string, validator, buildSolver или готового assembly result. Production CLI delegates тем же exports, а production defaults используют существующие Deno APIs, `sourceGraph`, WebCrypto и `run`. Snapshot dependency references до await и собственная копия graph предотвращают обычную mutable-fixture подмену. При code review надо проверить именно эти свойства, включая вложенные components, а не только shallow object copy.

5. **Fail-closed границы сохранены без новой policy.** Malformed JSON/type, invalid encoding/size, неверные identities, неизвестные/дублированные build flags и T2 cache failures обязаны дать reject и 0 execute callbacks. Неизвестные неиспользуемые JSON metadata fields **сохраняются** по принятому D2; их наличие не является неизвестной командой или основанием ввести новую schema policy. Internal exports не образуют новый пользовательский CLI. Flags/defaults, literal URI argv, capture/inherited stdout и release digest `SHA256(JSON.stringify({sources,closures}))` сохраняются. Scheme/trust policy, runtime environment и source authority не расширяются.

6. **Предлагаемые fixtures различают реальные дефекты.** Instrumented opener проверяет production read loop и max bytes; реальные временные файлы — decoder, regular-file check и roundtrip; оба actual CLI seams — preflight до dispatch; A→B именно на первом application build — causal early capture. Full fake assembly выполняет production pending/rename и проверяет recheck/copy ordering. Независимый SHA от actual outgoing JSON сверяет argv и returned binding. Эти fixtures не сводятся к source grep или дублированию validator и не заявляют выполнения Nix parser/assertion. Frozen tests сейчас покрывают D2 helper contract; им не приписывается новая CLI coverage до реализации и исполнения добавлений.

## Остаточные границы

Один descriptor исключает позднее разрешение pathname, но не обещает атомарный snapshot против trusted writer, malicious capture-path/FIFO race или hard-blocked kernel I/O. Это явно оставлено вне claim в D2 и addendum; новое trust enrollment не появилось. Real FIFO fixture не требуется для заявленного контракта.

Source design не доказывает, что будущая реализация выполнит snapshot/close/ordering корректно. Предстоящий CP-CODE должен сопоставить exports, production adapters, preparation reuse, exact argv и causal fixtures с этим контрактом. Один общий разрешённый Deno slot T1+T2 остаётся будущим и зависит от counters/prepared runtime/owned TMPDIR; review его не расходует и не создаёт ещё один invocation. Nix hash assertion, native output/origin и scientific acceptance остаются отдельными отсутствующими receipts.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Addendum задаёт production CLI seam, а не test-only копию | Named exports и низкоуровневая DI; primary private CLI bodies cfc38e1 | Только design, реализации и исполнения нет | изменить |
| Exact JSON/SHA и полный graph распространяются на оба callers | Addendum + D2 T1; caller search; no pathname fallback | Nix assertion не исполнялся | сохранить |
| Capture bound/UTF8/close и ранний preflight причинно проверяемы | Instrumented handle, real files, zero-callback negatives, A→B на первом app callback | Fixtures ещё не добавлены/не выполнены | изменить |
| CLI/runtime/trust/release identity не расширены | Fixed old argv/defaults/adapters и неизменённый D2 contract | CP-CODE должен подтвердить фактический diff | сохранить |
| Native/scientific acceptance доказана | Подтверждающих execution receipts нет | Все соответствующие counters 0 | данных недостаточно |
| Процедура была blind source-first | Реальный порядок чтения указан выше | Candidate прочитан до primary ops files | данных недостаточно |

**STOP. Передать coordinator для решения по design с указанным ограничением порядка review. Source edits, imports/tests/Nix/native/checkpoint этим report не активируются.**
