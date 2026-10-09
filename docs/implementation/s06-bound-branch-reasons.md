# S06: сохранение continuation и привязка причины к точной попытке

Дата: 2026-10-09. Это свидетельства локальной проверки Contracts и Runner;
runtime, восстановление VM и научная приёмка остаются отдельными gates.
Требование S06 взято из опубликованного корпуса документации `debda91`.

Исходный Contracts gitlink — `026c122cd386752c0792727a75f86cdac25d2dd0`.
Проверенный и опубликованный commit —
`923e0c6cd9cbbe63bd1fb9c77892ef171385ed76`;
[component PR #3](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/pull/3)
слит в родительскую feature-ветку `codex/single-science-archive`, не в `main`.
Gitlink superproject выбирает именно проверенный commit.

Новый `messages.branch_reason(record, *, plan, owner_point, owner_execution,
source_points)` независимо проверяет семь полей причины, frozen owner,
полный набор текущих и исторических точек, точную execution/point/attempt
identity источника и объявленного предка continuation. Для legacy-записи
без причины возвращается `None`: отсутствие свидетельства не означает pass.
Проверка identity не вычисляет физические критерии и не запускает solver.

Локальный targeted packet выполнил четыре вызова pytest: первоначальный
RED, GREEN, затем RED и GREEN для найденного независимым reviewer случая
огромного integer, который мог выдавать обычный `ValueError` вместо
`ContractError`. Окончательный результат: **90 passed, 24 deselected**
(88 tests metadata-пакета и две выбранные регрессии).
Совокупное измеренное tool wall time — 5,59 s; сохранённый вывод —
126651 bytes. Полный suite и численные расчёты не запускались.

Независимая source review окончательного исправления не выявила замечаний.
Перед публикацией проверены diff и формат трёх component-файлов;
bounded scan 590 добавленных строк не обнаружил секретов по заданным
паттернам и доступным чувствительным литералам. Это ограниченная проверка,
а не доказательство отсутствия любого возможного секрета.

Runner интегрирует эти правила в сохранение ветки. Выбранный опубликованный
commit — `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, исходный gitlink —
`c367a257e6ac578c1e685877a0b4723eb3251214`.
[Runner PR #8](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/8)
слит в родительскую feature-ветку `codex/gap07-saved-comparison`.

Raw source rows проверяются до преобразования типов, выбора по ID и первой
публикации. Точки сохраняются в порядке frozen-плана; причины остановки
ссылаются на фактическую историческую точку и её attempt. Поздняя отмена
сохраняет уже опубликованный completed native результат и его assessment.
Ранний отказ новой попытки не копирует locators предыдущей под новую identity.
Campaign stop сохраняет готовые точки других executions. Отдельная политика
completed retention допускает существующие явные engineering operator reruns;
их current row и history продолжают отражать новую выполненную попытку.

Независимые source reviews выявили ошибки caller integration и дополнительную
регрессию operator rerun; окончательный diff их исправляет. Финальная чистая
metadata-проверка: **302 Julia assertions passed**, **17 сериализованных
контекстов passed** независимым Contracts oracle. Совокупно Contracts и Runner
использовали 16 ограниченных test calls с сохранением первоначальных failed
logs; общий вывод — 166256 bytes. Три ошибки конструирования fixtures исправлены
отдельными разрешёнными попытками; первоначальный Runner RED проверял только
отсутствие helper-файла и не является полным behavioral RED.

Эти fixtures не вызывают production `execute_scientific_plan`, solver или
native recovery. Cached Test/Markdown warnings сохранены. Перед публикацией
проверены формат шести файлов и bounded scan 776 добавленных строк;
известных секретов в этом scope не обнаружено.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Причина привязана к frozen owner и точному source attempt | Commit `923e0c6`, `messages.branch_reason`; 90 passed | Metadata-проверка не доказывает физический диагноз | сохранить |
| Legacy отсутствие причины различимо | Возврат `None` и targeted fixtures | Старые результаты не получают новую научную приёмку | сохранить |
| Компонент опубликован | Component PR #3 и выбранный gitlink | Feature merge не равен full release | сохранить |
| Retention и causal metadata реализованы в Runner | Commit `0c53c6d`; source review; 302 assertions и 17 binding contexts | Pure metadata seam не устанавливает native lifecycle | сохранить |
| Production continuation/recovery принят | Такие проверки не выполнялись | Требуются Runner и реальные lifecycle gates | данных недостаточно |
