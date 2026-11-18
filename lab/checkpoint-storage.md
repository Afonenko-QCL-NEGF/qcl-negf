# Хранилище для продолжения расчёта

Первый вариант — существующий submit-узел HTCondor и его постоянный диск
`/srv/qcl`. Перед внедрением нужно проверить фактический путь `SPOOL`,
доступное место и права пользователя очереди. Отдельная VM для хранилища
на этом этапе не требуется. Потеря самого диска submit-узла остаётся за
границами такого восстановления.

В предполагаемой схеме worker пишет активное численное состояние в локальный
scratch. После согласованной записи Runner должен закрыть checkpoint, а
HTCondor — передать указанный комплект в spool. Для повторного запуска нужны исходный frozen
plan, указатели на зафиксированное поколение, проверяемый результат и файлы
этого checkpoint с необходимой историей. Worker должен получить комплект обратно
через штатную передачу файлов под совместимую среду Julia/Pkg. До подтверждения
передачи должен оставаться читаемым предыдущий восстановимый комплект.
Ёмкость выбирается по фактическому объёму checkpoint, его временной записи
и числу одновременно восстанавливаемых заданий.
[Штатный self-checkpointing HTCondor](https://htcondor.readthedocs.io/en/v26_0-branch/users-manual/self-checkpointing-applications.html).

## Предварительная проверка и опыт восстановления

Ниже — процедура контролируемой проверки; её результаты и оставшиеся ограничения приведены далее.
На доступном manager с текущими разрешёнными credentials для чтения конфигурации
сначала запросить работающий schedd и проверить файловую систему, не меняя их.
Локальные defaults TOOL не являются свидетельством конфигурации schedd:

```sh
qcl_spool_path="$(condor_config_val -schedd SPOOL)" || { printf 'Ошибка запроса SPOOL\n' >&2; exit 1; }
test -n "$qcl_spool_path" || { printf 'SPOOL не получен\n' >&2; exit 1; }
findmnt -T "$qcl_spool_path"
stat -c '%U:%G %a %n' "$qcl_spool_path"
df -h "$qcl_spool_path"
df -i "$qcl_spool_path"
```

Проверить фактический mount, владельца и доступ service account, свободные
байты и inode с запасом на два поколения, временную запись и все одновременно
восстанавливаемые задания. На обоих Linux workers под пользователем слота
прочитать `command -v julia`, `julia --version`, `JULIA_DEPOT_PATH`,
`julia --project=ПУТЬ -e 'using Pkg; Pkg.status(); println(DEPOT_PATH)'` и
`sha256sum ПУТЬ/Manifest.toml`; сверить фактические Core/Runner sources,
Manifest и доступность зависимостей в соответствующих depot. Совместимость
среды и доступность checkpoint не выводятся из одинакового имени версии Julia.
При недоступности узла или неполном комплекте переходить к опыту нельзя.

Для контролируемого опыта на собственном задании предусмотреть явный список
`transfer_checkpoint_files` с полным замкнутым комплектом и обычный
`when_to_transfer_output = ON_EXIT` для конечного результата. Обёртка может
вернуть настроенный HTCondor checkpoint exit code `85` только после здорового
состояния Runner `paused` и проверки полной закрытой генерации с её зависимостями
и хешами. Перед resume обёртка должна проверить paused/committed pointer, ожидаемый
путь и хеш поколения. Повреждённую копию или статус failed/invalid нужно
классифицировать как terminal failure без кода `85` и без повтора. Первый
resume повреждённой копии может записать failed в result JSON при CLI exit 0;
после него повторный общий вызов может уже не иметь `full_state`. Поэтому
нужно проверять структурированный результат, а не считать обычный exit 0
научной приёмкой. В проверенной обёртке после локальной проверки закрытой
генерации удаляется одноразовый `control/pause.json`, затем создаётся tar и
возвращается код 85. При повторном запуске на том же worker обёртка ожидает
управляемого выселения и не входит повторно в Runner. Manager отдельно читает
копию из spool и проверяет её хеш перед точечным vacate собственного задания.
На выбранном втором worker обёртка отклоняет восстановленный архив с оставшимся
`control/pause.json` и проверяет комплект до resume (`checkpoint-worker-v3.sh`).
Проверять ту же постановку, бюджет итераций и непрерывность истории; до
подтверждения сохранять прежний пригодный комплект.

После восстановления доступа native preflight HTCondor 26.0.1 сообщил
`SPOOL=/srv/qcl/condor/spool` и два свободных Linux worker; private receipt
`linux-native/preflight-live.log` в `.build/issue135-followup-2026-11-18/`.
Это не проверка checkpoint transfer или восстановления. При запуске manager
опубликовал loopback-адрес; после проверки пустой очереди всех пользователей,
стабильной LAN и смонтированного SPOOL перезапущен только его `condor.service`.
Конфигурацию и сеть не меняли (`service-rebind-receipt.log`).

Native задание `25.0` на первом Linux worker вернуло checkpoint exit code 85;
HTCondor показал `NumCkpts=1`. Закрытый tar размером 2 447 360 байт был
прочитан из spool: его SHA-256 совпал с копией из вывода задания
(`1403b653d28c6bd4487160b7f8b480efd3c33ba05321e09546404de31764a3ef`).
Проверка комплекта подтвердила `paused`, attempt 1, последнюю внутреннюю
итерацию 1 и хеши артефактов (`closed-checkpoint-25.0.log`). После повторной
регистрации второго Linux worker свежая проба передачи `26.0` завершилась с
exit 0 и показала Julia 1.13.4 (`handoff-worker-guard.log`); это не доказывает
совместимость полного окружения или восстановление checkpoint. Владелец изменил
требование только задания `25.0` на второй worker и выполнил его fast vacate
после повторной проверки spool (`handoff-vacate-25.0.log`). Затем `25.0` был назначен на второй worker и начал работу в новом scratch;
прочитан восстановленный указатель attempt 1 со статусом `paused`
(`resume-live-25.0.log`). На втором worker подтвердились хеш tar и проверка
commit. Совпали версия Julia, SHA-256 Manifest и заявленные ревизии Core и Runner.
Attempt 2 начал инициализацию из checkpoint, но
завершился `failed` с `POINT_FAILED: ArgumentError: restart scattering operators
differ (Khat, qK, or F_LO)` без fallback и нового commit; обёртка завершилась
кодом 42 без повтора (`NumJobStarts=2`, `resume-terminal-25.0.log`). Численное
продолжение не произошло; непрерывность истории через итерацию 2 не измерена.
Диагностика только метаданных в заданиях `29.0/29.1` показала: исходная
Ubuntu при настройках по умолчанию воспроизводит сохранённую identity, а
второй worker отличается во всех каналах операторов. Фиксированные `generic`
и `Nehalem` на двух установленных сборках Julia также не устранили различия;
хеши бинарных файлов различались при одинаковой версии Julia
(`kernel-probe-poll.log`). Это не устанавливает причину. Setup-only задания `31.0/31.1` с одним архивом Julia, совпадающими
хешами пяти бинарных файлов, Manifest, Core, Runner и frozen plan, одним
потоком, `-C generic` и фактическим Nehalem OpenBLAS дали идентичную полную
identity операторов на обоих workers (`shared-kernel-result.log`). Она
отличается от identity старого checkpoint `25.0`, поэтому не подтверждает
его совместимость. Новое задание `32.0` с этой средой запущено отдельно;
его закрытый checkpoint прочитан и проверен в spool: tar 2 498 560 байт,
SCBA 1, пять хешей и профиль операторов (`shared-runtime-spool-readback.log`).
После проверки владелец изменил только требование worker задания `32.0` и
выполнил fast vacate (`shared-runtime-queue-only-handoff.log`). Задание было назначено второму worker в новом scratch; attempt 2 продолжил
расчёт из checkpoint и достиг SCBA 2/2. То же задание завершилось с exit 0,
двумя стартами и статусами series `completed_with_warnings`, point `completed`
при отсутствии сходимости (`shared-runtime-resume-live.log`,
`shared-runtime-terminal.log`). Независимая проверка подтвердила хеши артефактов, цепочку commit к spool,
неизменный бюджет SCBA 2 и инициализацию из checkpoint без fallback. Координаты
истории продолжились с [1] до [1, 2], первая строка совпала побитно во всех
19 столбцах `/scba/*` (`shared-runtime-terminal.log`). Этот результат не является
научной приёмкой. Сценарий
использовал управляемый vacate, а не фактическую потерю хоста. На втором
worker действовал лимит памяти 5 GiB на уровне cgroup, по одному потоку
Julia и BLAS, без жёсткой CPU quota (`shared-runtime-dell-cgroup.log`). Для
воспроизведения именно этого контролируемого опыта в приватном `linux-native`
сохранены `shared-runtime-checkpoint-worker.sh`, `qualified-checkpoint-tools.py`
и `shared-runtime-checkpoint.submit`; профиль — общий архив Julia 1.13.4,
`-C generic`, Nehalem OpenBLAS и один поток Julia/BLAS.
Указанные журналы находятся в приватном каталоге
`linux-native` выше; это не опубликованные артефакты.

Отдельный native negative control `28.0` использовал обёртку
`checkpoint-worker-v3.sh` из опыта `25.0` и синтетический текстовый marker с неверным digest: передача входа и выхода
завершилась, проверка отклонила marker, задание завершилось кодом 42 после
одного старта, `NumCkpts=0`, без повтора. Julia и solver не запускались;
это не native проверка повреждённого HDF5
(`linux-native/synthetic-terminal-and-native-kernel-meta.log`).

Локальные fixture-тесты Runner прошли 90/90, локальный CLI достиг паузы на
SCBA 1/2. Повреждённая копия при публичном CLI resume дала series/point
`failed/failed`, initialization `checkpoint` и `POINT_FAILED` с причиной
`artifact byte count differs`, без fallback в solver. Отдельное повреждение
без изменения размера также дало `failed/failed`, initialization `checkpoint`
и `POINT_FAILED / ArgumentError: artifact digest differs`. Полный локальный tar восстановлен в новые каталоги: чистый CLI resume с тем же frozen plan
продолжил attempt 1 `paused` с SCBA 1 в attempt 2 `completed_with_warnings /
completed` (unconverged), initialization `checkpoint`, с историей SCBA [1, 2]. Префикс
совпал по 19 HDF5 массивам, пять хешей проверены по commit. Оба CLI вызова
вернули exit 0. Это не доказательство работы spool или научной приёмки. Private receipts находятся в
`.build/issue135-followup-2026-11-18/linux/`: `local-runner-fixtures-retry.log`,
`local-cli-pause.json`, `local-cli-live.jsonl`, `local-cli-resume-live.jsonl`,
`local-cli-checkpoint-sha256.log`, `local-cli-verification.log`,
`local-cli-exits.log`;
проверки недоступности manager до восстановления доступа — `preflight-live.log`, `preflight-numeric.log`,
`preflight-owned-management.log`, `private-route-summary.log`. Это локаторы
в приватном рабочем каталоге, а не публичные артефакты.

Та же схема предлагается для Windows worker без общего mount и без общих путей
кэша Julia. В этой схеме Windows должна использовать собственный локальный scratch и depot.
Сначала нужно подтвердить штатную передачу файлов и Julia под реальной
учётной записью слота. Перенос численного checkpoint Linux ↔ Windows
требует отдельной проверки правильности продолжения.
[Передача файлов HTCondor](https://htcondor.readthedocs.io/en/v26_0-branch/users-manual/file-transfer.html).

Runner записывает `progress/progress.yaml` с последним событием: путь и имя
этапа, номер итерации, прошедшее время и метрики этого события с единицами.
Набор метрик зависит от события: завершение этапа может заменить снимок
итерации, поэтому наличие последних невязок в любом снимке не гарантировано.
В закреплённом Runner снимок не содержит настенного времени; `elapsed_seconds`
сам по себе не определяет возраст данных. Для возраста нужна отдельно проверенная
метка времени наблюдения. См. [источник Runner](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/48f31e95d550f0aaeaece6cddf1267810ea4715c/src/infrastructure/telemetry/progress.jl).
Другой кандидат для наблюдения — `RESULT/current_point.json`: Runner записывает
`updated_unix`, этап, итерацию и метрики. Для события без метрик той же точки и
attempt он сохраняет прежние метрики, а следующее непустое событие заменяет их;
phase begin/end не заменяют проекцию. Поэтому timestamp относится к записи
указателя, а не обязательно ко времени измерения метрики и не является heartbeat.
Этап и сохранённые метрики могут относиться к разным событиям. См.
[источник указателя Runner](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/48f31e95d550f0aaeaece6cddf1267810ea4715c/src/composition/scientific_execution.jl#L279-L316).
Локально во время работающего CLI после resume наблюдались `stage=scba`,
`iteration=2/2`, безразмерные `r_K` и `r_Σ` и `updated_unix`
(`local-cli-resume-live.jsonl`). Последующее событие заменило эти метрики.

В возвращённом результате `20.0` указатель содержал `stage=poisson`,
`iteration=0` и только метрику `J`; конечный `progress.yaml` содержал
`stage=point`, `event=end` и пустые метрики. Локатор: результат задания в
[отчёте](../docs/implementation/stationary-checkpoint-2026-11-18.md),
`result/current_point.json`, SHA-256
`b84f9423906421e4d630558cd9e9fc913f3e30586006911e282b6952d221b827`;
`result/executions/execution-1/point-1/attempt-1/progress/progress.yaml`,
SHA-256 `894b8252fad99030dd2782340c6c10e3f99c8739a864c1cc9fd35e9f4641d11d`.

Возможный штатный путь чтения во время задания —
[`condor_tail`](https://htcondor.readthedocs.io/en/26.0/man-pages/condor_tail.html)
для конкретного файла, явно перечисленного в `transfer_output_files`. В задании
`25.0` он прочитал снимок с этапом SCBA, итерацией и timestamp во время работы
на первом worker (`native-v3-progress-tail.log`); метрик невязки в этом снимке
не было. В отдельном задании `30.0` обычный владелец очереди прочитал через
`condor_tail` при `JobStatus=2` снимок SCBA 1/2 с `updated_unix` и
безразмерными `r_D`, `r_K`, `r_Σ`, `r_λ`. Файл верхнего уровня
`progress-scba.json` формировался из `current_point.json` при наличии метрик
и был явно перечислен в output (`stationary-progress-live.log`). После
восстановления `32.0` тот же оператор прочитал снимок SCBA 2/2, attempt 2,
с невязками и временем (`shared-runtime-resume-live.log`). Метрики зависят
от события, а по одному снимку нельзя установить непрерывную работу.

Проверка `20.0` охватывала возврат результата через `ON_EXIT`. Чтение
живого снимка в `30.0` и `32.0` использовало `condor_tail` во время
работы задания.

Подтверждён обычный возврат файлов через HTCondor. Передача закрытого checkpoint в spool и его readback подтверждены для `25.0`;
первый профиль дал контролируемый отказ, а новый общий профиль позволил
заданию `32.0` продолжиться на другом узле с проверенным префиксом истории. [Отчёт сквозной проверки](../docs/implementation/stationary-checkpoint-2026-11-18.md).
