# DEV10 — независимый CP-CODE review

Дата: 2026-10-19. Reviewer /root/reviewer, gpt-6.1-sol high.
Verdict: **CHANGES_REQUESTED** — один blocking contract gap.
Source reasoning не заменяется GREEN receipt; новых tests/imports не выполнял.

## Immutable review input

Base `67287afb53960b27e830b529c2149833db92a0ba`, branch
`codex/review-closure-export-selection`.
Review diff `/tmp/qcl-dev10-review.diff`: 24954bytes,
SHA256 `93049ef348031c992b53dbc25ea02778e1da4add07d920ea6d38db6e96943b1d`.
Report `/tmp/qcl-dev10-report.md` SHA256
`d0b759b577dbd80d2fb04463d073aa009d65e7ef2eb79f5fb7c8c8f4d1a82712`.
Оба hashes и четыре final owning file hashes независимо сверены; live diff
reverse-apply check полного package exit0. Targeted tracked diff --check exit0.
Четыре changed files: README, service.py, test_export_plan.py, new test_export_selection.py.
Accepted DEV09 contract не менялся; existing `_select_child`/`_attempt` сохранены.

## Blocking finding DEV10-R1

**P2 / spec и fail-closed metadata:** present published selection без корректного
execution_id превращается в отсутствие selection и разрешает legacy fallback.

Локатор: `src/aiida_qcl_negf/service.py:150–156` в `_export_child`, продолжение
`:185–195`; downstream result read `:204–206`, inventory read `:225–226`.
Здесь проверяется только `isinstance(record, dict)`, а missing/None/nonstring
`record.get("execution_id")` просто не попадает в `chosen`. Если остаётся один
child requested execution, код выбирает его и читает metadata.

Контракт: `docs/export-selection.md:60` требует correct execution_id у present
published record; malformed record должен дать invalid metadata/422 **без fallback
на single child**. Error table `:135` и acceptance `:163` закрепляют тот же отказ.

Воспроизводимый source-level counterexample, используя existing fixture
`tests/test_export_selection.py::source`:

```python
children, node, selection, events = source
children.pop(0)                 # sole remaining child C2 of execution E
del selection["execution_id"]  # namespace record still present
service.get_export_selection(RUN, "E")
service.list_execution_artifacts(RUN, "E")
```

По текущим ветвям оба вызова проходят: первый возвращает C2/failed, второй —
inventory C2. Required outcome: `ValueError("Published attempt selection is invalid")`
до result/inventory/payload reads. Counterexample **не исполнялся** из-за
исчерпанного бюджета; ветвление проверено непосредственным чтением кода.
Варианты None, bool или иной invalid execution_id дают тот же обход validation.

`test_invalid_published_selection_never_falls_back:156–170` не покрывает этот
case: есть nonobject, bad_attempt, bad_uuid, foreign UUID, mismatched pair и
conflict, но нет missing/invalid execution_id при sole child. Поэтому107green
не различает эту contract violation.

Минимальное направление исправления: проверить required execution_id shape
перед applicability filter. Valid record другой execution должен оставаться
исключённым из выбора, malformed record не может считаться отсутствующим.
Explicit selectors по-прежнему обходят published records; old single-file
contract менять не требуется. Добавить соответствующий negative control после
отдельного решения coordinator о targeted budget: текущие4/4 calls исчерпаны.

## Остальная spec/quality оценка

По прочитанному diff соблюдены strict input selectors, exact effective pair
для existing selector, known new mismatch422/foreign404 и old single-file404,
status только selected result, bounded read_json32MiB+1, шесть source statuses,
unknown только absent output, copied process-independent status, inventory
без repository I/O, strict marker/path/size/count/duplicates и detached five-field
rows. Plan raw bytes/source/hash остаются pinned после selection change.
README пример передаёт оба selectors. Выбранные tests используют реальные
service functions с явно synthetic ORM/repository boundaries и bytes oracle;
не доказывают native AiiDA/Portal end-to-end или scientific acceptance.

## Test receipts: проверено чтением, без rerun

Все восемь receipt/log hashes четырёх попыток совпали с author report.
GREEN2 original log: `107 passed in 0.37s`; process receipt exit0,
wall4.180s, sampled tree RSS144871424B,180B output, no stop. RED2 original
log фиксирует DID NOT RAISE для present attempt без value, затем final helper
разделяет absent input и malformed present input. RED1/GREEN1 receipts retained.
Это четыре targeted calls, а не full suite; budget не сбрасывается reviewer.
INT01 импортная route — ранее измеренный owning editable path, не native/profile
acceptance. Final hashes связывают reviewed source package; review tests не запускал.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все malformed published records fail closed | service.py150–156 counterexample против contract60/135 | Invalid execution_id не покрыт current fixtures | изменить |
| Остальной exact-child/status/inventory контракт реализован | Прочитанный final diff и retained107-green selected tests | Synthetic boundaries; нет native/Portal integration | сохранить |
| GREEN2 является всем spec compliance | Log107passed + непокрытый counterexample | Count не proof missing negative property | данных недостаточно |
| Scientific/native acceptance достигнута | Таких receipts нет | Solver/server/build/native не выполнялись | данных недостаточно |
