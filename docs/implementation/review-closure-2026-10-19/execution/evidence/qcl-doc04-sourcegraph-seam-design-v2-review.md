# DOC04 SourceGraph seam D2 — независимый source-only review

**D2_TWO_REPAIRS_ACCEPTED_SOURCE_DESIGN.** Блокеров для двух адресных исправлений R1/R2 не найдено. Рекомендация Root: оформить два узких I-ready source tickets ниже. Это не CP/READY, разрешение исполнения, готовность production transport, полный DOC04 либо runtime PASS.

Проверен Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `107bac5697b37cf0e47c3feb44883a907837645c`. Наблюдены modified checkpoint и четыре untracked routing/publication artifacts из D2 identity; они не изменялись. Gitlinks прочитаны через `git submodule status --recursive`, без обновления. Native overlay HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; recipe overlay HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`. Overlay bytes не являются опубликованным Root API.

## Первичные наблюдения и R2

Actual Root `ops/git.ts:14–24,33–84` строит единственный SourceGraph с `localeCompare`, `git(root,args:string[])` и двумя параметрами `sourceGraph`. Native overlay `ops/git.ts:33–86` уже добавляет `GitReader(root,args:readonly string[])` и третий `readGit`; spread argv сохраняет способность передать readonly массив. Все внутренние Git reads там используют dependency. Native `ops/docs_tests_cli.ts:155–186` возвращает reader с readonly argv и вычисляет digest над UTF-8 `JSON.stringify(observed)`.

D2:19–65 выбирает именно этот additive API и сохраняет owning graph order, URL, format v1 и raw serialization. Отдельная docs projection копирует graph/components/inputs и сортирует только свои массивы; это не затрагивает Native raw digest. Совместимость заявлена достаточно конкретно для реализации: legacy two-arg callers, exact recorded replies, upper/lowercase/`.`/`-` cases, unchanged raw JSON/hash и отсутствие мутации original graph (D2:260–265). R2 v1 review закрыт на уровне design. Это не доказательство runtime/type compatibility: compiler/tests не запускались.

## R1: достижимость Changed и Unknown

Recipe overlay `ops/docs.ts:261–309` проверяет длину относительно собственного opened stat, bounded actual read и собственные metadata до/после. Frozen hash в этом reader отсутствует. Поэтому D2:67–124 может сохранить этот reader, передать policy cap и вернуть actual hash нового содержимого прежней длины. Нельзя передавать frozen length как доказанный текущий stat.

D2:138–209 разделяет наблюдение и pure comparison. При stable clean graph и same-size external plan/recipe mutation после execute наблюдение возвращает `present(actual)`; actual SHA отличается от expected; comparison создаёт `file_changed`; wrapper D2:211–255 выбирает `failed_source_changed`. Обязательного frozen match в этом пути больше нет. До execute тот же mismatch даёт `blocked_before`, execute count0. Сохранены фактические after bytes/hash, исходный before binding, raw и `candidate:null`. Контроль D2:267–276 различает старую ошибку: observer, бросающий исключение на hash mismatch, не выдаст требуемый typed Changed.

Для verified absence задан `file_absent`, без подстановки bytes/hash0. Чтение с permission/unstable/transport error без positive change даёт Unknown. Изменение одного input одновременно с unreadable другим даёт Changed с сохранёнными unknowns. Успешный непустой status из rejected owning graph позволяет positive dirty evidence; truncated/failed stdout этого не позволяет. Этим обходится ранний owning requireClean throw без второго graph builder (D2:126–136,171–185,277–282). Фактическое доказательство изменения имеет приоритет над неполнотой остальных наблюдений; unknown не превращается в matched.

Expected preparation по-прежнему требует frozen match и два clean stable complete graphs; это применимо до получения trusted expected, а не как условие возврата after observations. Callback failure/throw не отменяет after observation. R1 v1 review закрыт на уровне design; реальные file/transport controls отсутствуют.

## Сопоставление с frozen v1

V1:173–205 требовал frozen match внутри capture, а V1:248–255,315–316 одновременно обещал Changed и Unknown для несовместимых after outcomes. D2 явно заменяет эти clauses отдельными Observation/Comparison и precedence. V1:48–67 менял общий comparator и предлагал конкурирующий GitRunner; D2 заменяет их readonly GitReader и private docs projection. Frozen v1/review hashes совпали с поручением, исходные artifacts не менялись. V1 transport caps, aggregate attempt limits, original raw, createNew namespace и failure writer требования остаются. Не переаттестовывались все прочие clauses v1 либо прежний recipe review.

## Минимальные I tickets, рекомендуемые Root

1. **Owning readonly seam + compatibility fixtures:** только `ops/git.ts`, `tests/git_test.ts`; один Root writer переносит Native-compatible третий аргумент и readonly GitReader. Все calls инъецированы; сохранить legacy graph JSON/hash и порядок. Отдельно проверять public behavior на одинаковых recorded replies, не менять global comparator/duplicate policy.
2. **Docs observation/comparison/wrapper + private projection:** `ops/docs.ts`, `tests/docs_recipe_orchestration_test.ts`; fake-only bounded Git transport, recorder, current input observation, expected preparation, comparison precedence, detached canonicalization и wrapper. Controls из D2:260–282 должны различать same-size plan/recipe mutation, absence, unreadable, changed+unknown, dirty против truncated transport и callback throw; preflight без trusted dependency остаётся blocked. Реального Git/Julia/assembler dispatch нет. Namespace/write failure запрет bound success из v1 сохраняется.

Root может признать эти source tickets I-ready после собственного решения; текущий review ничего не запускает. Fixture execution потребует нового конечного grant: old DOC04 unit5/5 EXHAUSTED не изменён. До implementation нельзя заявлять CLOSED_IMPLEMENTED или runtime PASS.

Production transport/terminal writer, durable receipts, эффективная остановка процессов, native admission, ABA/exclusivity, staging/schema/assembler URL/полный renderer, resource/browser/offline/light acceptance остаются отдельными открытыми gates. Отдельную `.git` URL проблему и полный renderer не исследовал и не включал в исправления. Source-only I-Root остаётся PARTIAL.

## Метод и ограничения

Чтение именованных source excerpts, узкие текстовые поиски, read-only Git metadata и SHA256; изменения только этого review и companion identity в `/tmp`. Исходники/CP/index не менялись. Scripts/import/parser/compiler/tests/network/solver/native/READY actions и дочерние агенты — 0. Начальные наблюдения owning/Native reader и digest получены до чтения frozen v1-review; полной слепоты нет, поскольку задание и D2 называли R1/R2.

Логический объём именованных файлов существенно меньше 2 MiB; физический I/O/RSS не измерялись. Предел total tool output 64 KiB строго не счётился: многословные первичные чтения могли его превысить; соблюдение этого ограничения не аттестуется. Это ограничение процесса review, не свидетельство о runtime проекта.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Same-size mutation достигает Changed | D2:67–185,240–255,267–282; reader docs.ts:261–309 | Только design/source trace | изменить |
| Unknown не маскируется как matched | D2:171–185,240–255 | Transport/fixtures не исполнялись | сохранить |
| Additive seam совместим с Native design | Native git.ts:33–86, driver:155–186; D2:19–65 | Unpublished overlays, нужен один writer | изменить |
| Общий SourceGraph v1/raw digest остаётся прежним | Root git.ts:24,42–84; Native driver:182–186; D2:42–65 | Private docs projection реализовать отдельно | сохранить |
| Два узких source tickets можно объявить I-ready | R1/R2 закрыты design, controls определены | Решение Root; исполнения/полного DOC04 нет | изменить |
| Полный DOC04/BUILD/native/science прошёл | Таких измерений нет | Old unit5/5 exhausted, нового grant нет | данных недостаточно |

STOP: review-only. Никаких следующих действий review не активирует.
