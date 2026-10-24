# DEV17 — frozen design packet, 2026-10-19

Роль D ultra. Этап — source/design, L-SOURCE. CP-DESIGN ещё не пройден;
DEV18 не исполнялся и не объявляется READY до независимого high review.
Ветку/Runner HEAD/clean state предоставил coordinator: Runner
`12e4d025948847c1b5d18ef4eb43a9934d8e20da`,
`codex/review-closure-runtime-durability`; published PR10 merged.
Я не выполнял Git-команды, не подтверждал remote metadata независимо и
не менял root/component refs. Source hashes сняты до и после design edit.

Working root:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Sole owning edit:
`components/QCLNEGFRunner.jl/docs/runtime-checkpoint-durability.md`.
Frozen SHA-256:
`d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc`.
Owning new-file unified diff: `/tmp/qcl-dev17-design.patch` (обычный
`diff -u` against `/dev/null`, не Git diff и не commit).

## Primary sources / interpretation

Прочитаны applicable root AGENTS, root/Runner architecture,
implementation-entrypoint, role policy, development.md common budgets и
DEV17/18, primary `fixes/RV11-runtime-durability.md`, generic repository,
atomic rename, full direct save/load callers, production codec path,
scientific point artifacts только для сравнения и existing YAML fixture.
Успешный current save не имеет enclosing fsync: прямой checkpoint! caller
возвращает repository reference, YAML helper даёт лишь namespace rename,
other callers status/events/results не содержат persistence barrier.

Основные contract choices:

- No generic pointer file: последняя metadata filename — commit/selection.
  Fault cut `:metadata_published` точно покрывает logical pointer update.
- Closed payload → chmod/hash → file fsync → one native rename → ancestry
  directory fsync → closed metadata → chmod/file fsync → one native rename →
  checkpoint directory fsync → published envelope/bytes/hash readback → return.
- Existing atomic helper делает chmod; checkpoint publisher вызывает один
  `jl_fs_rename` напрямую после fsync без post-sync inode mutation. Никаких
  copy/delete fallbacks; shared atomic/YAML helpers не меняются.
- Generic writer lock охватывает generation allocation и весь commit.
  Private active flag определяет recursive-save error; finally освобождает
  flag/lock и сохраняет original exception/raw files. Reader lock не нужен
  при immutable single-writer protocol; два repository objects не координируются.
- Backward-compatible public reader keyword
  `expected_attempt::Union{Nothing,Integer}=nothing`: explicit positive
  expectation проверяется до payload/codec, mismatch rejects production
  reader. Default сохраняет historical cross-attempt resume; existing
  coordinator callers не получают фиктивного exact-attempt свойства.
- Existing v1 schema/reference/filenames и raw identity сохраняются.
  Последняя corrupt metadata не скрывается fallback на старую. Старые
  полные checkpoints читаются без migration/перезаписи; failure temporaries,
  named orphan и raw production files сохраняются; cleanup не включён.
- Local POSIX durability conditional on actual fsync/rename support.
  NFS/native device/power loss unknown; no production acceptance claim.

## DEV18 implementation packet

Private `_RuntimeCheckpointIO` fields, exact `_save_runtime_checkpoint!`
signature, production adapters и ten cut names определены в owning doc.
Proposed fixture `test/infrastructure/runtime_checkpoint_durability_faults.jl`
имеет конечные **55 cells**: 20 cuts, 9 operation/readback errors,
18 reader/expectation rejections, 5 healthy/compatibility, 3 lock/reentrancy.
E09 отдельно ломает published same-size bytes перед writer readback и
требует отказа save; healthy post-return oracle не может принять unavailable.

Independent raw reader не использует writer/reader validation helpers;
сам строит filename selection, literal identity, bytes и SHA assertions.
Public reader проверяется отдельно, включая positive wrong attempt guard.
Общий YAML parser/SHA library — явное ограничение независимости.

Fixture source-includes реальный selected composition module и избегает
Core/HDF5 import. Это selected-source evidence, не owning package import;
existing YAML fixture остаётся отдельной targeted invocation с original
assertions и native dependency blocker при недоступности. Два commands и
L-JL ceiling указаны; общий действующий master grant сильнее. Здесь вызовов
Julia/runtime/import/tests/build/install/network/NFS/solver не было.

Writable implementation paths, требующие согласования high reviewer:

- `src/infrastructure/runtime/filesystem_repository.jl`;
- existing `test/infrastructure/yaml_repository_provenance_spans_and_checkpoint_integrity.jl`;
- proposed `test/infrastructure/runtime_checkpoint_durability_faults.jl`;
- `docs/runtime-checkpoint-durability.md` для фактических implementation locators.

`atomic_files.jl` read-only comparison: direct checkpoint-only native publisher
делает его edit ненужным. Ни coordinator/contracts/schema, ни scientific
generation paths не меняются. S1 all-five-no-EE/strict criteria защищены.

## Фактические проверки и ограничения

Text-only checks: `awk` вывел `lines=324, fences=6, whitespace_errors=0`;
каждый из четырёх relative source-link targets существует; placeholder scan
`TODO|TBD|FIXME|pending decision` совпадений не нашёл. New-file diff создан
обычным `diff -u` (expected code 1), hash/size сняты отдельно.
Production source hashes совпадают с начальным чтением:

```text
cd65f6f5b1e7128e3f5e7be9c6126a7eb5db799e2723431c86a9db36ae07a03f  filesystem_repository.jl
7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4  atomic_files.jl
81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a  point_artifacts.jl
b80cbc3b486d671482478f9bb4c539490b79fdb40b6edc9c25d6c958bbff4480  coordinator.jl
1caf02786b19ea09734459966d00993d088fbb7219c16c51e8e089408530a72d  contracts.jl
ad8b0fe43df8d21765d91dbfcbef7cbbc498453b0d1b41a8193c0db8d2a99efe  application_runtime.jl
a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef  existing YAML fixture
```

Git diff/status and independent CP-DESIGN выполняет coordinator/reviewer.
Научные/численные проверки не выполнялись. Исторические review revision и
current Runner revision различаются; текущий source defect проверен чтением,
исторический runtime evidence не наследуется.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing generic path не подтверждает persistence | Exact Runner source/symbol trace, source hashes выше | Read-only source proof; без native измерения | изменить |
| Sequencing/errors/compatibility/attempt guard заданы исполнителю | Frozen owning doc, exact private/public signatures и 55 cells | Нужен independent high CP-DESIGN; DEV18 ещё не READY | изменить |
| Production и existing assertions сохранены | До/после одинаковые hashes семи primary sources | Полный Git status не снимался по task scope | сохранить |
| Native storage durability и numerical correctness установлены | Свидетельство отсутствует | Не запускались NFS/power-loss/SCBA/Poisson/tests/imports | данных недостаточно |

Следующее действие coordinator: freeze этого doc hash + primary sources,
передать независимому high reviewer вопрос о sequencing, failure visibility,
API compatibility и finite DEV18 readiness без готового диагноза, сопоставить
замечания. Дизайн на этой точке остановлен.
