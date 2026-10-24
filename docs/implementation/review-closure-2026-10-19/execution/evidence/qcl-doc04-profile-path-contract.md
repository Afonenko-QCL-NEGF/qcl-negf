# DOC04: точный внутренний layout pilot attempt

2026-10-20. Узкое source-only уточнение к frozen recipes D1+D2+D3; продуктовые файлы не меняются. Это контракт будущей реализации, а не свидетельство выполненного guard, импортов или BUILD. Выбор один: обязательный явный `QCL_DOCS_ATTEMPT`. Новый публичный формат, сервис и trust boundary не вводятся.

## Основание и область override

Применять совместно, не переписывая исходники:

| Frozen input | SHA256 |
| --- | --- |
| recipes D1 `/tmp/qcl-doc04-recipes-design.md` | `008650e7c9ff98bdaf38a3450d2b3b13818409795c92738d0a9dbddaba2c2505` |
| recipes D2 `/tmp/qcl-doc04-recipes-design-v2.md` | `ce582cc394d7dd70971c2a25929bf9362aad7d829403f1e2e0fba68a8ff65610` |
| recipes D3 `/tmp/qcl-doc04-recipes-design-v3.md` | `960a639dd281d7a5b99c582f2c9dc8b17e816715753557791460ebcef1159aee` |
| independent D3 R `/tmp/qcl-doc04-recipes-design-v3-review.md` | `7db5ad18c7c9e197fb0430422b917228ddc0216f90c0cdfb37f78ee80e9a4211` |

Уточняется только неопределённое выражение D1§3 «owned attempt root»: точный layout, before-import path predicate и сопряжение с Root. D3 `Module[]` и sitenames `QCLNEGF`, `QCLNEGFRunner`, `Документация оператора` сохраняются. Default Core/Runner branch, doctests, страницы, source-effect/asset/import prerequisites и shared DOC03 schema не меняются. Исторический original read overrun остаётся FAILED_RESOURCE_CAP; это отдельный ограниченный design phase.

## 1. Единственный layout и значения входов

Root `ops/docs.ts` использует уже заданный `--attempt-directory DIR`; нормализованный абсолютный `DIR` становится значением `QCL_DOCS_ATTEMPT`. Новый CLI selector не нужен. Root создаёт свежий attempt после внешней проверки права на этот namespace; отсутствие каталога до создания проверяет именно Root. Перед запуском recipe каталоги stage и raw уже подготовлены, но raw owner output отсутствует.

```text
ATTEMPT/
  stage/core/src/          # полный выбранный Core docs/src после допустимого staging
  stage/runner/src/        # полный выбранный Runner docs/src после допустимого staging
  stage/operator/src/      # index.md + recovery.md и согласованный support scope
  raw/                    # существует; сюда Documenter создаёт owner output
    core/                 # НЕ существует перед запуском Core recipe
    runner/               # НЕ существует перед запуском Runner recipe
    operator/             # НЕ существует перед запуском operator recipe
```

`ROOT` — выбранный source worktree superproject с `julia/Project.toml`; он не является attempt/staging/output. `ATTEMPT` расположен вне дерева ROOT, причём ROOT также не может лежать внутри ATTEMPT. Owner — literal в соответствующем recipe: `core`, `runner` или `operator`; переменной окружения для выбора owner нет.

| Recipe | QCL_DOCS_ROOT | QCL_DOCS_ATTEMPT | QCL_DOCS_SOURCE | QCL_DOCS_BUILD |
| --- | --- | --- | --- | --- |
| Core | ROOT | ATTEMPT | ATTEMPT/stage/core/src | ATTEMPT/raw/core |
| Runner | ROOT | ATTEMPT | ATTEMPT/stage/runner/src | ATTEMPT/raw/runner |
| operator | ROOT | ATTEMPT | ATTEMPT/stage/operator/src | ATTEMPT/raw/operator |

Четыре значения обязательны только при `QCL_DOCS_PROFILE=pilot-v1`, передаются явным ограниченным environment дочернего процесса. Ни cwd, ни recipe directory, ни random/latest directory не являются fallback. Core/Runner unset/empty profile продолжает существующую default branch; новая переменная там ничего не переключает. Operator остаётся pilot-only. Неизвестный непустой profile отказывает до импортов.

Сохранить byte-exact mapping operator `docs/public/operator-recovery.md` → `stage/operator/src/recovery.md`. Он даёт `operator/recovery.html` после последующей уже принятой assembly, не через post-render rename. Core/Runner сохраняют весь согласованный selected docs/src scope, страницы и anchors. Данное уточнение не разрешает изменять staged contents.

## 2. Точный read-only guard до owning imports

В каждом pilot recipe выполнить одинаковые правила с собственным literal owner средствами Base. До их завершения нет `using Documenter`, `using QCLNEGF`, `using QCLNEGFRunner`, owning include, создания/удаления файлов или каталогов. Guard не читает marker/receipt как полномочие. Средства Base для строк/путей и filesystem metadata разрешены; сторонний path package не нужен.

1. Все четыре значения непустые, абсолютные и уже нормализованные: строка должна точно совпадать с `normpath` этой строки. Дополнительно явно запретить компоненты `.`/`..`, повторные `/` и trailing `/`; не полагаться на то, сохраняет ли конкретный `normpath` trailing separator. Относительные и ненормализованные значения не исправляются молча. ROOT и ATTEMPT не равны filesystem root. Target paths — Linux absolute paths с `/`.
2. ROOT, ATTEMPT, SOURCE и `dirname(BUILD)` существуют как каталоги. Для каждого существующего компонента их абсолютных путей, включая ancestors, проверить `islink` и отклонить symlink. Затем вычислить `realpath` существующих каталогов и потребовать равенство переданным нормализованным строкам. Проверка лишь leaf недостаточна. Ошибка доступа/metadata/canonicalization отказывает.
3. Проверить точное равенство SOURCE с `joinpath(ATTEMPT,"stage",owner,"src")` и BUILD с `joinpath(ATTEMPT,"raw",owner)`. Поэтому SOURCE sibling другого owner, stage parent и любое произвольное поддерево не проходят. Для ещё отсутствующего BUILD canonical candidate образуется из проверенного `realpath(dirname(BUILD))` и literal owner; `realpath(BUILD)` не вызывается.
4. ROOT и ATTEMPT должны быть непересекающимися деревьями в обоих направлениях, включая запрет равенства. Containment сравнивает компоненты `splitpath`, а не строковый prefix: `/tmp/a` не является ancestor `/tmp/ab`. Проверить также SOURCE≠BUILD и отсутствие их ancestor relation в обоих направлениях. Layout уже даёт это разделение, явный predicate защищает дальнейшее сопровождение.
5. BUILD отсутствует: `ispath(BUILD) || islink(BUILD)` означает отказ, в том числе existing empty directory, regular file и dangling symlink. Parent raw существует и проверен. Recipe не создаёт/очищает raw owner output до `makedocs`; повторный запуск в тот же BUILD запрещён. Другие raw owner directories могут существовать после предыдущих шагов этого же attempt и сами по себе текущий owner не блокируют.
6. Сохранить D1 VERSION1.13.0 и active-project check до импортов: существующий обычный файл `ROOT/julia/Project.toml`, его компоненты без symlink; `Base.active_project()` должен указывать точно на этот canonical file. Это проверка выбранного пути, не proof состава зависимостей/бинарника. Ошибка любого predicate останавливает pilot до importer/output.

Не обходить рекурсивно дерево ROOT из recipe. Проверки выше покрывают путь к SOURCE, но **не доказывают содержимое staged payload**. Root обязательным finite staging/source preflight отдельно инвентаризует полный согласованный SOURCE, отклоняет все symlink entries внутри него, binds regular-file paths/bytes/hashes и source-effect allowlist. Special-file entries также запрещены. Успешная проверка ancestors не может подменять этот preflight. Рецепт использует проверенные строки как `makedocs(root=ROOT,source=SOURCE,build=BUILD,...)` без новой эвристики.

## 3. Root handoff, retention и граница доказательства

Root устанавливает один ATTEMPT и три точных owner tuples по таблице, последовательно запускает только допущенные recipes, сохраняет original stdout/stderr/exit/raw outputs и existing attempt receipt. При partial failure успешные raw owner outputs и failed owner outputs сохраняются; automatic cleanup, replacement или rerender поверх них нет. Новый запуск использует новый свежий ATTEMPT с parent-attempt reference в уже предусмотренном receipt. Ни path guard, ни данный документ не присваивают PASS, native-ready или release-ready.

В private receipt использовать существующие attempt/inputs/steps fields: точные ATTEMPT/ROOT/SOURCE/BUILD, literal owner, selected source/recipe/staging manifest bindings и наблюдавшийся результат predicate. Новую публичную схему не вводить; private absolute paths не экспортировать в public bundle. Самостоятельно написанные path/marker/receipt или caller-supplied boolean не являются техническим BIND.

До каждого запуска Root обязан иметь внешнее свежее BUILD admission, проверенную ownership/permissions и исключительность attempt namespace, source graph/recipe hashes, actual toolchain/cache/import/source-effect manifest, assets/license closure и конечный ресурсный бюджет по D1–D3. Эти свидетельства устанавливаются их owning preflight, а не выводятся из имени пути, UID процесса или наличия файла. Если обязательных данных нет — dependent BUILD blocked. Прямой вызов recipe даже с прошедшим path predicate не отменяет этого условия.

Base metadata checks не обеспечивают атомарность проверки/использования, защиту от bind mounts/hardlink aliases или конкурентной замены. Это внутренний fail-closed path contract для уже admitted/exclusive namespace, а не sandbox или новый security boundary. Внешний owner обязан исключить конкурентные изменения selected/staged inputs и attempt на время исполнения. Отсутствие такого свидетельства — prerequisite missing; не объявлять path containment доказательством ownership/admission.

## 4. Обязательные source-I controls и предел проверки

Будущая отдельная проверка I использует fake importer/output sentinel до реальных imports: missing ATTEMPT; relative/non-normalized path; SOURCE другого owner; existing BUILD (включая empty directory/file/dangling symlink); symlink ancestor; ROOT внутри ATTEMPT и наоборот; source/output overlap; lexical prefix trap `/tmp/a` против `/tmp/ab`; wrong project. Каждый invalid case обязан отказать до sentinel. Valid admitted-layout fixture проверяет только guard tuple и отсутствие ложного overlap; не импортирует owning module и не рендерит. Payload symlink case обязан отказать в Root staging preflight, не засчитываться как измеренный recipe-tree check. Default branch preservation остаётся отдельным existing source-I control. Здесь controls описаны, не исполнены; их запуск требует отдельного разрешённого конечного I envelope.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| «Owned attempt root» теперь имеет один точный layout | Четыре env inputs и literal owner tuples выше; D1§3/§6 | Source contract, без исполнения | изменить |
| Existing output нельзя случайно очистить повторным makedocs | Required absent BUILD, fresh attempt и retention rules | Runtime/TOCTOU не проверены | сохранить |
| Path predicate устанавливает BUILD ownership/admission | Только metadata containment; внешние prerequisites ещё обязательны | Caller path/marker не BIND | данных недостаточно |
| D3/default/scientific/UI границы сохраняются | Exact immutable inputs и узкий override | Native/full BUILD не запускался | сохранить |

STOP: frozen clarification для независимого high review; никакого product edit/BUILD этой записью не разрешено.
