# OPS04.S: независимый high CP-DESIGN source review

2026-10-19. **REQUEST_CHANGES — два узких уточнения ready implementation contract (F1/F2 ниже).** Evidence/carryforward/trust модель и T2 в целом подтверждены primary source; scientific/native contract не требуется переоткрывать. OPS04.N остаётся unknown. Ни imports/parsers/tests/Deno/Nix/Julia/build/install/network/server/SSH/Git mutations, ни children не выполнялись. Единственная запись — этот report. Счётчики и grants не сброшены/не увеличены.

## Identity / порядок чтения

| Frozen artifact / source | SHA256 |
| --- | --- |
| `/tmp/qcl-ops04-source-design.md` | `9c13f16187d0801dce35bebb55ed8aaeb332fba0594eed9ab0405cfc4162a355` |
| `/tmp/qcl-ops04-source-design-identity.json` | `7ddbbe1cd0174aca0c248d3807e9e47a9c7f6b8cc0cf6c38e42fc53459bbd291` |
| Root `ops/solver.ts` at cfc38e1 | `bc513f610cce976d108e17902ebd423c434992ba0edb91e2bdc3da2e5f3c247f` |
| Root `ops/application_cd.ts` at cfc38e1 | `91989d0171e011f4518e178e247d4f7a466d08bd02b7931308a202c4354ee9ce` |
| Root `nix/solver.nix` at cfc38e1 | `16c99da166ee2d9afc7d238fa317e43f0bcc71e2eccb8de3ff11e97b70aa858f` |

Primary refs: Root `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; selected Runner `9378396a3681c1eddf2c62f16674834fc4465583`. Root/Platform files читались из exact Git trees, включая `ops/git.ts`, solver/application assembler/nix entrypoints, root flake/depot/tests, Platform protected readers/trust snapshot/prefetch/cache/test bodies/docs и selected Runner Julia/package recipes. Затем прочитаны авторские §§1–9. Current local component heads не использованы как замена selected source.

Actual root HEAD всё ещё cfc38e1; status dirty чужими Core/Runner/Results gitlink candidates и execution evidence. Recursive observed Coree431609/Runner1acc165/Results33b1a39 отличаются от committed gitlinks Core7324d98/Runner9378396/Resultse2fdeda. Platform clean selected b067723. Этот tuple не объявлен clean final candidate или release-ready. Source audit не проверял remote publication.

## F1 — P2: T1 валидирует metadata object, но не задаёт binding к metadata bytes, которые потребляет Nix

**Design locator:** §5/T1 (строки80–90): pure validator `(spec, expectedGraph, expectedJuliaManifestSha256)`, оба CLI consumers вызывают его до prefetch/build. **Primary source locators:** `ops/solver.ts::buildSolver:44–48` принимает два независимых inputs `spec` и `target`; file prefetch использует spec.url/hash на62–77; Nix получает `Deno.realPath(target)` на96–98. `nix/solver.nix:6` заново читает JSON из переданного path. Root `flake.nix::mkPreparedDepot:11–17` сверяет format/Julia/root revision/Manifest, но не полный components graph.

Заявленная T1 цель — до native command отвергнуть неполный/ложный stored graph даже при том же root revision. Проверки только `spec` недостаточно для этого consumed-input claim: programmatic caller может передать правильный spec, но target JSON с иным components entry/URL/hash. Даже без конкурентной/злонамеренной подмены это разные аргументы существующего exported helper. Для обычных CLI остаётся отдельный поздний pathname read после первого parse/prefetch. Валидированный object не устанавливает identity этого второго чтения.

Самый дешёвый различающий source fixture: создать A — valid generated-shaped metadata; B — JSON с тем же root revision/Julia/Manifest, но ложным component entry; передать spec=A, target=B и fake execute callback. Pure T1 validator A пройдёт, Nix scheduled с B; same revision/flakes guards не отвергнут именно неправильный полный graph. Existing solver tests используют в target вообще `flake.nix` при fake commands, поэтому не являются positive fixture связи validated JSON↔consumed JSON. Дополнительный negative — изменение target между validation и последующим build scheduling; никакого реального Nix для fixtures не требуется.

**Минимальное уточнение T1:** зафиксировать один authoritative metadata input и exact bytes/hash, к которым привязаны и validation/prefetch, и последующий Nix read. Если object/path interface сохраняется, их соответствие не может оставаться caller convention. Допустим owned frozen input/snapshot либо другой bounded способ передать именно validated bytes; выбрать owning paths и receipt locator перед I. Не требуется новый global lock, trust root, depot schema или release_id algorithm. Проверить mismatch object/path и substitution control fake callback-ами; healthy generated JSON/prefetch/build должны использовать тот же bound input. Сохранить current clean sourceGraph и Nix native guards.

Это замечание о новой заявленной exact provenance correction, а не доказанный exploit solver/model и не требование adversarial Git ABA protection. В design уже честно ограничена атомарность sourceGraph; такое ограничение не должно неявно закрывать иной spec→file edge. Native receipts сами по себе позднее не делают ошибочно валидированные bytes правильными.

## F2 — P2: T3 не различает допустимые progressing short writes и отказ неполной snapshot записи

**Design locator:** T3 negative inventory: «partial/no-progress snapshot write … не выдаёт trusted snapshot». **Primary locator:** Platform `freeze_ssh_trust:411–415` использует `while view`, принимает положительный short write, сдвигает view и продолжает; `written<=0` бросает OSError. После полной записи делает fsync файла, directory и parent, лишь затем возвращает snapshot reference.

Положительный partial write сам по себе не failure. Если test по literal negative требованию вернёт несколько положительных коротких chunks и затем завершит запись, текущая корректная реализация должна успешно вернуть exact snapshot. Нельзя ради такого control ломать write-all loop или тратить future single invocation на известный false-red. Поведение обычных fragmented reads в T3 positive не определяет write-side case.

**Минимальное уточнение T3:** progressing short writes, которые в сумме записали все bytes, — healthy positive с exact bytes/SHA/mode/fsync/closed-descriptor assertions. Negative — zero/no-progress, exception после prefix/incomplete write либо fsync failure; trusted return/reference при таком incomplete/failure исходе запрещён, unknown partial attempt сохраняется по прежней policy. Source guard менять не нужно. Это точность fixture oracle, без изменения trust boundary или public semantics.

Если «partial» автор намеревался использовать как shorthand «partial then failure», это следует зафиксировать явно до передачи medium I. В frozen тексте такого различия нет, и primary code прямо показывает оба разных исхода.

## Подтверждённая часть дизайна

### Source → depot → derivation → contents/imports

- `sourceGraph` действительно использует root HEAD gitlinks, clean root/children, exact checked-out child revisions, complete .gitmodules и отсутствие nested gitlinks. Index/версии0.2.0/current local candidate не заменяют authority. Assembly before/after graph checks обнаруживают обычный drift; design не утверждает atomic/adversarial ABA guarantee.
- Depot generator сохраняет full derived graph, Julia1.13.0, Manifest SHA и archive SRI. Archive sorted/mtime/ownership normalization — рецепт, не выполненный build. Hash-prefetch local file name совпадает с fetchurl output name; rejection останавливает build. T1 мотивирован реальным revision-only consumer check, но требует F1 consumed-bytes clarification.
- Root/Runner Nix recipes фиксируют selected core/runner/environment, Julia factory/version/hash/profile/worker arguments и install checks. `Pkg.instantiate` offline и `using QCLNEGFRunner` остаются реальными build/import effects, не source-only proof и не скрытая scientific suite. Resolved upstream factory/phases/doInstallCheck и original execution receipts нужны отдельно; selected profile нельзя подменять package version.
- Application imports/factories в Platform install phase и Python version equality не подтверждают module commit origin. Предложенные observed __file__/pathof/origin bytes, installed transforms, active Project/Manifest/depot/sysimage и wrapper checks корректно локализуют scope перечисленных modules. Не заявляется полнота всех possible imports.
- Portal frontend source/lock/generated npm hash, derivation/output/NAR и installed static inventory образуют нужную отдельную цепочку. Произвольный prebuilt dist/сохранённая версия0.2.0 не принимаются вместо неё.
- Две top-output narHash/локальный path-info не названы recursive bytes verification. Реальная store verification сохраняет actual paths/count/bounds/scope, corruption blocks imports/reuse. Новый recursive verify или rebuild здесь не разрешены.

### Carryforward и новый full release

§§3.1–3.2 правильно требуют same resolved drv/output, verified contents, identical native test contract и original positive receipt. Contract включает source/factory/patch/phases/profile/worker/env/selected suite/exclusions; одинаковые bytes или version не переносят proof изменённого test contract. Cached path/prefetch не доказывают rebuild reproducibility.

Original producer/root и failed logs не переписываются. Новый root может сослаться на unchanged native output только с отдельным comparison receipt и сохранённой source distinction. Full-release нового head требует final source freeze/published owning refs/gitlinks и всех необходимых native/backend/restore/sole-final-CI/scientific gates. Это не наследуется от старого green. Derived evidence sidecar — observation dossier, не параллельный revisions registry или новый admission service.

### Existing cache URI/trust policy и T2

TS `.password` truthiness и Python `.password is not None` действительно различаются для explicit empty password delimiter; T2 имеет конкретную source-причину. Existing policy запрещает password/argument hazards, не все username characters. Nix SSH route содержит account username, поэтому blanket username/@ ban был бы неверен. Depot generation HTTP(S) policy — отдельная граница и не переносится на Nix cache URI.

T2 сохраняет username-only SSH/ssh-ng и существующие local/Nix URI forms, original URI одним argv element, normal Nix signature/trust checks, cache mirror вне release_id. Никакой новой scheme policy, query-secret scanner, key rotation или trust root не вводится. Требуемая TS/Python literal parity должна проверять raw explicit delimiter до потери этой информации при URL normalization; positive username-only и допустимые local forms сохраняются. Source design не обещает универсально распознать arbitrary secret в username/query.

`prefetch_controller_closures` требует ровно application+solver paths/hashes, validates before maintenance, bounded path-info evidence и exact hashes. Readonly authority probes/private attempt/lock writes могут быть раньше; design это честно указывает. Failed copy/malformed evidence/hash mismatch не становятся разрешением gate/service/fleet mutation. Existing source fakes показывают эту ordering policy, не native signature acceptance.

### Protected readers и frozen SSH trust

Primary `protected_directory/read_protected_file` действительно проверяет root-owned namespace/regular leaf, отсутствие group/other write, nofollow ancestors/leaf, O_NONBLOCK leaf и read≤limit+1. FIFO type отвергается до read; hard interruption blocked kernel I/O не обещается. Existing FakeProtectedFS — независимые синтетические syscall/inode facts, не признание /tmp protected production namespace.

T3 расширение exact0/1/65536/65537 bytes, FIFO/socket/directory-before-read, flags/descriptors/ownership/invalid paths и snapshot failures обосновано реальным coverage gap. Application-budget/lock FIFO tests не заменяют enrollment-file evidence. Source-only test stage не получает право изменять trusted config или реальные FIFO/native namespace. F2 уточняет только write oracle.

Existing read→freeze→late transport source и selected substitution fixture связывают SHA frozen bytes и snapshot path с SSH **и** NIX_SSHOPTS; исходный known_hosts позднее не перечитывается. Trusted root/operator mutation, hardware attestation или новая enrollment authority не обещаются. Cache signer config не выдаётся за доказательство подписанной closure или consumer trust.

## Gates, budgets и сохранённые residuals

T1+T2 Root fixtures объединены в один existing admitted Deno slot, Platform T2+T3 в один existing admitted Python slot; fake command/syscall tests не вызывают native/scientific runtime. Указанные120s/60s и CPU/RAM/output — proposed stage bounds в рамках remaining shared counters, а не новый grant этим review. При exhausted counter runtime остаётся blocked, no auto-rerun/full suites.

OPS04.N unknown: trusted inventory/access, named store/fresh admission, native contents/imports/original test receipts не представлены. Even native read/verify/self-check не исполнены и требуют конкретного bounded stage. Self-check остаётся engineering Hilbert/HDF transport oracle без scientific_accepted; selected Platform parser проверяет три receipt fields, не import origins/full numeric contract. Предложенный outer total wall≤300s с cleanup reserve честно учитывает, что existing inner timeout300+kill-after10 сам не даёт total≤300 guarantee.

Сохраняются без закрытия: OPS03 cooperative Python process-local authority; OS/systemd/bootstrap/provisioning writers вне owner; prepare-initial protected-role gap; CR04 atomic effective admission commit/read; native Slurm/NFS/proc/cgroup/SQL/VM/service/restore/backend и final CI/science gates. Store hashes и этот source-design review не устраняют их. Public release отдельный G1 gate; никаких серверных действий или повторных human approvals reviewer не запрашивает.

## Решение / STOP

Основная архитектура evidence contract, reuse/native/full-release separation и existing trust policy пригодны. **До CP-DESIGN READY для T1–T3 нужны только два коллированных уточнения:** authoritative consumed depot metadata bytes и short-write positive/failure distinction. Они не требуют scientific/CSP/new trust decision, но должны стать явным frozen implementation contract и fixture expectations. Reviewer исходный дизайн не редактировал и implementation не начинал.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact Git-derived source остаётся authority | selected ops/git.ts и frozen root tree | Dirty local candidates/remote/native proof отдельны | сохранить |
| T1 полностью связывает validated depot metadata с Nix input | spec/target split, nix readFile и proposed validator | F1 consumed-bytes edge не определён | изменить |
| T2 выравнивает existing password policy без username ban | TS/Python guards и actual SSH routes | Не secret scanner/новая trust policy | сохранить |
| T3 fixtures отражают reader/snapshot contract | Actual bounded reader + write-all loop | F2 partial progress vs failure смешаны | изменить |
| Carryforward требует drv+contents+identical native contract | §§3–6 evidence/receipt matrix | Actual native receipts отсутствуют | дополнительно измерить |
| OPS04.N/new full release/native/science ready | Подтверждающих измерений нет | Inventory/admission absent; OPS03/CR04 residuals открыты | данных недостаточно |

**STOP.** REQUEST_CHANGES ограничен F1/F2 source-design precision. No execution/import/test/network/server/Git mutation/children; sole output этот report.
