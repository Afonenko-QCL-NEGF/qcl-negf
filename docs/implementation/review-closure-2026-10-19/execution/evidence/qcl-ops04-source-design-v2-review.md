# OPS04.S — независимый high review frozen D2

2026-10-19. **APPROVE для CP-DESIGN D2: блокирующих замечаний к готовому source-only контракту не найдено.** Это review проекта T1–T4, а не CP-CODE, исполнение fixtures, Nix evaluation, доказательство native imports или OPS04.N. Координатор отдельно принимает CP-DESIGN и назначает ограниченный I. Нового разрешения человека этот review не запрашивает.

Роль reviewer: назначенный Sol/high, независимый второй проход. Дочерних агентов нет. Разрешённый этап — чтение исходников и frozen design; продуктовые файлы не изменялись. Sole output — этот файл в `/tmp`. Imports/parsers/tests, Deno/Nix/Julia/build/install, network/SSH/server, secrets/private inventory, Git mutations, full CI и scientific submissions: **0**. Выполнялись shell text reads/searches, read-only Git metadata/show/diff и SHA256. Cumulative read/CPU/RAM/tool-output telemetry не инструментирована; порученные 30 min/1 CPU/2 GiB/read 5 MiB/report 96 KiB не выдаются за измеренную нагрузку. Отдельного доступного OPS04 read-ledger по просмотренному `/tmp/qcl-ops04*ledger*` / `/tmp/qcl-*read-ledger*` не обнаружено.

## 1. Identity и порядок независимой проверки

До чтения авторского D2 проверены root AGENTS/architecture, implementation entrypoint/canonical role policy, P1 PERM13/G1 и OPS04; затем primary source Git composition, solver/depot/assembler/Nix recipe, Platform protected file/trust/prefetch/cache, relevant test bodies/docs и selected Runner recipes. После этого прочитаны D2/identity/delta, затем original D/R и сопоставлены F1/F2. Первичный source assessment не начинался с готового диагноза reviewer D1.

Root checkout `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` имеет HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Начальный `git status --short` показал чужие изменённые Core/Runner/Results gitlinks и execution artifacts; они не правились. Выбранные `git ls-tree HEAD` revisions: Core `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`, Runner `9378396a3681c1eddf2c62f16674834fc4465583`, Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Наблюдаемые local candidates Core `e431609`, Runner `1acc165`, Results `33b1a39` их не заменяют. Runner `nix/package.nix` и `nix/julia.nix` прочитаны через `git show 9378396:...`.

Platform HEAD `b067723c82382689bff5cc366981c56e99b926f8` выбран root gitlink; повторный `status --short` пуст. Повторный `git diff HEAD --` для root `ops/{git,solver,application_cd}.ts`, `nix/solver.nix`, `flake.nix`, `tests/{solver,application_cd}_test.ts` пуст: прочитанные root sources соответствуют frozen HEAD. Это не утверждение о чистоте всего integration checkout или remote publication.

| Frozen artifact | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-ops04-source-design-v2.md` | `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147` |
| `/tmp/qcl-ops04-source-design-v2-identity.json` | `ad7bbfafe544dbc4b7fe0d07395a29e73ed5a83de9f30961fa8b659bde082e74` |
| `/tmp/qcl-ops04-source-design-v2-delta.json` | `25f577f4439a00e8f2dd2ace4f10a4a838640ff59dc3eaabfc3626a6d410bc82` |
| Original `/tmp/qcl-ops04-source-design.md` | `9c13f16187d0801dce35bebb55ed8aaeb332fba0594eed9ab0405cfc4162a355` |
| Original `/tmp/qcl-ops04-source-design-review.md` | `0d2c9f3eca0bc62c9c82af4918c1b562d5c10376a06cdffe3760e32ff7bdcf73` |

Дополнительные primary source file SHA256: `ops/solver.ts` `bc513f610cce976d108e17902ebd423c434992ba0edb91e2bdc3da2e5f3c247f`; `ops/application_cd.ts` `91989d0171e011f4518e178e247d4f7a466d08bd02b7931308a202c4354ee9ce`; `nix/solver.nix` `16c99da166ee2d9afc7d238fa317e43f0bcc71e2eccb8de3ff11e97b70aa858f`; Platform `ops/application_release.py` `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0`; `tests/test_node_enrollment.py` `134c4b5215827a55a0a90276b16ff74ebb34f075fbd0afbec089d7e2db6d0314`.

## 2. F1: consumed metadata identity — закрыто в D2, реализация ещё требуется

Primary source подтверждает сам gap независимо от D1: `ops/solver.ts::buildSolver:44–48` принимает `spec` и `target`; prefetch на `62–77` использует `spec.url/hash`, но build на `96–98` передаёт `realPath(target)`. `nix/solver.nix:6` читает этот path заново. `flake.nix::mkPreparedDepot:11–17` проверяет format/Julia/root revision/Manifest, а не полный components graph. Existing root tests используют `flake.nix` как `target` при fake callback и потому не устанавливают связь parsed spec ↔ consumed JSON.

D2 §5/T1 (`82–105`) определяет достаточную адресную коррекцию этой edge:

- Остаётся один metadata input — immutable JSON string. Старого object/path overload и позднего pathname read нет; deliberate unsafe legacy invocation обязан отвергаться до callback.
- CLI file читается один раз с bound 65536 UTF8 bytes, максимум 65537 read, fatal decode/roundtrip/BOM/raw-NUL checks и закрытием descriptor. Path/inode остаётся observation locator. Защита от malicious capture-path race, adversarial Git ABA или kernel-blocked I/O не заявлена.
- Helper сам проверяет input/type/размер/options, format/Julia/Manifest и полный derived `(path,revision,url)` graph до первого callback. Missing/extra/duplicate paths reject; object/list ordering не становится ложным mismatch.
- Один `JSON.parse→JSON.stringify` определяет **produced** bytes. Duplicate raw members получают единственный JS parse outcome до отправки Nix; raw capture digest/count отделены от normalized digest/count. Prefetch URL/hash и Nix JSON берутся из одного validated normalized value; operative scalars фиксируются до первого await/callback.
- `--argstr depotManifestJson BOUND_JSON --argstr depotManifestSha256 HEX` передают data через `Deno.Command` argv. Nix entrypoint проверяет `hashString` именно этого string перед `fromJSON`; `readFile target` и fallback удалены. JSON не превращается в shell/Nix expression. `mkPreparedDepot`/`mkSolver` и profile/worker guards остаются.
- D2 задаёт fixture A→B **после capture** как healthy freeze control: outgoing JSON/hash остаются A. Подмена до capture валидирует фактически captured B. B с неверным component graph reject; B с другим корректным URL/SRI при том же graph/Manifest consistently используется обоими consumers и не выдаётся за доказательство production archive origin.
- Test независимо хеширует actual outgoing JSON argument и сверяет argv SHA и возвращённое observation. Это различающий source fixture, не fake исполнение Nix parser/assertion.

Такой контракт закрывает именно первоначальный F1, без нового source lock/trust root/schema/release_id. Декларативный SHA двух переданных аргументов не назван proof доверенного producer: original depot generator/archive receipts остаются обязательными отдельными свидетельствами.

### Callers, CLI и границы argv

Поиск `buildSolver(` / `nix/solver.nix` / `depotManifest` на selected source нашёл два operational TS callers: `ops/solver.ts` и `ops/application_cd.ts`, плюс root solver fixtures. D2 обновляет их вместе. CLI syntax `solver.ts build DEPOT_JSON ...` и `application_cd.ts DEPOT_JSON MANIFEST_JSON [CACHE]` сохраняется. Exported helper является внутренним integration API; отказ от прежнего unchecked object/path signature явно описан, случайного совместимого обхода нет.

Application assembler должен capture+validate depot metadata **до** своего `.#application` build; последующий helper recheck использует captured string. Это необходимо, потому что нынешний `ops/application_cd.ts:69–79` сначала начинает application build. Предложенный fixture assembly-before-first-command конкретно проверяет этот порядок.

Отдельный `nix/local-lab-packages.nix:14–16` читает `input.depotManifest`, не вызывает `nix/solver.nix`. Его recipe и документированный `package-input.json` route не изменяются и не получают T1 exact-consumption claim. Прямых дополнительных callers старого `nix/solver.nix --argstr depotManifest` в выбранном коде/публичных operational docs не найдено. Это локальный source search, не гарантия отсутствия внешних private callers.

64 KiB относится к UTF8 **produced argument bytes**, а не JS code units; D2 отдельно ограничивает raw и produced size и не разрешает усечь данные. Один JSON arg плюс короткий SHA не представляет очевидного превышения обычного Linux per-argument limit для named x86_64-linux builder. Реальная exec/OS/environment compatibility и Nix `hashString/fromJSON` здесь не измерялись; D2 правильно оставляет Nix execution для отдельной admitted evaluation/native gate. Нельзя повышать размер или вводить temp-path fallback при будущем exec failure без review, поскольку fallback вернул бы закрытую edge.

## 3. F2: progressing short writes — закрыто в D2, source loop сохраняется

Primary `P/ops/application_release.py::freeze_ssh_trust:411–420` содержит write-all loop: positive `written` сдвигает `view`, zero/no-progress throws; file, directory и parent fsync предшествуют trusted return. Поэтому нормальные несколько положительных short writes, которые в сумме записали payload, должны завершаться успешно.

D2 §5/T3 (`124–130`) прямо задаёт healthy short-write positive с exact bytes/SHA/mode/fsync/closed descriptors и полный-write positive. Failure controls — zero/no-progress, в том числе после prefix, exception после incomplete prefix, либо file/dir/parent fsync failure — не возвращают trusted reference. Partial failed attempt сохраняется; новый cleanup/retry не вводится. Это устраняет неоднозначное D1 «partial/no-progress» без изменения корректного guard.

Existing `tests/test_node_enrollment.py::FakeProtectedFS`, `test_protected_ancestors_and_snapshot_have_independent_syscall_evidence` и `test_source_trust_substitution_does_not_change_late_transport_snapshot` действительно дают пригодную source fixture основу. Их реальные тела сейчас не покрывают весь новый FIFO/socket/0/1/65536/65537/short-write failure inventory. D2 сохраняет разницу между необходимым fixture addition и уже выполненным test pass; lock FIFO/application metadata cases не подменяют enrollment-reader coverage.

## 4. Остальной evidence/trust контракт подтверждён в пределах source

`ops/git.ts::sourceGraph:42–85` выводит состав из root HEAD gitlinks, проверяет root/child clean state, exact child HEAD, public GitHub URLs, complete `.gitmodules` и отсутствие nested submodules. Нынешний грязный checkout не годится для release build guard, но годится для audit выбранного immutable tree. Graph recheck до/после assembly обнаруживает обычный drift; adversarial ABA guarantee D2 не приписывает.

Цепочка D2 §§2–3 связывает конкретные вопросы с разными свидетельствами: derived graph/native locks → depot captured/normalized/archive bytes → resolved derivations/factory/phases → actual contents → observed origins/build transforms → exact native test contract. Она явно сохраняет следующие границы:

- Selected Runner `nix/package.nix` устанавливает source copies/offline instantiate/import/wrapper и plan installCheck; это не полная scientific suite. `nix/julia.nix` использует pinned upstream generic-bin factory и profile/worker policy; фактически resolved upstream phases, `doInstallCheck` и исходные execution receipts ещё нужны.
- Platform `nix/application.nix` выполняет version/import/factory checks четырёх Python packages и копирует owning frontend output. Version `0.2.0` сама по себе origin не подтверждает. Python `__file__`/distribution paths и Julia `pathof` должны быть observed в named output и сопоставлены selected commits/build transforms; scope ограничен перечисленными files/imports.
- Selected Portal `nix/frontend.nix` исключает `node_modules/dist`, берёт generated npm dependency hash и строит static output. Source/lock/hash/derivation/output/static inventory нужны совместно, stale assets или произвольный prebuilt dist не проходят только по version string.
- `deploymentManifest` использует существующий digest `JSON.stringify({sources,closures})`, exact two top outputs/narHash и прежнюю schema; route не меняет release_id. Sidecar observation не становится альтернативным release identity, подписью manifest, ручным revisions lock или новой orchestration системой.
- `P/prefetch_controller_closures:1059–1114` валидирует ровно application+solver paths/hashes, duplicate evidence и bounded local path-info до maintenance. Bad copy/hash не означает permission закрывать gate/останавливать services/drain. Private attempt/lock writes и readonly authority probes могут уже состояться. `path-info narHash` не назван reading всех payload bytes; top-only `verify-path` не назван recursive whole-closure proof.
- Engineering carryforward требует same resolved drv/output, verified contents, identical native test contract и original positive receipts. Same version/content/cached path не переносит изменённые factory/phases/profile/worker/suite acceptance; original producer/root/failed logs сохраняются. Reproducibility и full release нового root требуют собственных receipts/gates.

### Cache URI и frozen trust

Primary TS `.password` truthiness против Python `.password is not None` подтверждает конкретный empty-password discrepancy. T2 задаёт parity с отказом named/encoded/explicit-empty password до callback и сохранением SSH/ssh-ng username-only, local/Nix routes и single argv data. Нельзя нормализацией URL потерять raw explicit delimiter до проверки. T2 не превращается в blanket username/@ ban, query-secret detector или новую scheme/trust policy. Original URI должен оставаться одним argv element; secret-free published artifact policy проверяется без печати secret bytes. Данные о credentials не подставляются в digest/report.

`read_protected_file:362–384` проверяет root-owned namespace, owner/mode/type, O_NOFOLLOW всех opens и leaf O_NONBLOCK, читает не больше limit+1. FIFO/socket/directory отвергаются fstat до read; kernel-blocked I/O не обещано прерывать. `freeze_ssh_trust` создаёт unique protected snapshot и возвращает SHA/path после fsync. `ssh:1668–1671` и native Nix dispatch `2591–2597` используют один snapshot, а named source-substitution test проверяет поздние SSH **и** NIX_SSHOPTS. Это не защита от trusted-root post-freeze mutation и не свидетельство реально установленного host key/signature authority. `modules/cache.nix` хранит runtime signing key path вне store; наличие config не доказывает подпись/consumer trust. P1 PERM13 bounds сохранены, новый controller/cache root или rotation не разрешены.

## 5. Закрытие original review и дальнейшие gates

| Original замечание | Независимое сопоставление D1 → D2 с primary source | Решение |
| --- | --- | --- |
| F1: валидированный object не связан с path, заново читаемым Nix | D1 T1 валидировал spec; D2 удаляет dual input, определяет one capture/normalized bytes+SHA argv/Nix assertion, actual outgoing argument fixtures и caller ordering | Закрыто на design уровне; CP-CODE и Nix/native execution ещё впереди |
| F2: partial progress ошибочно смешан с write failure | D1 negative wording неоднозначно; D2 требует healthy progressing writes и отдельные zero/prefix-exception/fsync failures, source write-all сохраняется | Закрыто на design уровне; fixtures ещё не реализованы/не исполнены |

Дополнительных load-bearing design defects не найдено. Здесь нет основания расширять correction round на новый collector/framework, source lock, trust policy, scientific contract или native install. T4 как existing dossier table достаточно; предлагаемые comparison scenarios являются reviewer fixtures записей, не обязательным новым runtime validator.

Один Root Deno invocation T1+T2 и один Platform Python invocation T2+T3 остаются **будущими** targeted checks из remaining shared counters, с prepared environment, exact selector/source binding и own temporary directory. Этот review их не расходовал и не выдаёт новый grant. При отсутствии remaining slot/runtime сообщается blocked соответствующего runtime check; code/source review может продолжаться. Full suites/install/build/science здесь не разрешены. Nix entrypoint source review не заменяет его admitted Nix evaluation.

**OPS04.N = unknown.** Named trusted inventory/access/store/fresh admission, actual depot/output/derivation/import/signature/native-suite receipts отсутствуют. До них even read/verify/import/self-check не выполняется. Source self-check parser принимает schema/completed/scientific false; это engineering contract, а не scientific acceptance/import-origin proof. Будущий total wall≤300 s должен заранее включать cleanup reserve: existing inner timeout300+kill-after10 сам этого не гарантирует.

Без изменений остаются OPS03 cooperative Python owner boundary; OS/systemd/bootstrap provisioning writers вне него; prepare-initial protected-role residual; CR04 atomic effective admission commit/read; native proc/cgroup/Slurm/NFS/SQL/transport/VM/service/restore/backend gates. Новый root full acceptance/final CI/science не наследуются; G1 public release требует отдельного решения. Отсутствие admission блокирует зависимые native operations, а не этот ready source-design результат.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Selected Git tree остаётся composition authority | cfc38e1 HEAD gitlinks, `sourceGraph`, source hashes и пустой targeted diff | Local Core/Runner/Results candidates не выбраны; remote publication не проверена | сохранить |
| F1 имеет полный exact-consumption correction contract | D2 T1 one string, normalized UTF8 bytes/SHA, Nix assertion, named callers и A/B fixtures | Product fix и native assertion execution отсутствуют | изменить |
| F2 fixture oracle соответствует actual write-all loop | D2 T3 healthy progress vs zero/prefix exception/fsync failure | Fixtures пока proposed/unexecuted | изменить |
| Existing trust/password/transport semantics сохранены | TS/Python guards, protected reader/snapshot, SSH/NIX_SSHOPTS source и fixtures | Не secret scanner, не actual signature/host-key proof | сохранить |
| Reuse требует drv+contents+identical executed native contract | D2 evidence table и carryforward rules, primary recipe boundaries | Actual native/original test receipts отсутствуют | дополнительно измерить |
| OPS04.N/full release/native/science acceptance доказаны | Подтверждающих receipts нет | Missing inventory/admission; OPS03/CR04 residuals открыты | данных недостаточно |

**STOP. APPROVE source-design D2; передать координатору CP-DESIGN.** I/fixtures/native/Git publication не начинались и этим report не активируются.
