# Локальный KVM-стенд QCL-NEGF

Поручение: подготовить и реально развернуть локальное тестирование пакетов и интеграций через
QEMU/KVM, OpenTofu и Ansible, исправляя обнаруженные ошибки. Доступ к production не требуется.
Пользователь снял лимиты этой сессии; admission по фактически свободной RAM и диску остаётся
обязательным условием запуска.

## Топология и владение

Четыре NixOS VM: `control`, `storage`, `worker-1`, `worker-2`. Production-модули controller,
Slurm/cgroup v2, NFS, state disk и worker scratch используются без ослабления их assertions. Storage
не совмещается с controller. Отдельная принадлежащая стенду libvirt NAT-сеть не меняет существующий
LAN bridge или `default` network. Все имена ресурсов имеют namespace. Private state, ключи,
инвентарь, disk images, депо и результаты находятся в ignored `.build/local-lab`.

Начальный ресурсный профиль: controller 2048 MiB/2 vCPU, storage 768 MiB/1 vCPU, workers по 2304
MiB/2 vCPU. Всего 7424 MiB guest RAM. Это профиль инфраструктурных и малых диагностических тестов, а
не разрешение уменьшить сетку научного расчёта. VM используют общий неизменяемый bootstrap QCOW2 и
отдельные COW root volumes; state/data/scratch volumes имеют стабильные serial и отдельный жизненный
цикл. Root capacities — логические sparse пределы, а не резервирование свободного диска.

## Bootstrap и установка

Один platform-only bootstrap image обеспечивает SSH, cloud-init и гостевые инструменты. Role
configurations собираются из owning NixOS-модулей; closures можно включить в общий image либо
передать `nix copy` и активировать Ansible. Secret bytes передаются Ansible в runtime/persistent
private paths, никогда не попадают в Nix store, Git или OpenTofu state. Только явно назначенные
новые пустые state/data/scratch disks могут форматироваться; повторный bootstrap сохраняет
filesystem UUID и данные. Неизвестный или чужой ресурс отклоняется.

Установка application/solver — отдельная стадия после реального boot/network/NFS/ Slurm proof.
Release guard и worker `node-check` сохраняются. Development source snapshot автоматически выводится
из точных Git commits и имеет собственную immutable identity; обычный release sourceGraph guard не
ослабляется. Набор gitlinks опубликованного superproject не заменяется вручную поддерживаемым lock.

## Проверки и доказательства

1. OpenTofu format/validate/plan; измерение RAM, disk, KVM и отсутствие overlap.
2. Реальные четыре KVM boots, SSH, hostname resolution, NFS root_squash и UID3000; отдельные
   data/state/scratch mount sources; Slurm два workers и cgroup v2.
3. Повторный apply/Ansible bootstrap без изменения UUID или потери данных; reboot controller и
   повторное чтение сохранённого output.
4. Installed package imports/entry points, exact Julia1.13.0, solver self-check на обоих workers,
   native HDF5 → results reader/export, AiiDA bootstrap identity.
5. Детерминированный небольшой negative transport fixture через настоящий CalcJob CLI и retrieve
   projection, затем Slurm/AiiDA; процесс и научная приёмка имеют раздельные статусы. Малый native
   pause/resume выполняется лишь после runtime installation и имеет явно записанный конечный
   per-attempt budget.
6. Проверка отсутствующего/stale release gate и сохранности предыдущего runtime.

Каждая проверка сохраняет команду, exit/status, Git/source identity и фактическое свидетельство.
`not_measured` не превращается в pass. Linux/KVM не подтверждает Windows/Hyper-V shutdown ordering.
Физика, допуски и production study grids не меняются ради прохождения инфраструктурной проверки.
