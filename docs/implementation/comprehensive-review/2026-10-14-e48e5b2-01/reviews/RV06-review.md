# RV06 independent review

Blind answer сохранён в RV06-blind.md до чтения candidate/fixes. Проверен candidate SHA256 `75c2a19e4340d28d54836a0112840a4cd2a872470948550df03c0c4246c75b43`, ticket SHA256 `02b0140007f002f83d20d83751e697277c6ad00d356a33e7dbc32be09817596e`. Source P=4ce214e29b72276157b10a9267e2f30fef4ac66f, S/overlay receipt и frozen L1–L7 N=7 совпадают. Source check only; tests/import/build/server не исполнялись.

Вердикт: **сохранить отчёт и ticket**. Блокирующего дефекта отчёта не выявлено. P1 source ownership gap воспроизводим статически: main использует activation.lock и matching closed admission, но не lifecycle_guard; lifecycle orchestrators используют delivery.lock. Существование public update marker поэтому не запрещает этот controller activation entrypoint. Candidate честно отделяет это от production incident и избегает неверной простой замены lock, способной заблокировать parent/child delivery. Дешёвый proposed recording-boundary fixture соответствует вопросу.

L2–L7 имеют локаторы и source evidence: ready=false/health/ready=true; pending command/independent admission intent; disappeared job scope требует verify-stop; authorized new-boot startup и terminal resume blocker; cold gate special case и fresh build snapshot. Дополнительная проверка prepare_initial подтвердила matching closed gate и повторное чтение gate bytes. Несинхронизированный ready unlink и отсутствие общей transaction не скрыты. Assertions fake fixtures не выданы за выполненные/native outcomes; M04 source review не превращён в n/N pass, M09 не получил RTO, M10 live drift unknown, M11 partial native cells not_measured.

Nonblocking уточнение для owning реализации P1: explicit parent/child binding должен различать controller-local и remote worker child и учитывать живого child после смерти parent; публикация binding без independently checked authority не является решением. Ticket уже требует owner×entrypoint catalogue/crash evidence; smallest fix отчёта не нужен. Новая реализация/fixture остаётся отдельным Platform grant/PR.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| P1 single-writer gap доказан source | P main/lifecycle_owner; blind L1 | Нет native interleaving | изменить |
| Candidate сохраняет unknown→barrier invariant | P checkpoint/close_after_failure/startup | Crash/runtime not_measured | сохранить |
| Selected N=7 и negative cases отражены корректно | RV06 L1–L7, named tests, ticket | Не full catalogue или measured M pass | сохранить |
| Live drift/four-role lifecycle требует data | M09–11 limitations report | Site/native evidence absent | дополнительно измерить |
