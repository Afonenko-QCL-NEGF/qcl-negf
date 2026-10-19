# QCL-NEGF: handoff после ревью, 2026-10-19

**Текущий режим — только планирование.** Product code/config, AGENTS/skills,
среды, кластер и научные результаты этим документом не изменяются.

Детальный план — в [единой точке входа handoff](review-closure-2026-10-19/README.md).
Он заменяет первоначальный набросок этого файла и содержит 75 задач:
25 DEV, 17 OPS, 15 SCI, 7 DOC, 7 SI и 4 INT.

- [Автономность, Sol effort, grants, checkpoints и operator decisions](review-closure-2026-10-19/autonomy.md).
- [Согласованные B/G1/S1 без e–e — approved_standby, не EXEC](review-closure-2026-10-19/operator-permissions.md).
- [Software и независимые oracle](review-closure-2026-10-19/development.md).
- [Кластер и дистрибутив worker](review-closure-2026-10-19/platform-worker.md).
- [Convergence и попытка physical acceptance](review-closure-2026-10-19/science.md).
- [Документация и SI01–SI07](review-closure-2026-10-19/documentation-instructions.md).
- [Полнота покрытия RV/SI и original proposals](review-closure-2026-10-19/coverage.md).

Полный целевой объём сохраняется: все findings, работающий подключённый кластер,
готовый worker distribution с инструкцией и агентский научный цикл. Сервер
сейчас недоступен; будущие live/native gates требуют fresh inputs. При отсутствии
финансового compute cap реальные ресурсы, конечные attempts и научная честность
остаются обязательными. Источник состава — selected root и Git gitlinks.

Оператор утвердил B/G1/S1 без электрон-электронного рассеяния. Перед реализацией
он отдельно активирует EXEC; принятые права повторно не согласуются. После
этого готовые задачи и внутренние review/checkpoints идут автономно без
повторных разрешений на каждый шаг. Production impact внутри B и science внутри
S1 проходят technical BIND/READY; существенные изменения вне scope, public release
и destructive exceptions остаются оператору.

Ранее подготовленные draft code changes отменены в отдельной рабочей копии;
восемь компонентов вернулись к исходным commits и чистому состоянию.
Они не считаются готовыми fixes/evidence. Сейчас создан только комплект плана.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Handoff детализирован | Карточки, dependencies, effort, permissions и acceptance | Режим PLAN, execution не начинается | сохранить |
| Все RV/SI имеют route | Coverage matrix и original proposal mapping | Фактическая приёмка ещё не выполнена | сохранить |
| Cluster/physical acceptance доказаны | Новых native/scientific результатов нет | Нужны отдельные выполненные gates | дополнительно измерить |
