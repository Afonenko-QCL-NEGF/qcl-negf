# RV02: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV02.md, fixes/RV02-*.md; reviews/RV02-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV02 — переносимость existing Results PR6

Owner Results; вход `fe27a2a9…`,
`components/qcl-negf-results/tests/test_equilibrium_diagnostics.py`:
`EXPECTED_RESULTS`, `EXPECTED_CONTRACTS`, fixture `archive`; existing
[PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6),
base `fe27a2a9ed065f9afacecc84113311f30d0c68d6`, head
`a1492b7b86b788885eff683ac71ca1167cbbaff1`.

- [ ] Прочитать exact diff и harness; при недоступном candidate сохранить gap,
  продолжить baseline portability audit. Не подменять candidate текущим checkout.
- [ ] Связать проверку owning imports с `pyproject.toml`, fixtures и manufactured
  oracle `inverse2`/`literal_sum`; отдельно проверить неизменность assertions.
- [ ] Описать negative case: чистый checkout другого пользователя и импорт
  чужой установленной версии. Подготовить selected-check ticket без запуска.
- [ ] Выпустить `R/RV02.md` с решением о candidate и способом продолжить PR6.

Приёмка: устранение личных paths сохраняет отказ неверного owning import;
неизвестный candidate не получает verdict. M06 — import links; M02 — только
existing exact-source report или `not_measured`; M05 — original repeats,
иначе `not_measured`. Будущий M02 check: после harness preflight
`coverage run --branch -m pytest -q tests/test_equilibrium_diagnostics.py`
на exact PR head; отчёт owning imports обязателен. Для M05 отдельный ticket
предлагает три одинаковых повтора этого файла, сохраняя все исходные logs;
это candidate proposal, не threshold pass и не доказательство отсутствия
flakiness. Число повторов и permissions фиксируются до запуска. Зависимость: candidate
diff, не terminal S01.

