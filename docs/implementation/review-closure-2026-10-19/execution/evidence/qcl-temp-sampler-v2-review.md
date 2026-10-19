# H1 R1: final narrow source recheck

Вердикт: **READY для одного root stdlib selftest packet** в явно заданном бюджете ≤30s /1CPU /256MiB RAM /1MiB owned TMP /256KiB raw output. Замечание предыдущего review закрыто. Это source readiness, **не selftest PASS и не product verdict**. После фактического successful selftest новые harness versions могут использоваться в отдельно admitted bounded project packets; automatic retry или сброс пяти старых OPS calls этим review не разрешён.

Рецензент прочитал actual new sources, direct old/new diffs и hashes; author report прочитан последним. Python/Julia/helper/selftest/import/project tests не исполнялись, Git не вызывался, исходники не изменялись. Создан только этот report. Предыдущий review сохранён: `/tmp/qcl-temp-sampler-review.md`, SHA256 `a8ae102fd2c17f92132924febf6b53500ad9064a79512b4a3ec9bf2f8608e488`.

## Сверённые immutable identities

| Файл | SHA256 |
| --- | --- |
| `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| `/tmp/qcl-temp-sampler-selftest-v2.py` | `b2394500d74441aad5e1539aeecc620fbc1214c7b44fcc9b537f8d458c2624b3` |
| `/tmp/qcl-python-targeted-run-v6.py` | `16e908e64bfc6fd9a4467897b9eade95cd8a353535610c52144c2ca912e41b75` |
| `/tmp/qcl-julia-targeted-run-v5.py` | `a37e9dd52f6c49181f80a956e2de334ff08d6c52653f7c7baae28a08ee7c98f0` |
| helper v2 narrow diff | `9c10852d5ca504f1a497cd0e55a318ac1be18ca204a9935b2ecfc0f2618c5ec2` |
| selftest v2 narrow diff | `ba4479a01b98749945dd8b4ec72fda6512f869efa2c2ecd11f8ac96419e13d1c` |
| Python v6 narrow diff | `89f388a2dd6d89f0d826cc64ca439063825c50ce0e297cd5f75680fa944e7ec6` |
| Julia v5 narrow diff | `3edfbba8b73af0e7f360e48a445870f35e17c8b46bc0f25d999db8ce057543e4` |
| Author report `/tmp/qcl-temp-sampler-v2-repair-report.md` | `d390dc81d5871990f1298f9951541ff08a642f9662a04f0626928b3cb64b4223` |

Непосредственно сверены и сохранённые identities: helper v1 `3d1dd39cfac5d0ee816e9d79d54c9cd77f6df560efa34407b40ce254b970c9c9`; selftest v1 `b07e1dd56359472c4ab4d051cc2d4b1b236732c50ffdd3299e702d7df41b713d`; Python v5 `4401dcb5ac03d253166fb0dececa525bfeb15200763f62aa4e579b2a67941e10`; Julia v4 `0ecd8c9357840f61646668467e6eaa055039469f81ea706958bd7f400239586b`; RawCapture `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`. Предыдущие версии не заменены новыми bytes.

## Закрытие strict ENOENT finding

Actual helper diff содержит ровно одну строку: `_disappeared(error)` теперь возвращает только `error.errno == errno.ENOENT` (v2:13–14). Ошибка с неизвестным errno или `FileNotFoundError(errno.EIO,...)` больше не подавляется. Predicate одинаково применяется к entry stat и к outer scandir/open/iteration catch; unexpected errors проходят без замены original exception в existing harness guard path.

Actual selftest diff ограничен helper path/hash, explicit ENOENT в positive missing-class injection и negative `FileNotFoundError(EIO)`/`FileNotFoundError()` в каждой из трёх групп entry/traversal/iteration. Для всех negative cases требуется точный исходный exception object через `assertIs`, не только тип. Следовательно, старый v1 predicate провалил бы шесть новых negative subcases. Eight-method structure, successful live-file counts, one-stat/no-follow assertion, static external/dangling symlinks, ordinary permission/EIO и malformed sizes сохранены. Positive disappearance во всех трёх местах содержит ENOENT явно.

Один no-follow stat result на entry, regular-only logical bytes, iterative traversal и preservation уже наблюдённых live bytes остались прежними. Устранена известная ordinary temporary disappearance race между `is_file()` и отдельным `stat()`; данные source по-прежнему не обещают atomic snapshot или adversarial path-swap protection.

## Harness gates unchanged

Direct Python v5→v6 и Julia v4→v5 diffs содержат ровно два literal substitutions: helper path v1→v2 и exact helper SHA. Все остальные строки byte-identical. Таким образом, прежний independently reviewed narrow capture delta остаётся применим: raw capture helper binding/start/drain/fallback/write-all, original errors, exclusive attempt directory, fixture/source identity receipts, command/runtime/environment, sampled peaks, completed-sample counter, metric receipt, limits, output overrun и final success predicate сохранены.

Python limits90s/1CPU/1GiB sampled RSS/16MiB TMP/2MiB output и Julia120s/1CPU/2GiB sampled RSS/16MiB TMP/2MiB output не расширены. Helper exception приводит к guard_error/guard_exception; final predicate требует отсутствие этой ошибки. Hash-bound asserts предполагают root launch без `-O`/PYTHONOPTIMIZE, как и прежние harnesses. Это не новая resource admission и не standalone guarantee hard quota.

## Что ещё должно быть измерено

Selftest содержит конечные8 unittest methods и небольшие real fixtures (максимум8199B одного live tree), импортирует только hash-bound pure helper и stdlib. Он не включает project/harness execution. Внешние30s/1CPU/256MiB/1MiB TMP/256KiB raw limits root должен применить отдельно; сами helper/selftest их не устанавливают. Receipt ещё не получен, поэтому runtime статус **not_measured**. После единственного selftest root сохраняет actual8-method result, helper/selftest SHA и полный raw/error outcome.

Только subsequent successful bounded execution даёт новый project denominator. Старый OPS03 GREEN2 остаётся guard-interrupted1.964s/exit−9/15dots complete raw без complete pytest summary; ему не приписывается pass задним числом. Пять исторических OPS calls остаются учтены; planned project replacement call6 требует собственного root admission/finite extension. Рецензент runtime calls не расходовал.

Trusted owned root/non-adversarial namespace остаётся precondition: static symlinks не следуются, но directory replacement между no-follow stat и path-based scandir не защищено. Metric — sampled logical st_size sum, не physical bytes, hard quota, instantaneous snapshot или доказанный transient peak. Ни project/native/scientific/full-release acceptance этим tooling readiness не устанавливается.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Strict ENOENT-only suppression и unexpected-I/O failguard реализованы | helper14 и exact propagation controls entry/traversal/iteration | source-only до selftest | сохранить |
| Single-stat/regular-only/static-no-symlink sampler сохранён | exact single-line helper diff | trusted namespace; sampled metric | сохранить |
| Capture/identity/limits/final guards сохранены | только helper path/hash меняются в двух harness diffs | external admission обязателен | сохранить |
| Selftest прошёл finite budget | actual receipt отсутствует | один root bounded packet pending | дополнительно измерить |
| Старый OPS03 packet получил product pass | полного denominator нет | tooling correction не ретросертификация | данных недостаточно |

STOP. Source READY для одного отдельно bounded stdlib selftest; никаких execution/retry или source edits рецензент не выполнял.
