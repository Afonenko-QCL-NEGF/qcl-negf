# Воспроизведение Fath при 54 мВ

Исследование использует исходники приложения
`08e90bc605f0662f1b5559f4c0f0c5a5655ed691` и Core
`c2f45cae21c3e2e4257805ea9c30f9c1d80a7515`. На первом из этих
коммитов нужны окружение `runner/` и Julia 1.13.4. Переменная `APP`
указывает на этот checkout, `STUDY` на директорию данного отчёта, `OUT`
на новый каталог для компактного вывода. Абсолютные пути `F13` и
`FATH_BDD` берутся из [таблицы исходных архивов](../fath-v843/reproduce.md).
Для `F25_RADIAL` нужен пакет парных ядер
`work/baseline/radial-regrid/input-E481x25-x9` из того же архива
`fath-dupont-next`. Он содержит 481 энергию, а независимая архивная
история F25 содержит 959 энергий. Использованные отпечатки входов и
фактически загруженных исходников записаны в [измерениях](evidence/measurements.json).

Команды основной и ранговой рук. Пакеты Julia установлены штатным
`Pkg.instantiate()` в окружении Runner. Вторичное звено `JULIA_DEPOT_PATH`
может указывать на доступный каталог уже установленных пакетов.
Число потоков двух одновременных процессов с GC и BLAS составляет 13.
Поля в RAM, программа записывает только журналы и компактные наблюдения.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 JULIA_PKG_PRECOMPILE_AUTO=0
export FATH_APP="$APP"
export FATH_BALANCE_SCRIPT="$STUDY/balance/observe_balance.jl"
touch "$OUT/primary7.jsonl.radial.json.decompose"
printf '16\n' > "$OUT/primary7.jsonl.fine.jsonl.target"
FATH_BALANCE_STEPS=48,64,80,96,112,128 \
FATH_RADIAL_STEP=48 FATH_RADIAL_SCRIPT="$STUDY/transfer/radial_control.jl" \
FATH_FINE_ARCHIVE="$F25_RADIAL" FATH_FINE_MAPS=8 \
julia --compiled-modules=existing --startup-file=no --project="$APP/runner" \
  --threads=5,0 --gcthreads=1,0 --heap-size-hint=6G \
  "$STUDY/drivers/night.jl" "$APP" "$F13" "$FATH_BDD" base 5 192 "$OUT/primary7.jsonl"

# Вторая команда выполняется параллельно с первой.
FATH_BALANCE_STEPS=48,64,80,96 \
julia --compiled-modules=existing --startup-file=no --project="$APP/runner" \
  --threads=4,0 --gcthreads=1,0 --heap-size-hint=6G \
  "$STUDY/drivers/night.jl" "$APP" "$F13" "$FATH_BDD" expanded 4 96 "$OUT/expanded8.jsonl"
```

Создание `$OUT/primary7.jsonl.radial.json.decompose` до карты 48
разрешает условную локализацию радиального эффекта. Разложение
выполняется при превышении допуска на общем наблюдателе K25.
Для альтернативы смешивания `drivers/decide.py` сравнивает
первые карты с архивными историями и создаёт
`$OUT/primary7.jsonl.compare` после выполнения условия замедления.
Запускайте эту проверку по мере записи свежих карт. Наличие файла `.stop`
рядом с JSONL запрашивает завершение после ближайшей карты и
независимое наблюдение. В ночном опыте тонкая рука прошла 16 карт,
а лимит зафиксирован в `.fine.jsonl.target` перед регистрацией её
результатов. Для высвобождения вычислительных ресурсов на
локализацию узлов по достижении 80-й карты запросили завершение
восьмимодовой руки. Основная рука завершена с независимым
наблюдением карты 96. После освобождения ресурсов 8-модовой руки выполняется
побитовый повтор состояния карты 48 и две свежие карты K24.

```bash
julia --compiled-modules=existing --startup-file=no --project="$APP/runner" \
  --threads=4,0 --gcthreads=1,0 --heap-size-hint=6G \
  "$STUDY/transfer/radial_node_replay.jl" "$F13" "$F25_RADIAL" \
  "$OUT/primary7.jsonl.radial.json" "$OUT/node-replay.json" 4
```

```bash
julia --compiled-modules=existing --project="$APP/runner" --threads=1,0 \
  "$STUDY/balance/check_balance.jl" "$APP/studies/fath-v843"
python3 "$STUDY/balance/archive.py" "$APP/studies" "$OUT/evidence"
python3 "$STUDY/drivers/collect.py" "$OUT" "$OUT/evidence"
python3 "$STUDY/drivers/plot.py" "$OUT/evidence"
```

[Условия сравнения ранга](conditions.md) ·
[Протокол вложенной радиальной сетки](transfer/protocol.md) ·
[Опубликованные строгие критерии](../fath-v843/method-freeze.toml)
