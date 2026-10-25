# DEV19 v2 — независимый narrow CP-DESIGN review

Вердикт: **PASS / DEV20 implementation READY в пределах описанного контракта**. Blocking R1 addressed; C2 отражён как точная fail-closed граница совместимости. Это приёмка проекта интерфейса, не реализации, native build или assets freshness текущего checkout.

Сначала прочитан actual v1→v2 delta, затем owning sections и author report. Owning source-first observations предыдущего review сохранены в `/tmp/qcl-dev19-design-review.md` (ca5725a645c58eb8cc35ce4ad299d183557dba32a940f722cb4bcc79dc41cd0d); глобальный source audit не повторялся.

## Binding

Portal baseline b9a876aa22d84dc13435bf970728b033d1345ba8. SHA-256 самостоятельно пересчитаны:

| Артефакт | SHA-256 |
| --- | --- |
| README.md | 31c3ca786384ad71d10db7c1cd1f88dd532e84fabddb95be79b65393a9a33938 |
| docs/package-identity.md | dbf2d4808a84cb97d1a656532aaf4c7271598195076ce084ca62d88a36e68cc9 |
| v1→v2 delta | b5539bf34daae37bf0cbdd7ebb636107cb0b7d52ff71afa1dabebaba02bb0509 |
| full v2 patch | 886aa4d37235ac2d1098a36d5d89ff06b8c3707f355f89b97cfa9799cd1e7199 |
| author report | c607313ccc0945675262af6709c2f0aa1f7f55b781e3ad6215ae05bb54f7f9a2 |

Оба actual owning файла byte-equal frozen v2 copies. Независимое применение unified delta в памяти с проверкой каждого old/context line к сохранённым v1 файлам воспроизводит оба actual v2 файла byte-exact. Full patch содержит только два заявленных docs paths.

## Spec/quality

- **R1 addressed**: docs/package-identity.md:91–97,181–188,205–223 требуют independent clean/recreate всего известного selected output до tsc/Vite. Literal token выбирает mode/root и прямо не выдаётся за интерпретацию TypeScript. Старые payload/stamp исчезают до compiler; zero-exit/no-output и вывод только в другом root не создают receipt. Missing/corrupt прежняя receipt не разрешает adoption; cleanup не зависит от её доверия.
- **Safety scoped**: :234–265 задаёт exact source-static/nix-dist paths, layout markers, lstat всех segments/tree, отказ на symlink/special/.git/device boundary до runner, исключительно generated ownership и сериализованный trusted tree. Nix frontend-only layout не требует Portal sibling и не удаляет его; произвольный effective outDir не очищается. Error cleanup ограничен собственным stamp. Это не защита от конкурентной подмены filesystem и не универсальная ownership attestation; ограничение явно сохранено.
- **Distinct controls**: :50–56,353–370 задают imported-only runner seam без CLI/env bypass; mandatory no-output/misdirected negative и fresh-output positive в обоих modes, empty-before-first-compiler observation, foreign sentinel и unsafe-symlink guard. Nix wheel verifier получает отдельную Portal fixture с исходным config и переносом только selected dist output. Существующие assets не подменяют новое свидетельство.
- **C2 addressed**: :111–123,368–370 прямо различают recursive Nix basename/cleanSourceFilter projection и полный hook inventory. Future omitted source row обязан дать inputs refusal; hook не исключает строку для pass. Compatibility ограничена текущим деревом плюс tool/отдельно проверенными будущими деревьями. Nix workflow/filter не меняется.
- **Границы сохранены**: :267–289 independent Python hook fail-closed; :28–34 receipt не объявлен builder подписью или byte verification dependencies; :372–386 native wheel/browser/offline/light/science отдельны. README описывает текущий existence-only guard и proposed implementation явно. Ни новая maintained SHA lock, ни stale stamp-only route не введены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 design предотвращает принятие старого selected payload после успешного no-output build | Exact cleanup/order и mandatory controls :205–265,353–370 | Реализация и controls не запускались | изменить |
| Nix projection mismatch не скрывается | :111–123 и missing-row negative :368–370 | Не универсальная совместимость будущих trees | сохранить |
| Medium DEV20 может реализовать этот интерфейс | Два exact docs, scoped runner seam, recipe/reset/schema/failure controls | CP-CODE и finite runtime evidence ещё нужны | изменить |
| Текущие assets/native wheel научно или продуктово приняты | Таких свидетельств здесь нет | Build/import/browser/full CI/science not_measured | данных недостаточно |

Reviewer не изменял owning source, не запускал helper, target imports, tests, Node, build, Nix, browser, solver, Git mutation или server. Выполнены только текстовое чтение, SHA-256 и in-memory patch reconstruction стандартной библиотекой Python. Новых blocking findings нет.
