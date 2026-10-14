# Автономный review: формализация и научная доказательность

Статус: исполнимый план review, 2026-10-14; карточки ещё не выполнены.
[Общий план](autonomous-review-plan.md) задаёт campaign, каталог `R`, source
binding, роли, общий бюджет и порядок независимого review. Здесь раскрыты
RV00/RV01/RV03/RV08/RV10; четыре цели и три роли сохраняют равный приоритет.
Карточка завершает объявленный анализ, даже когда научный ответ неизвестен.

## Общий вход и конечный выход

Source `S` фиксируется один раз при старте campaign по master: root HEAD,
выведенные из Git gitlinks и отдельно hashed dirty overlay. Наблюдавшийся
`e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` — исходный кандидат, к которому
относятся приведённые locators. При другом `S` исполнитель read-only находит
соответствующие symbols и фиксирует различия; submodules не обновляются до latest.
Policy/docs baseline — public root
`193f5bf8700b82e05f7e0f1fdd9c8f3ea0908f07` + конкретный path либо совпадающая
по hash frozen-копия из `/tmp/qcl-autonomous-plan-20261014/baseline/`.
Копия содержит только выбранные документы; отсутствующий там файл читается
на public ref. Dirty overlay, installed source и архивный source различаются.
Исполнитель проверяет identity и возвращает receipt вместе с отчётом;
только координатор обновляет `R/progress.md`.

Применяются [source audit](../implementation/comprehensive-review-source-audit-2026-10-14.md),
[метрики](review-metrics.md), [workflow](agent-review-workflow.md) и профильные
[physics](../../.agents/skills/qcl-physics-audit/SKILL.md),
[results](../../.agents/skills/qcl-results-analysis/SKILL.md),
[framing](../../.agents/skills/qcl-research-framing/SKILL.md).
Исторические locators из skill references проверяются на выбранном source.

Каждый пакет: один вопрос, максимум 20 минут общего wall time исполнителя
и рецензента, ≤1 CPU на чтение, ≤1 GiB рабочей RAM, ≤96 KiB показанных
extracts и ≤8 KiB отчёта на пакет. RV-отчёт агрегирует несколько пакетов.
Это предлагаемые caps внутри общего лимита 14 часов
из master, включая до двух корректирующих раундов; параллелизм не
умножает grant. Читаются metadata и адресные source sections; распаковка,
HDF5-постобработка или внешнее чтение требуют собственной оценки объёма.
Solver/build/tests/benchmark в эти пакеты не входят. Для будущего вычисления
CPU/RAM/wall/I/O/attempts остаются незаполненными до явного бюджетного контракта.

Отчёт содержит question, exact inputs, выполненные шаги, findings с категориями
«наблюдение/вывод/гипотеза/предложение», oracle, negative case, применимые M-ID,
неизвестные и таблицу «утверждение / свидетельство / ограничение / решение».
Для каждой роли указать доступное действие: исследователю — следующий научный
выбор, оператору — проверяемую identity/ресурсную границу, разработчику — owner
и адресный контракт; неприменимость обосновать.
Один writer собирает `R/RVxx.md`; независимый пакет передаёт ему замороженную
секцию со своим ID. Рецензент получает вопрос и первичные источники без диагноза.
Остановка: acceptance достигнут, budget исчерпан, вход недоступен либо следующий
шаг выходит за scope. Последние три случая оставляют точный gap и самый дешёвый
следующий источник, без автоматического повторения расчётов.

## RV00 — ledger актуальности требований

**READY:** каталогизация и поиск свидетельств. Owner Root с тремя ролями.
**Входы:** текущие уточнения пользователя; на docs ref —
`docs/system/{requirements,architecture,release-roadmap,implementation-entrypoint}.md`;
frozen `comprehensive-review.md` и source audit.

Исполняемые пакеты по 3–5 claims: `S01–S05`, `S06–S09`, `C01–C05`,
`C06–C09`, `C10–C13`, `R01–R04`, `R05–R08`, `R09–R12`, `I01–I05`,
`I06–I10`, `I11–I14`, `D01–D04`, `D05–D08`, `D09–D11`.
Claims вне каталога получают собственный locator и пакет, без раздувания
исходного denominator. Evidence прежней READY F01 переиспользуется адресно:
S01-first-gate в S01–S05, S07 в S06–S09, C01 в C01–C05; F01 целиком не
переносится в один пакет и не становится отдельным повторным аудитом.

- [ ] Извлечь точный текст, ID, дату, источник и последний статус каждой строки.
- [ ] Найти адресное decision evidence в текущем запросе, источнике и истории
  решения; код использовать только как свидетельство реализации.
- [ ] Записать applicability, конфликт/пробел, предлагаемое «подтвердить /
  уточнить / заменить / вывести из scope» и конкретный зависимый ticket.
- [ ] Проверить, что старые «С/Н/П» сохранены как история; составить только
  вопросы о невыводимом выборе, необходимом ближайшей зависимой карточке.

**Oracle/negative case:** прямое актуальное уточнение пользователя против
переноса старого S01 в обязательную нынешнюю цель. Отсутствие нового решения
не означает отмену всех прежних решений. **Acceptance:** каждая выбранная
строка имеет locator и обоснованный verdict либо локальный `needs_decision`.
**Выход:** `R/RV00.md`, M01/M12; RV03 получает конкретные owner constraints,
RV10 — выбранные научные ограничения. DONE относится только к объявленным,
проверенным claims пакета, даже если их принятие остаётся `needs_decision`.
Агрегированный RV00 сохраняет partial coverage, пока есть непроверенные
пакеты; другие карточки продолжаются.

## RV01 — паспорт наблюдавшегося исполнения

**READY:** metadata-only audit. Owners Results/Research/operator.
**Входы:** source audit, receipt
`canonical-update-ROOT-recovery-attempt4/ROOT-result.original.json`, SHA256
`4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3`;
run `dfb75b38-6019-4861-b868-f51648c71f02`, frozen-plan SHA256
`4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9`;
saved status SHA256
`d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90`.
Reader semantics — Results `src/qcl_negf_results/{multipart,native,model}.py` на `S`.

- [ ] Сопоставить доступные originals с hashes; если доступны только записи
  source audit, явно оставить первичную верификацию неизвестной.
- [ ] Разнести selected source, installed release `qcl-5d779b52-s01-20261012`,
  imported runtime, plan/model/schema, run, attempt и artifact profile по полям.
- [ ] Проверить `/native_owned_closure/runtime/ready`,
  `/native_owned_closure/gate/open`, `/native_owned_closure/delivery_report/status`,
  `/scientific_accepted`, `/full_release_CI_accepted`; составить inventory частей и gaps.
- [ ] Записать отдельный вектор execution/convergence/physics/discretization/
  experiment; назначить HDF5-подпакет только при доступных raw identity,
  schema/shapes/axes/weights и отдельном bounded объёме чтения.

**Oracle/negative case:** exact attempt + plan/hash; технический completed
при scientific=false, неполный multipart и старый RUNNING.
**Acceptance:** все поля имеют verified locator, secondary evidence или missing;
RUNNING от 2026-10-13 17:46 UTC не объявлен live now. **Выход:** `R/RV01.md`,
M06/M18/M19/M20; metadata-паспорт DONE не принимает физику. Missing matrices
создают `needs_data` только для raw-проверки RV08/сравнения RV10; новый submit
не восстанавливает provenance старой попытки.

## RV03 — actual views и обоснованные alternatives

**READY:** source-only views. Owner Root/all component owners.
**Входы:** `docs/architecture.md`, manifests каждого gitlink `S`;
Root `ops/{git,environment}.ts`; Core/Runner `src/QCLNEGF*.jl`;
AiiDA `src/aiida_qcl_negf/{service,workflow}.py`; Portal
`src/qcl_negf_api/api.py`; Platform `flake.nix`, `nix/application.nix`,
`ops/{application_release,worker_lifecycle}.py`. Target — docs-ref
`docs/system/architecture.md`, адресные RV00 rows.

- [ ] Отдельными пакетами восстановить dependency/import, context/container,
  job/data/release lifecycle и deployment/storage views.
- [ ] Для каждого edge записать source commit+path/symbol, направление,
  owner, interface и изменяемое состояние; проследить вызов или файл на обеих сторонах.
- [ ] Сопоставить actual с target; alternatives обозначить proposed, указать
  сохраняемый invariant, counterexample, цену и owner следующей проверки.

**Oracle/negative case:** две стороны контракта и executable/config evidence;
metadata DAG против dynamic/file cycle, repository против process boundary.
**Acceptance:** каждый показанный edge подтверждён либо marked unknown;
installed/deployment observation не приписана source baseline. **Выход:**
`R/RV03.md`, M06/M12; локальные views доступны RV04–RV07/RV13–RV19.
RV01 нужен лишь для installed/archive overlay, не для завершения остальных views.

## RV08 — операторные научные карточки

**READY:** статический аудит одного оператора, 2–3 properties на пакет.
Owners Core/Research. **Входы:** Core `docs/src/developer/traceability.md`,
соответствующая глава `docs/src/theory/`, `docs/src/physics/numerical-policy.md`,
`src/numerics/reference/acceptance_metadata.jl`, выбранный implementation
и literal/analytic fixture. Prefix путей таблицы — `components/QCLNEGF.jl/`.

| Пакет / properties | Точные implementation и начальный oracle |
| --- | --- |
| Dyson inversion/causality | `src/numerics/reference/greens.jl::retarded_green`; `test/physics/scalar_dyson_and_spectral_identity.jl` |
| Keldysh adjoint/scalar limit | `src/numerics/reference/greens.jl::keldysh_green`; `test/physics/scalar_dyson_and_spectral_identity.jl` |
| SCBA raw residual/final U–G | `src/numerics/reference/{scba,final_audit}.jl::{solve_scba,fresh_fixed_point_metrics}`; `test/numerics/fresh_candidate_residual.jl` |
| Poisson compatibility/gauge | `src/numerics/reference/poisson.jl::{build_poisson_matrix,solve_periodic_poisson}`; `test/physics/manufactured_periodic_poisson_solution.jl` |
| LO pair/balance | `src/numerics/reference/kernels.jl::lo_phonon_kernel`; `test/physics/production_lo_equilibrium_discretization.jl` |
| Current/basis reconstruction | `src/physics/observables.jl::{boundary_flux,energy_resolved_current,bond_current}`; `test/physics/cavity_current_and_spectral_oracles.jl`; EQ-CURRENT-001/002 |

Остальная очередь также конечна: отдельный пакет на каждый
`build_bdd_hamiltonian` (`hamiltonian.jl`), `build_localized_basis`,
`project_hamiltonians` (`basis.jl`), `build_shift_matrix`, `embedding_self_energy`
(`periodicity.jl`), `number_functional`, `normalize_lesser` (`greens.jl`),
`impurity_kernel`, `interface_roughness_kernel`, `acoustic_kernel`,
`alloy_kernel`, `_static_contraction`, `_lo_contraction`,
`direct_hilbert_transform`, `retarded_self_energy` (`kernels.jl`),
`electron_density`, `sheet_density_matrix`, `effective_levels`, `collision_balance`,
`power_balance` (`src/physics/observables.jl`), `validate_problem`,
`validate_solution` (`validation.jl`). Имена `.jl` без prefix относятся к
`src/numerics/reference/`. Каждый такой пакет проверяет формулу/размерность и
нормировку/квадратуру, третьим свойством — соответствующий ограниченный предел
из traceability. Production counterpart проверяется отдельным пакетом на те
же свойства по PROD-ID traceability, с literal oracle; не весь optimized путь сразу.

- [ ] Привязать 2–3 свойства назначенного оператора к traceability и ограничить
  applicability; записать exact source/fixture symbols на `S`.
- [ ] Построить formula→assumptions→discretization→symbol→observable→criterion;
  проверить units, norm, weights, tolerance basis и near-zero правило.
- [ ] Проследить independence oracle до helper graph; прочитать positive и
  negative assertion, не считать наличие fixture выполненным test.
- [ ] Зафиксировать отсутствующий критерий/предел и минимальный различающий
  analytic check или dataset slice. Прежняя S01 seed-карточка включается без дубля.

**Acceptance:** verdict для выбранных properties не сильнее evidence;
малый mixed step не заменяет raw residual, старое G не принимает новое U,
общий kernel не независимый oracle. **Выход:** `R/RV08.md`, M03/M19;
RV09 получает fixture/oracle gaps, RV10 — применимые критерии. Данные запуска
нужны только для измеренного verdict, не для source audit.

## RV10 — полный контракт следующего научного сравнения

**READY:** brief и варианты; выбор не выводимой физики — локальный `needs_decision`.
Owner Research с оператором и разработчиком. **Входы:** Research
`docs/{scientific-inputs,equilibrium-s01}.md`, `config/model/reference-2019-70k.yaml`,
`config/studies/{reference-48,grid-refinement-48,equilibrium-0-70}.yaml`,
`literature/reference-2019/{source.yaml,negf_iv_digitized.csv}`;
адресные RV00/RV01/RV08 outputs и шаблон framing brief.

- [ ] Сформулировать question/decision, observable/units, competing hypotheses,
  различающее предсказание и first gate; отделить transport от operator check.
- [ ] Заполнить модель, условия, границы, fixed/controlled differences,
  publication comparison и uncertainty только из выбранных источников.
- [ ] Развести calibration/validation и code/model/experiment evidence;
  проверить mismatch модели 70 K и digitized curve 200 K.
- [ ] Указать критерии с owner locators, authority, следующий минимальный
  comparison, attempts/CPU/RAM/wall/I/O/stop/resume envelope и неизвестные поля.

**Oracle/negative case:** независимые published conditions и RV08 derivation;
совпадение двух unconverged runs, toy equilibrium вместо прибора, допуск без основания.
**Acceptance:** полный brief описывает анализ/решение в названных пределах,
содержит 3–5 boundary cases, альтернативы и finite exit criteria. Неизвестные
model/tolerances не придуманы; пустой solver budget блокирует только запуск.
**Выход:** `R/RV10.md`, M01/M03/M18/M19/M20; brief DONE при явно локализованных
unknowns. Следующая comparison/gate-карточка READY лишь после собственных
данных, научного выбора и конечного budget; весь review продолжает работу.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Пакеты исполняются независимо | READY-входы и адресные outputs пяти RV | Это план, review ещё не выполнен | сохранить |
| Исторический S01 имеет собственную identity | Source audit, receipt/plan/status hashes | Live и научный verdict неизвестны | данных недостаточно |
| Научный пробел локализуется | RV01/RV08/RV10 dependency rules | Новый опыт требует отдельного бюджета | дополнительно измерить |
