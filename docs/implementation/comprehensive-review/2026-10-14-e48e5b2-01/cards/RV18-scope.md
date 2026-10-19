# RV18: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV18.md, fixes/RV18-*.md; reviews/RV18-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV18 · ADR единого входа документации

**Owner:** root/docs/Portal/Platform. **Вход:** три selected materials RV16,
mapping RV19; `components/QCLNEGFRunner.jl/docs/build/index.html`,
`objects.inv`, `search_index.js`, `assets/`; Portal `api.py`,
Platform `modules/application.nix`; root `README.md`, `docs/system/README.md`.
Existing Runner HTML доступен локально, но его source/build receipt пока
не установлен; это материал чтения, не current-release evidence.

- [ ] Подготовить ADR: static hub MkDocs или Quarto + existing Documenter;
  Antora; Backstage; минимальные ссылки на owning artifacts. Сравнить единый
  поиск, multi-repo version binding, ownership, maintenance, local assets,
  private exclusions и migration стоимости; выбор обосновать выбранным срезом.
- [ ] Спроектировать один pilot главы/API/runbook и docs-entry integration:
  source/release locator, prefix до catch-all, стабильные anchors и migration
  старых links. Публичный bundle исключает inventories, credentials, private
  supplements и raw operational logs. Portal показывает owning смысл ссылками.
- [ ] Статически инвентаризировать существующий HTML и assets; описать отдельный
  future browser protocol: light при dark OS, прямой anchor, поиск/math/fonts
  без внешней сети, доступные focus/contrast/error states. Предложить pilot
  ticket; исполнять pilot лишь в scope, включающем build и browser checks.

**Выход:** `R/RV18.md`: ADR, layout/integration proposal, candidate pilot.
READY pilot требует выбранных generator/version, source/build identity,
точных checks, разрешённого build/browser этапа и принятого бюджета.
**Приёмка:** M06/M16/M17; source binding и три journeys представлены явно;
offline/light пока `not_measured`, если проверен лишь source. **Negative case:**
светлый Portal окружает docs с auto-dark или внешним math/font CDN;
это gap, не выполненный M17. **Зависимость:** concrete selected outputs RV16/19;
ADR alternatives можно читать раньше. **Cap:** два packets, 40 min.
Произвольный dashboard/site build в этой карточке отсутствует.

