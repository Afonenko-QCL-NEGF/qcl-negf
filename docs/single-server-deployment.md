# Первое развёртывание на одном Proxmox-сервере

Этот runbook описывает существующий маршрут и исторические проверки с
ограниченной областью применимости. Требования следующего релиза и план
холодной пересборки находятся в [едином корпусе](system/README.md) и
[плане пересборки](system/rebuild.md). Новая схема локального управления и
передачи ресурсов ещё не реализована; этот файл не является командой удалять VM/диски.

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
проверить `git status --short` и выполнить штатные команды. Перед тяжёлой native
сборкой выполнить preflight ниже; команды не являются разрешением обойти его:

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
вместо Arch inventory и обязательный `--preflight-receipt ACTUAL_PREFLIGHT.json`.
Перед первым image stage он сопоставляет четыре role derivations, nginx
executable/config и актуальный hash с успешным native preflight receipt.
Образы и depot остаются на сервере; передачей образов
владеет [platform](../components/qcl-negf-platform/docs/image-transfer.md).

## Preflight до тяжёлой сборки

Из корня superproject запускать owning проверку platform:

```sh
deno task bootstrap:preflight --receipt /absolute/private-site/preflight.json preflight \
  --site /absolute/private-site --nix /run/current-system/sw/bin/nix --check-nginx \
  --openssl /absolute/measured/openssl --mount /absolute/measured/mount \
  --nginx-namespace '["/run/current-system/sw/bin/sudo","-n","/run/current-system/sw/bin/unshare","--mount","--net","--propagation","private"]'
```

Она сохраняет bounded stdout/stderr, проверяет четыре роли, собирает только
generated nginx config и запускает фактический nginx executable с `-t`.
Namespace entry разрешён доверенному административному builder, отдельно от
изолированного Actions runner. Пути openssl/mount/sudo/unshare сначала измеряют;
оператор root может выбрать prefix без sudo. Недоступный namespace означает
отказ проверки. Инженерный тест подставляет собственный сертификат только в
объявленные TLS directives и не читает production private key.
Подробный контракт и отдельная команда root accounting описаны в
[platform bootstrap](../components/qcl-negf-platform/docs/bootstrap.md) и
[nginx preflight](../components/qcl-negf-platform/docs/nginx-preflight.md).

После подготовки приватного site и реальных depot metadata, до native
installCheck и полной сборки образов, проверить все четыре роли `storage`,
`control`, `compute`, `ci`. Для каждой получить
`nixosConfigurations.<role>.config.system.build.toplevel.drvPath` через bounded
`nix eval`; это evaluation, а не system build. Использовать те же source inputs,
site files, runtime modules и `mkSolver` arguments, что в будущей сборке.
Fixture constructor check отдельно обозначается как fixture и не заменяет
evaluation реального site. NixOS assertions, в частности явный interface для
`networking.defaultGateway` при networkd, должны пройти до длинного запуска.

Для control получить context строго выбранного nginx config: при
`services.nginx.enableReload = true` использовать
`environment.etc."nginx/nginx.conf".source`, иначе
`systemd.services.nginx.serviceConfig.ExecStart` из control configuration.
Выбрать единственную зарегистрированную derivation `nginx.conf.drv`. Затем
собрать только её `^out` строгим config writer и выполнить обязательный native
`nginx -t` на фактической конфигурации. Writer exit code 0 и включённая
validation сами по себе этот gate не закрывают. Native test должен завершиться
успешно с нулевыми warn/error/crit/alert/emerg counters. Severity counters gixy фиксируются отдельно:
отсутствующий вывод, в том числе при cache hit, остаётся `not_measured`, а не
измеренным нулём. Не заменять config writer
полной image/system сборкой и не ослаблять gixy. `proxy_set_header Host $host;`
согласуется с нормализованным host; forwarded headers, TLS и relative portal
routes проверяются для конкретного site отдельно.

Для штатного API proxy site включает `qclNegf.application.api.tls.enable`,
задаёт runtime certificate/key paths и удаляет дублирующий site vhost.
Owning module использует `onlySSL`, loopback listener и systemd runtime
credentials. Ручное `listen.ssl = true` без `onlySSL`/`addSSL`/`forceSSL` не
гарантирует, что nginx module добавит certificate directives.

Bootstrap профиля использует supported `engine_kwargs.connect_args` для
PostgreSQL Unix socket. Холодная инициализация запрещена при любой непустой или
частичной repository либо существующем database catalog; `reset=False` не
заменяет этот guard. Существующий совместимый профиль сохраняет UUID и данные.

Runtime environment фиксируется до запуска: проверенные абсолютные executable
paths, явный `PATH`, рабочий каталог builder и принадлежащие ему Git indexes.
Успешная interactive shell не доказывает, что `nix`, `deno` или другой tool
доступен в systemd unit. Использовать абсолютный путь из выбранного NixOS
toolchain; для `qemu-img` выбрать declared `out` реальной image-input derivation,
а не первый результат multi-output query. Параметры flake inputs относятся к
выбранной системе, а не к directory name Nix output. Путь, добавленный внутрь
read-only store tree, не использовать как новый изменяемый source.

Private site flake должен иметь явный существующий input path/URL и frozen
source revision; после переноса checkout проверить resolved input и generated
lock. Выражение для source revision применяется к flake; для функции из файла
`{ siteDir }: ...` передать
`--apply 'f: f { siteDir = builtins.getEnv "QCL_SITE_DIR"; }'` с явно заданным
существующим site directory. Сама lambda не является строкой revision.
Если Nix string context проверяется словарём, context снимается только с ключа
такого словаря; derivation/output dependency не заменяется plain string.

Для административных read-only Git проверок задавать `GIT_OPTIONAL_LOCKS=0`
либо `git --no-optional-locks`, чтобы status после передачи владельца не создал
root-owned index. Проверить root и все восемь owning checkouts. Состав derive
из committed gitlinks; не создавать второй вручную поддерживаемый список SHA.
Новые private helpers сначала проходят bounded source/metadata fixtures и
независимый review на одном immutable наборе входов. Первый отказ сохраняется;
повтор разрешён после конкретного диагноза с новой attempt identity и бюджетом.

Все этапы одной попытки сборки используют общий сохранённый deadline, один
параллельный build и не более 100 GiB дополнительных артефактов, включая
server store, depot и новые копии образов на гипервизоре.
Профиль `local-debug` предназначен для ноутбука: 4 vCPU / 8 GiB RAM,
7 GiB общей build slice, два Julia test workers и две Pkg precompile tasks. Он явно выбирается
конструктором `nix/local-lab-packages.nix`; ограничения ноутбука не задают
серверный бюджет. `mkSolver` принимает `juliaTestProfile`, по умолчанию
`production-build`; необязательный `juliaTestWorkerLimit` ограничивает только
тестовые процессы по бюджету памяти. CLI передаёт его как
`solver:build RECEIPT --profile production-build --test-workers INTEGER`.
Не заданный предел сохраняет upstream CPU-based worker count. Этот профиль сохраняет реальные CPU Julia и полный
набор native install checks. CPU/RAM серверного bootstrap задаются в приватном
site по свежему inventory; platform согласует VM, общую slice и Nix cores.
Bootstrap может совместно использовать все физические CPU хоста, сохраняя
работу остальных VM и резерв RAM гипервизора. Число независимых Julia workers
должно учитывать измеренный расход памяти, а параллелизм компиляции — весь
доступный бюджет. При долгой сборке сохраняют телеметрию и оценивают прогресс.
Перед включением production compute bootstrap возвращают к обычному
распределению ресурсов; CI запускают после серверной и локальной проверки
готового результата.

`production-build` использует доступные CPU для компиляции через
`NIX_BUILD_CORES`; предел test workers задаётся отдельно по памяти. Пример:
32 доступных CPU, explicit `juliaTestWorkerLimit = 16`, 2 GiB на каждый worker
и 4 GiB резерва требуют envelope 36 GiB. Это эвристика admission, а не доказанная
верхняя граница RSS; нужны telemetry/OOM counters. На builder с меньшим числом
доступных CPU launcher берёт минимум CPU, числа тестов и explicit limit.
Без explicit limit остаётся upstream поведение, допустимое при достаточной RAM.
`local-debug` сохраняет два workers и две precompile tasks. Ни один профиль
не задаёт `JULIA_CPU_THREADS`: `Sys.CPU_THREADS`, `Sys.EFFECTIVE_CPU_THREADS`
и native BLAS affinity остаются реальными. Версия Julia, upstream factory,
native phases и исходный declared test skip list сохраняются.

Совместимые исторические профили builder: `standard` — 4 vCPU / 8 GiB RAM;
`burst` —
12 vCPU / 24 GiB RAM при выключенной compute VM, пустой очереди и проверенном
свободном ресурсе хоста с резервом 8 GiB для гипервизора и 8 GiB для pnetlab.
Выбор профиля проходит штатный preflight, OpenTofu plan и apply; изменение
максимальной RAM применяется между сборками с перезапуском. Общие ограничения
Nix daemon, административной сборки и jobs runner принадлежат одной build slice.
Перед включением compute нужно вернуть стандартный профиль.
Бюджет и точки оценки целесообразности конкретной попытки фиксируются в приватном
runbook согласно поручению пользователя. Смена профиля сохраняет прежние журналы
и создаёт новую попытку с точной source identity. Новые SCBA/Poisson и научные
benchmarks сюда не входят.

## Сохранение попытки и приёмка

Main build запускать в owned normal runtime systemd unit с ограничениями CPU/RAM,
deadline и output. Сохранить unit bytes, InvocationID, source graph, command logs
и terminal state. Transient unit может исчезнуть сразу после успеха и оставить
пустой InvocationID; для main provenance этого недостаточно. Observer связывает
каждый sample с captured InvocationID. Перед reboot сохранить completed receipts
в постоянном artifact directory: `/run` после reboot не является источником
истории. Не изменять already executed script или прежний receipt ради новой
попытки.

Если все owning commands завершены, но final accounting отказал из-за прав на
root-only history, не пересобирать native/images только ради этого bookkeeping.
Отдельный root read-only verifier проверяет original failed unit и disk report,
source/depot/native/image identities и новый полный учёт тех же каталогов.
Original failure сохраняется. Composite engineering receipt отдельно фиксирует
`owning_commands = pass`, original accounting failure и fresh root accounting
pass; он не объявляет failed main unit успешным.

Дисковая политика считает одним `du -B1 -s` allocated bytes `/nix/store`, releases
и artifacts в исходном порядке, включая все retained histories. Отдельные du по
каждому root меняют cross-root hardlink deduplication. К сумме добавляется только
`max(0, st_size - st_blocks * 512)` для каждого из четырёх новых QCOW файлов.
Это mixed allocated-plus-QCOW-sparse policy; apparent bytes всего дерева,
QCOW virtual size и `df` не заменяют её. Не добавлять полный размер образа второй
раз и не исключать history ради лимита. Root reader снимает permission blocker,
а не ослабляет права. `df` может показать `/nix/store` как отдельный bind-mount
target того же filesystem; serial used/free rows могут различаться. Проверять
соответствующие mount ancestors и реальный filesystem identity, а не требовать
одинакового target `/` или атомарного совпадения всех строк. Сканирование не
атомарно при посторонних writes/GC; эту границу evidence следует сохранить.

Доказанный native output можно повторно использовать при совпадении точных
derivation/output, проверенных contents, версии, factory/phases и profile/worker
arguments. Original proof сохраняет собственные root/gitlinks, producer и
attempt. Новая continuation содержит explicit carry-forward и отдельно
проверяет текущий source graph; она не переписывает старую source identity.
Changed native contract или неподтверждённые contents требуют новой native
приёмки. Новый root HEAD сам по себе не доказывает, что прежние solver/images
построены из него.

После этих исправлений следующий опубликованный HEAD отличается от исторически
собранного `fade6f021edf`; старые receipts остаются свидетельствами своего freeze.
Этот runbook фиксирует engineering procedure и не заявляет live production
deployment, guest/service success или scientific acceptance для нового HEAD.

| Gate | Необходимое свидетельство | Что остаётся отдельным |
| --- | --- | --- |
| Engineering build | Source graph, selected native suite/content proof, packages, four images и disk accounting | Подписи, recipient trust, image staging, guest boot |
| Production acceptance | Реальные guest boot/services и transport/cancellation/failure contracts | Restore и scientific validation |
| Restore | Согласованная archive boundary, проверка manifest/hash и фактическое восстановление | Независимость внешней backup-копии |
| Final CI | Ready source ref, verified PR heads, empty queue и один full dispatch | Научная приёмка |

Перед final CI публикуются и проверяются восемь owning component refs/PRs,
затем superproject с exact gitlinks. Remote refs, PR state и защиты читаются
заново. Runner registration выполняется на final ready stage после fresh empty
queue check; административный PAT не передаётся jobs runner. Один full CI run
должен иметь expected root `head_sha`; automatic reruns запрещены. До готового
результата нужны дешёвые локальные/server checks, а не промежуточные CI dispatches.
Отсутствующий inventory, admission, credentials или обязательное evidence
останавливает зависимый этап; доступная независимая подготовка продолжается.

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
