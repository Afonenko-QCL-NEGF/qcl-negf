# RV16 · Три proposed дополнения выбранных материалов

Статус: draft текст для будущих owning docs edits; не применённый patch. Inputs/commits — RV16.md и source-receipt.json. Примеры illustrative/analytic; output solver не измерялся. Independent reader должен объяснить границу примера; такой reader acceptance пока не выполнен.

## Chapter · Core numerical-policy, после «Внутренний допуск и финальная проверка»

Prerequisites: Σ — текущее self-energy, F(Σ) — кандидат raw map при согласованных U/G; fixed-point условие F(Σ)=Σ. Здесь показывается только scalar linear mixing, а не весь SCBA/Poisson.

Малый смешанный шаг показывает действие mixing, но сам не проверяет уравнение. При Σ_next=Σ+α[F(Σ)−Σ], одной фиксированной норме и положительном масштабе S raw residual равен ||F(Σ)−Σ||/S, а step residual — ||Σ_next−Σ||/S=α·raw residual. Оба отношения безразмерны.

Пусть S=100 meV и норма candidate correction равна 10 meV. Читатель может предсказать: при α=0.01 шаг равен 0.1 meV, step residual 0.001, тогда как raw residual исходного состояния остаётся 0.1. Причина малого шага — берётся одна сотая поправки. Это ничего не говорит о новом raw residual после шага: его требуется вычислить в новом состоянии.

Изменим только α на 0.5, сохранив Σ и F(Σ). Шаг теперь 5 meV, step residual 0.05; исходный raw residual 0.1 тот же. Поэтому финальный verdict опирается на свежую raw map и согласованные U/G, а не размер поправки. Эта иллюстрация не назначает tolerance. Для Anderson/Pulay, state-dependent normalization и native metric definitions равенство автоматически не переносится.

Canonical links: Core `theory/12_validation.md` anchors `acceptance-metadata-registry` и `eq-validation-residuals`; там реестр applicability, norm/floor, weights и policy thresholds. Даже малая raw residual не доказывает достаточность сетки и экспериментальную валидацию. Locator результата указывается отдельно: exact artifact hash, receipt, HDF5 dataset и selection; если они отсутствуют, статус evidence missing.

## Reference · Runner api/public Types и Extension contracts, связать с configuration guide

`configuration_source(configuration::ResolvedRunConfiguration, dotted_path::AbstractString)` возвращает назначивший файл из последней записи leaf provenance либо `nothing`, если история отсутствует/пуста. Return не содержит физической величины или единицы; это provenance lookup. Для значения используйте typed configuration или `resolved_configuration_dict`, для units/constraints — canonical schema и typed conversion. Отсутствие source не означает, что schema назначила value.

Loader `validate_configuration_source` принимает canonical YAML/JSON files в объявленном порядке; later leaf overrides earlier leaf. Он читает файлы, deep-merges, validates schema и сохраняет provenance. Неверный формат, paired manifest/profile или невалидный merged mapping дают `ConfigurationError`. Формула физической величины, эффективное значение и файл, назначивший его, — разные facts.

Illustrative example: полный base configuration + override A задаёт `production.energy_chunk: 17`, override B задаёт `production.energy_chunk: 23`. При порядке base,A,B ожидается 23 и source B, поскольку B последним назначает leaf. Изменим только порядок на base,B,A: ожидается 17 и source A. `energy_chunk` — unitless chunk count; остальные base prerequisites нельзя опустить из executable configuration. Пример выводится из existing `test/application/configuration_merge_order_and_fail_closed_validation.jl`; тест данным review не выполнялся. Операция не решает transport.

Перед applying уточнить `nothing` wording против typed-default paths по RV19. Не документировать universal source-origin guarantee по одному leaf. Canonical example должен храниться единожды и включаться/линковаться из reference и guide; две независимо редактируемые копии не нужны.

## Goal runbook · Runner results, portable recovery

Цель — подготовить проверяемые prerequisites восстановления exact state, сохранив научную identity и использованный бюджет. Сам recovery запуск разрешается отдельным вычислительным поручением. Prerequisites: frozen plan; execution ID; source attempt; новый attempt больше source; совместимые model/grids/algorithms/runtime dependencies; весь hash-bound generation directory; prior completed-point archive closure для multipoint; принятый recovery и archive byte budget.

Сначала найдите `recovery/EXECUTION/POINT/current.json` и весь указанный generation. Проверьте его receipt и каждый declared artifact canonical verifier’ом в разрешённом read-only verification scope. Не копируйте только `physics.h5`: generation также содержит identity/config/history/commit/receipt. `pending-*` никогда не источник resume. При corrupt latest допустим только проверенный previous; при отсутствии обеих генераций остановка с error, без silent cold start.

Для multipoint проверьте `execution_progress.json` и все prior-final archives, указанные его closure. Неполный prefix не восстанавливает завершённые точки заново. Только после успешной closure проверки и разрешённого вычислительного этапа используйте документированный `run-plan ... --recovery-bundle DIRECTORY` с fresh attempt и `--archive-bundle DIRECTORY` при требуемых prior finals. Disk/archive budget refusal означает остановку; budgets не отменяют quotas/capacity planning.

Exit criteria: verifier подтвердил именно выбранную identity, whole closure и publication receipt; новый attempt сохраняет consumed logical iteration coordinates. Pause request alone не exit criterion: соответствующий `pause-receipt.json` обязан пройти `verify-pause`. Receipt scope `local_filesystem` не доказывает transfer/LAN fsync durability. Successful recovery/publication не утверждает convergence, discretization или experimental validation; проверяйте эти статусы отдельно.

Изменим одно условие: источник latest повреждён. Предсказуемый результат — проверка предыдущей declared generation; если она также повреждена, явный отказ. Причина — пригодность задают receipt+closure, а не имя папки. Граница переноса: backup/restore control-plane PostgreSQL+AiiDA является другим dataset и owning Platform runbook; этот путь его не заменяет.
