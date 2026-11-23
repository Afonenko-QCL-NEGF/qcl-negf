# Воспроизведение

Расчёт использует исходники приложения
`08e90bc605f0662f1b5559f4c0f0c5a5655ed691`, Julia 1.13.4 и Core
`c2f45cae21c3e2e4257805ea9c30f9c1d80a7515`, закреплённый в `runner/`.
Ночной наблюдатель и данные сверки берутся из
`1815bf37cb978777f1cf8df69cba9b6af52e2e2a`.
До запуска подготовьте Julia-окружение Runner через `Pkg.instantiate()`
и Python с NumPy. Для графика требуется Matplotlib.

| Переменная | Вход |
| --- | --- |
| `FATH_APP` | Абсолютный путь к научной ревизии приложения |
| `STUDY` | Абсолютный путь к каталогу данного исследования |
| `NIGHT` | Абсолютный путь к `studies/fath54-stability-night` из ночной ревизии |
| `F13` | `work/method/checkpoints/linked-E481x13-step9-alpha050` из архива `fath-dupont-next` |
| `F25_RADIAL` | `work/baseline/radial-regrid/input-E481x25-x9` из того же архива |
| `FATH_ARCHIVED_REGRID` | `work/baseline/radial-regrid/regrid.py` из того же архива, в исходной структуре архива |
| `FATH_BDD` | Замороженный `model.h5` из паспорта Fath |
| `FATH_SECOND_HISTORY` | `work/method/checkpoints/linked-E481x13-norm-alpha020-step0002` из архива `fath-dupont-next` |
| `FATH_KERNEL_PYTHON` | Python с NumPy и доступом к тому же загрузчику архивного HDF5 |
| `OUT` | Каталог компактного вывода |

Архивы и смежные каталоги конструктора следуют путям, указанным в
[ночном воспроизведении](../fath54-stability-night/reproduce.md) и
[паспорте Fath–V843](../fath-v843/reproduce.md).
SHA-256 `spec.toml` равны
`25d608a98548c489f6537a3f9fd3918220d137f036c65680d181d4d80a9898e5`
для F13 и
`3f954e90fc47eeb141a1a726ad16358c77b5db845946b5b19355892ffa9548f3`
для K25. Сырые поля живут в RAM. Конструктор отдаёт статические
матрицы рабочему процессу через стандартный канал ввода, и промежуточные
бинарные файлы в новом опыте отсутствуют.

```bash
export FATH_APP FATH_ARCHIVED_REGRID FATH_BDD FATH_SECOND_HISTORY FATH_KERNEL_PYTHON
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 JULIA_PKG_PRECOMPILE_AUTO=0
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$OUT"
for level in K25 K27 K31 K31_shift; do
  "$FATH_KERNEL_PYTHON" "$STUDY/physical_kernels.py" "$F25_RADIAL" \
      "$FATH_ARCHIVED_REGRID" "$level" --check-only > "$OUT/preflight-$level.json"
done
cd "$FATH_APP"
/usr/bin/time -v -o "$OUT/refinement.resources" julia --compiled-modules=existing \
  --startup-file=no --project=runner --threads=8,0 --gcthreads=1,0 --heap-size-hint=10G \
  "$STUDY/replay.jl" "$NIGHT/transfer/radial_node_replay.jl" "$F13" "$F25_RADIAL" \
  "$NIGHT/evidence/measurements.json" "$OUT/refinement.json" "$STUDY/refinement.jl" \
  > "$OUT/refinement.log" 2>&1
python3 "$STUDY/collect.py" "$OUT/refinement.json" "$OUT/evidence"
python3 "$STUDY/plot.py" "$OUT/evidence"
```

Первая карта проверяет равенство укороченного обновления источника
и полной карты. После 47 обновлений со смешиванием 0,35 измеряется
полная 48-я карта и сверяются SHA-256 исходного состояния и свежего
образа. Те же физические сечения используются во всех руках.
`collect.py` повторно рассчитывает скалярные метрики профилей и
проверяет суммы радиальных вкладов из компактного вывода.

## Восстановление после прерывания

Штатная команда выше повторяет кампанию с начала. Если полный K27
успел записать компактное свидетельство, сохраните JSON со
`stage="K27"` в отдельный файл. После перезапуска укажите его
абсолютный путь в `FATH_RESUME_EVIDENCE` и передайте
`"$STUDY/resume.jl"` последним аргументом команды Julia. Выберите
новый путь для выходного JSON. В последнем запуске использовалось
`--threads=10,0`. Драйвер сверяет отпечаток F13,
перенос и свежий образ K25. Он также проверяет совпадение заряда,
профиля и долей мод K25 при измерении с опущенными интегралами
столкновений в наблюдателе. Дальнейшие карты использовали тот же
полный оператор столкновений. Для K31 и контролей GL20 заново
восстанавливает все физические сечения, заряд и моды.
