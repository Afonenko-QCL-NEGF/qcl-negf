# Кампания133: заключительный отчёт после перезагрузки

**Исходный native real-energy SCBA solver до сходимости не доведён.** Последняя согласованная пара0/1мВ без e-e завершена; по прямому указанию пользователя вычислительная кампания остановлена. Выявлены чувствительность к начальному заполнению и конкретная незакрытая lesser-компонента embedding; причина нелинейной медленной сходимости целиком не доказана. Далее — только сохранение, независимая проверка и публикация; будущие методы не запускались.

Старт кампании неизменен: **15 ноября2026,16:33:33UTC**. После reboot пользователь продлил report/STOP до16ноября17:00Минск/14:00UTC, heavy cutoff13:00UTC; последнее указание означает более раннее завершение после текущего run. Фактическая новая VM:26CPU,29,246,926,848B RAM, Julia1.13.4; BLAS задавался setter/getter1. Один тяжёлый Julia-процесс, OS memory/CPU/swap/file/time limits, свежий RAM/data admission перед запуском. Общий output cap повышен **до72GiB до FD actual**, старые массивы не удалялись. Active human minutes не измерялись; ручные start/steering/abort пользователя не считаются нулевым участием.

## Identity и исторический результат

[Отчёт A / Root136](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/136), merge`e74aef3b0520da80ad56d36643e58599707abe97`, сохраняет прежний meaningful finite-N/M3 equilibrium reference. Он относится к отдельному fixed-U0/V0 all5/direct-static/full-line-LO/reference-tail finite45/hH варианту, не к принятому original native baseline, Poisson или finite-bias transport. Старые native baseline имели Coref50/Julia1.13.3; postboot science — **Coree171**, отдельная принятая интеграционная пара — **Coredb26/Runner53b**. Их source identities не объединяются задним числом.

Postboot matched0/1mV/period: full native R/L/G, all5/no correlation e–e, U0/70K, direct-staticC+LOPIFFT, finite_chain4, Nz96/Nb5/Nk11, E[−.3,.9]eV. Coarse N24001 означает50μeV, LO734steps и field20steps при1mV. Fine N48001 — отдельный cold-grid control. Fixed-Hartree опыт не является самосогласованной electrostatic/device задачей.

## Завершённые траектории и последний FD control

Raw rK/rΣ/rλ приведены до признания fixed point; нормированная native paired density не заменяет raw charge gate. J указан вA/cm² **только как диагностика несошедшегося состояния**, не I–V, conductance или power prediction.

| Ветвь | Completed maps / статус | rK | rΣ | rλ | J,A/cm² |
|---|---|---:|---:|---:|---:|
| Cold N24001,0mV |32,unresolved|0.531711|0.316054|0.0392018|−614.984|
| Cold N24001,1mV |32,unresolved|0.503138|0.212567|0.0251051|2.95978|
| Fine N48001,0mV |32,unresolved|0.494176|0.278510|0.0376794|−591.561|
| Fine N48001,1mV |29,USER ABORT|0.311393|0.241417|0.0297145|−66.0137|
| Unmodified warm128,0mV |128incl.replay,unresolved|0.0239599|0.122988|0.00291043|115.496|
| Unmodified warm128,1mV |128incl.replay,unresolved|0.0121243|0.0507753|0.00117496|17.3171|
| One-time FDseed128,0mV |128,unresolved|0.0093542976|0.015346101|0.00047343381|-0.16849126|
| One-time FDseed128,1mV |128,unresolved|0.0021297946|0.0065082864|0.00017553328|2.6055344|

Coarse32 — законченная пара, reviewed в `reviews/native-bias1mV-result.md`. Finecase0 сохранён полностью, case1 пользователь остановил после29: это **не accepted matched32 pair**, не доказанная fine-grid accuracy или отрицательный результат сходимости. Все partial files/abort metadata сохранены.

Warm128 starts от соответствующих coarse32 полных состояний без изменения Green: первая map повторяет boundary, поэтому **127новых состояний/case при128 вычислениях карты, nominal terminal159**, не160. Перенос GR/GL/GG/A и13boundary scalars воспроизведён; все256strict-pass flags false/streak0. Лучшие joint defects не совпали с последними: монотонность не установлена. См. `reviews/native-bias1mV-warm128-max26-result.md`.

FDseed — **ровно одна initialization**, не итерационная FD restriction: source retarded GR/A сохраняются, native common-μ number fit формирует начальные GL/GG, затем128 ordinary full R/L/G maps без нового FD. Все блоки source A и восьми retardedΓR проверены по прежнему native PSD/Hermiticity budget до изменения L/G, без clipping/floor/ΓK substitution. Это численный budget-pass, **не exact PSD-сертификат**: например, в source embeddingΓR при0mV обнаружен minλ≈−1.34e−13, допущенный исходным backward-error budget; отрицательное значение не скрывалось и не обнулялось. Начальные λ≈1 и J≈0 **сконструированы**, это не equilibrium/native acceptance. Смена seed имеет новую identity; она не превращает warm control в сошедшийся baseline. Source folder: `native-bias1mV-FDseed128-max26/attempt01`. Оба случая завершили128карт, `max_iterations/unresolved`, scientific acceptance=false. По сравнению с unmodified warm128 конечный rΣ уменьшился примерно в8.01× при0mV и7.80× при1mV; это finite-budget initialization effect, не сходимость. Рабочая политика residual4/other26 изменяет выполнение измерителя, raw-гейты и физические Φ не менялись; время двух разных траекторий не является чистым benchmark ускорения.


**Доказанная локализация незакрытого условия:** при0mV максимальный component-relative rΣ приходится на `embedding_plus.lesser`: norm-difference0.00243838911 / scale0.1588930693 =0.0153461. При1mV тот же компонент:0.001080255419 /0.1659815436 =0.00650829. Масштабы далеко выше native floor1e−14; это не только деление на почти нулевой канал. В обоих случаях lesser-компоненты total/minus embedding также не самосогласованы. Одновременно rD≈(2.5–4.7)e−16, rA≈(5.3–8.0)e−15, rPSD=0 в native budget. Малые уравневые rD/rA и точно нормированное число не закрывают fresh Keldysh/Σ/λ условия; они также не дают универсальной forward-error границы при плохой conditioning. Это локализация остаточной ошибки данной траектории, не доказательство единственной физической/сеточной причины или невозможности дальнейшей сходимости.

## Ресурсы: измерение вместо предположений

Warm max26 pair завершилась1587.40s, CPU28325.98s≈17.84cores в среднем, peak17,083,142,144B, Swap0/oom0. Residual phase заняла857.35s wall/21217.59CPU: она доминирует в измеренной траектории, но уже использовала≈24.6cores в checked segment. Называть её serial bottleneck неправильно; process allocation counters также не доказывают RSS leak.

Отдельный **residual-suite surrogate**, не Φ/SCBA, сохранил все5metrics/12witness bits в14calls. INFO layouts имели26раздельных cache-line spans: specific INFO-to-INFO sharing не подтверждён, padding выигрыша не дал. Median W4=1.424913s против W26=3.504493s: **W26 медленнее2.45944×**; причина и end-to-end gain не установлены (`reviews/core32-info-padding-result.md`, summarySHA`599026d2…`).

Поэтому последний FD run использует **существующий phase_request: residuals4, остальные phases26**, BLAS1; это execution policy, не изменение Core/физики/strict gates. Его actual hard20.75GiB/high20.25GiB/Swap0 приняты свежим admission; preflight отказ старого большего cap произошёл до Julia, guard не обходился. FD-пара заняла1228.41s, processCPU8927.38s (в среднем7.27CPU), peak16,765,247,488B, high/max/oom0. Это цена всей другой траектории с source checks/fit, не изолированное end-to-end сравнение. Native estimate — не rigorous RSS upper bound: coarse actual peak превышал estimate примерно на2.08GiB.

[Core issue32](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/issues/32) и три независимых review — `core32-scientific-review.md`, `core32-api-review.md`, `adjacent/residual-cost-addendum.md` — отделяют safe proposals от доказанной эквивалентности. Opt-in state-only checkpoint и lazy diagnostic work требуют отдельных regression/oracle checks; никакой Root/Core refactor здесь не выполнен, eigenvalue/INFO guards не удалялись.

## Сохранность и один будущий discriminator

Research[PR14](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/pull/14) merged`3ac74cb1272ded02a183f6ae817917d2b7688040`, tree`64d8d3f1…`; manifest1632entries SHA`e3da9ea2d74069b82c8b9bdff7348e6671ab591896db62df532e56f076980e22`, независимые source/public/privacy checks выполнены. Это frozen public evidence packet, не публикация всех локальных raw HDF5. Большие состояния остаются локально; старый archive read-only. Финальные FD/benchmark артефакты и независимые обзоры сохраняются отдельным следующим snapshot; они не подменяют уже merged snapshot. Полные FD states SHA256:0mV `b175f676c28f80b330a43c162ee18acdcb68ec5c30c45e92b618b961c47530a9`,1mV `a34db685669bdde89351e7854f1eadd74e8f93a545462a5711cc7384a5922279`; полные остальные source/environment hashes находятся в immutable attempts и manifests.

**Единственный следующий различающий опыт, FUTURE/UNRUN:** на том же сохранённом старте1mV и при том же ограниченном бюджете Φ сопоставить записанный native контроль с Green-variable AA5; сначала проверить один полный unprojected composition map и затем потребовать три последовательные пройденные strict-native проверки на кандидате, считая все фактические Φ в общем лимите. Это отдельное будущее поручение. Сравнивается та же native root с Green-variable map X=(GR,GL,GG), сохранив все5 fresh self-energies, embedding, normalization и финальные native gates. История одного state —3F вместо21F native families; это не live-set/RSS/speed bound. Source/math assessment `adjacent/green-variable-map-assessment.md` отдельно связывает roots при rawλ=1; независимый source/docs review `reviews/green-variable-future-review.md` подтверждает только эту узкую эквивалентность. Каждый raw T(G) сохраняется; проекция разрешается только следующему trial. Малый projected step не означает raw root, materializeΣ→nativeDyson→freshΦ и full native exit обязательны. [Walker–Ni2011](https://doi.org/10.1137/10078356X) связывает AA/GMRES только при линейности, full history и условиях отсутствия stagnation: наша nonlinear/truncated/projected SCBA гарантии не получает. См. `adjacent/green-AA-primary-sources.md`. Ничего из этого не реализуется и не запускается после текущего FD run.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Coarse/warm native state ещё unresolved | Полные scalar histories/strict flags и result reviews | Не steady-current/IV | Сохранить, не принимать |
| Fine pair прерван |32+29maps/USER ABORT | Нет matched-grid error bound | Сохранить partial, не достраивать |
| INFO sharing не поддержано | Layout witness и fixed-input surrogate | Не причина всех затрат | Не refactor по этой гипотезе |
| FD seed улучшил ограниченную траекторию | rΣ ниже8.01×/7.80×, обе max_iterations | Initialλ1/J0 — construction; raw128 не прошли | Сохранить, не принимать |
| Green3F — будущая гипотеза | Source composition и conditional AA reference | Не convergence/RSS theorem | Только отдельное новое поручение |

**STOP:** все научные процессы завершены после последней FD-пары; никаких дальнейших опытов в оставшемся временном резерве не запускается.

## Финальная запись сохранения

Научный численный этап окончен **16 ноября2026,08:11:40UTC /11:11:40Минск**, после последнего FD run по прямому указанию пользователя. После этого выполнялись только проверки сохранённых артефактов, review и публикация. Новых solver/Φ/benchmark запусков нет.

Заключительный public packet принят через [Research PR15](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/pull/15): merge`76926d0035eeddf7c59a8c4357ab98f4e3bc9eba`, tree`7b6d7becf7adaf6d9b8b451244f4fee0aea15b13`. Manifest **1669entries**, SHA256`b418df939befe2e3f6266da54a005cfc38bc587897419c7c22a00828f0a1df15`; прежние1632строки сохранены побайтно. Семь проекций явно помечены, большие HDF5, private environment/addresses и authorized inputs не публиковались. Independent publication reviewSHA`400fc2e345385a5b6c82938bc6f0ad8eae835f9c63ce0996a11f54f148681ba2`.

[Независимый scientific review](issue133-postboot-independent-review.md) одобрил точный scientific body SHA256`ed34d4344cb6d265872e13ce62f47486863c2944421b38667bed60a82665f942`. Этот финальный раздел добавляет только даты, ссылки и preservation metadata; scientific body не изменён. FD result reviewSHA`c3256c15f63b47f02c1fdc2027495deb1a4c4e0f58fdb28a3db8a5a57990a624`, Green future reviewSHA`d75f9de1a336de607e588f6ed7a507ace54c787e5a90741301abaeab14254510`.

Все **7завершённых state.h5 и7model.h5** повторно проверены потоковым SHA256 по исходным summaries и fsync; исходный старый архив не изменялся. Учтённые logical files старого/нового workspace:67,215,577,426B при cap72GiB; integrity JSON и большие массивы сохранены локально в соответствующих `.build/campaign133/`. Это размер файлов, не измерение RAM или величина публичного пакета.

Кампания закрывается без научного acceptance исходного solver; Core issue32 остаётся отдельной задачей пересмотра. Новый научный запуск требует отдельного поручения.
