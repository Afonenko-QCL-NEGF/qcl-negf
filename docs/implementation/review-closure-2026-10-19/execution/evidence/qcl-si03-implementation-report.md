# SI03 — narrow implementation freeze

**Статус: DONE — frozen для отдельного CP-CODE координатора.** Никаких commits, push или PR не выполнено. Новый дизайн не создавался.

Root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, неизменный HEAD `c43935567df010d43cab9bcd8d851a9ed976a8d7`. Этап — docs-only implementation точного approved candidate. One writer: si03_impl для root AGENTS и восьми CONTRIBUTING. Dirty Core DEV05 и checkpoint принадлежат другим заданиям.

Входы: frozen `/tmp/qcl-si03-design.patch`, SHA-256 `b3bb0dca45047edc67373f141ed0feedc820246f1b268bc7db8a05fd96edb340`; independent CP-DESIGN `/tmp/qcl-si03-design-review.md`, SHA-256 `8c848558b676fef1ae24b1dc893c9bb3198e72d76bd26a8530ed44d89f5e41b2`. Baseline `/tmp/qcl-si03-baseline`, candidate `/tmp/qcl-si03-candidate`; оригинальные D artifacts не изменены.

Прочитаны root AGENTS, architecture, implementation entrypoint/canonical role policy, SI03 handoff и RV17 routing, eight owning CONTRIBUTING, Portal AGENTS/README; skills using-superpowers (subagent исключён), using-git-worktrees, subagent-driven-development и verification-before-completion. Здесь исполнитель не делегировал review: им владеет координатор.

## Изоляция и применение

Native app worktree инструмент относится к root repository; отдельные owning repositories изолированы через согласованный component Git fallback. `git worktree add -b codex/review-closure-contribution-routing /tmp/qcl-si03-worktrees/<component> <selected-gitlink>` выполнен один раз на компонент с scoped escalation. Existing checkout HEAD, status, diff и CONTRIBUTING не менялись. Ни reset/stash/update --remote/submodule update/checkout existing, ни stage/commit/push/PR не выполнялись.

До записи все 9 live inputs совпали с baseline, а 8 baseline CONTRIBUTING — с `git show <selected root gitlink>:CONTRIBUTING.md`. Повторная проверка перед записью выполнена. Root AGENTS получил только exact candidate; все остальные root paths вне writer scope.

| Owner | Selected component base | Worktree | Frozen patch SHA-256 |
| --- | --- | --- | --- |
| QCLNEGF.jl | `f5b73369a96d1225bd96fb34f5262c8dcf965f86` | `/tmp/qcl-si03-worktrees/QCLNEGF.jl` | `8caed3f5cc20ee7ed3617118fd486310a060d04ac9a408bd40172e730e752fc7` |
| QCLNEGFRunner.jl | `2d0190d5573f74d847d92a0dac8dd6ec524d494c` | `/tmp/qcl-si03-worktrees/QCLNEGFRunner.jl` | `379630cdabbe36a0d8f0bf3f02490a25d077e665e5ffd312f6af233abda64bf9` |
| qcl-negf-aiida | `312ed8a6363103d05a971d14ac9cbcca1c782358` | `/tmp/qcl-si03-worktrees/qcl-negf-aiida` | `d48bea753badf76e2c3a6aeec6fb45d33a633f8fd5cedb44361b1ec897d72e20` |
| qcl-negf-contracts | `26cacbe1688fee0af300d0949fc6b94e55a29f4a` | `/tmp/qcl-si03-worktrees/qcl-negf-contracts` | `90df7364761a92885a066f241e702cc7c8d1c0de247d919670107db80eb4f1e8` |
| qcl-negf-platform | `6a5d8048cd17e46d0149f529d03bef666276d5ce` | `/tmp/qcl-si03-worktrees/qcl-negf-platform` | `d9a9fd17720d9404e23adb15254df6b1ad724144965160c1dadfa39314086783` |
| qcl-negf-portal | `ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363` | `/tmp/qcl-si03-worktrees/qcl-negf-portal` | `d1f7a334f76e36f0a6342e1e0576f844438555713aa13413ed3ada24078a4ab2` |
| qcl-negf-research | `8325d228f5219bd1c219a1f9972a76db3c7a8c29` | `/tmp/qcl-si03-worktrees/qcl-negf-research` | `8d7ae50b57f8051d6e49f1f2c2245ee85df765a70b1c76130c6fcc3eadb16639` |
| qcl-negf-results | `17574ca4c5495f74d86ed9bef51c60dea8265062` | `/tmp/qcl-si03-worktrees/qcl-negf-results` | `dd1555b08daa405b97d931732e92557c8b65d85f6c92ed79f230c43278999cd7` |

Root patch: `/tmp/qcl-si03-implementation-patches/root.patch`, SHA-256 `d411b33b5c8d715ec2666bcf963d08242f231739d43ce8fa6664b40b231cef3a`. Component patches: `/tmp/qcl-si03-implementation-patches/<component>.patch`. Каждый patch содержит только owning CONTRIBUTING; root patch — только AGENTS. Подробные source HEAD/status до/после, diff hashes, file hashes и check receipts: `/tmp/qcl-si03-implementation-identity.json` (это receipt исполнения, не revision lock).

## Проверки и пределы

`python3 /tmp/qcl-si03-implement.py`: preflight 9 byte comparisons + 8 selected committed-source comparisons. `python3 /tmp/qcl-si03-verify.py`: **121/121 PASS**, включая 14 локальных Markdown targets, anchors, exact candidate equality, UTF-8/final newline/no trailing whitespace, fences, девять `git diff --check`, exact permitted path scope, unchanged source HEAD/status/diff. Script sources и exact per-check results сохранены в /tmp.

Root original instructions сохранены побайтово целиком: удаление единственной добавленной секции маршрутизации из нового AGENTS даёт baseline bytes. Полный diff просмотрен; компонентные тексты равны принятому CP-DESIGN candidate. Не менялись физические/численные правила, ownership, finite budget, bootstrap four-role+nginx/fresh admission и CI-once/fixed-light. Свежий независимый CP-CODE ещё не выполнен и не подменяется этим self-check.

External link availability не проверялась. Не выполнялись imports продукта, Julia/Python/Deno suites, environment install/instantiate, render/browser, benchmarks/profiling, Nix evaluation/build, solver/SCBA/Poisson, server actions или CI. Native/runtime/scientific acceptance не заявлена.

Budget: ≤45 min, 1 CPU/2 GiB/128 KiB output, один implementation round; последовательные дешёвые проверки. Peak RSS/CPU time отдельно не измерялись. Получен один согласованный implementation candidate; repair rounds не было.

## Сохранённое чужое состояние

Before root status:
```text
m components/QCLNEGF.jl
 M docs/implementation/review-closure-2026-10-19/execution/checkpoint.json
```
After root status:
```text
M AGENTS.md
 m components/QCLNEGF.jl
 M docs/implementation/review-closure-2026-10-19/execution/checkpoint.json
```

Recursive component heads до/после совпали. Core dirty diff SHA-256 до/после совпал. Checkpoint не читался/не записывался этим исполнителем; его dirty marker сохранён. Root AGENTS freeze добавляет единственный owned root dirty path.

## Передача координатору

Остановлено после freeze. Координатор выполняет независимый CP-CODE на exact patches/files, затем отдельно владеет staging/commit/publication и обновлением опубликованных gitlinks. Восемь component branches отделены от Core DEV05. Публикация или слияние не следуют из этого отчёта.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SI03 exact approved candidate применён | 9 file hashes в identity; 9 frozen per-repo patches | CP-CODE и publication впереди | изменить |
| Existing component source и Core DEV05 защищены | HEAD/status/diff/CONTRIBUTING до=после; recursive status до=после | Git metadata дополнена linked worktrees/branches | сохранить |
| Root gates и scientific invariants сохранены | Whole original AGENTS byte equality; component candidate exact equality + approved CP-DESIGN | Self-check не независимая приёмка | сохранить |
| Native/runtime/science выполнены | Таких запусков и receipts нет | Все соответствующие checks not_run | данных недостаточно |
