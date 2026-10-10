# I02/GAP04: local management и граница Root CI

Source prepared; local YAML structure / targeted TypeScript format / type checks passed. Selected
Root entry: `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`. Gitlinks остаются authoritative; Platform
gitlink этого entry — `4ce214e29b72276157b10a9267e2f30fef4ac66f`. Это binding исходного состава, не
приёмка текущего Platform candidate.

Разделение CI изменяет `.github/workflows/release.yml`, comment в `ops/application_cd.ts`,
historical notice в `cr03-root-enrollment-caller.md` и эту note. Последующая интеграция обновляет
Platform gitlink на опубликованный `fe8e2de649e13def69c723eed3917ae575d9b54f`. Manual-only workflow
содержит только assemble. Delivery input/job/SSH/environment/target vars удалены; CI больше не
требует cache URI и передаёт assembler ровно DEPOT_JSON MANIFEST_JSON. Pinned checkout/upload,
locked prepare/check/test, Runner JULIA/bootstrap, package retention, solver depot identity, source
graph и immutable manifest contract сохранены.

Assembler сохраняет optional cache argument, conditional local nix copy, NarHashes, release
identity, sourceGraph before/after, exclusive pending file и atomic rename. Manifest upload не
содержит store closures и не доказывает ready recipient import. Trusted local signing/cache
publication/import и whole-cluster update принадлежат существующему local Platform controller под
local operator authority.

Platform source опубликован и слит в
[PR #10](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/10). Полный локальный
`test_application_release.py`: 105 tests, `OK`, exit 0, 18.696s. Независимая проверка подтвердила
полный набор selectors и совпадение семи source files до/после запуска и в опубликованном дереве
`000f0ca99f365368dd64ed0930ada6a1a2c78b40`. SHA256 исходного лога:
`f605d20e8a57ea9a4815a3ab98f5b4ca1feac269e037f02ea8c344b9d7211d7a`.

Complete enrollment, manual upper-workflow/retry/Slurm cancellation, closed admission/all-worker
execution barrier, one release/final health, current registration и fail-closed unknown semantics
проверены на локальных fixtures. Перед эксплуатацией нужны отдельные installed-cluster проверки.
Native delivery/bootstrap/reboot/final CI/science этим изменением не приняты.

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

| Утверждение                                                      | Свидетельство                                                | Ограничение                                                     | Решение                |
| ---------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- | ---------------------- |
| Selected workflow только assemble, без delivery/cache obligation | Exact four-path diff; YAML structure packet passed           | Не аудит account grants/других workflows                        | изменить               |
| Manifest/application/solver identity API сохранён                | application_cd.ts comment-only diff, optional cache retained | Native build/import не выполнялись                              | сохранить              |
| Historical CR03 caller retired, Platform guards локальны         | Notice; Platform PR #10, whole105/OK и проверенное дерево    | Старые34 cases не whole I14 evidence; installed cluster pending | сохранить              |
| Actual credentials отозваны/отсутствуют                          | Root HTTP403 observation, list count0                        | Read access incomplete; revoke0                                 | данных недостаточно    |
| Local delivery/native/final CI/science приняты                   | Local105 passed; native/scientific/final CI0                 | Native gates pending; публикация source не deploy               | дополнительно измерить |
