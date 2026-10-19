# Старт новой Codex-сессии

Это готовое сообщение **для отправки человеком** в новой сессии. Само чтение
этого файла или создание PR не активирует EXEC в публикующей сессии.
Инструменты на другом компьютере идентичны по условию пользователя; начните
с синхронизации Git и краткой проверки фактического source, без повторной
установки инструментов и полного повторения review. Если выявится реальный
environment gap, решайте его только в разрешённом INT01/BUILD envelope.

До merge этого PR используйте его head branch
`codex/review-closure-handoff`, **не main**, где этого handoff ещё может не быть.
После merge найдите те же repository-relative документы в принятом source.

## Промпт

```text
Продолжи QCL-NEGF в репозитории https://github.com/Afonenko-QCL-NEGF/qcl-negf.
Среда идентична предыдущей по инструментам. Синхронизируй root с опубликованной
веткой codex/review-closure-handoff и submodules строго по её gitlinks:
fetch, безопасный checkout/изолированная рабочая ветка, submodule sync и
update --init --recursive, без --remote. Локальные изменения сохрани;
reset/clean и переписывание чужих веток не разрешаю. Если PR уже merged,
выбери принятый source, содержащий этот handoff, и зафиксируй его identity.

Прочитай AGENTS.md, docs/architecture.md и точку входа
docs/implementation/review-closure-2026-10-19/README.md, затем autonomy.md,
operator-permissions.md и только нужные карточки. Первичное review включено
в Git: docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/;
правила historical paths/hash/missing inputs — PORTABILITY.md.

Этим сообщением я активирую EXEC и подтверждаю согласованные B/G1/S1 из P1,
включая разработку, проверки, публикацию PR, условный merge и scoped BUILD/OPS/SCI
после обязательных technical gates. S1 — без электрон-электронного рассеяния;
LO/acoustic/impurity/IFR/alloy сохраняются. Пределы: B до3 сборок по12ч/36ч
суммарно и100GiB additional peak; S1 до13 attempts/936 node-hours, ≤72ч/attempt,
≤2 одновременно и byte ceilings P1. Это общие пределы всех агентов.
Публичный release и остальные exceptions вне P1 отдельно согласовываются.

Начинай исполнение75 задач с INT01 и готовой независимой очереди. Работай на
выбранной Sol: coordinator/audit/review high, design/docs ultra, ready implementation
medium; версию модели не подменяй. Делегируй независимые задачи с одним writer
на owning paths и отдельным reviewer. Уже принятые scope/права и внутренние
design/code checkpoints повторно со мной не согласовывай.

Сначала сохрани HEAD/status/gitlinks и coordination checkpoint с grants,
владельцами, completed/blocked tasks, ресурсными счётчиками и operation IDs.
Продолжай до выполнения scope или конкретного blocker; compaction/handoff
не повод повторять завершённые задачи или делать duplicate submit.
Не ограничивайся новым пересказом плана.

Сервер был недоступен; новое сообщение не доказывает восстановление доступа.
Не блокируй локальные DEV/DOC/SI/научный design: при наличии trusted доступа
получи fresh inventory/admission и закрывай BIND/READY по P1. Старый S01,
foreign jobs/VM, persistent данные и неизвестные диски защищены.
Не ослабляй модель/критерии ради pass; missing/not_measured не pass.
Сохраняй failed raw/provenance, единственную final full CI запускай только
на final ready source без автоматических reruns. Все веб-интерфейсы светлые.
Отчёт веди по результатам и свидетельствам, физическую приёмку не обещай заранее.
```

## Выход первого прохода

CP-SOURCE/INT01 receipt и одна реально начатая ready task либо конкретный
зависимый blocker. Готовые авторизованные задачи идут дальше без нового опроса.
Private inputs и массивы Git не восстанавливает; одинаковые инструменты не
доказывают fresh серверные ресурсы или научную готовность.
