# DEV19 — D candidate: standalone assets и import routes

Freeze: 2026-10-19 14:34 UTC. Stage: **CP-DESIGN / L-SOURCE**, candidate для
независимого high review; DEV20 READY возможен после принятия контракта.
Рабочий checkout: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Поручение: sole writer только Portal `docs/package-identity.md` и supported
build section `README.md`; no hook/config/code changes, installs/builds,
runtime imports/tests/server actions/Git mutations. Эти границы соблюдены.
Новый source-build grant для этого documentation-only этапа не нужен.

## Source и фактическое состояние

Root HEAD: `cbb24a61344a947761b6c049a6bb6687e14cff04`.
Portal HEAD: `b9a876aa22d84dc13435bf970728b033d1345ba8`.
Portal branch: `codex/review-closure-package-identity`; Portal status перед
работой пуст, после — ровно ` M README.md` и `?? docs/package-identity.md`.
PR9 merged/publication сообщён координатором; remote metadata в этой D-задаче
самостоятельно не запрашивалась. Root/gitlink publication не выполнялась.

Сняты `git rev-parse HEAD`, `git status --short` и
`git submodule status --recursive` до authoring и после freeze. Root заранее
содержал чужие modified/dirty component trees, checkpoint и untracked
execution evidence/tests. Они не редактировались этим writer.
Первоначальный recursive component source snapshot:

```text
a8d2c0de21dfdce3ed3c7c585c555656443f6d89 components/QCLNEGF.jl
0c53c6d0f68e0b25fce79388db831da6fc3ae856 components/QCLNEGFRunner.jl
5579d55684939495230241f446b7ea07c8ae0224 components/qcl-negf-aiida
26cacbe1688fee0af300d0949fc6b94e55a29f4a components/qcl-negf-contracts
6c5b11f3c74d44fed8b2c159f890b83e0b5456b9 components/qcl-negf-platform
b9a876aa22d84dc13435bf970728b033d1345ba8 components/qcl-negf-portal
b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3 components/qcl-negf-research
17574ca4c5495f74d86ed9bef51c60dea8265062 components/qcl-negf-results
```

Portal уже отличался от recorded root gitlink (leading `+`); этот writer не
обновлял gitlinks. Во время независимой работы Runner HEAD изменился на
`12e4d025948847c1b5d18ef4eb43a9934d8e20da` другой задачей. Оба прочитанных
Runner route inputs (`Project.toml`, `tools/prepare_workspace.jl`) повторно
сверены SHA-256 с immutable original `0c53c6d…`; bytes совпадают.
Source interpretation ограничена именно этими files, не новым общим Runner
acceptance. Не произведено submodule update/reset, stage/commit или ref change.

Применены root AGENTS, architecture, implementation entrypoint, canonical
role policy, Portal AGENTS/CONTRIBUTING/README и DEV19/20/21/22 cards из
`development.md` (слово taskdevelopment в handoff трактовано как task
`development.md`; отдельного taskdevelopment.md в checkout нет).
Engineering design не использует physics/results/performance skills как
разрешение новых запусков. `using-superpowers` прочитан: его Subagent Stop
применим; `brainstorming` использован для rationale и self-review конкретного
контракта. Никаких дополнительных human permission gates не добавлено.

## Первичные source inputs

Paths в таблице относительны root; `P/` означает
`components/qcl-negf-portal/`. Это derived snapshot доказательств D-прохода,
а не maintained revision lock.

| Path | SHA-256 |
| --- | --- |
| AGENTS.md | b795916b286983cc4c71ed3614bc0fb431acfc1d29974594565e71a30e66b648 |
| docs/architecture.md | 8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7 |
| docs/system/release-roadmap.md | 58c7ce6007fe13b71027a397908555138065e2b9d72da24aba588542fd0256e3 |
| docs/implementation/review-closure-2026-10-19/development.md | 494b1c487183ca02e6d19f8c571e3aeba77e0e49e467aa7655dc68eff711ad13 |
| comprehensive review RV14.md | 430c4bca1cdfa821c80feaaf8f1665243aa51c2a2ac205cb7497f1942b353c0b |
| comprehensive review fixes/RV14-asset-contract.md | bbf6479340614fe853561b9daccefb0a7512f09a544c71b9d5717ab045160daa |
| comprehensive review RV02.md | 8adcafdc418bc6101508c3d2a79fc1b89cbdc163ef0b895179495ca5fe431610 |
| comprehensive review fixes/RV02-selected-check.md | 472e83297926c45f8a21adb74fb96a374b6f7f79582335a344b4249bbaa21b45 |
| P/hatch_build.py | ea0780383d6e8ac50f65c82a1e683b5fa87cba346d075e9268a5639fe0f03d8e |
| P/frontend/vite.config.ts | dbc43d0ac27668bb6073adacc8d4cd3ac25a7c4128b9a7592cc8d1e86e10786e |
| P/frontend/package.json | 015951ea6ec7342175de3eef8ec08f97e7797837e8450abced9ca473648476c0 |
| P/frontend/package-lock.json | da6d6342c88de0c602a6157b07d7f83fd442ac35b6f63485910b6f2a2478af21 |
| P/frontend/tsconfig.json | cda8bbe5fc411a4278d6cc8b6fd92efc75414fc08cf6d4d4681ec79e5ae0cec2 |
| P/nix/frontend.nix | 2713a2c7c7f2a0b67a0614a9ded7520155fb164fa40075ea2599ef7d557ce348 |
| P/.gitignore | 73d0d60905b75b5b348651c6106a8d27d42b82a0ebabd7efc72705d3668ab711 |
| ops/release.ts | a72e6e4ff6c89333a42df8031524b966e0a718f2b3b8c3a7b1503f34499f5ba2 |
| ops/environment.ts | ac241561486efea1509d227b2640f525d64c562a7fd154ece2db4d726a5139f0 |
| pyproject.toml | 87f592f043bb3df35db25fb493694df2210d59b9773df6b84e9395fbb7ca96e2 |
| julia/Manifest.toml | a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47 |
| components/QCLNEGFRunner.jl/Project.toml | 7b014003904a20f04577a4bcb6fd865a680785453b62873fd4c5135d93ba7830 |
| components/QCLNEGFRunner.jl/tools/prepare_workspace.jl | 22f036fae56dd9fa7782c62e13cbe15b0af1b2be9662be548a0dc704c11974ed |
| components/qcl-negf-platform/nix/application.nix | 6da5caf7119ff8cfea0e7d84ff15c70efb93a6bd34abf9a9aeafbe63617eb11d |
| components/qcl-negf-results/tests/source_ownership.py | 95b2a6811c3ea10c77efcc4c64d90bc6d1ef04e529d027f5a65eb7db00d501ea |

Comprehensive review prefix:
`docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/`.
Дополнительно прочитаны RV14/RV02 source-review cards, Portal
`scripts/ci.ts`, `deno.json`, frontend index/style/API paths, root Python
sources и actual owning import-helper logic. Ни один из них не исполнен.

## Проектное решение

Выбран derived receipt с независимым stdlib hook verifier. Документ ровно
определяет filename `.qcl-negf-frontend-v1.json`, format
`qcl-negf.frontend-receipt.v1`, node CLI build/verify и экспортируемые
function signatures. `npm run build` вызывает wrapper; wrapper invalidates
stamp до TypeScript, исполняет local tsc/Vite, проверяет source/toolchain
до/после, публикует canonical JSON atomic rename последним и повторно verify.
Нет stamp-only/skip/rebuild-from-hook. Полный frontend tree inventory
исключает только top-level node_modules/dist; source `.env*`, unsafe paths
и symlinks дают отказ. Outputs перечисляются полностью, исключая только
саму receipt. Recipe/input/output digests, byte sizes, ordering, encoding и
strict schema/types перечислены; extra/missing rows и output bytes отвергаются.

Mode source-static соответствует standalone/root route. Mode nix-dist
соответствует единственной существующей outDir byte replacement; Python
hook виртуально применяет ровно её к одному input перед comparison.
Nix recipe копирует hidden receipt вместе со всем dist/. в frontend output,
platform копирует весь output в API source static. Ни Nix recipe, ни root
workflow не изменяются; их native/build evidence не объявлено полученным.
Receipt не содержит private environment dumps/absolute roots/revision pins.
Она устанавливает freshness consistency, но не cryptographic builder trust,
правильность compiler, reproducibility или scientific/browser acceptance.

Route matrix охватывает standalone wheel/editable, root workspace editable,
root release wheels, Nix frontend/application, Julia workspace, Runner
standalone Core tag и Results owning imports. Для каждой версии/import
нужны отдельно source/module/distribution/build identities. Локальный Core
v0.2.0 tag resolves `92a217a31f2d0cdec503cb8e9c162709d2a89fd8`; workspace
Core gitlink post-tag — отдельный source. Версия0.2.0 не переносит provenance.
Actual import/installed-wheel/depot/solver identities не измерялись.

## Покрытие design criteria DEV19

| Criterion | Candidate locator | D-only disposition |
| --- | --- | --- |
| Supported source→frontend→wheel flow | Решение; Единственный интерфейс; README build section | Определён |
| Exact inputs/exclusions/output hashes | Точный набор inputs и outputs; Receipt schema v1 | Определён |
| Mode/CLI/function signatures | Единственный интерфейс; Два режима одного формата | Определён |
| Build recipe and atomic publish/hook errors | Schema; Build lifecycle и fail-closed hook | Определён |
| Stale TS/lock/index+JS, missing/corrupt output, incomplete receipt | Hook rules; Приёмка DEV20 | Обязательные future synthetic cases |
| Editable bypass без release claim | Hook branch; route matrix; README | Явно сохранён |
| Root/Nix controls | Mode transform; root/Nix route matrix и existing copy semantics | Только source compatibility |
| Version не переносит owning-import evidence | Route matrix; required Python/Julia fields | Определён |
| Light/offline/no CDN; no secret/revision lock | Решение; schema; Приёмка DEV20 | Инварианты сохранены |

## Выполненные проверки и точные ограничения

- `git diff --check` в Portal: exit0, diagnostics пусты.
- `git diff --no-index --check /dev/null docs/package-identity.md`: exit1,
  diagnostics пусты; no-index обнаруживает новый отличный файл. Это не
  runtime/test failure и не подтверждение выполнения кода.
- `rg -n '[[:blank:]]+$' README.md docs/package-identity.md`: exit1, совпадений
  нет; trailing whitespace не найден.
- README relative link к docs/package-identity.md и все четыре actual
  Python module paths из route record проверены `test -f`; files существуют.
- Candidate self-review: missing schema/placeholder/незаданный mode не
  оставлены. Добавлены exact scripts.build/no prebuild/postbuild и явный
  отказ cleanup при unsafe paths; source/env inputs не объявлены zero.
- Фактический component status после freeze содержит только два разрешённых
  doc files. Сняты hashes и `cmp` с frozen copies: оба exit0.
- No actual frontend/wheel/Nix build, npm install, dependency refresh,
  hook/module/runtime import, tests, profiler, solver, full suite, CI,
  browser/server, Git mutations или publication. Numeric checks не выполнялись.
- Existing INT01 generated assets и единственный прежний passing 404 assertion
  не использованы как freshness/wheel acceptance evidence.

Независимый review ещё не выполнен этим writer. Parent выдаёт immutable
candidate + primary sources high reviewer, затем решает CP-DESIGN acceptance
и DEV20 READY. Medium implementation не начинается автоматически этим report.
Дорогой BUILD stage отдельно; отсутствие source-build grant не является
blocker завершённого документационного D-stage.

## Frozen candidate artifacts

| Artifact | SHA-256 |
| --- | --- |
| P/README.md = /tmp/qcl-dev19-README.md | 2c37cb053f0f36024249ceaeb9c0cb0b71d4415319295ecf56c9f2e9981b5ae3 |
| P/docs/package-identity.md = /tmp/qcl-dev19-package-identity.md | d59be5f43d72d1604bc29ca962d9eb375f17c0a26066974d19caac730279bb59 |
| /tmp/qcl-dev19-design.patch | 249aa32eac06e8e83f456e4ff5ddf565b04c702e1985ed25701b562b8532f564 |

Patch ниже — полный reviewable diff двух файлов, без stage/commit.

```diff
diff --git a/README.md b/README.md
index 254dc8f..d5a7dbf 100644
--- a/README.md
+++ b/README.md
@@ -162,7 +162,19 @@ python3 -m unittest discover -s tests -p test_ci_environment.py
 It checks argument order, working directory, the explicit environment and exit propagation
 without installing packages, contacting a registry or building frontend assets.
 
-`npm run build` writes assets to `src/qcl_negf_api/static/`, which the wheel includes. Release wheel construction rejects missing browser assets. Editable development installation permits the API to run before the browser is built. Generated assets and dependency directories are ignored by Git. `nix/frontend.nix` builds browser assets with the verified npm dependency hash committed alongside the recipe. The platform uses this derivation when building the API wheel from the same root `uv.lock`; Python dependencies are not declared again in a separate Nix package definition. After updating `frontend/package-lock.json`, run `deno task lock:nix` in the Nix development shell to regenerate `nix/generated-npm-hash.json`; do not edit its hash manually.
+`npm run build` writes assets to `src/qcl_negf_api/static/`, which the wheel includes. The current release hook rejects missing index/JS files; it does not establish that existing assets match the current TypeScript, lock or build recipe. For a standalone source checkout with prepared locked dependencies, build the frontend immediately before the wheel:
+
+```console
+npm --prefix frontend ci --ignore-scripts
+npm --prefix frontend run build
+uv build --wheel --no-sources --out-dir dist
+```
+
+These are build-stage commands; dependency preparation and build cost need their own admission. Retain the exact source/lock identities and wheel SHA-256. The proposed [package identity contract](docs/package-identity.md) specifies the DEV20 generated receipt and fail-closed stale/output checks. Its generator and stronger wheel guard are not implemented by this documentation change. Until that implementation and route-specific verification exist, a successful direct wheel build alone is not source-freshness evidence.
+
+Editable development installation permits the API to run before the browser is built and makes no release browser-asset claim. Workspace editable imports, standalone wheels/editables, Julia Core tag/path resolution and Nix closures require separate source/import receipts; the shared `0.2.0` version does not transfer acceptance. The package identity document defines the required fields and boundaries.
+
+Generated assets and dependency directories are ignored by Git. `nix/frontend.nix` builds browser assets with the verified npm dependency hash committed alongside the recipe, replacing only Vite's output directory with `dist`. The platform copies that complete output into the API wheel build from the same root `uv.lock`; Python dependencies are not declared again in a separate Nix package definition. The proposed receipt has an explicit `nix-dist` mode for this existing transform; its native acceptance is separate from the standalone route. After updating `frontend/package-lock.json`, run `deno task lock:nix` in the Nix development shell to regenerate `nix/generated-npm-hash.json`; do not edit its hash manually. Root release construction continues to call its own frontend build before packaging. All routes retain local same-origin assets and the fixed light theme.
 
 For local browser development run the API on port 8080 and `npm --prefix frontend run dev`; Vite proxies `/api` to the local API. Production serves the built files directly; it does not run the Vite development server.
 
diff --git a/docs/package-identity.md b/docs/package-identity.md
new file mode 100644
index 0000000..add4640
--- /dev/null
+++ b/docs/package-identity.md
@@ -0,0 +1,301 @@
+# Package identity: frontend receipt и маршруты импорта
+
+Статус: **DEV19, проект контракта для независимого review**. Этот документ
+задаёт интерфейс DEV20; генератор и проверка ниже ещё не реализованы.
+Он не разрешает install, build, import, tests, CI или deploy. Фактический
+baseline Portal — `b9a876aa22d84dc13435bf970728b033d1345ba8`.
+`hatch_build.py::CustomBuildHook.initialize` сейчас проверяет только наличие
+`static/index.html` и хотя бы одного `static/assets/*.js`; editable обходит
+эту проверку. Наличие этих файлов не устанавливает source freshness.
+
+## Решение и граница утверждения
+
+Поддерживаемый release wheel строится из полного исходного checkout Portal
+с подготовленными locked JS dependencies: штатный `npm run build` создаёт
+bundle и derived receipt; wheel hook независимо сверяет source inputs и
+каждый output byte. Прямой wheel build не запускает npm автоматически и
+отказывает при отсутствии подходящей receipt. Editable остаётся отдельным
+API development route, без утверждения о release browser assets.
+
+Выбран receipt вместо безусловной сборки из wheel hook: hook работает без
+Node/network, а root release и Nix сохраняют собственные build stages.
+Одно обязательное «сначала собери frontend» без проверки не различает старый
+bundle рядом с изменённым TS. Повторная сборка внутри hook увеличила бы
+стоимость и скрыла переход этапа. Receipt — generated artifact, полностью
+попадает под существующий ignore `src/qcl_negf_api/static/`; Nix `dist/`
+также ignored. Его не коммитят и не редактируют вручную.
+
+Receipt устанавливает соответствие заявленных текущих inputs, recipe и
+предъявленных output bytes. Это не подпись builder, не защита от злонамеренного
+изготовления согласованных JSON и bytes, не доказательство корректности
+транслятора, bitwise reproducibility, browser acceptance или научной приёмки.
+Происхождение dependency installation и доверие builder задаёт отдельный
+build receipt. Gitlinks остаются authority компонентных ревизий; ещё один
+maintained revision lock не вводится.
+
+## Единственный интерфейс генератора
+
+DEV20 добавляет `frontend/tools/asset-receipt.mjs` без новых dependencies.
+Из Portal checkout поддерживаются ровно следующие CLI; показанные команды
+являются будущим интерфейсом, а не результатом выполненной здесь проверки:
+
+```console
+node frontend/tools/asset-receipt.mjs build
+node frontend/tools/asset-receipt.mjs verify
+```
+
+Скрипт определяет frontend root по собственному `import.meta.url`, независимо
+от cwd. Нет опций output/source root, stamp-only, skip-check или environment
+bypass. Неизвестные аргументы дают nonzero. Экспортируемые функции для
+synthetic fixtures: `buildFrontend(frontendRoot: string): Promise<void>` и
+`verifyFrontend(frontendRoot: string): Promise<void>`. Аргумент fixture не
+является production CLI override. В `frontend/package.json` только script
+`build` меняется на `node tools/asset-receipt.mjs build`; script `check`,
+test и Deno command/environment contract остаются прежними.
+Generator и hook требуют именно это значение `scripts.build` и отсутствие
+`prebuild`/`postbuild`: дополнительные lifecycle commands не входят в v1
+recipe. Импорт самого tool module не запускает CLI; CLI выполняется только
+при direct invocation.
+
+Build исполняет последовательно local TypeScript и Vite через тот же Node:
+
+```text
+node node_modules/typescript/bin/tsc --noEmit
+node node_modules/vite/bin/vite.js build --mode production
+```
+
+cwd обеих команд — frontend root; shell и глобальные `tsc`/`vite` не нужны.
+Child environment задаёт `NODE_ENV=production`. Наличие inherited `VITE_*`
+или `NODE_OPTIONS`, либо source `.env`/`.env.*`, отвергается до build:
+тайные или неучтённые browser inputs не становятся частью этого контракта.
+Остальная среда builder не записывается в frontend receipt. Её происхождение
+и возможное влияние остаются ограничением воспроизводимости, включая Nix.
+Node.js 24 — поддерживаемый reference builder; npm, TypeScript и Vite берутся
+из подготовленного окружения. `npm --version` только читает версию; build не
+исполняет `npm ci`, install, fetch, Python import или solver.
+
+## Два режима одного формата
+
+| `mode` | Effective Vite outDir | Source для проверки wheel hook |
+| --- | --- | --- |
+| `source-static` | `../src/qcl_negf_api/static` | Полные реальные bytes `frontend/` в Portal checkout |
+| `nix-dist` | `dist` | Те же inputs, но для `vite.config.ts` применяется ровно существующая Nix замена ниже |
+
+Build определяет режим по `vite.config.ts`: должна присутствовать ровно одна
+literal byte sequence `../src/qcl_negf_api/static` в source-static либо
+ровно один `outDir: "dist"` и ни одной первой sequence в nix-dist. Остальные
+outDir/config variants отвергаются до записи. Для nix-dist hook требует в
+своём исходном config ровно одну `../src/qcl_negf_api/static` и заменяет её
+bytes на `dist` перед хешированием **только этого файла**. Это точная
+`substituteInPlace --replace-fail` из `nix/frontend.nix::postPatch`, а не
+общая нормализация source/config. Generator хеширует реальные patched bytes;
+receipt различает режимы и сохраняет effective recipe. Других transforms нет.
+
+В wheel оба режима проверяют один и тот же физический
+`src/qcl_negf_api/static/`: `output_root` ниже описывает место генерации,
+а не разрешённый произвольный путь чтения. Nix копирует весь `dist/.` в
+frontend output, затем platform копирует весь `${frontend}/.` в static,
+включая receipt. Mode не даёт bypass input/output verification.
+
+## Точный набор inputs и outputs
+
+Input paths — относительные POSIX paths от frontend root. Рекурсивно
+включаются **все** regular files, в том числе hidden files, `tests/`,
+`tools/asset-receipt.mjs`, `package.json`, `package-lock.json`, `index.html`,
+`tsconfig.json`, `vite.config.ts`, весь `src/` и будущий `public/`.
+Только две top-level директории исключаются целиком: `node_modules/` и
+`dist/`. Отсутствующие optional directories не добавляются фиктивными rows.
+Для build обязательны перечисленные шесть root/build files (включая tool)
+и `src/main.tsx`; остальные rows выводятся из фактического дерева.
+
+Symlinks, special files, непредставимые UTF-8 имена и `.env`/`.env.*` в
+перечисляемом дереве дают отказ. Имена не нормализуются. Исключённые
+dependency/output директории не обходятся. `.git`, backend `src/`, root
+`uv.lock`, Nix recipe и private inventory находятся **вне frontend root**:
+они не заявлены frontend inputs; их identities принадлежат внешнему route
+receipt. Любой новый build input вне frontend, кроме locked dependencies,
+требует изменения этого контракта до поддержки такого build.
+
+Output rows — все regular files рекурсивно от effective output root,
+за исключением ровно `.qcl-negf-frontend-v1.json` в его корне. Иных exclusions
+нет: CSS, JS, maps, fonts, images, hidden files также хешируются. Обязательны
+непустые `index.html` и хотя бы один непустой `assets/*.js`. Symlinks и special
+files отвергаются; лишний файл, включая оставшийся temporary receipt,
+не может быть молча проигнорирован. Перенос всего output tree в wheel
+сохраняет относительные output paths и bytes.
+
+В каждом inventory row ровно `path`, `bytes`, `sha256` в этом порядке.
+`bytes` — точная длина файла, JSON integer 0…9007199254740991 (не boolean).
+SHA-256 — 64 lowercase hexadecimal characters от raw bytes. Paths непустые,
+относительные, с `/`; запрещены `\`, NUL/control characters, пустые segments,
+`.` и `..`. Rows уникальны и отсортированы по unsigned UTF-8 bytes path.
+Добавление, удаление и переименование файла меняет inventory.
+
+## Receipt schema v1
+
+Файл — `<output-root>/.qcl-negf-frontend-v1.json`. Объекты имеют ровно поля
+таблицы в указанном порядке; unknown/missing fields, duplicate JSON keys,
+NaN/Infinity и неверные types отвергаются. JSON canonical encoding:
+UTF-8 без BOM, компактные separators `,` и `:`, без ASCII escaping Unicode,
+обычное JSON escaping строк, без trailing spaces; файл оканчивается одним
+LF. Reader проверяет совпадение bytes с этой canonical формой. Саму receipt
+её output inventory не хеширует; её bytes связывает внешний wheel hash.
+
+| Поле | Точное значение / тип |
+| --- | --- |
+| `format` | `"qcl-negf.frontend-receipt.v1"` |
+| `mode` | `"source-static"` либо `"nix-dist"` |
+| `recipe` | Объект с полями `id`, `commands`, `output_root`, `node_env` |
+| `recipe_sha256` | SHA-256 canonical JSON bytes объекта `recipe`, без LF |
+| `toolchain` | Объект с полями `node`, `npm`, `typescript`, `vite`; точные непустые version strings |
+| `inputs` | Полный непустой массив input rows |
+| `inputs_sha256` | SHA-256 canonical JSON bytes массива `inputs`, без LF |
+| `outputs` | Полный непустой массив output rows |
+| `outputs_sha256` | SHA-256 canonical JSON bytes массива `outputs`, без LF |
+
+`recipe.id` равен `"qcl-negf.frontend-build.v1"`; `commands` — ровно
+`[["node","node_modules/typescript/bin/tsc","--noEmit"],
+["node","node_modules/vite/bin/vite.js","build","--mode","production"]]`.
+`output_root` равен `"../src/qcl_negf_api/static"` для source-static и
+`"dist"` для nix-dist; `node_env` равен `"production"`.
+Изменение recipe вне этих двух вариантов требует нового format/контракта.
+Input hashing включает bytes package script и самого generator, поэтому
+изменение реализации recipe также делает прежнюю receipt stale.
+
+`toolchain.node` берётся из `process.versions.node` (24.x.y), `npm` — из
+единственной version line успешного `npm --version`; обе строки — SemVer
+без `v`. TypeScript и Vite версии читаются из local `node_modules` package
+metadata и должны совпадать с соответствующими `packages["node_modules/…"]`
+в текущем `package-lock.json`. Те же версии сверяются после build. Hook
+проверяет structure/version constraints и совпадение TS/Vite с lock без
+запуска Node. Это не byte verification dependency directory: integrity
+locked installation подтверждает внешний build route, не поле version.
+Receipt не содержит timestamps, usernames, абсолютных paths, Git revision
+списков, environment dumps, credentials или приватных site values.
+
+## Build lifecycle и fail-closed hook
+
+1. Build проверяет безопасность двух известных generated root paths и
+   удаляет прежнюю receipt в обоих (`static` и `frontend/dist`) **до**
+   source/config validation и TypeScript; затем определяет mode.
+   Отсутствующий root не создаёт. Ошибка удаления или unsafe root — отказ;
+   после такого отказа предыдущий build log не становится новым success.
+   Параллельные frontend/wheel builds одного дерева не поддерживаются;
+   build owner сериализует доступ.
+2. Сохраняет input inventory и toolchain до запуска. Исполняет tsc, затем
+   Vite; первый failure прекращает процесс с исходным nonzero, без retry.
+   Vite сохраняет `emptyOutDir: true`; источник assets не дополняется CDN.
+3. Снова получает inputs/toolchain и требует полного равенства до/после.
+   Снимает полный output inventory, ещё раз проверяет inputs перед publish.
+   Неопределённый/изменившийся source и неполный output дают отказ.
+4. Записывает canonical receipt во вновь созданный temporary regular file
+   того же output directory с exclusive create, flush и fsync; atomic
+   rename публикует финальное имя последним (directory fsync там, где
+   поддержан). До rename ready receipt отсутствует. После rename выполняет
+   обычную verify; failure удаляет финальную receipt. Cleanup при любой
+   ошибке пытается удалить собственный temp/final stamp; невозможность
+   удаления отражается дополнительным diagnostic, не заменяя исходную
+   ошибку. Не удаляет файлы через unsafe root/symlink. Это
+   atomic publication receipt; весь output tree не заявлен atomic snapshot.
+
+Node `verify` только читает inferred output root и применяет те же schema,
+inventory и mode правила; оно не пересоздаёт stamp. Wheel hook использует
+независимую stdlib Python реализацию
+`verify_frontend_assets(portal_root: Path) -> None` в `hatch_build.py`:
+
+- При `target_name != "wheel"` либо `version == "editable"` сохраняет
+  существующий return. Editable не читает stamp и не выдаёт release claim.
+- Для остальных wheel читает полный Portal frontend source и static;
+  применяет только разрешённый mode transform, заново хеширует input и
+  output inventories, проверяет их точное равенство receipt и три digest.
+  Не вызывает Node, Git, target package import, AiiDA, services или network.
+- Missing source/payload/receipt, malformed receipt, неизвестный mode/schema,
+  incomplete inventory, stale input/recipe, changed/missing/extra output,
+  symlink и I/O error дают `RuntimeError` до упаковки. Не fallback к старому
+  existence-only guard, не auto-rebuild, не `skip/pass`.
+
+Сообщение hook имеет вид
+`QCL_FRONTEND_RECEIPT_INVALID:<reason>; run npm --prefix frontend run build with prepared locked dependencies`.
+`reason` выбирается из `missing`, `schema`, `mode`, `inputs`, `recipe`,
+`outputs`, `toolchain`, `unsafe-path`, `io`; diagnostics могут назвать
+относительный публичный file path, но не прочитанные contents/private env.
+CLI verify возвращает 0 только после всех проверок, при отказе — nonzero
+с тем же reason. Наличие старого успешного log не меняет результат.
+
+## Поддерживаемые маршруты и отдельные identity receipts
+
+| Route | Source/dependency selection | Нужное различающее evidence |
+| --- | --- | --- |
+| Standalone Portal wheel | Полный Portal source checkout, native package metadata, JS lock; frontend build → direct wheel без workspace source overrides | Source commit/dirty state, lock hash, frontend receipt hash, wheel filename/SHA-256 и проверка exact wheel static inventory |
+| Standalone Portal editable | Явный абсолютный editable source root; Python dependencies из согласованного wheel set или явно названных editable owners | Actual import paths и distribution metadata; browser assets могут отсутствовать, release asset identity не заявляется |
+| Root Python workspace editable | Root gitlinks и `pyproject.toml::tool.uv.sources`, generated root `uv.lock` выбирают Contracts/Results/AiiDA/Portal | Каждый actual import должен принадлежать выбранному component `src`; editable и wheel receipts различаются |
+| Root release wheels | `ops/release.ts` вызывает `ops/environment.ts::frontendBuild`: `npm ci --ignore-scripts`, `npm run build`; затем locked sync и `uv build --no-sources`; source graph проверяется повторно | Source-static receipt внутри Portal wheel, четыре wheel hashes и derived release manifest; root workflow здесь не изменяется |
+| Nix frontend/application | `nix/frontend.nix` cleanSource frontend без node_modules/dist, native lock + generated npmDepsHash, Node24, точная outDir patch; platform `nix/application.nix` копирует frontend в API build | Nix-dist receipt и static bytes в wheel/application, exact derivation, output store paths/narHashes, root Git source graph и flake inputs; version assertions не заменяют эти hashes |
+| Julia workspace | Root `julia/Manifest.toml` имеет paths на Core и Runner; Runner `tools/prepare_workspace.jl` делает `Pkg.develop` обеих выбранных component paths | Actual `pathof(QCLNEGF)`/`pathof(QCLNEGFRunner)`, UUID/version, active project/manifest hash и выбранные source commits/dirty bytes |
+| Runner standalone | Runner `Project.toml::[sources]` выбирает Core URL + `rev="v0.2.0"`, compat `=0.2.0`; конкретное разрешение устанавливает созданный Pkg manifest | Resolved Core commit/tree из manifest/depot плюс actual pathof; workspace Core post-tag не подменяет этот route |
+| Results standalone/workspace | Results требует Contracts `0.2.0`; existing `tests/source_ownership.py` выбирает sibling Contracts, явный абсолютный `QCL_NEGF_TEST_CONTRACTS_SOURCE` или distribution file owner | Expected и actual `state.py`/`artifacts.py` owners совпадают; wheel SHA и source bytes отдельны от location/version guard |
+
+Frontend receipt переносится целиком между build output и wheel только с
+совпадающими проверенными inventories; root/Nix build не наследуют native
+acceptance друг друга. Наличие прежнего static tree, HTTP 200 или одного
+старого passing/missing-asset assertion не доказывает freshness и wheel
+acceptance. Sdist сам не даёт release asset claim; wheel из неполного sdist
+без полного frontend source/receipt обязан отказаться.
+
+Внешний import/build evidence record для **каждого route/attempt** содержит
+`route`, `attempt_id`, `status` (`measured`, `not_measured`, `failed`), exact
+command и result/log hash; selected root/component HEAD, dirty diff hash и
+gitlink comparison; hashes package metadata/native locks; build artifact
+identity либо явное `not_measured`. Это derived evidence, не maintained lock.
+Python record также содержит `sys.executable`, `sys.version`, resolved
+module `__file__` и его SHA-256 для `qcl_negf_api.api`,
+`aiida_qcl_negf.service`, `qcl_negf_results.state`,
+`qcl_negf_contracts.artifacts` по применимости; для каждой distribution —
+name/version, metadata location, `direct_url.json` при наличии и declared
+`RECORD` owner. Отсутствие metadata/direct_url записывается явно, а actual
+path сравнивается с независимо выбранным expected owner. Wheel route
+дополнительно хранит trusted wheel SHA-256 и сравнение installed bytes с
+его RECORD; RECORD без trusted artifact не доказывает происхождение.
+
+Julia record дополнительно содержит Julia version/executable, active
+project, manifest SHA, UUID/version/pathof обоих модулей, resolved Pkg
+commit/tree/path и source dirty state; sysimage/solver executable hash,
+derivation и native test-contract identity либо `not_measured`.
+В публичный отчёт не копируют personal absolute roots; private raw receipt
+сохраняет точные paths, публичный locator использует named source/artifact
+root и относительный path с hash. Expected owners не задаются личными
+hardcoded `/home/...` constants.
+
+Одна строка `0.2.0` не разрешает перенос import/test evidence. В прочитанном
+source Core tag `v0.2.0` указывает на `92a217a31f2d0cdec503cb8e9c162709d2a89fd8`,
+а selected workspace gitlink — post-tag; фактическую ревизию конкретного
+execution выводят из его Git/Pkg evidence, а не переписывают этим документом.
+Новый root HEAD получает свой evidence scope. Повторное использование
+native output требует одновременного совпадения derivation, contents и
+native test contract; научная приёмка остаётся самостоятельным gate.
+
+## Приёмка DEV20 и отложенные измерения
+
+Synthetic public directories должны различить healthy receipt/payload,
+изменённый TS при старом index/JS, изменённый lock, missing asset, изменённые
+output bytes, лишний output, malformed/incomplete receipt и input rename.
+Отдельно проверить отсутствие receipt после failing TypeScript/build и
+editable bypass без release claim; оба mode требуют positive/negative
+inventory controls. Это tiny fixture tests без npm install/реальной сборки.
+Не подменять отсутствие Hatchling fake module как доказательство native hook.
+
+Source-wise compatibility проверяется по сохранённым root frontendBuild,
+Nix outDir substitution и копированию `dist/.`/`${frontend}/.`. Native wheel
+contents/import/HTTP/light/offline acceptance принадлежит отдельному DEV22
+с подготовленными BUILD artifacts. Никакой CDN, remote theme или automatic
+dark mode не вводится: весь web остаётся `color-scheme: light` и работает
+из локального same-origin bundle. Offline runtime проверяется отдельно от
+доступа к registries при cold-source bootstrap.
+
+| Утверждение | Свидетельство | Ограничение | Решение |
+| --- | --- | --- | --- |
+| Existence-only guard оставляет stale-assets gap | Baseline `hatch_build.py::CustomBuildHook.initialize` | Негативный native wheel здесь не запускался | изменить |
+| Receipt задаёт проверяемую связь source/recipe/output | Поля, inventories и fail-closed lifecycle выше | Это проект DEV19, implementation/fixtures ещё нет | изменить |
+| Root и Nix имеют отдельные supported build routes | `ops/release.ts`, `ops/environment.ts`, `nix/frontend.nix`, platform `nix/application.nix` | Native derivation/wheel/import receipt не измерены | сохранить |
+| Same version не устанавливает imported source | Runner tag/path routes; Results owning-import guard | Actual runtime paths здесь не читались через import | дополнительно измерить |
+| Freshness/wheel/browser/scientific acceptance ещё не установлены | Только source и documentation review | Build/runtime/offline/light native checks — `not_measured` | данных недостаточно |
```

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| DEV19 даёт конкретный candidate contract для DEV20 | Frozen два doc files и полный patch; exact schema/mode/CLI/lifecycle | Независимое принятие ещё ожидается | изменить |
| Existing existence-only hook не доказывает source freshness | b9a876a:hatch_build.py::CustomBuildHook.initialize; RV14 F14.1 | Native stale wheel не строился | изменить |
| Root/Nix routes source-wise совместимы с предложенным интерфейсом | Unchanged npm run build entrypoint, exact Nix transform и complete copy | Native receipts/import/browser acceptance not_measured | дополнительно измерить |
| Version0.2.0 не устанавливает тождество source/imports | Runner Project/Manifest routes; Results owner-helper; Core tag object | Actual runtime identities не измерены | сохранить |
| Full release/scientific acceptance этим D-stage не получены | Только source/doc checks; no runtime execution | Native/CI/offline/light/science outcomes not_measured | данных недостаточно |
