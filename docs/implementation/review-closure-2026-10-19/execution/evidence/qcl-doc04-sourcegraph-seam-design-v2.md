# DOC04 SourceGraph seam D2: два адресных исправления

Статус: **D2_FOR_FRESH_HIGH_REVIEW; I ещё не разрешён этим документом**.
Исправлены только R1/R2 из [frozen review](qcl-doc04-sourcegraph-seam-design-v1-review.md),
SHA256 `852f66eac8efca500d34a9d5116074931a1b444ec6fdd57e5e443b361b13272b`.
V1 и его artifacts сохраняются byte-exact. D2 заменяет ниже API/order/observation/
comparison/wrapper clauses V1; transport caps, failure raw, namespace, blocked
BUILD и остальные exclusions V1 сохраняются. Ни реализация, ни controls не запускались.

Actual Root повторно наблюдён: `107bac5697b37cf0e47c3feb44883a907837645c`,
Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Runner
`4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`, Results
`de70638a982f91b7e125ab1cfc70a2daef2a656d`. Status прежний: modified checkpoint
и четыре untracked routing/publication artifacts. Root ledger — единственный
источник product/runtime counters. Product90/source11 и CHECK3/compiler0,
guard UNKNOWN1 failed/unit not ready переданы координатором; здесь не измерены.
Нового runtime grant нет, DOC04 old5/5 exhausted не изменён.

## R2: один owning GitReader, прежний общий graph/digest

Exact merge contract выбран по уже существующему Native overlay
`/tmp/qcl-docs-test-routing-worktree/ops/git.ts:33–86`:

```ts
export type GitReader =
  (root: string, args: readonly string[]) => Promise<string>;
export function git(root: string, args: readonly string[]): Promise<string>;
export async function sourceGraph(
  root = workspace, requireClean = true, readGit: GitReader = git,
): Promise<SourceGraph>;
```

`git` по-прежнему копирует readonly args через `[...args]` в Command args.
Все внутренние Git calls единственного owning `sourceGraph` используют readGit.
Все проверки clean/gitlink/URL/nested/orphan и двухаргументные legacy callers
сохраняются. Docs factories возвращают **GitReader**, принимают readonly argv
и копируют его перед transport; имени/типа GitRunner из V1 больше нет.
`preflight(args,root=workspace,deps?:{readGit:GitReader})`: при наличии доверенной
code dependency вызывает `sourceGraph(root,true,deps.readGit)`; без binding
сохраняет sources:null/blocker. Нельзя разрешать production CLI по наличию deps,
возвращать empty graph при failure либо падать обратно на buffered default.

**Не менять** `gitlinks(...).sort((a,b)=>a.path.localeCompare(b.path))`, формат
`qcl-negf.git-graph.v1`, returned components order/URL, общую JSON serialization
и raw JSON digest. Native driver `ops/docs_tests_cli.ts:182–186` продолжает
хэшировать UTF-8 `JSON.stringify(observed)` без docs normalization. В этом D2
не добавлять новый global graph ordering/duplicate-policy patch: прежняя owning
семантика полностью сохраняется. Вопрос malformed duplicates не расширяет этот ticket.

Root — единственный будущий writer canonical `ops/git.ts`; reuse выбранный
additive Native seam, не применять две конкурирующие реализации третьего аргумента.
Native overlay — unpublished исходник, не published API actual Root. Docs/Native
не редактируют этот путь параллельно. I-ticket paths остаются `ops/git.ts`,
`ops/docs.ts`, `tests/git_test.ts`, `tests/docs_recipe_orchestration_test.ts`;
Core/Runner profiles и operator recipe не входят.

Docs-only identity использует **отдельную private detached copy**: graph keys
format/revision/components, component keys path/revision/url, inputs keys
path/bytes/sha256; arrays копируются и сортируются code-unit comparator
`a.path<b.path?-1:a.path>b.path?1:0`. UTF-8 JSON.stringify({graph,inputs}), без
whitespace/LF, даёт `docs_identity_sha256`. Исходный graph не мутировать.
Его raw JSON digest сохранять отдельно как provenance, не подменять им docs
digest и не менять Native digest. Private comparator сравнивает точные наборы,
включая URL/компоненты; повторные paths отвергает **docs projection**, не global
builder. Изменение только порядка равных entries не есть docs source change.

## R1: observation сначала, frozen comparison отдельно

Ни observer, ни reader не требуют actual hash=expected hash, чтобы вернуть
фактически измеренные bytes/hash. Они не получают frozen file sizes в качестве
доказанного текущего stat. Existing bounded regular reader проверяет собственный
наблюдённый stat, а trusted caps берутся из policy. Новый hash при прежнем размере
— полноценное наблюдение, а не исключение `cannot_capture_identity`.

Ниже exact предлагаемые **новые docs types**. Это source API design, не новый
public SourceGraph/schema и не разрешение production execution.

```ts
interface FileBinding { path: string; bytes: number; sha256: string }
interface EvidenceRef { path: string; sha256: string | null }
interface ObservationError {
  code: string; path: string | null; detail: string;
  evidence: readonly EvidenceRef[];
}
type InputObservation =
  | { kind: "present"; actual: FileBinding; evidence: readonly EvidenceRef[] }
  | { kind: "absent"; path: string; evidence: readonly EvidenceRef[] }
  | { kind: "unreadable"; path: string; error: ObservationError };
interface GitReadEvidence {
  ordinal: number; root: string; args: readonly string[];
  stdout: string; stdout_sha256: string; receipt: EvidenceRef;
}
type GraphRead =
  | { kind: "complete"; graph: SourceGraph; raw_json_sha256: string;
      git: readonly GitReadEvidence[] }
  | { kind: "rejected"; git: readonly GitReadEvidence[];
      error: ObservationError };
interface DocsObservation {
  start: GraphRead;
  inputs: readonly InputObservation[];
  end: GraphRead;
}
interface ObservationDeps {
  readGit: GitReader;
  readInput: (path: string, cap: number) => Promise<InputObservation>;
  limits: { maxFiles: number; maxFileBytes: number; maxTotalBytes: number };
}
export async function observeDocsSources(
  root: string, paths: readonly string[], deps: ObservationDeps,
): Promise<DocsObservation>;
```

`paths` — точный проверенный unique canonical path set frozen manifest, без
его ожидаемых hashes/размеров; limits проверены до reads, общий budget — на
весь enclosing attempt. Прежние per-call/aggregate Git limits V1 сохраняются.
Observer делает owning graph-start → bounded current input reads → owning
graph-end; не прекращает наблюдение только из-за frozen mismatch. Для каждого
input ровно одно состояние. Cap = min(maxFileBytes,remaining actual total);
actual present bytes суммируются. Превышение cap, denied access, unstable read,
deadline/transport failure — unreadable с причиной, не отсутствие и не bytes0.
После исчерпания бюджета последующие entries получают unreadable/budget_exhausted
без дополнительного I/O; end rejected/budget_exhausted без нового Git call.
Verified NotFound requested path означает absent, hashes/bytes для него отсутствуют.
Пустой regular file — present с bytes0 и SHA256 пустых bytes, что отличается от absent.

`readGit` оборачивается recorder в docs code: записывает только **полностью
успешный transport stdout** и его receipt перед возвратом owning builder.
При builder throw сохраняются уже полученные Git evidence; graph rejected
не становится complete. Raw truncated/failed stdout не годится для positive
Git change evidence. `status --porcelain` с непустым successful stdout доказывает
наблюдённый dirty scope; successful `rev-parse HEAD` позволяет сравнить actual
revision с expected. Evidence содержит bounded original status string/hash,
root/argv и receipt, а не caller-provided clean boolean. Gitlink mismatch может
быть доказан фактически прочитанным child HEAD против expected committed link;
остальные builder rejects сохраняются unknown, если positive evidence отсутствует.
Это извлечение наблюдений из existing reader, не второй SourceGraph builder.

```ts
type ChangeEvidence =
  | { kind: "file_changed"; expected: FileBinding; actual: FileBinding;
      evidence: readonly EvidenceRef[] }
  | { kind: "file_absent"; expected: FileBinding;
      evidence: readonly EvidenceRef[] }
  | { kind: "graph_changed"; expected: SourceGraph; actual: SourceGraph }
  | { kind: "git_dirty"; root: string; actual_status: string;
      evidence: GitReadEvidence }
  | { kind: "git_revision_changed"; root: string;
      expected_revision: string; actual_revision: string;
      evidence: GitReadEvidence }
  | { kind: "graph_changed_during_observation";
      start: SourceGraph; end: SourceGraph };
interface DocsIdentity { graph: SourceGraph; inputs: readonly FileBinding[] }
interface Matched {
  kind: "matched"; observation: DocsObservation; actual: DocsIdentity;
}
interface ObservedChanged {
  kind: "observed_changed"; observation: DocsObservation;
  changes: readonly [ChangeEvidence, ...ChangeEvidence[]];
  unknowns: readonly ObservationError[];
}
interface UnreadableUnknown {
  kind: "unreadable_unknown"; observation: DocsObservation;
  unknowns: readonly [ObservationError, ...ObservationError[]];
}
type Comparison = Matched | ObservedChanged | UnreadableUnknown;
export function compareDocsObservation(
  expected: DocsIdentity, observed: DocsObservation,
): Comparison;
```

Comparison — pure, без I/O. Сначала собрать **все доступные** positive changes
и unknowns: present.actual против expected path/size/hash; absent для ожидаемого
пути; оба complete graphs против expected и друг друга; successful dirty/revision
Git evidence из rejected graphs. Потом strict precedence:

1. Есть хотя бы одно положительное изменение → ObservedChanged, даже если есть
   дополнительные unknowns. Сохранить их, не объявлять остальные inputs известными.
2. Нет доказанного изменения, но есть missing/rejected/invalid/unstable fields →
   UnreadableUnknown, без выдуманного actual identity.
3. Только все inputs present и равны, оба complete/равные graphs с clean contract,
   нет unknowns/changes → Matched с detached actual identity.

Некорректный/дублированный/добавленный input path set из недоверенного deps даёт
unknown/invalid_observation_shape, не matched. Frozen bytes/hashes проверяются
валидатором expected заранее. Изменение такого input set не принимается как
валидная новая identity. Source cleanliness для complete graph следует из
owning builder requireClean=true, не из присланного status flag.

Expected разрешено создать только late-fresh trusted binding:

```ts
type ExpectedPreparation =
  | { kind: "expected_ready"; expected: DocsIdentity }
  | { kind: "expected_invalid"; observation: DocsObservation;
      changes: readonly ChangeEvidence[];
      unknowns: readonly ObservationError[] };
export function prepareDocsExpected(
  frozen: { inputs: readonly FileBinding[] }, observed: DocsObservation,
): ExpectedPreparation;
```

Preparation требует valid frozen manifest, все present hashes=его hashes, два
complete clean graphs с равным private projection, ни dirty evidence, ни unknown.
Успех возвращает detached copy actual graph/validated frozen bindings; сначала
выбирается final clean Root ref, затем создаётся fresh expected. Раннее freeze
file bytes не фиксирует исторический Root SHA. Invalid expected не запускает
wrapper вообще и сохраняет typed evidence/error. Произвольный JSON receipt не
может стать expected_ready по своему `kind`: creation доступно только доверенному
code path. Auth/admission и opaque type сами по себе не равны этому контракту.

## Wrapper: reachable before/after outcomes

```ts
type Operation<T> =
  | { kind: "completed"; value: T }
  | { kind: "failed" | "unknown_partial"; error: string };
type FailureOperation = Extract<Operation<never>, { error: string }>;
interface CommonResult {
  expected: DocsIdentity; candidate: null;
}
type ScopedIdentityResult<T> = CommonResult & (
  | { state: "blocked_before"; before: ObservedChanged | UnreadableUnknown;
      operation: null; after: null }
  | { state: "completed_bound"; before: Matched; after: Matched;
      operation: Extract<Operation<T>, {kind: "completed"}> }
  | { state: "failed_bound"; before: Matched; after: Matched;
      operation: FailureOperation }
  | { state: "failed_source_changed"; before: Matched; after: ObservedChanged;
      operation: Operation<T> }
  | { state: "failed_identity_unknown"; before: Matched; after: UnreadableUnknown;
      operation: Operation<T> }
);
export async function withDocsSourceIdentity<T>(options: {
  expected: DocsIdentity; // validated detached expected_ready value only
  observe: () => Promise<DocsObservation>;
  execute: () => Promise<Operation<T>>;
}): Promise<ScopedIdentityResult<T>>;
```

Before = compare(expected,observe()). Changed/unknown → blocked_before,
execute count0. После matched вызвать execute ровно один раз, затем независимо
от его завершения/throw выполнить after observe+compare. Callback throw становится
operation.unknown_partial с original error; raw сохраняется. Throw observer вне
его штатного typed API преобразовать в UnreadableUnknown с synthetic rejected
graph records/непрочитанными input entries, причину не терять. After Changed →
failed_source_changed, after Unknown → failed_identity_unknown. Только after
Matched выбирает completed_bound/failed_bound по operation. Никакой branch не
выдаёт docs acceptance/PASS, source-only I-Root остаётся PARTIAL.

Original raw и provenance не удаляются на mismatch; candidate:null во всех
branches. Receipts сохраняют **полную Observation + Comparison**, включая
actual новый hash, verified absence, dirty status и unknowns; нельзя заменить
их одним error string либо старым expected hash. Namespace/createNew/failure
writer правила V1 сохраняются; production terminal writer не становится готовым.
ABA/exclusivity, missing native admission и эффективная остановка процессов
сохраняют отдельные ограничения и не препятствуют этому source design repair.

## Два адресных набора controls для I-ticket

**R2 compatibility:** owning sourceGraph с Native-compatible readonly fake reader;
все Git calls инъецированы. Проверить legacy graph order и exact
JSON.stringify(graph)/его SHA unchanged при тех же recorded Git replies,
включая upper/lowercase/`.`/`-` paths. Отдельно docs projection из перестановки
равных entries даёт тот же private digest и не мутирует original array. Никакого
требования глобального ASCII order. Старые callers не используют docs projection.

**R1 reachable evidence:** создать valid frozen+late-fresh expected; before
Matched. В fake execute один раз изменить external plan либо recipe при том
же размере, сохранив graph replies clean/stable. Reader-after возвращает present
actual bytes → actual hash differs → ObservedChanged/file_changed →
failed_source_changed. Проверить exact новые hashes/bytes, before original hash,
execute count1, original nonzero raw intact, candidate:null. До execute такой
же mismatch даёт blocked_before/count0. Это различает ошибку D1: observer,
отвергающий frozen mismatch, не сможет пройти требуемый typed Changed branch.

Дополнительные ветви того же control: verified absence → ObservedChanged/
file_absent без bytes/hash0; permission error при отсутствии других changes →
UnreadableUnknown/failed_identity_unknown; новый hash плюс unreadable второй
input → ObservedChanged **с** unknowns; успешный dirty status после execute →
ObservedChanged/git_dirty с original status, не generic unknown; truncated
status transport → Unknown без dirty claim. Operation failed/throw всё равно
получает after. Ни один fixture не запускает Git/Julia/assembler или production
transport; tests/typecheck исполнения в этой фазе отсутствуют.

Staging/schema/assembler `.git` URL mismatch/renderer/production runner/sentinel/
native/resource/browser/offline/light acceptance остаются отдельными tickets.
Не править их ради прохождения двух controls и не расширять source gap verdict.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Один additive owning API согласован с Native | GitReader readonly, readGit third arg; Native source33–86 | Unpublished seam, нужен один Root writer и свежий review | изменить |
| Общий release graph/digest сохраняется | D2 явно сохраняет localeCompare/v1/raw JSON | Docs private projection не global migration | сохранить |
| Известное изменение не теряется как unknown | Observation/Comparison precedence; same-size control | Реализация/исполнение отсутствуют | изменить |
| Отсутствие/ошибка чтения не заменяются нулём | absent/unreadable/present отдельны, evidence nullable | IO/exclusivity/durability не доказаны | сохранить |
| I и полный DOC04 готовы | Fresh high review ещё предстоит; broader gaps сохранены | BUILD/native/runtime не запускались | данных недостаточно |

STOP: свежий independent high review D2; только затем решение I-ready.
