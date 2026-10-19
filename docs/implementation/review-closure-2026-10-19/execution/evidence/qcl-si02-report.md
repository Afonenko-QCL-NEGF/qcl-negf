# SI02 · authoring receipt · 2026-10-19

Статус: **candidate_for_CP-CODE**, independent CP-CODE ещё не выполнен. Evidence
level: **source/static docs**. Это не observed agent behavior, runtime, cluster
или scientific acceptance. Публикация, stage и commit не выполнялись.

## Immutable candidate / authority

Worktree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, branch
`codex/review-closure-exec`; исходный root HEAD
`e0f244d075dd49874ba4f3847f4efa693f3b3622`. Единственный изменённый этой задачей
product path — `docs/system/agent-review-workflow.md` (79 additions, 25 deletions).
Чужие staged DOC01/checkpoint/Core gitlink не менялись командами этого автора;
никакие stage/commit/reset команды не выполнялись. AGENTS/skills/code не правились.

- Принятый CP-DESIGN: `/tmp/qcl-si02-design.md`, SHA256
  `485ce6e8ef14bc9fb5ed33f317de046679e4fc9f3d977ef7436b7f6bc8c81057`.
- Independent design review: `/tmp/qcl-si02-review.md`, SHA256
  `1493519cd5ccbd9f1d7d97f574719987f5106e890cd9276fb13ca36891926eca`;
  CP-DESIGN PASS, Q01 учтён разделением coverage denominator и общего checklist.
- Исходный owner file SHA256:
  `c018491d66c286604b3b389c63b6beeced36be759dcc5353470486aaa2793ae0`.
- Финальный owner file и `/tmp/qcl-si02-workflow.candidate.md` SHA256:
  `63ef521b538eadebb83b5835de3588d09f763b68d11431e9f6704ff7f5e36f1c`.
- Review diff `/tmp/qcl-si02-review.diff`, SHA256
  `b47940597639f56658cef6f8bfdd9666ab38b715604aab58551c7c59f913f8eb`.

Точная активация/grant переданы координатором от человека: EXEC+B/G1/S1 и
последующее разрешение использовать доступные development/deployment ресурсы и
необходимые checks без per-test resource questions. Exact human message locator
остаётся у координатора; historical standby-файл сам по себе EXEC не активирует.
Следуя последнему coordinator brief, budget paragraph отличается от accepted
proposal одной локальной адаптацией: не копирует dated P1 как новый фиксированный
test cap, а берёт конкретные пределы из последнего применимого user grant.
Finite packet accounting, remaining envelope, scientific caps, protected reserves
и CI-once прямо сохранены (:143–155). Согласованные scientific 13/936/byte caps
не заменяются общим разрешением engineering resources.

## Что изменено

Все locators ниже относительно frozen candidate
`docs/system/agent-review-workflow.md` с указанным SHA256.

- :64–96 — единственный canonical contract, ровно existing nine row names;
  denominator, evidence level, healthy/negative/near-zero cases и local unknown.
- :130–155 — immutable input/candidate handoff, raw originals без author diagnosis,
  finite shared envelope и честное завершение отрицательного read-only вопроса.
- :168–200 — already-authorized scope survives resume, latest user intent выше
  dated PLAN/P1; CP-OPS/SCI остаются technical BIND/READY внутри policy, exceptions
  человеку; timeout требует reconciliation перед повтором remote action.
- :188–191 — явные guards fresh admission, four-role/nginx preflight,
  backup/restore, old S01/foreign, fixed light и единственный final full CI.

Исторический introduction и четыре карточки не переписаны. Новый §READY прямо
ограничивает их датированным review; source refs и old statuses остаются history.
Новый registry/service/template в skills/AGENTS не создавался.

## Фактически выполненные docs-only checks

1. Source recheck: исходный owner file и accepted design hashes совпали с
   CP-DESIGN packet; перед правкой `git diff -- owner-file` был пуст.
2. Прочитан весь `git diff -- docs/system/agent-review-workflow.md`.
3. `git diff --check -- docs/system/agent-review-workflow.md` — exit 0, output пуст.
4. `awk` счётчик строк первой `| Поле |` таблицы — `contract_rows=9`;
   row names сохранены по исходному diff/read.
5. New relative Markdown targets проверены `ls -l`: P1, `../../AGENTS.md` и
   `../single-server-deployment.md` существуют относительно owner file.
   Новые anchors не вводились. Не заявляется crawl существующих external URLs.
6. `git diff --cached --numstat -- owner-file AGENTS.md .agents/skills` — output
   пуст; unstaged scope view содержит только owner file `79 25`.
7. Historical suffix от «Четыре READY-карточки для чтения» до EOF сравнен
   с `git show HEAD:owner-file` через `cmp` — exit 0. Оба suffix SHA256:
   `22f3ea9347194fe509c8adfc06263bd0d098826f7eb855c9aa966f80d1c88b34`.
8. Final owner file и frozen `/tmp` candidate сверены byte-for-byte.

Проверки выше — чтение, формат и filesystem path existence. Tests/imports,
validator/agent samples, scientific environment, build, browser, server и solver
не выполнялись. Никакие новые SSH/probes/remote side effects не вызывались.

## Coverage denominator: 13 items

**Denominator именно 9 K-properties + 4 requested route cases = 13**. Это не число
строк таблицы сверх её девяти полей и не denominator всех project invariants.
Ниже отдельная disposition каждого item; общий preservation checklist следует
следом и в 13 не включён. Все dispositions — **source/static reading**; 0 observed
behavior samples, 0 reproduced remote outcomes. Авторский receipt не заменяет
independent CP-CODE.

| Item | Static disposition и locator | Ограничение |
| --- | --- | --- |
| K01 goal/property | Одно проверяемое поведение, Task/requirement IDs, owner/roles :76 | Не весь requirement ledger |
| K02 immutable inputs | Source/data refs/hash и candidate/runtime/publication :77; frozen bytes :130–135 | Artifacts задач не исполнялись |
| K03 paths/actions | Already-authorized stage/actions/grants и один writer :78; READY не выдаёт grant | Tool policy остаётся обязательной |
| K04 oracle | Denominator/evidence level, healthy positive/negative/near-zero, units/weights/basis :80; evidence separation :91–96 | Численные thresholds принадлежат owner, не введены |
| K05 budget/stop | Shared finite attempts/cycles/resources :83, :143–155, unchanged detailed envelope :202–209 | Resource admission фактически не измерялся |
| K06 output | Hash/diff, original evidence/failed receipts, disposition/residual :84 | Сам receipt не physics pass |
| K07 writer/handoff | Один writer/отдельный reviewer :76/78; first reviewer raw originals без diagnosis :130–138 | CP-CODE ещё нужен на этих bytes |
| K08 local unknown | Missing blocks dependents :82, :86–102, :173–175; independent READY продолжается | Missing raw не получены |
| K09 finite loop/resume | Finite cycles и no-until-green :140–155; current grants/remaining envelope/IDs/reconciliation :168–200 | Remote loop не наблюдался |
| A authorized check | Unchanged granted action не требует нового human approval :168–175; непорученное не получает grant :78/173 | Check scenario только static, command не запускался |
| D docs-only | :81 позволяет static protocol без numeric environment; выход/приёмка ограничены source level :91–96 | Numerical/build acceptance не заявлена |
| M missing raw | Inventory может быть READY, FDR требует matrices/identity :86–96; missing только dependent :174–175 | Raw/FDR verdict отсутствует |
| U unknown remote outcome | Сначала reconciliation persisted IDs; timeout не terminal и не duplicate :193–200 | Никакого remote timeout не воспроизводили |

Healthy controls для четырёх cases из design сохранены как static questions:
разрешённый unchanged action продолжает route; docs finding завершается без
Julia; доступный inventory завершается при missing dependent matrices; verified
terminal receipt позволяет только следующий разрешённый шаг. Соответствующие
negative clauses запрещают непорученный check, docs→full suite/science promotion,
missing→zero/pass и timeout→duplicate. Это анализ clauses, не observed controls.

## Общий preservation checklist, вне coverage denominator 13

| Invariant/check | Evidence / static disposition | Граница |
| --- | --- | --- |
| Единственная reusable contract form | :64–72; unchanged no-registry :124–128; ровно9 rows | Handoff остаётся конкретным binding, не новый mandatory registry |
| Current user authority выше historical PLAN/P1 | :66–69, :145–151, :168–175 | Historical bytes сохранены |
| Physics/model/grid/basis/tolerance не ослаблены | Unchanged invariant row :79; evidence separation :91–96; owner source boundaries unchanged | Solver/model не исследовались этой docs задачей |
| S1 caps/без e–e не расширены | :150 scientific caps unchanged; active B/G1/S1 link :177–185; P1 contents не менялись | 13/936/bytes и e–e=none принадлежат научному grant, не скопированы как новая authority |
| Finite shared accounting | :83, :143–155, :202–209 | All-agent budget не умножается |
| Fresh admission/preflight preserved | :187–190; required four-role/nginx, runbook link; unchanged detailed envelope | Admission не измерялся и не считается fresh по старому receipt |
| CP-OPS/SCI technical BIND/READY; exceptions human | :177–185; :199–200 | Approved predicates обязательны; grant сам не доказывает readiness |
| Protected old S01/foreign | :183–190 | Чужие/старые jobs не отменялись |
| Backup/raw/provenance preservation | :130–133, :152–153, :187–190 | Source arrays не трогались |
| CI-once | Unchanged :163–164 и explicit :191 | CI не запускался, rerun не разрешён |
| Fixed light web | :190, unchanged AGENTS authority | UI код/браузер не менялись |
| Links/format/nine row names | Actual checks 3–5 и diff above | External pages/old anchors не crawling |
| Historical карточки unchanged | `cmp` и equal suffix SHA256 | Не переаттестует их старые facts |

## Resume / next checkpoint

Потребление этого SI02 authoring packet: одна docs редакция и один основной
source/format/link review pass; ноль imports/tests/build/server/solve/behavior
samples, никаких remote operation IDs и unknown outcomes. Дополнительная ресурсная
волна не требуется. Source recheck и final hashes выше позволяют reviewer
заморозить exact candidate; изменение bytes потребует нового hash и локальной
инвалидации dependent checks.

Next: independent CP-CODE на `/tmp/qcl-si02-review.diff` + original workflow
bytes из root HEAD + frozen candidate SHA256, с 13-item table и отдельным
preservation checklist. Reviewer сначала получает original question/inputs;
author receipt служит evidence и не задаёт expected verdict. После него commit/
publish остаются координатору по active grant; автор их не выполняет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Canonical nine-field contract и autonomy route уточнены | Frozen candidate hash, diff, :64–209 и13 static dispositions | Independent CP-CODE pending | изменить |
| Формат, новые paths и historical suffix проверены | Exit0 checks,9rows, existing targets, equal suffix hashes | Не runtime/behavior/science | сохранить |
| Grants сохраняются без per-test approval | :143–155, :168–200; latest coordinator authority | Fresh admission/BIND/exceptions обязательны | сохранить |
| Реальное autonomous behavior доказано | Только static clauses,0samples/remote observations | Behavioral evidence отсутствует | данных недостаточно |
