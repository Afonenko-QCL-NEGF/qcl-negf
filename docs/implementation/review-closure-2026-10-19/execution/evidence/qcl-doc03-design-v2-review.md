# DOC03 D2 — focused independent CP-DESIGN recheck

**Вердикт: PASS для exact frozen D2 design.** R1/R2 закрыты на уровне проекта контракта; новых блокирующих замечаний в focused recheck нет. Это не acceptance реализации schema/Runner/AiiDA/Portal, не production known-origin capture, render/browser/native или научная приёмка.

## Exact inputs и выбранный source

| Артефакт | Проверенный SHA-256 |
| --- | --- |
| `/tmp/qcl-doc03-design-v2.md` — 70,041 bytes | `01bd504b382062ad896280e58dca4588e67f725e5deb72f350eae99c91aca625` |
| `/tmp/qcl-doc03-design-v2-identity.json` | `855fabbf01442e527304f4fc1a91a5ec49ccac1c6b12bdde9181fd6974818c9e` |
| `/tmp/qcl-doc03-design-v2-delta.json` | `8dcb31ec749898ee7149efe70c57f383b8937d1955c45839ce128170dc16024e` |
| Предыдущий independent review | `176f2b3e317bfabc4e0b7525e89738df02a64aa4006f8044cf307273ab8b1f53` |

D1 report/source identity/freeze/review independently остались равны четырём captured parent hashes. Root фактически `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`; gitlinks получены непосредственно через `git ls-tree <root> components/`. Для этого recheck selected Core f7b108bef206d2b2dc5afe0306b2dff60d27ac59, Runner 23860d9e660a3cddf6cb5203d449d1b62f3745a1, AiiDA d8f8092ca1c76523d85384b4bac8198d8bfa736b, Research 1eacefcd81a50e245ea9da74a0b717b33818c61e, Contracts 02a564b78dc9c5e19eacf496bc8c891361eafaab. Observed Core e86ac74…, Runner9378396… и Contracts12fc264… не подставлены вместо них.

Все 11 D2 primary witnesses independently совпали с selected Git objects по полным bytes/size/hash. Это 219,792 bytes; вместе с parent artifacts initial verification прочитал 313,792 bytes. В том числе повторно сверены Runner scientific execution/CLI/planning/configuration types, AiiDA calculation/workflow/parser/service, Core operating-point/types и Research YAML. Источники/дельта проверены до author conclusion; final claims §10 прочитаны последними.

## R1 — закрыт

**D2 locators:** `:260`, `:273–344`, `:369–377`, `:695–699`, `:710–714`.

Static input теперь содержит `reference_value_origin`, явно подписанный reference-only, с exact public parameter-set/selector/hash, сгенерированным Atom и authored applicability conditions. Actual `InputView` имеет отдельные declared/used `ValueOriginView`. Bound требует retained source-binding receipt последнего assigning source, exact value/context/phase и проверенный snapshot; numerical equality не является достаточным условием. Declared origin не наследуется used при unbound override.

Повторно разобран исходный counterexample: reference A=0.10 nm с publication, run B=0.15 nm без origin. В D2 reference origin A остаётся reference-only; actual B получает unknown/override_unbound. Равное B=0.10 nm с другой assignment либо иными T/composition тоже не получает автоматически origin A. Positive branch требует exact retained binding/context; удаление proof/condition переводит actual origin в unknown. Эти сценарии и healthy fixture теперь явно описаны.

Вывод сверяется с selected Research YAML и ограниченным assigning-source API Runner; это не просто переименование полей. Отдельно сохранена принципиальная граница: selected source не производит origin capture receipt; реальный DOC07 без такого входа возвращает actual value_origin unknown, `origin_bindings=[]`. Новый capture ingress не объявлен существующим, исторический receipt не реконструируется из filename/equality. Bound positive fixture синтетический и не выдаётся за production evidence. Unknown не блокирует exploratory solve.

**Решение R1:** сохранить D2 correction. Предыдущая возможность выдать reference provenance за provenance run override устранена спецификацией.

## R2 — закрыт

**D2 locators:** `:401–460`, `:462–547`, `:715–719`, `:734–737`.

Runner-local snapshot отделён от actor-enriched API context. Local context содержит frozen fingerprints/model revision, execution/point/allocated attempt и declared point configuration hash; AiiDA UUID/release/bundle identities в него не входят. Trusted selected-child actor добавляет run_uuid/calcjob_uuid/attempt. UUID из payload не принимаются. Нет нового UUID CLI input и нет выдуманного actor identity standalone Runner.

Snapshot placement теперь per-point/per-attempt:
`result/executions/<execution_id>/<point_id>/attempt-<attempt>/model-help-inputs.json`.
Это existing attempt subtree, который уже входит в selected CalcJob retrieve tuple. Закрытая запись immutable, no replace; payload/file/aggregate bounds и diagnostic при отказе заданы. Capture определён после actual point retarget/checkpoint restore/final runtime options перед solver invocation; listed dimensional mappings проверяемы по selected Core/Runner symbols. Derived/adaptive values после входа в solve этим снимком не удостоверяются.

Обязательный AiiDA owner diff теперь задан явно: optional parser index после inventory и до scientific early exits, bounded reads/schema/hash/context validation, separate invalid/missing/incomplete outcomes, detached index и raw retention. Новый read-only actor operation выбирает child один раз и затем использует explicit immutable attempt/UUID для plan/index/payload, повторно сверяет local context/hash и возвращает scalar projection. Это соответствует существующей `_export_child` selection authority; current deployment не подставляет release/source receipt старого execution.

Разобраны two-points/retry controls: P1/P2 имеют разные logical paths и hashes; запрос P2 не получает P1. Retry C2/attempt2 получает собственный P2 snapshot; imported completed P1 не получает fabricated attempt2 snapshot. P1/C2 возвращает `point_not_executed_by_selected_child`; исходный P1/C1 доступен по explicit original child. Invalid optional help остаётся used unknown и не меняет science exit/status. Index/retention/selection mapping теперь являются обязательной implementation частью, а не условным пожеланием.

**Primary selected locators:** Runner238 `src/composition/scientific_execution.jl::_scientific_attempt_directory`, point attempt allocation, restore/runtime-options/solve block; `src/application/scientific/planning.jl::_point_passport`; Coref7 `src/composition/operating_point.jl:26–87` и physical typed fields; AiiDAd8 `calculation.py:100–143`, `parser.py::QCLExecutionParser.parse`, `service.py:133–199`, `workflow.py::QCLExecutionRestartWorkChain` exposed outputs. Это source feasibility проверки; retrieval/parser/actor ещё не исполнялись.

**Решение R2:** сохранить D2 correction. Производитель local fields, point/attempt lifecycle и путь до trusted API consumer определены достаточно для owning implementation с последующим CP-CODE.

## Preserved remainder и границы

Sections 2, 3, 4, 6 и 7 D2 побайтово равны соответствующим D1 sections: source observations, минимальный Documenter/static hub, owner map, allowlist/tools/prerequisites, serving/offline/anchors не перепроектированы. Изменения §5/negative controls/handoff ограничены R1/R2 и необходимым типизированным input status.

Сохраняются: Documenter1.17.0/root Julia1.13.0 как lock facts; installed executable/version/assets/CSP проверки как DOC04 prerequisites; `/docs` до catch-all и явные docs404; version-local aliases, fixed light, local math/fonts/search; exact release/source binding без latest fallback; public output allowlist; preserved expert/optical reference и deferred quantitative gain; human/agent help scope по DOC01 без нового operator approval. Нет нового solver/model registry, universal resolver или научных правил в UI.

Обязательные пять negatives сохранены. Unknown-origin case расширен override/context controls; added two-points/retry/identity/missing/standalone controls проверяют прежние findings. Они записаны как будущие checks. D2 не называет их passing runtime tests.

## Limits и STOP

Один focused recheck, без children, чтение менее 2 MiB и без product imports/tests/build/render/browser/network/server/solver/Git mutations/source edits. Были две read-only команды `git show` с cwd другого component, вернувшие missing path; сразу перепроверены правильными selected repository/ref через subprocess. Их отказы не трактовались как отсутствующий selected source. Единственный reviewer writer output — этот файл.

PASS относится к exact D2 hash и разрешает следующий внутренний implementation checkpoint. Создание schemas/content/snapshot/index/actor adapter, реальные bounded tests, docs asset closure, native publication и scientific acceptance потребуют собственных evidence. Реального production known-origin proof D2 не создаёт; отсутствие retained receipt остаётся явным unknown.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 закрывает run override/context attribution | D2 ReferenceValueOrigin/ValueOriginView/receipt invariants и negative/positive controls | Actual capture receipt в selected source отсутствует | сохранить |
| R2 завершает local snapshot→retrieved index→selected actor contract | D2 §§5.3a–b и 11 exact selected witnesses; two-points/retry walkthrough | Реализация и controls ещё не исполнялись | сохранить |
| Минимальный route/owners/physics и прежние gates сохранены | Exact unchanged sections 2/3/4/6/7; focused delta | Не повторный полный source audit всех компонентов | сохранить |
| Native/browser/scientific acceptance установлена | Таких runtime artifacts нет | Source-only design recheck | данных недостаточно |

**STOP:** CP-DESIGN D2 PASS; дальнейшая owning implementation — координатор.
