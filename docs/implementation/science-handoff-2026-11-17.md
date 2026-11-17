# Свежая научная дельта для clean-start, 17 ноября 2026

Read-only проверка GitHub и checkout `c53f988464d026861262a5a8a9239b1cb8f26374`; status пуст, submodules не инициализированы. Solver, Julia/Pkg, science VM и Git mutations не использовались. Это source/handoff audit; live состояние VM и raw HDF5 независимо не проверялись.

## Refs и владение

- Core main: `db26a0ef49673d8246ae336cbe73bafe6d7482ac`; Runner main: `53b3a280109228a980df7ddea59e4f1b75b836be`.
- Инфраструктурные ветки остаются отдельными: Core `codex/project-simplification-2026-10-27` = `01d472141a91c9429f43f7237460a17592d65845`; Runner одноимённая = `97ab889ff83b73d9fad5d34e278309b2efe3b299`. Нельзя переносить ветку целиком по признаку «позже».
- [Root137](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/137) merged `cd1bad44d29b34cf515cae1575e4ed88b37d66af`; Research gitlink `76926d0035eeddf7c59a8c4357ab98f4e3bc9eba` (Research15). Изменены только Research pin и три campaign report/review файла.
- [Финальный handoff133](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/133#issuecomment-6912158562): кампания остановлена по прямому поручению, последний solve 16 ноября 08:11:40 UTC, агенты остановлены. Доступ/cleanup независимой science VM и её результатов инженерному этапу не передан. Активная научная правка по опубликованному handoff завершена; live владение конкретных файлов этим чтением не устанавливалось.
- Postboot runs исполняли Core `e171caa60cce676c6c4238dd671e7c527f2bd977`, Julia 1.13.4. Core db26 содержит поверх e171 только accepted exact-IFR change; его нельзя задним числом приписывать postboot данным.
- [Runner53b Project.toml](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/53b3a280109228a980df7ddea59e4f1b75b836be/Project.toml#L7) по-прежнему задаёт `[sources].QCLNEGF.rev=e171…`. Root integration gitlink db26, native Pkg selection и run source — разные свидетельства. Фактически импортированный Core будущей среды следует измерить до первого scientific check.

## Изменившиеся пути против карты 15 ноября

| Участок | Свежий источник / символ | Дельта и ограничение |
| --- | --- | --- |
| Native Julia | Core `src/QCLNEGF.jl`, Runner `src/QCLNEGFRunner.jl`, Project.toml | Exact Julia patch guard снят; Julia compat `~1.13.0`. Это не доказательство готовой среды clean-start. |
| Выбранный Hilbert cache | Core db26 `src/numerics/optimized/production_cache.jl::build_production_cache` | `hilbert=:product_integration` выбирает FFT plan на uniform grid, dense PI matrix на nonuniform; ordinary FFT plan создаётся только при `:fft`. Старый диагноз ненужного cache не переносить. |
| Uniform PI | Core db26 `fft_parallel.jl::_ProductionPIFFTHilbertPlan`, `_production_pi_fft_hilbert_transform`; `production_operators.jl::_retarded_self_energy_selected` | PI convolution исполняется через FFT при распознанной uniform geometry; tests `uniform_product_integration_fft.jl` отделены от native convergence. |
| Static retarded variant | Core db26 `domain/algorithm_options.jl::AlgorithmOptions.elastic_retarded`, `reference/scba.jl::solve_scba`, `production_operators.jl` | `:direct_green` даёт SigmaR=K[GR]; явно controlled numerical variant, не roundoff-equivalent optimization. Truncated low-rank combination запрещена. `algorithm_impact/algorithm_manifest` сохраняют identity. |
| Exact IFR | Core db26 `optimized/kernels.jl::_interface_roughness_kernel_data`, `production_cache.jl::_canonical_ifr_production_kernel`, `production_operators.jl::_production_static_contraction!` | Канонический IFR использует точные интерфейсные/радиальные factors только после точного совпадения source tensor, иначе dense fallback. Oracle/test `exact_ifr_structured_contraction.jl` сохраняет complex/Kraus/CP/gauge/custom-tensor cases. Runtime здесь не повторялся. |
| Restart compatibility | Core db26 `domain/algorithm_options.jl::_check_exact_restart_contract`; Runner53b `persistence/production_state.jl::_load_production_restart` | Отсутствующее историческое `elastic_retarded` значит Hilbert, unknown fields не отбрасываются. Runner делегирует algorithms check Core, solver comparison остаётся отдельно. Same package version guard пока существует; его не считать снятым вместе с Julia patch guard. |
| Core/Runner boundary | Core db26 `src/QCLNEGF.jl:974` `solve_production`; Runner53b `composition/production_solver_adapter.jl::solve_production`; `src/core_api.jl` | In-memory solver/callback и durable checkpoint adapter разделены, но Runner53b core_api ещё импортирует 278 underscore-prefixed bindings. Public snapshot/restore API поздней инфраструктурной ветки нельзя приписывать научному main. Cleanup boundary остаётся отдельной работой. |
| Diagnostics/checkpoint cost | [Core32](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/issues/32), `production_solver.jl`, `physics_markers.jl` | Residuals уже parallel; aligned checkpoint requests могут принудительно запускать markers. State-only checkpoint/lazy diagnostics/Green-AA — предложения; production refactor этим handoff не выполнен. |

## Научный итог и неизвестное

[Финальный отчёт](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/cd1bad44d29b34cf515cae1575e4ed88b37d66af/docs/campaigns/issue133-postboot-report.md): исходный native SCBA unresolved. Последняя separate fixed-U0/all5/no-e-e FDseed128 пара: 0 мВ rK=.00935430, rΣ=.0153461, |λ−1|=.000473434; 1 мВ rK=.00212979, rΣ=.00650829, |λ−1|=.000175533. Strict 1e−8 не пройдены, I–V не принята. Максимальный rΣ находится в embedding_plus.lesser; это локализация, не доказательство единственной причины. Малые Dyson/spectral residuals не закрывают nonlinear self-consistency. Matsubara/M3 finite-N остаётся отдельной equilibrium опорой. Green-variable AA — FUTURE/UNRUN.

Отчёт сообщает сохранённые семь state.h5 и семь model.h5, hashes/fsync и partial attempts в `.build/campaign133/`; повторного чтения/хеширования больших массивов здесь не было. Новый запуск, Poisson, finite-bias transport acceptance, grid/basis/window adequacy, эксперимент и end-to-end restart нового приложения этим аудитом не доказаны.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Кампания133 закончена | Final comment6912158562 + merged Root137 | Live process table не читалась | сохранить STOP и новые массивы |
| Gitlinks достаточно для выбора run source | Runner53b `[sources]` e171 против Core main db26 | Будущая среда не создана | изменить карту: явно различать checkout/Pkg/import/run |
| Старые cache/patch/restart диагнозы актуальны | Исправленные публичные paths и contract checks | Source-only | изменить соответствующие строки карты |
| Native science принята | Published raw residual summaries и independent review | Не все original arrays читались здесь | данных недостаточно для acceptance; сохранить unresolved |
| Можно переносить current main целиком как законченный новый app | Остались private Core imports и отдельная infra line | Новый producer-reader/runtime не проверен | дополнительно измерить выбранный целостный путь |
