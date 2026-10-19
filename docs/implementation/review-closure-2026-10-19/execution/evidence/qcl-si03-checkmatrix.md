# SI03: before/after requirements-preservation checklist

Статус: **design candidate**, source/text-only self-check; independent CP-DESIGN ещё не выполнен. Before — `/tmp/qcl-si03-baseline`, after — `/tmp/qcl-si03-candidate`. Локаторы ниже относятся к этим двум frozen деревьям, не к будущему опубликованному source. Полная исходная версия root AGENTS сохранена побайтово: удаление только новой секции маршрутизации даёт baseline целиком. Это сильнее проверки наличия отдельных ключевых слов.

## Root AGENTS: все исходные группы требований

| Требование | До | После | Disposition / свидетельство |
| --- | --- | --- | --- |
| Приоритет физики; рабочие выводы по-русски, units/API/primary sources | `AGENTS.md:3` | `AGENTS.md:3` | сохранить; original paragraph retained |
| Этап по запросу, architecture и component instructions; не расширять полномочия | `AGENTS.md:9` | `AGENTS.md:9` | сохранить; original paragraph retained |
| HEAD/status/recursive gitlinks, без второго lock | `AGENTS.md:12` | `AGENTS.md:12` | сохранить; original paragraph retained |
| Archive revision/frozen plan/model/run/attempt/completeness; не latest | `AGENTS.md:15` | `AGENTS.md:15` | сохранить; original paragraph retained |
| Relevant skill не grant; старые чаты/планы контекст | `AGENTS.md:18` | `AGENTS.md:18` | сохранить; original paragraph retained |
| Entrypoint и canonical role policy | `AGENTS.md:21` | `AGENTS.md:21` | сохранить; original paragraph retained |
| Четыре QCL skill routes, без расширения scope | `AGENTS.md:27` | `AGENTS.md:27` | сохранить; original paragraph retained |
| Execution/convergence/physics/discretization/experiment раздельны | `AGENTS.md:34` | `AGENTS.md:63` | сохранить; original paragraph retained |
| Evidence chain; applicability/normalization/weights/units/tolerance/near-zero | `AGENTS.md:37` | `AGENTS.md:66` | сохранить; original paragraph retained |
| Observation/inference/hypothesis/proposal; source/artifact locators; missing не zero | `AGENTS.md:40` | `AGENTS.md:69` | сохранить; original paragraph retained |
| Не менять model/channels/grid/basis/window/tolerances ради pass/cost | `AGENTS.md:43` | `AGENTS.md:72` | сохранить; original paragraph retained |
| Прозрачный reference; независимый oracle | `AGENTS.md:46` | `AGENTS.md:75` | сохранить; original paragraph retained |
| Без необоснованных требований gain/I–V/bias/J(E); finite basis local current | `AGENTS.md:48` | `AGENTS.md:77` | сохранить; original paragraph retained |
| Read/postprocess existing data; estimate extraction/RAM/I/O; archive scripts не execute | `AGENTS.md:54` | `AGENTS.md:83` | сохранить; original paragraph retained |
| Новые SCBA/Poisson/profile/benchmark/env/full checks: stage+finite shared budget | `AGENTS.md:59` | `AGENTS.md:88` | сохранить; original paragraph retained |
| Stop бесконечных reruns и без повторного разрешения approved stage | `AGENTS.md:63` | `AGENTS.md:92` | сохранить; original paragraph retained |
| Bootstrap measured safe maximum; profiles/VM/build-slice/Nix/Julia; reserves; production return | `AGENTS.md:66` | `AGENTS.md:95` | сохранить; original paragraph retained |
| Four-role+strict nginx preflight | `AGENTS.md:75` | `AGENTS.md:104` | сохранить; original paragraph retained |
| Executable paths/flake inputs/builder/Git index ownership/fresh admission | `AGENTS.md:77` | `AGENTS.md:106` | сохранить; original paragraph retained |
| Admin read-only Git GIT_OPTIONAL_LOCKS=0; failed logs/new attempt | `AGENTS.md:79` | `AGENTS.md:108` | сохранить; original paragraph retained |
| Native reuse only same derivation/contents/test contract; new root no inherited pass | `AGENTS.md:80` | `AGENTS.md:109` | сохранить; original paragraph retained |
| Engineering/signatures/staging/guests/restore/final CI/science separate | `AGENTS.md:82` | `AGENTS.md:111` | сохранить; original paragraph retained |
| No repeated approval; missing inventory/admission/credentials blocker | `AGENTS.md:85` | `AGENTS.md:114` | сохранить; original paragraph retained |
| One final CI on final-ready ref; no automatic reruns | `AGENTS.md:88` | `AGENTS.md:117` | сохранить; original paragraph retained |
| PR scope no inferred merge/deploy/cancel/server; docs/skill-format checks included | `AGENTS.md:91` | `AGENTS.md:120` | сохранить; original paragraph retained |
| Docs-only no numerical environment; disclose absent numerical checks | `AGENTS.md:93` | `AGENTS.md:122` | сохранить; original paragraph retained |
| Owning responsibilities; no formulas/acceptance in UI/scheduler/agent | `AGENTS.md:98` | `AGENTS.md:127` | сохранить; original paragraph retained |
| Owning component PR then published gitlink; arrays/depot/secrets/private inventory excluded | `AGENTS.md:103` | `AGENTS.md:132` | сохранить; original paragraph retained |
| Frozen independent reviewer inputs without diagnosis; disagreements retained | `AGENTS.md:108` | `AGENTS.md:137` | сохранить; original paragraph retained |
| Claims/evidence/limits/decision; diff/links/format before PR | `AGENTS.md:114` | `AGENTS.md:143` | сохранить; original paragraph retained |
| Blocking review criteria with reproducible locator | `AGENTS.md:121` | `AGENTS.md:150` | сохранить; original paragraph retained |
| Fixed light all web incl states/charts/dialogs; no OS autodark/alternative; contrast | `AGENTS.md:128` | `AGENTS.md:157` | сохранить; original paragraph retained |

## Root routing: новые уточнения без нового task contract

| Требование SI03 | Before / основание | After | Disposition |
| --- | --- | --- | --- |
| Восемь action classes | SI03 handoff + SI02 canonical contract | `AGENTS.md:41`–48 | изменить: docs/source/metadata/targeted/environment/build/live/science различаются |
| Один reusable девятиполевой contract | accepted working SI02 `agent-review-workflow.md#разбиение-до-ready` | `AGENTS.md:35` | сохранить: только ссылка, ни второго task form, ни framework |
| Current direct EXEC сильнее historical PLAN; уже выданное не переспросить | accepted working SI01/02 + coordinator current-authority brief | `AGENTS.md:50` | изменить: explicit route; assignment/READY не создают grant |
| Technical BIND/READY/fresh admission и CP-EXCEPTION | P1 PERM06–18, autonomy §4; owner contracts | `AGENTS.md:53` | сохранить; готовое authorized действие не требует нового human approval |
| Missing блокирует dependents; later resource grant сохраняет caps/reserves/CI-once | accepted working SI02 route + latest-grant constraint | `AGENTS.md:54` | сохранить; без inventing inventory/admission |
| Protected old S01/foreign VM/jobs/disks/data + failed raw/log/provenance | P1 PERM09–13 и coordinator brief | `AGENTS.md:57` | сохранить; campaign grant не доказывает ownership |

## Восемь owning component dispositions

Каждая строка ниже относится к отдельному будущему owning PR. Full-suite/build команды остаются доступными и required для своего этапа; docs-only exception ограничен текстом/ссылками, а executable examples, recipes, API/schema/config/data/code требуют relevant checks. Missing runtime обозначается limitation, не pass.

| Component | До: универсальная команда / действующие обязанности | После: qualified command route | Сохранённые обязанности / disposition |
| --- | --- | --- | --- |
| Core `QCLNEGF.jl` | `deno task check/test/docs` перед любым change; dimensional model/normalization/index/assumptions; independent oracle; threshold protection; reference independence; convergence/discretization/validation; public types/callbacks coordinated with Runner; in-memory ownership; root gitlink CI | Текст/links/format без Julia/install/full suite/render; code relevant checks; TS `check` отдельно от Julia `test/docs`, возможный instantiate явно назван; full stages имеют finite shared budget | Все physics/ownership/coordination/CI абзацы сохранены дословно после первой command line; изменить только применение команд |
| Runner `QCLNEGFRunner.jl` | `deno task check/test/docs` универсально; public adapter tests, invalid fields/units, identity/checksums/exact restart, corrupt/incompatible+positive input; core one-way dependency; Contracts/Results/AiiDA coordination; no exit acceptance; no hosts/secrets/studies | Тот же docs-only/source vs TS vs relevant Julia/runtime vs full test/docs/environment route | Все абзацы после первой command line сохранены дословно; изменить только применение команд |
| AiiDA | Python3.14 workspace, standalone install, complete `pytest`, non-integration group, temp SQLite/synthetic executable, namespace/temp requirements, no extra lock, `python -m build`; immutable plan bytes; failure/malformed/continuation/precision/identity semantics; Runner owns staging | Docs-only static route; selected pytest cases+failure/healthy controls in prepared env; install/full `pytest`/group/build explicitly assigned finite stages; no profile marker claim broadened | Все immutable-science/schema/staging and source-lock ownership requirements сохранены; namespace/storage/external synthetic facts не изменены; изменить cost routing |
| Contracts | Focused behavior tests; install+all README commands; compatible producer/readers, explicit contract revision, no process/export science pass; nonconfidential issue input; infrastructure review; MIT | Docs-only static route; code/schema relevant tests with rejected+healthy controls; README install/full suite/distribution build separate finite stages | Все contract compatibility/revision/acceptance/secret/source graph/trusted review/license правила сохранены; изменить cost routing |
| Platform | `nix develop --command deno task check`; five private-site configs for NixOS changes; relevant Nix; Slurm/NFS/identity/scratch/cgroup → `slurm-vm` logs; provider checks; numerical ownership; locks/secrets/CI isolation | Docs-only static; prepared relevant operational checks; full Deno+Python pipeline distinct; five configs сохранены; VM-boot check native stage+admission/envelope; four-role+nginx before heavy bootstrap; missing private input only dependents | Все перечисленные commands/conditions, numerical ownership, secret prohibition and trusted CI safeguards retained. Five config evaluations are not substituted for four-role preflight. Изменить cost routing |
| Portal | Python3.14/Node24; all README commands; API+client+negative tests; scientific-vs-exit; token secrecy; source/package locks; no generated assets; sanitized issues; root CI | Docs-only static; prepared relevant backend/client checks; full/install/build stages explicit; `test:frontend` npm install/test/typecheck/build disclosed; link to current fixed-light AGENTS | API coordination, security, generated asset/lock boundaries, sanitized input, root graph CI retained дословно; fixed-light strengthened by local link. Изменить cost routing |
| Research | validator+tests README; `qcl-negf plan` each changed entrypoint with matching Runner; Slurm transport; convergence/accuracy separate; study sources/units/variants/reachability; scientific rationale/DOI/uncertainty/conditions; no fake accepted label; provenance no arrays/logs/secrets; isolated untrusted CI | Docs-only static; changed inputs/validator code → relevant structural checks; changed entrypoint → assigned matching Julia semantic plan check; preparation/full suite separate; transport science stage/freeze/admission/budget | Все study/scientific rationale/data/provenance/untrusted CI правила сохранены; structural-vs-science not relaxed; изменить scope применения plan/install |
| Results | Same generic issue/test/install/README directions as Contracts; compatibility/contract revisions/no process/export science acceptance, trusted root CI/MIT | Docs-only static; selected reader/code/schema tests; full/install/build separate; README actual Julia SCBA integration explicitly assigned numerical stage+matching env+finite budget | Все contract/producer/reader/data/secrets/CI правила сохранены; SCBA integration disclosure prevents hidden solver run; synthetic/native fixture evidence не становится physical acceptance. Изменить cost routing |

## Static scenario matrix — ожидаемая маршрутизация, не runtime witness

| Scenario | Expected route | Ограничение / решение |
| --- | --- | --- |
| Поправка русской фразы или Markdown link, Julia отсутствует | Diff+link/anchor+format; disclose no numerical/rendering checks | Docs-only READY может продолжаться; сохранить |
| Изменён executable doc example или docs recipe | Relevant semantic/render/build check в assigned stage; no text-only exemption | Build/runtime evidence до его claims; сохранить |
| Исправлен Runner/Core numerical/public API behavior | Relevant Julia fixtures, independent oracle; cross-component callback/type checks where applicable | `deno task check` alone не behavioral acceptance; сохранить |
| Исправлен Platform source, private inventory missing | Доступные prepared source/unit checks; dependent native/preflight pending | Не inventing inventory, unrelated docs продолжаются; сохранить |
| Active B/G1/S1 и technical BIND/READY fulfilled | Proceed approved action within scope+budget without per-hash human approval | Old PLAN не отзывает EXEC; no auto-grant from candidate; сохранить |
| Active B/G1/S1, fresh host admission missing | Block dependent BUILD/OPS/SCI action; collect only within active read scope | No fabricated admission; independent READY continues; сохранить |
| Results Python-reader change prompts full README commands | Select relevant Python checks; actual SCBA integration only separate assigned numerical stage | No hidden Julia producer; сохранить |
| New scientific model/tolerance relaxation/public release/foreign job cancel/second final CI | CP-EXCEPTION/operator for outside approved predicates | Не выполняется этим design; сохранить |
| Unknown remote operation outcome | Canonical workflow requires persisted-ID reconciliation before repeat | SI03 не создаёт rerun permission; сохранить |
