# DOC04 — SourceGraph seam и identity вокруг одного вызова

Предлагаемый следующий I-ticket: добавить runner injection в существующий
`ops/git.ts::sourceGraph`, связать его с ограниченным docs transport и дать
чистый контроль identity до/после одного injected вызова. BUILD остаётся blocked.
Это один ограниченный контракт, готовый для независимого source review;
его реализация и исполнение controls здесь не выполнены.

## Исходники и граница

Actual Root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
HEAD `107bac5697b37cf0e47c3feb44883a907837645c`; selected Core
`9f4a96d032ad868ec010ce92d915bb81087c8d92`, Runner
`4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`, Results
`de70638a982f91b7e125ab1cfc70a2daef2a656d`. Results c00 не selected.
Есть чужие текущие изменения checkpoint и четыре untracked evidence/identity/
publication files; они не редактировались. Точные пути — companion identity.

Recipe overlay: `/tmp/qcl-doc04-root-recipe-worktree`, HEAD
`b07974b8e46bf8afdf1740947b842669a62a5ccc`; три untracked пути
`ops/docs.ts`, `docs/public/make.jl`, `tests/docs_recipe_orchestration_test.ts`.
Его Runner gitlink всё ещё `fefaa27f194bfddf85dd51a0e255beef2218c06d`,
submodules не инициализированы. Не выдавать overlay за actual selected Root.
`ops/git.ts` и `ops/process.ts` в обеих базах совпадают по SHA256.
Общий I-Root PARTIAL / NOT_READY, R1/R2 CLOSED_SOURCE по v2 review.

Наблюдаемые owning API:

- `ops/git.ts:2–12`: `Component {path,revision,url}` и
  `SourceGraph {format:"qcl-negf.git-graph.v1",revision,components}`.
- `sourceGraph(root=workspace, requireClean=true): Promise<SourceGraph>`
  проверяет Root HEAD/clean, `.gitmodules`, committed gitlinks, public HTTPS URL,
  child HEAD/clean, отсутствие nested gitlinks и orphan sections.
- `git(root,args)` вызывает `process.run(...,true)`; последний использует
  `Deno.Command.output()` и buffered stdout. Его нельзя вызвать из docs path.
- Overlay `ops/docs.ts:317–338` хранит `sources:null`; production graph transport
  отсутствует. `runFinite` уже имеет capped streams/deadline и честный
  acknowledged/unknown-partial result, но не production spawn/sink binding.

## 1. Additive owning seam

Разрешённые source paths следующего I-ticket: `ops/git.ts`, `ops/docs.ts`,
`tests/git_test.ts`, `tests/docs_recipe_orchestration_test.ts`. `ops/process.ts`
и owning Core/Runner profiles не менять. Unchanged operator recipe сохранить.

```ts
// ops/git.ts — новые type и третий необязательный параметр.
export type GitRunner = (root: string, args: string[]) => Promise<string>;
export async function sourceGraph(
  root = workspace,
  requireClean = true,
  runGit: GitRunner = git,
): Promise<SourceGraph>;
```

Внутри `sourceGraph` **каждый** прежний `git(...)` заменить на `runGit(...)`;
argv и все проверки сохранить. Старые callers сохраняют прежнюю семантику;
docs всегда передаёт свой runner явно и только `requireClean=true`.
Не дублировать SourceGraph builder в `docs.ts`, не добавлять caller
`sourceClean`, `gitlinksMatch`, `sourceReady` или аналогичные booleans.

`gitlinks:24` сейчас сортирует через `localeCompare`. Заменить только comparator
на `a.path < b.path ? -1 : a.path > b.path ? 1 : 0`. Имена разрешены ASCII;
это даёт стабильный порядок code units независимо от locale, совпадающий
с лексикографическим порядком ASCII в Python. Формат графа и исходные URL
сохраняются. Для duplicate gitlink records — явный отказ; builder не должен
возвращать repeated path даже при injected malformed Git output.

У actual `.gitmodules` URL заканчиваются `.git`. Existing
`ops/docs/assemble.py:94–114::validate_source_binding` принимает иной URL regex
без `.git`. Это конкретная соседняя несовместимость; seam **не** нормализует
URL ради неё. Исправление/приёмка assembler остаётся отдельному owner ticket.

## 2. Docs transport, без неявного production fallback

```ts
// ops/docs.ts — предлагаемые additive types, не существующие API.
export interface GitLimits {
  wallMs: number; drainMs: number;
  streamBytes: number; totalBytes: number;
  maxCommands: number; maxTotalBytes: number; totalWallMs: number;
}
export interface GitCall {
  executable: string; // canonical absolute admitted git path
  args: string[];     // ниже: fixed options + -C root + owning argv
  cwd: string;
  env: Record<string, string>;
  clearEnv: true;
  tag: { attempt: string; ordinal: number };
}
export interface GitReply {
  stdout: Uint8Array; // именно acknowledged bytes данного stdout
  result: FiniteResult;
}
export type GitTransport = (call: GitCall) => Promise<GitReply>;
export function makeDocsGitRunner(options: {
  root: string; attempt: string; gitExecutable: string;
  limits: GitLimits; invoke: GitTransport;
}): GitRunner;
```

`invoke` — зависимость доверенного кода orchestration, не имя callback/команды
из CLI, plan или admission JSON. В этом I-ticket допустима только fake transport
реализация. Отсутствующий production binding возвращает явный blocker; никакого
`invoke ?? run`, buffered `.output()` или автоматического запуска Deno/Git.
`preflight` может получить optional code dependency object с `gitRunner`, но
при отсутствии остаётся `sources:null` и существующий blocker. Предлагаемая
сигнатура: `preflight(args, root=workspace, deps?: {gitRunner: GitRunner})`.
Если deps есть, вызвать `sourceGraph(root,true,deps.gitRunner)`; исключение
пишется в blocked receipt, не проглатывается и не преобразуется в empty graph.
Это source observation, не разрешение BUILD.

Runner принимает только root либо canonical direct `root/components/<name>` и
owning argv из текущего `sourceGraph`: `rev-parse HEAD`, `status --porcelain`,
`ls-tree -rz HEAD`, два точных `config -f .gitmodules ...` варианта. Root URLs
читаются только из `.gitmodules`, не из shell. GitCall args:
`["--no-pager","--no-optional-locks","-c","core.fsmonitor=false",
"-c","core.untrackedCache=false","-C",root,...args]`.
Environment: `GIT_OPTIONAL_LOCKS=0`, `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`;
`clearEnv:true`, stdin null в будущем production adapter. Local repo config и
Git filesystem access не становятся sandbox: это отдельный BUILD contract.

Все limits — положительные safe integers, проверенные до transport. Runner
один на весь scoped attempt: counters/deadline делят все graph calls и snapshots.
После исчерпания `maxCommands`, `maxTotalBytes` либо
общего deadline новый transport call не допускается. Per-call caps и deadlines
должны укладываться в remaining limits; retries отсутствуют. Для графа из N
components один successful `sourceGraph(...,true,runner)` требует `4+4N` Git
calls; capture ниже использует два, expected/before/after вместе — шесть.
Нельзя дать каждому snapshot новый полный grant. Конкретный execution envelope
для этих calls выдаётся отдельно; этот design runtime budget не активирует.

Успех отдельного Git call требует: exit non-null, code0, success=true,
reason=null, drain=complete, retention=acknowledged, errors empty,
received=attempted=acknowledged отдельно для обоих streams; stdout.length равен
его acknowledged count. Nonempty stderr сам по себе не failure, но сохраняется.
Иначе бросить typed `GitObservationError` с call tag и конечным failure code:
`spawn_failed`, `transport_failed`, `deadline`, `log_cap`, `drain_incomplete`,
`retention_unknown`, `git_nonzero`, `invalid_reply`, `invalid_utf8` или
`budget_exhausted`. stdout декодируется UTF-8 fatal только после этих проверок;
для совместимости owning API возвращается `.trimEnd()`. `ls-tree` сохраняет NUL
внутри строки. Не парсить частичный/обрезанный stdout как graph.

Transport пишет оригинальные capped stdout/stderr и terminal result даже на
failure. Spawn rejection до `Child` обязательно становится failure receipt;
это отсутствует у raw `runFinite` и не должно маскироваться. Durable storage,
остановка descendants, эффективная отмена sink/IO и total RSS не следуют из
`FiniteResult`; прежние null/unknown сохраняются. В fake implementation
подтверждается только строгий отказ runner по этим полям, не enforcement ОС.

## 3. Frozen inputs и late fresh SourceRef

Не создавать вручную поддерживаемый список SHA компонентов. Фиксированный
manifest входных **файлов** и новый ephemeral SourceRef имеют разные роли.

```ts
export interface InputBinding {
  path: string; // canonical absolute path, уникальный
  bytes: number;
  sha256: string;
}
export interface DocsSourceIdentity {
  graph: SourceGraph;
  inputs: InputBinding[];
}
export interface FrozenDocsInputs { inputs: InputBinding[] }
export interface IdentityDeps {
  git: GitRunner;
  limits: { maxFiles: number; maxFileBytes: number; maxTotalBytes: number };
  readInput: (path: string, cap: number) => Promise<Uint8Array>;
}
export async function captureDocsIdentity(
  root: string, frozen: FrozenDocsInputs,
  deps: IdentityDeps,
): Promise<DocsSourceIdentity>;
export function compareDocsIdentity(
  expected: DocsSourceIdentity, observed: DocsSourceIdentity,
): { equal: true } | { equal: false; fields: string[] };
```

`readInput` production binding — существующий `readRegularBounded`; mandatory
per-file и total input byte caps принадлежат trusted enclosing policy, не hashes
из недоверенного manifest. Все три limits — положительные safe integers,
проверенные до Git/чтения; число inputs не больше maxFiles. В каждый read передать
`min(maxFileBytes, maxTotalBytes-actualTotal)`; нулевой remaining допускает только
заявленный пустой файл с overflow sentinel существующего reader. ActualTotal
увеличить на фактическую длину; oversize либо mismatch expected bytes/hash
запрещает identity. Нельзя использовать input.bytes как единственный предел.
SHA256 вычисляется из фактических bytes текущим
`sha256`. Нет metadata-only успеха. Invalid/missing/duplicate path, invalid
hash/size, дополнительные/исчезнувшие entries отвергаются.

Frozen manifest обязательно включает plan, Julia Project/Manifest, выбранные
recipe и operator source, исполняемые ops docs/Git/assembly/math sources и
asset lock; выбранный owner source/staged manifest добавляет future staging
owner, а не этот seam. Любые внешние прочитанные файлы, требуемые реальным
вызовом, должны быть перечислены его owning input contract. Hash readback
стейджинга, toolchain/cache/import closure пока отсутствует — их не считать
покрытыми списком из текущего preflight. Manifest сравнивается как точный
набор path+size+hash, порядок — стабильный code-unit comparator.

Один capture: `g1=sourceGraph(root,true,deps.git)` → bounded read/hash ровно
frozen input paths → `g2=sourceGraph(root,true,deps.git)` → exact g1=g2 →
фактические file bindings равны frozen manifest → detached identity.
При ошибке Git/чтения нет identity. Graph включает format, Root revision,
полный состав и revision/URL каждого компонента. Canonical byte serialization:
UTF-8 `JSON.stringify({graph:{format,revision,components:[{path,revision,url}]},
inputs:[{path,bytes,sha256}]})`, фиксированный порядок keys, сортированные arrays,
без пробелов/финального LF; digest SHA256 — для provenance, сравнение полей
явное и не ограничивается одним digest. Expected и observed глубоко копируются;
поздняя мутация caller arrays не меняет receipt.

Late fresh SourceRef — `graph` из успешного capture **после** выбора финального
чистого Root ref. Это ephemeral observation в attempt, не lock-файл. Root SHA
нельзя заранее брать из старого design/receipt, из текущего dirty coordinator
checkout либо автоматически заменять на HEAD при mismatch. Frozen file bytes
позволяют подготовить inputs раньше финального commit; поздний capture связывает
их с фактическими committed gitlinks. Пересмотр frozen manifest или selected
ref требует нового attempt/identity. Пара boundary snapshots обнаруживает
наблюдённые изменения, но не доказывает отсутствия ABA/same-size overwrite или
замены и возврата между наблюдениями: exclusivity остаётся внешним prerequisite.

## 4. Чистый before/after control вокруг одного execute

```ts
export type OperationOutcome<T> =
  | { kind: "completed"; value: T }
  | { kind: "failed" | "unknown_partial"; error: string };
export interface ScopedIdentityResult<T> {
  state: "blocked_before" | "completed_bound" | "failed_bound" |
    "failed_source_changed" | "failed_identity_unknown";
  expected: DocsSourceIdentity;
  before: DocsSourceIdentity | null;
  after: DocsSourceIdentity | null;
  operation: OperationOutcome<T> | null;
  error: string | null;
  mismatches: string[];
  candidate: null;
}
export async function withDocsSourceIdentity<T>(options: {
  expected: DocsSourceIdentity;
  capture: () => Promise<DocsSourceIdentity>;
  execute: () => Promise<OperationOutcome<T>>;
}): Promise<ScopedIdentityResult<T>>;
```

Правила: capture-before и exact compare с detached expected обязательны до
execute. Ошибка/dirty/Root change/child mismatch/input change дают blocked_before,
operation=null, execute count0. После допуска execute вызывается ровно один раз.
После его success, failure или throw **всегда** capture-after; throw callback
преобразуется в unknown_partial, исходная ошибка сохраняется. Если after
отличается от expected/before — failed_source_changed, raw operation сохраняется
без приёмки. Если after получить нельзя — failed_identity_unknown; Root/child
dirty после исполнения относится сюда с конкретной причиной. Совпавшие снимки
дают completed_bound только при operation.completed, иначе failed_bound.
Это process/source binding, ни в одном случае не docs/scientific PASS.

`execute` по контракту пишет только raw namespace. Pure wrapper не может
изолировать произвольный callback от FS; test dependency — trusted fixture,
production effect binding ещё отсутствует. `candidate:null` обязательно во
всех состояниях этого seam; promotion требует отдельного accepted assembly +
schema + content acceptance и успешно закрытого after capture. Preflight не
вызывает withDocsSourceIdentity с реальным Julia/assembler и сохраняет blockers.

## 5. Namespace и provenance

Использовать существующий exclusive `attempt` вне source tree. Read-only inputs
не менять. Git metadata: `<attempt>/provenance/git/<ordinal>/` с
`command.json`, `stdout.raw`, `stderr.raw`, `result.json`; ordinal attempt-global,
без повторного использования. Identity receipts связывают каждый start/end
capture с точными ordinal ranges. Files createNew, directory creation exclusive,
caps включают все шесть graph observations expected/before/after.
`command.json` содержит exact executable/argv/cwd/safe env и limits; terminal
receipt — stdout/stderr counters, outcome/error/null measurements и paths/hashes
только реально прочитанных сохранённых bytes. Не записанные bytes — missing,
не zero. Partial raw не очищать и не заменять успешным повтором.

`<attempt>/provenance/source-identity/{expected,before,after,terminal}.json`
содержит full snapshots, input paths/actual hashes, identity digest, attempt,
parent_attempt (null либо точный original), command receipt refs и missing/error
fields. Отсутствующий after сохраняется null с причиной. Исходные failure raw/
receipts immutable по контракту createNew; acknowledgement не означает fsync.
Result raw остаётся `<attempt>/raw/<owner>`; source
`<attempt>/stage/<owner>/src`. Этот seam candidate bundle не создаёт и старый
receipt/candidate не ищет. Ошибка provenance write сама запрещает bound success;
нельзя продолжить молча с отсутствующим terminal receipt. Production terminal
writer и namespace ownership/exclusivity остаются отдельным binding.

## 6. Meaningful controls следующего I-ticket

Только source fixtures с fake transport/capture/execute/sink; исполнение требует
отдельного finite fixture grant. Здесь они спроектированы, не запускались.

1. Вызвать настоящий `sourceGraph(...,true,fakeGit)`, записать каждый argv;
   valid N-component fixture возвращает точный graph, root/child calls идут
   только в fake, legacy buffered runner не вызывается. Отдельные dirty Root,
   dirty child, child HEAD≠gitlink, nested gitlink, orphan/missing `.gitmodules`,
   invalid URL/path/duplicate graph entry отвергаются. Incomplete stdout никогда
   не принимается. Lowercase/uppercase и `-`/`.` fixtures проверяют exact ASCII
   order, включая permutations входа; localeCompare replacement будет заметен.
2. Success transport с ненулевыми stdout/stderr сохраняет exact bytes и counts.
   Nonzero exit, log cap, deadline, hanging drain, sink reject, spawn reject,
   invalid UTF-8, inconsistent counts/length, cumulative command/byte/deadline
   exhaustion запрещают graph; error receipt с правильным tag остаётся. После
   exhaustion invoke count не растёт. Fake props не доказывают ОС enforcement.
3. Expected capture и before совпадают: один execute и один after; completed_bound,
   точные full graph/input hashes, candidate=null. Failed operation + stable after
   даёт failed_bound, throw — unknown_partial + after; no swallowed failure.
4. Перед execute изменить Root revision либо actual child≠committed gitlink,
   dirty Root/child, файл при прежнем размере: operation count0, blocked_before,
   сохранены expected/before/error. Не принимать old receipt с новым Root SHA.
5. Внутри fake execute поменять Root revision, component revision/URL/set либо
   байты plan/recipe при прежнем размере: execute count1, after mismatch,
   failed_source_changed, original raw exact bytes остаются, candidate отсутствует.
   Capture-after rejection/dirty даёт failed_identity_unknown, after=null;
   before success не превращается в итоговый PASS.
6. Изменить graph между двумя внутренними graph reads одного capture — отказ;
   перестановка равных entries не меняет canonical identity. Поздно мутировать
   fake input arrays после return — detached terminal result неизменен.
7. Старая preflight fixture без deps по-прежнему blocked; с fake graph deps
   sources может быть заполнен, но остальные blockers, admission:null,
   steps:[] и отсутствие real execute/candidate сохраняются.

При реализации менять `buildBlockers` только для фактически связанного docs
runner, не снимать его по наличию marker/deps key; production binding отсутствует
— production CLI blocker остаётся. Runtime old DOC04 5/5 EXHAUSTED сохраняется;
данный source ticket не открывает retry и не перезаписывает старую историю.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning SourceGraph должен остаться единственным builder | `ops/git.ts::sourceGraph`, actual Root107bac5, SHA companion | Сегодня buffered Git transport | изменить |
| Locale-independent порядок нужен для воспроизводимой identity | `gitlinks:24` использует localeCompare, ASCII path grammar | Новый comparator/controls ещё не реализованы | изменить |
| SourceRef обязан быть поздним и свежим | Actual107bac5 против overlayb07974b и разных Runner links | Текущие dirty trees не admitted execution inputs | сохранить |
| R1/R2 source correction не требует повторной реализации | v2 review SHA97f01e8b…, actual overlay hashes сверены | Нет runtime evidence | сохранить |
| Before/after seam можно реализовать без BUILD | Exact signatures и discriminating controls выше | Нужны I и независимый review; callback не sandbox | изменить |
| Полный docs pipeline готов | SourceGraph/assembler URL mismatch; staging/schema/assembler/runner/sentinels ещё открыты | Ни compile/import/render/browser/offline/light/native/full acceptance не измерены | данных недостаточно |

STOP после одного контракта. Следующий шаг — независимый high source review этого
design на тех же frozen inputs; не автоматический переход к implementation.
