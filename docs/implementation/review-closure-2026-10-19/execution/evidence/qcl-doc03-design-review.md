# DOC03 — независимый CP-DESIGN review

**Вердикт: CHANGES_REQUIRED.** Минимальный путь Documenter + static hub + bounded fragments, ownership и publication boundaries пригодны. До CP-DESIGN нужно закрыть два конкретных пробела exact contract: привязку происхождения численного значения к override данного run и полный Runner→AiiDA handoff нового snapshot. Это внутренние design corrections в уже принятом scope, нового вопроса пользователю не требуется.

## Immutable inputs и фактическая композиция

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, фактический HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`.

| Вход | Проверенный SHA-256 |
| --- | --- |
| `/tmp/qcl-doc03-design.md` — 50,004 bytes, 537 lines | `a25204b1883c97b5c3be1b2a26fb228e5efe8d4aa89230c938e34b56b903afcd` |
| `/tmp/qcl-doc03-source-identity.json` | `71900e472eeba5cd819207de6752e08ce2ea87bc3cb8f09c963ec9b09df1fecf` |
| `/tmp/qcl-doc03-design-freeze.json` | `a191903eca29e58092029e45ee1b6031d0dbae3b6d28e4b3ab935bdda0096f42` |

Все 61 source witness независимо сверены через `git show <revision>:<path>`: точные hashes/sizes совпали, прочитано 846,485 source bytes. Derived gitlink map совпал с `git ls-tree HEAD components/`. Selected Core — f7b108bef206d2b2dc5afe0306b2dff60d27ac59; Runner — 23860d9e660a3cddf6cb5203d449d1b62f3745a1; Contracts — 02a564b78dc9c5e19eacf496bc8c891361eafaab; Research — 1eacefcd81a50e245ea9da74a0b717b33818c61e; Portal — 2622de5ee28b454ff4f809cc3dd00c1e5bc2295d; Platform — b067723c82382689bff5cc366981c56e99b926f8; AiiDA — d8f8092ca1c76523d85384b4bac8198d8bfa736b.

Фактический recursive status: Core +e86ac74c4fe04a8999b889970c5a9f3c65575694 и Runner +9378396a3681c1eddf2c62f16674834fc4465583; остальные совпадают с gitlinks. Root dirty: эти component pointers, checkpoint/census, runbook и execution evidence. Не приняты ни за DOC03 изменения, ни за selected composition. Различие observed Core candidate в датированном author record и сегодняшнего working HEAD не подменяет immutable witnesses.

Прочитаны DOC03 handoff, architecture/AGENTS, physics-documentation, соответствующие requirements/DOC01 dispositions и release roadmap; затем primary source и frozen design. Author self-check/final claims рассмотрены после независимой проверки. Применён qcl-physics-audit для границы meaning/value/assigning/used evidence. Новых агентов не было.

## R1 / P1 — value origin привязан к static reference, но не к числу этого run

**Locators:** design `:145`, `:156`, `:230`, `:260–283`, `:306–320`, `:347–350`, `:466–468`.

Static fragment содержит `inputs[{path,schema_source,facts,value_origin}]`; value annotation относится к выбранному public reference parameter-set YAML. Run `InputView` имеет **ровно** `{path,declared,used,assigning,effective_origin}` и не содержит ни run-specific value origin, ни привязки статической value-origin annotation к конкретному parameter-set value/selector. Сам static JSON запрещено переписывать в API (`:262`). Graph equality устанавливает версию исходников, но не доказывает, что run не переопределил число.

**Воспроизводимый design counterexample, synthetic:** в одном graph reference Δ=0.10 nm имеет подтверждённый табличный источник; другой frozen plan этого же graph явно задаёт Δ=0.15 nm без физического источника. Fragment ID/schema path/source graph остаются теми же. Dynamic response может корректно показать used=0.15 nm и файл назначения, но единственное структурированное `value_origin` остаётся static known publication для 0.10 nm. Нет поля или правила, которое связывает origin с reference value и выдаёт unknown для override. Сходный риск возникает при иных T/composition/fit conditions даже при равном числе. Обозначение назначения отдельно не исправляет атрибуцию научного источника.

**Primary source:** Research 1eacefc `config/model/reference-2019-70k.yaml:70–76` задаёт конкретные screening/IFR значения; Runner 238 `src/application/scientific/planning.jl::_point_resolved_raw` применяет point axes, `scientific_plan_dict` хранит resolved configuration и assignment history; `src/application/configuration_types.jl:209–232` явно ограничивает `configuration_source` assigning provenance. Root `docs/system/physics-documentation.md`, «Три разных происхождения», требует источник конкретного числа и условия, а не только source файла. Это не обвинение существующих чисел в неверности, а неполнота предлагаемого transport contract для объяснения overrides.

**Минимальная correction:** оставить authored reference origin в Core/Research, но структурированно связать его с public parameter-set locator/selector/условиями. Run projection должен либо вернуть отдельный bound `value_origin` с evidence для фактически declared/used значения, либо явно вернуть unknown/not-bound и подписать static reference origin как reference-only. Не выводить applicability origin только из равенства чисел. Добавить negative/positive pair: известный origin reference A + explicit unknown override B → неизвестный origin B; exact documented value/context с retained binding → known. Это не требует поиска всех DOI и не блокирует exploratory solve.

**Решение:** изменить design до CP-DESIGN. Иначе UI/agent может получить выдуманное происхождение run-specific значения при формально правильном release binding.

## R2 / P2 — snapshot не имеет полного производящего и транспортного контракта

**Locators:** design `:240–260`, `:294–331`, особенно `:295–300`, `:306–318`; handoff `:499–509`.

Выбран один output `result/model_help_inputs.json` с top-level `context` «как выше». Этот context требует `run_uuid`, execution/point и metadata AiiDA selection. При этом producer указан Runner persistence, снимающий actual solver arguments. Не определён input, из которого standalone Runner получает actor-owned run UUID, и отсутствует правило trusted actor enrichment. Нельзя подставить arbitrary UUID или plan fingerprint. Nullable разрешён только для attempt/calcjob/configuration hash, а не для run UUID.

Есть также незавершённый lifecycle того же output:

1. Одна scientific execution содержит несколько sequential points и attempts; snapshot имеет один point/attempt context и один фиксированный filename. Не указаны per-point retention/collection и правило предотвращения overwrite предыдущей точки.
2. Selected AiiDA retrieve contract не получает этот новый root-result файл. Заявленного «existing bounded artifact read path» недостаточно, пока file не включён в retrieved closure и не сохранена связь с выбранным child/point/attempt. В handoff AiiDA projection описан условно, хотя для выбранного filename изменение retrieval обязательно.

**Primary reproducible locators:** Runner 238 `src/composition/scientific_execution.jl:436–456` принимает plan/output/execution_id/attempt и перечисленные recovery/telemetry kwargs — AiiDA UUID context отсутствует; `src/cli.jl` run-plan dispatcher не принимает его. AiiDA d8f8092 `src/aiida_qcl_negf/calculation.py:100–101` передаёт execution/attempt, `:140–143` retrieve list содержит series/scientific_plan/pause/retrieval-manifest/archive/recovery/executions, но не model_help_inputs.json; `service.py::_select_child`, `get_artifact_metadata`, `open_artifact` владеют actor selection и читают только retrieved repository. `planning.jl:scientific_plan_dict` перечисляет multiple points внутри execution.

Дополнительные read-only source hashes вне исходных 61 witnesses:

| Selected source | SHA-256 |
| --- | --- |
| AiiDA d8f8092 `src/aiida_qcl_negf/calculation.py` | `677eccfcf211b24230d8cb912955d2ec80a508d2d31d4e60d81cfbd2db1a156c` |
| AiiDA d8f8092 `src/aiida_qcl_negf/workflow.py` | `ae5d71d06d92369a1848770fdfdabde82cdbb9dca10756ddebc47dcf8fe159fc` |
| Runner 238 `src/composition/scientific_execution.jl` | `55a3737a35b21867d91992a2a3a7807729a3b9d83b0931006d99dc82addbf9cd` |
| Runner 238 `src/cli.jl` | `aa5e129312707a7927e1bc97caf4c830c7cf9ed29cf12c648f8afbd7fbcf2cd0` |

**Минимальная correction:** определить Runner-local snapshot context отдельно от actor-enriched API view; API добавляет run/calcjob identity из trusted selected child, сверяя local plan/execution/point/attempt. Либо явно описать новый bounded identity input и владельца его выдачи. Затем зафиксировать per-point/per-attempt logical snapshot placement или bounded collection, retrieval/parser inventory inclusion, retention и read-selection mapping. Не менять scientific fingerprints/старые artifacts. Добавить control с двумя points и retry: оба нужных snapshot доступны с собственными identities; standalone producer не придумывает AiiDA UUID; отсутствие snapshot даёт только unknown used/help status.

Это замечание не требует наличия новой реализации уже сейчас. Оно требует закончить **проект** exact produced/consumed fields и их передачи, чтобы implementer не принимал новое interface решение после freeze.

**Решение:** изменить design до CP-DESIGN.

## Что сохраняется без нового operator decision

| Аспект | Проверка | Вывод |
| --- | --- | --- |
| Scope human/agent help и минимальный UI | DOC01 C11/C12/R11 implement; D10 conditional; существующий plan submit UI | Включение уже принято; field configurator/новый DSL не требуются. |
| Owning facts | Core/Runner signatures/units/effects; Contracts schema constraints; Core meaning; Research numeric origins; Runner effective projection | Разделение разумно. R1/R2 исправляют связь между фактами, не переносят физику в Portal. |
| Preserved Documenter | Selected make.jl используют Documenter, prettyurls=false, doctest=true/checkdocs exports; root CI передаёт workspace project | Hub + per-section search минимален; global search adapter обоснованно deferred. |
| Generator/pins | Manifest Julia1.13.0/Documenter1.17.0 UUID/tree сверены; installed tools/local assets/CSP compatibility явно prereqs | Design не выдаёт manifest за executable/native receipt; latest imports/build не делались. |
| Bundle identity/allowlist | Exact graph binding, external SHA256 manifest receipt, source/public path restrictions, bounded plain-text fragments, unsupported formats incompatible | Нет ручного source lock, нового model registry или scientific ledger. |
| `/docs`/anchors/offline | Selected Portal mount `/` расположен последним; Platform proxy `/`; design требует `/docs` раньше catch-all, version-local aliases, local assets | Архитектурно согласовано; cold-cache/light/search/math/404 остаются будущими controls. |
| Scientific boundaries | Unknown не ноль/pass; planned не used; DOC04 imports отдельно; no solver in build/view; expert optics retained/deferred | Допуски/модель/acceptance не ослабляются. |

Пять требуемых negatives описаны в `design:478–484`: wrong release, missing source, private path, unknown origin, catch-all. Их ожидаемые outcomes в целом корректны, но unknown-origin control следует расширить R1 override/context случаем, а dynamic handoff — R2 multiple-point/retry control. Ни один negative здесь не исполнялся.

## Limits, evidence и STOP

Scope — один bounded source/design review, ≤30 min, 1 CPU/2 GiB; чтение менее 4 MiB. Проверялись exact UTF-8/hashes/source objects и семантика contract; не запускались imports, tests, builds/render, browser/server/network, solver, profiling или массивы. Были read-only попытки старых путей `qcl_negf_portal`/nested calculations, вернувшие missing path; затем использованы реальные `qcl_negf_api` и flat `calculation.py`. Не считать missing-path команды source evidence.

Никаких source edits/Git mutations; единственный writer output — этот review. Status и execution source могут меняться координатором параллельно; вывод привязан к exact frozen hashes, а не к latest checkout. Новое CP-DESIGN не закрыто до focused correction и независимого recheck; научная или native acceptance этим review не устанавливается.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Минимальный docs route сохраняет архитектуру и accepted scope | Selected source witnesses, DOC01/DOC03, design §§3–4/6–8 | Serving/assets/runtime не измерены | сохранить |
| Exact run-specific value origin безопасен при overrides | R1 counterexample и поля §5 | Static Origin не bound к числу/условиям run | изменить |
| Snapshot producer/consumer handoff завершён | R2 поля и selected Runner/AiiDA paths | UUID producer, point retention и retrieval не определены полностью | изменить |
| Offline/light/direct anchors работают | Только proposed controls и source route order | Нет render/browser/native receipt | дополнительно измерить |
| Release/native/scientific acceptance установлена | Таких проверок нет | Source design не scientific evidence | данных недостаточно |

**STOP после отчёта.** Передать координатору R1/R2 для focused D correction; product implementation не начинать по этому freeze.
