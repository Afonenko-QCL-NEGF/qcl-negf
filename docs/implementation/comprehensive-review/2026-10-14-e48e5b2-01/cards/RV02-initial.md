# RV02: начальный контракт

Вопрос: Сохраняет ли exact PR6 owning import и переносимость fixture?
Owner: Results. Writer назначен единственный.
Denominator: exact base/head diff; imports; inverse2/literal_sum assertions; clean foreign-user case.
Inputs: Results fe27a2a9ed065f9afacecc84113311f30d0c68d6; PR6 head a1492b7b86b788885eff683ac71ca1167cbbaff1; pyproject/harness/fixture. S и frozen overlay — source-receipt.json.
Разрешённые записи: только RV02.md; fixes/RV02-*.md внутри R; progress/index — только coordinator.
Oracle/negative: чужая установленная версия должна быть отвергнута; отсутствие candidate не есть baseline verdict.
Проверка: адресное статическое чтение двух сторон и fixtures, не исполнение тестов.
Выход: отчёт с claims/locators, observation/inference/proposal, M-ID, gaps, role actions и конечной таблицей.
Budget: пакет <=20 минут включая независимое review; writer ориентир <=12 минут, reviewer <=8 минут; <=1 CPU, <=1 GiB RAM/process, extracts <=96 KiB, section <=8 KiB. Grant всего прохода 14ч с 17:41 UTC.
Stop: verdict/gap, cap или следующий шаг за scope. Missing source блокирует зависимый verdict, другие вопросы продолжаются.
