# SI03 — independent CP-CODE

**Verdict: ACCEPT / CP-CODE PASS для exact docs-only implementation.** Блокирующих замечаний не найдено. Проверка относится к девяти frozen файлам ниже, не к чужому dirty Core/checkpoint и не к последующим изменённым bytes. Новый дизайн не вводился.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD при начале и завершении review `c43935567df010d43cab9bcd8d851a9ed976a8d7`. Checked identity `/tmp/qcl-si03-implementation-identity.json`, SHA-256 `bf14130ceb239762f94a4c0c6332ff1b98da32aa5b369dde6b5114fdccb3051f`. Approved proposal `/tmp/qcl-si03-design.patch`, SHA-256 `b3bb0dca45047edc67373f141ed0feedc820246f1b268bc7db8a05fd96edb340`; CP-DESIGN report SHA-256 `8c848558b676fef1ae24b1dc893c9bb3198e72d76bd26a8530ed44d89f5e41b2`. Author implementation report прочитан после самостоятельных byte/scope/source/format checks: `/tmp/qcl-si03-implementation-report.md`, SHA-256 `bcd74e54c77fe17cabe9789a4c007b2977b4606eb0b34b2052e3b6517a609a87`.

## Exact material и изоляция

`cmp` подтвердил равенство каждого actual implementation файла с accepted candidate. SHA-256 самостоятельно вычислены на actual root/worktree файлах:

| Фактический файл | SHA-256 |
| --- | --- |
| Root `AGENTS.md` | `ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330` |
| `/tmp/qcl-si03-worktrees/QCLNEGF.jl/CONTRIBUTING.md` | `25c92d052efca42a28455990ff1e70d0e1a341ee3604c35118d1bade9a4b6fd9` |
| `/tmp/qcl-si03-worktrees/QCLNEGFRunner.jl/CONTRIBUTING.md` | `2e59d623c611e0ebfe9380590802bd79af61590ac3f3a65f5af92937de01efc0` |
| `/tmp/qcl-si03-worktrees/qcl-negf-aiida/CONTRIBUTING.md` | `90dab32996d6952e40f74a1f26491f3ef43124f01f8a8a56eb60288a404876ca` |
| `/tmp/qcl-si03-worktrees/qcl-negf-contracts/CONTRIBUTING.md` | `029859ad06814ad33740497d494227193b23593861c67423846176f8d3ce65bb` |
| `/tmp/qcl-si03-worktrees/qcl-negf-platform/CONTRIBUTING.md` | `1e957beb71b3c4d1ad632453f3aefdb7cfe97ecc02fbce038020480af1182f39` |
| `/tmp/qcl-si03-worktrees/qcl-negf-portal/CONTRIBUTING.md` | `b0994d41b7e460e28e28710d6949258c6ccb084706ef6e07bb65f64e0a24ed10` |
| `/tmp/qcl-si03-worktrees/qcl-negf-research/CONTRIBUTING.md` | `52e86709eb4013e08df130768e110908863ca103ab6468d6122bf030432f25fe` |
| `/tmp/qcl-si03-worktrees/qcl-negf-results/CONTRIBUTING.md` | `c228613ad22198b125128437aac6047de3c3e22885c5f5bb3ec3c71bb62be48c` |

Все восемь isolated worktrees находятся на отдельной owning repository branch `codex/review-closure-contribution-routing`. Общий Git directory каждого совпал с соответствующим owning component repository, а не с root или другим component. Worktree HEAD равен выбранному gitlink root `c439355…`:

| Component | Проверенный HEAD/base |
| --- | --- |
| Core | `f5b73369a96d1225bd96fb34f5262c8dcf965f86` |
| Runner | `2d0190d5573f74d847d92a0dac8dd6ec524d494c` |
| AiiDA | `312ed8a6363103d05a971d14ac9cbcca1c782358` |
| Contracts | `26cacbe1688fee0af300d0949fc6b94e55a29f4a` |
| Platform | `6a5d8048cd17e46d0149f529d03bef666276d5ce` |
| Portal | `ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363` |
| Research | `8325d228f5219bd1c219a1f9972a76db3c7a8c29` |
| Results | `17574ca4c5495f74d86ed9bef51c60dea8265062` |

Для каждого `git show HEAD:CONTRIBUTING.md | cmp` совпал с approved baseline, несмотря на продвижение трёх gitlinks после proposal. Таким образом новый состав root взят из Gitlinks; исторические таблицы наблюдений не заменяют source authority. Root committed AGENTS в `c439355…` также совпал с approved baseline.

Каждый isolated `git status --short` содержит только ` M CONTRIBUTING.md`; `git diff HEAD --name-only` содержит только этот путь. Самостоятельно полученный `git diff --binary -- CONTRIBUTING.md` имеет тот же SHA-256, что corresponding `/tmp/qcl-si03-implementation-patches/<component>.patch` и identity. Root diff по AGENTS равен frozen `root.patch`, SHA-256 `d411b33b5c8d715ec2666bcf963d08242f231739d43ce8fa6664b40b231cef3a`. Staged root изменений нет. Иные root dirty paths — protected Core и coordination checkpoint; дополнительно появился чужой untracked `execution/evidence/qcl-sci04-design-review.md`, не являющийся SI03 diff.

## Сохранённое состояние и инструкции

Original component checkouts сохранены: самостоятельно снятые HEAD/status и tracked binary diff hashes совпали с before identity; их восемь CONTRIBUTING по-прежнему равны baseline. Семь original checkouts чисты, с SHA-256 пустого tracked diff `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Original Core сохраняет ` M docs/src/development/review_oracle_contracts.md` и `?? test/numerics/final_state_alignment_oracle.jl`; tracked diff SHA-256 `645905bfe92a0304ec6a25e9a486d89c5c1ea0a8c0e4de5ca5031bab618fa258`, ровно before receipt. Review не менял эти файлы. Ограничение: before receipt не содержит content hash untracked oracle, поэтому его побайтовую неизменность из status/diff доказать нельзя; подтверждены сохранение пути/status и отсутствие вмешательства рецензента, а не полный historical byte audit untracked файла.

Из actual root AGENTS удалена только новая секция маршрутизации; результат `cmp` равен всему baseline. Физика/нормировки/oracle/provenance/ownership/cost/bootstrap/four-role+strict nginx/fresh admission/admin read-only Git/native reuse/CI-once/fixed light сохранены целиком. Exact component candidate equality связывает implementation с ранее независимо принятым design. Docs-only exception по-прежнему не распространяется на executable recipes/API/schema/config/data behavior; relevant code checks и отдельные finite environment/full-suite/native/science stages сохранены.

## Выполненные checks и limits

Выполнены `git rev-parse`, status/submodule metadata, branch/common-dir/selected-gitlink проверки, `git show`, `cmp`, SHA-256, diff scope/patch equality и `git diff --check` для девяти owned diff. Whitespace diagnostics отсутствуют. Проверены UTF-8, final newline и отсутствие trailing whitespace всех девяти файлов. Root ссылки существуют, заголовки canonical task/authority route и role policy разрешаются; локальные Platform infrastructure, Portal AGENTS и Research README/Validate inputs существуют в соответствующих isolated owning worktrees. Новых machine-specific absolute links в текст не внесено. External GitHub доступность сетью не проверялась.

121/121 author self-check не принят за независимое свидетельство: перечисленные выше действия выполнены самостоятельно. Новые product imports, Julia/Deno/Python product tests/full suites, installation/instantiate, docs/browser rendering, Nix/build, solver/SCBA/Poisson, benchmark/profiling, live/server и CI не выполнялись. Они не нужны для этих exact text changes и не объявляются pass.

Один CP-CODE round в заданном конечном envelope ≤30 min, 1 CPU/2 GiB/128 KiB output. CPU time и peak RSS не измерялись; это лимиты, не telemetry pass. Рецензент не создавал commits/branches/worktrees, не stage/push/PR и не изменял native/root source. Единственный новый output — этот отчёт. CP-CODE разрешает дальнейший owning publication workflow только в пределах уже выданных координатору прав; не доказывает состоявшуюся публикацию и не наследует release/native/scientific acceptance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual nine-file implementation равен approved candidate | 9 independent `cmp` и hashes, exact per-repo patches | При изменении bytes нужен новый affected review | сохранить |
| Восемь owning branches изолированы, baseline/gates не ослаблены | Common-dir/branch/base/status checks, selected-source equality, whole-root preservation | Source authority остаётся у Gitlinks; публикация впереди | сохранить |
| Original Core DEV05 и остальные checkouts защищены | Matching HEAD/status/tracked diff/CONTRIBUTING observations | Historical untracked oracle byte hash отсутствует | сохранить |
| Full release/native/runtime/science приняты | Таких receipts этот review не создаёт | Отдельные gates остаются | данных недостаточно |

STOP: exact CP-CODE завершён; дальнейших действий не выполнялось.
