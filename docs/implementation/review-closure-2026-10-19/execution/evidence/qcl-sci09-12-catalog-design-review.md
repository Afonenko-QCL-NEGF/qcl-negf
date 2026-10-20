# SCI09/SCI12 — independent CP-DESIGN R1

2026-10-20. **APPROVED для source catalog и conditional predicate design** exact D1 SHA256 `b80c5e354a0453a7151fc243f7a98d97f14c722baef733d7a53e0166fb7d998d`.
Блокирующих отклонений от P1/S1, SCI03 error/raw contract и SCI07 resource contract в данном source design не найдено. Этот verdict не означает CP-SCI READY/BIND, runtime или scientific acceptance. SCI12-MAP не объявляется готовой implementation-задачей: её точные операторы и literal oracle ещё должны быть заморожены (§5 ниже).

## 1. Scope и immutable source

Независимый reviewer / high. Применён qcl-physics-audit; прочитаны actual AGENTS, architecture, applicable skill и physics-checks. Сначала проверены P1/science и owning SCI03/02, затем D1. Рассмотрены primary SCI04 D2 sections 2–4,8 locators, accepted R2 и SCI07 D1/D2. Не выполнялась повторная полная экспертиза формул уже принятых SCI02/03/04.

Actual Root HEAD `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`; 8 direct gitlinks совпали с `git submodule status --recursive`. Git-derived `git ls-tree HEAD:components | sha256sum` = `39529e5f6ecf26b57e005b0d8712ccef96a191099be182785e3b43b525fa1b0f`. Это observation receipt, не второй maintained source lock. Tracked dirty checkpoint/census и concurrent untracked execution evidence сохранены; reviewer их не менял и не принимает за frozen scientific input. Actual runtime/source import, model/plan fingerprints, P0/A1, execution/attempt/state IDs и admission не наблюдались и остаются null с причиной source-only. `run=not_created` здесь — статус проверяемого нового S1 design, не утверждение о старом защищённом S01.

Проверены hashes D1, identity `5a10537ac3f7fd1b966a102d4def872e2f1a36d0081543f8a87dd7e7ba0817f1`, ledger `9ea2d0eb79f4f3fceb695be6dff60d492e2fbbc774df494fa7f6e4269b8a1ef0`. Owning Research measurement contract SHA `61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c` совпал. SCI08-R1 PR16/engineering349 сообщены координатором; в reviewed Root gitlinks ещё прежний Runner fefaa27. Их runtime/CP-CODE closure этим review не устанавливается.

## 2. Проверка finite catalog и модели

**Сохранить.** P1 `operator-permissions.md:183–246`, `science.md:129–148,405–417,446–460`; D1:26–67,71–79,120–127.

Все rows сохраняют 0 mV/period, lattice/LO70 K, пять LO/acoustic/impurity/IFR/alloy, e–e none, finite_chain4 и strict policy. B0 читает model→analytical-diagnostic→study overrides; фактический model содержит 56 mV/alloy=false, поэтому D1 правильно требует effective override0/alloy=true и e–e runtime binding, а не проверку одного файла. Primary provenance caveat sheet/caption сохранён, новая dose interpretation не вводится. Locator: Research `config/studies/equilibrium-0-70.yaml`, `config/policies/analytical-diagnostic.yaml`, `config/model/reference-2019-70k.yaml`; `docs/reference-2019-model-passport.md:42–80,202–246`.

Exact E1/P1/K1/W/Z/B/A/Q дельты соответствуют science wave table. C имеет Nk16/kmax.9 и energy_max1.2/NE38401, сохраняет radial step.06 и energy step39.0625 μeV; это явно coupled cutoff/window. Общий C/W domain [-.30,1.05], W-only low и C-only high strips сохраняются; C−W не объявлен чистым cutoff bound. B basis5→7 требует физических projectors/coherence/local current, embedding4→8 исключён.

13 slots =4+5+1+2+1 и 936 node-hours =288+360+72+144+72; max1 submit/row,72h/attempt,concurrency≤2. R1/R2 только cause-specific same-physics repair/approved row, не method/mixing roulette. Unknown submit reconcile, failure debit не сбрасывается. Два одинаковых successive fingerprints останавливают affected wave, не весь независимый source work. Новый каталог не продлевает C08=8/8 и не разрешает tests/solver.

Runner source support проверен без исполнения: `planning.jl::_comparison_inputs` удаляет лишь run/output/study и exact controlled leaves; `_validate_controlled_variant` поддерживает discretization/representation; independent points получают predecessor=nothing/:cold; dedup использует effective seed. D1 правильно не приравнивает administrative row/method labels к actual execution membership/fingerprint. Real C01 ещё нужен; source-expressible не означает resolved/frozen.

## 3. Error contract, raw audit и H

**Сохранить.** Owning Research `docs/equilibrium-measurement-contract.md:92–124,248–368`; SCI04 D2 §§2–4,8; D1:79–116,121–127,137–141.

W=gs/(2π)·wE·wk применяется один раз; native wk уже содержит radial factor. Full matrices/coherence, raw/normalized, stored/fresh и signed channel integrals различены. J± в A/m² и near-zero absolute εJ не заменяются division/J. Backward/fixed-point residual не превращён в forward solution bound; η/μ/n/U/J targets, nonlinear conditioning, tails, quadrature/truncation/interaction остаются unknown. Двух h недостаточно для Richardson order, common-domain sensitivity не infinite-domain bound. Pilot допускает только labelled measurement при остальных guards/gates; новая A1 не ретроактивна к pilot.

Fresh audit должен относиться к одному final U/G/n, unmixed candidate Σ/embedding и Poisson map, с complete native/commit equality/state lineage. Stored reader не переименован в fresh-map oracle. SCI04 scalar/metadata/full final ownership contract сохранён; source design не доказывает конкретный final или independence общих production kernels. D1 §7 правильно требует B0 strict same-final closure до accuracy refinements.

H+candidate.h/4 совпадает с заранее предложенным SCI03 §8. Это существующий enum discretization и только два controlled endpoints, fixed width/NE/physics/method/strict gates; ordinary FD cold seed не initial-amplitude sweep. Доля/знак заданы до pilot. Deterministic first-eligible single row order не создаёт combined конфигурацию и не выбирает минимальную измеренную ошибку. Eligibility требует strict closure, complete raw, A1 targets/bounds/controls/feasibility и invalidation/reuse affected proof после correction. Новая source identity не наследует старую приёмку.

Embargo строже минимального требования: до доступа к H raw frozen exact A1, selected candidate source/plan, controls и H plan. H не используется для ε/coefficient/candidate selection, failure съедает единственный H slot, новые criteria тот же H не принимают. При missing ε/bound/candidate H не запускается. H подтверждает только заявленный finite contract/phase robustness, не continuum tails, conditioning или глобальную эргодичность. Это допускает конечный честный unknown без нового интервью.

## 4. Resource contract

**Сохранить.** P1:224–246; SCI07 D1 §§2,6–10 + normative D2 §2 override; D1:60–67,127,142–149.

W1 per-attempt128GiB/2TiB writes/4TiB reads/1GiB logs; later256GiB/4TiB/8TiB/1GiB; shared2TiB current resident/44TiB writes/88TiB reads/13GiB logs. Logs входят в resident/write, protocol/hash/retrieval/export duplicates учитываются. 4×128+9×256=2816GiB=2.75TiB local maxima превышают shared2TiB; D1 прямо запрещает удалять protected finals/failed raw ради следующего slot. Нужен меньший доказанный actual bound/placement либо stop, не silent prune, меньшее physics/window/basis или повышенный cap.

Per-FS alias/lifetime, retained2+pending+pointer/receipt/final, logical/physical/inode views и shared leases обязательны. D2 T=E+U+P+S≤A и отдельно G=U+P+S≤H передаётся без double debit. Quota/io.stat/engineering GREEN не заменяют complete NFS/cumulative coverage и native admission. Unknown counter, missing guard/stop headroom/identity — отказ до growth, OOM/ENOSPC не normal stop. Неизвестная capacity не заполнена паспортными32CPU.

Recovery8GiB/64MiB остаётся существующим default, не доказанной operational allowance. Перед BIND нужен explicit calculated recovery budget/reserve внутри S1 lease по SCI07 D1 §6 (последний абзац), после SCI08; его изменение не должно скрываться как scientific delta. D1 §28 это ограничивает, §8 сохраняет fit/admission неизвестными. Данный review не закрывает этот runtime input.

## 5. Минимальная следующая работа и оговорка о READY

**Готов source-only ticket SCI09-CAT-SOURCE / Research:** добавить actual ten-row static meta/one-row YAML и catalog doc по D1 §§2–4, сохранив existing B0 и historical48/56; точные variant overrides/controlled_paths, effective0/70/all5/no-e–e intent, caps и conditional membership. R/H не materialize до predicates. Проверить reviewable text diff/order/leaves и protected historical files; не выполнять parser/resolver/tests в данном scope. После owning publication Root выбирает published gitlink. Actual plan/fingerprint/membership остаются null до отдельно bounded C01 в prepared environment; missing runtime не разрешает install.

**Готов следующий design ticket SCI12-MAP-D / Research+Results/Core:** exact boundary-cell partitions, E/k overlap/interpolation, spatial coordinate/cell semantics и conservative transfer, cross-basis projector/current operator; frozen literal controls, output status/null rules и finite read/derive envelope. D1:89–104 уже перечисляет измеримые outputs и требуемые negative controls, но не полностью задаёт эти операторы. Фраза D1:102 «Ready D→I ticket» должна читаться вместе с её явным «Перед I ... freeze» и §8:139; это условный precursor, не немедленный I-ready reducer. Source verdict не разрешает исполнителю угадать interpolation/current operator или написать API по усмотрению.

Это nonblocking clarification границы данного approval, а не разрешение нового author round/compute. До точного operator/oracle freeze SCI12-MAP implementation остаётся blocked; независимая подготовка каталога продолжается. Полная S1 technical READY всё ещё требует actual SCI02/03/04/06/07/08 closure, P0/A1/plan/runtime bindings, fresh native guards/admission и остаток общего бюджета.

## 6. Проверки и ограничения

Только read-only Git/text/SHA/source operations и bounded Python stdlib для записи этих двух review outputs; никаких product imports, parser/resolver/compiler/tests/Julia/Pkg/SCBA/Poisson, network/server/native/archive execution. Научные arrays не открывались. Scientific submits0, test calls0, product/CP writes0. Read content консервативно <4MiB (предел8MiB), новые artifacts <128KiB; CPU/RSS/syscall I/O не измерены и не объявляются enforced cgroup profile. Бюджет15min/1CPU/2GiB соблюдён по объёму ручного source review; runtime resource measurements отсутствуют. Повторные truncated tool outputs не считаются прочитанным целым: важные H/caps/raw/transition sections были доступны отдельными ranged reads. Review не переоценивает unrelated full release/native gates.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Finite source catalog и H predicates соответствуют S1 | P1:183–246; science:129–148,405–460; D1:26–79,106–127; Runner planning symbols | Actual YAML/plans/membership ещё не созданы | сохранить |
| Error/raw contract не ослаблен | Owning SCI03 §§3,5–8; SCI04 §§2–4,8; D1 §§5–8 | Finite ε/conditioning/tail/truncation и actual final неизвестны | сохранить |
| Shared caps не подменены суммой local maxima | P1 byte table; SCI07 D1+D2; D1:60–67 | Native capacity/counter/stop guards не доказаны | сохранить |
| Catalog source preparation доступна сейчас | Exact owner paths/leaves/conditional exclusions D1 §§2–4 | Implementation/test scope не добавлен самим review | изменить |
| SCI12-MAP уже I-ready | D1:102 требует exact operator/oracle freeze; §8:139 | Это следующий D-contract, не исполненный reducer | данных недостаточно |
| CP-SCI READY/physical/discretization acceptance получены | Missing plans/P0/A1/targets/bounds/native guards/admission | Source approval не numerical/native result | данных недостаточно |
| S1 способен дать useful sensitivity evidence | Frozen single-axis rows и held-out protocol | Sensitivity не гарантирует bound/experiment | дополнительно измерить |

STOP. Дополнительные source/implementation/runtime stages — по уже существующим разрешениям и их техническим predicates, без повторного human интервью и без fabrication unknown READY.
