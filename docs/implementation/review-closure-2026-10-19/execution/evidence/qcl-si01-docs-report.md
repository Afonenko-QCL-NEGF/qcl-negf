# SI01 — authored authority/epoch docs, frozen candidate

Дата: 2026-10-19. Этап: порученное docs-only исполнение SI01; authored D.
Независимое CP-CODE этим автором не закрывается. После freeze работа остановлена
для отдельного high review. Один author round, corrective rounds0; cap2 не исчерпан.

## Source identity и owned paths

Managed worktree `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
branch `codex/review-closure-exec`. Initial/final root
`9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`.
Выполнены `git rev-parse HEAD`, `git status --short`,
`git submodule status --recursive` и `git ls-tree HEAD components/`.
Восемь checked-out revisions совпали с root gitlinks. В status были чужие
Core/AiiDA/Platform/Research overlays и execution/checkpoint/evidence files;
они не входят в SI01 и не менялись автором.
Исходный checkout `/home/tolya/Загрузки/qcl-negf` не использовался для записи.

Ровно два owning изменённых Markdown paths:
- `docs/system/agent-review-workflow.md`
- `docs/system/skills-and-instructions-review.md`

В Git не выполнялись mutations, commit/push/PR; component code/deps/locks,
AGENTS, skills/references и historical archive не менялись. Native I/O двух
owned docs выполнено один раз после проверки равенства pre-write baseline,
через разрешённый scoped escalation managed worktree. Это не серверная операция.

## Frozen bytes

- Patch `/tmp/qcl-si01-docs.patch`, SHA256 `b0dc81bf31f98edee977088831dd9659af1359cc4086233beb2355a36eba2ac6`.
- Exact candidate files `/tmp/qcl-si01-candidate/`; baseline files
  `/tmp/qcl-si01-baseline/`.
- `/tmp/qcl-si01-source.json`: base/final root, Git-derived gitlinks,
  per-file original/candidate SHA256, hashes16 primary reading inputs и
  native bytes equality. Это receipt чтения, не maintained revision lock.
- `/tmp/qcl-si01-check.py` и `/tmp/qcl-si01-check.json`: source/text checker
  и фактический bounded result. Продуктовые modules не импортировались.

Candidate SHA256:

| Path | SHA256 |
| --- | --- |
| `agent-review-workflow.md` | `8a00d94c2306ffb391887f8e6eaa6d7c6ebc82c55461e5135891147619647dfc` |
| `skills-and-instructions-review.md` | `a683b0b9b34de7a83736db15eb3864d93e387a30f80b682671a618040067e38d` |

## Claim × primary locator × epoch

Все current paths ниже прочитаны на root9f8, кроме явно historical source.
Direct current EXEC/resource instruction передан координатором в task scope;
checkpoint не выдаётся за primary user transcript. P1 сохраняет фактические
ответы B/G1/S1, а не восстановленный primary provenance59 прежних требований.

| Claim | Primary locator | Epoch / граница вывода | Disposition |
| --- | --- | --- | --- |
| C01 source composition | AGENTS «Начало задачи» п.2; architecture «Source composition»; actual Git tree | Current invariant; старые8SHAs — audit2026-10-14 source-receipt.commands | сохранить; не второй lock |
| C02 implementation/target/history/publication | architecture introduction; DOC01 appendix «Источники и epoch»/«Семантика ledger»; RV17 SI01; PORTABILITY «Карта путей» | Current source требует property locator; RV17/public-byte routes — historical2026-10-14; fresh external publication unknown | уточнить epoch; `unpublished` не выводится из отсутствия свежей проверки |
| C03 effort/scope | release-roadmap «Политика ролей и координации» | Current policy; harness actual не измерен SI01 | сохранить, не compute grant |
| C04 actions/authorization | P1 «Как устроено условное разрешение», PERM01–18; current user assignment; canonical workflow permissions | EXEC2026-10-19 сильнее PLAN; BIND/READY и CP-EXCEPTION сохранены | выполнять ready inside scope без повторного approval; missing blocks dependents |
| C05 owners | AGENTS «Владение компонентами»; architecture «Package review»/«Scientific execution» | Current boundary, не implementation каждого API | сохранить |
| C06 independent acceptance | AGENTS «Физическая и численная добросовестность»; architecture «Verification boundaries» | Current invariant; source/static/metadata/runtime/science различаются | hash/exit/schema/render не scientific truth/pass |
| C07 fixed light / CI | AGENTS «Светлая тема…» и «На этом bootstrap»; P1 PERM18; workflow rounds | Current all-web light; named bootstrap/currentB single final fullCI; targeted repeat conditional | сохранить, без universal запрета relevant targeted check |

Original fixcard:
`docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/fixes/RV17-SI01-claims.md`.
Original catalogue/claims: `RV17.md`, §SI01, C01–C07.
SI02 fixcard и published canonical contract использованы как неизменяемые inputs.
DOC01 report/review прочитаны; 59-ID ledger не пересоставлялся.

Конкретная неверная универсальная формулировка: old skills-review сообщал, что
содержимое temporary snapshot не публикуется и недоступно опубликованному читателю.
PORTABILITY теперь описывает public original reports и mapping frozen roots.
Замена сохраняет точный gap: original frozen sys/README, private/native и raw
inputs не восстановлены. Старые source hashes, gitlinks, public-byte claims,
proposals и tabletop observations не удалены; их epoch обозначена явно.

AGENTS exact false claim, требующий SI01 правки, не продемонстрирован. Поэтому
AGENTS оставлен read-only; routing/contribution предложения остаются SI03.
Skills/references остаются SI04/05. SCI03 criterion bounds и DOC03/07 source/help
interfaces SI01 не определяет; runtime/scientific implications здесь unknown.
Новых требований либо competing task/authority registry нет.

## Реально выполненная проверка

| Check | Outcome | Ограничение |
| --- | --- | --- |
| `git apply --check --whitespace=error /tmp/qcl-si01-docs.patch` до I/O | exit0 | Applicability/added whitespace |
| Stdlib `python3 /tmp/qcl-si01-check.py` до и после I/O | exit0 | Candidate text checks; native equality проверена отдельно SHA256 |
| Canonical contract preservation | 9 fields, entire independent-rounds block и entire permissions/gates block byte-identical baseline | SI02 forward behavior не проверялось |
| C01–C07 denominator | 7 explicit rows, 5 declared columns each | Count не semantic proof |
| Local links/anchors | 46 checked, missing0 | External destinations не reverified, browser/render отсутствуют |
| Protected root equality | AGENTS + requirements + DOC01 appendix +12 skills/reference/UI files:15 unchanged against9f8 | Component overlays чужие и не принимаются этим выводом |
| Format | Final newline, no trailing whitespace, balanced fenced blocks | Markdown source only |
| `git diff --check --` two paths | exit0 | Scoped new authored diff |
| Reverse-apply check frozen patch после I/O | exit0 | Не разрешение повторного применения |
| Native bytes == frozen candidate | 2/2 exact SHA256 equality | Не runtime evidence |

Diff: 2 files,82 insertions31 deletions. Full authored patch прочитан.
Никакого product import, env setup/install, build/docs build, test suite, CI,
network, server/profiling/solver/new SCBA/Poisson не запускалось.
Архив148 повторно целиком не hash-проверялся; его publication receipt/PORTABILITY
прочитаны как limited historical evidence. Archive hash verified не scientific truth.

## Envelope и residual

Назначенный envelope45min/1CPU/2GiB/read-text/output128KiB, max2 author rounds.
Выполнен1 author round, две scoped text проверочные стадии по изменённым bytes.
CPU/RAM peak и полный объём transcript extracts не инструментировались и не
выдаются за измеренный performance/budget pass; ранние объединённые чтения
давали truncation, после чего чтение сужено до sections. Frozen deliverables
patch/report/check/source — малые text artifacts; их размеры записаны отдельно.
Никакого costly/runtime этапа и создания scientific arrays нет.

Следующий шаг: независимый high reviewer получает тот же source9f8, исходный
вопрос C01–C07 и primary materials, frozen patch/hash без готового диагноза.
Author report допустим после первого самостоятельного source pass. Не менять
candidate bytes до фиксации finding; коррекция создаст новый hash/round.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SI01 claims имеют authority/epoch/owner/primary/limits | 7-row matrix и frozen source/patch hashes | Semantic independent review ожидается | сохранить |
| Canonical SI02 и gates не потеряны | Побайтовое сравнение contract/rounds/permissions, unchanged15 protected files | Это source preservation, не forward pass | сохранить |
| Historical sources и publication claims остаются current truth | Explicit epoch; source-receipt/PORTABILITY/DOC01 comparison | Fresh public verification/runtime/science отсутствуют | изменить |
| Docs/static проверка доказывает научную приёмку | Только scoped link/format/source evidence | Нет native/SCBA/Poisson/raw acceptance | данных недостаточно |
