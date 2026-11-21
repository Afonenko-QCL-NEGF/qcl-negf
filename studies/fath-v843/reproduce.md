# Воспроизведение Fath–V843

Расчёты используют Julia 1.13.4 и Core
`c2f45cae21c3e2e4257805ea9c30f9c1d80a7515`, закреплённый в проекте
`runner/`. Сначала выполните `julia --project=runner -e 'using Pkg; Pkg.instantiate()'`
из корня приложения. Процессы использовали один поток BLAS и по одному
потоку управления сборкой мусора, кроме исходного пространственного
F13 с двумя потоками сборки мусора. Число рабочих потоков указано в последнем
аргументе каждой команды. Выходной JSON следует выбрать в доступном каталоге.
Источники и рабочие поля во всех опытах находятся в RAM.

## Входы и контрольные суммы

Имена ниже относятся к сохранённому архиву рабочей станции. При
переносе архива пути можно заменить. Отчёт проверяет хеши `spec.toml`,
запечатанного seed, геометрии и использованных полей. Для входа из другого
checkout сверяются эти хеши. Сами полные состояния остаются в архиве.

| Имя в командах | Относительный путь от исходной рабочей папки |
| --- | --- |
| `F13` | `.build/fath-dupont-next/work/method/checkpoints/linked-E481x13-step9-alpha050` |
| `F25` | `.build/fath-dupont-next/work/method/checkpoints/linked-E959x25-x9-fixed-H-alpha020` |
| `F13_REFERENCE` | `.build/fath-dupont-next/work/method/runs/linked-E481x13-step9-alpha050` |
| `FATH_BDD` | `.build/fath54-20261120/work/05-iterator/runs/causal-native-512/model.h5` |
| `V843_21` | `.build/fath-dupont-next/work/dupont/linked-input-q28-f21-e239-cont` |
| `V843_125` | `.build/fath-dupont-next/work/dupont/linked-input-q28-f125-e239-cont` |
| `V843_GEOMETRY` | `.build/fath-dupont-next/work/dupont/tail-geometry-q28.h5` |

Исходный F13 BDD имеет SHA-256
`9ad6f3815dfeda5e199a5201132dab00a4b9eef2858a7ea7bdd11416610399ba`.
У файла свежего источника `fresh_source_LG_packed.bin` из F13_REFERENCE
SHA-256 `c2c39821e5cf3f6ade42c773c074bb71b43b3622bf1f6b96c2b03bfe28ca891e`.
Его используют две проверки замороженного источника.
[Вход V843 и контрольные суммы](controls/v843-input/README.md)

## Прогоны Fath

Выберите исходники опыта по приведённым ревизиям. Каждая команда
запускается из корня соответствующей копии приложения.
Переменные F13, F25, FATH_BDD, F13_REFERENCE означают абсолютные пути
к входам таблицы, OUT — существующий каталог для повторных отчётов.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
study=studies/fath-v843
fresh=c2c39821e5cf3f6ade42c773c074bb71b43b3622bf1f6b96c2b03bfe28ca891e

# 84ed22a
julia --threads=8,0 --gcthreads=2,0 --project=runner "$study/profile_experiment.jl" \
  "$F13" "$OUT/fath-F13-profile.json" 8 compare-unitary
# b174bab
julia --threads=6,0 --gcthreads=1,0 --project=runner "$study/impurity_experiment.jl" \
  "$F13" "$OUT/fath-F13-impurity.json" 6 25:26 26:27 58:62
# e32812f
julia --threads=2,0 --gcthreads=1,0 --project=runner "$study/impurity_experiment.jl" \
  "$F13" "$OUT/fath-F13-ifr.json" 2 IFR 25:26 26:27
# ed67776
julia --threads=2,0 --gcthreads=1,0 --project=runner "$study/nearby_resonance.jl" \
  "$F13" "$FATH_BDD" "$OUT/fath-nearby-resonance.json" 54.71186 2
```

Две независимые проверки без обращения к полным архивным состояниям
используют малые сконструированные задачи с известным знаком тока,
согласованными уравнениями и парой упругих ядер.

```sh
julia --project=runner "$study/test_spatial_balance.jl"
julia --project=runner "$study/test_elastic_common_measure.jl"
```

Аудит парной радиальной меры использует только ядра и веса из
соответствующего запечатанного входа. Для расчёта требуется NumPy.

```sh
python3 "$study/audit_radial_reciprocity.py" "$F13" "$OUT/fath-F13-reciprocity.json"
python3 "$study/audit_radial_reciprocity.py" "$F25" "$OUT/fath-F25-reciprocity.json"
```

Варианты буферного пространственного баланса сохраняют исходники
точной ревизии для каждого отчёта.

```sh
# a94526e
julia --threads=2,0 --gcthreads=1,0 --project=runner "$study/continuation.jl" \
  "$F13" "$OUT/fath-F13-positive.json" 6 0.20 projected 2
# fe8c37e
julia --threads=6,0 --gcthreads=1,0 --project=runner "$study/tail_experiment.jl" \
  "$F13" "$FATH_BDD" "$F13_REFERENCE" "$fresh" "$OUT/fath-F13-tails.json" 6
```

```sh
# e32812f
julia --threads=6,0 --gcthreads=1,0 --project=runner "$study/direct_continuum.jl" \
  "$F13" "$F13_REFERENCE" "$fresh" "$OUT/fath-F13-continuum.json" 6 1 6
```

```sh
# fe8c37e
julia --threads=5,0 --gcthreads=1,0 --project=runner "$study/profile_experiment.jl" \
  "$F25" "$OUT/fath-F25-profile.json" 5
```
