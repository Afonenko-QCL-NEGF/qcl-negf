# SCI03-M1 RED v2 — narrow R1 correction review

2026-10-19. **APPROVED source-only на test SHA256
`d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79`.**
R1 закрыт; иных замечаний в narrow delta нет. Предыдущее полное R
`ba228b23c4d9e17f0c1b35fb171b38cad0d6e75feba2efd9903cedce306299fc`
сохраняется с единственным изменением disposition R1. Этот отчёт не заявляет
executed RED/GREEN, runtime/native/scientific acceptance. STOP.

Прочитаны v2 report/identity/delta, сопоставлены v1/v2 frozen patches и actual
test source. Проверено восстановленное v1 source SHA:
`7d2a9d69a0d4cb02334b9b4617a09a9cb3746247eba17f7ebff364eb62ab8921`.
Actual `diff -u v1-source candidate` содержит ровно одну замену на строке716:

```diff
-    assert bound['state_defects']['raw']['sum_norm'] == 0
+    m1_close(bound['state_defects']['raw']['sum_norm'], 0)
```

Patch-v1→patch-v2 отличается этим же assertion и новым Git blob ID; иных
changes нет. `m1_close` и `M1_ROUNDOFF=512*2^-53` неизменны. Runtime finite-t
closure теперь допускает принятую engineering roundoff ошибку; product defects
не обнуляются и scientific threshold не добавлен. Проверка c=n+p по-прежнему
различима: raw n>0, normalized c>0 и separate norms сохраняются, а допустимый
runtime raw c мал по прежней fixture policy.

Exact dyadic f0 identities/commutators и c_raw²=0 в M1_09 сохранены. Literal
boundary-zero exact coefficient/term/B/current assertions M1_03 сохранены.
Другие oracle, шесть unavailable-μ gates, overflow, read counts, report cap и
meaningful missing-namespace RED mechanism не менялись; они covered прежним
полным source R. Source forecast51 cases,13 expected RED failures/38passes
не является collection/runtime receipt.

Worktree HEAD/base `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`, sole modified
path `tests/test_equilibrium_diagnostics.py`, +324/−0. Full29322-byte baseline
prefix cmp успешен. `git diff --check` без сообщений. Actual diff SHA совпал
с frozen v2 patch. Production/README hashes и ранее одобренный harness сохранены:

| Объект | Проверенный SHA256 |
| --- | --- |
| v2 report | `139a0e3a0fd3234db1a65b39db3b31aad14c8e27cf8d19db6a6d201748e6fd2e` |
| v2 identity | `ab7a1359b7f5a0148a43501a0060a0b8d05051bf630249af2d15e72011edb0c8` |
| v2 delta | `5ed2c20740d13b4c35c6b545337d59c669985f7463f8c248c68a03072d343ec1` |
| v2 patch | `c599065fd8e38d5e165693b091a075cee1ac9f128601f3a1b748ac47dcc45acc` |
| Production equilibrium.py | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| README | `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9` |
| Approved M1 harness | `98d91c6795ca4c9425c7dd91a62a3619ca703a936ebac6097158924f7c42124b` |

Read-only Git с GIT_OPTIONAL_LOCKS=0; только explicit named source/receipt files,
без execution subtree поиска. С учётом полных inputs для sed/diff/hashes
консервативный logical text ledger <700KiB, в пределах1MiB. Physical/kernel/
compressed Git-object I/O не инструментирован; прежние gaps не пересмотрены.
Envelope≤10min/1CPU/2GiB/output32KiB. Imports/parsers/tests/collection/HDF/
Julia/solver/build/network/server/sourcewrites/Gitmutations/children=0.
Consumed M1calls0/2, C08=0. Записаны только этот report и identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 исправлен без нового допуска | Exact single-line diff и unchanged m1_close | Runtime ещё не выполнен | сохранить |
| Dyadic zero controls/base36/prod сохранены | Full-prefix cmp, sole-line delta, hashes | Source evidence | сохранить |
| Full source R и harness approval применимы к v2 | Остальной delta отсутствует; harness SHA неизменен | Coordinator exact binding и finite calls отдельно | сохранить |
| RED/GREEN/scientific acceptance установлены | Ничего не исполнялось | Final arrays/admission/εJ_abs/H отсутствуют | данных недостаточно |

**STOP REVIEW. APPROVED exact test SHA d4bb720f…f87f79; никаких дополнительных
calls, автоматических reruns или scientific grants.**
