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

Следующее — процедура для будущей native-проверки, не подтверждённая реализация.
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
научной приёмкой. После self-checkpoint с кодом 85 HTCondor сразу повторно запускает тот же
executable в прежнем sandbox. Будущий опыт требует gate в обёртке до этого
повторного входа в Runner: проверить завершённый transfer, замкнутость и хеши
копии в spool. Только после проверки удалить одноразовый `control/pause.json`,
чтобы корректное продолжение не запросило паузу повторно. Затем владелец
контролируемо выполняет vacate/rematch только собственного задания и только на
точно выбранный второй Linux worker с чистым sandbox. Этот gate и native
сценарий пока не реализованы и не проверены. Проверить ту же постановку, бюджет итераций и
непрерывность истории; до подтверждения сохранить прежний пригодный комплект.
Пока native transfer, spool readback и межузловое восстановление не измерены.

Локальные fixture-тесты Runner прошли 90/90, локальный CLI достиг паузы на
SCBA 1/2. Повреждённая копия при публичном CLI resume дала series/point
`failed/failed`, initialization `checkpoint` и `POINT_FAILED` с причиной
`artifact byte count differs`, без fallback в solver; это отдельное свидетельство
от fixture-проверки digest. Полный локальный tar восстановлен в новые каталоги: чистый CLI resume с тем же frozen plan
продолжил attempt 1 `paused` с SCBA 1 в attempt 2 `completed_with_warnings /
completed` (unconverged), initialization `checkpoint`, с историей SCBA [1, 2]. Префикс
совпал по 19 HDF5 массивам, пять хешей проверены по commit. Оба CLI вызова
вернули exit 0. Это не доказательство работы spool или научной приёмки. Private receipts находятся в
`.build/issue135-followup-2026-11-18/linux/`: `local-runner-fixtures-retry.log`,
`local-cli-pause.json`, `local-cli-live.jsonl`, `local-cli-resume-live.jsonl`,
`local-cli-checkpoint-sha256.log`, `local-cli-verification.log`,
`local-cli-exits.log`;
проверки недоступного manager — `preflight-live.log`, `preflight-numeric.log`,
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
(`local-cli-resume-live.jsonl`). Последующее событие заменило эти метрики. Доступность
актуальных невязок через HTCondor во время задания не проверена.

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
для конкретного файла, явно перечисленного в `transfer_output_files`. Его работа
с вложенным путём одновременно с передачей каталога и фактическая доступность
`current_point.json` в пуле ещё не проверены.

В проверенном задании HTCondor `20.0` результат возвращался при `ON_EXIT`;
доступность снимка вне worker во время исполнения не измерена. Свежая проверка
manager не состоялась: mDNS не разрешился, а прежний SSH-маршрут ответил
`No route to host`. Признак живого процесса также не проверен; один снимок
не доказывает liveness.

Подтверждён обычный возврат файлов через HTCondor. Сценарий сохранения
checkpoint в spool, потери worker и продолжения на другом узле остаётся
открытым. [Отчёт сквозной проверки](../docs/implementation/stationary-checkpoint-2026-11-18.md).
