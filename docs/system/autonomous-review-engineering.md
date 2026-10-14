# План автономного инженерного review

> Для исполнителя: выполнять source-bound задания по checkbox; использовать
> `superpowers:subagent-driven-development` либо `superpowers:executing-plans`
> как организацию конечного аудита. Шаги изменения кода и запуска tests сюда
> не включены. После отдельного поручения их задаёт готовый owning ticket.

**Цель:** завершить RV02/RV04–07/RV09/RV11–15 воспроизводимыми инженерными
выводами и ограниченными заданиями исправлений, пригодными для автономного
выполнения. **Архитектура работы:** факты принадлежат owning component;
cross-component вывод связывает конкретные producer/consumer. Формализация,
документация, код и наука равноприоритетны. **Средства:** статическое чтение
Julia/Python/TypeScript/Nix/HCL, native manifests, fixtures и saved receipts.
**Контракт:** [общий план](autonomous-review-plan.md),
[метрики](review-metrics.md), [архитектура](../architecture.md).

## Frozen inputs и полномочия

Эта редакция подготовлена 2026-10-14 на root
`e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` и его восьми gitlinks.
Gitlinks — authority состава, а перечисленные далее пути — локаторы, не
новый revision lock. Фактический dirty overlay сохранён отдельно от HEAD.
Для будущего прохода `S` — root HEAD + gitlinks **на момент запуска**;
локаторы e48… перепроверяются адресным чтением на S. Другой checkout требует
rebinding paths/symbols, без reset, rollback или обновления submodules к latest.
Frozen review corpus при подготовке прочитан из вспомогательного
`/tmp/qcl-autonomous-plan-20261014/baseline/`, receipt `snapshot.json`;
обязательные воспроизводимые inputs — S и опубликованный docs ref
`193f5bf8700b82e05f7e0f1fdd9c8f3ea0908f07`. Временный каталог не требуется
для будущего исполнения: исходный corpus читается по public docs ref.
Его отсутствие в локальной Git object database не означает отсутствия
опубликованных документов. Старые требования перепроверяются через RV00;
существующий механизм не становится обязательным только вследствие реализации.

В момент запуска master один раз назначает
`R=docs/implementation/comprehensive-review/<campaign>/`, где campaign содержит
UTC date, короткий root HEAD и sequence. Каждый RV пишет только свой `R/RVxx.md`;
master владеет progress. Перед чтением зафиксировать текущие HEAD/status/gitlinks
и отклонения от frozen inputs. При смене source прекратить зависимый вывод,
сохранить старый отчёт и оформить отдельное rebinding; не смешивать источники.
Наблюдения архивного audit о Portal `36837e98…` и AiiDA `53e2a205…` относятся
к отдельным refs; текущие gitlinks — Portal `10b6c871…`, AiiDA `69aa1309…`.

Предлагаемый envelope будущего статического аудита: общий предел master
6 часов, включая всех агентов и независимое review; до трёх работников,
если доступны. Atomic source-bound packet ≤20 минут, включая review;
максимум две коррекции готового отчёта после review. Resource/output caps
назначает [master](autonomous-review-plan.md): 96 KiB показанных extracts и
8 KiB отчёта **на packet**. Один `RVxx.md` может накапливать sections нескольких
пакетов; 8 KiB не является пределом целого RV. Отдельные host caps этот план
не вводит. Это плановые пределы, не измерения и не новое разрешение.
При исчерпании бюджета
опубликовать проверенный срез, незакрытые claims и следующий точный packet.
Сейчас выполняется только подготовка плана.

Минимальный протокол при порученном audit: прочитать actual `AGENTS.md`,
применимые component instructions и архитектуру; `git rev-parse HEAD`,
`git status --short`, `git submodule status --recursive`; далее `rg --files`,
адресный `rg -n`, чтение указанных symbols, manifests, imports и fixtures.
Не импортировать packages ради перечисления API. До любого будущего selected
check прочитать harness, fixtures и subprocess paths: он может вызвать Julia
producer, solver или сервис. Installation, full suites, builds, benchmarks,
profiling, VM/server actions и SCBA/Poisson требуют отдельного конечного
envelope. Private inventory и admission нужны runtime-проверкам, но их
отсутствие не блокирует public source audit. Секреты не становятся входом отчёта.

Пять сквозных failure classes распределены ниже: неоднозначный attempt (RV07/11),
bool/int/nonfinite и origin (RV07), crash во время публикации (RV06/11),
неизвестный исход submit/cancel (RV12), неверный imported source/assets (RV14).

## Единый выход и handoff

В каждом `RVxx.md`: вопрос; точные inputs/ref и dirty attribution; property
catalogue с denominator; source→producer→consumer→fixture→assertion; findings
с воспроизводимыми локаторами; negative case; metrical status; вывод для
исследователя, оператора и разработчика; таблица
«утверждение / свидетельство / ограничение / решение».
Решения: сохранить, изменить, дополнительно измерить, данных недостаточно.
Завершение audit означает достаточный отчёт, включая gaps; оно не означает
runtime pass или научную приёмку.

Для каждого предлагаемого исправления записать trigger, owner, точные файлы,
immutable inputs, сохраняемый invariant, минимальный patch scope, различающий
check с expected outcome, budget/stop, exclusions и permission class.
Пометка `READY` допустима только при известном локальном контракте, invariant
и проверке; иначе указать конкретный недостающий выбор/вход. Наличие finding
не разрешает произвольный refactor. Реализация — owning component PR,
независимое review и затем опубликованный root gitlink. Один writer на
component; конкурирующие tickets сериализуются. Existing Results PR6
продолжается без дубликата. Первому независимому рецензенту передать вопрос
и первичные sources без готового диагноза; разногласия сохранить с дешёвым
различающим check. Недоступный вход задерживает только зависимую часть.

## Исполнимые задания

### RV02 — переносимость existing Results PR6

Owner Results; вход `fe27a2a9…`,
`components/qcl-negf-results/tests/test_equilibrium_diagnostics.py`:
`EXPECTED_RESULTS`, `EXPECTED_CONTRACTS`, fixture `archive`; existing
[PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6),
base `fe27a2a9ed065f9afacecc84113311f30d0c68d6`, head
`a1492b7b86b788885eff683ac71ca1167cbbaff1`.

- [ ] Прочитать exact diff и harness; при недоступном candidate сохранить gap,
  продолжить baseline portability audit. Не подменять candidate текущим checkout.
- [ ] Связать проверку owning imports с `pyproject.toml`, fixtures и manufactured
  oracle `inverse2`/`literal_sum`; отдельно проверить неизменность assertions.
- [ ] Описать negative case: чистый checkout другого пользователя и импорт
  чужой установленной версии. Подготовить selected-check ticket без запуска.
- [ ] Выпустить `R/RV02.md` с решением о candidate и способом продолжить PR6.

Приёмка: устранение личных paths сохраняет отказ неверного owning import;
неизвестный candidate не получает verdict. M06 — import links; M02 — только
existing exact-source report или `not_measured`; M05 — original repeats,
иначе `not_measured`. Будущий M02 check: после harness preflight
`coverage run --branch -m pytest -q tests/test_equilibrium_diagnostics.py`
на exact PR head; отчёт owning imports обязателен. Для M05 отдельный ticket
предлагает три одинаковых повтора этого файла, сохраняя все исходные logs;
это candidate proposal, не threshold pass и не доказательство отсутствия
flakiness. Число повторов и permissions фиксируются до запуска. Зависимость: candidate
diff, не terminal S01.

### RV04 — Core/Runner cohesion и impact

Входы: `components/QCLNEGF.jl/src/QCLNEGF.jl`, `src/domain/`,
`src/numerics/reference/`, `src/numerics/optimized/`; Runner
`src/QCLNEGFRunner.jl`, `src/core_api.jl`,
`src/application/coordinator.jl::run_sweep!`,
`src/composition/configured_execution.jl::execute_configured_run`.

- [ ] Построить include/import/call/mutation карту одного operating-point→persist
  пути; отдельно dynamic, file и orchestration edges.
- [ ] Проверить владельца каждого эффекта и hotspot по состояниям/exception
  paths, сопоставить relevant tests.
- [ ] Рассмотреть negative case: перенос persistence в Core или общего helper
  в oracle; предложить только bounded alternatives с invariant.
- [ ] Сохранить `R/RV04.md`: карта и change-impact tickets.

Приёмка: source каждого edge, owner и affected interfaces/tests известны;
LOC не объявлен дефектом. M12 — SCC/forbidden edges выбранного graph; M13 —
объяснённые hotspots, численный CFG неизвестен без инструмента. RV03 нужен
только для утверждения спорной локальной границы, не начала чтения.

### RV05 — AiiDA actor и HTTP complexity

Входы: Portal `src/qcl_negf_api/service.py::AiidaService._call/close/open_artifact`,
`api.py::create_app/ClosingStreamingResponse`, `exports.py::ExportStore`;
AiiDA `src/aiida_qcl_negf/service.py`, `workflow.py`; Portal
`tests/test_service.py`, `test_stream_disconnect.py`, `test_exports.py`.

- [ ] Табулировать profile/loop/handle owners, queue, deadlines, errors и close;
  читать assertions о единственном thread и освобождении reader.
- [ ] Проследить exception/cancel пути HTTP→actor→AiiDA и export→spool.
- [ ] Описать stalled operation и disconnect как negative cases; отделить
  подтверждённый synchronous wait от недоказанного production hang.
- [ ] Выпустить `R/RV05.md` с targeted fixture tickets и contract gaps.

Приёмка: каждое обещание responsiveness имеет boundary и witness/unknown.
M04 — property×failure catalogue; M13 — состояния/fan-out выбранных функций.
Зависимость RV07: только semantics выбранной операции.

### RV06 — Platform lifecycle ownership

Входы: Platform `ops/application_release.py::lifecycle_owner/activate/deliver_cli/guard`,
`ops/worker_lifecycle.py::shutdown_step/startup`, `ops/bootstrap_build.py::main`;
`tests/test_application_release.py`, `test_worker_lifecycle.py`,
`test_worker_shutdown_intent.py`, `test_build_admission.py`.

- [ ] Выписать desired/observed states, flock scope, durable intent, ready/admission
  publications и recovery transitions.
- [ ] Сопоставить assertions со сценарием crash между profiles, environment,
  allowlist и ready marker; проверить отсутствие второго lifecycle writer.
- [ ] Разобрать negative cases stale admission и disappeared job без receipt.
- [ ] Выпустить `R/RV06.md`, указать публичный fixture и отдельный live check.

Приёмка: неопределённый исход не открывает admission по предполагаемому успеху.
M04 — отказные переходы; M10 — declared managed objects и неизвестный live drift;
M11 — role×scenario catalogue, native cells `not_measured`. Private inputs
ограничивают runtime cells, сохраняя source conclusions.

### RV07 — Contracts и consumer semantics

Входы: Contracts `src/qcl_negf_contracts/schemas/`,
`artifacts.py::validate_export_receipt/validate_commit/validate_execution_progress`;
Runner `schema/PROVENANCE.json`, `src/infrastructure/config/json_schema.jl`,
`configuration_contract.jl`; AiiDA `service.py::_select_child/get_export_plan/list_artifacts`;
Portal `exports.py::ExportStore.create/_prepare`, `api.py::ExportRequest`.

- [ ] Построить producer/consumer/version/migration matrix: attempt, missing,
  precision, limits, effective origin; найти existing schema drift guard.
- [ ] Сопоставить `tests/test_contracts.py`, AiiDA `tests/test_restart.py`, Portal
  `tests/test_exports.py`, Runner `test/contracts/draft_2020_12_configuration_contract.jl`.
- [ ] Задать valid/invalid corpus bool/int/NaN/Infinity/origin и два attempts:
  frozen plan и raw bytes должны иметь одну exact selection.
- [ ] Выпустить `R/RV07.md`; current и archived refs получить отдельные claims.

Приёмка: одинаковые schema hashes не заменяют guard; ambiguous export не
считается допустимым молча. M04 — corpus; M06 — schema identity edges;
M12 — contract ownership. От RV00 требуется лишь решение спорного ограничения.

### RV09 — tests, свойства и независимость oracle

Входы: Core `test/physics/scalar_dyson_and_spectral_identity.jl`,
`manufactured_periodic_poisson_solution.jl`,
`analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl`,
`test/numerics/physics_first_exact_scba_candidate_equivalence.jl`;
Results manufactured fixture RV02; component harnesses и relevant tests RV07.

- [ ] Построить property→producer/consumer→fixture→assertion→mock-limit matrix.
- [ ] Проверить dependency graph analytic/manufactured oracle; общий helper
  и agreement reference/optimized отметить как ограниченную независимость.
- [ ] Описать negative mutation веса/знака/attempt, которую assertion различает;
  новые fixtures оставить tickets с применимостью из RV08.
- [ ] Выпустить `R/RV09.md`, выбрать минимальный будущий selected check.

Приёмка: наличие test отделено от исполнения и результата. M02 — repo×language
scope; Julia branch `not_measured` без проверенного инструмента. M04 — failure
denominator, M05 — только реальные comparable repeats. RV08 предоставляет
определения выбранных scientific properties, не блокируя harness inventory.

### RV11 — publication, checkpoint и raw preservation

Входы: Runner `src/infrastructure/persistence/point_artifacts.jl::commit_point_artifacts/load_recovery_commit`,
`atomic_files.jl::_atomic_replace_file`,
`src/infrastructure/runtime/filesystem_repository.jl::save_runtime_checkpoint!`,
`src/composition/scratch_execution.jl::stage_result_tree`; Results
`state.py::StateReader/verify_recovery_bundle`, `archive.py::verify_archive`.

- [ ] Проследить generation→commit→receipt→pointer→reader, fsync и pruning;
  назвать сохраняемые raw/model/plan/attempt invariants.
- [ ] Читать Runner `test/infrastructure/scratch_execution.jl`,
  `production_restart_validates_metadata_and_restores_state.jl`, Results
  `tests/test_state_reader.py`, `test_series_commit_identity.py`.
- [ ] Составить partial-write/ENOSPC/NFS-loss/worker-loss packet;
  hash-valid external HDF5 и wrong attempt — negative cases.
- [ ] Выпустить `R/RV11.md`, раздельные local durability и production claims.

Приёмка: сохранены original arrays и failure evidence; receipt не science pass.
M04 — fault catalogue; M09 — recovery timeline requirements, RPO/RTO
`not_measured` без опыта. RV07 даёт выбранную identity semantics;
RV01 нужен только для архивного экземпляра, не synthetic/source audit.

### RV12 — retry, timeout, submit и cancellation

Входы: AiiDA `workflow.py::attempt_decision/QCLExecutionRestartWorkChain/QCLPlanWorkChain`,
`calculation.py::prepare_for_submission/_setup_metadata`, `service.py::kill_run`;
Runner `configured_execution.jl::_check_solver_run_budget`, staging RV11;
Platform `application_release.py::command`, `worker_lifecycle.py::jobs`.

- [ ] Составить parent/CalcJob/Slurm/Runner budgets, ownership и retry matrix;
  проверить сохранение spent budget после recovery.
- [ ] Читать AiiDA `tests/test_restart.py`, `test_submission_identity.py`,
  Runner `test/application/restored_stage_progress_consumes_the_original_budget.jl`.
- [ ] Разобрать submit acknowledged-but-response-lost, ambiguous scheduler owner,
  daemon unavailable и cancel failure; никакого скрытого duplicate submit.
- [ ] Выпустить `R/RV12.md` с exact selected check и отдельным native envelope.

Приёмка: завершение parent, job stop и recovery eligibility различены.
M04 — отказные пары; M11 — native submit/cancel cells неизвестны.
Зависимость: RV11 receipt invariant, RV06 lifecycle boundary выбранного пути.

### RV13 — публичный restore и границы private site

Входы: Platform `flake.nix`, `modules/state-archive.nix`, `storage.nix`,
`ops/state_archive.py::pack/verify/restore_admission/stop_services`,
`docs/state-archive.md`, `docs/host-storage.md`, IaC `tofu/proxmox/` и
`tofu/local-lab/`; root `docs/single-server-deployment.md`.

- [ ] Сопоставить четыре roles, config/storage owners, DB+repository consistency,
  backup/reinstall/cold-start и foreign VM/data exclusions.
- [ ] Читать `tests/test_state_archive.py`, `test_proxmox_storage_contract.py`;
  выделить synthetic bytes restore и реальные PostgreSQL/service гарантии.
- [ ] Описать negative cases mismatched DB/repository generation и общий
  filesystem AiiDA/Slurm; составить sanitized inventory contract без секретов.
- [ ] Выпустить `R/RV13.md`; продолжить public audit при missing site inputs.

Приёмка: отсутствующий admission блокирует только operation; сохранение
mutable datasets явно проверяемо. M09 — incident/recovered timeline;
M10 — managed objects; M11 — role/backend/scenario cells. Live restore
`not_measured`; зависит от RV06/11 outputs лишь для соответствующих transitions.

### RV14 — source/build/import/runtime closure

Входы: root `ops/git.ts::sourceGraph`, `ops/release.ts`, `ops/solver.ts::buildSolver`,
`ops/application_cd.ts::deploymentManifest`, `ops/ci.ts`, `nix/solver.nix`,
`flake.lock`, `uv.lock`, `julia/Manifest.toml`; Runner `Project.toml`,
`tools/prepare_workspace.jl`; Portal `hatch_build.py::CustomBuildHook.initialize`,
`frontend/package-lock.json`.

- [ ] Построить selected-source→lock→derivation→artifact→import/runtime chain,
  включая standalone versus workspace Core resolution.
- [ ] Прочитать saved receipts при наличии; проверить reused native output
  только по derivation, contents и native test contract, сохранив failed logs.
- [ ] Описать stale compiled assets и пакет `0.2.0` из другого commit как
  negative cases; связать Portal assets с source/lock.
- [ ] Выпустить `R/RV14.md` и отдельные rebuild/import tickets.

Приёмка: новый root ref не наследует full release acceptance. M06 — identity
links; M07 — declared bitwise outputs; M08 — consumer properties; последние
два `not_measured` без bounded rebuild. Будущий M07 check: два независимых
rebuilds одной derivation, SHA256 всех заранее declared outputs и byte diff;
это отдельный build envelope, без повторного final CI. Будущий M08 check:
`solver_executable self-check` через `solver_self_check`, receipt
`qcl-negf-self-check-v1/completed`, `scientific_accepted=false`, плюс declared
consumer fixtures. M20 — elapsed до claim; CPU/RSS/I/O неизвестны без
telemetry. RV01 нужен только для installed/archive цепочки.

### RV15 — security boundaries и rejected paths

Входы: Portal `api.py::BodyLimit/create_app/byte_range`, `settings.py::Settings`,
`exports.py`; AiiDA `validation.py::validate_scratch_root/scheduler_options`,
`calculation.py::prepare_for_submission`, `service.py::_artifact_path`;
Platform `application_release.py::read_protected_file/freeze_ssh_trust`,
`ops/bootstrap_ownership.py`, root `.github/workflows/`.

- [ ] Составить auth/read/submit/cancel/download, executable input и trusted CI
  boundary matrix; учитывать single trusted team scope.
- [ ] Читать Portal `tests/test_api.py`, AiiDA `tests/test_artifact_locator.py`,
  Platform `tests/test_bootstrap_ownership.py`; найти public logging/redaction.
- [ ] Описать path traversal, symlink/FIFO, oversized body и untrusted executable
  как negative cases; не читать реальные token/private inventory.
- [ ] Выпустить `R/RV15.md` с минимальными rejected-input tickets.

Приёмка: threat assumptions, failure locators и пределы mock известны;
source audit не утверждает отсутствие всех уязвимостей. M04 — rejected paths;
M12 — trust edges. RV07/12 дают только конкретные contract/cancel outputs.

## Завершение этой редакции

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все 11 инженерных RV разложены до автономного audit | Точные symbols, checkboxes, negative cases и `RVxx.md` выше | Будущее исполнение требует task capsule и общего envelope | сохранить |
| Public baseline доступен независимо от live/site данных | HEAD/gitlinks, адресно прочитанные owning source/tests/manifests | Candidate PR6 object отсутствует локально; remote diff ещё не прочитан | сохранить |
| Runtime, coverage, rebuild и recovery не установлены | На этапе автора выполнено только чтение и статическая проверка плана | Suites/builds/server/solver/profile не запускались | данных недостаточно |
