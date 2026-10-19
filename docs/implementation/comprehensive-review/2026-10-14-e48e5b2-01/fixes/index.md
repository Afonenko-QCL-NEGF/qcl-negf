# Очередь адресных proposals и discovery

Это handoff из review, **ни одна строка не READY implementation**. Полномочия этого
прохода не включали внедрение, выполнение checks, install/build/solver/server или публикацию.
Readiness относится к конкретному stage карточки; `READY discovery/design` не создаёт compute grant.

Все строки ниже — proposed next work, не автоматически запущенный следующий цикл.
Если field future budget/interface/version/input отсутствует, сохраняется `needs_contract`/
`needs_budget`/`needs_data`/`needs_stage`. Existing evidence не превращается в новый permission.

## Конечный следующий discovery-пакет

Для выбранной строки: **один** вопрос из next operation, один owning writer, exact S/gitlinks
и frozen hashes из [source receipt](../source-receipt.json) плюс конкретные cited paths карточки.
Permitted read paths — только cited owning sources/fixtures/docs; permitted write path будущего
review — `R/fixes/<card-stem>-discovery.md`; actual code/AGENTS/skills/results не writable этим stage.
До назначения фиксируется конкретный denominator и независимый oracle/negative из original card.
Budget proposal source-only: один atomic packet, <=20min author+review, <=1CPU/1GiB/process,
shown extracts<=96KiB, reportsection<=8KiB; grant не суммируется с14h этого поручения.
Stop: exact invariant/check найден либо локальный disposition; unavailable input/cap/next costly
stage останавливают только dependent action. Не повторять закрытое чтение без нового входа/вопроса.
Это переиспользует [canonical contract](/home/tolya/Загрузки/qcl-negf/docs/system/agent-review-workflow.md), не второй план.

## Карточки

| Proposal | Owner | Stage/disposition сейчас | Следующая точная операция |
| --- | --- | --- | --- |
| [RV00 — requirement provenance и dated source status](RV00-requirement-provenance.md) | Root/Research | proposal; needs_stage/contract/budget as declared | найти primary decision locator или локализовать невыводимый выбор; не повторять59-row ledger |
| [RV00 → RV10 — локальный выбор следующего scientific contract](RV00-scientific-selection.md) | Root/Research | proposal; needs_stage/contract/budget as declared | найти primary decision locator или локализовать невыводимый выбор; не повторять59-row ledger |
| [RV00 — owning design и operator scope](RV00-scope-and-proposals.md) | Root/Research | proposal; needs_stage/contract/budget as declared | найти primary decision locator или локализовать невыводимый выбор; не повторять59-row ledger |
| [RV02 selected-check ticket — предложение, не разрешённый запуск](RV02-selected-check.md) | Results | proposal; needs_stage/contract/budget as declared | establish exact-source available harness/owning imports для future selected check |
| [RV05-1 — bounded actor lifecycle](RV05-actor-deadline.md) | Portal/AiiDA | proposal; needs_stage/contract/budget as declared | определить timeout/unknown outcome/close contract single-owner actor |
| [RV06-01 — explicit controller activation ownership](RV06-01-controller-activation-ownership.md) | Platform | proposal; needs_stage/contract/budget as declared | проследить parent→remote child activation ownership; определить explicit contract без naive lock swap |
| [RV07-1 — composite export exact attempt](RV07-attempt-export.md) | Portal/AiiDA selection interface | proposal; needs_stage/contract/budget as declared | resolve one attempt snapshot либо guard owner/docs legacy scope по конкретной карточке |
| [RV07-legacy-doc-scope](RV07-legacy-doc-scope.md) | Contracts/consumers | proposal; needs_stage/contract/budget as declared | resolve one attempt snapshot либо guard owner/docs legacy scope по конкретной карточке |
| [RV07-schema-drift](RV07-schema-drift.md) | Contracts/consumers | proposal; needs_stage/contract/budget as declared | resolve one attempt snapshot либо guard owner/docs legacy scope по конкретной карточке |
| [RV08 — concrete handoff, product/source patches не выполнялись](RV08-doc-and-oracle-handoff.md) | Core/Research | proposal; needs_stage/contract/budget as declared | разбить owning docs corrections и oracle gaps; выбрать независимый existing anchor before new fixture |
| [RV09 — finite oracle-gap proposals](RV09-oracle-gaps.md) | Core/Results/Contracts | proposal; needs_stage/contract/budget as declared | определить selected negative versus positive property scope; не выводить general pass из subset |
| [RV09 — минимальный future selected check](RV09-selected-check.md) | Contracts | proposal; needs_stage/contract/budget as declared | определить selected negative versus positive property scope; не выводить general pass из subset |
| [RV10 — next gate proposal, not run authorization](RV10-next-gate.md) | Results/operator with Research/Runner binding | needs_data/decision/budget before scientific comparison | получить exact terminal/raw/source metadata; научный выбор и критерии/budget отдельны |
| [RV11-runtime-durability](RV11-runtime-durability.md) | Runner/Results | proposal; needs_stage/contract/budget as declared | установить требуемый generic checkpoint durability и independent fault oracle |
| [RV13-01 — bounded coordinated restore evidence](RV13-01-bounded-restore-evidence.md) | Platform | needs_inventory/admission/native budget | подготовить sanitized generation/inventory/admission и restore measurement envelope |
| [RV14-1 — standalone Portal asset contract](RV14-asset-contract.md) | Root/Portal | proposal; needs_stage/contract/budget as declared | определить supported standalone asset/source build contract и импортную identity |
| [RV16-P1 · Статический inventory](RV16-inventory.md) | Docs owners | evidence appendix; not an implementation ticket | выбрать owning reader-section/example correction из трёх маршрутов |
| [RV16 · Три proposed дополнения выбранных материалов](RV16-selected-materials.md) | Docs owners | proposal; needs_stage/contract/budget as declared | выбрать owning reader-section/example correction из трёх маршрутов |
| [SI01 correction candidate — authority ledger](RV17-SI01-claims.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI02 correction candidate — один task contract](RV17-SI02-contract.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI03 correction candidate — action routing](RV17-SI03-routing.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI04 correction candidate — четыре references](RV17-SI04-references.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI05 correction candidate — four SKILL + UI](RV17-SI05-skills-ui.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI06 — preserve current route; conditional creation ticket](RV17-SI06-engineering-route.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [SI07 — proposed formal protocol and future forward ticket](RV17-SI07-validation.md) | Root/skill owners | proposal; needs_stage/contract/budget as declared | выбрать отдельный SI patch/validator/forward scenario с сохранением stages |
| [RV18 — one future docs pilot](RV18-pilot.md) | Root/Portal/Platform | needs_build_identity/version/browser-build grant | зафиксировать pilot generator/version/source binding и будущий build/browser budget |
| [RV19 — future bounded static prototype](RV19-prototype.md) | Code/docs owners | proposal; needs_stage/contract/budget as declared | развести API/config authored meaning и static generator prerequisites |
| [RV19 — narrow owning descriptions](RV19-source-meaning.md) | Code/docs owners | proposal; needs_stage/contract/budget as declared | развести API/config authored meaning и static generator prerequisites |

## Приоритетные различающие вопросы

P1 source findings: RV06 controller activation ownership; RV18 fixed-light/offline publication gate.
Scientific/docs distinctions: RV08 current prefactor, seed normalization и rejected legacy_pzp alias;
RV10 raw/criterion/source compatibility. Execution contracts: RV07 exact-attempt whole export,
RV05 stalled owner lifecycle, RV11 generic checkpoint durability. Priority — source risk/готовность
входа, не приказ запустить новый solver или менять физическую постановку.
