# OPS04.S Root — independent high CPP formatted candidate

2026-10-20. **APPROVE exact formatted source candidate: блокирующих замечаний не найдено.** Реализация соответствует принятому D2 T1/T2 и CLI seam; исправленный F1 oracle сохранён. Это source/CPP verdict на пяти файлах ниже, а не observed GREEN, Nix evaluation, native/scientific acceptance или разрешение дополнительного runtime invocation. Координатор отдельно связывает actual integration source и решает единственный оставшийся finite GREEN.

## Source identity и порядок независимой проверки

Сначала прочитаны baseline `git show HEAD:ops/solver.ts`, `ops/application_cd.ts`, `nix/solver.nix`, accepted D2/seam и relevant review sections; затем formatted production source и test/format delta; после primary code — implementation report и original RED/format receipts. Reviewer отдельный от автора, тот же, который выполнил полные v2 и narrow v3 test-source reviews. Ранее раскрытое ограничение порядка чтения в original seam-design review не скрывается; этот code review выполнен с baseline/design перед candidate.

Checkout `/tmp/qcl-ops04-root-worktree`, фактический HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Status показывает ровно пять owning files: `nix/solver.nix`, `ops/application_cd.ts`, `ops/solver.ts`, `tests/application_cd_test.ts`, `tests/solver_test.ts`. Восемь selected root gitlinks не инициализированы и не обновлялись. Root tree остаётся authority состава; identity receipts не заменяют Git и не являются revision lock. Координаторское продвижение другого integration root не подменяет этот reviewed base и требует собственного final source binding.

| Точный candidate input | Проверенный SHA256 |
| --- | --- |
| ops/solver.ts | 63c26b64d981d5436172a676dd309a6f74cee1184b3e1b392a9c8a99d5193912 |
| ops/application_cd.ts | 5e79f0ac36f922cc77805d68ca8122bd8b9fc34267109362d5fc4a6299b5bf71 |
| tests/solver_test.ts | d17eaf24461d702f202209a086f3f819b287690c9ebbd14fce20ef7cb949a025 |
| tests/application_cd_test.ts | da25777fc58752236b3e8b812bbbbc11fa63b328bb7e8aaf0c3fcf987d1bfcc2 |
| nix/solver.nix | dacc900b41f3e9866e3b164243385ce81fdf9df3925061573bc8731f26e71e8b |
| root-formatted-identity.json | 6ef3020ab43bcb03d75288018e2e08f4f59e67f1dc1dd14cf1940d6113dc9bab |
| root-formatted-patch.diff | 841e8b236bbcc84b9d04b2c18f03fbce8260e1854af86f41443909d9146bccf4 |
| root-format-delta.diff | 5e8503bd2ef7303799d1a118a7ca2f837366ddb88110562ba778bae04de95b4f |

Actual `git diff --` по этим пяти файлам независимо даёт SHA full formatted patch `841e8b...`; размер сохранённого patch 73167 bytes. Accepted inputs SHA: D2 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147`, high D2 R `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`, CLI seam `93ffbbcdd50770295f2f21e1a9befc47acc63231279b1ff79aebf48e7cc69a7f`, seam R `626159c6307b5664025d800f7d3d8101fb1ab55a4bd8a809f76b4aa949e653d5` проверены.

## Причинный production contract

### Capture и UTF8

`ops/solver.ts::captureDepotMetadata:45–76` действительно открывает original pathname один раз. `stat().isFile` до read; один buffer 65537 bytes; каждый read получает только оставшийся subarray. Positive short read увеличивает count, invalid/zero progress отвергается, sentinel65537 вызывает немедленный throw без дополнительного read. Для exact65536 остаётся one-byte view, на котором требуется EOF. Descriptor закрывается в `finally` на success/stat/read/size/decode outcomes; open failure не создаёт descriptor.

Raw NUL и начальный UTF8 BOM проверяются до fatal decoder; encode-roundtrip сравнивает длину и каждый byte. CLI не использует unbounded readTextFile/readFile для depot metadata. Отдельный Manifest reader `41–43` измеряет bytes существующего `julia/Manifest.toml` через WebCrypto, без checksum subprocess. Ограничения против trusted concurrent writer, hostile path/FIFO race и kernel-blocked I/O остаются явно вне claim, как принято в D2; дополнительного trust namespace не появляется.

### Единый metadata input и полный graph

`prepareDepotMetadata:99–171` — одна общая preparation routine для direct helper и assembly preflight. Она экспортирована только для межмодульного internal import, не инъецируется dependencies и не является отдельным CLI. До callback проверяет runtime string type, raw UTF8 bound/roundtrip/BOM/NUL, JSON/top-object, depot/Julia/Manifest identities, graph format/root, полный path→revision+URL set. Map rejects duplicates, size+lookup detects missing/extra/changed components; object/array order не становится mismatch. Expected graph поступает от actual `sourceGraph()` defaults и хранится CLI как собственный structuredClone; доверие к произвольному handwritten expected graph не заявлено.

URL/hash — обязательные strings; сохраняется прежняя URL parsing и Nix/prefetch admission, без новой scheme/SRI/secret policy. Один JSON.parse→JSON.stringify сохраняет неизвестные metadata fields, разрешает raw duplicates обычным JS outcome и не сортирует keys. Raw и produced UTF8 sizes ограничены отдельно. URL/hash/protocol/root/Manifest/produced JSON скопированы в local primitive values до первого async hash; callback не получает parsed object. Frozen binding содержит отдельные raw/consumed SHA/count и identities, без success-status подмены. Общая preparation может сформировать observation до build; successful `buildSolver` возвращает его только после обоих нужных dispatches.

`buildSolver:207–280` имеет только принятый JSON/fullGraph/Manifest API: unchecked spec/path overload удалён. Options переобрабатываются прежним validator и копируются в local profile/workers до await. File prefetch берёт archive_url/hash из той же frozen binding, Nix получает boundJson и consumed digest. Failed prefetch/build распространяется без последующего build/success return. Legacy object+path invocation отвергается runtime type guard до callback.

### Actual callers, argv и Nix

`runSolverBuildCli:283–304` фиксирует dependency function references до await, сохраняет старый tail argv/options, вызывает настоящий capture, derives/copies graph, измеряет Manifest и вызывает настоящий buildSolver. Private `solver():318–384` build branch delegates этому же export; depot branch сохранил prior generation/checksum/archive/schema/guards. `runApplicationCdCli` ниже также вызывает тот же helper. Bounded caller search по `ops`, `tests`, `nix`, `docs`, `flake.nix`, `deno.json` не нашёл оставшихся DepotSpec или operational object/path callers. `nix/local-lab-packages.nix:14` — отдельный неизменённый route, не вызов этого entrypoint; новый consumption claim на него не переносится. CLI flags/defaults и documented command syntax сохранены.

`buildSolver:248–278` передаёт `--argstr depotManifestJson boundJson` и `--argstr depotManifestSha256 binding.consumed_metadata_sha256`; target pathname/realPath отсутствуют. `ops/process.ts::run` остаётся Deno.Command(argv), без shell interpolation. `nix/solver.nix:2–11` требует два strings, ставит outer type assert и hashString equality **до** let/fromJSON; readFile/path fallback удалён. Unchanged mkPreparedDepot/mkSolver/profile/workers guards сохраняются. Это достаточная source edge, но actual Nix evaluator/assertion/parser execution здесь не выполнен.

### Application preflight, identity и publication

`ops/application_cd.ts::runApplicationCdCli:79–141` — production assembly body, а main adapter вызывает именно его. Dependencies только low-level opener, readonly identity readers и dispatch; validator/buildSolver/captured string/manifest/result injection отсутствуют. Функции фиксируются до await, nested graph копируется до application callback. Capture→graph→Manifest→общий полный preparation предшествует первому execute. Последующий helper получает тот же immutable captured string; исходный pathname не читается поздно.

Application/solver/prefetch/path-info сохраняют capture=true, copy — inherited stdout; standalone solver CLI сохраняет inherited stdout. Store paths/path-info/deploymentManifest, обязательный graph recheck после path-info, optional literal cache copy, createNew pending и rename сохранены. Drift блокирует copy и manifest writes. Release digest и manifest schema остались `SHA256(JSON.stringify({sources,closures}))` / qcl-negf-release-v1. Наличие этих source guards не доказывает output contents, signatures или safe activation.

`validateCacheUri:18–38` общий для early CLI preflight и deploymentManifest. Type/whitespace/control/leading-dash/malformed URL reject; raw authority userinfo до last @ проверяется на literal colon, поэтому явный empty password delimiter не теряется при URL normalization. Username-only SSH/ssh-ng и percent-encoded colon в username сохранены; local/Nix forms не получили новую scheme policy. Literal URI остаётся одним argv element и не входит в release_id. Это прежний T2 password/argument guard, не universal secret scanner или новый trust root.

## Tests, formatter и original RED

Полные test-source reviews v2 и narrow v3 остаются применимы с проверенным format delta. Pre-format source-freeze `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.build/review-closure-coordination/source-freezes/OPS04-PRE-FMT-1` имеет solver/application tests SHA `d2c5da7...` / `bd92a82...`, совпадающие с принятым R3, и functional production SHA `22b6a3c...` / `4062fa9...`; Nix SHA не менялся. Delta прочитан как текст: imports type order, whitespace/wrapping, trailing commas, braces вокруг тех же single statement bodies и retained main adapter formatting. Не найдено изменения literals, conditions, callback route, fixture inventory или assertions. Это ручной source assessment, не AST equivalence proof.

В formatted `tests/solver_test.ts:265–307` F1 corrected expected всё ещё explicit ordered hash,url,format,sources,julia,juliaManifest, с literal reversed components; expected не выведен из outgoing/raw parser result. Actual outgoing JSON независимо SHA-хешируется в bound helper. Instrumented capture fixtures требуют actual production loop, exact65536/EOF, sentinel/no-extra-read, no-progress/close; real files проверяют actual opener/UTF8/BOM/NUL/directory. Solver actual CLI fixtures проверяют one capture и 0 callback на invalid encoding/size/graph/lock/options.

Application actual CLI A→B fixture выполняет atomic path replacement на **первом application callback** и проверяет A у prefetch/Nix/returned binding. Второй healthy B/dependency-mutation fixture различает stable function refs и owned nested graph. Полный order/stdout/literal cache/release digest/final-file assertions сохранены; actual pending/rename не заменены high-level fake. Drift/collision negatives остаются. Production adapters действительно delegates тем же именам, поэтому seam не test-only и fake не обходит preparation.

Original ROOT-RED-1 raw SHA `5ab3e0c1ba7a178fd6dd60c297119cac38e86a0d39df0bfa24df7d8a88ccb943` и receipt SHA `3dff28530a17d48d4bb28fadffa1f8692d8f06dd935fb08acaca4329688491d3` сверены и прочитаны. Raw показывает Deno test Check обеих files, затем 17 failed/9 passed; failure classes — old helper mismatch, absent seam healthy failures, missing-function downstream assertions, explicit-empty password gap. Author mapping всех17 соответствует raw и конкретному source repair. Девять passes, включая caught missing-function negatives, не названы полным доказательством. Receipt exit1, complete12460-byte raw, wall1.639s, guard_error/stop_reason null; это coordinator execution, не reviewer rerun.

FORMAT-1 receipt SHA `162c0f0a7494b76be4a853f9523ad9e5399577d9619a165854e58250c5bb14c5` описывает один pinned Deno2.8.3 fmt четырёх TS files, exit0/wall0.104s. Formatter receipt не является product unit/typecheck pass; final formatted code ещё не имеет GREEN. Нет основания запускать новый formatter или изменять tests ради зелёного статуса.

## Выполненный scope и дальнейшие gates

Envelope reviewer ≤25min/1CPU/2GiB/read≤5MiB/report≤128KiB. Cumulative CPU/RAM/read/tool-output telemetry не инструментировалась; assigned limits не выдаются за measured usage. Использовались explicit source/freeze/receipt paths, не traversal execution tree. Только text/Git/SHA reads и запись этих review artifacts в `/tmp`. Target imports/parsers/typecheck/Deno/Nix/tests/build/network/server, source edits, Git mutations, children и checkpoint writes reviewer — **0**. Runtime slots расход reviewer — **0**.

Coordinator-owned Root unit counter по проверенным inputs: 1/2 использован; единственный GREEN остаётся отдельным решением Root на exact final source и прежних finite limits. Этот APPROVE не переносит partial source evidence на Nix/native/import origins/full release/final CI/scientific gates. New root не наследует их по content/version equality. Platform T2/T3, trust/native/OPS03/CR04 residuals вне этого пятифайлового Root CPP.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D2 T1 exact input/full graph реализован в actual callers | solver preparation/build/CLI, application early preflight, exact JSON/SHA argv | Final GREEN и Nix assertion не исполнялись reviewer | сохранить |
| Bounded actual capture и immutable callback inputs сохранены | one-open loop/UTF8/finally, local scalars, structuredClone, causal fixtures | Нет hostile capture-race/kernel-I/O guarantee | сохранить |
| T2 guard сохраняет usernames и закрывает empty password | raw authority colon guard и literal URI fixture tables | Не secret scanner/trust enrollment | сохранить |
| R3 test semantics/F1 oracle пережили formatter | Pre-format hashes, прочитанный exact delta, formatted assertions | Ручной source review, не AST proof или GREEN | сохранить |
| ROOT-RED-1 наблюдён и все17 failures объяснены | Original complete raw+receipt и author/source mapping | RED не доказывает исправление | сохранить |
| Formatted candidate GREEN/Nix/native/science принят | Подтверждающих receipts нет | Coordinator execution/native gates впереди | дополнительно измерить |

**STOP. APPROVE exact formatted source CPP. Root решает actual source binding и sole remaining finite GREEN; reviewer не запускает дополнительные проверки.**
