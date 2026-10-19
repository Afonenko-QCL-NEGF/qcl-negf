# RV00: начальный контракт

Вопрос: Какова актуальность каждой строки требований S/C/R/I/D?
Owner: Root/Research. Writer назначен единственный.
Denominator: все ID строк requirements.md; пакеты по 3–5 claims.
Inputs: frozen docs/system/{requirements,architecture,release-roadmap,implementation-entrypoint,comprehensive-review}.md; текущий запрос выполнить review; source audit. S и frozen overlay — source-receipt.json.
Разрешённые записи: только RV00.md; fixes/RV00-*.md внутри R; progress/index — только coordinator.
Oracle/negative: прямое уточнение против исторического S01-first; absence не отменяет историю.
Проверка: адресное статическое чтение двух сторон и fixtures, не исполнение тестов.
Выход: отчёт с claims/locators, observation/inference/proposal, M-ID, gaps, role actions и конечной таблицей.
Budget: пакет <=20 минут включая независимое review; writer ориентир <=12 минут, reviewer <=8 минут; <=1 CPU, <=1 GiB RAM/process, extracts <=96 KiB, section <=8 KiB. Grant всего прохода 14ч с 17:41 UTC.
Stop: verdict/gap, cap или следующий шаг за scope. Missing source блокирует зависимый verdict, другие вопросы продолжаются.
