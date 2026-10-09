# Переход к полному storage budget AC2

На 2026-10-03 полный AC2 ещё не подтверждён. Recovery, staging и export имеют проверки логических
байтов, но произвольные scratch writes, stdout/stderr и AiiDA retrieval пока не ограничены общей
штатной filesystem quota. Лимиты Slurm CPU/RAM не служат ограничением диска.

Документ фиксирует инженерный аудит и предлагаемое разделение хранения. Он не является конфигурацией
установленной quota и не меняет научный план, модель, сетку, каналы рассеяния или критерии приёмки.

## Фактические владельцы записи

| Область               | Owning locator                                                                                               | Состояние                                                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Worker scratch        | `qcl-negf-platform/modules/cluster.nix`, `execute_scientific_plan_staged` Runner                             | Отдельный ext4 `/scratch`, пока только `noatime`; промежуточные writes без OS quota                                                                                    |
| Recovery/staging      | `QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl`, `src/composition/scratch_execution.jl` | Logical guards учитывают publication metadata и source/pending copy; transient allocation и другие writers требуют filesystem enforcement                              |
| NFS jobs/logs         | `qcl-negf-platform/modules/storage.nix`, `aiida_qcl_negf/calculation.py`                                     | UID/GID3000, NFSv4 `root_squash`; jobs, logs, recovery и archive сейчас сосуществуют                                                                                   |
| AiiDA retrieval       | AiiDA2.9.2 `engine.daemon.execmanager.retrieve_calculation`                                                  | Весь `retrieve_list` сначала копируется в `SandboxFolder(storage.sandbox)`, затем в permanent repository; post-retrieval guard не ограничивает первую копию            |
| Export spool          | `qcl_negf_api/exports.py`, `qcl_negf_results/export.py`                                                      | Remaining reservation передаётся exporter; учитываются retrieved source, temporary spool, receipt и retained output; default temporary filesystem отдельно не объявлен |
| Persistent provenance | `qcl-negf-platform/modules/persistent-state.nix`, `ops/bootstrap.ts`                                         | PostgreSQL, AiiDA profile/repository и backups — постоянные данные, а не disposable temp                                                                               |

Storage/application modules проверены на Platform `d0097db`; переход к `066c6b1` меняет только
bounded чтение public key. Runner guards проверены на `a942727`, portal на `779c557`, AiiDA
retrieval contract на `241c812`. Это локаторы аудита, не альтернативный release lock: состав
опубликованного проекта продолжает задаваться Gitlinks.

## Предлагаемое штатное ограничение

Минимальный fail-closed вариант — конечные hard block/inode quotas UID3000 на отдельных operational
ext4 filesystems. Scientific finals и permanent repository получают отдельную вместимость; они не
удаляются для освобождения operational budget. Общая quota нынешнего NFS job tree ограничила бы
также finals и потому не закрывает требование разделения.

1. Worker operational filesystem содержит scratch и job temporary files; `TMPDIR` выбирает явно
   принадлежащий ему каталог.
2. Storage operational filesystem/export содержит jobs, recovery, staging и stdout/stderr.
   Scientific archive хранится на отдельном persistent filesystem/export. Runner/AiiDA должны явно
   маршрутизировать эти destinations, сохраняя portable manifests, commit identity и archive
   ownership.
3. Controller operational filesystem содержит AiiDA sandbox и portal/results temporary/export trees.
   Оба сервиса получают `TMPDIR`; bootstrap reconciles штатный AiiDA `storage.sandbox`. Profile, DB
   и permanent repository остаются на persistent state filesystem.
4. Owning platform объявляет положительные budgets в bytes и inodes, reserve и stable device
   identities. Обязательная oneshot unit применяет стандартные `quotaon`/`setquota`, сверяет
   effective limits через `repquota` и предшествует зависимым NFS/Slurm/application services. Отказ
   настройки блокирует их старт.

Kernel quotas считают выделенные blocks/inodes, а logical guards — длины файлов. Обе проверки нужны.
`setquota` принимает KiB; округление должно давать предел не выше выбранного byte budget. Budgets
меньше 1KiB и округлённый hard limit0 отвергаются: значение0 выключает quota. Inode hard limit также
должен быть положительным. Сумма finite pools ограничивает общий operational storage; она не
является транзакционной per-attempt reservation. NFS quota применяется на server, включая
одновременные записи разных clients с UID3000. `root_squash` сохраняется.

Project quotas могут сократить число disks для trusted writers, но требуют проверки ext4 features,
inheritance, существующих inodes, rename/hardlink и изменения project IDs. `NoNewPrivileges` само по
себе не защищает project IDs. Это дополнительный вариант, а не установленный default enforcement.

Новый blank operational volume можно явно форматировать с quota features. Existing persistent ext4
не преобразуется автоматически: включение необходимых on-disk features относится к отдельной offline
maintenance операции с сохранением данных. Mount option не доказывает наличие features.

Первичные основания:
[kernel quota subsystem](https://www.kernel.org/doc/html/latest/filesystems/quota.html),
[setquota](https://www.man7.org/linux/man-pages/man8/setquota.8.html),
[ext4](https://www.man7.org/linux/man-pages/man5/ext4.5.html),
[NFS exports](https://www.man7.org/linux/man-pages/man5/exports.5.html),
[tune2fs](https://www.man7.org/linux/man-pages/man8/tune2fs.8.html).

## Обязательные проверки перехода

До full AC2 нужно подтвердить actual effective quotas после reconciliation и reboot, отсутствие
форматирования/удаления existing данных, а также refusal нового launch при исчерпанном budget.
`EDQUOT`/`ENOSPC` должны давать различимую причину storage exhaustion и конечное прекращение retry
до восстановления вместимости. Предыдущий valid checkpoint и finals остаются читаемыми.

Первый ограниченный kernel probe использует только новый временный filesystem в owned lab VM:
budget600s, CPU1/RAM1GiB, image64MiB, dense writes суммарно не более96MiB, logs2MiB. Проверяются
block limit8MiB, inode refusal, чтение прежнего малого checkpoint и точная очистка собственного
mount/loop/image. Sparse `truncate` не доказывает block quota. Этот probe отдельно не подтверждает
Runner publication, NFS concurrency, Slurm stdout или AiiDA retrieval.

Первая попытка остановлена `not_measured` до запуска quota-tools: импорт пакета quota из
официального cache прошёл, но recursive signature verification отказала на 17 зависимостях, уже
зарегистрированных bootstrap image без подписей. Host closure metadata содержала официальные подписи
всех 18 paths; это не заменяет guest verification. Image, loop и mount не создавались, trust
configuration не менялась. `EDQUOT` и inode exhaustion пока не измерены.

Следующие integration proofs требуют выбранного path split: concurrent NFS dense writers; real Slurm
stdout writer; recovery failure до ack при сохранном previous; заполнение AiiDA sandbox и export
spool; восстановление admission без удаления finals или cold restart. Journald retention/rate limits
не равны строгому byte ceiling активного журнала; `LimitFSIZE` ограничивает отдельный файл и не
заменяет aggregate quota.

| Утверждение                                          | Свидетельство                                                                                                                    | Ограничение                                                                | Решение                |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------- |
| Logical recovery/staging/export guards исправлены    | Runner package64/64 до последнего pre-hash guard; isolated production staging28/28 после него; portal42/42 и независимые reviews | Нет OS quota и NFS durability proof                                        | сохранить              |
| Полный AC2 выполнен                                  | Доказательств недостаточно                                                                                                       | Scratch/logs/retrieval filesystem enforcement и path split ещё отсутствуют | изменить               |
| Штатные quotas подходят для finite operational pools | Kernel/quota-tools contract, единый UID3000                                                                                      | Actual full-stack fault tests ещё требуются                                | дополнительно измерить |
| Финалы сохраняются при нехватке operational места    | Требования118/254 запрещают удалять finals ради operational budget                                                               | Final archive capacity проверяется отдельно                                | сохранить              |
