# S06: привязка причины остановки continuation к сохранённой точке

Дата: 2026-10-09. Это свидетельства локальной проверки Contracts;
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

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Причина привязана к frozen owner и точному source attempt | Commit `923e0c6`, `messages.branch_reason`; 90 passed | Metadata-проверка не доказывает физический диагноз | сохранить |
| Legacy отсутствие причины различимо | Возврат `None` и targeted fixtures | Старые результаты не получают новую научную приёмку | сохранить |
| Компонент опубликован | Component PR #3 и выбранный gitlink | Feature merge не равен full release | сохранить |
| Production continuation/recovery принят | Такие проверки не выполнялись | Требуются Runner и реальные lifecycle gates | данных недостаточно |
