# OPS03 Python harness v7 — frozen budget/telemetry delta

Основание: accepted independent wall review `/tmp/qcl-ops03-walltime-review.md`, SHA-256 `7cb5713e1baad15d025ec5a23427675346d19a21484ffc64f7f1612f011c0504`. Это инженерная калибровка finite execution envelope; product/tests и физические/численные критерии не менялись.

Новый `/tmp/qcl-python-targeted-run-v7.py` — копия immutable v6 с ровно четырьмя разрешёнными изменениями:

1. pytest `-q` заменён на `-vv --durations=0` для полного nodeid/outcome/duration evidence.
2. RLIMIT_CPU soft/hard `(90,95)` заменён на `(180,185)`.
3. Monitor wall threshold 90 заменён на 180 секунд.
4. Receipt limits.wall_seconds 90 заменён на 180.

Прочитанный exact narrow diff содержит только эти четыре изменённые строки. Affinity1 CPU, sampled RSS1GiB, sampled trusted-owned-TMP16MiB, nominal raw2MiB/128KiB stop reserve, helper path/hash, sample counter/meaning, RawCapture full drain/fallback/write-all/error preservation, source/attempt identities и final success predicate не менялись. Sampler, Julia harness, product и tests не редактировались. Старый v6 hash совпадает с принятым. Автор ничего не исполнял/импортировал, Git mutations отсутствуют.

| Артефакт | SHA-256 |
| --- | --- |
| preserved qcl-python-targeted-run-v6.py | 16e908e64bfc6fd9a4467897b9eade95cd8a353535610c52144c2ca912e41b75 |
| new qcl-python-targeted-run-v7.py | 47980ee8c5bfebdb10d8f14948bc98d40088ff38c9bc6ace6bdf734cacb3495a |
| qcl-python-harness-v7-narrow.diff | 071a710bbd6b3b95f54957fde15cbfdb12240a16bf12ceccdd3bbfeba25b9e70 |

STOP перед independent exact-delta review. Только root после review и concrete checkpoint выполняет ONE packet7 total с теми же тремя frozen test files, wall180s/affinity1/RSS1GiB/TMP16MiB/raw2MiB. Все шесть прежних consumed calls, failed/interrupted receipts/logs и unknown outcomes сохраняются. Этот freeze не запускает пакет и не разрешает automatic next/retry. Любой interruption остаётся incomplete; complete summary/exit0/no guard требуются отдельно. Provisioning/OS/systemd writer closure, prepare role gap, CR04 atomic admission, native/full-release/science gates остаются прежними отдельными residuals.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Разрешённый budget/telemetry delta внесён | Ровно четыре строки narrow diff | Source-only | изменить |
| Capture/остальные caps/final predicate сохранены | Exact v6→v7 diff | Исполнения новой версии не было | сохранить |
| Full suite завершится в180s/CP-CODE закрыт | Такого runtime evidence нет | Review оценивает110–140s, не гарантирует upper bound | данных недостаточно |
