# Локальный KVM lab: результаты и границы проверки

Срез: 2026-10-03 21:30 UTC / 2026-10-04 00:30 Minsk. Реальные VM проверки подтвердили platform
bootstrap, повторяемость конфигурации и отдельные свойства NFS/Slurm. Application05 и synthetic05
действительно собраны на хосте. Полная VM application/CD/solver приёмка остаётся открытой; научная
приёмка не выполнялась. Отчёт подготовлен чтением сохранённых receipts, без новых runtime/build/VM
действий.

## Исходники и область свидетельств

Root HEAD: `ed5ef3da49f18d67bbc0d3b21d36e7f232f940b0`. Локальные owning HEAD получены из Git; это
описательный срез, а не дополнительный release lock. Gitlinks остаются источником состава
опубликованного проекта и ещё не обновлены на эти локальные commits. Публикация и deployment
изменений не выполнены.

| Component  | Локальный HEAD                             |
| ---------- | ------------------------------------------ |
| QCLNEGF.jl | `aebe1812a2d66d933a3bc1584f65685c91fd93fc` |
| Runner     | `e57677c1a54b42b2905ceba6bb18fb9942b7bc22` |
| AiiDA      | `241c812f410fc90b4cbd6693405af5024aedd06b` |
| Contracts  | `026c122cd386752c0792727a75f86cdac25d2dd0` |
| Platform   | `066c6b1d8b86b18515db90efe57f633c2c3efc82` |
| Portal     | `779c5578f5c4a8dff7da986fbc9deba66e52baac` |
| Research   | `ab2d616f600981c112ba45658af490ba1ebcfb18` |
| Results    | `f50c35abfbf2706cd6809be1b3f9f3ba2f8adcd9` |

Platform integration receipt относится к Platform `785ca78c837fd027402171c223fa9adc3afd9782`;
read-only reboot и Slurm resource/cancel — к `482f7d13a811e85fc50d23a3ac15199d5738153e`; temporary
CD cleanup — к `066c6b1d8b86b18515db90efe57f633c2c3efc82`. Более новый checkout не переносит старое
VM свидетельство на новый код. Snapshot04: `387917ff437e20978b506373aa3320fcda85706e`; snapshot05:
`8a1d3921bec50c470c86546dc71de02cea829f3b`. Development snapshots не заменяют release integrity или
научную приёмку.

## Реальные проверки и незавершённые этапы

- Созданы четыре роли: control, storage и два worker. Повторный actual OpenTofu apply и проверка
  после reboot показали `No changes`. Повторный Ansible bootstrap завершился с `changed=0`,
  `failed=0`, `unreachable=0` для всех ролей. Строгий SSH, ownership admission, NFS `root_squash` и
  запись сервисного UID проверены platform probes.
- После reboot контроллера сохранённый read-only producer прочитал существующие state/NFS markers до
  новых writable probes. Сравнены содержимое, SHA-256, inode, размер, mtime/ctime и UID/GID. Это
  сохранность тестовых файлов при reboot; согласованный PostgreSQL/AiiDA repository backup restore
  не измерен.
- В Slurm batch job измерены affinity на один CPU и `memory.max=134217728` bytes на ограничивающих
  уровнях cgroup. Собственное задание прошло `RUNNING`→`CANCELLED`. Намеренный OOM и host contention
  не проверены. Предыдущий `srun` был `TIMEOUT`; исправление callback range ещё требует actual
  `srun` подтверждения.
- Application05: actual build `exit_code=0`, 46.33 s; installed integrity check также `exit_code=0`.
  NAR: `sha256-S1LAvy3rG1cXI1j8h+xzo6rxQXwyMQJUgBaZsMNP2bE=`.
- Synthetic05: actual build/installed CLI integrity `exit_code=0`, 14.67 s; проверены immutable
  binding, closure references, wrapper и installed help. NAR:
  `sha256-4n7HZKfhFZS3xkDdVgrNgZcBXFxGL56ucU7HkPIoBjA=`. Client cgroup: RAM 1 GiB, swap 0, CPU quota
  одного ядра; peak 211427328 bytes. Nix daemon builders находятся вне этого cgroup. Producer05,
  Slurm/AiiDA profile и solver не запускались. Оба package receipts имеют
  `scientific_accepted=false`. Совпадение fixture bytes04/05 не переносит старое host process
  evidence04 на05.
- Public constructor [`local-lab-systems.nix`](../../nix/local-lab-systems.nix) прошёл actual
  eval04: `rc=0`, 186.72 s, четыре output paths совпали с ранее зарегистрированными role
  derivations. Неверные prepared Manifest/depot graph при storage-only selection отклонены
  ожидаемыми assertions (`rc=1`). Прямой JSON текущих role derivations — `not_measured` из-за Nix
  coercion attrsets с `outPath` в строки. Проверка не была новой role build/activation.
- Julia04 ещё проходит upstream installCheck. Попытка03 завершилась timeout; попытка04 имеет
  конечный client timeout 10800 s, наблюдались два Julia worker, перед запуском проверялось наличие
  свободной host RAM. `JULIA_CPU_THREADS=2` ограничивает первоначальный launcher pool, а не общий
  CPU/RAM всех вложенных upstream Distributed workers. Solver05 имеет только evaluation derivation;
  его успешная build/runtime проверка отсутствует.
- Temporary CD cleanup восстановил исходные `authorized_keys` по SHA-256 на control и обоих workers,
  удалил собственные runtime-каталоги и временный controller config; admin SSH проверен. Storage не
  входил в этот cleanup. Полный CD deployment/rollback этим receipt не доказан.

Первый application import в guest отклонён штатной signature guard. Постоянное добавление публичного
signing key в root Nix configuration четырёх VM ожидает прямого подтверждения пользователя после
отказа автоматической проверки разрешений. Обход не выполнялся; `require-sigs` и `trusted-users` не
ослаблены. Application profiles, AiiDA bootstrap и admission gate ещё не активированы.

Quota fixture остановился на default signature verification: 17 существующих guest closure
dependencies оказались untrusted. Coordinator вернул ошибку до запуска fixture producer;
image/loop/mount не создавались. Block/inode `EDQUOT`, NFS quotas и concurrent writers —
`not_measured`. Сохранённая host metadata содержит официальные подписи для всех 18 paths; её наличие
не заменяет guest verification. Portal export accounting и Runner recovery retention имеют отдельные
локальные regression проверки. Это partial guards; общий бюджет scratch/logs/staging/ первого AiiDA
sandbox retrieval не обеспечен. Full AC2 path split и OS quotas остаются proposal в
[storage-budget-transition.md](storage-budget-transition.md). Финальные научные данные нельзя
удалять ради operational budget.

## Очистка Git и перенос исходников

Лишний объём удерживали два служебных Codex diff refs с научными blobs и локальное копирование
лишних Git objects. Source snapshots являются clones, а не worktrees; для новых snapshots
используется `git clone --no-local`. После подтверждённого пользователем внешнего переноса results
удалены лишний recovery archive, старый temporary garbage и ровно два служебных diff refs. Ordinary
refs/reflogs/index/ status и identities сохранённых snapshots проверены cleanup receipt.
Зафиксированный после очистки срез: root `.git` около 8.3 MiB, `.build` около 3.4 GiB; последующие
сборки меняют `.build`. Внешняя копия results независимо побайтово не проверялась. Переносимый
source handoff пока подготавливается: успешный replay и archive SHA в этом срезе не
засвидетельствованы.

## Первичные receipts

Пути отсчитываются от root checkout. Артефакты остаются в игнорируемой `.build`; их отсутствие в
опубликованном checkout означает отсутствие свидетельства. Bound leaves platform/reboot/Slurm/API и
stdout/stderr сборок05 проверены по SHA-256. Исторический
[recovery-cd-local-validation.md](recovery-cd-local-validation.md) и старые архивы не переписаны.

| ID  | Artifact                                                               | SHA-256                                                            |
| --- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| R01 | `.build/git-object-recovery/20261003/hard-cleanup-proof.json`          | `579875d349f8dd9db1eaf4df9ae2af7fbeb1b16d55bc7c1501dd4b66e1982cea` |
| R02 | `.build/local-lab/evidence/platform-integration-proof.json`            | `64e74b7513e8e34c95567628b81fd16747f6accd7512b4b647b36aca0e8370e0` |
| R03 | `.build/local-lab/evidence/terraform-idempotence.json`                 | `6e5d082d452cf25109f77d2c778a8da81f19f4ce496ec9a1115ad590cffd5a69` |
| R04 | `.build/local-lab/evidence/repeat-bootstrap-proof.json`                | `f1fa1e041036fc1946f59cdd44f106fbd12c0ec12a0449087b8a12040858eb26` |
| R05 | `.build/local-lab/evidence/read-only-reboot-02/proof.json`             | `ddeafc7e6204b0ddf21756e54c4c4cfbdbfa5b676a25edfe5ed4700fdab97f90` |
| R06 | `.build/local-lab/evidence/slurm-resource-cancel-02/proof.json`        | `c7ec187b9124886bb61eccf183a1c39864498698ecb3be90df8fd25d604ee474` |
| R07 | `.build/local-lab/evidence/tofu-after-reboot-sealed-proof.json`        | `f4a14a9fd3d08fb58ff6140f498ce611e9afe60f6b957cf24296803997c93ef7` |
| R08 | `.build/local-lab/private/package-05/application-build-attempt-1.json` | `02d2b0fc6cf65cc07e2cbe8e7106696c80a9dbd9b8b406485d0c5cfa986e7f99` |
| R09 | `.build/local-lab/private/package-05/synthetic-build-attempt-1.json`   | `cd2da3ccada8e40bcb705176eae542f8601afea7d56828997ce44ad168a04345` |
| R10 | `.build/local-lab/evidence/public-systems-api/proof.json`              | `92e6313d1cb1d60fd5beb234dc8b0aec66ae9c307164a03ae547e4a1c6e62936` |
| R11 | `.build/local-lab/evidence/quota-fixture-20261003-01/result.json`      | `e34598299362c9815c529e86d0d93642ba7ffea6cac556df6236a7b3933b2bb1` |
| R12 | `.build/local-lab/evidence/quota-fixture-20261003-01/commands.jsonl`   | `e19d29075d7307ab87bc32ccc05428ca6dced69fdae68021fbd59d840e32e3a2` |
| R13 | `.build/local-lab/evidence/temporary-cd-cleanup-02/proof.json`         | `c4678cee42959fa98c716b42ed20ce5788419f9055c51261547e3725f09d3ae9` |
| R14 | `.build/local-lab/evidence/temporary-cd-cleanup-02/seal.json`          | `ab268a164cd0b04d63c8c7f8dc2b21d7ecebf6b3fa5dea748eaedbb6e177dd9c` |

## Решения по свидетельствам

| Утверждение                                             | Свидетельство                                         | Ограничение                                                                                    | Решение                |
| ------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------- |
| Owned platform развёрнут и повторяем                    | R02–R04, R07                                          | Старые проверенные Platform ревизии; application runtime открыт                                | Сохранить              |
| State/NFS markers пережили reboot                       | R05; source producer и файловые атрибуты              | DB/repository backup restore не измерен                                                        | Дополнительно измерить |
| Slurm batch ограничен и отменяется                      | R06; affinity, memory.max, RUNNING→CANCELLED          | OOM, host contention и исправленный srun не проверены                                          | Дополнительно измерить |
| Application05 и synthetic05 собраны                     | R08–R09; integrity и NAR hashes                       | Host package/CLI scope; profile/producer/science не выполнялись                                | Сохранить              |
| Public API сохраняет output paths и storage-only guards | R10; eval04 и отрицательные selections                | Current drv JSON, новая build/activation не измерены                                           | Сохранить              |
| Solver готов к VM приёмке                               | Julia04 installCheck идёт; solver05 только evaluation | Нет завершённой solver05 build/runtime evidence                                                | Данных недостаточно    |
| Full AC2 disk budget обеспечен                          | R11–R12; partial guards и storage proposal            | EDQUOT/NFS не измерены; path split/OS quotas не реализованы                                    | Изменить               |
| Temporary CD доступ очищен                              | R13–R14; SHA-256 и admin SSH                          | Три VM роли/controller config; полный CD не проверен                                           | Сохранить              |
| Лишние Git objects очищены, source identities сохранены | R01                                                   | Внешняя копия results независимо не хэшировалась                                               | Сохранить              |
| Получена научно принятая QCL-NEGF модель                | scientific_accepted=false / science not_performed     | В этом VM этапе SCBA/Poisson, физические, сеточные и экспериментальные проверки не выполнялись | Данных недостаточно    |
