# OPS04.S — узкий addendum: исполняемый CLI seam

Статус: **предложение для независимого high review; STOP до решения координатора**. Этап — source-only design, без реализации и выполнения fixtures. Этот документ уточняет только отсутствовавший test seam в принятом D2, SHA256 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147`; независимая D2 review — `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`. D2 §5/T1/T2, full graph, produced JSON/SHA256, Nix assertion и все остальные gates сохраняются. Никакого native/scientific verdict этот addendum не даёт.

## Задача и выбранная граница

Нужно причинно проверить **тот же код, который вызывает CLI**: bounded capture, один capture исходного пути, отказ invalid UTF8 и отказ metadata до первого Nix callback application assembly. Frozen RED packet честно отмечает, что его A/B fixture моделирует capture через `Deno.readTextFile`, а не вызывает production capture. Root source authority — `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; прочитан exact checkout `/tmp/qcl-ops04-root-worktree`, где изменены только два frozen test files. Gitlinks не менялись; submodules не инициализированы.

Первичные локаторы: `ops/solver.ts:124–136` держит capture внутри private `solver`; `ops/application_cd.ts:63–107` держит assembly внутри `import.meta.main`, причём application build (`69–76`) предшествует чтению metadata (`77`). `ops/solver.ts::buildSolver:44–110` уже имеет командный callback, но не CLI/capture seam. `nix/solver.nix:2–9` сейчас принимает поздний pathname; его исправление остаётся ровно D2. Caller search ограничен root `ops/`, `tests/`, `nix/`, `flake.nix`: operational callers — эти два TS пути. `nix/local-lab-packages.nix:14` — отдельный route, без нового exact-consumption claim.

Выбор: обычные именованные orchestration-функции с production defaults и узкий file opener. Subprocess harness потребовал бы отдельного runtime/permission scope. Source-text assertions не устанавливают причинное выполнение reader/order. Новый framework, отдельный executable или DI container не нужны.

## Именованные internal exports

Это внутренние TS exports для импорта root tests, а не новый пользовательский CLI или обещание стабильного внешнего API. Имена и сигнатуры фиксируются этим addendum:

```ts
interface DepotInputFile {
  stat(): Promise<{ isFile: boolean }>;
  read(buffer: Uint8Array): Promise<number | null>;
  close(): void;
}
type OpenDepotInput = (path: string) => Promise<DepotInputFile>;

export function captureDepotMetadata(
  path: string,
  open?: OpenDepotInput,
): Promise<string>;

interface BuildCliDependencies {
  openDepotInput: OpenDepotInput;
  readSourceGraph(): Promise<SourceGraph>;
  readJuliaManifestSha256(): Promise<string>;
  execute(command: Command, capture?: boolean): Promise<string>;
}

export function runSolverBuildCli(
  args: readonly string[],
  dependencies?: Partial<BuildCliDependencies>,
): Promise<DepotBinding>;

export function runApplicationCdCli(
  args: readonly string[],
  dependencies?: Partial<BuildCliDependencies>,
): Promise<{ manifest: Awaited<ReturnType<typeof deploymentManifest>>;
             depotBinding: DepotBinding }>;
```

`captureDepotMetadata`, `runSolverBuildCli` и общие types находятся в `ops/solver.ts`; `runApplicationCdCli` — в `ops/application_cd.ts`. Types экспортируются при необходимости импортов, без отдельного нового модуля. `DepotBinding` — ровно readonly observation из D2 §5/T1, не новый schema. Принятый `buildSolver(metadataJson, expectedGraph, expectedManifest, execute, options?)` не получает overload, path или новый аргумент. `DepotSpec` с unchecked object/path не остаётся обходом.

Production defaults: opener вызывает `Deno.open(path, { read: true })`; graph reader — штатный `sourceGraph()`; Manifest reader измеряет SHA256 bytes существующего `${workspace}/julia/Manifest.toml` через `Deno.readFile` + WebCrypto; execute — существующий `run`. Это не новый shell tool/dependency. Старый checksum для depot generation не требует изменения. Dependency functions фиксируются в local references до первого await; пользовательские callbacks не могут подменить последующие зависимости изменением переданного объекта. Graph сохраняется как собственный snapshot для сборки и recheck, а не mutable borrowed fixture object.

**Нельзя инъецировать** готовую captured string вместо reader, metadata validator, `buildSolver`, готовый manifest либо high-level assemble result. Иначе fixture мог бы обойти проверяемый production путь. Тест заменяет только низкоуровневый opener, readonly identity reads и фактический dispatch внешней команды. Запись `.pending` и rename остаются обычным production кодом и используют принадлежащий тесту TMPDIR.

## Capture: точный bounded контракт

Reader делает один `open(path)` и один capture через его descriptor. До первого data read проверяет `file.stat().isFile`; nonregular input отвергается. После успешного open descriptor закрывается ровно один раз через `finally` на success, stat/read/decode/size failure. До успешного open закрывать нечего. Source path после capture не читается и не разрешается заново; Nix этот path не получает.

«Один read» здесь означает один capture/open исходного файла, **не один syscall**: regular-file read вправе вернуть short read. Один буфер на 65537 bytes и последовательные чтения в его оставшуюся часть допускают суммарно максимум 65537 полученных bytes. EOF завершает capture; 65537-й byte немедленно отвергает oversize, без следующего read. Нулевой progress при непустом buffer отвергается, чтобы не образовать бесконечный loop. Ошибка read распространяется после close. Файл ровно 65536 bytes допустим только при EOF до sentinel byte. Не допускаются `readTextFile`/неограниченный `readFile` с последующей проверкой длины.

На captured bytes: reject raw NUL; reject UTF8 BOM `EF BB BF` до decoder; fatal UTF8 decode; encode-roundtrip должен побайтно воспроизвести capture. Невалидная кодировка не заменяется U+FFFD. JSON/type/full-graph/Manifest/archive/produced-size проверки выполняет общий D2 preparation code. Пустые bytes или malformed JSON не превращаются в пустую metadata. Reader не обещает snapshot против trusted writer, malicious capture-path race, FIFO race или kernel-blocked I/O; это те же ограничения D2.

## Единственный production путь и порядок

`runSolverBuildCli` принимает tail `[DEPOT_JSON, ...buildFlags]`. Private `solver()` сохраняет `depot` branch; его `build` branch только передаёт tail в эту функцию. Она проверяет аргументы/options, вызывает настоящий `captureDepotMetadata`, получает derived graph/Manifest SHA и вызывает D2 `buildSolver` с captured string. CLI `solver.ts build DEPOT_JSON [--profile ...] [--test-workers ...]`, ошибки и defaults сохраняются. Default execute не захватывает stdout solver build/prefetch, как прежний `run`.

`runApplicationCdCli` принимает `[DEPOT_JSON, MANIFEST_JSON, NIX_CACHE_URI?]` и содержит существующий assembly body. `import.meta.main` становится только `main(() => runApplicationCdCli(Deno.args))` с адаптацией возвращаемого значения к `Promise<void>`; успешное сообщение остаётся прежним. После проверки argv и существующей T2 cache guard:

1. Один настоящий capture → sourceGraph snapshot → измеренный Manifest SHA → полный D2 validate/normalize/size/hash preflight, **до `execute`**. Приватная общая preparation routine используется и здесь, и внутри `buildSolver`; новая параллельная validator implementation не создаётся. Preflight не выдаёт успешный build receipt.
2. Existing `.#application` build; затем `buildSolver` повторно валидирует **тот же captured string** с теми же expected identities и штатным default build options. Повторной metadata file capture нет. Prefetch/build scalar values и bound JSON/SHA берутся из одного D2 normalized value.
3. Existing path-info → `deploymentManifest` → штатный sourceGraph recheck → optional cache copy → createNew `.pending` → rename → сообщение. Readonly observation возвращается только вместе с успешным результатом; exception не выдаёт success receipt.

Capture flags для execute сохраняются: application/solver build и path-info получают `capture=true`, copy — прежний inherited stdout. `buildSolver` получает адаптер `(command) => execute(command, true)`. URI остаётся одним literal argv element. Извлечение общей существующей T2 syntactic guard для ранней проверки разрешено; scheme/password/trust policy не расширяется, `deploymentManifest` продолжает проверять guard и сохраняет digest `SHA256(JSON.stringify({sources,closures}))` без изменения.

«До первой команды» в fixtures означает первый `execute` callback для Nix build/prefetch/path-info/copy. Production `sourceGraph()` выполняет прежние readonly Git probes для установления expected graph; отказ metadata не обещает отсутствие этих probes. В тесте reader identities инъецируются, поэтому ни Git, ни иной subprocess не вызывается. SourceGraph recheck не удаляется и не подменяется предварительным snapshot; его изменение по-прежнему блокирует публикацию.

## Различающие fixtures, добавляемые к frozen RED source

Все fixtures импортируют эти exports; `import.meta.main` не запускается. Production adapters делегируют тем же функциям — отдельной test-only orchestration нет. Существующий helper/T2 inventory frozen packet сохраняется; им не приписывается новая coverage до появления следующих fixtures.

| Fixture | Причинный oracle |
| --- | --- |
| Instrumented opener + progressing short reads | Один open; stat до read; requested buffer lengths и суммарно returned bytes ≤65537; exact65536+EOF accepted, 65537 rejected без следующего read; close ровно один на каждом opened outcome; read/stat error и no-progress reject. Фальшивый handle использует production loop, не переопределяет capture. |
| Real temporary regular files с default capture | Валидный UTF8 roundtrip; invalid sequence `C3 28`, truncated multibyte, BOM и NUL отвергаются. Nonregular directory отвергается по stat до read. Не создавать/открывать real FIFO: отсутствие зависания при hostile path-race не заявляется. |
| Оба CLI seams: raw oversize/invalid UTF8 и wrong component graph | Fake `execute` записывает каждое обращение; reject + ровно 0 callbacks. Application output и `.pending` отсутствуют. Identity readers возвращают fixture graph/Manifest и не запускают команды. |
| Solver HTTPS/file healthy | Тот же actual outgoing `depotManifestJson` независимо хешируется; SHA argv/returned binding совпадают, late `depotManifest` arg отсутствует; command count 1/2, options сохранены. Opening-counter wrapper подтверждает один capture. |
| Application A→B на **первом application build callback** | Real temp file содержит A; callback атомарно заменяет его валидным B с другой archive URL/hash. Открытие path второй раз — fail. Последующие prefetch и solver build обязаны использовать A, возвращённые raw/produced hashes — A. Это различает поздний capture: он выбрал бы B. |
| Application full successful fake assembly | Fake ответы: exact application/solver store paths, path-info two SRI; actual owned TMPDIR получает manifest через production pending/rename. Assert existing manifest/release_id, sourceGraph вызван до assembly и после path-info, cache copy только после recheck, literal URI. B captured до начала consistently используется обоими consumers. |
| CLI argument/cache/preflight failure | Existing D2/T2 rejected values дают 0 execute callbacks; helper call cannot mask failed preflight. Никакого assertion-only grep по source. |

Read bound измеряется instrumented handle, fatal decoder проверяется real bytes, реальная causal ordering — mutation именно на первом application callback. Эти три свидетельства не заменяют друг друга. Frozen direct helper tests продолжают отдельно проверять полный graph, mutable callback inputs, normalization, options и failed prefetch. Никакой fake не заявляет выполнение Nix `hashString/fromJSON`, native outputs, runtime origin или scientific acceptance.

## Handoff и границы стоимости

Изменение после review ограничено root `ops/solver.ts`, `ops/application_cd.ts`, `nix/solver.nix` и двумя существующими test files. Новые dependencies, CLI flags, runtime environment, persistent registry, второй source lock и late pathname fallback не вводятся. Design не добавляет invocation: новые fixtures входят в **тот же один** общий D2 root Deno slot T1+T2, если координатор подтвердит remaining counter и exact prepared runtime/owned TMPDIR. Не выполнять отдельный capture subprocess, probe, fmt/test invocation или автоматический rerun из этого addendum.

Текущий envelope: ≤20min/1CPU/2GiB/source reads≤3MiB/report≤64KiB; CPU/RAM/read телеметрия не инструментирована, это порученные пределы, не измеренные значения. Выполнены только source/Git metadata/SHA reads и запись design/identity/digest artifacts в `/tmp`. Product edits, target imports, tests, Deno, Nix evaluation/build, Julia, installs, network/server, native/science, children и checkpoint writes — **0**. Root остаётся единственным checkpoint writer.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Frozen D2 не называл executable CLI seam | D2 §5/T1, frozen RED report; root cfc38e1 CLI locators | Только source observation | изменить |
| Предложенный seam проверяет production capture и assembly ordering | Именованные exports, low-level opener, A→B на первом application callback | Design; исходники/fixtures ещё не изменены и не исполнены | изменить |
| CLI, full graph, consumed JSON/SHA и release_id contract сохранены | Этот addendum + неизменённый D2, named adapters | Нужна independent review и последующая CP-CODE проверка | сохранить |
| Runtime/native/scientific acceptance установлена | Execution receipts отсутствуют | Все такие counters 0 | данных недостаточно |

**STOP: передать frozen addendum независимому high reviewer. Не начинать source edits, RED execution, Nix evaluation, native или checkpoint mutation.**
