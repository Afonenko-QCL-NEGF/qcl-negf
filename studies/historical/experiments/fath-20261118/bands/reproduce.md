# Воспроизведение одночастичных тестов

Исходная папка команд — `bands/`. Нужны Julia 1.13.4 с уже установленными зависимостями e171, Python ≥3.11 и NumPy. `JULIA_PROJECT` должен указывать на проект с Unitful и Core из `passport.toml`. `CPU_LIST` — одна или две разрешённые CPU. Команды заменяют выходные файлы в текущей папке, поэтому удобна копия экспериментального каталога.

```bash
set -eu
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0 PYTHONDONTWRITEBYTECODE=1
: "${JULIA_PROJECT:?Set JULIA_PROJECT to an existing environment with pinned QCLNEGF, Unitful and TOML}"
CPU_LIST="${CPU_LIST:-$(python -c 'import os; print(min(os.sched_getaffinity(0)))')}"

limited() {
    taskset -c "$CPU_LIST" timeout --signal=KILL 180s \
        prlimit --as=2147483648:2147483648 --fsize=8388608:8388608 -- "$@"
}

native() {
    limited julia --startup-file=no --threads=1,0 --gcthreads=1 \
        --heap-size-hint=512M --compiled-modules=existing "$@"
}

native native.jl
limited python compare.py
native scan_native.jl scan
limited python scan_compare.py scan
native scan_native.jl refine 12:3 12:4 12:5 5:4 5:5 7:3 14:2
limited python scan_compare.py refine
```

`native.toml`, `native_scan.toml` и `native_refine.toml` содержат исходные матрицы e171 и измеренное время работы. Эти TOML с сырыми матрицами не включены в публикацию: их создают приведённые команды перед постобработкой. Файлы JSON и CSV содержат сравнения и диагностические критерии. Временные поля могут отличаться при повторе. Контрольные суммы публичного пакета перечислены в SHA256SUMS. Для QCLNEGF нужен чистый checkout [e171caa60cce676c6c4238dd671e7c527f2bd977](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/tree/e171caa60cce676c6c4238dd671e7c527f2bd977); локальная среда исполнения не входит в пакет.
