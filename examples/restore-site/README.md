# Изолированный restore controller

`nix/restore-site.nix` принимает уже вычисленные `production`, её `platform`,
данные `productionSite` и новый `target`. Он расширяет тот же controller через
`extendModules`, сохраняет application/solver closures, PostgreSQL 17 и UID 3000,
маскирует bootstrap/API/AiiDA/Slurm/nginx/секретные units и отключает автомонтирование
общего job directory. PostgreSQL и локальный state repository остаются доступны
для отдельной процедуры восстановления. Образ не содержит backup или credentials.

Для flake caller используйте один source input `qcl`, закреплённый полным commit
с submodules, и source input `productionSite` с `flake = false`. В outputs
вызовите `default.nix` с этими inputs. Тогда `productionSite` является исходным
деревом в store, а её `outputs` вычисляются с тем же `qcl`; второй вложенный
production lock graph не создаётся. Файл `default.nix` показывает composition;
адрес `192.0.2.22`, VM ID и MAC в нём — пример, который требует замены.

Не импортируйте mutable абсолютный private path внутри derivation и не
предполагайте, что relative path input будет разрешаться относительно соседнего
site после копирования flake в store. После eval сохраните эффективные source
identities и проверьте совпадение production/restore application и solver,
native runtime, assertions, масок, state mount и PostgreSQL. Nix определяет
outputs как функцию от вычисленных inputs и ограничивает relative path inputs
их source tree: [Nix flake reference](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-flake.html).

По умолчанию intent содержит один **stopped** target с 2 vCPU, 4096 MiB RAM,
root 32 GiB и отдельным state 16 GiB; значения ресурсов задаёт private caller
после свежего admission. VM ID и MAC отличаются от всех production targets;
production image paths/hashes не наследуются. `initializeBlankStateDisk = false` по умолчанию.
Значение `true` разрешает форматирование только отдельно подтверждённого нового
пустого диска. После первого форматирования нужен образ со значением `false`.

Constructor не создаёт VM, не принимает существующий диск, не подписывает и
не переносит image, не запускает restore или службы. Generic production
Proxmox backend рассчитан на четыре production roles; этому target требуется
отдельный проверенный provider plan и backend. Перед загрузкой проверяются
подписи, QCOW SHA, ресурсы и маски `/dev/null` в построенном system closure;
после загрузки отдельно проверяются пустая БД, disk identity, восстановление
согласованного PostgreSQL/repository backup и runtime поведение. Eval или build
не означают научную либо service acceptance.

`tests/restore_site_eval.nix` — малые pure fixtures с injected конфигурацией,
без nixpkgs/download/build. Они проверяют свежий stopped target, исходные
closures, masks и явное разрешение форматирования. Реальный NixOS eval и boot
проверяются отдельно на pinned private site.
