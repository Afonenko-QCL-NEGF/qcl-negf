# I02/GAP04: local management и граница Root CI

Source prepared; local YAML structure / targeted TypeScript format / type checks passed. Selected
Root entry: `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`. Gitlinks остаются authoritative; Platform
gitlink этого entry — `4ce214e29b72276157b10a9267e2f30fef4ac66f`. Это binding исходного состава, не
приёмка текущего Platform candidate.

Изменены только `.github/workflows/release.yml`, comment в `ops/application_cd.ts`, historical
notice в `cr03-root-enrollment-caller.md` и эта note. Manual-only workflow содержит только assemble.
Delivery input/job/SSH/environment/target vars удалены; CI больше не требует cache URI и передаёт
assembler ровно DEPOT_JSON MANIFEST_JSON. Pinned checkout/upload, locked prepare/check/test, Runner
JULIA/bootstrap, package retention, solver depot identity, source graph и immutable manifest
contract сохранены.

Assembler сохраняет optional cache argument, conditional local nix copy, NarHashes, release
identity, sourceGraph before/after, exclusive pending file и atomic rename. Manifest upload не
содержит store closures и не доказывает ready recipient import. Trusted local signing/cache
publication/import и whole-cluster update принадлежат существующему local Platform controller под
local operator authority.

Platform final independently accepted high review ещё pending: complete enrollment, manual
upper-workflow/retry/Slurm cancellation, closed admission/all-worker execution barrier, one
release/final health, current registration и fail-closed unknown semantics остаются prerequisite
эксплуатации. Root gitlink/publication ждут принятого Platform source. Native
delivery/bootstrap/reboot/final CI/science этим изменением не приняты.

Finite local source packet: один вызов ≤60s, 1CPU/1GiB target, combined output128KiB, own temp8MiB.
Cached YAML BaseLoader structure assertions, targeted Deno fmt/check `ops/application_cd.ts` и doc
format; без targeted runtime tests (TS comment-only). Документация форматируется в этом же packet;
original receipt сохранён. Новые builds/CI/install/network, GitHub writes/SSH/Nix/application_cd
main/SCI не выполняются.

Credential provenance — Root administrative observation: secrets/variables read HTTP403;
environment/deploy-key list count0 не устанавливает полноту grants/keys/secrets/vars. Source удаляет
использование credential bridge в selected workflow, не отзывает существующие credentials. Actual
existence/revocation unknown; revoke0 этого scope. Private inventory/targets/secrets не входят в
note.

| Утверждение                                                      | Свидетельство                                                | Ограничение                                                  | Решение                |
| ---------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| Selected workflow только assemble, без delivery/cache obligation | Exact four-path diff; YAML structure packet passed           | Не аудит account grants/других workflows                     | изменить               |
| Manifest/application/solver identity API сохранён                | application_cd.ts comment-only diff, optional cache retained | Native build/import не выполнялись                           | сохранить              |
| Historical CR03 caller retired, Platform guards локальны         | Notice и unchanged selected Platform gitlink                 | Старые34 cases не whole I14 evidence; final Platform pending | сохранить              |
| Actual credentials отозваны/отсутствуют                          | Root HTTP403 observation, list count0                        | Read access incomplete; revoke0                              | данных недостаточно    |
| Local delivery/native/final CI/science приняты                   | Native/GitHub writes/scientific0                             | Platform high review и native gates pending                  | дополнительно измерить |
