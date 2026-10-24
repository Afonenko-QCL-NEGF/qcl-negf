# D report — DEV02 O08-03 final U/G assembly

Дата 2026-10-19. Статус: **reviewable design candidate, round 1**.
Автор не закрывает свой CP-DESIGN. Julia/import/build/solver/tests/install,
сервер, component edits и scientific execution: **0 / not_measured**.

Прочитаны applicable root AGENTS, architecture, handoff README,
autonomy, operator-permissions, DEV02/DEV05, SCI04 и
`.agents/skills/qcl-physics-audit/SKILL.md` с physics-checks. Использование
qcl-physics-audit сообщено координатору. Scope — исходники и независимая
скалярная арифметика Python standard library, 1CPU/2GiB. Права EXEC переданы
координатором; старое PLAN wording файлов не использовалось как новый запрет
или как источник более широкого execution grant.

## Deliverable и основное решение

`/tmp/qcl-final-ug-design.md` — полный candidate для независимого high review.
Никаких owning docs/code не изменено. Original dirty checkout защищён;
чтение шло в managed root
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.

Построен аналитический complete final-API fixture:

* checked carrier `Nz3/Nb1/:none`, six E/k blocks, channels off как явный
  функциональный предел; source/model S1 не меняется;
* target donor sheet D=1/64 (manufactured input, заранее выведен для Pauli
  capacity), φ²=`[1/4,1/2,1/4]`, `n=Dφ²`;
* literal cyclic L3 и `U*=lambda*D/36*[-1,2,-1]` дают ненулевую связанную
  Poisson/Dyson сборку;
* causal quadratic задаёт **все** Green blocks и actual same-state legacy
  `T± G T±†` self-energies; это не произвольный bath Σ carrier;
* raw/candidate/normalized chargeD и Pauli-valid lesser/greater; actual
  candidate сравнивается с independent literals;
* все problem/scba/candidate/solution/history поля имеют отдельное объяснение,
  метрики final report вычисляет `validate_solution`, zero-sentinel dict не
  используется;
* healthy designated fresh gates проходят математически; wrong-U и
  fixed-U/stale-G различаются при сохранённом **и fresh** rΣ≈0.

Числа из Python scalar derivation, **не Julia receipt**:

| Величина | Полученный algebraic ориентир |
| --- | --- |
| t,lambda | .0568654045716371;18.0951281797278 |
| projected u* | .00392689413622566 |
| U*max | .0157075765449026 E0 =.00157075765449026 eV |
| Aactive/f healthy |37.5340379643918 /.0657376939463092 |
| Aactive/f stale at Uold0 |55.7172917139956 /.0442842971072220 |
| wrong-U fresh Dyson |.0894656724575317 |
| stale-G fresh Dyson |.0901358790834612 |

Healthy global report намеренно **FAIL ровно по r_sum≈4.9737276762**;
он не становится scientific pass. N1/N2 сравнивают exact failed-key sets,
поэтому общий FAIL не маскирует отсутствующий alignment gate. Неизменяемые
default gates сохраняются. Derived error contract даёт короткие scalar
product/accumulation bounds и independent Poisson forward enclosure из
L3 eigenvalue3 на zero-mean subspace. Не используется эмпирическая правка
допуска после теста. Дальнейшая реализация и её outcomes пока не измерены.

Единственный существенный вопрос CP-DESIGN: принять ли именно **complete
functional aligned raw-map assembly** как scope DEV05, когда full global
report остаётся честно failed по заведомо неразрешённой spectral quadrature.
Карточка требует healthy designated fresh residual/gate; если reviewer
толкует её как обязательный all-gates global PASS, этот более сильный пункт
остаётся blocked. Candidate не понижает это требование молча.

## Identity и provenance чтения

Фактический root HEAD при старте:
`7d179b28647f0b89347d2d6358f08cf2fe479653`.
Root status: existing чужие modifications Runner/platform/portal и execution
checkpoint/evidence. Они не изменялись этим D packet.
`git submodule status --recursive` прочитан; selected Core HEAD чистый:
**`f5b73369a96d1225bd96fb34f5262c8dcf965f86`**. Core revision не обновлялась.
Current four accepted functional oracles/658 assertions учтены как ранее
принятые root evidence; в данном D task их runtime не повторялся.

Все SHA256 ниже — фактически прочитанные bytes именно Core f5b73369:

| Path относительно Core | SHA256 |
| --- | --- |
| src/domain/types.jl | f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b |
| src/domain/numerical_convergence.jl | 0a0bd0d1d84b54aac51dd534758240923b19cb701f17f213ac657a4bea2bf053 |
| src/numerics/reference/final_audit.jl | 8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673 |
| src/numerics/reference/validation.jl | 29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a |
| src/numerics/reference/poisson.jl | 8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645 |
| src/numerics/reference/basis.jl | 6f58663e6a3276744cd2d0b72edac103f42150b4588468efa4136f5f0685725e |
| src/numerics/reference/periodicity.jl | b7c3b7098ae1ed79492f6a84ddd1e55ba53e14fa703c264c2c4a8ff0f3864b35 |
| src/numerics/reference/greens.jl |25f476e3ac4f4c282433f55286ded0893994ac9bb1ce8c0ab17fe1c3b288f5b9 |
| src/numerics/reference/grids.jl |71c4cff98cbefb834eea818067549dc150cb0cd18141854f27dfbd549862d18e |
| src/numerics/reference/kernels.jl |ad3e5172d80eeaebab496d5e22a82b4db960a66e27ee4bcb3a234b987dbf055d |
| src/physics/observables.jl |b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f |
| src/numerics/optimized/production_solver.jl |ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa |
| src/numerics/optimized/certification.jl |de2dd971a8d466b53b0b2b4c682e085c743cd789b7e9e0c839f0a9042c5a13e3 |
| docs/src/development/review_oracle_contracts.md |673bc9641318b01ffe29bcbe6edc6198b5e243a0d246af8072a2190a70e072f2 |
| test/physics/nonzero_public_current_oracle.jl |17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01 |
| test/physics/nonneutral_periodic_poisson_assessment.jl |9aab7a4eea3a7fcb93033d2c9f6f3b420f6b1872843168e0deb98461f2602730 |
| test/numerics/fresh_candidate_residual.jl |8ab459b5be0c39f96839b862aad38e1dbcd6a8dc633770838fd239c8a871a6a0 |
| test/numerics/independent_nonlinear_and_continuum_anchors.jl |a6a826980fe13de96376383251329da4d3ff6e3225a5b8907b3dc83ed9cdeaec |

Ручного revision lock не создаётся: эта таблица — input reading receipt
для одного design candidate, состав root по-прежнему задают gitlinks.

## SCI04 reuse и ограничение независимости

Source trace включён в design: educational и production final paths
восстанавливают `published_U`, reconstruct final n из final Green и подают
fresh same-state map в final validation. Public audit source-positive,
runtime/serialization source lineage не измерена.

No-new-criterion disposition: текущий fixture — reusable literal U/G
distinction; production common kernels, selected cavity map, five-channel
map, serialized raw metadata, audit-error/process0 и alpha-scaled-step
controls остаются отдельными SCI04 dispositions. Соответствующие факты
переданы SCI03 D автору вместе с разницей единиц двух current floors.

Независимого reviewer внутри этого D task не запускали: все 4 concurrency
slots были заняты действующими root tasks. Следующий независимый CP-DESIGN
организует координатор на frozen candidate. Авторский арифметический
cross-check не выдан за независимую приёмку.

## Проверено и не проверено

Проверено чтением исходников и стандартной скалярной арифметикой: literal
quadratic branches и их support inventory, nonzero projected U, Poisson
sign/gauge/eigenvalue, target/raw-number measure, Pauli margins, wrong-U и
stale-G numeric margins, existing limits/API fields, full 38-base gate-key
inventory и code path final selection. Финальная file check подтвердила
18/18 исходных paths и SHA256, парность Markdown fences, завершающий newline
и отсутствие trailing whitespace в обоих outputs. Core остался чистым на
f5b73369. Design имеет 34,157 bytes; оба deliverables вместе менее128 KiB.

Не выполнялись Julia imports/runtime/tests, installation, SCBA/outer loops,
benchmarks, numerical environment setup, Nix/fullCI, server/native probes,
source mutations или source publication. Scientific acceptance отсутствует.
Следующий шаг — independent CP-DESIGN, затем отдельный owning writer;
не automatic design/solve loop. Max2 design rounds не превышен.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Полный literal final U/G oracle выведен | Design §§3–8; exact source/hash inventory | CP-DESIGN pending, manufactured rank1/channels-off/bulk scope | изменить |
| Small Σ больше не достаточен в контрольных inputs | N1/N2 exact rD margins; retained stored/fresh rΣ≈0 | Julia execution not_measured | дополнительно измерить |
| Healthy global report можно объявить pass | r_sum exact finite-grid defect≈4.9737 | Противоречит unchanged spectral gate | данных недостаточно |
| S1/physics/tolerances сохранены | Никаких owning component edits; separate fixture identity | Physical convergence/discretization/experiment отсутствуют | сохранить |
| SCI04 закрыт полностью | Same-source final-audit trace и new reusable functional contract | Production kernel/persistence/failure controls отдельно | данных недостаточно |
