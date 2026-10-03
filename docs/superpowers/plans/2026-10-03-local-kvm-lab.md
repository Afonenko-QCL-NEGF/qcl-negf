# Реализация локального KVM-стенда

Spec: [local-kvm-lab](../specs/2026-10-03-local-kvm-lab.md).

## Обязательные условия

Владение ресурсами ограничено новым namespace стенда. Production и чужие libvirt ресурсы не
меняются. Secret bytes, private state и образы не коммитятся. Owning platform-модули сохраняют
физическое и ресурсное разделение. Development snapshot не снимает release integrity guard. Проверки
имеют воспроизводимую source identity, а scientific_accepted не выводится из exit code.

## Задачи

- [x] Задача 1. Зафиксировать host/source baseline; реализовать `tofu/local-lab`, компактные NixOS
      role configurations и Ansible bootstrap; проверить ownership/idempotence.
- [x] Задача 2. Исправить AiiDA transport acceptance fixture по фактическому CalcJob CLI и
      retrieve_list; добавить regression и исполняемый installed acceptance сценарий.
- [x] Задача 3. Реализовать private lab preparation/orchestration и автоматически выведенный
      immutable development snapshot, сохраняя Gitlinks как источник состава.
- [x] Задача 4. Собрать platform bootstrap/roles, создать owned network и четыре VM; выполнить
      SSH/NFS/Slurm/cgroup, повторный bootstrap и controller reboot.
- [ ] Задача 5. Собрать/установить application и solver, выполнить package/Slurm/AiiDA/native
      integration с сохранением отрицательного научного результата и evidence.
- [ ] Задача 6. Независимо проверить изменения и actual evidence; исправить блокирующие ошибки,
      сохранить устойчивую конфигурацию, инструкции повторного запуска и отчёт.

## Измеренное состояние на 2026-10-04

Задачи 1–4 подтверждены реальным созданием четырёх KVM VM, строгим SSH, NFS `root_squash`, заданиями
Slurm, ограничением CPU/RAM через cgroup, отменой собственного тестового задания и controller
reboot. Повторные OpenTofu apply и Ansible bootstrap не изменили ресурсы; durable filesystem UUID
сохранились. Повторный reboot проверен сохранённым read-only producer до новых записей. Это platform
acceptance, а не application или scientific acceptance.

Application и отдельный synthetic transport package из snapshot05 реально собраны на хосте;
installed application integrity и synthetic immutable binding/references/wrapper/help завершились
успешно. Это package/CLI scope, без запуска producer05, Slurm/AiiDA profile или научной приёмки.
Существующие host synthetic receipts04 сохраняют свою source identity и не переименовываются в05.

Public constructor `nix/local-lab-systems.nix` прошёл actual eval04: rc0, четыре прежних output
paths, 186.72 s; неверные Manifest/depot при storage-only selection отклонены. Новые role
build/activation этой проверкой не выполнялись. Solver05 имеет только evaluation derivation. Julia04
ещё проходит upstream installCheck; часовая попытка03 была timeout. Попытка04 имеет client timeout
10800 s, наблюдались два Julia workers и проверялось наличие свободной host RAM. Launcher
`JULIA_CPU_THREADS=2` не задаёт общий hard CPU/RAM cap вложенным upstream Distributed workers.

Первый импорт application в guest store отклонён штатной проверкой доверенной подписи. Signing
identity стенда подготовлена вне Git/store. Постоянное добавление её публичного ключа в root Nix
user configuration четырёх VM ожидает отдельного подтверждения пользователя после отказа
автоматической проверки разрешений. Application profiles, AiiDA bootstrap и admission gate ещё не
активированы.

Временный CD-доступ очищен на control и двух workers: исходные `authorized_keys` совпали по SHA-256,
собственные runtime-каталоги и временный controller config удалены; admin SSH сохранён. Storage не
входил в этот cleanup. Это не full CD/application acceptance.

Независимый аудит AC2 разделил ограничение recovery/export spool и общий предел
scratch/logs/staging/retrieval. Исправления portal и Runner проверены отдельными локальными
regressions. Quota fixture остановлен до image/mount из-за 17 untrusted существующих guest closure
dependencies: EDQUOT и NFS quotas не измерены. Разделение operational paths и OS quotas для full AC2
пока proposal в `docs/implementation/storage-budget-transition.md`; VM CPU/RAM proof не означает
disk quota proof. Задачи 5–6 остаются открытыми.

После подтверждённого пользователем переноса results очищены лишние Git objects; зафиксированный
после очистки срез root `.git` около 8.3 MiB, `.build` около 3.4 GiB. Source snapshots создаются
`git clone --no-local`; это clones, а не worktrees. Source identities сохранены. Подготовленные
component commits остаются локальными, gitlinks не обновлены. Переносимый source handoff ещё
подготавливается; replay и archive hash в этом срезе не засвидетельствованы.

Публичный [отчёт проверки](../../implementation/local-kvm-lab-validation.md) фиксирует primary
receipt hashes, source scope и незавершённые acceptance границы. Исторические validation reports,
пользовательский requirements и план 2026-10-02 не переписываются.

## Интерфейсы и порядок

Platform предоставляет lab module, host configurations и bootstrap playbook; orchestrator генерирует
private variables/inventory и выполняет OpenTofu/Ansible. AiiDA fixture repair независим от VM
generation; installed acceptance использует реальный Slurm Computer/Code. Image и closures
фиксируются store path/hash, а не именем mutable checkout. Измерение свободного диска выполняется до
каждой большой сборки/импорта. Тесты fixtures не служат научной валидацией модели.

## Принятые решения

- Четыре VM выбраны для сохранения production storage assertion; цена — 768 MiB дополнительной guest
  RAM и небольшой отдельный root overlay.
- Существующий production `arch-libvirt` остаётся отдельным контрактом; новый lab module владеет
  NAT-сетью и компактными дисками.
- Работа продолжается на существующих topic branches с явно распределёнными файлами; уже
  подготовленные component commits сохраняются, submodules не откатываются.
- Нет общего лимита сессии; каждый диагностический scientific attempt получает конечный timeout и
  ресурсный профиль до запуска, без изменения физики для успеха.
