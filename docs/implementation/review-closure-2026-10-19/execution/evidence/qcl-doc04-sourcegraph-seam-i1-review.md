# DOC04 I1 — fresh independent source review

**CPP_QUALIFIED_PASS_SOURCE_ONLY.** В owning seam регрессии не найдено. Реализация соответствует узкому D2 I1 и byte-equal Native overlay. Literal JSON и SHA согласованы; fixtures вызывают настоящий `sourceGraph` с dependency, без mocked validator. Ни исполнение fixtures, ни compiler, ни Root admission/READY, ни полный DOC04 этим verdict не подтверждены. Есть ограничение фиксированного locale order ниже.

## Проверенный source set

Workspace `/tmp/qcl-doc04-root-recipe-worktree`, HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`. На обоих refs b079… и Root `107bac5697b37cf0e47c3feb44883a907837645c` read-only `git ls-tree` показывает одинаковые owning blobs: `ops/git.ts=d006375ca701a646f7854daefa089bf4dcedb3b0`, `tests/git_test.ts=41e8ba3193de54e1497f8f9d1d729f0179ba746b`. Это совместимость двух paths, не identity/admission всего checkout. Все восемь submodules здесь uninitialized; fake fixtures не нуждаются в них.

Изменены только tracked `ops/git.ts`, `tests/git_test.ts`. Три untracked docs paths прежние; их текущие SHA совпадают с frozen baseline manifest: `ops/docs.ts=0837ceda6be4fbfbd90e411fe6e4fe665f8bc8979e63ac1fbfe6bacedd8b178a`, `docs/public/make.jl=b673bf4e2ba53179bccd7dcff631c8c1fe03893944cf2add868155e133705c8b`, `tests/docs_recipe_orchestration_test.ts=697b1774ee0573acfc6ec5e5c6ebf4b3c922fb6588cc9d291deab2f10f3408c3`.

## Owning implementation

`ops/git.ts:33–86`: mutable args заменены readonly; args передаются spread-copy, Git executable/env/default transport не менялись. Третий `readGit:GitReader=git` additive; все восемь lexical call sites используют dependency. Аргументы, root/child traversal, requireClean short circuit, malformed revision/config/gitlink/URL/nested/orphan guards и returned object insertion order прежние. `gitlinks:24` сохраняет global `localeCompare`. Формат v1, URL и raw serialization не нормализуются. SHA owning file совпадает с Native overlay: `f1b37ea11c20bd3e64ac7e57ce4d5bc649897a8db9f099ccdc87ada4e4e65764`.

Двухаргументные callers сохраняют прежний default code path. `tests/git_test.ts:193–197` содержит assignability witnesses без dispatch, но compiler их не проверял. Docs private projection, observer/comparator/wrapper I2 отсутствуют и не требуются для I1.

## Независимая трассировка fixtures

`tests/git_test.ts:40–50` fake reader проверяет exact root и JSON argv, потребляет каждый reply один раз и проверяет exhaustion. Production `sourceGraph` реально строит graph и реально исполняет guards; fake не выдаёт готовый graph либо validation boolean.

Для clean N=1 трасса `61–106`: root HEAD/status/config/tree (4 calls), child URL/tree/HEAD/status (4 calls), итого 8; оба status читаются один раз. `108–113` requireClean=false исключает оба status, оставляя 6 calls. N=4 в `126–159` даёт 4+4N=20 calls; записи URL и child roots соответствуют configured sections, а порядок определяется настоящим `gitlinks`.

Guard controls `161–190` обрезают replies именно в точке expected throw: invalid revision=1, root dirty=2, invalid config=3, missing/invalid gitlink/config section=4, URL=5, nested=6, child mismatch=7, child dirty/orphan=8. Exact error message и exhaustion отличают ожидаемый guard от unexpected argv failure. Исходные чистые parsing tests сохранены.

В single graph literal component keys идут revision/path/url, как `{...item,url}` в builder. Без LF SHA256 independently hashed literal JSON = `95a1af7b7d1bd04187ffa64d8b94dbd4eb0345bdd5edac06d7cceee87ada3958`, совпадает с `tests/git_test.ts:102–105`. Mixed literal из `154–158` независимо rehashed = `842a16f0d2d2323eee605ccbe1f03e2c8ef7f1ec464c6ddf9d025371afcf9304`; это правильный hash именно заявленных bytes. Hashing строк не исполняет fixture и не подтверждает, что runtime вернёт этот порядок.

**Квалификация F1 — default locale не привязан.** `tests/git_test.ts:115–124,137–158` фиксирует порядок `a,A,a-,a.` и соответствующий traversal/digest. Production `ops/git.ts:24` использует `localeCompare` без locale; `deno.json:3` не фиксирует locale runtime. Поэтому literal expectation выражает конкретное предположение о collation, а не переносимый результат для любого окружения. В этой source-only проверке collation/ICU не исполнялись и actual test locale не установлен. Это не регрессия owning seam и не основание менять global comparator. Для исполнения нужно зафиксировать применимое окружение fixtures; для portability control можно сопоставлять injection path с независимой сохранённой legacy semantics в той же locale, сохраняя отдельный fixed JSON/hash oracle. До этого не заявлять locale-independent fixture PASS. Рекомендация: дополнительно измерить/уточнить fixture applicability перед широким runtime claim.

## Границы verdict

Source review соответствует D2 repair R2; I2 repair R1 не рассмотрен как implemented. Old DOC04 unit5/5 EXHAUSTED, нового execution grant нет. Product/source/CHECK counters — только authority Root CP; здесь они не переаттестованы. CPP-qualified source verdict не расходует E1 и не активирует его. ROOT full acceptance, Native transport, docs assembly/render и science не следуют из этой проверки.

Читались только именованные файлы/короткие excerpts, Git metadata и hashes; записаны только этот review и identity. Исходники/index/CP не менялись; tests/Deno/compiler/import/parser/scripts/network/native/solver/children — 0. SHA256 literal metadata JSON выполнен отдельно от проекта. Один ошибочный lookup baseline filenames дал NotFound; затем прочитан именованный baseline manifest. Missing baseline files не были приняты за нулевые данные. Физический I/O/RSS и total output не измерялись; набор чтений значительно ниже 4 MiB, вывод ограничен адресными excerpts, без утверждения strict enforcement PASS.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| I1 реализует выбранный additive seam | git.ts diff; точный Native SHA | Default runtime не запускался | сохранить |
| Fixtures идут через production builder | tests:40–113,126–190; trace 8/6/20 calls | Нет execution/typecheck | сохранить |
| Literal SHA корректны | Независимое SHA256 обоих JSON literals | Hash не доказывает runtime collation | сохранить |
| Mixed order применим ко всем locales | tests:115–158; git.ts:24 | Default locale не зафиксирован | дополнительно измерить |
| Protected docs paths сохранены | Baseline manifest + текущие SHA | Не review содержания I2 | сохранить |
| Root/DOC04/runtime READY/PASS | Нет нового runtime evidence | CPP source-only; unit exhausted | данных недостаточно |

STOP: review-only, qualified CPP source verdict, дальнейшего grant нет.
