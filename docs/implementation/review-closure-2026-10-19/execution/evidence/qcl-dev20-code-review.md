# DEV20 — независимый CP-CODE review

Вердикт: **PASS в пределах принятого DEV19 v2 и tiny-fixture gate**. Новых blocking findings нет. Native wheel, actual compiler/build, browser, offline/light runtime, native Nix и DEV22 этим вердиктом не приняты.

Этап: независимое read-only review исходников и предоставленного executor evidence. Сначала прочитаны root AGENTS.md, docs/architecture.md, Portal AGENTS.md, accepted owning contract и design review; затем четыре candidate source files и owning route sources. Отчёт автора прочитан после самостоятельного source/contract анализа. Reviewer не запускал target code, imports, tests, Node, npm, tsc, Vite, Nix, wheel, browser, solver или Git; source не менял. Единственная запись — этот отчёт в /tmp. HEAD/status/submodule evidence принадлежит root executor: по его binding Portal HEAD c55d0c57c8feee13ce611d45a9da67eb9e912314, docs-only над baseline b9a876aa22d84dc13435bf970728b033d1345ba8; самостоятельно Git не выполнялся согласно narrow review scope.

## Binding

Actual candidate и frozen artifacts SHA-256 независимо пересчитаны read-only:

| Артефакт | SHA-256 |
| --- | --- |
| docs/package-identity.md | dbf2d4808a84cb97d1a656532aaf4c7271598195076ce084ca62d88a36e68cc9 |
| /tmp/qcl-dev19-design-v2-review.md | 4f0aec0141c92ddd2fbd407fc7685ef77e348f305bda98da8f563465a20780a9 |
| hatch_build.py | d8393b11add6af03825f587181d32ced35bdc50d9cefd9552ad56b12f47c747f |
| frontend/tools/asset-receipt.mjs | e471dda9e68176d965b6cf560f0ae578b7f397de9083fa118caef1f5d17ae8e3 |
| frontend/package.json | dce393b2af93a6f6aa7c3189a65c0ae6b11e9245566bebcbf2a262faecb6f46d |
| tests/test_build_assets.py | c229bc16514930887abe5bc69102e8fa1156618e9bbdd6dd91c6e2320e6f1240 |
| /tmp/qcl-dev20-implementation.patch | 6c6f5e8fecfb009c67d6963ef5349621d347251f6640c1c78c072a2e68007c3d |
| /tmp/qcl-dev20-implementation-report.md | f5bd42235b1e9b085a37d25b1d0da427974a68881895050729bfb866a1181e11 |
| /tmp/qcl-DEV20-GREEN-1/receipt.json | 8578ffe2cf6f2e4d4b3014445628f938f9cd8193d0d3a30606b431c8089e0192 |
| /tmp/qcl-DEV20-GREEN-1/original.log | f34190e6a214b299ba6544405f0ecc9011e87c266f4fb374e76dbb64c43912ab |

Frozen patch headers содержат ровно четыре candidate paths выше; package.json delta меняет только scripts.build. Других source mutations reviewer не делал. Byte-for-byte применение всего patch к baseline здесь не повторялось; вывод привязан к actual file hashes и прочитанному patch.

## Независимые выводы

1. **R1 implemented.** frontend/tools/asset-receipt.mjs:84–121 выбирает только известный mode/root и проверяет layout markers; :123–168 проверяет имена, lstat/symlinks/special files/device/.git. :238–250 проверяет весь старый selected tree и source, затем удаляет и заново создаёт только selected root до первого compiler call. Старый stamp не читается и не даёт permission на adoption. Nonselected root и effective чужой outDir не выбираются для cleanup. :253–279 требует одинаковые inputs/toolchain, новый index/JS из selected root, повторную input проверку, exclusive temp + fsync + rename-last и обычную verification. Zero-exit/no-output и output только в другом root доходят до payload refusal без новой receipt. Trusted serialized filesystem limitation сохранено; защиты от concurrent filesystem replacement не заявляю.

2. **Independent wheel gate implemented.** hatch_build.py:36–98 отдельно реализует canonical JSON, duplicate/nonfinite rejection, exact key order, строгие row types, UTF-8 path ordering/uniqueness и SHA syntax. :101–147 заново читает полный recursive inventory, исключает только известные top-level dependency/output directories и ровно root stamp из outputs. :156–224 сверяет recipe, все три digest, полный input/output inventory, обязательные payload files, Node24/SemVer и TS/Vite lock versions. От stale TS/lock, changed/missing/extra assets не остаётся existence-only fallback. :227–241 вызывает gate только для noneditable wheel, без Node, rebuild или target package import. Receipt не является подписью builder или byte verification dependencies.

3. **Source-static/Nix interface retained; actual native route not accepted.** Node project mode selection :101–120 использует literal tokens как выбор известного cleanup root. hatch_build.py:139–143 делает единственный byte transform только vite.config.ts для nix-dist; :201–203 требует исходный source token в Portal config. Hook output всегда Portal static. Frontend route находится фактически в nix/frontend.nix: existing substituteInPlace, Node24 и cp -r dist/. сохранены; platform nix/application.nix:13–16 копирует весь frontend output в static, включая hidden receipt. Root ops/environment.ts:7–9 остаётся npm ci --ignore-scripts → npm run build. Hook не имитирует recursive Nix basename/cleanSourceFilter: full inventory сохраняет src/dist/entry.ts и даёт inputs refusal при missing row.

   Actual source trace: root flake.nix передаёт self.outPath как workspaceRoot в platform.lib.mkApplication; platform flake.nix вызывает mkPythonEnvironment; application.nix:5 вызывает uv2nix.lib.workspace.loadWorkspace, :8 отдельно импортирует frontend derivation из этого workspaceRoot, :22 выбирает workspace.mkPyprojectOverlay с sourcePreference="wheel", а :13–16 добавляет frontend output к package build source. Поэтому frontend source projection и package build source projection — разные стадии, и равенство видимых hook inputs нельзя выводить только из cp. В actual frontend имеются tests/api.test.ts и tests/export-selection.test.ts: они входят в полный inventory generator/hook. Owning frontend filter явно исключает только basename node_modules/dist на любой глубине и применяет cleanSourceFilter, без явного tests exclusion. Прочитанный локальный nixpkgs lib/sources.nix:43–79 также не исключает basename tests, но его exact pinned dependency identity здесь не установлена. Точный uv2nix/pyproject-nix package-source filter отсутствовал среди найденных локальных source trees; read-only попытка открыть pinned upstream sources дала cache miss. Таким образом, guaranteed current projection mismatch не установлен, и baseline native compatibility также не установлена. Если package source уже сейчас теряет frontend/tests либо иной row, это **текущий route gap с inputs refusal**, а не разрешённая совместимость и не только future C2 scenario. Native DEV22 обязан установить actual inventories обеих стадий; исправлять mismatch исключением source row из hook нельзя.

4. **CLI/environment/dependencies scope retained.** asset-receipt.mjs:169–192 отвергает inherited VITE_*/NODE_OPTIONS, требует Node24, сверяет local TS/Vite metadata с lock. :194–210 использует shell:false; :246–251 передаёт production environment и тот же process.execPath с local compiler paths. Import-only runner seam :233 не появляется в CLI; direct invocation :327–338 принимает только build/verify и выводит root из tool location. Новые dependencies или lock changes отсутствуют в patch. Остальная inherited environment остаётся явно принятой границей воспроизводимости.

5. **Mandatory controls present.** tests/test_build_assets.py:40–101 — отдельный Python receipt writer/inventory oracle; :119–128 использует actual installed Hatchling interface, не fake module. :135–226 содержит stale input/output, lock, missing/extra, rename, malformed/duplicate/noncanonical, toolchain, editable и C2 controls. :240–285 сохраняет actual production lifecycle при synthetic runner, проверяет empty selected root до tsc, no-output/misdirected/failure/mutation/unsafe outcomes. :290–368 покрывает оба modes и valid/missing/corrupt old stamps; Nix hook получает отдельный Portal fixture с восстановленным исходным config и только selected dist output. Foreign sentinel byte comparison и zero-runner unsafe check присутствуют. 19 — число test methods; nested subTests дают дополнительные cells.

6. **Light/offline source scope retained.** Изменения относятся к build metadata/verification и тестам; presentation и Vite configuration не меняются. Existing frontend/src/style.css:8 содержит color-scheme: light. Генератор не добавляет CDN, network fetch или remote theme. Это source-level отсутствие изменения требований; actual browser/offline/light acceptance остаётся отдельным DEV22 gate.

## Runtime evidence и пределы

Root executor GREEN-1 original.log содержит `19 passed in 1.54s`; receipt сообщает exit_code 0, wall 2.183 s, sampled peak process-tree RSS 115003392 bytes, sampled owned temporary peak 136369 bytes, 99 bytes полного raw capture, без guard_error/stop_reason/output overrun. Fixture hash совпадает с reviewed candidate. Prepared Node24 selection сообщена root executor; reviewer её самостоятельно не исполнял. RSS/TMP sampling не доказывает transient peak/hard quota и не измеряет explicit paths вне TMPDIR. Этот gate использует injected runner и actual Hatch hook interface; actual npm/compiler/wheel/browser/native CI не выполняются.

Новых blocking или неблокирующих дефектов, требующих изменения candidate в этом scope, не найдено. Согласие reviewer/автора не подменяет приведённые source locators и executor evidence. Независимая проверка исходников выполнена; независимого повторного runtime run не было и он не требовался narrow review поручением.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Stale source/output отвергаются независимым wheel reader | Frozen hatch_build.py:114–224; GREEN-1 reviewed fixture cases | Synthetic public fixtures; не native wheel build | сохранить |
| Старый selected payload не усыновляется после no-output/misdirected exit0 | asset-receipt.mjs:238–279; tests:240–285,352–357; GREEN-1 | Trusted serialized build tree; runner synthetic | сохранить |
| Exact mode transform и C2 fail-closed соблюдены | Exact config transform; full hook inventory; tests:217–226,320–333 | Synthetic route; actual package-source projection не установлена | сохранить |
| Текущий native Nix route даёт совпадающие frontend/hook input trees | Owning flake→application→две source стадии прослежены; frontend/tests существуют | Exact uv2nix/pyproject-nix projection и native DEV22 отсутствуют; current mismatch не исключён | дополнительно измерить |
| CLI/environment/receipt schema отвечают принятому DEV19 v2 | Независимое чтение frozen Python/Node source; hashes выше | Не подпись builder и не dependency byte verification | сохранить |
| Fixed-light/offline runtime и native DEV22 приняты | Нет соответствующего runtime evidence | Только unchanged presentation/source route observation | данных недостаточно |
