# DOC04 public operator recovery — independent high prose review

2026-10-20. **PASS_SOURCE / APPROVE chapter `8f05ff4...`: блокирующих замечаний к public prose не найдено.** Текст даёт последовательный путь source/readiness → сохранение evidence → verified acknowledged selection → явно исполняемый new-attempt handoff. Source approval допускает Root copy; recipe/mapping/render/browser/served/public-ready gates остаются отдельными и здесь не подтверждены.

## Identity и порядок проверки

Сначала прочитаны accepted DOC04 design/review, frozen pilot plan, root deployment runbook, selected Runner `1acc165650fd4f4c2d49605cc679f90e3f6fcdae` docs и implemented CLI/selection/import/restart/staging paths. Затем — candidate chapter целиком; author report/identity/patch прочитаны после первичных sources и prose. После этого статически сверены target owning IDs/paths. Никаких renderer/parser/import/test или network calls не выполнялось.

Author checkout `/tmp/qcl-doc04-operator-worktree`, фактический HEAD `d4113f43cddf02d46025434eb3a9dd8e110e90d6`, status только `?? docs/public/`; в нём один file `operator-recovery.md`, 10216 bytes. Восемь selected gitlinks не инициализированы, не обновлялись. Root pilot checkout отдельно имеет base cfc38e1 и untracked docs tooling/tests; его parser/assembly не выполнялись и не объявляются опубликованным composition. Source authority остаётся Git/root gitlinks, не review identity receipt.

| Проверенный input | SHA256 |
| --- | --- |
| docs/public/operator-recovery.md | 8f05ff4cced8579b09cccd4b4315101e861e1896b87321b42e597374da79de49 |
| /tmp/qcl-doc04-design.md | 77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b |
| /tmp/qcl-doc04-design-review.md | 6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164 |
| /tmp/qcl-doc04-root-worktree/ops/docs/pilot-plan.json | cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50 |
| Root deployment runbook, same at d4113 | 8f659f7ee6dc3a5ff89acba052b1eadbcbeb2436fa6429d47d8dd400948da242 |
| /tmp/qcl-doc04-operator-report.md | db1deafd66705aeec7b8b9bceaefddca71f0ff645839c638bd7b84f22dcbc355 |
| /tmp/qcl-doc04-operator-identity.json | 609d28b9ba6010268bf6e59e73fa004635a100ccfbb3d2a67fcbe7d15e0c2a86 |
| /tmp/qcl-doc04-operator-patch.diff | 443e476860c493eb5337c2a375c464b1194d0af24c7667a5dd8317a0d3b315eb |

## Соответствие journey реализованному маршруту

- **Source и unknown:** строки11–29 требуют exact execution/point/source attempt/frozen plan/model и связь с root/gitlinks; явно запрещают заменять unknown текущими defaults или чужим attempt. Docs binding, metadata availability и science разделены. Отсутствие docs fragment не стирает независимо проверенные metadata. Это согласуется с accepted DOC04 §3 и root source/provenance contract; native source origin или release acceptance из имени файла не выводится.
- **Staging и preservation:** строки31–55 требуют inventory/budget/free space до payload copy, целую generation и prior-final closure, сохранение raw/pointers/logs/attempt и отсутствие pruning finals ради recovery. S01/foreign jobs/VM/disks не получают permission на cancel/format/replace. Scratch/shared staging не названы backup; local publication, LAN durability, restore и external-copy independence различены. Selected Runner `scratch_execution.jl::execute_scientific_plan_staged:123–162` действительно bypasses end-only scratch stage при включённом recovery.
- **Selection:** строки57–75 правильно описывают current→previous с повторной проверкой digest/commit/receipt/declared artifacts, pending/progress как недостаточные inputs и explicit no-valid-generation failure. Primary Runner `point_artifacts.jl::_verify_recovery_pointer:684–696`, `load_recovery_commit:698–711`, `verify_recovery_receipt:567–579` подтверждают порядок и error. Текст не предлагает pointer repair, удаление evidence или silent cold start.
- **Execution boundary:** строки79–101 отмечают `run-plan` как вычисление, используют один `text` fence с условными PLAN/OUTPUT/ID/N/DIRECTORY и отдельный OUTPUT. Grammar/flags совпадают с selected `src/cli.jl:74–91`. `scientific_execution.jl:490–529` требует explicit new attempt, N>source attempt, exact plan/execution/progress identity, imports prior-final closure до solving и сохраняет source attempt. `_import_completed_archives!:388–426` подтверждает archive-bundle layout и bounded required closure. Native restart default `load_production_restart(...; incompatible=:error)` остаётся строгим; глава не вводит ignore/quarantine route.
- **Научные границы:** operational import не назван scientific acceptance. Process/convergence/physical/discretization/experimental claims разделены, not_measured не превращён в pass. Глава направляет к owning Core/Research/Contracts, не копирует формулы, thresholds или implementation API definitions и не создаёт новый evaluator/format. Никакого real recovery locator или измеренного installation success в тексте нет.

Глава полезна как public operator orientation: указывает входы, последовательность выбора, безопасные исходы отказа и пакет handoff. Она не выдумывает отдельную readonly CLI-команду выбора generation: внутренний owning reader остаётся ссылкой на Runner, а единственная показанная команда явно execution. Доступность actual artifacts, fresh admission/credentials и конечный runtime budget устанавливаются отдельно для конкретной попытки.

## Anchors, links и public boundary

Primary `operator/recovery.html#operator-recovery` точно совпадает с plan operator slice. Chapter содержит шесть уникальных explicit IDs: operator-recovery, recovery-prerequisites, staging-prerequisites, recovery-selection, recovery-handoff, recovery-owning-references. Pilot expected `operator-recovery-route` правильно остаётся Runner source ID; root не дублирует и не переименовывает его.

Из будущего `operator/recovery.html` relative refs `../runner/user/results.html#operator-recovery-route` и `../core/theory/12_validation.html#researcher-final-route` разрешаются к принятым sibling sections. Selected Runner1acc results doc содержит первый ID; selected Coree431 validation doc содержит второй, его SHA `be55b03e7a228aebad88b24410d2633cd575ae63211a01ff4187f2c1bb95755b` сверён. Root pilot `assemble.py`/plan называют тот же operator source/URL, но actual `docs/public/make.jl` и source→Documenter recovery.md mapping в author checkout отсутствуют: это ещё не подтверждение generated HTML path/anchor.

Все три внешних источника — HTTPS GitHub blob refs на полные40-hex commits: Runner1acc results doc, Research3ed equilibrium-measurement-contract.md, Contracts12fc artifacts.py. Immutable objects/paths существуют в локальных owning repositories. Remote publication/HTTP reachability не проверялись и не названы pass. Ссылки не являются downloaded assets. Chapter не содержит private hosts/usernames/mounted inventory paths/credentials, historical receipts/log payloads или numerical arrays. Условный archive path — grammar, а S01 упомянут только как protected existing work без locator/measurements. Цветов/CSS/theme controls нет; fixed-light policy остаётся обязательной для будущего renderer.

## N1 — неблокирующая точность author bookkeeping

Author report и identity утверждают exit0 для `git diff --no-index --check /dev/null docs/public/operator-recovery.md`. Reviewer воспроизвёл **exit1 с пустым stdout/stderr**. Для нового отличающегося file no-index exit1 сам по себе не whitespace diagnostic. Не следует переносить author `exit0` как подтверждённый факт; корректное review свидетельство — command exit1, whitespace diagnostics absent. Source chapter менять из-за этого не требуется. Это замечание к сопроводительному receipt, не blocker prose/source copy.

## Границы выполненного review

Envelope ≤15min/1CPU/2GiB/read≤3MiB/report≤64KiB; cumulative CPU/RAM/read/tool-output telemetry не инструментирована. Только text/Git/SHA reads, static path/object/anchor inspection и запись review artifacts в `/tmp`. Target imports/parsers/render/tests/Julia/Nix/native/network/server, children, source edits, Git mutations и checkpoint writes — **0**. Чтение Runner/Core sources не выполняло solver и не создало нового scientific evidence.

Recipe/mapping, actual Documenter build, complete resource closure, transformed anchors, fixed-light/offline browser behavior, serving и DOC03 bundle acceptance требуют собственных receipts. Эта глава их не обещает, и source PASS их не наследует. Root copy/publication остаются отдельными действиями; reviewer их не выполняет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Public recovery journey соответствует owning CLI/reader | Chapter11–101; selected Runner CLI/import/selection/restart/staging paths | Source-only; реальные recovery inputs не проверялись | сохранить |
| Provenance, raw evidence, S01/foreign protection сохранены | Chapter source/unknown/staging/failure/handoff wording | Не actual inventory/restore/native proof | сохранить |
| Primary anchors и source link targets согласованы | Pilot plan, source IDs, immutable local blobs | Generated mapping/render/remote links не измерены | сохранить |
| Author whitespace command exit0 подтверждён | Reproduced no-index exit1/empty diagnostics | Сопроводительное bookkeeping; prose unaffected | изменить |
| Rendered/served/light/offline/native/science readiness установлена | Таких receipts нет | Future recipe/build/browser/acceptance gates | данных недостаточно |

**STOP. PASS_SOURCE chapter для Root copy с N1 bookkeeping caveat; никаких render/native/publication claims или запусков этим review не добавлено.**
