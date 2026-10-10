# Чистая пересборка QCL-инфраструктуры

Статус: **план будущей операции**, 2026-10-09. В этой задаче ни VM, ни диски,
ни результаты не изменяются. Связанные требования: I03–I05, I10–I13,
D04–D08. До исполнения нужны фактические identities/capacity и конкретный
проверенный change plan; их в публичном репозитории сейчас нет.

## Согласованная область

Удалить только всю инфраструктуру QCL, включая неактивные VM и старые
QCL resources на требуемых backend. Посторонние VM остаются активными.
Старые научные результаты, AiiDA DB/repository, образы, depots, caches,
scratch и QCL operation state **не сохранять и не переносить**. Это
необратимая потеря старого QCL state, выбранная для проверки cold bootstrap.
План не требует их backup и не подменяет cold start восстановлением старой DB.

Новый старт — свежий clone выбранного опубликованного source ref с его
gitlinks. Private values и access tokens предоставляет локальный доверенный
shell-файл. Это внешний вход установки, а не восстановленный private
repository и не источник hidden policy. Git history/исходники не входят
в удаляемый runtime набор.

## 0. Подготовить доказуемый cold-start маршрут

До удаления определить, **где исполняется первый bootstrap и как создаётся
первый builder**. Если images создаёт прежняя QCL builder VM, её удаление
создаёт цикл. Допустимые решения для проверки:

- trusted локальная Linux среда исполняет только orchestration; первый
  builder создаётся из доступного pinned seed image/installer, затем все
  тяжёлые builds идут на нём;
- заранее доступный базовый Nix builder вне удаляемого QCL набора, если его
  наличие объявлено внешней предпосылкой и он не предоставляет прежний
  QCL depot/store outputs как скрытое условие успеха.

Рекомендуется первый путь. В текущем коде уже есть отдельный `tofu/bootstrap`
и [официальный ISO маршрут](../../components/qcl-negf-platform/docs/bootstrap.md)
без зависимости от solver; не следует заново изобретать этот adapter.
Первичная ручная установка builder из checksum-pinned upstream NixOS ISO
допустима. Seed — объявленный upstream installer либо заново созданный
артефакт, не старый QCL image/depot. Полный cold-source путь, новые identities
и совместимость с измеренным storage надо подтвердить до wipe; документация
этого маршрута сама не является runtime доказательством.

Установочный manifest должен перечислить обязательные inputs: адрес/API
Proxmox и host identities, bridge/subnet/controller endpoint, storage IDs,
boot profiles, storage/NFS endpoint и trusted hostname/NodeAddr mappings,
защищённые foreign VM floors, CPU/RAM/диск, credential sources.
Обычно публичный source не способен сам узнать, какой физический диск можно
переформатировать. Shell-файл проверяется без печати секретов, не попадает
в Git/Nix store/общий logfile; отсутствующее значение — ранний blocker.

Определить доступность GitHub/upstream packages/seed image. Daily LAN
operations без GitHub — другой контракт, не обещание offline cold build.
Проверить точный source ref и то, что каждый gitlink доступен из нового clone.

## 1. Read-only inventory и план принадлежности

Снять полный inventory **всех**, включая inactive, QCL VM/containers/domains
на Proxmox, libvirt и Hyper-V. Не удалять native host OS. Для каждого объекта:
provider/UUID/VMID, роль, состояние, диски, snapshots, backing chain, cloud-init
seeds/snippets, imported images, networks, registrations и operation files.

Принадлежность определять по source/provider state и реальным identifiers;
имя с префиксом QCL — подсказка, а не достаточное основание. Найти orphaned
QCL ресурсы, которых больше нет в текущем OpenTofu state. Несогласие state
и реального inventory разрешить до удаления.

Разделить объекты на:

- QCL-exclusive — точный destructive набор;
- shared с foreign consumer — исключить из удаления, удалить только QCL data;
- unknown ownership — blocker, нельзя угадать по filename/size.

Shared bridge/storage pool/PVE root disk нельзя стирать вместе с QCL VM.
Построить список foreign VM и их зависимостей для проверки сохранности.
`tofu state rm` не удаляет remote объект; broad `destroy` на общем state
не гарантирует правильную область. [OpenTofu resource behavior](https://opentofu.org/docs/language/resources/behavior/).

## 2. Свежие ресурсы и SSD

Установить installed PVE version, physical CPU/RAM, actual usage/reserves,
активные foreign VM и поддерживаемое ballooning. Прошлые 56 GB/30 cores
не используются как текущая capacity. Для SSD: стабильный device ID,
model/capacity/health, partitions, filesystem, mount points, VG/LV или ZFS
topology, thin-pool data/metadata, свободные extents и реальные consumers.

Уточнить, что означает «основной том 100 ГБ»: PVE root, guest filesystem
builder или artifact storage. Числа GB/GiB не взаимозаменяемы. Диск seed,
Nix store/closures, depot, build temporary files, images/staging и swap
имеют совместный peak; существующий cap 100 GiB не является измерением
этого peak.

Если 100 ГБ относятся к builder root, учитывать ещё и source guard:
`ansible/bootstrap-root.yml:14` сейчас допускает максимум 100 GiB. Расширение
реального LV само не обновляет cold-bootstrap contract. Новый measured cap
должен пройти через private inputs, storage budget и owning platform checks,
а не получиться разовым обходом assertion.

Нужен short capacity worksheet с protected reserve и оценкой boot/build
peak. Private hardware values остаются вне Git. На этом этапе не запускаются
научные benchmarks ради выяснения дисковой topology.

## 3. Адресное удаление

После готовности нового маршрута:

1. Закрыть QCL submission. Работающие QCL jobs завершить или остановить по
   отдельно принятому teardown порядку; чужие jobs/VM не затрагивать.
2. Остановить и удалить **точные** QCL VM identities, включая inactive.
   Защиты `prevent_destroy` снять адресно только для принятого QCL набора.
3. Удалить их exclusive disks/snapshots/backing assets/seeds; не удалять
   shared consumer resources. Очистить старые QCL results/AiiDA/cache/scratch.
4. Удалить QCL registrations/старый operation state и stale access grants,
   сохранив внешние provider credentials, необходимые новому bootstrap.
5. Повторить inventory: удаляемый набор отсутствует; foreign VM активны,
   их disks/network/storage config сохранны. Пустой provider state без этого
   не является доказательством удаления всех ресурсов.

Исполняемые команды генерируются только после измеренного exact inventory.
В этом документе нет универсального `wipefs`/`rm -rf` по предположительному
device path. Обратный путь после выбранного wipe — новая установка из source,
а не обещание вернуть старые scientific data.

## 4. Расширение тома: условные маршруты

| Измеренное состояние | Допустимый маршрут | Условие / остановка |
| --- | --- | --- |
| LVM, целевой LV/FS, достаточные free extents | Расширение LV и поддерживаемое filesystem grow по документации установленной версии | Рассчитаны root/build/swap/foreign reserves; не расходовать весь VG на один том |
| Свободный SSD/доступная дополнительная область | Отдельный volume для QCL build/artifacts и/или swap; либо поддерживаемое добавление capacity | SSD/область точно не используется foreign VM/host data |
| Свободное место находится внутри thin pool, занятого foreign VM | Сохранить pool; искать дополнительный disk/volume или изменить QCL storage layout | Не обещать безопасное shrink/reformat только потому, что часть QCL volumes удалена |
| ZFS/другая topology | Отдельный план согласно backend и filesystem support | Не переносить LVM рецепт; сначала topology/health/dependencies |
| Изменение требует reboot/остановки foreign VM | Отложить этот вариант; предпочесть online grow/отдельный data volume, если возможно | Требование foreign VM active не отменяется автоматически |

PVE storage documentation отдельно учитывает thin-pool metadata при
расширении: [Administration Guide, LVM-thin](https://pve.proxmox.com/pve-docs-8/pve-admin-guide.pdf).
Это справка по механизму; точную установленную версию и команды выбрать
по inventory. **Возможность расширить именно этот 100 ГБ том пока неизвестна.**

## 5. Большая подкачка без обещания вытеснить конкретные VM

Разделить host SSD swap и guest/build swap. Наличие host swap не отменяет
guest cgroup `MemorySwapMax=0`; текущие builder profiles именно так ограничены.
Zram расходует RAM и не равен свободному SSD swap:
[kernel zram documentation](https://kernel.org/doc/html/next/admin-guide/blockdev/zram.html).

Размер swap выбирается после SSD/free-space/build-peak inventory. Policy
задаётся в host/guest configuration, а не командой разового включения без
владельца. Swap не включать в Slurm RealMemory и не увеличивать автоматически
scientific request выше physical budget. PVE/foreign floors и CPU weights
задаются отдельно.

Приёмка будущего ограниченного опыта: без host/guest OOM, control/storage
доступны, swap-in/out и pressure наблюдаемы, память действительно возвращается
перед стартом большой VM, тяжёлая фаза остаётся в согласованном времени.
Проверять на bounded инженерной нагрузке, затем на реальном согласованном
scientific run. При thrashing снизить overcommit/нагрузку; не уменьшать
физическую задачу скрытно. Exact performance threshold устанавливается до
опыта по цели, а не задним числом для pass.

## 6. Новый холодный bootstrap

1. Свежий clone выбранного source ref/gitlinks; загрузить validated private
   inputs; создать fresh site config. Старые receipts/state/depot не читать.
2. Создать первый builder по доказанному seed маршруту. Назначить измеренный
   build ресурс после host/foreign/control/storage reserve; согласовать Nix,
   systemd slice и Julia/CI parallelism.
3. Cheap preflight всех четырёх NixOS ролей, native nginx config, paths,
   flake inputs, builder identity/permissions и capacity до heavy builds.
4. Построить native dependencies/Julia/application/guest artifacts из pinned
   inputs; измерить disk/build peak. Отдельно проверить release publishing,
   Nix signature и recipient trust/import. Checksum SSH transfer не называется
   detached подписью image.
   На окончательном ready source ref выполнить **единственный final CI dispatch
   этого bootstrap-кандидата в build-фазе, до освобождения builder**.
   Test fixtures/VM integration здесь принадлежат CI; реальные production
   guest/service проверки ниже остаются отдельными gates. Не менять source
   после CI и считать receipt относящимся к изменённому составу.
5. Создать fresh storage/control и compute; fresh AiiDA profile/DB/repository,
   identities, Slurm/NFS и credentials. Admission закрыт до service checks.
6. Передать ресурс builder → compute только после завершения builds и CI шага 4 и
   daemon tasks, graceful освобождения и свежей capacity проверки. Проверить
   services, actual RealMemory/cgroups/NFS и installed executable.
7. Small engineering CalcJob: submit/status/result/cancel/failure/staging.
   Fixture явно synthetic; success не засчитывается за S01.
8. Подключать остальные workers по accepted install profiles; explicit
   controller endpoint в input, trusted identity и release gate до RESUME.
9. Сверить source identity CI шага 4 и всех последующих gates. Второго CI
   dispatch здесь нет; старые receipts/full acceptance не наследуются.
   Если выбранный CI contract действительно требует уже готовых production
   guests, выбрать **до запуска** другой порядок: compute engineering smoke →
   idle handoff в builder → один final CI → idle handoff в compute → повторная
   service проверка. Научный S01 начинается только после этого цикла.
10. Выполнить S01 (равновесие 0 mV/period, 70 K) по отдельному finite scientific budget; получить результат
    существующим независимым Results/CLI reader из NFS. Новый brief/full/agent
    API не является prerequisite S01; позднее он принимается на доступном
    сохранённом результате через те же identity/interpretation contracts.

## 7. Восстановление и итог приёмки

Restore проверять на **новом disposable state**, созданном после bootstrap:
согласованные DB/repository backup/restore, небольшой result artifact и
ссылки/права. Для старого удалённого QCL state restore не обещан и backup
не делается. Этот тест проверяет будущую эксплуатацию и не должен позволять
cold bootstrap опереться на старую инфраструктуру.

| Gate | Свидетельство | Что не следует из него |
| --- | --- | --- |
| Exact wipe | Реальный inventory до/после и foreign checks | Bootstrap |
| Disk/swap readiness | Topology/capacity/health + выбранный change plan | Быстрая научная задача |
| Cold build | Native outputs из source + new private inputs | Подпись, guest boot или физика |
| Trust/delivery | Подпись/recipient import и точная enrolled identity | Работоспособность scheduler |
| Infrastructure | Guests/services/NFS/Slurm и interrupted transition cases | Convergence/validation QCL |
| Restore | Новый test state восстановлен согласованно | Сохранность уже удалённых old results |
| Scientific S01 | Итоговое равновесие 0 V / 70 K, FDR/raw checks и discretization sensitivity | Ненулевой транспорт, вся ВАХ/все модели/оптическая мощность |

Желаемый суточный маршрут реалистично оценивать после seed/preflight/storage
проверок и дешёвых targeted fixes. До них точное время неизвестно. Если
диск или first-builder route блокирует bootstrap, это явный blocker,
а не повод начать разрушение и рассчитывать устранить цикл после удаления.
