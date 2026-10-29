# Кэшируемый пакет документации

Root собирает один обычный Nix-пакет со всеми страницами Core, Runner и оператора. Его ключ включает
полный опубликованный source graph, исходные страницы и рецепты, Manifest, выбранные инструменты,
исходное свидетельство depot, asset bytes и независимые публичные review receipts. Изменение графа
означает новый docs derivation даже при неизменных страницах. Это намеренная граница первой
реализации. Runtime/depot source filters P15 при этом не меняются.

## Входы и команды

Передайте абсолютный путь через `--inputs` или `QCL_NEGF_DOCS_INPUTS`. Файл имеет закрытую форму:

```json
{
  "format": "qcl-negf.docs-request.v1",
  "depot_metadata": { "path": "/owned/solver-depot.json", "sha256": "<64 hex>" },
  "asset_inputs": { "path": "/owned/asset-inputs.json", "sha256": "<64 hex>" },
  "review_inputs": { "path": "/owned/review-inputs.json", "sha256": "<64 hex>" },
  "factory": { "profile": "production-build", "test_workers": 2 }
}
```

Пути — отдельные обычные файлы без symlink ancestors. Reader ограничивает объём и связывает
проверяемый hash с фактически прочитанными байтами одного FD. Повторные JSON-ключи, неверный UTF-8,
нечисловые значения, неизвестные поля и наблюдаемое изменение файла отклоняются.

`deno task docs:plan --inputs /owned/request.json` проверяет захваченные входы и выбранный CURRENT
source graph и показывает обычный Nix argv. Для v2 выполняется только offline eval текущей
совместимости depot. Команда не реализует пакет. `docs:prepare` явно реализует его input closure;
`docs:build` реализует сам пакет. Проверки не вызывают подготовку автоматически. Missing depot,
инструменты, assets или review packet — конкретный prerequisite failure, а не разрешение на fetch,
Pkg или подстановку фиктивного подтверждения.

CLI передаёт в Nix захваченные raw depot metadata и их hash отдельно от нормализованного значения.
`lib.mkDocumentation` требует `capturedMetadata` и проверяет равенство его JSON-значения переданному
`metadata`. Исходные Unicode/whitespace bytes остаются в приватном provenance. V1 сохраняет
существующую exact-graph проверку; совместимый v2 хранит **исходный producer graph**, тогда как URL
сборки указывает текущий выбранный граф. Совместимость не переписывает старое свидетельство.

Стандартные Nix sandbox/store/substitution правила сохраняются. Нет отдельного docs VM, daemon,
cache ledger, обязательного root admission или таблицы заблокированных ревизий. Ограничения объёма
файлов, потоков логов и отдельных команд защищают конкретный транспорт; они не измеряют CPU/RAM или
завершение всех потомков процесса.

## Локальные проверки без сборки

`deno task docs:check --inputs /owned/asset-inputs.json` принимает **asset map**, а не полный
request сборки. Допустим fallback `QCL_NEGF_DOCS_ASSET_INPUTS`. Явно выберите существующие
`QCL_NEGF_DOCS_NODE` (Node 24) и `QCL_NEGF_DOCS_PYTHON` (Python 3.14 с PyYAML 6 и jsonschema). Путь
Python venv сохраняется, включая его штатную ссылку на интерпретатор. Deno — исполняемый файл
текущего процесса. PATH lookup и установка отсутствуют; несовместимые версии завершают проверку.

Проверка подтверждает весь asset/license набор существующим validator и создаёт отдельный временный
fixture. В нём выполняются полные неизменённые `test_docs_assembly.py`, `docs_math_test.mjs` и
`docs_static_slice_test.ts`. Последний получает единственный принадлежащий harness `/tmp` capability
и подготовленные живые symlink negative fixtures. Math получает точные KaTeX/Documenter/CSS bytes.
Общий discovery исключает только два специальных Node/Deno файла; `deno task check` обязательно
вызывает их через `docs:check`. Нет Nix, Git source traversal, Julia, render, Pkg, сети или
bootstrap в этом unit entry point. CI получает пути от подготовленного runner через явные
переменные; отсутствие этих prerequisites не превращается в skip.

## Результат и приёмка

`out/public` содержит serving payload и `docs-bundle.v1`; приватный provenance рядом связывает
точные входы, исходное depot proof, инструменты и bundle hash. Текущие абсолютные временные пути,
время, argv, RSS и успешный raw scratch в default artifact не входят. Ошибки сохраняют собственные
CLI receipts и штатный Nix `--keep-failed` workspace. Потерянный ответ, неполное сохранение логов,
нечитаемый bundle или изменение графа после dispatch дают `unknown`, а не успешную сборку.

Публичный Contracts API проверяет finite/C1/C2 и source refs всей coverage/media. Затем Root
проверяет собственный presentation allowlist, полноту media и точное равенство source/payload bytes.
Light theme, CSP, локальные fonts/math/search worker и все три page graphs обязательны.

Source/unit и чистый Nix eval не доказывают native render или cache hit. Отдельная приёмка Root
проверяет offline imports, полные страницы и C1/C2, реальный store output и логи, затем повтор тех
же входов без вызова builder. Substitution, NAR reproducibility и browser journeys с заблокированной
сетью проверяются отдельно. Scientific acceptance здесь не заявляется.
