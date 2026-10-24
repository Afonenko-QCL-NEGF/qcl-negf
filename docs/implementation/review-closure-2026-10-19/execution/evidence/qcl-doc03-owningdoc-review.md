# DOC03 — independent CP-CODE owning documentation

**Вердикт: PASS. Блокирующих замечаний нет.** Actual `docs/system/physics-documentation.md` соответствует принятому D2 через проверяемое обратимое преобразование. CP-CODE относится только к этому docs diff; schemas/adapters/serving/runtime/scientific acceptance не установлены.

## Exact identity

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, фактический HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`.

| Input/output | Проверенный SHA-256 |
| --- | --- |
| Accepted `/tmp/qcl-doc03-design-v2.md` | `01bd504b382062ad896280e58dca4588e67f725e5deb72f350eae99c91aca625` |
| Accepted D2 review | `accfdda98914e3f1ab235b82cc5849d91af6d05bfa0561e610817e46eaf2555a` |
| Actual owning doc — 88,916 bytes | `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb` |
| Original root blob — 28,349 bytes | `434ad2513188d52c915ea2de5dee92b4257711abad3e19d51be47f31f2b7da20` |
| Frozen identity | `3c5bfc530e2fa2cea2ea13bd4d0545b8701ef3bcf600d2a6f539037c516f6575` |
| Frozen patch | `86813476770580907c17fac00c2368404c518addab55fab4c9f8cfa1c6cddf6a` |
| Body mapping | `1ae35c958f952df6537a9cce38dfd78a248cece0dcceb16ac248fba86c1b383f` |
| Author report — прочитан после actual/mapping checks | `031222ab72df40b11a594fd5311ffa7f5e392d6588b19737b3a90550b739479c` |

Все восемь immutable D1/D2/source/review/freeze inputs остались равны captured hashes. Никакой working Core/Contracts candidate не использован вместо selected source. 61 исходный source witness дополнительно сверены с exact Git objects: 846,485 bytes, mismatch 0. Source facts сохраняют root9d8/gitlink epoch; исторический аудит — bce0aee epoch.

## Независимая проверка переноса

Сначала просмотрены actual diff и accepted D2; затем mapping/identity; author report прочитан после независимой сверки. Author helper script не импортировался и не исполнялся.

Из D2 независимо выделен body от `## 2. Что установлено по source` до `## 9. Handoff` exclusive. Проверены 15 heading→explicit-anchor преобразований, 3 вида локальных link replacements и ровно 4 body rewrites. Самостоятельно сформированный transformed body найден в actual документе ровно один раз; обратные преобразования дали **побайтово exact D2 body**.

Source body hash `18ca8e0f6303ea6047977abd809ca1dd34c0d37cec71318a779c24a8fd47f9ae`; transplanted body hash `6356341fd7f21256f6fa69034dc073ef3f86dde09d5ca26b8d291cc1c16a3ba4` совпали с frozen mapping.

Четыре правки смысла контракта не меняют: proposed-after-design заменён принятым implementation contract без объявления existing API; «этим D2» заменено «этим контрактом»; invariants D1 названы общими invariants документа; удалён временный dirty-checkout operational факт при сохранении clean published source prerequisite.

Сравнение original/actual содержит только две insertion groups: 6 и 683 lines. Удалений/замен исходных строк нет; все original bytes и 12 headings сохранены. Новые status/introduction paragraphs корректно отделяют accepted design от реализации/runtime, reference set от used S1 inputs и historical audit от source facts.

Frozen patch не обязан совпадать с Git diff serialization: это обычный unified patch без Git metadata. Он **побайтово совпал с независимо сгенерированным `difflib.unified_diff` original→actual**. Fresh reverse apply dry-check завершился exit0. Первые сравнения с Git plain/binary diff дали byte mismatch из-за формата заголовков/context; это не объявлялось content mismatch.

## Content, source и links

| Проверяемая граница | Actual locator / свидетельство | Вывод |
| --- | --- | --- |
| R1 actual origin против reference-only origin | `#model-help-value-origin`, строка408; exact D2 body | Override/context/evidence invariants сохранены; production capture не выдуман, missing proof→unknown. |
| R2 local snapshot и actor enrichment | `#model-help-local-snapshot`, строка540; `#model-help-retrieval`, строка603 | Per-point/attempt capture/retention, retrieved subtree, parser index и selected-child mapping сохранены целиком. |
| Unknown/version/release binding | `#model-help-compatibility`, строка692 | Planned не used; current/latest не заменяет retained graph; unsupported format остаётся incompatible. |
| Minimal route/allowlist/light/offline | `#model-help-publication-route`, строка266; `#model-help-build`, строка724; `#model-help-serving`, строка787 | Existing Documenter сохранён; tools/assets/serving readiness — prerequisites, не native pass. |
| Future controls | `#model-help-negative-controls`, строка837; `#model-help-point-retry-controls`, строка860 | Пять negatives и R1/R2 controls сохранены и не названы выполненными tests. |

16 explicit anchors уникальны; все actual local Markdown anchor/file targets существуют, missing 0. Existing external URLs не добавлены как доказательство сетевой доступности: network не использовалась. `/docs/...` URLs, endpoint/schema/authoring paths и новые output formats явно proposed/implementation-target; их существование не заявлено.

Actual документ не содержит `/tmp/` или `/home/` paths, author logs, reviewer receipts или временных operational source-status записей. `/private/site/…` остаётся явно synthetic negative case. Нормативный body переносит technical contract, а не session log. Новых физических формул/допусков/моделей, registry или status promotion нет; original formulas и historical limits сохранены.

## Fresh checks и ограничения

- `git diff --check -- docs/system/physics-documentation.md`: exit0, без diagnostics.
- `git apply --reverse --check <frozen patch>`: exit0; patch не применялся.
- Actual file hash, reversible body mapping, independent unified patch и immutable hashes: совпали.
- `git diff --cached --name-only -- docs/system/physics-documentation.md`: пусто; этот файл не staged. Другие staged paths/index не менялись reviewer.

Один bounded source/docs review, чтение менее2MiB. Никаких children, imports, tests, build/render, browser/network/server/CI/solver/arrays или Git mutations. Reviewer написал только этот отчёт. Точное сохранение source-bound design не доказывает поведение будущего Runtime/Portal/AiiDA implementation. Owning commit/publication и новые gitlinks — отдельный шаг координатора.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Accepted D2 перенесён без semantic omission/redesign | Exact reverse body equality, hashes, независимый unified patch | CP-CODE только документационного переноса | сохранить |
| Original prose/formulas/anchors и source epochs сохранены | Только две insertion groups, 16 anchors, dated status/source qualifications | External URL availability не проверялась | сохранить |
| Runtime/native/scientific readiness установлена | Таких evidence здесь нет | Imports/tests/build/solver не выполнялись | данных недостаточно |

**STOP:** docs CP-CODE PASS; дальнейшие stage/commit/publication — координатор.
