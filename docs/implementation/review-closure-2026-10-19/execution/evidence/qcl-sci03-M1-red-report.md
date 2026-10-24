# SCI03-M1 — immutable RED test source, phase 1

2026-10-19. Автор I Sol/medium. Этап: только исходник тестов, **STOP до независимого high review и единственного coordinator RED call**. Никакие tests/imports/parsers/HDF/Julia/solver/build/install/network/server/stage/commit/push не выполнены. Production и README не изменены. Runtime/scientific/native acceptance не установлены.

## Исходники и подготовка

Root при чтении: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Root имел concurrent modified Core/Runner/Results gitlinks и checkpoint, а также untracked review/evidence artifacts; они не редактировались. `git submodule status --recursive` прочитан: selected Results `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`, Core `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee`, Runner `1acc165650fd4f4c2d49605cc679f90e3f6fcdae`; остальной состав не менялся. Gitlinks root остаются authority состава, этот report — audit snapshot, не revision lock.

Прочитаны root AGENTS/architecture, Results CONTRIBUTING, P1/SCI03/SCI06 scope, qcl-physics-audit, TDD и writing-good-tests, принятые D/R и owning contract appendix. Независимый R: `fa1311a4bf16f08f6e417590b77b7e6179aa9320907934fbd4496ebc059ca4a9`; D: `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7`; owning Research file `/tmp/qcl-sci03-current-bound-doc-worktree/docs/equilibrium-measurement-contract.md`: `61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c`. Publication owning Research перед consumer publication остаётся gate координатора.

Initial preparation attempt `SCI03-M1-PREP-1`:

```
git -C /home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-results worktree add -b codex/review-closure-current-bound-measurements /tmp/qcl-sci03-M1-results-worktree 33b1a39eab62b0c00532c4d6b30fa3279c06a5d3
```

Git ответил: `fatal: cannot lock ref 'refs/heads/codex/review-closure-current-bound-measurements': Unable to create '/home/tolya/Загрузки/qcl-negf/.git/worktrees/qcl-negf19/modules/qcl-negf-results/refs/heads/codex/review-closure-current-bound-measurements.lock': Read-only file system`. Ошибка сохранена здесь; mutation не повторялась, runtime counter не расходовался. Никакого protected-original write не произошло.

Отдельная успешная preparation attempt `SCI03-M1-PREP-2`: локальный `git clone --shared --no-checkout` selected Results в `/tmp/qcl-sci03-M1-results-source.git`, затем `git worktree add` из этого clone в `/tmp/qcl-sci03-M1-results-worktree` на exact `33b1a39`, branch `codex/review-closure-current-bound-measurements`. Все metadata writes находятся в `/tmp`; clone использует read-only object alternates selected source, no network/no source refs writes. Это shared local clone, не `--no-hardlinks` self-contained clone; зависимость objects явно сохранена в identity. Protected original не редактировался; его object store доступен только на чтение. Component recursive submodule status пуст.

## Frozen test delta

Изменён единственный файл `tests/test_equilibrium_diagnostics.py`, только +324 строк. SHA256 `7d2a9d69a0d4cb02334b9b4617a09a9cb3746247eba17f7ebff364eb62ab8921`; patch `/tmp/qcl-sci03-M1-red-patch.diff`, SHA256 `8c7aa6f21518e86534135c99fec4d354a1162b546f03f8dd85598c9dcc7575b1`.

Baseline test SHA `ce35954b2503d7a910048d6e95bcc6b6b0c88eea40f8a018dc13bdf8ca4bbad0`; full baseline prefix сравнён `head -c ... | cmp` успешно. Все прежние 36 tests и helper semantics сохранены, не переименованы и не ослаблены. Production `src/qcl_negf_results/equilibrium.py` SHA остался `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6`; README SHA `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9`.

Новые 9 test functions дают 15 parametrized cases, ожидаемый total 51 (source count, collection не запускалась):

| Test | Что различает |
| --- | --- |
| M1_01 ×2 | D literal 1E×2k×2×2 matrices, weights/spin/radial factor, both versions/sides, exact separate norms/terms; centered common μ и off-centered quarter-capacity μ различают f/(1−f) swap |
| M1_02 | Nnormalized+iρI, ρ=1/32: complex-current imaginary part и full complex norms; проверяются обе части и hypot |
| M1_03 | Stored literal zero boundary при defined μ: measured exact zero coefficients/terms/B несмотря на ненулевой normalized sum defect |
| M1_04 ×6 | Missing context, drive, unequal LO, e−e mode, empty spectrum, μ algorithm_limit: exact status/reason наследуются до zero shortcut, dependent values null; A/correction rows independently measured |
| M1_05 | Existing healthy 5E/nonuniform weights сохраняют FDR; exact matrix-read counts: A два passes, остальные один; no added matrix payload reads/third pass |
| M1_06 | Finite inputs с J0=1e308, normalized state×64: signed currents finite, absolute RHS overflow должен дать invalid_data |
| M1_07 | Report cap равен размеру existing namespace: добавление не даёт truncation/silent success |
| M1_08 | Missing embedding_plus datasets отвергается inventory guard, не трактуется zero |
| M1_09 | Pure scalar dyadic f0 table, distinct Γ norms/noncommutators, unequal k moments и literal signed currents |

Expected arithmetic использует literal rational M=3/(8π), L=7M/512, R=13M/65536, gamma²=11/32 и21/64, t из одного public reported μ с независимым scalar exp. Ни `_Norm`, `_fd`, `_fit_mu`, product reducer/bound builder не вызываются для expected. Existing fixture encoder/provenance используется только для format plumbing; это ограничивает независимость encoding, не literal arithmetic. Обе μ constructions отдельно проверяются known μ/bracket/stop/width; finite-t oracle не выдаётся за независимую проверку точности μ algorithm. Engineering bound `512*2^-53*max(1,abs(expected))` соответствует принятому fixed-scale ≤512-operation fixture policy; не rigorous libm enclosure/scientific tolerance. Exact dyadic/zero/sign controls отдельно сохраняются. Reviewer должен проверить actual operation chain, не увеличивать допуск при падении.

## Ожидаемый RED и бюджет

На baseline `33b1a39` ожидается 13 failed новых cases и 38 passed total: 12 failures с assertion `missing SCI03-5.3 measured current-bound instrumentation`, ещё M1_06 с `DID NOT RAISE ContractError`. M1_08/M1_09 должны пройти. Это **прогноз из исходника, не executed receipt**; любое иное падение требует анализа до production edit. Existing 36 historical passes здесь повторно не заявляются. Mu bracket и fixture format/source binding должны дойти до instrumentation assertion; high source review обязателен до расходования RED call.

Execution budget принадлежит координатору: SCI03-M1 максимум 2 Python calls (1 RED +1 GREEN), каждая ≤90s, 1CPU, 1GiB RSS, owned TMP32MiB, raw2MiB; суммарно≤180s. Никакого third call/automatic rerun. SCI05/08 C08 остаётся exhausted8/8, не сброшен/не расширен; scientific caps прежние. Здесь израсходовано 0/2 Python calls и0 C08. Source-author envelope≤30min,1CPU,2GiB,read4MiB,output64KiB; targeted text reads/hashes, без массивов. Read/RSS wall telemetry не инструментированы; source files/outputs значительно меньше caps, измеренный process resource admission не заявляется.

S1 остаётся 0mV/70K, LO/acoustic/impurity/IFR/alloy, e−e none, no tolerances/model/physical grid change. Single-E plane — manufactured diagnostic fixture, не production build_grids. H, εJ_abs, actual final arrays/run/attempt/frozen plan и native admission неизвестны. Bound instrumentation не устанавливает scientific accuracy/equilibrium/native truth.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED source создан в owning Results, baseline сохранён | exact33b1a39, append-only diff+324, baseline byte cmp, hashes | tests/imports/parsers не выполнялись | изменить |
| Literal controls различают основные ошибки | D/R approved table, new M1_01–09 source | самостоятельная high review и coordinator RED ещё нужны | дополнительно измерить |
| Production/README сохранены | unchanged SHA и diff name-only | phase2 не начат | сохранить |
| Bound подтверждает scientific acceptance | нет final arrays/admission/H/εJ_abs | source fixtures не numerical experiment | данных недостаточно |
