# DOC02 — независимый CP-DESIGN review

**Вердикт: PASS для frozen документационного design-пакета; блокирующих замечаний к семи candidate docs нет.** Это разрешение перейти к узкой owning implementation, а не CP-CODE текущего checkout, публикация, browser/native/runtime или scientific acceptance. Есть одно неблокирующее расхождение в записи author check, E1 ниже; его следует исправить в последующем отчёте, сохранив исходную запись.

## Проверяемый пакет и authority

Корень: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Фактический HEAD: `965ebed95d2b627423805d10c46d0ae8dd425e9d`.
Read-only `git ls-tree HEAD` подтвердил выбранные gitlinks:
Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, Runner `23860d9e660a3cddf6cb5203d449d1b62f3745a1`, Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`, Portal `d28d076c83611278153752d94cc3729d91b32667`.

Фактический recursive submodule status показывал Core `+f7b108bef206d2b2dc5afe0306b2dff60d27ac59` и Portal `+2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; остальные шесть submodules совпадали с gitlinks. Эти рабочие HEAD не приняты за selected composition. Дополнительно read-only сравнение Core f5→f7 показало только `CONTRIBUTING.md`, `docs/src/development/review_oracle_contracts.md`, `test/numerics/final_state_alignment_oracle.jl`; использованные production source bytes совпадают с selected f5 и проверены непосредственно через Git.

Входные SHA-256 проверены независимо:

| Артефакт | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc02-candidate/full.patch` | `cc0bc5f923da2bda21b5680e7fba03529504aba81c611ef2308369b356e4af2e` |
| `/tmp/qcl-doc02-candidate/manifest.json` | `68b28c09af6ccd821559577375a43bd1a460e53e213869cb45dd71ff0577d942` |
| `/tmp/qcl-doc02-candidate/journeys.md` | `4f9c7318512875e2158a114f221107087fee14214dcca915a7fd93b505f24b04` |
| `/tmp/qcl-doc02-candidate/report.md` — прочитан последним | `ce7a361f55421f8a1ad07b61e107c7ad3025d54e569f3968e0f1fae1363e17c8` |

Manifest — inventory этого proposal, не второй lock состава. Все 14 baseline/candidate snapshot hashes и sizes совпали с manifest. Все семь baseline файлов и все 28 source-witness hashes/sizes независимо совпали с `git show <selected-ref>:<path>`. Все семь настоящих owning docs по окончании review всё ещё byte-equal baseline; candidate не принят за реализованный source.

Начальный и конечный `git status --short` совпали. Существовавшие изменения: 12 skill/UI/reference файлов четырёх qcl skills; Core/Portal gitlinks; `execution/checkpoint.json`, `execution/qcl-targeted-receipt-census.json`; untracked DEV05 D2 review, DEV24 auth report, SCI04 design-v2 report/review, SI04 checkmatrix/design report/review и DEV05-GREEN-2/DEV24-GREEN-2 test directories. Reviewer не изменял ни один из них и не использовал их как current scientific acceptance.

## Основание и способ проверки

Сначала прочитаны root AGENTS, architecture, применимый `qcl-physics-audit`, DOC02 handoff, текущие requirements/DOC01 dispositions и исходные owning docs/source. Затем просмотрен семифайловый patch и последовательно выполнены три reader tabletop scenarios; author report прочитан после независимой сверки. Это один отдельный reviewer, а не три независимых человека или три runtime опыта.

Нормативные locators: root `docs/implementation/review-closure-2026-10-19/documentation-instructions.md:46–71`; `docs/system/requirement-dispositions-2026-10-19.md`, строки D09/D11 и таблица «S01 и scope науки»; `docs/architecture.md`, Source composition/Scientific execution/Verification boundaries. Tutorial-first дополняет полный expert reference; quantitative optical validation не обещается. Текущая SCI05 C1 proposed raw-record работа не подставляется вместо selected implementation.

## Три reader scenarios

| Читатель / вход | Проверенное действие и ожидаемый результат | Первичные locators | Ограничение / решение |
| --- | --- | --- | --- |
| Исследователь с QM/semiconductor подготовкой; одно final state с model/plan/execution/point/attempt identity | Candidate Core `09_scba.md:18` сначала отделяет raw map residual от mixed step. Synthetic Σ=1, candidate=2, α=10⁻³ даёт шаг 0.001 и raw residual 0.4999999999999975. Переход в `12_validation.md:13` ведёт к тому же published U/G, fresh candidate, отдельному r_U и статусам/units/weights/floor/threshold origin. `not_measured` не превращается в ноль/pass; discretization/experiment не выводятся из stationary acceptance. | Core f5 `src/numerics/reference/final_audit.jl:38–85` и `:138–242`; `acceptance_metadata.jl:21–128`, ветвь r_U; `validation.jl::validate_solution`, особенно fresh merge и Poisson по `solution.n`; `reference/solver.jl:229–252`; optimized `production_solver.jl` final publication/audit | Source/maths и навигация согласованы. Нет raw production locator и нет утверждения, что raw audit record уже сохранён. Исторический spectral пример сохранён с явным provenance gap. **Сохранить design.** |
| Разработчик; complete base fixture и два override файла | Candidate Runner `configuration.md:9` даёт конкретные YAML и обычный неисполняемый Julia fence. Порядок base,first17,second23 даёт 23/second; обратный — 17/first. Missing/empty history даёт `nothing` при существующем значении. Таблица различает физический смысл/formula, numeric value, assigning origin и effective execution plan; `energy_chunk` — scheduling bound по числу узлов, а не ΔE. `application:auto_exact` ограничен соответствующим production planner path. | Runner 238 `test/application/configuration_merge_order_and_fail_closed_validation.jl:5–41`; `src/application/configuration_types.jl:209–232`; `auto_strategy.jl:39–70`, `:453–523`; Contracts 02a run schema; retained `ExecutionPlan` API | Пример воспроизводит исходные fixture inputs; это source expectation, не runtime receipt. Equal 64/default не объявлен origin. Полная causal chain не приписана одному lookup. **Сохранить design.** |
| Оператор; interrupted execution и frozen identity/бюджет | Candidate Runner `results.md:24`, public API `:7` и root runbook `:267` начинают с цели recovery. Pending/progress недостаточны. Reader проверяет current, при corruption — previous; оба missing/invalid дают явную ошибку с сохранением evidence. Import — новый явно разрешённый attempt N>source, с compatibility/prior-final/cumulative-work boundaries. `run-plan` явно назван вычислением. | Runner 238 `point_artifacts.jl:565–576`, `:682–709`; `test/infrastructure/bounded_portable_recovery.jl:7–32`; `scientific_execution.jl:490–520`; `production_state.jl::load_production_restart`; `cli.jl` run-plan option dispatch; Contracts artifacts/output policy | Внутренний selector не объявлен новым public API. Директория/receipt status не заменяют readback. Нет implicit cold start, pointer repair или удаления failed attempt. Local receipt не native/LAN restore и не scientific acceptance. **Сохранить design.** |

Числа и размерности проверены по owning evaluator, а не по согласованности двух текстов: r_Σ использует unweighted norms и additive 10⁻¹⁴; radial passport явно включает 1/(2π); current-change floor — 10⁻¹² A/m²; r_U — абсолютная scaled Hartree energy разность с индикатором r_U E0 в eV. Новый текст не меняет строгие inner/outer подтверждения, конечный evaluator или project thresholds. `r_D` относится к stored total Σ, candidate residuals — к свежей несмешанной Σ при том же published U/G.

## Dispositions всех семи файлов

Пути ниже относительно `/tmp/qcl-doc02-candidate/candidate/`; baseline находится в соседнем `baseline/`.

| Owner / path | Disposition | Основание / граница |
| --- | --- | --- |
| Core `components/QCLNEGF.jl/docs/src/theory/09_scba.md` | Изменить owning docs по proposal | Короткий вход, корректный synthetic raw/mixed пример, прежний expert SCBA сохранён. |
| Core `components/QCLNEGF.jl/docs/src/theory/12_validation.md` | Изменить owning docs по proposal | Final-state route, passport interpretation, historical evidence limitation; raw records не выдуманы. |
| Core `components/QCLNEGF.jl/docs/src/developer/traceability.md` | Изменить owning docs по proposal | Source/function/criterion chain дополняет прежние formula tables; нового evaluator нет. |
| Runner `components/QCLNEGFRunner.jl/docs/src/user/configuration.md` | Изменить owning docs по proposal | Реальные 17/23 inputs, observable lookup boundary и четыре вида facts/origins. |
| Runner `components/QCLNEGFRunner.jl/docs/src/user/results.md` | Изменить owning docs по proposal | Goal→verify→import/error; recovery не scientific verdict. |
| Runner `components/QCLNEGFRunner.jl/docs/src/api/public.md` | Изменить owning docs по proposal | Таблица входов; старые `@docs` blocks сохранены буквально, optics deferral явен. |
| Root `docs/single-server-deployment.md` | Изменить owning docs по proposal | Operational recovery route с ссылками на owners; формулы и strict acceptance rules не скопированы в runbook. |

Изменения ограничены этими семью Markdown files. UI/assets/source/schema не меняются; light-theme policy не нарушена. Это не доказательство browser contrast/readability/offline serving. Owning Core/Runner PR и последующее опубликованное gitlink обновление остаются отдельными integration шагами. Cross-component immutable links проверены как ссылки на выбранные baseline references; они сами не публикуют новые candidate sections.

## Свежие статические проверки

1. Проверены 33 добавленных Documenter reference: каждый target найден в explicit `@id` либо существующем `@docs` соответствующего owner corpus с candidate overlay; unresolved 0. Это текстовая проверка, не Documenter execution.
2. Добавленные selected-commit links: 13 уникальных repository/ref/path targets (14 occurrences); локальный Git подтвердил существование всех. `point_artifacts.jl#L682` указывает на `_verify_recovery_pointer`. HTTP/public availability не проверялась.
3. Все пять added relative links существуют; все прежние explicit anchors сохранены. Старые `@docs`/`@meta` blocks byte-content неизменны; fence parity корректна; новых executable docs blocks нет.
4. `git apply --whitespace=error --check /tmp/qcl-doc02-candidate/full.patch` из immutable `baseline/`: exit **0**, вывода нет. Patch не применялся.
5. `git diff --no-index --check /tmp/qcl-doc02-candidate/baseline /tmp/qcl-doc02-candidate/candidate`: exit **1**, stdout/stderr пусты; whitespace diagnostics нет. Не подменять этот exit code нулём; см. E1.
6. Synthetic arithmetic пересчитана Python Decimal; target Julia/imports/fixtures не исполнялись. Baseline/snapshot/source hashes и seven actual-owning-doc equality проверены независимо, как описано выше.

**E1 — неблокирующее расхождение evidence statement.** `/tmp/qcl-doc02-candidate/report.md:91` записывает для `git diff --no-index --check baseline candidate` «exit0». На том же frozen pair reviewer получил exit1 без diagnostics. В no-index сравнении differing trees это не свидетельство whitespace failure, но дословная запись exit0 не воспроизводится. Исправить последующую запись на фактический code/output либо приложить исходный raw receipt, не переписывая frozen original. Сам candidate независимо прошёл `git apply --whitespace=error --check` exit0; E1 не блокирует CP-DESIGN и не требует runtime rerun.

## Пределы вердикта

Не выполнялись target imports, Julia, tests, builds/render, browser, server/native действия, solver, profiling/benchmarks, распаковка архивов или чтение научных массивов. Никаких Git/file mutations owning checkout; единственный reviewer output — этот файл. Конечный review scope: один bounded source/docs review, не новая research campaign. Новый опубликованный source не наследует scientific/full-release acceptance.

DEV05 925 functional assertions и обязательный global healthy FAIL по r_sum получены из dispatch/context и прочитанного последним author report; исходный runtime receipt не перепроверялся в этом review. Их нельзя использовать как DOC02 test pass или device acceptance. SCI05 C1 raw-record candidate не является selected current и здесь не принят. Наличие ссылок/паспортов не закрывает missing raw provenance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| DOC02 design даёт три понятных reader journeys | Exact frozen seven-file patch; независимые tabletop walkthroughs и source/API/math locators выше | Один reviewer; без browser/human usability измерения | сохранить |
| Новый текст соответствует selected source и сохраняет expert/optical границы | Gitlinks, 28 exact source witnesses, evaluator/fixture reading, literal сохранение @docs/anchors | Source contract не доказывает runtime/device accuracy | сохранить |
| Семь owning docs можно реализовать по узкому design | Checked patch и owner dispositions | Actual owning checkout ещё baseline; нужны owning implementation/review/publication | изменить |
| Author whitespace-check exit0 воспроизведён | E1: fresh no-index exit1 без diagnostics; apply whitespace-error check exit0 | Original raw author receipt отсутствует | изменить |
| Browser/light/offline/native restore подтверждены | Только prose/static checks | Соответствующие DOC04/05/infrastructure stages не выполнялись | дополнительно измерить |
| Scientific acceptance или новый raw final-audit record установлен | В DOC02 таких measured artifacts нет | C1 pending; solver/arrays/runtime запрещены в этом review | данных недостаточно |
