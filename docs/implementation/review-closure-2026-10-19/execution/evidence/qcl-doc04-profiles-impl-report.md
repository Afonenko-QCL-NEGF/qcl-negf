# DOC04 Core/Runner pilot profiles — source I

Реализованы только два owning `docs/make.jl`, каждый в отдельном worktree на exact selected head и ветке `codex/review-closure-docs-pilot-profile`. Нет commits/push/Root checkpoint edits. Исходный managed Root observed HEAD e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b; его unrelated dirty Platform/checkpoint/census/OPS08 состояние не исправлялось.

Frozen D1+D2+D3 и accepted D4 path contract применены совместно; hashes в identity. D4 устраняет исходный пробел owned-attempt boundary обязательным QCL_DOCS_ATTEMPT, без inferred ownership или admission. Проверки четырёх strict Linux absolute normalized paths, всех symlink ancestors, canonical existing directories, exact owner layout, absent BUILD, component containment в обе стороны, Julia1.13.0 и exact active ROOT/julia/Project.toml стоят до imports и makedocs. Дополнительно проверяется существующий regular nonsymlink root Manifest.toml из D1 locked-project contract. Metadata exceptions не подавляются.

Pilot сохраняет existing module vectors, fixed nonempty sitename, весь original pages vector, pagesonly=false, checkdocs=:exports, warnonly=false, draft=false. Explicit doctest=false/linkcheck=false применяются только pilot. HTML использует принятые pinned kwargs, fixed-light asset, mathengine=nothing; CSS не создаётся и assets не считаются проверенными по имени. Root preflight остаётся обязательным BUILD entrypoint, независимо от прямого вызова recipe. Guards не обходят staged payload tree и не устанавливают ownership/BIND/exclusivity; это явно отмечено в source comments. Unknown profile отказывает перед imports.

## Immutable output package

| Owner | Base HEAD | Modified make.jl SHA256 | Patch SHA256 |
| --- | --- | --- | --- |
| core | `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee` | `b26574d7632747feee06094ef99ce96edcc35c97d794a2f243f6921c2de3812e` | `8ec0fd22e1c46ddcac0a9abed36a361c86a3530206bd9d1b542c684d5a0a1682` |
| runner | `1acc165650fd4f4c2d49605cc679f90e3f6fcdae` | `6db896ca38bad4ac8ad6b5ba9103712d51383ca065709a1b856b25a99049f051` | `59c5354e289adf00f6a5d3a317f20c677d617c07aad9401d1e92c38a25633a64` |

Worktrees: `/tmp/qcl-doc04-core-profile-worktree` и `/tmp/qcl-doc04-runner-profile-worktree`. Separate patches: `/tmp/qcl-doc04-core-profile.patch`, `/tmp/qcl-doc04-runner-profile.patch`. Identity: `/tmp/qcl-doc04-profiles-impl-identity.json`.

## Source verification и ограничения

`git diff --check` выполнен для обоих owning diffs: exit0. Git diff name-only в каждом содержит ровно docs/make.jl. Отдельное извлечение bytes между else и final end совпало с immutable `git show BASE:docs/make.jl` в обоих случаях (original hashes и extracted hashes в identity). Original normal recipe оставлен побайтным непрерывным блоком: imports, DocMeta, navigation, doctest=true, checkdocs, warnonly, normal output/publish arguments сохранены. Exact pilot page vectors совпали с original после удаления только добавленных четырёх indentation spaces. Это byte/source comparisons, не Julia syntax/type/runtime tests.

Julia, Documenter или owning imports, Julia parsers/typechecking/tests/render/build, package setup, network и scientific runs не выполнялись. Runtime invalid/valid guard controls и fake importer/output sentinel не запускались по явной границе source-only поручения. Никакого runtime PASS нет. Независимый high CPP остаётся следующим gate; coordinator владеет owning PR/G1.

Первое создание worktrees было заблокировано read-only Git metadata sandbox; разрешённая повторная операция с sandbox escalation создала только порученные owning branches/worktrees. Это не отказ automatic approval review и не BUILD admission. Новых worktrees во время continuation не создавалось.

Read ledger `/tmp/qcl-doc04-profiles-read-ledger-prep.json`:606590 B консервативно charged до D4, плюс524288 B reserve на все continuation source/patch/final verification reads; суммарная верхняя граница1130878 B<4MiB. Раздельный continuation ≤10min/1CPU/2GiB/output96KiB; physical I/O/RSS не измерялись. Ожидание D4 было явно остановлено interim STOP, продолжено отдельным finite grant; исходный failed design resource history не переписан.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Normal recipes сохранены побайтно | Immutable git show + extracted default byte equality, hashes identity | Julia branch behavior не исполнялось | сохранить |
| Полный pilot page graph сохранён | Byte equality original/pilot vectors после indentation removal | Render/anchor checks не выполнялись | сохранить |
| Exact D4 guards добавлены до imports/output | Two owning diffs, strict Base-only branch | Runtime controls/TOCTOU не измерены | изменить |
| BUILD ownership/import/assets/source/cache/admission доказаны | Только recipe guards; внешние prerequisites сохранены явно | Guard не устанавливает эти факты | данных недостаточно |
| Готовность source I к independent CPP | Only two owning files, diff --check, hashes/patches | Независимый CPP ещё не выполнен | дополнительно измерить |

STOP: source implementation packet, без commit/PR/BUILD.
