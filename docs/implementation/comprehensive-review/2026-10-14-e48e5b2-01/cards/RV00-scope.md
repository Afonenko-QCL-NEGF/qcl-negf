# RV00: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV00.md, fixes/RV00-*.md; reviews/RV00-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV00 — ledger актуальности требований

**READY:** каталогизация и поиск свидетельств. Owner Root с тремя ролями.
**Входы:** текущие уточнения пользователя; на docs ref —
`docs/system/{requirements,architecture,release-roadmap,implementation-entrypoint}.md`;
frozen `comprehensive-review.md` и source audit.

Исполняемые пакеты по 3–5 claims: `S01–S05`, `S06–S09`, `C01–C05`,
`C06–C09`, `C10–C13`, `R01–R04`, `R05–R08`, `R09–R12`, `I01–I05`,
`I06–I10`, `I11–I14`, `D01–D04`, `D05–D08`, `D09–D11`.
Claims вне каталога получают собственный locator и пакет, без раздувания
исходного denominator. Evidence прежней READY F01 переиспользуется адресно:
S01-first-gate в S01–S05, S07 в S06–S09, C01 в C01–C05; F01 целиком не
переносится в один пакет и не становится отдельным повторным аудитом.

- [ ] Извлечь точный текст, ID, дату, источник и последний статус каждой строки.
- [ ] Найти адресное decision evidence в текущем запросе, источнике и истории
  решения; код использовать только как свидетельство реализации.
- [ ] Записать applicability, конфликт/пробел, предлагаемое «подтвердить /
  уточнить / заменить / вывести из scope» и конкретный зависимый ticket.
- [ ] Проверить, что старые «С/Н/П» сохранены как история; составить только
  вопросы о невыводимом выборе, необходимом ближайшей зависимой карточке.

**Oracle/negative case:** прямое актуальное уточнение пользователя против
переноса старого S01 в обязательную нынешнюю цель. Отсутствие нового решения
не означает отмену всех прежних решений. **Acceptance:** каждая выбранная
строка имеет locator и обоснованный verdict либо локальный `needs_decision`.
**Выход:** `R/RV00.md`, M01/M12; RV03 получает конкретные owner constraints,
RV10 — выбранные научные ограничения. DONE относится только к объявленным,
проверенным claims пакета, даже если их принятие остаётся `needs_decision`.
Агрегированный RV00 сохраняет partial coverage, пока есть непроверенные
пакеты; другие карточки продолжаются.

