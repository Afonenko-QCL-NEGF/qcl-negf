# Контрольная точка инженерного этапа, 17 ноября 2026

Ручной старт — 16:34:28 Europe/Minsk, окно уточнено пользователем до 22:00.
Первый инженерный результат получен до окончания окна. Это действующий Linux
кластер и проверка его эксплуатационных путей; полный научный продукт ещё не принят.
Задание —[#135](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/135),
реализация —[#134](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/134).

## Что работает

| Узел | Роль | Ресурсы HTCondor | Фактический runtime |
| --- | --- | --- | --- |
| CachyOS `dell` | Host execute worker | 8 CPU / 8192 MiB | HTCondor 26.0.1, официальный Linux tarball |
| Ubuntu `qcl-condor`, VM 715 | Manager, submit, execute, GUI/monitor | 6 CPU / 11264 MiB | HTCondor 26.0.1, официальный APT |

Оба зарегистрированы в общей очереди. Worker limits оставляют резервы ОС и
другим нагрузкам; native CPU shares допускают свободные циклы, hard CPU quota
не заявлена. Производительность или масштабирование научного solve не измерялись.

- CLI: job 10 на host и 11 на guest после обновления26, затем16 и17 после
  перезапуска manager: фактические Running→Completed/ExitCode0, stdout/stderr
  и outputs получены с обоих узлов. Последняя пара — 5 с, 1 CPU / 256 MiB на job.
- Совместное исполнение: два job одновременно на CachyOS и ещё один на guest;
  отдельные PID namespaces/cgroup families. Cancel 7 удалил только своё семейство;
  сосед 8 продолжил и завершился. Это инженерная проверка, не научный benchmark.
- GUI: native Project Manager создаёт проект из template, форма передаёт CPU/RAM
  и явные inputs. Job 6/12 с CPU8/RAM 769 MiB выполнились на host, `input.txt`
  передан через HTCondor, `result.txt` возвращён. После адресной правки job 14
  с открытой карточкой получил Completed по 30 с poll без console error; первый
  ответ этой проверки был queued. Running отдельно наблюдался у GUI cancel 15.
  GUI Stop 15 на26 дал native REMOVED, исчезновение payload processes и возврат
  allocation. Отмена не приравнивается к успешному normal exit.
- Julia 1.13.4: постоянный Pkg project/depot, установка/precompile вне solver job,
  второй процесс с запретом сети читает cache. На host job 2 реально использовал
  подготовленную среду. Никакого SCBA/Poisson или другого научного solve не было.
- Beszel: три штатных agent (PVE, Ubuntu, CachyOS), native metrics/history;
  после перезапуска все 3 `up`, HTTPS/auth отвечают. Missing отличается от zero.
  Проверены светлые login/home/admin/charts/forms/dialogs/loading/404 при dark OS,
  сохранённых dark preferences и переключении OS. [Подробная QA](../../lab/monitoring-qa-2026-11-17.md).
- SSH: обычный пользователь и отдельный администратор. RDP: неверный пароль
  отклонён, действительный принят, полный GNOME desktop подтверждён сессией 321
  (`Remote=yes`, Wayland). VNC через временный native PVE proxy: desktop и
  сессия 288 подтверждены. Только тестовые сессии завершены; постоянный внешний
  VNC порт не открывался. Reconnect/длительная desktop стабильность не измерялись.

Практические адреса: [задания и файлы](https://qcl-condor.local/),
[мониторинг](https://qcl-condor.local:8443/), RDP `qcl-condor.local:3389`;
`ssh qcl-condor` и `ssh qcl-admin`. Пароли находятся только в private access files.

## Управляемость и изменения

VM 715 — Ubuntu 26.04.1 LTS, 8 vCPU / 16 GiB, root 64 GiB и отдельный data 128 GiB `/srv/qcl`.
VM принята native OpenTofu import в единственный приватный local state. Exact
plan предложил только `ostype: ""→l26`; после независимого review, пустой очереди
и native drain выполнен controlled shutdown/start. Диски, сеть, cloud-init и
administrative account не менялись. Повторный canonical plan: **No changes**,
exit0. UUID data filesystem и контрольный файл сохранились, службы восстановились.

OpenTofu source —[lab/tofu](../../lab/tofu/main.tf), внутреннее окружение —
[Ansible](../../lab/ansible/inventory.example.yml). Есть заготовки Ubuntu и Windows
clone workers, native HTCondor/Julia/Pkg, credential permissions и firewall.
Новые clone templates и Windows runtime не развёртывались. Windows slot users,
Julia/depot ACL и PSRP/WinRM должны пройти отдельный реальный опыт.

Правило инструментов принято: системная установка по умолчанию; при отсутствии —
актуальная стабильная upstream. Exact runtime pins и собственные SHA/admission/
receipt механизмы отсутствуют. Стандартная целостность package managers и Pkg
Manifest сохраняются. Native API token даёт audit и управление только VM 715;
по чужой VM проверено отсутствие write privileges. Нового IAM/vault/dispatcher нет.

OOD потребовал конечные patches поставляемого adapter/Project Manager:
argv/environment/RAM/inputs, dotted job IDs, native history/UNKNOWN/REMOVED,
Rails DateHelper и открытая карточка. Для JS использованы существующие зависимости
и штатный asset pipeline, без сети/install,2 CPU / 4 GiB / 180 с; old assets сохранены.
[Описание и воспроизводимые contracts](../../lab/ood-repair.md).

## Что удалено и сохранено

Подтверждённые старые QCL VM 710–713, их относящиеся диски, старые QCL bridges,
таблицы/цепочки firewall, installer mount и адресные bootstrap файлы удалены.
Виртуальная ёмкость удалённых disks не выдаётся за физически освобождённое место.
Сам PVE, management/LAN bridges, shared storage pools, 8 чужих VM/template states
и административные machine keys сохранены. Неизвестные/смешанные credential и
storage remnants не удалялись по одному имени `qcl`. Старый runner inventory
GitHub не получен из-за transport EOF; registrations не удалялись вслепую.

Старая рабочая копия, её HEAD/dirty gitlinks и private access files сохранены.
Новая ветка начиналась от `c53f988…`; свежий main интегрирован с опубликованными
scientific gitlinks и финальными отчётами133. Independent scientific VM, её raw
данные/изменения не трогались; её live filesystem не обследовался.
[Свежий Core/Runner handoff](science-handoff-2026-11-17.md) отделяет source текущих
refs от source фактических опытов. Строгая SCBA сходимость кампании133 не принята.

Новые operational inventory/access/TLS/state/backend references сохранены в ignored
`site/cluster-clean-start-20261117` с правами 0700/0600; исходные `.build` файлы не удалены.
В Git нет credentials, depots, scientific arrays или runtime state. Это не off-host
backup новых данных; перед важными научными запусками требуется обычное сохранение
результатов и private configuration вне этого PVE.

## Проверки и оставшиеся границы

Выполнены independent Sol/high review, native source/schema/format/link/privacy
проверки; OOD production bundle contracts: 5 tests / 32 assertions и 8 tests / 45 assertions, Ruby/bash/Ansible syntax;
настоящие CLI/GUI jobs, cancel/process cleanup, file transfer, TLS/auth, monitor
history, RDP/VNC desktops, OpenTofu import/apply/NoOp и data/service restart checks.
Старые release/bootstrap CI и научные suites не запускались.

Важное наблюдение: после collector restart host сам восстановил регистрацию через
8 мин 01 с. Старую security session отклонили, следующий native update пришёл через 300 с.
Reconfig/restart host не требовался. Быстрая или безразрывная recovery не заявлена;
при необходимости настраивается штатный UPDATE_INTERVAL, без своего watchdog.
В Editor осталась upstream console error, не помешавшая edit/save/reopen;
сквозная научная GUI-среда этим OOD прототипом не подменяется. Smoke project может
переиспользовать имена output; научные run/attempt directories должен владеть Runner.

**Следующий шаг:** на свежих scientific refs согласовать и довести один путь
input/resolver→execution→state→independent analysis, с честной маркировкой
несходимости; затем подключать его к научному GUI и автоматической оценке ресурсов.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Два Linux worker исполняют общую очередь | CLI 16/17 после restart, GUI 14/15, outputs и cleanup | Короткие synthetic jobs | сохранить |
| VM управляется OpenTofu | Native import, one-property apply, canonical NoOp | Новые clones не проверены | сохранить |
| Мониторинг и доступы действуют | 3 up/history, TLS/auth, SSH/RDP/VNC desktops | Не HA/длительный soak | сохранить |
| Все научные функции PR уже готовы | Инфраструктурный payload не вызывает solver | Core/Runner и scientific GUI впереди | данных недостаточно |
| Любой solve использует все свободные ядра автоматически | Размещение измерено, scientific scaling нет | Зависит от алгоритма и resource sizing | дополнительно измерить |
