# Julia targeted harness v3 — narrow technical source review

Вердикт: **READY для отдельно авторизованного selected-fixture packet**, с указанными sampled resource limitations. Harness не исполнялся; никакой новый test result этим review не установлен.

## Binding и метод

Самостоятельно пересчитанный SHA-256 `/tmp/qcl-julia-targeted-run-v3.py`:
`da42ab9bf913dd28715824fe4c0b5efbba004d1d5f23be0a32efdadcf6096911` (7629 bytes).
Сравнение с уже reviewed Python v4 `60f1e75cad84047e6a9322dab4d2531ca50713bac4893956bd6d9c68a654c38d`; SHA-bound helper остаётся `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`. Все три файла AST-parse успешно стандартной библиотекой; ни один не executed/imported. Блок от rss_tree до receipt byte-equal Python v4 после замены только двух заявленных wall/RSS thresholds. Полный diff прочитан.

## Проверенные условия

- :3–19 сохраняет exact worktree, confined existing fixture realpaths внутри components, ASCII task/attempt basenames и exclusive attempt folder/log. Julia fixture — plain path, без pytest `::` selectors. Scope caller обязан выбрать уже reviewed finite fixture; harness не определяет научную допустимость содержимого.
- :20–31 использует selected Julia runtime, отдельный copied project и prepared depot; flags startup=no, threads=1, bounds=yes; generic CPU, offline Pkg/server empty, auto-precompile=0/task1, BLAS/MKL/OMP1. Affinity 1 CPU, RLIMIT_CPU soft120/hard125; monitor wall120s/RSS2GiB. Нет нового setup/install/solver command. Offline variables сами по себе не являются network sandbox.
- :56–58 exclusive raw log открывается до child, RawCapture запускается сразу после Popen. :79–118 сохраняет terminate/drain на normal/stop/exception, capture-construction fallback communicate, memoryview write-all с отказом при отсутствии progress, stream close и original guard diagnostics. Error не выдаётся за successful empty output.
- :65,114–123 сохраняет nominal2MiB envelope и early threshold; после drain exact captured byte count overrun превращается в failure, bytes не обрезаются. Receipt содержит raw completeness/error, stop reason, guard error, exit code, fixture/harness hashes. Unknown exit и collector failure не проходят success predicate.
- TMPDIR указывает на новый owned attempt/tmp; 16MiB и process-tree RSS sampled каждые50ms. Нет hard cgroup/RAM/disk quota или доказательства transient peak; явные записи вне TMPDIR, в том числе project/depot paths, остаются вне измеренного owned temporary объёма. Это прямо записано в receipt caveat; не объявлять zero temp глобальной нулевой записью.

Hashes записываются при создании receipt, не доказывают before/after source freeze сами по себе. Runtime/project/depot identity и допустимость fixture должны связываться root packet receipt с ранее принятым source; harness не заменяет admission. Старые v1/v2 и их actual evidence не исправлялись и не наследуют новый failure-path review.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Raw failure branches R1/R2 и safe IDs перенесены без регрессии | Exact capture/finally comparison и :5–19,79–123 | Только source/AST, fault paths не запускались | сохранить |
| Julia adaptation соответствует finite selected-fixture route | :20–31,62–63,119 | Sampled RAM/TMP, no hard wall guarantee during drain, no network sandbox | сохранить |
| Новая fixture прошла тест | Runtime evidence отсутствует | READY не является PASS fixture/full CI/science | данных недостаточно |

Новых blocking findings в этой адаптации нет. Reviewer не изменял harness/owning source, не выполнял Julia/Python project imports/tests/build/Git/server; записан только этот /tmp report.
