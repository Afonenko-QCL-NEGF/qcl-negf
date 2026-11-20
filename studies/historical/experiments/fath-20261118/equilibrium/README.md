# Доступность равновесных проверок

В этом разделе результаты относятся к 0 мВ, 10 K, фиксированному U=0, CBO149 мэВ, пяти каналам рассеяния и выключенному столкновительному e–e. Холодная SCBA и проверка после FDT-старта остаются непринятыми. KMS и уточнение спектрального интеграла — отдельные frozen проверки, а не новые самосогласованные состояния.

Публикуются условия и исходники, малые скалярные результаты и hashes. Большие `model.h5`/`state.h5` и полный per-map архив не входят в Git. Публичные агрегаты позволяют проверить числа и логику вывода, но не восстановить матрицы. Для точного повторения постобработки нужен внешний архив с указанными hashes. Это явная граница доступности.

Генерирующие исходники включены: `run.jl` создаёт холодный нулевой контроль, `attempt01/transport-run.jl` содержит построение физической модели и служебные функции, `kms.jl` определяет общую модель для KMS и FDT-старта, `projected-control/run.jl` выполняет проецированный этап и неналоженные SCBA-проверки. Они зависят от [Core e171](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/tree/e171caa60cce676c6c4238dd671e7c527f2bd977), Julia 1.13.4, Unitful и HDF5. Архивный cold driver проверяет также точный Manifest SHA, но сам runtime Manifest здесь не распространяется. Пакет поэтому не объявлен автономным повтором исходного окружения.

Команды ниже документируют отдельное будущее исполнение. Они не выполнялись при упаковке. Используйте отдельную копию экспериментального каталога, новые выходные папки и совместимое подготовленное окружение. Скрипты могут записывать результаты рядом с собой.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p /path/to/new-zero-output
julia --startup-file=no --threads=1 --project=/path/to/pinned-environment equilibrium/run.jl /path/to/new-zero-output equilibrium/attempt01/device.toml
mkdir -p /path/to/new-projected-output
julia --startup-file=no --threads=1 --project=/path/to/pinned-environment equilibrium/projected-control/run.jl /path/to/new-projected-output
```

Для постобработки восстановите отдельно архивные HDF5 по зафиксированным hashes в `equilibrium/attempt01/linear` и `equilibrium/projected-control/attempt01`. FDT-скрипт дополнительно читает полный исходный biased ledger `method/alpha-extended/attempt01/linear`; опубликованного агрегата вместо него недостаточно. `spectral_refinement.py` для описания тренда использует полную `projected.csv`. В Git сохранены выбранные строки, а полную историю создаёт генерирующий driver или предоставляет архив. Поэтому повтор именно всех чисел этих скриптов требует дополнительных исходных данных, а не одного Git clone.

```sh
python equilibrium/fdt.py
julia --startup-file=no --threads=1 --project=/path/to/pinned-environment equilibrium/kms.jl
python equilibrium/projected-control/independent.py
python equilibrium/projected-control/spectral_refinement.py
python equilibrium/projected-control/adaptive_poles.py
```
