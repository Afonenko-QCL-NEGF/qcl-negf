# SI04 — independent CP-CODE

**Verdict: ACCEPT / CP-CODE PASS для exact четырёх references.** Блокирующих замечаний нет. Это принятие документационного implementation, не whole-skill/SI05/SI07, reader runtime или scientific acceptance.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`. Frozen implementation patch SHA-256 `11fd8c8794f701bca0594c0a567266f25807eb389045448ac48f517b770bdd1d`; identity SHA-256 `59a114da0b0283453d10365848fad0fd87c57df7901c8e8982b1146c52daea50`. Author report SHA-256 `d5ff433e5c9e73fee1f6a428841bb06de4e52391c69e08f13a316687d24247fb` прочитан после независимых actual byte/guard/source checks.

Approved design patch SHA-256 `ebc09a7219751c09fa5eadcb007129bea19c3fdccfe63325b1bb638569f452c3`; independent design review SHA-256 `bb63c9116e7f3365e8d79fbdb2174e0bcb9ca6f9ab8155d6200b94e122e8fb0c`. Новый дизайн и corrective edits не выполнялись.

| Actual path под `.agents/skills/` | Самостоятельно вычисленный SHA-256; `cmp` с approved candidate |
| --- | --- |
| `qcl-research-framing/references/brief.md` | `5acf06b37185d31f25b8b52a08bd62d6dfe2d5e8d5244afc9da1eedf272a9f0e`; равен |
| `qcl-physics-audit/references/physics-checks.md` | `a2b41df68de6ced8921e43a8f46bb123b84381fe9cc30441211cc8d306d5fb29`; равен |
| `qcl-results-analysis/references/comparison.md` | `ae11f2a66bbc43289f64ef850180d5bf165ca77b1a24e95fed8c2df008a9860f`; равен |
| `qcl-performance-audit/references/telemetry.md` | `c7a463d9e5397f331b1b4ab5a73c2c19daf02c42c4c0ae70e1193d3efc1fe7d5`; равен |

Самостоятельно сформированный `git diff --binary` только этих четырёх paths имеет exact implementation patch hash. Git diff по skill tree содержит только четыре разрешённых references; protected восемь SKILL/UI файлов совпали с committed root и identity hashes. Root AGENTS и восемь actual CONTRIBUTING побайтово совпали с guard hashes и selected committed content. Core CONTRIBUTING остаётся прежним, его SI03 proposal не выдан за опубликованный; семь остальных компонентов несут published SI03 docs. Foreign dirty Core/Portal и coordination/evidence paths не входят в SI04 patch и не изменялись рецензентом.

Все 34 production/source наблюдения identity независимо перепроверены: каждый live hash равен declared hash, а `git show <selected_commit>:<path>` даёт тот же hash. Таким образом source-map материалы не подменены dirty overlay; состав проекта определяется Gitlinks. Исторический D source root `c439355…` и implementation root `965ebed…` различаются явно; ранее проверенные owning formulas/readers не получили нового scientific acceptance от смены root.

Проверены все 12 route rows в actual refs: Brief `:13–15`, Physics `:12–14`, Results `:11–13`, Performance `:12–14`. Их bytes равны independently accepted design. Current source-only, archived compatible-reader interpretation и standalone supplied-material audit разделены. Current README не заменяет old archive contract, exact missing owner/version сохраняется; формулы/threshold/schema остаются у owner. Standalone essential content не создаёт новую task форму и не требует отсутствующего root. Никакого нового perpetual approval/runtime authority нет; existing grants, finite budget, fresh admission и dependent-only blockers сохранены.

`git diff --check` по четырём refs без diagnostics. Независимо проверены UTF-8/final newline/no trailing whitespace и пять actual relative Markdown links в own `../SKILL.md`. Root/owner paths остаются conditional textual locators, не обязательными standalone файлами. Новая network availability external URLs не проверялась. Author 196/196 static self-check не использован как независимый behavioral score.

Protected Physics archive-first opening и Results RO-Crate sentence остаются SI05 entrypoint work; это не load-bearing defect этих exact reference changes. Formal/forward samples относятся к SI07. Здесь не запускались product imports, tests/suites, Julia/install/build/render/browser, solver/SCBA/Poisson, benchmarks/profiling, server/live или CI. Runtime/archive execution/science не объявлены pass. Выполнены только read-only Git, text/hash/byte checks; Git mutations и source edits рецензента отсутствуют. Единственный новый output этого CP-CODE — настоящий отчёт.

Один CP-CODE round внутри общего assignment envelope ≤45 min, 1 CPU/2 GiB/128 KiB вместе с отдельно порученным read-only SI06 review; CPU time/peak RSS не измерены. Если bytes или selected source contract изменятся, review не переносится автоматически. Commit/publication остаются отдельными действиями координатора в active grants.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact SI04 implementation соответствует approved design | 4 hashes/`cmp`, exact patch equality, 12 routes | Только frozen text | сохранить |
| Protected instructions и selected source сохранены | 8 SKILL/UI, 9 guards, 34 live/committed hash comparisons | Не runtime/whole-skill acceptance | сохранить |
| Native/runtime/science приняты | Таких receipts нет | SI05/SI07/runtime/science отдельны | данных недостаточно |

STOP для SI04 CP-CODE; scope второго отчёта — только отдельно порученный SI06 read-only audit.
