# SCI08-R1 — независимая source review engineering harness v1

**Вердикт: CHANGES_REQUIRED_SOURCE; STOP перед RED/GREEN.** Ниже два блокирующих дефекта в заявленном контроле свидетельств. Это review исходников, не grant на выполнение и не результат тестов.

Frozen candidate заново проверен:

| Артефакт | SHA256 |
| --- | --- |
| `local-unit-run-v1.py` | `e198d49c81ecded2ca4e5cecf0d2a40776ae56358a973e53d536ec24980c8930` |
| `engineering-plan-v1.json` | `0cb62f99bd8439bf5f6b33aaabdda1000d7b17520894b99d9c062e9005a0ec48` |
| `harness-report.md` | `37da39acdda0280179b5b8050cd617338ba317c3cdbee93a3f357edb1c14d86a` |
| `harness-identity.json` | `d4c7f0445ecb057fdf05bcd9f8010177c194efd1ea496fa6811242c43aa6fb6a` |
| RawCapture helper | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| TMP sampler helper | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |

Фактические identities: owning Runner `/tmp/qcl-sci08-r1-runner-worktree` HEAD `fefaa27f194bfddf85dd51a0e255beef2218c06d`, три modified и два untracked selected fixtures; `git diff HEAD -- src` пуст, `git diff --check` без ошибок, recursive submodules пусты. Bound Root HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`; bound Core HEAD `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Core status пуст. Рабочий cwd другого checkout имеет HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; его dirty status и восемь gitlinks сняты read-only, его environment не выбирается. Это наблюдение, не новый revision lock.

## Блокирующие замечания

**B1, P1 — неизмеренный RSS превращается в ноль и может пройти gate.** Локатор: harness `:75–90,173,179–180,211,225`. `peak=0; samples=0`; единственный RSS sample расположен внутри `while p.poll() is None`. Если child завершился до первого poll, цикл пропускается; последующая ветка `finally` измеряет только TMP. При complete raw capture и ожидаемых counts `good` допускает `peak==0, samples==0`, а receipt содержит `sampled_RSS_peak_bytes:0`. Дополнительно `rss_tree` возвращает 0, если процесс исчез между poll и чтением `/proc`, и считает отсутствие `VmRSS` как строковый `'0'`. Поэтому даже положительный `samples` не доказывает наблюдение RSS. Это воспроизводимый по control flow путь `not_measured → numeric0 → possible pass`, запрещённый требованиями evidence. Не утверждается, что pinned Julia фактически завершится настолько быстро.

Минимальное исправление: различать число попыток и число успешных RSS observations, отсутствие/исчезновение/отсутствующий `VmRSS` возвращать как unknown; хранить `null`/`not_measured` при отсутствии успешного sample и не выдавать bounded RSS PASS. Делать prelaunch TMP sample и final TMP sample с отдельными величинами/статусами; это не RSS измерение. Если требуется принимать быстрый child при отсутствии `/proc` observation, нужен отдельный принятый способ terminal measurement с честным названием quantity, а не присвоенный RSS0. Sampled maxima по-прежнему не доказывают transient peak или hard quota. На этом этапе исправление не выполнялось.

**B2, P2 — заявленный complete source/support snapshot не включает исполняемый include и входные файлы выбранного теста.** Локатор: harness `snapshot():55–61`; Runner `src/infrastructure/config/configuration_contract.jl:2,45–64`; selected `test/application/execution_resource_contract.jl:46–48`; `src/infrastructure/config/configuration_sources.jl:36–52`. В snapshot есть `src`, `ext`, `test/support`, пять fixtures и frozen docs, но нет:

- `tools/verify_schema_provenance.jl`, непосредственно исполняемого при import через `include(_package_path(...))`;
- `test/fixtures/configurations/exact_cpu.yaml`, действительно читаемого selected application fixture;
- `schema/PROVENANCE.json`, `schema/run.schema.json`, `schema/results-contract-set.json`, действительно читаемых loader/provenance path.

Наблюдённые SHA: tool `8bdb801a6e9b5419735c1248b3efc9a01900e2f6335c359693cf2e4dee7fcf09`; YAML `7d308b39c3ccb75f394993c5f21d36bf3527bf8fac42ab9e4af789a75186682c`. `HEAD`+`status` помогают заметить переход clean→dirty, но не связывают содержимое уже dirty файла: Root READY может содержать тот же status при иных bytes, и snapshot equality этого не различит. Internal schema provenance связывает payload с mutable PROVENANCE, а не с принятым frozen source. Current clean omitted paths не означают observed corruption; finding касается неполной promised binding.

Минимальное исправление: включить exact imported tool и перечисленные runtime inputs в content hash closure до READY и после child. Проверить остальные statically included/read inputs выбранного call graph и явно назвать границу closure. В том же исправлении включить frozen harness/plan bytes или отдельные saved-before hashes в terminal equality: сейчас source snapshot не содержит их, а receipt `:221` перечитывает текущие hashes без сравнения с reviewed before binding. Также отдельно проверять copied Project/Manifest и symlink destinations после child, если утверждается неизменность созданного environment, а не только исходников. Никакой OS-level TOCTOU lock это не создаёт.

## Что подтверждено исходниками

Exact Root `julia/Project.toml`/Manifest используют `../components/QCLNEGF.jl` и `../components/QCLNEGFRunner.jl`. Harness `:150–166` копирует их байты в `owned/environment/julia`, создаёт sibling links на bound Root Core и owning Runner overlay; `BOOTSTRAP:19–25` проверяет VERSION1.13.0 и фактические realpath `Base.pkgdir/pathof` обоих modules до fixtures. Выбор overlay логически корректен. Это не observed import. Root main Runner/test Project не подставлены.

RED selection — только отдельный existing forecast API с healthy literal16777728 и Bool-negative assertion; `QCL_COUNTS` ожидает ровно1pass/1fail/0errors/0broken и один nested set, exit1. GREEN — пять frozen fixture files,349/0/0/0 и33 nested sets, плюс completion marker и exit0. Import error не может удовлетворить predicate.349 assertions/31 logical groups сохранены как nominal source contract fixture v2/high review; они не были исполнены. GREEN дополнительно требует observed exact RED, medium I, independent CPP, actual O1/O2 traces и final fixture count от Root. Production остаётся baseline; будущий I/fake boot chain ещё отдельный gate.

Root READY связывает phase/id, свежесть≤300s, exact plan/harness, источник, call ordinal и milestone81→87 с двумя reserved calls. Fixed exclusive phase directory исключает повтор в том же сохранённом namespace. Harness не пишет CP/shared counters и не вызывает C08; exhausted8/8 не используются. Сам по себе непустой `operation_identity` не является authenticated issuer или permanent filesystem lock; это доверенный Root protocol. Ничего не удаляется автоматически. Root обязан сохранять оба attempt folders и original receipts; удаление folder для повторного вызова противоречило бы принятому no-rerun contract.

Helper hash и compile/exec используют один и тот же bytes buffer с non-main namespace; helper entrypoint не вызывается, path loader/pyc для helper не используется. RawCapture стартует сразу после Popen, нормальные success/failure paths проходят owned-process-group termination, drain и post-source/TMP checks; fallback сохраняет bytes при неудачном создании capture thread. После reservation setup error сохраняет diagnostic и consumed-attempt receipt. Не выдается абсолютная гарантия для внешнего убийства самого guardian/ошибки файловой системы: tail read/hash/receipt write сами могут завершиться исключением, а incomplete non-daemon reader после `finish(5)==False` не имеет доказанного terminal wall bound. Для trusted selected path нет найденного spawn/escape call; это ограничение аварийного supervisor behavior, не основание объявить native isolation PASS.

Один CPU affinity, BLAS/Julia threads1, CPU soft/hard570/575s, wall stop580s и verdict≤600s прописаны. RSS2GiB/TMP16MiB/output1MiB — sampled/observed verdict limits, не hard resident/disk enforcement. RawCapture способен превысить stop threshold между polls; превышение final1MiB даёт STOP и требует сохранить полный original raw. TMP sampler считает logical bytes regular files, не physical allocation; symlinks не traversed. Начальные/final quantities должны сохранять свои настоящие semantics.

## Оценка environment-only ограничения

Для этих exact trusted selected fixtures и просмотренного import path допустимо рассматривать controlled HOME/XDG/TMP/first depot, existing-only Julia caches и offline package flags как **явно признанное bounded engineering предположение**. Selected fixtures используют manufactured scalars/fake roots; actual solver/HTTP sender не вызываются. Runner `__init__` только назначает schema path; imported verifier определяет функции, не запускает CLI. Core precompile workload помечен как precompile-only, а создание новых caches выключено existing-only flags; фактический runtime behavior не наблюдался.

Это не OS read-only/network enforcement: prepared secondary depot и source writable для того же пользователя, direct package writes/syscalls физически не запрещены, native libraries/dependency caches не прошли новую isolation приёмку. Root должен принять указанную engineering границу до READY; если требуется предотвращение всех внешних writes/network, v1 не подходит. Само это честно указанное ограничение не требует нового setup в рамках данного source review и не является дополнительным blocker поверх B1/B2. Вывод относится к frozen call graph; будущий accepted production I нужно проверить заново.

## Проверки и стоимость

Выполнены только чтение текста, hash/Git metadata, selected source paths и diff checks. Target Julia/parser/import/tests/native/network/install calls0; harness/helper import/compile/selftest0. Не запускались candidate Python, Julia, `Pkg`, downloader или Test. Созданы только этот report и review identity; production/test/CP/Git edits0. Conservative logical read charge с metadata reserve менее1MiB из лимита3MiB; physical I/O/CPU/RSS не измерялись. Review укладывается в15min/1CPU/1GiB/report128KiB как source-only scope, без заявления measured resource peaks. Runtime fit2GiB и научная приёмка не установлены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Manifest выбирает Runner overlay и bound Core | copied relative paths, sibling links, pkgdir/pathof assertions | Import не выполнялся | сохранить |
| RSS unknown не проходит как0 | counter/initialization/loop/good predicate B1 | Быстрый exit или disappearing proc не различены | изменить |
| Все используемые source/input bytes frozen | snapshot closure B2 + actual tool/YAML/schema reads | Omitted executable/data bytes не hashed | изменить |
| Два bounded calls и no-rerun protocol | fixed ids/folders, fresh Root READY, no counter mutation | Root owns authorization/retention; нет нового grant | сохранить |
| Engineering environment/offline acknowledgement достаточен для выбранного trusted scope | controlled env/existing flags + static fake-only selection | Нет hard filesystem/network isolation | сохранить |
| Native/S1/scientific acceptance установлена | Target calls0 | Нет runtime/scientific evidence | данных недостаточно |

**STOP. Сначала исправить B1/B2 и повторно независимо проверить новый immutable harness/plan. Этот source verdict не разрешает RED/GREEN, новые C08 calls, setup, native или science runtime.**
