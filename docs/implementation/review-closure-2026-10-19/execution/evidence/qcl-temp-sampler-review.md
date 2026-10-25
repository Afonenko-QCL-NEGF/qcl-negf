# H1 tooling sampler: независимый source review

Вердикт: **исправить одно узкое несоответствие strict ENOENT-only contract перед selftest/replacement packet**. Само устранение ordinary unlink/rename double-stat race реализовано; raw capture, limits, identity и final success predicates сохранены. Ни sampler/selftest, ни harnesses, ни project tests рецензент не исполнял; Git не вызывал и код не менял. Создан только этот review artifact. Авторский repair report прочитан после helper/selftest/actual old-new diffs и original failure receipt.

## Проверенная идентичность

| Файл | SHA256 |
| --- | --- |
| `/tmp/qcl-python-targeted-run-v5.py` | `4401dcb5ac03d253166fb0dececa525bfeb15200763f62aa4e579b2a67941e10` |
| `/tmp/qcl-julia-targeted-run-v4.py` | `0ecd8c9357840f61646668467e6eaa055039469f81ea706958bd7f400239586b` |
| `/tmp/qcl-owned-temp-sampler-v1.py` | `3d1dd39cfac5d0ee816e9d79d54c9cd77f6df560efa34407b40ce254b970c9c9` |
| `/tmp/qcl-temp-sampler-selftest.py` | `b07e1dd56359472c4ab4d051cc2d4b1b236732c50ffdd3299e702d7df41b713d` |
| Python narrow diff | `43c430c32373a62d9c411f0b726fd65732a620b6e8098fcf35130c2efbd4fc46` |
| Julia narrow diff | `0bc4c06ec45b4ad7f2ab8991b3ebeb07c6d7997467dbf630807360812953a3fa` |
| Preserved Python v4 | `60f1e75cad84047e6a9322dab4d2531ca50713bac4893956bd6d9c68a654c38d` |
| Preserved Julia v3 | `da42ab9bf913dd28715824fe4c0b5efbba004d1d5f23be0a32efdadcf6096911` |
| Preserved RawCapture helper | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| Author repair report, read last | `f1cd6d8a4cbf4a67ff2252498b437715417b382703eabf6151590f6b1e32a29f` |

## Единственное finding

`qcl-owned-temp-sampler-v1.py:13–14`:

```python
return isinstance(error, FileNotFoundError) or error.errno == errno.ENOENT
```

Это шире поставленного strict «ENOENT only tolerated; unexpected I/O failguard». Например, объект `FileNotFoundError(errno.EIO, 'I/O')` будет проигнорирован вместо propagation в guard. Для обычных реальных OS syscall exceptions тип `FileNotFoundError` соответствует ENOENT, поэтому исходный реальный rename/unlink race исправлен; finding касается точности заявленной политики обработки ошибок, в том числе deterministic injected controls.

Selftest81–88 закрепляет более широкую политику, принимая `FileNotFoundError()` с отсутствующим errno. Минимальное различающее исправление: `_disappeared` принимает только `error.errno == errno.ENOENT`; missing-class test задаёт `FileNotFoundError(errno.ENOENT, 'gone')`; negative unexpected-I/O cases дополнительно включают `FileNotFoundError(errno.EIO, 'I/O')` и требуют exact exception propagation. Поскольку predicate общий для entry/traversal/iteration, желательно сохранить этот negative case для всех трёх групп. После исправления обновить helper hash во всех hash-bound consumers, selftest hashes/diffs/report; остальной harness code оставить прежним. Runtime ещё не запускать до recheck новых frozen hashes.

## Поддержанные свойства текущего candidate

Helper17–42 использует один `entry.stat(follow_symlinks=False)` и один result для type/size. Исходного `is_file()` → отдельный `stat()` нет. Исчезновение entry, queued directory до `scandir` и enumeration ENOENT охвачено catches; уже учтённые live bytes сохраняются. Другие обычные PermissionError/EIO распространяются; некорректный size (negative/non-int/Bool) вызывает ValueError. Только S_ISREG прибавляется, S_ISDIR ставится в stack, symlinks и non-regular entries не учитываются. Это sampled logical st_size sum, не physical storage/hard quota/atomic snapshot/transient peak proof.

Static directory/file/dangling symlinks не следуются. Directory replacement на symlink между no-follow stat и последующим path-based scandir не защищено; root path также доверен. Это согласуется с явно указанным trusted TEMP/no adversarial namespace assumption, но абсолютное «никогда не следует symlink при любом race» не доказано. Ordinary rename между разными ветвями может дать несовместимую по времени выборку; это не исправляется одной no-follow stat и не обещается metric.

Детерминированный selftest имеет8 конечных методов: real regular/nested+external/dangling symlinks; entry disappearance; directory disappearance; iteration disappearance; exact error propagation при entry/traversal/iteration; malformed size. Entry adapter требует ровно один no-follow stat и падает при повторной observation; тесты тем самым различают старую двухшаговую схему. Реальный nested test требует ровно7 logical bytes и запрещает scandir outside. Моки не проверяют actual kernel scheduling, однако не требуют timing race и адресуют известный failure path. Исходники/stdlib imports ограничены sampler/selftest, harness imports/project tests отсутствуют.

Сам selftest не устанавливает CPU/RAM/wall/TMP/log limits. Его конечный объём файлов (8199B максимум одного live tree) и циклов совместим с заявленным бюджетом, но **≤30s/1CPU/256MiB/1MiB TMP/256KiB logs должен обеспечить отдельный root invocation guard**, а фактический receipt ещё отсутствует. Source review не равен successful selftest и не выдаёт resource measurement.

## Narrow harness delta

Прямые old-new diff обоих harnesses сверены с narrow diff artifacts. Различаются только6 строк hash-bound helper import; `temp_samples=0`; замена старого expression вызовом shared sampler плюс counter после успешного return;3 добавленных receipt fields (sampler SHA/counter/metric). Existing source/fixture identity capture, exclusive `folder.mkdir(exist_ok=False)`, command/runtime/env selection, RawCapture hash/import/start/drain/fallback/write-all, guard exception capture, raw completeness, output envelope/post-drain failure и final all-gates predicate не менялись.

Лимиты прежние: Python90s/1CPU/1GiB sampled RSS/16MiB TMP/2MiB output, Julia120s/1CPU/2GiB sampled RSS/16MiB TMP/2MiB output; output stop threshold сохраняет128KiB запас. Sampler exception попадает в existing `except BaseException` guard_error/guard_exception и final predicate не допускает pass. Hash-bound helper import использует прежний assert pattern; поддерживаемый root launch должен оставаться без Python `-O`/PYTHONOPTIMIZE, иначе assertions отключаются. Это существующее ограничение admission, не новая смена scope.

## Original OPS03 GREEN2

Независимо прочитаны `/tmp/qcl-OPS03-GREEN-2/receipt.json`, `guard-error.txt`, `original.log`. Зафиксированы1.964s, exit−9, `stop_reason=guard_exception`, FileNotFoundError `[Errno2]` между `p.is_file()` и `p.stat()`,15B complete raw capture `...............`. Pytest summary/полного denominator нет. Это guard-interrupted packet;15 dots не доказывают complete product pass или product failure. Старые5calls/failed receipts сохраняются; planned replacement остаётся отдельно admitted call6, не обнулением счётчика. Рецензент runtime budget не расходовал.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Ordinary temporary disappearance double-stat race устранён | helper27 один no-follow stat result; deterministic Entry contract | source-only; selftest pending | сохранить |
| Strict ENOENT-only error policy реализована | helper14 также принимает любой FileNotFoundError | artificial unexpected errno проглатывается | изменить |
| Raw capture/identity/limits/final predicates сохранены | actual old-new narrow diffs и preserved hashes | не новое execution evidence | сохранить |
| Selftest уложился в finite budget | receipt отсутствует | root external guard ещё требуется | дополнительно измерить |
| OPS03 GREEN2 дал product verdict | только15dots и guard traceback | complete denominator отсутствует | данных недостаточно |

STOP. Один узкий predicate/selftest correction и exact-hash recheck; tests/project execution этим review не разрешаются и не выполнялись.
