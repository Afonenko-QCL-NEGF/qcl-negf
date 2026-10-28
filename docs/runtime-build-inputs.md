# Runtime inputs и повторная сборка

Gitlinks Root определяют полный состав исходников. Для сборки runtime используются отдельные ресурсы
owning компонентов: это уменьшает пересборки после правок документации и сохраняет полный source
graph для происхождения выпуска.

## Julia solver

`nix/runtime-sources.nix` передаёт в существующий native пакет Runner:

- Core: `Project.toml`, весь `src`, `LICENSE`; при наличии `Manifest.toml`, `Artifacts.toml`, `ext`,
  `deps`.
- Runner: те же основные файлы, весь `schema`, `tools/verify_schema_provenance.jl`,
  `scripts/scientific_workflow.jl`, все `examples/config`; те же необязательные native ресурсы.
- Окружение Julia: исходные `Project.toml` и `Manifest.toml`.

Сохраняются схемы и их provenance, runtime source, install check с примером operator algebra,
зависимости Julia и прежний launcher. Изменение ресурса Core или Runner должно менять solver. Правка
только их документации не должна менять runtime derivation. Julia binary имеет собственные inputs;
его исходники и native проверки этой фильтрацией не меняются.

Python application, capture CLI, frontend receipt и исследовательский каталог описаны в
[руководстве Platform](../components/qcl-negf-platform/docs/runtime-build-inputs.md). Capture
остаётся зависимостью solver, поэтому изменение Results или Contracts может менять solver.

## Evaluation без установки

Существующий `tests/capture_runtime_eval.nix` возвращает application, capture и solver `.drv`. Вызов
требует выбранный source flake и существующий подготовленный depot:

```bash
nix --extra-experimental-features 'nix-command flakes' eval --impure --offline --json \
  --expr 'import ./tests/capture_runtime_eval.nix {
    root = ./.;
    preparedDepot = /nix/store/REPLACE-WITH-PREPARED-DEPOT;
  }'
```

Замените depot на действительный input установки. Не передавайте пустой depot в настоящую сборку: в
evaluation он допустим только как явный placeholder для изучения графа зависимостей. Сравнивайте
деривации в отдельных source-копиях с одной поправкой; не меняйте рабочие данные ради проверки.

Проверка `.drv` не является запуском solver, native install или scientific acceptance. Проверки
Manifest, версии Julia и соответствия подготовленного depot исходникам сохраняются. Политика
совместимости depot — отдельный этап P15; этот source filter сам по себе её не расширяет.
