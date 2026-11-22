# Воспроизведение

Исходный научный вход закреплён в приложении
`497ac103d8b28d642e1062e4529278589f87d8ac` и Core
`c2f45cae21c3e2e4257805ea9c30f9c1d80a7515`. Команды запускаются из
корня приложения с опубликованными драйверами исследования. Нужны
Julia 1.13.4, Python 3 и предварительно установленное окружение
`runner/`. Полные поля в оперативной памяти.

```sh
julia --project=runner -e 'using Pkg; Pkg.instantiate()'
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
study=studies/fath-lo-rank-v843
```

Переменные F13, F25, FATH_BDD, V843_21 и V843_GEOMETRY означают
абсолютные архивные пути из исходного исследования. OUT — существующий
каталог для компактных выходов. Идентификаторы входных полей, исходной
геометрии и реально загруженного кода входят в отчёты.
[Архив и условия исходного исследования](../fath-v843/reproduce.md)

## A. Факторный опыт Fath

```sh
for rank in base expanded; do
  for lo in cell hat; do
    julia --startup-file=no --project=runner --threads=5,0 --gcthreads=1,0 \
      --heap-size-hint=6G "$study/fath_factorial.jl" "$F13" "$FATH_BDD" \
      "$rank" "$lo" 1 5 map "$OUT/fath-A-$rank-$lo.json"
  done
done
python3 "$study/compare.py" fath "$OUT" "$OUT/fath-contrast.json"
```

## B. LO-оператор

```sh
julia --startup-file=no --project=runner --threads=1,0 --gcthreads=1,0 \
  "$study/lo_control.jl" "$OUT/lo-fixture-audit.json"
for rank in base expanded; do
  julia --startup-file=no --project=runner --threads=5,0 --gcthreads=1,0 \
    --heap-size-hint=6G "$study/fath_factorial.jl" "$F13" "$FATH_BDD" \
    "$rank" cell 1 5 operator "$OUT/fath-$rank-cell-B.json"
done
```

В отчёте B обе меры используют одно G внутри каждого прогона.
Скорости в таблице событий приведены в единицах упакованной меры
$w_E w_k$ без общего множителя $g_s/(2\pi)$. Отношения энергий даны в мэВ.

## C. V843, 21 кВ/см

```sh
julia --startup-file=no --project=runner --threads=5,0 --gcthreads=1,0 \
  --heap-size-hint=6G "$study/v843_selected.jl" "$V843_21" "$V843_GEOMETRY" 47 5 "$OUT"
python3 "$study/compare.py" v843 "$OUT" "$OUT/v843-radial-contrast.json"
```

Проверка сравнивает k5 и k9 с опубликованными наблюдаемыми
48-й карты. Можно также ввести число обновлений 0 и отдельный
выходной каталог для проверки радиальных условий на входе первого
свежего отображения. Причинное разложение и профиль сохраняются в
отчёте по каждому числу колец.

## Дополнительный тепловой и причинный контроль Fath

```sh
julia --startup-file=no --project=runner --threads=1,0 --gcthreads=1,0 \
  "$study/lo_thermal_grid.jl" "$OUT/lo-thermal-grid.json"
julia --startup-file=no --project=runner --threads=6,0 --gcthreads=1,0 \
  --heap-size-hint=6G "$study/lo_causality.jl" "$F13" 6 "$OUT/fath-causality.json"
julia --startup-file=no --project=runner --threads=6,0 --gcthreads=1,0 \
  --heap-size-hint=6G "$study/lo_thermal_balance.jl" "$F13" 6 "$OUT/lo-thermal-balance.json"
```

В причинном контроле носитель $\Gamma=i(\Sigma^>-\Sigma^<)$ имеет те же
нулевые крайние узлы, что в связанных уравнениях. Главная часть
от $\Gamma$ проверяется отдельным интегрированием с вычитанием
полюса. Тепловой контроль применяет изменённые коэффициенты
только через поддерживаемый вход LO-оператора.

## D. Продолжение Fath

Исходный шестипоточный прогон из того же F13 и с той же долей
свежего источника 0,35 воспроизводится командой для 48 карт из
[предыдущего исследования](../fath-v843/reproduce.md#прогоны-fath).
Для расширенного базиса подставляется та же нулевая фиксированная
потенциальная часть Хартри и прежняя мера LO.

```sh
julia --startup-file=no --project=runner --threads=6,0 --gcthreads=1,0 \
  --heap-size-hint=6G "$study/fath_factorial.jl" "$F13" "$FATH_BDD" \
  expanded cell 48 6 map "$OUT/fath-D-expanded-cell.json"
```

Второй начальный источник F13 и удержанный F25 запускаются
отдельно. Для F13_SECOND используется каталог
`linked-E481x13-norm-alpha020-step0002` в том же архиве
`work/method/checkpoints/`. Физические входы прежней задачи
совпадают, начальный архивный источник отличается.

```sh
julia --startup-file=no --project=runner --threads=6,0 --gcthreads=1,0 \
  --heap-size-hint=6G "$study/fath_factorial.jl" "$F13_SECOND" "$FATH_BDD" \
  base cell 48 6 map "$OUT/fath-D-second-seed.json"
julia --startup-file=no --project=runner --threads=5,0 --gcthreads=1,0 \
  --heap-size-hint=10G "$study/fath_rank_holdout.jl" "$F25" "$FATH_BDD" \
  5 "$OUT/fath-D-F25-expanded-cell.json"
```

Базовый профиль F25 для парного сравнения берётся из
[опубликованной карты F25](../fath-v843/evidence/fath-F25-projected.json)
после проверки идентичности входа. Для построения сводного рисунка
из компактных отчётов нужен Matplotlib.

```sh
python3 "$study/plot_profiles.py" "$OUT" "$OUT/current-profiles.png"
```

## Учёт ресурсов

Запуски проведены локальным CLI Julia через окружение Runner.
Всего использовалось до 13 потоков Julia и сборки мусора в
одновременных расчётах. BLAS работал в одном потоке каждого
процесса. Проверка штатного пути на Fath и V843 перед длинными
продолжениями записывала только компактные отчёты и журналы.
Пик RSS, CPU-время и счётчики записи приведены в квитанциях.
Для нескольких ранних проб использованы 512-байтовые блоки
записи GNU time. Основные запуски измерены по `/proc/PID/io`
и `wait4` лёгкой обёрткой `run_measured.py`.
Ведущий Sol выполнял научный разбор, Terra сверила технический
путь воспроизведения V843. Расчётами и фиксацией метрик
управлял Runner через прямой CLI.
[Квитанции ресурсов](evidence/run-receipts.tsv)
