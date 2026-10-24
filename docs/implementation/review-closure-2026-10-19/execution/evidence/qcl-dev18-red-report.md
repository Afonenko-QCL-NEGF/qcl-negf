# DEV18 tests-only RED candidate — frozen, runtime pending

Этап: изменение тестов по accepted DEV17, без production implementation.
Writer: DEV18 medium. Source root:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Parent-provided immutable Runner HEAD:
`12e4d025948847c1b5d18ef4eb43a9934d8e20da`, branch
`codex/review-closure-runtime-durability`. Собственные Git commands не выполнялись
согласно поручению; root владеет фактическими HEAD/status/submodule receipts.

## Identity и изменение

- Accepted owning doc SHA256 `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc`.
- Accepted CP-DESIGN `/tmp/qcl-dev17-design-review.md` SHA256
  `bbe7e46b440db2d02a361949cfa55e7ab7895bb470375bfc5af0038308f0eadb`.
- DEV17 author report SHA256
  `466197b58198880c8d95c6b2281fac7fcbd51a866b052a5d40eda815a85fe4be`.
- Единственное owning изменение: новый
  `test/infrastructure/runtime_checkpoint_durability_faults.jl`, 22506 bytes,
  SHA256 `4e74a26ab5caf80e12ddae3e85ca4b3bb793081686bd0bbaeeb0fa35028ac429`.
- Tests-only diff `/tmp/qcl-dev18-red.patch`, SHA256
  `66ef2d239de54de50f4d29d8d0fa5c3d0ea034627c9181767e07f4a17c059e1e`.
  Этот patch создан difflib от `/dev/null`, не Git mutation.
- Staging copy `/tmp/qcl-dev18-runtime_checkpoint_durability_faults.jl` byte-equal owning file.
- Production `src/infrastructure/runtime/filesystem_repository.jl` unchanged,
  SHA256 `cd65f6f5b1e7128e3f5e7be9c6126a7eb5db799e2723431c86a9db36ae07a03f`.
- Read-only `src/infrastructure/persistence/atomic_files.jl` unchanged,
  SHA256 `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4`.
- Existing integrity fixture unchanged, SHA256
  `a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef`.
  Immutable provenance/tagged NaN/generation skip/hash assertions сохранены.
- Owning documentation frozen, writer её не менял.

## Конечная матрица и oracle

55 fresh trees: C01–C20, E01–E09, R01–R18, H01–H05, L01–L03.
Не расширял accepted matrix. R17/R18 — именно accepted expected_attempt=0/true;
это не два дополнительных Int-overflow cases.

C: ten exact cuts × empty/literal old baseline; exception object identity,
no returned reference, exact syscall/cut prefix, temporary/named bytes,
old/absent before metadata publication и complete new afterwards.
E: partial closed payload/metadata ENOSPC, file/directory/rename ordinal EIO,
no reference, original error object, no later trace operations, preserved raw files;
E09 same-size `state: bad\n` corruption после final directory sync требует
реальный writer readback CheckpointIntegrityError, unavailable latest без fallback.
E02–E09 проверяют полный exact trace prefix до отказа; C/H — полный ordered trace.
File adapter также проверяет regular/nonlink и chmod0640 перед native file sync.
H01 проверяет missing nested root/anchor chain; H02 две реальные sequential
записи и сохранность g1; H03 closed callback/readback без codec decode;
H04 literal historical attempt1 default+matching guard и absent-point guard;
H05 named orphan g2 survives, allocation g3, no current/previous pointer migration.
L01 pause first task через Channel; second task не достигает codec/allocation,
затем distinct generations. L02 failed generation/orphan + released lock.
L03 nested public save rejects до нового filesystem mutation, outer survives,
next ordinary public save возможен.

Independent oracle сам выбирает last metadata filename и проверяет regex,
literal v1 schema/ids/generation/attempt, regular non-symlink files, basename,
length и SHA по raw bytes. Он не вызывает production validate/reference/hash,
public load, codec validator или writer readback helper. SHA/YAML библиотеки
общие, что явно ограничивает независимость. Все malformed latest R-cells
содержат good g1, но oracle не делает fallback. Public reader вызывается
отдельно с codec counter=0 для всех rejected R-cells. Foreign symlink-target
bytes и старый g1 snapshot проверяются неизменными.

Fixture включает realpath `src/composition/application_runtime.jl` внутри
своего module и выводит composition+repository source SHA. Нет Core/HDF5/common
import, substitute packages, scientific solve, global monkeypatch или pointer.
Каждая cell использует `mktempdir(cleanup=false)`; исходные raw trees/trace.txt
сохраняются. Tiny payload ≤1KiB, envelopes ≤4KiB; finite retained output
по конструкции существенно ниже accepted8MiB; root harness cap всё равно обязателен.

## Selection/helper guard и ожидаемый RED

Selection target — весь новый owning file из superproject root:

```sh
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/infrastructure/runtime_checkpoint_durability_faults.jl")'
```

Только root запускает через reviewed bounded harness: максимум2 L-JL calls,
каждая120s/1CPU/2GiB/16MiB temporary/2MiB logs, общий ceiling4min.
Существующий harness/raw fix сначала независимо review; автор не менял его.

`HAVE_SEAM` вычисляется по exact private DEV17 symbols, каждое seam-dependent
C/E/H/L testset содержит failing `@test HAVE_SEAM`, затем guard от UndefVarError.
Это не PASS/skip отсутствующего API и не скрытие behavioral RED. Guard нужен,
чтобы отсутствующий новый injectable interface не оборвал R01–R18/H04.
Actual public-reader R/H04 execute независимо от seam. На baseline ожидаются
различающие semantic failures: R06 не классифицирует invalid YAML как
CheckpointIntegrityError; R09 metadata filename/generation не проверяется;
R15/R16 symlink принимаются и вызывают decoder; R14/R17/R18/H04 не имеют
accepted optional keyword (interface RED). Не ослаблять assertions ради exit0.
Expected behavior здесь source inference; observed RED ещё отсутствует.

## Выполненная проверка и сохранённая ошибка

Прочитаны AGENTS/architecture/CONTRIBUTING, DEV17/18 cards, accepted doc/review,
contracts/codec/repository/composition и existing integrity fixture. Применён
TDD tests-first порядок. Python static checks подтвердили exact copied bytes,
финальный newline, отсутствие trailing whitespace, перечисление55 cells,
отсутствие запрещённых common/HDF5 imports. Это не Julia parse/compilation.

Original first write failed, tool chunk `7a8873`, shell exit1:

```
/usr/bin/bash: line 1: components/QCLNEGFRunner.jl/test/infrastructure/runtime_checkpoint_durability_faults.jl: Read-only file system
```

Это sandbox boundary managed worktree вне writable roots, не test result.
Диагностика сохранена здесь. Parent подтвердил existing authorized scope;
scoped `require_escalated` copy успешно выполнен, без нового human permission,
без auto-review rejection. Не менялись failed harness/source/oldS01/foreign states.
Собственных Julia/import/tests/builds/install/Git/server/SCBA/Poisson runs = 0.
Production implementation запрещена до root semantic-RED release.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Tests-only candidate соответствует exact55 matrix/seam | Frozen fixture+patch SHA, independent reader и public rejection assertions | Julia parse/runtime пока отсутствуют | дополнительно измерить |
| Public reader имеет meaningful expected behavioral RED | Baseline source R06/R09/R15/R16, counter assertions | Пока source inference, не observed receipt | дополнительно измерить |
| Production/atomic/docs/integrity fixture сохранены | Baseline source hashes и единственный новый owning file | Git status принадлежит root | сохранить |
| Numerical/native/NFS/power-loss acceptance установлена | Свидетельства отсутствуют; runs0 | Synthetic live-tree tests этих gates не закрывают | данных недостаточно |

STOP: candidate frozen, ждёт root semantic RED/release. Следующих действий и
production writes до release не выполняю.
