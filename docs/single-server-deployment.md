# Первое развёртывание на одном Proxmox-сервере

Первый site содержит четыре NixOS VM: storage, control, compute и CI/build.
Дополнительный Arch worker подключается отдельным этапом. Адреса, MAC, VMID,
диски, ключи, runtime-пути и OpenTofu state принадлежат приватному site-репозиторию.
Состав исходников определяет опубликованный commit superproject и его gitlinks.

Начальная VM сборки устанавливается с официального checksum-pinned NixOS ISO
по [bootstrap-процедуре platform](../components/qcl-negf-platform/docs/bootstrap.md).
Её минимальная конфигурация не зависит от solver. Регистрация GitHub runner
отдельная: `qclNegf.runner.enable = false` оставляет административный toolchain
доступным без CI-токена. Производственные секреты jobs runner не получает.
PAT для управления runners остаётся на административном компьютере. CI получает
только краткоживущий registration token; зарегистрированный persistent runner
работает под отдельным пользователем без sudo и доступа к административным
releases. Его артефакты размещаются в `/var/lib/qcl-negf-ci/releases`.
Режим `runner-smoke` существующего workflow проверяет регистрацию и изоляцию
за пять минут без установки Julia и запуска научных тестов. Полная интеграция
остаётся отдельным запуском.

В build VM нужно получить точный опубликованный checkout с submodules,
проверить `git status --short` и выполнить штатные команды:

```sh
deno task --cwd components/QCLNEGFRunner.jl bootstrap
export JULIA="$PWD/components/QCLNEGFRunner.jl/.build/julia/bin/julia"
deno task graph
deno task solver:depot /var/lib/qcl-negf-artifacts/first-install
deno task solver:build /var/lib/qcl-negf-artifacts/first-install/solver-depot.json
```

Подготовленный depot включает закреплённый registry и lazy artifacts; его receipt
связан с commit superproject и SHA-256 Julia manifest. Архив остаётся вне Git.
Для локального `file://` receipt команда `solver:build` сначала проверяет hash
через `nix store prefetch-file` с тем же именем store-объекта, что и `fetchurl`.
Этот шаг выполняется на builder до прямой сборки site-образов: холодный Nix
sandbox не видит произвольный архив в `/var/lib`. Оригинал архива сохраняется
для повторного prefetch после garbage collection; копия в store входит в общий
дисковый бюджет. Для другого builder нужен опубликованный HTTP(S) artifact URL.
Owning Nix package закрепляет публичный CA bundle и для build environment,
и для installed wrapper: Julia Pkg инициализирует LibGit2 также в offline mode.
Проверка CA-контракта через pure Nix evaluation не заменяет native solver build.
Приватный flake использует этот receipt, `mkApplication`, `mkSolver` и
`platform.lib.mkImages`. Для режима с четырьмя VM `build-images.ts` принимает `-`
вместо Arch inventory. Образы и depot остаются на сервере; передачей образов
владеет [platform](../components/qcl-negf-platform/docs/image-transfer.md).

Все этапы одной попытки сборки используют общий сохранённый deadline, один
параллельный build и не более 100 GiB дополнительных артефактов, включая
server store, depot и новые копии образов на гипервизоре.
Стандартный профиль builder — 4 vCPU / 8 GiB RAM. Усиленный профиль —
12 vCPU / 24 GiB RAM при выключенной compute VM, пустой очереди и проверенном
свободном ресурсе хоста с резервом 8 GiB для гипервизора и 8 GiB для pnetlab.
Выбор профиля проходит штатный preflight, OpenTofu plan и apply; изменение
максимальной RAM применяется между сборками с перезапуском. Общие ограничения
Nix daemon, административной сборки и jobs runner принадлежат одной build slice.
Перед включением compute нужно вернуть стандартный профиль.
Предел — две попытки по шесть часов; исправление не продлевает текущий deadline.
Проверки инфраструктуры имеют отдельный предел: две попытки по 30 минут и
одно задание одновременно. Новые SCBA/Poisson и научные benchmarks сюда не входят.

Перед apply следует проверить plan, идентификаторы и размеры дисков. Storage
и control защищены от уничтожения. Первоначальное форматирование разрешается
только для новых пустых дисков по стабильным serial ID; после инициализации
`initializeBlankDisk` / `initializeBlankScratch` выключаются. Последующий rebuild
должен сохранять data/state/scratch и immutable Code identity.

Runtime-секреты поступают отдельно от образов. Nix получает строковые пути,
systemd проверяет владельца и права, а зависимые сервисы запускаются после
публикации credentials. Для первоначального TLS-доступа через SSH tunnel нужны
проверяемая цепочка CA и сертификат с SAN используемого имени. Проверка
сертификата Proxmox и portal остаётся включённой.

Новый экспорт — один `.tar.xz` с размером и SHA-256; браузер скачивает его штатным
потоком, а авторизованный HTTP Range позволяет возобновление. Чтение старых
multipart receipts сохраняется. Admission budget и TTL экспортного кеша задаются
явно; scientific export profiles остаются прежними.

При отсутствии внешнего backup-хранилища штатный state archive проверяется
локальным восстановлением и затем вручную копируется на внешний диск вместе
с необходимыми NFS-данными и отдельным набором runtime-секретов. Копия на том же
физическом сервере не является независимой резервной копией. Перед копированием
сохраняется согласованная граница PostgreSQL/AiiDA repository и выполняется
проверка manifest/hash; результат восстановления оценивается отдельно.

Приёмка доказывает работу инфраструктуры и транспорта синтетическими заданиями.
Научная точность модели этим этапом не проверяется.
