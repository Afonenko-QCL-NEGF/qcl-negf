# DEV21 — review packet

Этап: изменение тестового покрытия существующего Results PR6. Production physics,
solver, CI, server и installation/build не выполнялись. Существующий PR продолжен;
новый PR не создавался. Commit/push пока не выполнялись.

## Source

- Active root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
  HEAD `eb59809a4e601c9bd1d4859228d68502679b6d93`.
- Первичный Results checkout clean HEAD `fe27a2a9ed065f9afacecc84113311f30d0c68d6`.
- `gh pr view 6 --repo Afonenko-QCL-NEGF/qcl-negf-results --json url,baseRefOid,headRefOid,headRefName,files,state,isDraft`
  вернул OPEN DRAFT, base `fe27a2a9ed065f9afacecc84113311f30d0c68d6`,
  head `a1492b7b86b788885eff683ac71ca1167cbbaff1`,
  head branch `codex/portable-equilibrium-test-ownership`.
- Published PR paths: `README.md`, `tests/source_ownership.py`,
  `tests/test_equilibrium_diagnostics.py`, `tests/test_source_ownership.py`.
- Локальная ветка создана на exact existing published head без переноса чужих изменений.
- Другие dirty components/root coordination files сохранены без изменений этим writer.

## Incremental change

Только `README.md` и `tests/test_source_ownership.py`: 47 additions.

- `standalone_distribution_metadata`: synthetic temporary `dist-info` METADATA/RECORD
  и artifact pathname; реальные importlib.metadata.PathDistribution parser/locate_file
  используются, discovery distribution lookup перехвачен явно synthetic fixture.
- `test_standalone_distribution_ownership`: standalone branch без sibling и override,
  версия0.2.0, точный ожидаемый путь artifacts.py и один запрос owning distribution.
- `test_wrong_distribution_version_is_rejected`: та же полноценная file metadata
  с версией0.2.1, обязательное rejection с конкретным текстом assertion.
- README явно разделяет metadata branch evidence и actual wheel installation/import.

`tests/source_ownership.py` и `tests/test_equilibrium_diagnostics.py` byte-identical
published head a1492b7. Source read подтверждает 36 R01…R36 functions,
literal inverse2/math.fsum/weights и metamorphic R02/R04/R06/R35 сохранены.
Текущая source-проверка не является numerical runtime pass.

## Verification and ownership

`git diff --check` → exit0. `git diff --stat`, four-file full diff и incremental
прочитаны. `git diff a1492b7 -- tests/source_ownership.py tests/test_equilibrium_diagnostics.py`
пустой. Production files не изменены.

Pytest не запускался автором: coordinator владеет sole shared test slot.
Запрос направлен координатору: bounded Python3.14 locked owning import invocation
для `tests/test_source_ownership.py` + `tests/test_equilibrium_diagnostics.py`.
Новый behavior bug не обнаружен, поэтому implementation fix/red-green не выполнялись;
это недостающее coverage существующего поведения. Синтетические metadata fixtures
не доказывают реальный wheel/editable import; actual trusted artifact route остаётся
отдельным DEV22/BUILD свидетельством. Независимый high review ещё ожидается.

## Frozen hashes

| Object | SHA256 |
| --- | --- |
| Full base-to-tree review `/tmp/qcl-dev21-review.diff` | `e39426fecd08d19786187369c0f635e71e3a6cda7be6fe08d10cbc3d46cda126` |
| Head-to-tree `/tmp/qcl-dev21-incremental.diff` | `82a0ca3a00579c424467cba042085b1c8313305fbb5fb97c8737d2a9c5635dfa` |
| README.md | `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9` |
| tests/source_ownership.py | `95b2a6811c3ea10c77efcc4c64d90bc6d1ef04e529d027f5a65eb7db00d501ea` |
| tests/test_source_ownership.py | `a12218553195e07ecb74b1d06dd5b27477307ec67b8fcecd42e854a0e1ba2c03` |
| tests/test_equilibrium_diagnostics.py | `ce35954b2503d7a910048d6e95bcc6b6b0c88eea40f8a018dc13bdf8ca4bbad0` |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing PR6 exact candidate продолжен | Fresh gh metadata, local HEAD a1492b7, four allowed paths | Incremental changes пока uncommitted | сохранить |
| Guard и 36 numerical properties сохранены | Empty incremental diff двух файлов, source locators R01…R36 | Runtime outcome неизвестен | сохранить |
| Standalone distribution metadata branches представлены | Два новых теста, synthetic PathDistribution fixture | pytest ещё не выполнен; не actual wheel/import | дополнительно измерить |
| Scientific acceptance | Нет новых scientific runs | Не входит в DEV21 evidence | данных недостаточно |
