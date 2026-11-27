# QCL NEGF

Приложение для расчёта квантового транспорта в квантово-каскадных лазерах.
[QCLNEGF.jl](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl) содержит физическую
модель, численные операторы и решатель в памяти. Это приложение содержит
[Runner](runner/), [независимый анализ](analysis/), [исследования](studies/)
и [инструкции лаборатории HTCondor](lab/).
[Исследовательский архив](docs/research-archive/index.md) связывает опыты
с источниками, критериями и численными свидетельствами.

## Проверочный расчёт

Из корня приложения с Julia 1.13:

```sh
julia --startup-file=no --project=runner -e 'using Pkg; Pkg.instantiate()'
runner/bin/qcl-negf plan runner/examples/config/stationary-smoke.yaml --max-runs 1 > plan.json
runner/bin/qcl-negf run-plan plan.json stationary-result
runner/bin/qcl-negf analyze stationary-result stationary-report
```

Пример ограничен двумя итерациями SCBA. Результат показывает прохождение
инженерного тракта и содержит оценку сходимости. Установка независимого
читателя описана в [analysis](analysis/README.md), а запуск того же плана
через очередь в [lab](lab/README.md).

[Проверочная кампания](studies/experiment-contract-smoke.yaml) объединяет
этот расчёт с независимой спектральной проверкой V843 B7. Для кампании
передайте её YAML команде `plan` с `--max-runs 2`.

[Документация программы](docs/index.md) · [Участие в разработке](CONTRIBUTING.md) · [Лицензия MIT](LICENSE)
