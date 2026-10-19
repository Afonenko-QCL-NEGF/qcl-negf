# SCI03-M1 Phase1 RED sources + harness: независимое high review

2026-10-19. Source-only, без выполнения проверяемого Python.
**Tests: CHANGES REQUESTED на SHA `7d2a9d69a0d4cb02334b9b4617a09a9cb3746247eba17f7ebff364eb62ab8921`: одно точечное замечание R1. Harness narrow delta: APPROVED на SHA `98d91c6795ca4c9425c7dd91a62a3619ca703a936ebac6097158924f7c42124b`.**
Тестовый RED intent осмыслен; замечание касается будущей корректной GREEN
реализации и устраняется до расходования конечных RED/GREEN calls. Ни тесты,
ни harness, ни production рецензент не менял. STOP после отчёта и identity.

## R1 — runtime exact zero для суммы defects сильнее Float64 контракта

**Локатор:** `/tmp/qcl-sci03-M1-results-worktree/tests/test_equilibrium_diagnostics.py:716`,
`m1_check_literal_report`:

```
assert bound['state_defects']['raw']['sum_norm'] == 0
```

Этот helper вызывается с fitted finite μ в M1_01 centered/off-centered и M1_02.
Accepted D §6 и Research A.4 требуют складывать полные defects
`D=(N-f*A)+(P-(1-f)*A)`. Даже когда literal raw `N+P=A` точно, такое вычисление
не гарантирует floating-point D=0 при произвольном вычисленном f. Например,
для diagonal entries N=P=1, A=2 и binary64 round-to-nearest-even
`f=1/2-2^-54` имеем:

```
fl(1-f)=1/2
fl(1-2*f)=2^-53
fl(1-2*fl(1-f))=0
D_diagonal=2^-53, хотя exact-arithmetic D=0.
```

Это ручной exact binary counterexample, не исполненный Python check. При
quarter-capacity `f=1/4+2^-54` аналогично `fl(1-f)=3/4` и D=−2^-53.
Actual scalar FD oracle и production masked FD также используют математически
равносильные, но не побитово одинаковые exp formulas. Фиксированные fixture
μ/tolerance/libm не дают source-доказательства, что опасная parity невозможна.
Поэтому assertion может отвергнуть корректное измерение опубликованной нормы
или побудить автора принудительно обнулить c по closure, что контракт запрещает.

**Минимальная правка:** runtime finite-t c_raw проверять тем же существующим
`m1_close(actual, 0)`/M1_ROUNDOFF, которым уже проверяется эта expected row в
строках710–712. Exact dyadic `c_raw²=0` оставить в scalar M1_09; exact zeros
коэффициентов/terms/B при literal boundary Σ=0 в M1_03 тоже оставить. При этом
c=n+p ошибку всё ещё отличают nonzero n/p, отдельные exact dyadic identities
и малый existing fixture bound. Новый scientific tolerance, новый D, ослабление
S1/физических gates или изменение production algorithm не нужны.

Категория: вывод из source/IEEE binary64 algebra; существенность — надёжность
одноразового GREEN и oracle, не scientific accuracy. Контраргумент: конкретный
текущий libm может дать f с cancellation exactly0. Это не даёт переносимого
контракта на всю разрешённую arithmetic chain. Самая дешёвая различающая
проверка — указанная ручная binary expansion и точечная правка runtime assert;
не тратить новую test call для диагностики. Решение: **изменить до freeze RED**.

## 1. Привязка исходников и отсутствие production delta

Сначала перечитаны accepted D, owning Research contract at `3ed8a9f` и Results
production `equilibrium.py` at `33b1a39`. После этого — candidate source,
report/identity/patch и v6 harness/delta. Не использованы broad root/execution
searches; `rg` работал только по явно названным test/harness files.

| Input | Проверенный SHA256 |
| --- | --- |
| Accepted D | `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7` (из принятой earlier R identity; bytes перечитаны) |
| Owning Research file at `3ed8a9f` | `61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c` |
| Baseline production Results `equilibrium.py` | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| Candidate `test_equilibrium_diagnostics.py`, 46686 bytes | `7d2a9d69a0d4cb02334b9b4617a09a9cb3746247eba17f7ebff364eb62ab8921` |
| RED report, 9814 bytes | `dd95cd8eabc86f7978c11a0e0af457a449b02f1b721ef1779acb507b98848d7e` |
| RED identity, 5406 bytes | `c501b2e6f762fc77ba5d84d467bb793ca3d2912de8e91b50fdfb897ad1e0a8ab` |
| RED patch, 18118 bytes | `8c7aa6f21518e86534135c99fec4d354a1162b546f03f8dd85598c9dcc7575b1` |
| Baseline v6 harness | `16e908e64bfc6fd9a4467897b9eade95cd8a353535610c52144c2ca912e41b75` |
| M1 v1 harness | `98d91c6795ca4c9425c7dd91a62a3619ca703a936ebac6097158924f7c42124b` |

Candidate worktree HEAD `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`;
`git status --short` показал только modified tests file; numstat +324/−0,
`git diff --check` без сообщений. Actual diff SHA совпал с frozen patch.
Full **29322-byte** baseline prefix сравнен cmp успешно; baseline SHA
`ce35954b2503d7a910048d6e95bcc6b6b0c88eea40f8a018dc13bdf8ca4bbad0`.
Первый вспомогательный cmp был выполнен на неполную длину28779; затем
исправлен до полной29322, именно полный результат является evidence.
Прежние36 cases/helpers не менялись. Production candidate source SHA равен
baseline; README candidate/baseline SHA совпали:
`39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9`.

## 2. Literal oracle, meaningful RED и compatibility

Остальная new source проверена без blocking findings. `m1_archive` устанавливает
принятые 1E×2k×2×2 full complex entries, W, Γ±, dyadic five-family partition,
embedding_total ровно как сумму sides, GR=−iI и N/Pnormalized. Это synthetic
measurement plane, явно не production grid/model/scientific run. Existing
format/provenance plumbing общая; expected arithmetic не использует `_Norm`,
product FD/μ fit или bound builder. Одна reported μ идёт в scalar finite-t
expectations для обеих versions/sides. Known μ independently проверяется по
bracket, status, stop_reason и width/adjacent endpoints.

Полные norms, corrections/FDR numerators, g±, d, separate B terms и signed
currents согласуются с принятой ручной 2×2 таблицей. Imaginary control добавляет
2ρ²M в occupied defect/sum/correction squared norms и `Im J=13·3M/256` при
ρ=1/32; test проверяет imaginary и hypot, а не только Re current. Quarter
capacity различает f/(1−f) swap. Norm-sum=n+p, false normalized closure,
side reuse, embedding double-count и dropped offdiagonals/imaginary terms
нарушают отдельные assertions, даже если завышенная ошибочная B покрывает J.

Математические exact dyadic f0/scalar commutator controls M1_09 корректны:
Γplus² norm11/32, Γminus21/64, commutator diagonal i/4 и−i/8; unequal k moments
L=7M/512 и R=13M/65536; normalized currents −69M/32768 и17M/32768.
M1_ROUNDOFF=512·2^-53 остаётся accepted engineering fixture policy. При малом
1E×2k×2×2 plane scalar/product/norm reductions имеют ограниченную цепочку;
никакой rigorous libm certificate или device acceptance этим не заявляется.

На baseline production namespace отсутствует. Поэтому до дальнейших norms
должны падать 12 cases через явную missing-instrumentation assertion;
M1_06 ожидает отсутствующий bound-overflow rejection. M1_08/M1_09 — healthy
controls. Итого forecast13failed/38passed из51 соответствует source count
(9 new functions,15 cases), но collection/runtime не выполнялись.
R1 располагается после первого namespace assertion и не меняет meaningful
baseline RED cause; его следует устранить заранее для будущей GREEN, сохранив
исходный snapshot/это замечание. Иное runtime падение должно разбираться до I.

M1_05 проверяет current old FDR и exact matrix-read inventory на unchanged
5E nonuniform fixture: два k и один tile, Areal/imag по4 calls, GR/GL/GG по2,
каждая SL/SG real/imag для пяти internal+трёх embedding families по2.
Всего84 matrix-component reads. Это meaningful regression третьего pass/
added matrix read, не доказательство всей physical I/O или будущей liveness.
Existing36-prefix остаётся отдельной compatibility/invalid-input проверкой.

## 3. Шесть μ gates, overflow и budget controls

| M1_04 mutation | Ожидаемый existing μ status/reason | Source verdict |
| --- | --- | --- |
| Missing context | not_measured/missing_model_context | Корректно |
| Nonzero F | not_applicable/finite_drive | Корректно |
| T_LO=71 вместо70 | not_applicable/unequal_LO_temperature | Корректно |
| e–e mode=closure | unsupported_context/unsupported_electron_electron_closure | Корректно |
| Stored A=0 | not_measured/empty_represented_spectrum | Корректно |
| max_iterations=1 | algorithm_limit/algorithm_limit | Корректно |

Каждая mutation сохраняет literal boundary zero; null gating state defects,
side coefficients и все B terms должен поэтому предшествовать zero shortcut.
Test отдельно проверяет μ=None и independently measured A/correction rows.
Нет conversion unavailable→pass/zero. Zero boundary при defined μ в M1_03
обоснованно сохраняет exact zero coefficients/terms/B и nonzero normalized c.

M1_06: при scaling normalized GL/GG×64, J0=1e308 все arrays/state norms finite.
Signed normalized dimensionless plus current около−0.0161, minus≈0.00396,
так что physical signed currents/их balance finite. Absolute n/p≈sqrt(2M)·63,
g≈0.1 делают J0·g·n overflow. Поэтому expected ContractError invalid_data
различает новый RHS overflow, а baseline не обязан падать на старых currents.
Объявлять exact runtime result без запуска здесь нельзя.

M1_07 задаёт report cap размером old namespace snapshot и требует
budget_exceeded с новым namespace, не truncation. M1_08 missing side datasets
правильно ожидает existing incomplete-embedding guard вместо нулевого kernel.
Existing guards и assertions не удалялись; новый scientific threshold отсутствует.

## 4. Narrow harness variant

Полностью прочитан v6; `diff -u v6 m1-v1` показывает **ровно два** изменения:
line70 TMP guard16→32MiB и line125 receipt `temporary_bytes`16→32MiB.
Сохранены helper/sampler SHA pins, 90s wall loop, single CPU affinity,
CPU rlimit90/95, process-tree RSS1GiB sampled guard, owned-temp sampling,
byte-preserving raw capture/collector-failure fallback, output2MiB with stop
headroom, exception teardown, SIGTERM/SIGKILL, finish/drain, post-drain overrun
и truthful receipt/exit semantics. Sampling caveats не ослаблены: нет hard
cgroup/disk quota/transient-peak guarantee, explicit paths outsideTMP unmeasured.
Дельта соответствует отдельно предоставленному TMP32MiB grant и не расширяет
C08 или science.

Перед coordinator call требуется обычный exact binding: harness fixtures
разрешены только под integration root/components; напрямую `/tmp/...` путь
отклонится. Actual source, old production33b1, selected editable imports и
new frozen test SHA должны совпасть с receipt; guard path restriction сохранять.
Этот review не выполняет binding и не разрешает подмену source path/production.
Два calls RED/GREEN учитывает coordinator; harness сам не создаёт дополнительный
call budget и автоматический rerun из него не следует.

## 5. Scope, resource receipt и решение

Только shell text/Git read/hash/diff/cmp явно названных файлов. Никаких
imports/parsers/test collection/pytest/HDF/Julia/solver/build/network/server/
source writes/Git mutations/children; consumed M1 Python calls0/2, C08=0.
Записаны только этот report и companion identity. Root/checkpoint не изменялись.
Envelope review≤20min/1CPU/2GiB/read3MiB/output96KiB. Повторное source чтение
включая полные sed input files консервативно укладывается в1.5MiB logical
text; physical/kernel/Git-object I/O не инструментировался. Broad execution
subtree searches отсутствуют. Прежние resource receipt gaps не переопределены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED source имеет meaningful missing-feature signal | Actual baseline report constructor, explicit namespace assert и overflow case | Прогноз, runtime не выполнен | сохранить |
| Exact runtime craw=0 переносим | Binary counterexample R1; test716 и full-defect computation | Конкретный libm может случайно дать0 | изменить |
| Literal norms/signs/weights/complex currents и μ gates корректны | Source oracle + accepted D/Research A.1–A.5 | Shared format plumbing; execution нет | сохранить |
| Existing36/prod/README сохранены | Full29322-byte prefix cmp; diff+324/−0; unchanged hashes | Source evidence, не fresh36-pass receipt | сохранить |
| Harness narrowly changes only authorized TMP cap | Full v6 read и exact two-literal diff | Guards sampled; root source binding ещё нужен | сохранить |
| Новые fixtures доказывают scientific/native acceptance | Нет actual final arrays/run/admission/εJ_abs/H | Engineering source-only checks | данных недостаточно |

**STOP. Tests CHANGES REQUESTED: устранить R1 и заморозить новый test/patch
hash перед sole RED. Narrow harness APPROVED exact98d91…2124b.**
