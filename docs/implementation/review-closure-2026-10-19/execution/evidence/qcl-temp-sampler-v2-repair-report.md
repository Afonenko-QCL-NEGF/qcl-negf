# H1 R1 — strict ENOENT frozen repair

Принят narrow contract independent review `/tmp/qcl-temp-sampler-review.md` SHA `a8ae102fd2c17f92132924febf6b53500ad9064a79512b4a3ec9bf2f8608e488`.

Созданы только новые `/tmp` files. В helper v2 predicate изменён ровно на `error.errno == errno.ENOENT`: класс FileNotFoundError сам по себе не разрешает suppression. В selftest v2 обе positive missing-entry injections имеют ENOENT; отрицательные FileNotFoundError(EIO) и FileNotFoundError() проверяют exact exception propagation для entry stat, traversal и iteration. Eight-method structure, live-file preservation, one-stat, symlink, permission/I/O и malformed-size controls сохранены. Selftest hash-bound к helper v2. Python v6/Julia v5 отличаются от v5/v4 только новым helper path и SHA; capture, limits, counters, receipt metric и final predicate byte-for-byte остались прежними вне этих двух literals.

Старые helper v1, selftest, Python v5, Julia v4 и RawCapture не изменены; hashes пересчитаны и совпадают с предыдущим freeze. Product/app/tests/Git не редактировались. Автор не выполнял imports, helper/selftest/harness/project tests или native commands. Narrow diffs прочитаны; runtime evidence отсутствует.

| Новый файл | SHA-256 |
| --- | --- |
| qcl-owned-temp-sampler-v2.py | 16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e |
| qcl-temp-sampler-selftest-v2.py | b2394500d74441aad5e1539aeecc620fbc1214c7b44fcc9b537f8d458c2624b3 |
| qcl-python-targeted-run-v6.py | 16e908e64bfc6fd9a4467897b9eade95cd8a353535610c52144c2ca912e41b75 |
| qcl-julia-targeted-run-v5.py | a37e9dd52f6c49181f80a956e2de334ff08d6c52653f7c7baae28a08ee7c98f0 |
| qcl-temp-sampler-v2-narrow.diff | 9c10852d5ca504f1a497cd0e55a318ac1be18ca204a9935b2ecfc0f2618c5ec2 |
| qcl-temp-sampler-selftest-v2-narrow.diff | ba4479a01b98749945dd8b4ec72fda6512f869efa2c2ecd11f8ac96419e13d1c |
| qcl-python-harness-v6-narrow.diff | 89f388a2dd6d89f0d826cc64ca439063825c50ce0e297cd5f75680fa944e7ec6 |
| qcl-julia-harness-v5-narrow.diff | 3edfbba8b73af0e7f360e48a445870f35e17c8b46bc0f25d999db8ce057543e4 |

| Сохранённый файл | SHA-256 |
| --- | --- |
| qcl-owned-temp-sampler-v1.py | 3d1dd39cfac5d0ee816e9d79d54c9cd77f6df560efa34407b40ce254b970c9c9 |
| qcl-temp-sampler-selftest.py | b07e1dd56359472c4ab4d051cc2d4b1b236732c50ffdd3299e702d7df41b713d |
| qcl-python-targeted-run-v5.py | 4401dcb5ac03d253166fb0dececa525bfeb15200763f62aa4e579b2a67941e10 |
| qcl-julia-targeted-run-v4.py | 0ecd8c9357840f61646668467e6eaa055039469f81ea706958bd7f400239586b |
| qcl-local-julia-guard-v2.py | e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f |

STOP для independent high review. Selftest — только root после review, один finite packet ≤30s/1CPU/256MiB RAM/1MiB TMP/256KiB logs, внешним guard; helper/selftest сами эти limits не обеспечивают. Старые пять OPS calls сохраняются. Project replacement ещё не разрешён данным freeze; новый root checkpoint/extension обязателен. Нет automatic loop/rerun.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Strict ENOENT predicate реализован | Одно выражение helper v2, negative controls для unknown/mismatched errno | Source-only | изменить |
| Остальные harness gates сохранены | Два literal substitutions в каждом narrow diff | Runtime не запускался | сохранить |
| Tooling selftest/OPS03 готовы | Receipt отсутствует | Independent review и root selftest ещё нужны, product residuals прежние | данных недостаточно |
