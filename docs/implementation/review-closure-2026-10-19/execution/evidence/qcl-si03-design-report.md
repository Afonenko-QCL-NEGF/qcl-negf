# SI03 — routing и восемь CONTRIBUTING: design-only candidate

Статус **PROPOSAL ONLY / CP-DESIGN CANDIDATE**. Owning/native/root файлы, Git refs/indexes и checkpoint не менялись. Это не independent review, не CP-CODE, не runtime/build/native/scientific acceptance. Перед применением координатор организует independent CP-DESIGN на этом exact candidate; narrow implementation затем идёт отдельными owning PR и опубликованными gitlinks. SI04/05 skills не затронуты.

Этап: авторство существующих инструкций/документации, не product execution. Coordinator поручил D≤45 min, 1 CPU, 2 GiB, output≤256 KiB, ≤2 corrective rounds, только source/text; никаких product imports/runtime/tests/install/build/solver/server/Git mutation. Исполнялись только read-only Git, text/hash tooling и stdlib static tooling; scientific attempts/final CI/native операций: **0**. CPU time/peak RSS полного author session не измерялись; эти ограничения не выдаются за telemetry pass.

## Вопрос, intent и подход

Нужно, чтобы исправление текста не требовало Julia/install/full suite, а code/schema/config и native/science задачи сохраняли meaningful checks и все gates. SI01 authority/epoch и SI02 девятиполевой контракт приняты координатором как predecessors. Последний прямой human EXEC B/G1/S1 без e–e и поздний engineering resource grant имеют приоритет над historical PLAN. Эта authority передана trusted coordinator brief; первичный human transcript здесь отдельно не перечитывался. Никакого нового grant этот пакет не создаёт.

Выбран **минимальный additive route**: 29 строк в root AGENTS, ссылка на canonical SI02, qualified команды восьми CONTRIBUTING. Старые root invariants остаются побайтово. Альтернатива с сокращением bootstrap блока в ссылку отклонена для этого narrow ticket из-за риска потерять конкретный gate. Новая shared contribution framework/lock/task registration отклонена: это лишняя конкурирующая форма. Generic cleanup не выполнялся.

## Freeze и source identity

Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`. Baseline observation UTC `2026-10-19T16:12:32.154006+00:00`. Полные фактические `git status --short` и `git submodule status --recursive` сохранены в `/tmp/qcl-si03-baseline-observation.json`; dirty parallel work признано и сохранено. Gitlinks выбранного root являются source authority. Все девять наблюдаемых исходных файлов совпали побайтово с committed content выбранного root/gitlinks; новая manually maintained revision-lock система не создавалась.

Наблюдаемые HEAD могут быть новее выбранного root gitlink: это не меняет происхождение CONTRIBUTING и не выдаётся за публикацию/merge. Сверка byte content локализована на девяти разрешённых файлах. Full source-graph acceptance нового root здесь не утверждается.

| Path | Selected source commit (root/gitlink) | Observed actual HEAD |
| --- | --- | --- |
| `AGENTS.md` | `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8` | `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8` |
| `components/QCLNEGF.jl/CONTRIBUTING.md` | `f5b73369a96d1225bd96fb34f5262c8dcf965f86` | `f5b73369a96d1225bd96fb34f5262c8dcf965f86` |
| `components/QCLNEGFRunner.jl/CONTRIBUTING.md` | `2d0190d5573f74d847d92a0dac8dd6ec524d494c` | `2d0190d5573f74d847d92a0dac8dd6ec524d494c` |
| `components/qcl-negf-aiida/CONTRIBUTING.md` | `5579d55684939495230241f446b7ea07c8ae0224` | `312ed8a6363103d05a971d14ac9cbcca1c782358` |
| `components/qcl-negf-contracts/CONTRIBUTING.md` | `26cacbe1688fee0af300d0949fc6b94e55a29f4a` | `26cacbe1688fee0af300d0949fc6b94e55a29f4a` |
| `components/qcl-negf-platform/CONTRIBUTING.md` | `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9` | `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9` |
| `components/qcl-negf-portal/CONTRIBUTING.md` | `ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363` | `ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363` |
| `components/qcl-negf-research/CONTRIBUTING.md` | `b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3` | `b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3` |
| `components/qcl-negf-results/CONTRIBUTING.md` | `17574ca4c5495f74d86ed9bef51c60dea8265062` | `17574ca4c5495f74d86ed9bef51c60dea8265062` |

Первичные команды/опасные эффекты проверены чтением owning sources: Core/Runner `deno.json` и `tools/ci.ts` (`test/docs` запускают Julia и при отсутствии prepared project instantiate); Platform `deno.json` (`check` включает Python tests) и `docs/infrastructure.md#validation` (`slurm-vm` boots guests); Portal `deno.json`, `scripts/ci.ts` и README development (`test:frontend` npm install/test/TS/build); Research README validate + Runner `src/cli.jl` (`plan` semantic resolve, отдельно от `run-plan`); Results README и `integration/test_live_julia_export.py`/`live_julia_export.jl` (actual SCBA producer). Их observed SHA-256 находятся в `/tmp/qcl-si03-support-observation.json`. Это one-time evidence, не второй source lock. Target modules не импортировались.

## Exact permitted proposal paths и артефакты

Candidate tree `/tmp/qcl-si03-candidate/` содержит ровно следующие девять путей; baseline tree `/tmp/qcl-si03-baseline/` имеет ту же структуру. Ни один существующий source файл не редактировался.

| Path | Baseline SHA-256 | Candidate SHA-256 |
| --- | --- | --- |
| `AGENTS.md` | `b795916b286983cc4c71ed3614bc0fb431acfc1d29974594565e71a30e66b648` | `ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330` |
| `components/QCLNEGF.jl/CONTRIBUTING.md` | `da2eb6272ebe7248a0b247d56a8ee1547b6b7128d93fffe38f072f7a9b5f73d1` | `25c92d052efca42a28455990ff1e70d0e1a341ee3604c35118d1bade9a4b6fd9` |
| `components/QCLNEGFRunner.jl/CONTRIBUTING.md` | `33baab1a45e5d8d5486893b084ec677abf560a386514ec0dac00e0426bd9cc5a` | `2e59d623c611e0ebfe9380590802bd79af61590ac3f3a65f5af92937de01efc0` |
| `components/qcl-negf-aiida/CONTRIBUTING.md` | `ca7013e5d39a76fae4178627afb0139039d51c545a402588e1affe5f9e7a3606` | `90dab32996d6952e40f74a1f26491f3ef43124f01f8a8a56eb60288a404876ca` |
| `components/qcl-negf-contracts/CONTRIBUTING.md` | `8de856612b93ef9ce08b94da8b238658933ed094c25c031dcc9a9bb7cc35549d` | `029859ad06814ad33740497d494227193b23593861c67423846176f8d3ce65bb` |
| `components/qcl-negf-platform/CONTRIBUTING.md` | `f3f5d3b006053947a0334ea9bc30a78a7a4bfc1bc844afe488496f51a9d7a61e` | `1e957beb71b3c4d1ad632453f3aefdb7cfe97ecc02fbce038020480af1182f39` |
| `components/qcl-negf-portal/CONTRIBUTING.md` | `c873a46ae4fe62d145862568c6722eca3136c4413a02d886702fd1070bc5ed3f` | `b0994d41b7e460e28e28710d6949258c6ccb084706ef6e07bb65f64e0a24ed10` |
| `components/qcl-negf-research/CONTRIBUTING.md` | `5ec397b20520ab511a34e847477ff32be19ca238ae16b62d1ad7145027f1ddf2` | `52e86709eb4013e08df130768e110908863ca103ab6468d6122bf030432f25fe` |
| `components/qcl-negf-results/CONTRIBUTING.md` | `8de856612b93ef9ce08b94da8b238658933ed094c25c031dcc9a9bb7cc35549d` | `c228613ad22198b125128437aac6047de3c3e22885c5f5bb3ec3c71bb62be48c` |

Patch `/tmp/qcl-si03-design.patch`, SHA-256 `b3bb0dca45047edc67373f141ed0feedc820246f1b268bc7db8a05fd96edb340`. Complete before/after checklist и 8 owning dispositions: `/tmp/qcl-si03-checkmatrix.md`. Machine-readable static result: `/tmp/qcl-si03-checks.json`. Baseline observation содержит selected gitlink, observed actual HEAD, exact file hash и equality observation для каждого path. Эти /tmp receipts остаются supplemental review inputs и не коммитятся автоматически.

## Содержание контракта

Root route различает docs, source audit, metadata/existing data, targeted code checks, environment preparation, build/full suite, live/native и science. Это dispatch к existing contract, а не новый workflow. Последнее прямое поручение определяет active grants; historical PLAN/standby не отзывает activated EXEC. Already-authorized ready action идёт без нового human question, но fresh admission/technical BIND/READY и outside-predicate CP-EXCEPTION сохраняются. Missing обязательный input блокирует только dependent action/claim. Более поздний ресурсный grant не отменяет scientific caps, protected reserves и sole final CI.

Root bootstrap/physical/numerical/secret/ownership/light правила сохранены целиком. В частности, four-role+strict nginx preflight, executable paths/flake inputs/builder identity/Git index ownership, admin read-only `GIT_OPTIONAL_LOCKS=0`, failed logs/new attempt, native reuse derivation+contents+test-contract, new-root-no-old-pass, separate engineering/signature/staging/guest/restore/final-CI/science gates, no automatic CI rerun, protected old S01/foreign state не ослаблены. Восемь CONTRIBUTING сохраняют все scientific/format/provenance/security/CI обязанности; изменяется scope команды, не критерий результата.

Текстовые исправления проверяют diff/links/anchors/format и сообщают непроведённые numerical/render/browser checks. Executable examples/recipes/API/schema/config/scientific data не получают text-only exemption. Code требует relevant behavioral checks/controls в prepared matching environment. Install/instantiate/full suite/docs render/package-image/frontend build остаются соответствующими assigned stages с finite shared envelope. Platform five-host evaluation сохранён; он не заменяет four-role preflight. Native Results SCBA integration явно раскрыт как отдельный numerical stage, чтобы его нельзя было запустить как Python-only/text check.

## Фактическая проверка и limitations

Static checks: **41/41 PASS**, denominator объявлен в `/tmp/qcl-si03-checks.json`. Среди них exact nine paths; original selected committed byte equality; whole original AGENTS byte preservation; candidate exact hashes; девять live-source hashes неизменны; UTF-8/final newline/no trailing whitespace; fences; все локальные Markdown file/anchor targets. `git diff --no-index --check /tmp/qcl-si03-baseline /tmp/qcl-si03-candidate`: exit1 из-за наличия diff, diagnostics пусты (no whitespace diagnostics). Это не code/runtime test pass.

External GitHub/публичные ссылки network-проверкой не проверялись. Frontend/browser/render/Julia/Python-product imports, code tests/full suites, env setup, profiling/benchmark, Nix evaluations/builds, server probes/mutations, SCBA/Poisson и sole final CI не выполнялись. Отсутствие этих checks не выдаётся за zero-cost runtime или scientific evidence. Доступность полной численной среды не установлена; для docs-only proposal она не prerequisite.

Все 4 agent slots были заняты (root + final_ug_design + sci04_design + этот author), поэтому дочерний independent reviewer не создавался. Пакет передаётся координатору для отдельного high CP-DESIGN без авторского verdict как исходного диагноза. До него файлы остаются только в /tmp. При rebase/implementation повторно снять live hashes выбранных 9 paths, preserve unrelated writers; если CONTRIBUTING исходник изменился — stop dependent application и resolve delta, не overwrite.

## Handoff и остановка

Авторский вопрос завершён reviewable candidate; implementation намеренно не выполнялся по PROPOSALONLY scope. Текущий canonical SI01/SI02 working corpus прочитан по фактическим hashes; после их owning commit проверить anchors/semantics ещё раз, без нового опроса уже принятого scope. Координатор единолично владеет Git/checkpoint. После independent CP-DESIGN I `medium` применяет approved text только на owning branches, делает local diff/links/format review, затем отдельные component PR и root gitlinks при active publication grants. Merge/deploy/build/science не следует автоматически из этого diff; уже выданные B/G1/S1 исполняются после своих сохранённых technical predicates, без повторного разрешения.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Docs-only путь самодостаточен без Julia/install/full suite | Exact 9-file patch + component scope clauses + static scenarios matrix | Текстовый design; будущая реализация и independent CP-DESIGN впереди | изменить |
| Root physics/cost/bootstrap/CI/light requirements сохранены | Whole original AGENTS byte equality after removal of sole inserted route; full before/after matrix | Semantic additive routing требует independent review | сохранить |
| Eight owning component commands qualified без потери обязанностей | 8 dispositions + primary command sources + exact baseline/candidate hashes | Code/native/runtime claims не проверялись | изменить |
| Historical PLAN не отзывает current approved action, readiness остаётся mandatory | Canonical working SI01/02 route + P1 predicates, candidate explicit route | Current authority trusted coordinator brief; technical evidence не подменено approval | сохранить |
| Native release/science accepted | Таких receipts не производилось | 0 runtime/build/native/science/CI executions | данных недостаточно |
