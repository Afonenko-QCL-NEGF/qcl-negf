# Windows worker: подготовка, не готовая интеграция

Каркас рассчитан на принадлежащую QCL Windows-машину; при наличии системной команды condor_version.exe установленный HTCondor используется без MSI и проверки конкретной версии. До применения: настроить WinRM/PSRP по TLS с доверенным сертификатом и отдельным private inventory администратора, установить ansible.windows/community.windows и Python transport на controller, подтвердить владение QCL VM, резерв CPU/RAM и адрес менеджера, подготовить private daemon IDTOKEN condor@qcl, выданный менеджером и разрешённый его конфигурацией. Для взаимной проверки IDTOKENS нужен native pool signing key; play передаёт его отдельно с SYSTEM/Administrators ACL и no_log. Это доверие полноценного узла пулу, а не простая проверка публичным ключом. При повторном запуске принадлежащие QCL каталоги credentials проверяются по владельцу и ACL; неизвестный владелец или reparse point блокирует изменение конкретного пути. Проверить срок token, фактическую NTFS ACL, другие действующие firewall rules, схему имён и локальные каталоги. MSI может автоматически запускать службу — MSI использует RUNJOBS=A и подготовленную заранее локальную конфигурацию; на реальной машине подтвердить, что LOCALCONFIG действительно загружен и закрытые сетевые настройки применены при первом старте.

MSI URL указывает на подвижный официальный канал 26.0: https://htcss-downloads.chtc.wisc.edu/tarball/26.0/current/condor-Windows-x64.msi ; URL можно заменить переменной, no exact version/hash gate. Процедура MSI: https://htcondor.readthedocs.io/en/lts/platform-specific/windows-installer.html ; служба Condor работает под LocalSystem. Windows NOBODY_SLOT_USER игнорирует: по умолчанию Starter создаёт временных пользователей слотов, отдельный qcl Windows user здесь только для ручного использования и не является job identity. https://htcondor.readthedocs.io/en/main/admin-manual/configuration/global.html

Следующий Windows runtime опыт: подтвердить реальные LOCAL_CONFIG_FILE/LOCAL_CONFIG_DIR и итоговые START, token ACL, доступ входящих портов, взаимную IDTOKEN auth с manager, связь worker и оба направления сети; проверить совместимость версий, Windows file transfer и требования OpSys/Arch, Julia/depot/ACL для временных slot users, сохранение и чтение результатов; CPU/RAM/job memory enforcement замерить, без предположения cgroup Linux. Не перезапускать действующий сервис с активными заданиями; проверить применение конфигурации и выполнить инженерный payload в подходящем окне. Установка, запуск процесса и доступность очереди не являются научной приёмкой.

Julia в Windows: сначала найти и использовать рабочую системную `julia` с обычным `julia --version`; при отсутствии рассмотреть официальный Juliaup через WinGet, если WinGet установлен и доступен, либо официальный установщик. Не фиксировать искусственно конкретную версию. Juliaup может ставиться в профиль конкретного пользователя, поэтому для временных slot accounts нужно проверить фактический доступ и разрешение пути. Общий заранее подготовленный depot допустимо рассматривать как read-only нижний слой, а первый depot конкретного задания — как отдельный writable слой для пакетов/компиляции; фактические пути, ACL, повторное использование и I/O проверить на Windows. Общая директория `C:\QCL\depot` в каркасе не доказывает ни эти права, ни совместимость бинарных кешей.

Повторный запуск: существующий QCL token сохраняется без автоматической замены; обновление credentials — отдельная штатная операция. ACL системного каталога и token приводится к SYSTEM/Administrators только после проверки владельца каталога; при неизвестном владельце или reparse point остановиться. Установленная служба ищется по PATH и реестру. До изменения конфигурации running startd опрашивается напрямую, при claimed/busy/неизвестном состоянии остановка; Непосредственно перед изменённым restart выполняется native `condor_drain -check`, который должен отклонить обслуживание при новом claim. Для существующей установки основной CONDOR_CONFIG из реестра дополняется `include :` (штатный синтаксис), что требует проверки после будущих обновлений MSI и при override через environment. После parser check изменение config/token/include вызывает native drain и restart службы: изменение `DAEMON_LIST` требует restart, одного reconfig недостаточно. Существующие роли SCHEDD/COLLECTOR/NEGOTIATOR не превращаются в execute worker. Применение этого playbook на Windows остаётся непроверенным.

Наблюдение на 17 ноября 2026: alias current/current отдавал 25.15.15, а 26.0/current — 26.0.1. Последний путь задаёт канал, не фиксирует patch. Системная установка имеет приоритет без version gate.

В конфигурацию добавлены POOL signing key, daemon token и локальная NTSSPI-авторизация администратора. Идентичность NTSSPI и работу обоих направлений IDTOKENS нужно подтвердить на Windows runtime; до этого не считать узел интегрированным.

Для нового clone нужен WinRM HTTPS сертификат с именем конкретной VM и проверяемая цепочка доверия в private inventory; сертификат старого hostname из шаблона не подтверждает TLS нового узла. Отдельный `ansible/windows-julia.yml` сначала ищет системную Julia и Julia обычного пользователя, затем официальный Juliaup WinGet или MSI; Pkg запускается обычным пользователем только при заданном проекте. Доступ временных slot users к runtime/depot и безопасность разделяемого read-only кеша остаются непроверенными.

## Попытка на Windows 18 ноября 2026

На отдельном QCOW2-слое Windows 10 x64 официальный MSI HTCondor 26.0.1 завершился
с кодом 0. SHA256 файла, полученного по HTTPS, совпал с SHA256 файла
в гостевой системе, где `Get-AuthenticodeSignature` вернул `NotSigned`.
SCM показал службу `Condor` в состоянии `Running` под `LocalSystem`.
В списке процессов были `condor_master`, `condor_procd` и `condor_shared_port`;
`condor_startd` отсутствовал. Проба в изолированной VM завершилась ошибкой
связи с локальным collector. Установщик и служба проверены на этом образе,
применение playbook и интеграция с QCL pool остаются непроверенными.

При повторной проверке с ноутбука имя менеджера из private inventory
не разрешалось. Последний известный IPv4 вернул `No route to host` на SSH/22
и TCP/9618. В inventory есть локальная ссылка на POOL signing key. Наличие
файла не устанавливает соответствие работающему пулу или пригодность daemon
IDTOKEN, а действующего Windows host entry в этом inventory нет. Подключение
worker, взаимная аутентификация и Windows job не проверены. Снимок Windows
остановлен, исходный диск использовался как read-only backing file. Закрытые
журналы сохранены в `.build/issue135-followup-2026-11-18/windows/`
(`guest-install-attempt2.log`, `pool-diagnose.log`, `single-vm-smoke.err`,
`manager-endpoints.private.log`, `overlay-custody.log`).

## Подготовка Windows-клона и проба через общую очередь

1. Создать выделенный QCL clone с уникальным именем и адресом. Подтвердить
   владение, запас ресурсов, сетевую достижимость Windows ↔ manager/schedd
   и доверенный WinRM HTTPS для нового имени. В закрытом inventory заполнить
   `windows_workers` по [примеру](ansible/inventory.example.yml), указать свежие
   `qcl_manager_address`, `qcl_manager_ip` и источники `qcl_pool_key_file` /
   `qcl_windows_daemon_token_file` из действующего пула. Подтвердить разрешение
   на доверие клону с правом хранить этот POOL key. Подставить путь к private
   inventory, private vars и имя клона. В private vars указать `ansible_password`
   для WinRM и `qcl_windows_user_password` для создаваемой локальной учётной записи;
   значения хранить вне Git. Запустить из корня checkout на Ansible controller.

   ```sh
   inventory=/path/to/private/inventory.yml
   clone=qcl-windows-01.example.invalid
   private_vars=/path/to/private/windows-vars.yml
   ansible-playbook -i "$inventory" -e "@$private_vars" \
       lab/ansible/windows-worker.yml --limit "$clone"
   ```

2. На клоне проверить загруженные local config, итоговые `DAEMON_LIST` и
   `START`, управление через локальную NTSSPI, ACL credentials и состояние
   `condor_startd`. Подтвердить IDTOKEN-связь в обе стороны. С manager проверить,
   что тот же clone виден в `condor_status -af Machine OpSys Arch Name` как
   `WINDOWS X86_64`. Сохранить соответствие `Machine`, имени компьютера и
   Windows endpoint в закрытом журнале. Наличие одной записи collector не
   подтверждает обратный маршрут для starter и transfer.

3. После проверки связи запустить с действующего submit host как обычный
   оператор очереди. Ввести абсолютный путь к checkout и точное значение
   `Machine` из объявления worker. В отдельный каталог будут сохранены
   JobID, вход, event log, stdout, stderr, история и SHA256. Нужны `jq`
   и штатные CLI HTCondor.

   ```sh
   checkout=/path/to/qcl-negf
   worker=qcl-windows-01.example.invalid
   (
       set -eu
       umask 077
       evidence=$(mktemp -d "$HOME/qcl-windows-smoke.XXXXXX")
       printf 'Evidence directory %s\n' "$evidence"
       cd "$evidence"
       cp "$checkout"/lab/smoke/windows.submit "$checkout"/lab/smoke/windows-payload.ps1 .
       printf 'qcl-windows-smoke %s %s\n' "$(date -u +%FT%TZ)" "${evidence##*/}" > challenge.txt
       sha256sum challenge.txt > challenge.sha256
       condor_submit -terse windows.submit "worker=$worker" > jobid.txt 2> submit.err
       job=$(awk 'NR == 1 && $1 ~ /^[0-9]+\.[0-9]+$/ {print $1}' jobid.txt)
       test -n "$job"
       if ! condor_wait -wait 150 "windows.$job.log" "$job" > wait.log 2>&1; then
           condor_q "$job" -long > queue-at-timeout.ad 2>&1
           if condor_q "$job" -af ClusterId ProcId | grep -q "^${job%.*} ${job#*.}\$"; then
               condor_rm "$job" > remove.log 2>&1
           fi
       fi
       condor_history "$job" -limit 1 -json > history.json
       jq -e --arg "job" "$job" --arg "machine" "$worker" '
           length == 1 and (.[0] |
               ((.ClusterId|tostring) + "." + (.ProcId|tostring)) == $job and
               .JobStatus == 4 and .ExitBySignal == false and .ExitCode == 0 and
               ((.LastRemoteHost // "") | endswith("@" + $machine)))
       ' history.json
       sha256sum --check challenge.sha256
       challenge_hash=$(cut -d ' ' -f 1 challenge.sha256)
       jq -e --arg hash "$challenge_hash" '
           .InputSHA256 == $hash and .IsAdministrator == false and
           .HasAdministratorsSid == false and
           (.User | type == "string" and length > 0) and
           (.Hostname | type == "string" and length > 0) and
           (.UserSid | type == "string" and test("^S-1-5-21-([0-9]+-){3}[0-9]+$"))
       ' result.json
       sha256sum result.json > result.sha256
       result_hash=$(cut -d ' ' -f 1 result.sha256)
       sed 's/\r$//' "windows.$job.out" | grep -Fx "QCL_WINDOWS_RESULT_SHA256=$result_hash"
       sed 's/\r$//' "windows.$job.out" | grep -Fx 'QCL_WINDOWS_SMOKE_STDOUT'
       sed 's/\r$//' "windows.$job.err" | grep -Fx 'QCL_WINDOWS_SMOKE_STDERR'
   )
   ```

   Сверить `Hostname` с Windows-клоном, а `User` и `UserSid` — с
   идентичностью временного пользователя по StarterLog для того же JobID.
   Отсутствие этого свидетельства оставляет slot identity непроверенной.
   Проба ограничена одним заданием на 1 CPU, 256 MiB RAM, 32 MiB scratch
   с удалением по достижении 120 секунд со времени постановки; выполнение
   политики зависит от её интервала проверки в schedd. При задержке
   transfer или истории сначала сверить native состояние точного JobID.
   Сохранять файлы неудачной попытки отдельно от следующей.

   `windows.submit` проверен локальным `condor_submit -dry-run` HTCondor
   26.0.1. В полученном ClassAd проверены требования `OpSys`, `Arch` и точное
   `Machine`, `RunAsOwner = false` и настройки transfer. Синтаксис PowerShell
   проверен локальным парсером. Windows slot, политика
   запуска PowerShell, передача файлов и cleanup по этой инструкции ещё
   требуют нативной проверки.
