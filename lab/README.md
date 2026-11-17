# Лабораторный кластер QCL

HTCondor отвечает за очередь, размещение и file transfer; Open OnDemand — за
доступ к заданиям и файлам; Beszel — за host/VM telemetry. OpenTofu описывает
VM, Ansible — установленное окружение. Научный Core/Runner подключается отдельно:
инженерный smoke не является доказательством сходимости или готового scientific GUI.

## Инструменты и версии

По умолчанию используется установленный системный инструмент. Если его нет,
устанавливается актуальный стабильный upstream штатным способом. Нет exact
runtime version gate, собственного package manager, списка разрешённых SHA,
подтверждений запуска или reconciliation service. Обновление общего runtime —
при свободном worker, с обычной проверкой native queue/config после изменения.
Фактически проверенные версии указываются в отчёте опыта; они не задают pin.

Для запрошенного HTCondor 26+ fallback использует подвижный официальный канал
`26.0/current`, Ubuntu APT — канал `26.0`. Канал можно изменить в inventory.
17 ноября общий tarball alias `current/current` фактически выдавал 25.15.15,
а `26.0/current` — 26.0.1; поэтому общий alias не доказывает наличие 26+.
Стандартная APT signature validation и целостность upstream download сохраняются.
Pkg Manifest принадлежит научному проекту и описывает его зависимости.

## VM как код

[OpenTofu definitions](tofu/main.tf) создают Ubuntu и Windows workers из
подготовленных OS templates. Копируется полноценный диск; сторонние VM не
включаются в state. Новый экземпляр добавляется записью в `workers`:
node/template ID, принадлежащий QCL VM ID, storage, CPU/RAM и LAN bridge.
Пример — [workers.example.tfvars](tofu/workers.example.tfvars).

До клонирования Ubuntu template должен иметь cloud-init, QEMU guest agent,
VirtIO SCSI root disk `scsi0` и initial SSH/sudo access. Windows template —
VirtIO drivers, QEMU guest agent, Sysprep и Cloudbase-Init с ConfigDriveService,
HTTPS WinRM и доверенным серверным сертификатом. Его тип cloud-init —
`configdrive2`; это свойство подготовленного template. Bootstrap password для
Windows передаётся приватно через provider cloud-init metadata. Лицензия/образ
Windows не входят в репозиторий. Подробности — [Windows workers](windows-workers.md).

```sh
cd lab/tofu
# PROXMOX_VE_ENDPOINT и native provider credentials заданы в private environment.
tofu init -upgrade -backend-config=/private/qcl/backend.hcl
tofu plan -var-file=/private/qcl/workers.tfvars -out=/private/qcl/workers.tfplan
tofu apply /private/qcl/workers.tfplan
```

Provider получает credentials через штатные `PROXMOX_VE_*`, проверка TLS включена.
`backend.hcl` содержит только `path` к приватному local state. Для постоянного
доступа используется обычный PVE API token с минимальными native ACL; текущий
операторский token имеет audit и управление только VM715, без прав изменения
чужих VM. При добавлении новых принадлежащих QCL VM/template/storage native ACL
расширяются адресно администратором перед apply. Собственного IAM/vault нет.
Обычный `.terraform.lock.hcl` может создаваться локально самим OpenTofu;
собственного hash/approval слоя нет. State, планы и private variable files
хранятся вне Git с ограниченными правами: Windows bootstrap secrets могут попасть
в state. Перед destructive replacement сохраняются новые научные данные.

Работающая VM первого опыта не пересоздавалась под template. Её последующее
принятие в state — native `tofu import` с описанием, совпадающим с фактической
VM, и просмотром drift до apply. Для нового worker задаётся `template_id`; при принятии существующей VM
`template_id = null` исключает clone block. `data_serial` и `user_data_file_id`
позволяют сохранить фактические serial и cloud-init snippet. До import описание
аппаратуры и дисков сверяется с native `qm config`; подстановка VM ID без
корректного import недопустима.

Проверены `tofu init`, provider schema validation и `fmt`; реальный clone/apply
этих заготовок пока не выполнялся. Первый гость создан в инженерном опыте через
[provision-guest.yml](ansible/provision-guest.yml); этот адресный исторический
playbook не является способом дальнейшего управления VM вместо OpenTofu.

## Окружение через Ansible

Private inventory использует группы `proxmox`, `qcl_manager`, `cachyos_workers`,
`ubuntu_workers`, `windows_workers`. Пример содержит только placeholders:
[inventory.example.yml](ansible/inventory.example.yml). Ключи, пароли, tokens,
сертификаты, depots и scientific state в репозитории отсутствуют.

Порядок для первого Ubuntu manager:

1. `ubuntu-pool.yml` — data mount и native manager/submit/execute.
2. `julia-runtime.yml`, `julia-pkg.yml` — системная Julia или stable fallback,
   отдельная установка/precompile и offline cache check.
3. `ubuntu-gui-packages.yml` — готовые Desktop/OOD пакеты; при отсутствии OOD
   подключается официальный `latest` APT repository для установленной Ubuntu.
4. `ubuntu-gui-config.yml`, `ood-htcondor-repair.yml`, `ood-light.yml` — TLS,
   native cluster adapter, инженерный project template и светлая тема.
5. `ubuntu-rdp.yml`, `ubuntu-network.yml` — remote login и обычная LAN identity.
6. `monitor-hub.yml`, `monitor-agent.yml` — Beszel hub/agents.

Новый Ubuntu execute-only worker: `ubuntu-worker.yml`, затем Julia/Pkg с
ограничением нужного host. Он использует обычные native POOL signing key и IDTOKEN, как штатная
многомашинная установка HTCondor; private inventory ссылается на файл ключа,
его содержимое не публикуется. Windows:
`windows-worker.yml` через штатное Ansible PSRP/WinRM HTTPS. Неопробованные
Windows особенности отмечены отдельно, а не объявлены готовыми.

```sh
ansible-playbook -i /private/qcl/inventory.yml lab/ansible/ubuntu-worker.yml
ansible-playbook -i /private/qcl/inventory.yml lab/ansible/julia-runtime.yml --limit qcl-linux-01
ansible-playbook -i /private/qcl/inventory.yml lab/ansible/julia-pkg.yml --limit qcl-linux-01
ansible-playbook -i /private/qcl/inventory.yml lab/ansible/windows-worker.yml
```

Для CachyOS, где нет подходящего системного HTCondor package, используется
официальный Linux tarball и обычный systemd service:
`cachyos-worker.yml`. Неустановленные native RDP/SSH clients, CA и адресные
правила UFW — `host-admin.yml`. Правила разрешают TCP9618/45876 только от
текущего IPv4 manager, не выключая и не сбрасывая чужой firewall. При изменении
DHCP адреса manager правило обновляют обычным Ansible запуском. Для дальнейшей
сети предпочтительны обычный DNS и стабильная DHCP reservation.

Резервы CPU/RAM задаются для машины один раз. Ubuntu worker вычисляет advertised
ресурсы из native facts после резервов; на машине с чужими VM/сервисами резервы
выбираются по live inventory. HTCondor partitionable slots размещают несколько
заданий и учитывают CPU/RAM/disk. Memory hard limit и PID/cgroup tracking
на Linux отделяют семьи concurrent jobs. CPU shares позволяют использовать
свободные циклы и не являются hard CPU affinity/quota.

Обычному научному запуску не нужен ручной выбор сервера или обязательный ввод
лимитов. Defaults/оценка памяти и threads входят в следующий Core/Runner этап;
инженерная форма пока позволяет проверить явные CPU/RAM/input requests.
Нельзя выдавать свободные ядра за доказательство масштабирования одного solve.

## Использование первого опыта

- Задания и файлы: `https://qcl-condor.local/`.
- Мониторинг: `https://qcl-condor.local:8443/`.
- SSH пользователя: `ssh qcl-condor`; администратора: `ssh qcl-admin`.
- RDP: native Remmina/FreeRDP, `qcl-condor.local:3389`.
- VNC: штатная консоль Proxmox; постоянный внешний VNC порт не открывается.

Credentials доступны оператору в private access files; в URL/скриптах задания
их нет. HTTP работает поверх TLS с лабораторным CA, установленным в native
trust store. Первая учётная запись OOD использует Basic Auth и локального
пользователя; это LAN установка, не готовая схема публичного Internet/SSO.

CLI обычного пользователя на manager:

```sh
condor_status
condor_q
# В отдельном каталоге с копиями lab/smoke/payload.sh и cli.submit:
condor_submit cli.submit
condor_q -nobatch
condor_history -limit 5
condor_rm JOB_ID
```

После timeout сначала читается native queue/history; повторный submit вслепую
не выполняется. Успешный exit code проверяется вместе с output/eventlog.
Отмена проверяется по native event и освобождению процессов/слотов.

GUI: Project Manager → Create from template → QCL Native Smoke → Show → Launch.
Шаблон передаёт только скрипт и явно указанные inputs, не весь project/depot.
`result.txt`, `job.log`, stdout/stderr возвращаются в project; их можно открыть
через Files/Editor. Это sleep-only smoke до120s, не научный solver.
[Адресный ремонт OOD](ood-repair.md) описывает проверенный upstream contract.
Все web views остаются светлыми, включая Editor и Beszel admin.

## Мониторинг, данные и ограничения

[Сборка светлого Beszel](monitoring-build.md) использует upstream backend/agent;
[реальная browser QA](monitoring-qa-2026-11-17.md) отличает missing от настоящего
нуля. CPU/RAM/disk/network/history — host-level telemetry. Per-job requests,
allocations и execution events принадлежат HTCondor. Научные невязки принадлежат
Runner/Core и не выводятся из технического статуса очереди.

Данные нового гостя находятся на отдельном `/srv/qcl`; проверена перезагрузка
с сохранением mount/data. Это не off-host backup. До хранения новых важных
расчётов нужен выбранный обычный backup этого каталога и private configuration.
Independent scientific VM/campaign133 не включена в этот lifecycle.

Целевой научный GUI, автоматическая оценка памяти solve, scientific resume,
Windows runtime и импорт существующей VM в OpenTofu пока не приняты. Остаток
и фактические scientific refs — в [handoff](../docs/implementation/science-handoff-2026-11-17.md)
и контрольном отчёте этапа.
