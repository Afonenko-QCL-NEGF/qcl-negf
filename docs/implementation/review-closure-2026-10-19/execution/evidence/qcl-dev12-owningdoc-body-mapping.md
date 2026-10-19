# Accepted v2 to owning doc editorial mapping

Input v2 technical body: sections 2–12 inclusive; all other campaign sections omitted.
Owning header/section1: baseline/status/scope only; no new behavior.

| Exact old text | Exact owning text |
| --- | --- |
| Решение candidate | Решение контракта |
| ## 4. Exact proposed Python types и интерфейсы | ## 4. Целевые Python types и интерфейсы |
| Все имена ниже новые **proposed**, до CP-DESIGN не выдаются за existing API. | Имена ниже задают принятый целевой контракт; их наличие в baseline implementation не утверждается. |
| **новое operational решение этого candidate** | **новое operational решение этого контракта** |
| queue, также новые решения candidate. | queue, также новые решения этого контракта. |
| Все exact DEV11<br>selectors | Все существующие exact-child<br>selectors |
| ### 10.1. R1: store lock admission и coalesced filesystem cleanup | ### 10.1. Store lock admission и coalesced filesystem cleanup |
| Выбран один из предложенных R1 вариантов: | Выбран следующий вариант: |
| Это не требует frontend implementation вне DEV13 permitted paths. | Новый frontend API для этого контракта не требуется. |
| ## 12. Acceptance design для DEV13, без исполнения здесь | ## 12. Контракт проверок реализации |
| Для первого existing ASGI control DEV13 **обязан** согласовать fake producer | Для первого existing ASGI control реализация **обязана** согласовать fake producer |
| с DEV11; его current SimpleNamespace45–57 | с существующим exact-child producer; его baseline SimpleNamespace45–57 |
| exact DEV09 rows | exact selected-child rows |
| Дополнительный mandatory R1 Event oracle | Дополнительный mandatory filesystem Event oracle |
| Named proposed tests DEV13 retains: | Целевые имена fault-тестов: |

EOF format normalization: remove one final empty line from the extracted body; preserve exactly one terminal newline. No body token changes.
