# H1 — frozen tooling-only sampler repair

Основание: independent review `/tmp/qcl-ops03-final-code-review.md` SHA-256 `ca1d08d9b108877519f30e444d49b5b819f12f94ba4703d57cad69db13ca6aad`. GREEN2 остановлен guard race между is_file и stat; это interrupted packet, test denominator неизвестен. Пять исторических calls и original logs/receipts сохраняются.

Изменены только новые файлы `/tmp`; product/tests frozen GREEN2 не редактировались. Старые harnesses и RawCapture helper не изменены. Никаких imports, helper execution, selftest, pytest/Julia, native/service/SSH или Git mutations автор не выполнял.

## Согласованный механизм

`qcl-owned-temp-sampler-v1.py` содержит чистый sampler без execution on import. Итеративный os.scandir обходит trusted owned TEMP. Каждая entry наблюдается одним `entry.stat(follow_symlinks=False)`; один result используется для типа и размера. Учитываются только regular files. Symlinks не учитываются, directory symlinks не добавляются в traversal. Только FileNotFoundError или errno ENOENT допускают продолжение, в том числе при открытии/итерации исчезнувшего каталога. Другие OSError/PermissionError, malformed regular-file size и прочие ошибки распространяются в existing guard_exception path. Значение — сумма logical st_size наблюдённых regular files; не physical storage, hard quota или доказанный transient peak. При обычном исчезновении часть дерева может отсутствовать в конкретной выборке. Нет adversarial namespace/security guarantee; trusted TEMP assumption сохраняется.

Python v5 и Julia v4 отличаются от старых версий только hash-bound загрузкой этого shared helper, заменой sampler expression и receipt meaning/counter. Counter `owned_temporary_samples_completed` увеличивается только после успешного sampler return. Existing peak field/limits, exclusive attempt mkdir, full source hashes, runtime/env/commands, RawCapture load/hash, drain/fallback/write-all, original error preservation, output overrun и final success predicate не менялись. Receipt дополнен exact sampler SHA и явным metric meaning. Narrow diffs сохранены отдельно.

## Детерминированный selftest (не запускался)

`qcl-temp-sampler-selftest.py`: stdlib unittest, hash-bound импортирует только sampler; не импортирует harnesses и не исполняет pytest. Восемь методов с конечными subcases: реальные live/nested files и external/dangling symlinks; disappearance перед lstat (FileNotFoundError и ENOENT); directory disappearance перед traversal; disappearance во время iteration с сохранением уже учтённого live file; PermissionError/EIO при entry stat, traversal и iteration распространяются exact exception object; отрицательный/string/bool size отвергается. Entry adapter требует ровно один no-follow stat. Реальные test files суммарно 8199 bytes в одном isolated TemporaryDirectory; cleanup после каждого метода. Execution result пока отсутствует.

Root самостоятельно source-reviews и выполняет один отдельно разрешённый selftest packet ≤30s / 1CPU / 256MiB RAM / 1MiB TMP / 256KiB logs до любого replacement project packet. Автор на STOP. Selftest не сбрасывает consumed project calls. Replacement call6 требует отдельного root checkpoint/finite extension latest human grant; automatic retries/reruns не разрешены этим freeze.

## Frozen hashes

| Файл | SHA-256 |
| --- | --- |
| qcl-owned-temp-sampler-v1.py | 3d1dd39cfac5d0ee816e9d79d54c9cd77f6df560efa34407b40ce254b970c9c9 |
| qcl-temp-sampler-selftest.py | b07e1dd56359472c4ab4d051cc2d4b1b236732c50ffdd3299e702d7df41b713d |
| qcl-python-targeted-run-v5.py | 4401dcb5ac03d253166fb0dececa525bfeb15200763f62aa4e579b2a67941e10 |
| qcl-julia-targeted-run-v4.py | 0ecd8c9357840f61646668467e6eaa055039469f81ea706958bd7f400239586b |
| qcl-python-harness-v5-narrow.diff | 43c430c32373a62d9c411f0b726fd65732a620b6e8098fcf35130c2efbd4fc46 |
| qcl-julia-harness-v4-narrow.diff | 0bc4c06ec45b4ad7f2ab8991b3ebeb07c6d7997467dbf630807360812953a3fa |
| unchanged qcl-python-targeted-run-v4.py | 60f1e75cad84047e6a9322dab4d2531ca50713bac4893956bd6d9c68a654c38d |
| unchanged qcl-julia-targeted-run-v3.py | da42ab9bf913dd28715824fe4c0b5efbba004d1d5f23be0a32efdadcf6096911 |
| unchanged qcl-local-julia-guard-v2.py | e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Non-atomic is_file→stat pair устранён | Один no-follow stat result per entry, shared sampler | Source-only до root selftest | изменить |
| Неожиданные sampler ошибки остаются guard failures | Только FileNotFoundError/ENOENT catches; deterministic negative controls | Selftest не исполнен | сохранить |
| Raw capture/limits/final predicate сохранены | Narrow diffs; unchanged RawCapture hash | Runtime новой версии ещё не проверен | сохранить |
| OPS03/CP-CODE ready | Полного test denominator нет | H1 review/selftest и отдельно admitted replacement packet ещё нужны; provisioning/prepare/CR04/native/full-release/science residuals прежние | данных недостаточно |
