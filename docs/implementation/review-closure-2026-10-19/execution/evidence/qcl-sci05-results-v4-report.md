# SCI05-N1 Results v4 — F1 correction и explicit actual-producer control

2026-10-19. F1 correction сохранена в v3, после её freeze координатор прямо
поручил добавить отдельный positive transport control внутри будущего call8.
V4 добавляет только этот owning test; production native.py/state.py byte-exact
совпадают с v3. Ни нового production corrective loop, ни исполнения здесь нет.
Independent CPP/runtime/scientific PASS автором не заявляются.

## F1 и сохранённые freeze

F1 review SHA256 `9ae7330b6a4ba3bdf5f7ffd358a976be48b36037fa37a1319e93efce6335e6b0`;
E2 scope/production correction/controls подробно зафиксированы в
`/tmp/qcl-sci05-results-v3-report.md`. Present analysis record теперь требует
собственную native point identity exact actual commit identity на том же handle;
absent-copy/recovery policy сохранена. V4 эту correction не меняет.

Все v3 raw artifacts проверены byte-exact:

| Artifact | SHA256 |
| --- | --- |
| /tmp/qcl-sci05-results-v3-report.md | d313606547313efe81e0f92fcbcb98870f5953101f422e00c8056d2a5614e9b8 |
| /tmp/qcl-sci05-results-v3-identity.json | a8eae785481379d1763439e2ab6c5426970b46e8380e084a2778edd42a6dc1fd |
| /tmp/qcl-sci05-results-v3-patch.diff | c6b9a9cf45ae0cfbc284de64ddc82cb1eae32567ddec5f30406a3594636a67e3 |

V2 и первоначальные artifacts также не перезаписывались. Worktree остаётся
`/tmp/qcl-sci05-results-worktree`, branch
`codex/review-closure-final-audit-reader`, HEAD/base e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae.

## Новый actual producer control

Первичный прочитанный Runner source:
`/tmp/qcl-sci05-runner-worktree/test/infrastructure/final_fixed_point_audit.jl`,
SHA256 `2deeff785cc09ee724dbbaffd0d99693178483c90b7b5685eefe47bbcc773e8b`.
Прочитаны native_roundtrip и owning commit_point_artifacts archive-root/identity
paths. Никакой Julia fixture не создавался и не читался в этом поручении.

`test_actual_runner_producer_transport_when_explicitly_bound`:

- При отсутствующем `QCL_SCI05_RUNNER_FIXTURE_ROOT` выдаёт explicit
  `not_run`/pytest.skip. Такой skip не является producer evidence.
- При заданном env требует absolute root и существующий exact
  `root/archive/final/commit.json`. Отсутствие/ошибка fixture — failure;
  Python fallback/generator отсутствует.
- Использует существующий StateReader с literal expected execution/point/
  attempt2/plan fingerprint и finite physical cap4MiB, включающим commit,
  receipt, full+analysis SHA и HDF metadata passes. Проверяет actual generated
  state_id/sequence, pair status/identity, shape9×3×2, literal Unicode detail,
  measured0, source_owner_role и оба expected owner paths.
- Проверяет summed owner SHA bytes, положительные HDF/metadata counters и
  общий cap. Чтение научных массивов/новый solve отсутствуют; fixture остаётся
  manufactured transport evidence, не physical/scientific acceptance.

Actual producer identity/source hashes/native library versions и сохранённые
call7 output hashes должен связать runtime receipt. Code/test source не
доказывает, что будущий artifact возник от проверенного Runner; это отдельное
obligation координатора. Call8 обязан задать env; explicit skip неприемлем
как закрытие transport gate.

## Обнаруженное требование к Runner caller, переданное координатору

При чтении указанного primary Runner test его tail допускал env output только
`/tmp/qcl-sci05-runner-portable-fixture`; назначенный координатором будущий root
`/tmp/qcl-SCI05-C08-RUNNER-7/tmp/producer-fixture` таким source был бы отвергнут.
Это concrete source/caller mismatch, передан координатору; Runner source здесь
не изменялся. Перед call7 нужен owning exact whitelist/source binding update.

Также layout уточнён по реальному source: default archive_root равен
`joinpath(directory,"archive")`, final=archive_root/final. Поэтому consumer
читает `root/archive/final/commit.json`, не выдумывает `root/final` и не
подменяет producer layout Python fixture. Если owning producer path contract
изменится, нужен новый exact source binding, не silent search/fallback.

## Фактические checks и ограничения

Только text/Git/hash operations и `git diff --check` (exit0). Imports/parser/
pytest/HDF5/Julia/target execution/build/install/network/solver=0; stage/commit/
push=0; children=0. C08 consumed6/8 не изменён; producer control предназначен
для того же выделенного call8, не дополнительного invocation. Actual fixture
пока отсутствует/не читался этим агентом; runtime results неизвестны.

StateReader same-budgeted-handle claim и ограничения historical
verify_recovery_bundle/_json_scalar/native metadata RAM остаются в v3, без
расширения. Новый общий native-sandbox proof не заявлен.

## Frozen source

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| src/qcl_negf_results/native.py | 16498 | 532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5 |
| src/qcl_negf_results/state.py | 29877 | 4de0129ca7a5d0a85d9e33b06bf9c5e48858c1c1c73c56e2949e1f9376c93823 |
| tests/test_final_fixed_point_audit.py | 33332 | c94bd68fa6b328c880211d15d61ec1baaeb2da2b3a8e72e429edf8f6b5fccb6f |
| /tmp/qcl-sci05-results-v4-patch.diff | 47760 | d2fe0d8e4830cfca663e734950294ebf3292c39c0d1061e0790ef4d869706c88 |

Identity: `/tmp/qcl-sci05-results-v4-identity.json`. Patch полный от exact base,
включает untracked test; сохранённые v3 bytes дают отдельный F1-only review diff.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 production binding сохранён | native/state exact v3 hashes | Independent CPP ещё нужен | сохранить |
| Actual producer transport control подготовлен | Env-gated existing StateReader test, literal assertions | Fixture/runtime ещё отсутствуют; skip не evidence | дополнительно измерить |
| Call7 output path готов на прочитанном Runner source | Hardcoded old whitelist и новый assigned root различаются | Owning Runner update требуется до call7 | изменить |
| Runtime/scientific acceptance установлены | Исполнений/arrays нет | Future C08/physical gates раздельны | данных недостаточно |

STOP: финальный v4 source frozen; дальнейших edits/исполнений нет без READY.
