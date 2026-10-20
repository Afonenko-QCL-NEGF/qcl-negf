# DOC04 private attempt/path clarification — independent high CP-DESIGN

**PASS_SOURCE.** Узкий внутренний path/layout contract достаточно конкретен для medium profiles I и согласован с D1–D3. Blocking findings не найдены. Он не устанавливает ownership, technical BIND, payload closure или BUILD admission; соответствующие Root prerequisites остаются обязательными.

## Frozen identity и первичные источники

| Input | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc04-profile-path-contract.md`,15261 B | `ec7717494878fbec813fe89c1ded0c5c43dcbeb6942271d0ef8d113445f5a935` |
| `/tmp/qcl-doc04-profile-path-contract-identity.json`,3682 B | `d95de918d51e282662dfa1359f678ccb292692143bae71dc582a0530a230d376` |
| prior D3 | `960a639dd281d7a5b99c582f2c9dc8b17e816715753557791460ebcef1159aee` |
| accepted prior D3 R | `7db5ad18c7c9e197fb0430422b917228ddc0216f90c0cdfb37f78ee80e9a4211` |
| prepared Julia `base/path.jl`,20779 B | `5841d139f073104fa289aa02bb945d57dfb4f811917ba113902a331219a5159e` |
| prepared Julia `base/stat.jl`,20187 B | `3811d5d926879a5727ae0ad1f189045b7ab9d03cb758f2693d5246b3f2d30e46` |
| prepared Julia `base/initdefs.jl`,20392 B | `e3ae82d7cbe446a0ef763fda526e91dd851306803398cbb7d6937990b54892ba` |

Prepared Base source root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/.build/julia/share/julia/base`. Root сообщил existing Julia1.13.0 binding с executable SHA `02618fb870c4b0f35976837605b39026b55ed998fc51dfe1edb95ae928c85d4f` и archive SHA `8975da61c128a5e5ded3e719e868da8c8781deb7ad7913d37fb99be02a81904b`; reviewer проверил названные Base source bytes, **не** запускал executable и не повторял binary/archive verification. Полный install inventory не читался.

Actual managed Root HEAD `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`; Coree431609, Runner1acc165. Unrelated dirty Platform/Contracts/checkpoint state сохранён; Gitlinks остаются authority. Этот review не является новым source-graph/whole-release acceptance и не обновляет компоненты.

## Layout/guard — конкретность и совместимость

`QCL_DOCS_ATTEMPT` однозначно связан с существующим Root `--attempt-directory DIR`; owner literal закреплён recipe. Для каждого owner source равен ровно `ATTEMPT/stage/<owner>/src`, build — ровно `ATTEMPT/raw/<owner>`. ATTEMPT и ROOT разнесены в обе стороны. Root создаёт fresh attempt/stage/raw перед recipe; recipe видит existing parents и **отсутствующий текущий owner BUILD**. Success/failed raw outputs сохраняются; retry требует новый attempt, а не очистку старого каталога. Existing outputs других owners внутри того же последовательного attempt разрешены.

Это устраняет прежнее неопределённое «owned attempt root» без нового public selector, owner environment switch, schema или registry. Core/Runner default branch при unset/empty profile сохраняет существующие imports/doctests. Unknown nonempty profile отказывает до импорта; operator pilot-only. D3 `Module[]` и три точных sitename не меняются. Absolute SOURCE/BUILD совместимы с ранее принятым Documenter kwargs contract; никакого нового Documenter API не требуется.

Primary Base compatibility подтверждена source-only:

| Predicate | Prepared Base locator | Следствие для I |
| --- | --- | --- |
| Component containment | `path.jl:258–275`, `splitpath` возвращает компоненты с root | Prefix `/tmp/a` против `/tmp/ab` нельзя сравнивать строковым startswith; явный sequence-prefix predicate реализуем |
| Exact normalized spelling | `path.jl:390–421`, normpath убирает . и .., но сохраняет directory suffix | Дополнительный явный trailing-slash/repeated-slash/dot-component rejection в контракте необходим и верен; не полагаться на normpath alone |
| Existing-path canonicalization | `path.jl:498–515`, realpath через libuv и error при nonexisting/error | realpath применим к existing ROOT/ATTEMPT/SOURCE/raw parent; для absent BUILD используется canonical parent + literal owner |
| Symlink including dangling leaf | `stat.jl:202–204,465,590`, islink использует lstat | Ancestors должны проверяться по одному; `ispath(BUILD)||islink(BUILD)` не теряет dangling symlink |
| Access/metadata failure | `stat.jl:184–205,374–383`, errors кроме описанных absent/invalid cases не превращаются в existing success | Контракт требует fail-closed на metadata/canonicalization error; не оборачивать его в permissive catch/fallback |
| Selected active Project file | `initdefs.jl:331–352`, Base.active_project возвращает путь либо nothing | Guard должен отдельно проверить ordinary nonsymlink ROOT/julia/Project.toml и exact canonical equality, отклонить nothing; это path observation, не dependency/toolchain proof |

Все эти routines находятся в Base, сторонние path packages/owning includes не нужны. VERSION1.13.0 check остаётся до Documenter/Core/Runner imports. Path guard сам не создаёт/чистит BUILD и не читает receipt/marker как разрешение.

## Authority и payload не подменены путями

Контракт правильно разделяет ограниченную read-only metadata проверку recipe и обязательный Root preflight. Recipe проверяет весь existing ancestor chain, exact tuple, canonical equality и отсутствие текущего output. Это не inventory содержимого SOURCE. Root отдельно должен finite-обходом staged payload отклонить все внутренние symlink/special-file entries, bind paths/bytes/hashes/source effects и подтвердить full selected source scope. Успешный ancestor guard нельзя засчитать как такой tree check.

Ownership/permissions/exclusive namespace, actual source graph/recipe/toolchain/cache/import/effect identity, assets/license closure, fresh BUILD admission и конечный resource envelope остаются внешними gates **перед каждым dispatch**. Если общий admission охватывает последовательные owner steps, он должен всё ещё удовлетворять своим predicates; path contract не создаёт новых human approval циклов и не разрешает отождествить env или caller boolean с BIND.

TOCTOU/concurrent replacement, bind mounts/hardlink aliases и hostile filesystem не заявлены защищёнными. Это внутренний контракт для уже admitted/exclusive namespace; отсутствие exclusivity блокирует зависимый BUILD. Прошедший direct recipe guard сам по себе не авторизует imports/render. Private absolute paths остаются в existing private attempt/inputs/steps receipt и не экспортируются в public bundle. Никакого native/pass/release статуса из имени каталога не выводится.

Перечень future source-I controls различает missing/relative/non-normalized paths, wrong owner, existing output/file/dangling link, symlink ancestor, overlap, lexical prefix trap и wrong project до fake importer/output sentinel. Valid control проверяет guard tuple без real imports/render; payload symlink negative принадлежит Root staging preflight. Это конкретный I handoff, но сами controls здесь не исполнялись.

## Ledger и пределы

Envelope≤10min/1CPU/1GiB/read2MiB/output32KiB. Каждый named source extract/search/hash заряжен консервативно по полному размеру файла, анализ повторно использовал tool/context cache.

| Read group | Upper bound B |
| --- | ---: |
| Contract+identity text, их SHA pass, D3/R hashes | 52003 |
| Named runtime metadata/recipe identity search | 6790 |
| Первичный поиск APIs в `/usr/share/julia/base/{path,file,loading,stat}.jl` | 276892 |
| Prepared named path/stat/initdefs API search | 61358 |
| Prepared selected extracts + SHA pass | 122716 |
| **Total** | **519759** |

Первичный `/usr/share` probe не был связан с exact prepared runtime; он **не использован как binding evidence**, его reads всё равно учтены. Primary API conclusion основан на названном prepared source и hashes выше. Directory/path/Git metadata и собственные review artifacts отдельно; physical I/O/RSS не измерены. Не читались large install inventory, научные данные или execution subtree payloads.

Reviewer target execution/Julia/import/parser/tests/build/network/server/children/product edits/Git mutations/checkpoint/C08/science —0. Original broad read failure сохраняется; этот отдельный clarification review не превращает его в retrospective PASS.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Layout и before-import guard достаточно конкретны | Exact four inputs/owner tuples и Base source locators | Implementation/control execution ещё впереди | сохранить |
| D3/default/retention/source scope не меняются | Узкий contract override и frozen D3/R hashes | Не global re-audit recipes | сохранить |
| Guard доказывает ownership/BIND/payload closure | Contract явно оставляет это Root preflight | Metadata containment не external authority | данных недостаточно |
| Medium source profiles I можно продолжить | Blocking interface ambiguity устранена | BUILD prerequisites всё ещё conditional | сохранить |
| BUILD/native/public/science выполнены | Execution receipts отсутствуют | Source-only design review | данных недостаточно |

**STOP. PASS_SOURCE exact path clarification; medium I guard разблокирован, BUILD не admitted.**
