# OPS04.S Root v2 — independent high test-source review

2026-10-19. **REQUEST CHANGES: один блокирующий ошибочный oracle в frozen test source.** Новые CLI/capture fixtures в целом причинные и соответствуют принятому seam, но combined packet нельзя считать готовым для планового RED/GREEN до исправления F1 и нового freeze. Reviewer ничего не исполнял; observed RED отсутствует. Решение о correction/runtime counters принадлежит координатору.

## F1 — ошибочное ожидание порядка ключей после duplicate-member normalization

**Локатор:** root `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, frozen `tests/solver_test.ts` SHA256 `d26512392d63eaccf44ab7711ea07b1b6c8a15a3fb3108afd47c1ccacbf9d542`, test `OPS04 graph and object order are immaterial while raw duplicate members normalize once`, строки **163–171**, конкретно assertion **171**.

Строка 166 строит raw JSON с первыми полями `hash`, `url`, а затем дописывает serialized `spec`, в котором эти поля повторяются. При `JSON.parse` повторное присваивание member изменяет значение существующего property, сохраняя позицию его первого появления. Поэтому принятая D2 normalization `JSON.stringify(JSON.parse(raw))` имеет порядок `hash,url,format,sources,julia,juliaManifest`. Правая часть assertion `JSON.stringify(spec)` имеет порядок `format,sources,julia,juliaManifest,url,hash`.

Значения одинаковы; строки различны. Корректная реализация ровно D2 parse→stringify будет отвергнута fixture. Чтобы удовлетворить ему, пришлось бы неоговорённо перестраивать key order, что противоречит заданному exact produced-JSON oracle. Это не intended behavioral RED: defect переживёт правильную реализацию и помешает GREEN.

**Минимальное исправление предложения:** сохранить duplicate-value positive, но ожидаемую produced string задать как определённый контрактом JS parse→stringify outcome, например независимо вычислить `JSON.stringify(JSON.parse(raw))`, либо явно собрать объект с правильным first-occurrence key order. Сохранить независимый SHA actual outgoing JSON и проверки archive/full graph/raw-versus-produced evidence. Не вводить canonical key sorting ради этого теста. Reviewer source не менял.

## Identity и порядок проверки

Primary accepted D2 T1/T2 и CLI seam, затем фактические `ops/solver.ts`, `ops/application_cd.ts`, `nix/solver.nix` прочитаны **до candidate test source**. Затем прочитаны оба frozen test files целиком; только после них author report/identity/delta и baseline tests/deno config. Это отдельный от автора source review; использован тот же reviewer, который ранее проверял seam design. Ранее раскрытое ограничение порядка чтения относится к предыдущему seam-design review, не к этому test-source проходу.

Checkout `/tmp/qcl-ops04-root-worktree`; фактический root HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`. Начальный и конечный status: только ` M tests/application_cd_test.ts` и ` M tests/solver_test.ts`. Восемь selected gitlinks не инициализированы и не обновлялись. Targeted product diff к HEAD для трёх owning product files пуст, exit 0. Source authority остаётся Git tree, identity receipt не является lock.

| Frozen input | Проверенный SHA256 |
| --- | --- |
| tests/solver_test.ts | d26512392d63eaccf44ab7711ea07b1b6c8a15a3fb3108afd47c1ccacbf9d542 |
| tests/application_cd_test.ts | bd92a82d858ea17d1a124f2a9d257a76329f7f1630e423aad5ba1840c1982f85 |
| root-red-v2-report.md | 4f60d3d684f7bb4246a58ca0713ec0d4451e5a1c6f0624ccbce903ae6bf39e34 |
| root-red-v2-identity.json | 4e8c943c6574c887815b2c7d37715401f97f2f0e62472d5fe634dc57dbf953f3 |
| root-red-v2-patch.diff | c3a5fded8313ad9949873b6b43167f2c096d211d50157e669d0d695645356cc8 |
| root-red-v2-delta.json | 696d452b20eaf505ad034087cfaa3cf3a6adece60d0acd93f787309092d7ade4 |

## Что остальная source проверка установила

- **RED адресует изменение поведения.** Current `buildSolver` принимает unchecked object/revision/path, а новые direct healthy tests передают требуемый immutable JSON/full graph/Manifest. Signature bridge через `unknown` не делает TypeScript incompatibility единственной причиной RED. Namespace export casts обходят missing-export compile error, после чего baseline absent seam ломает healthy runtime fixtures. Negative tests, которые могут пройти из-за отсутствующего seam, сами по себе не названы observed RED. Никакой parser/typecheck reviewer не запускал; отсутствие иных type errors не установлено исполнением.
- **Full graph и consumed bytes:** `solver_test.ts:54–74` независимо хеширует actual outgoing arg и сверяет SHA argv/returned observation, archive URL/hash, root и каждый component. Строки 185–223 дают wrong commit/url/path, missing/extra/duplicate graph, lock/format/type/size controls, raw/produced UTF8 bounds и exact65536 positive. Фикстура expanded numeric JSON различает raw bound и produced bound. Единственный найденный ошибочный normalization oracle — F1.
- **Path mutation:** прежний helper A→B test `116–140` честно моделирует string boundary; новый actual application test `206–274` выполняет атомарную replacement именно на первом application callback, требует capture до него, запрещает второй open и проверяет A у обоих consumers. B captured до начала проходит отдельным healthy сценарием `276–317`; это соответствует contract, не искусственный отказ допустимого B.
- **Actual bounded capture:** `solver_test.ts:276–361` отдаёт production loop инструментированный file handle. Exact65536 short reads включают split multibyte codepoint; каждый requested view равен оставшемуся bounded storage; EOF sentinel проверен. Oversize fixture требует ровно65537 returned bytes и отсутствие дополнительного read. Stat/read/no-progress/decode/size/nonregular outcomes закрывают handle; I/O errors сохраняются. Реальные файлы `363–385` проверяют default opener, invalid/truncated UTF8, BOM, raw NUL, directory и empty capture. FIFO/hostile race guarantee не заявляется.
- **No execute на invalid inputs:** solver actual seam `410–439` и application `319–354` проверяют encoding/size/graph/lock/argv/cache failures и ровно0 dispatch callbacks. Identity reads инъецированы; Git/subprocess не нужны. Application проверяет отсутствие final/pending output, solver — matching open/close count.
- **Assembly и persistence:** `application_cd_test.ts:206–274` фиксирует open→graph→lock→application→prefetch→solver→path-info→graph→copy, stdout capture flags и literal cache argv; independently вычисляет старый release digest и читает actual final file. `276–317` меняет dependency object и nested borrowed graph, проверяя captured function refs и owned snapshot; array-shaped path-info/no-cache route сохранён. `356–386` graph drift после path-info запрещает copy/write. `389–416` pending collision сохраняет существующие bytes и не создаёт final output. Filesystem operations не инъецированы high-level fake.
- **Cache и совместимость:** прежний `application_cd_test.ts:21–100` corpus сохранён; `102–152` дополняет synthetic named/explicit-empty/encoded-password/control/type negatives и username-only/local/Nix literal positives без новой scheme policy. SSH/ssh-ng username и `%3A` внутри username не перепутаны с password delimiter. Solver resource defaults/options, file prefetch name/hash/order, failed prefetch и HTTPS command counts перенесены из baseline на новый API. Removed old source-grep assertion о fetchurl name не заменяется fake proof actual Nix recipe; это остаётся source review/Nix gate. Новые tests не заявляют Nix parser/hash assertion или native outputs.

## Стоимость и границы результата

Разрешённый review envelope: ≤20 min, 1 CPU, 2 GiB, reads≤4 MiB, report≤96 KiB. Cumulative read/CPU/RAM/tool-output telemetry не инструментировалась; пределы не выдаются за измеренные данные. Использованы явные source/packet paths, без execution-tree traversal. Выполнялись только text/Git/SHA reads и запись двух review artifacts в `/tmp`. Source writes, target imports/parsers/typecheck, Deno/Nix/tests/build/network/server, children и checkpoint writes: **0**.

Сообщённые coordinator точные runtime Deno2.8.3/Node24.21 и source-binding receipts здесь не воспроизводились и не проверялись запуском. Они не устраняют F1. Этот review не расходует и не переопределяет coordinator-owned план двух finite Root Deno RED/GREEN invocations; обе стадии остаются будущими. Нет observed RED, GREEN, native/scientific acceptance или permission на phase2 implementation.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Combined frozen v2 готов к intended RED/GREEN | F1: solver_test.ts:166–171 ожидает неверный key order | Правильная D2 normalization не даст GREEN | изменить |
| Новые CLI seams дают причинные reader/order controls | Actual export calls, low-level opener, first-app-callback mutation и pending/rename fixtures | Только source, не execution | сохранить |
| Полный graph и exact outgoing SHA покрыты | solver bound helper и wrong-graph controls; application actual argv/raw/produced hashes | Nix hashString/fromJSON не выполнялся | сохранить |
| Runtime compatibility и observed RED установлены | Execution receipts reviewer отсутствуют | Без импорта/typecheck/test run | дополнительно измерить |
| Native/scientific acceptance установлена | Таких receipts нет | Source-only review | данных недостаточно |

**STOP. REQUEST CHANGES F1; coordinator решает correction и следующий freeze. Reviewer source не менял и runtime slots не расходовал.**
