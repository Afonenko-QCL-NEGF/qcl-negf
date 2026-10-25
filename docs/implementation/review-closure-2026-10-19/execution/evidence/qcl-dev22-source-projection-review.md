# DEV22 — source projection audit выбранных pinned inputs

Наблюдение: в рассмотренном source chain не найдено исключения `frontend/tests`; все 11 текущих tracked regular frontend files проходят прочитанный filter. Решение — сохранить fail-closed asset/input contract и дополнительно измерить actual Nix/store/wheel route после admission. Это не утверждение о собранном wheel, совместимости prepared cache или native runtime.

## Identity и первичные материалы

Root при сборе `965ebed95d2b627423805d10c46d0ae8dd425e9d`, Platform `b067723c82382689bff5cc366981c56e99b926f8`, Portal `d28d076c83611278153752d94cc3729d91b32667`; последующее Portal `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d` меняет только `tests/test_api.py`, frontend тот же. Source authority — root gitlinks и `flake.lock`, не параллельный lock. Сводка `/tmp/qcl-dev22-projection-source-summary.json`, исходные REST responses и verified bytes `/tmp/qcl-dev22-projection-source/`. Прочитаны 8 GitHub primary files, 95 849 source bytes / 140 239 response bytes; для каждого повторно вычислены Git blob SHA1 (с blob header) и SHA256. Network read конечный, без eval/import/build. Недостающий helper первоначально остановил локальную подготовку до соответствующего request; затем helper исправлен, выполнено одно pinned чтение. Этот tooling failure не является native failure.

## Owning source chain

1. Root `flake.nix` передаёт `self.outPath`, submodules включены; Platform `nix/application.nix` вызывает `workspace.loadWorkspace` и `mkPyprojectOverlay`, `sourcePreference = "wheel"`.
2. [uv2nix workspace.nix:117–125](https://github.com/pyproject-nix/uv2nix/blob/a24323e9e6ecbbf305c238845ff6c612d50467c0/lib/workspace.nix#L117) вызывает `lock1.getLocalProjects`. [lock1.nix:514–570](https://github.com/pyproject-nix/uv2nix/blob/a24323e9e6ecbbf305c238845ff6c612d50467c0/lib/lock1.nix#L514) строит `projectRoot = workspaceRoot + localPath`, передаёт его `loadUVPyproject`. Отсутствующий submodule/pyproject не превращается в доказанный полноценный source.
3. [overlays.nix:139–146](https://github.com/pyproject-nix/uv2nix/blob/a24323e9e6ecbbf305c238845ff6c612d50467c0/lib/overlays.nix#L139) выбирает `build.local` для local projects, несмотря на wheel preference для remote dependencies. [build.nix:29,198–205](https://github.com/pyproject-nix/uv2nix/blob/a24323e9e6ecbbf305c238845ff6c612d50467c0/lib/build.nix#L198) использует **pyproject-nix.build.lib.renderers**.
4. Именно [build/lib/renderers.nix:34–70](https://github.com/pyproject-nix/pyproject.nix/blob/6a8a7881d75b6f98967e7b8069f4ead331384301/build/lib/renderers.nix#L34) задаёт `src = project.projectRoot` при наличии root; здесь нет дополнительного tests filter. SHA256 `6d8f53adaec8ab0c58d9a6826086d8ba4a7e6ad620d04fdf9ee1819f646818ae`. Ранее также прочитан `lib/renderers.nix`; это другой namespace, его содержимое **не** используется как свидетельство owning route. Оба оригинала сохранены.
5. Отдельный Portal `nix/frontend.nix` применяет `cleanSourceWith`: recursive basename `node_modules`/`dist` плюс pinned [nixpkgs lib/sources.nix:43–78](https://github.com/NixOS/nixpkgs/blob/f5c082a40f7571c266e74e80ae2e68aadd8a9fc7/lib/sources.nix#L43). Filter исключает VCS, editor backups, `.o`/`.so`, result symlinks, unknown type; `tests` не исключает. Platform `postPatch` копирует frontend output с hidden stamp в Portal static. Это отдельные input/source/output projections; project docs не тождественны frontend inputs.

Static inventory из `git ls-tree` Portal: index.html, package-lock.json, package.json, src/api.ts, src/main.tsx, src/style.css, tests/api.test.ts, tests/export-selection.test.ts, tools/asset-receipt.mjs, tsconfig.json, vite.config.ts. Итого11 regular files,0 из них исключены прочитанными predicate. Это моделирование имён/типов по исходникам; actual Nix/store inventory не получен.

## Ограничение и следующий gate

Nix evaluation, store source inventory, compiler/build, installed wheel/import, browser/native compatibility здесь не выполнялись. Совпадение derivation/contents/native test contract ещё не установлено; старый native output и прежний root не наследуют acceptance нового root. DEV22 в целом открыт до route-specific проверок в разрешённом конечном envelope. Новый фильтр в будущем обязан доказать совместимость asset-stamp/inputs либо fail closed; текущий static audit не основание ослаблять C2/DEV20 guard или исключать frontend tests.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Local builder сохраняет projectRoot в src на просмотренном route | Exact pinned uv2nix → build.lib.renderers source chain, verified Git blobs/SHA256 | Не actual evaluation/store | сохранить |
| Текущие frontend tests не исключены просмотренным filter | 11 tracked regular paths, predicates и pinned nixpkgs source | Только static path/type model | сохранить |
| Same-source build/import/native closure получено | Native calls0, отсутствует admission/store/wheel receipt | DEV22 полный acceptance неизвестен | дополнительно измерить |
| Physics/CI/science изменены этим аудитом | Чтение первичных исходников, product mutations0/test calls0 | Нет новых численных данных | сохранить |
