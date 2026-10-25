# DOC04 I1 — owning readonly GitReader seam

Статус: **IMPLEMENTED_SOURCE_ONLY_PENDING_FRESH_HIGH_REVIEW**. CP/READY, commit,
push, runtime PASS и полный DOC04 этим отчётом не выдаются. STOP перед fresh high review.

Owning workspace `/tmp/qcl-doc04-root-recipe-worktree`, ветка
`codex/review-closure-doc04-root-recipes`, HEAD
`b07974b8e46bf8afdf1740947b842669a62a5ccc`. Managed Root target
`107bac5697b37cf0e47c3feb44883a907837645c`. До записи `git diff` двух refs по
двум owning paths был пуст, и `git ls-tree` подтвердил одинаковые blobs:
`ops/git.ts` `d006375ca701a646f7854daefa089bf4dcedb3b0`,
`tests/git_test.ts` `41e8ba3193de54e1497f8f9d1d729f0179ba746b`.
Это source compatibility, не перенос/приёмка всего checkout. Recursive submodule
status сохранён в tool evidence: все восемь submodules не инициализированы;
gitlinks не обновлялись. Target Root status заново здесь не измерялся.

Прочитаны AGENTS, architecture excerpt, нужные design clauses V1/D2 и review.
D2 SHA256 `6c747fdd3b029143ae0047320d7a2f089cbabb3d70f21b5bb24de9c6cf87236c`,
review `74030c0c5ce06f2e91b495fa900d21bc31c12c29fea3248e0292d3e4824ca527`
подтверждены. Большие объединённые чтения были truncated; это ограничивает
полноту прочтения невыведенных clauses. Адресные D2 R2 API/order clauses
прочитаны отдельно полностью. Применён test-driven-development с явным
source-only override: fixtures записаны первыми, RED/GREEN не исполнялись.

## Source delta

Изменены только `ops/git.ts` и `tests/git_test.ts`. Первый файл теперь принимает
readonly argv, экспортирует `GitReader=(root:string,args:readonly string[])=>Promise<string>`
и третий аргумент `readGit:GitReader=git` у `sourceGraph`. Все восемь внутренних
Git reads используют dependency. Command args по-прежнему создаются spread-copy.
После записи `diff -q` с Native overlay `/tmp/qcl-docs-test-routing-worktree/ops/git.ts`
вернул 0: один и тот же seam, без копирования других файлов overlay.

Двухаргументный default path сохранён source-wise: default `git`, root workspace,
requireClean true; argv, порядок вызовов, guards, URL, graph format,
`localeCompare`, object key insertion order и raw serialization не менялись.
Никакой global duplicate-policy migration или private docs projection нет.
Два compile-time witnesses сохраняют legacy sourceGraph call shape и GitReader
assignability; compiler их не проверял. Фактический default Git transport не
исполнялся, его runtime equivalence не аттестуется.

## Номинальное покрытие fixtures

Handwritten fake reader принимает readonly argv и требует точных root/argv
на каждой записи; лишние/недостающие вызовы отказывают. Сами tests вызывают
реальный owning sourceGraph; fixtures никогда не вызывают Git. Старые три
tests сохранены без изменения их тел.

Добавлены controls: clean empty statuses; requireClean false без обеих status
reads; invalid root SHA; dirty root и child; отсутствующие и escaping gitlinks;
missing, duplicate, invalid и orphan .gitmodules entries; invalid URL; nested
submodule; checked-out SHA mismatch. Positive graph проверяет сохранение `.git`
URL и literal JSON/SHA256. Mixed-case/punctuation graph и отдельный gitlinks
control задают literal traversal `a,A,a-,a.` и literal raw JSON/hash, независимо
от production helpers. Hash literals рассчитаны `sha256sum` над handwritten
JSON без LF, не sourceGraph. Эти значения/порядок ещё не проверены в Deno;
locale-dependent legacy expectation требует runtime проверки в разрешённой среде.

Основной fixture set записан до production patch; его SHA256 сохранён в
`/tmp/qcl-doc04-seam-i1-baseline/tests-first.sha256`. Затем добавлен ещё один
mixed graph control без последующих production edits. Это test-first source
sequence, не завершённый RED/GREEN TDD.

## Exact bytes и проверки

Baseline `/tmp/qcl-doc04-seam-i1-baseline/ops/git.ts`:
`1fd37fad1ac94e890e8fbc4b8f73147965b4a5eb5cd9ce735a98c2ff15d13be7`.
Baseline `tests/git_test.ts`:
`705ae50649d88fed7cf53475fe49f3450177d213ed0815ab358ba405814a7b40`.
After `ops/git.ts`:
`f1b37ea11c20bd3e64ac7e57ce4d5bc649897a8db9f099ccdc87ada4e4e65764`.
After `tests/git_test.ts`:
`927cbd5efc64536ffece01668eb8ee28d502e6fd1ab7a204aaeb807f0371e968`.
Complete patch SHA256:
`f066ecfb83b806df268c801d83e2c9049a7f6c89578a2d5b241ec0ee4e59a05b`.
`git diff --check` выполнен успешно; это whitespace check, не parser/compiler.
Protected `ops/docs.ts`, `docs/public/make.jl`,
`tests/docs_recipe_orchestration_test.ts` повторно проверены по исходному manifest:
все три SHA256 unchanged. Index/HEAD не менялись.

Scripts/import/parser/compiler/tests/Deno/formatter/linter/network/native/solver,
CP/READY/index/commit/push и дочерние агенты: 0. Использованы только source
reads, read-only Git metadata/diff, SHA256, cp baseline и source edits. Старый
DOC04 unit5/5 exhausted не потрачен повторно. CPU/RSS/physical IO и суммарный
tool-output byte count не измерялись; строгая аттестация caps отсутствует.
Объём двух baseline sources 4929 bytes, complete patch 12713 bytes; чтения узкие,
логический именованный corpus существенно меньше 2 MiB.

## Remaining I2 / gates

Не реализованы observation/comparison/wrapper, private detached projection,
late-fresh expected, precedence Changed/Unknown и same-size mutation controls.
Protected frozen docs sources не тронуты. Bounded production transport,
terminal writer, durable receipts, process stop, native admission, ABA,
staging/schema/assembler URL/rendering, browser/offline/light acceptance остаются
вне I1. Следующее действие — fresh high source review этого patch; исполнения
требуют нового конечного Root envelope.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning readonly seam совпадает с Native | diff -q exit0; after hash | Unpublished source, без compiler | сохранить |
| Общие guards/order/raw JSON сохранены | Узкий ops/git.ts diff; literal fixtures | Fixtures не исполнены; locale зависит от среды | дополнительно измерить |
| Target Root owning bytes совместимы | Два равных Git blobs b079→107 | Остальные paths/refs не аттестованы | сохранить |
| Frozen docs artifacts сохранены | Три manifest SHA checks OK | I2 не реализован | сохранить |
| DOC04/runtime/science приняли | Измерений нет | Source-only, unit budget exhausted | данных недостаточно |
