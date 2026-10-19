# RV16: начальный контракт

Вопрос: Как устроены inventory и маршруты трёх читателей?
Owner: Docs owners. Writer назначен единственный.
Denominator: root, все 8 компонентов: Markdown/docs генераторы и entry points, сегменты отдельно.
Inputs: frozen root docs; manifests/README/docs/build configs всех 8 Git gitlinks. S и frozen overlay — source-receipt.json.
Разрешённые записи: только RV16.md; fixes/RV16-*.md внутри R; progress/index — только coordinator.
Oracle/negative: README link существует но доставка content не доказана; student flow против implementation log.
Проверка: адресное статическое чтение двух сторон и fixtures, не исполнение тестов.
Выход: отчёт с claims/locators, observation/inference/proposal, M-ID, gaps, role actions и конечной таблицей.
Budget: пакет <=20 минут включая независимое review; writer ориентир <=12 минут, reviewer <=8 минут; <=1 CPU, <=1 GiB RAM/process, extracts <=96 KiB, section <=8 KiB. Grant всего прохода 14ч с 17:41 UTC.
Stop: verdict/gap, cap или следующий шаг за scope. Missing source блокирует зависимый verdict, другие вопросы продолжаются.
