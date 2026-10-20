# DOC04 SourceGraph seam — независимый source design review v1

**DESIGN_CHANGES_REQUIRED; I-ticket пока не готов.** Найдены два конкретных блокера: несовместимые правила after-capture при изменении frozen input и неразрешённая общая семантика/API `SourceGraph` поверх уже существующего unpublished Native seam. Исполнение, source implementation и полный DOC04 READY/PASS не подтверждены.

## Проверенный набор

Design `/tmp/qcl-doc04-sourcegraph-seam-design-v1.md`, SHA256 `0842a7f6b826d4f69b90b556029bbed5d43dcfbdd6950bb8bb7553d2d847de0c`; companion identity `5b08d70701de70d269898ad4ceba8e8b2c9a281a6c4bd4d7702494f73e47faae`; read-ledger `c8f7d7c7a8f0288e2b97e288473d3e761f93aee458c35d1d851cd1581eec5c0a`.

Actual Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `107bac5697b37cf0e47c3feb44883a907837645c`. Git status соответствует design identity: modified checkpoint и четыре untracked evidence/publication files. Восемь фактических gitlinks сняты напрямую; Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Runner `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`, Results `de70638a982f91b7e125ab1cfc70a2daef2a656d`. Results c00 этим Root не selected. SourceGraph `ops/git.ts` SHA256 `1fd37fad1ac94e890e8fbc4b8f73147965b4a5eb5cd9ce735a98c2ff15d13be7`; его фактическая сигнатура имеет два параметра.

Recipe overlay `/tmp/qcl-doc04-root-recipe-worktree`, HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`: три прежних untracked recipe/orchestrator/test paths, исходники совпадают с frozen v2 hashes. Предыдущий review `97f01e8b463a2554c32c28ac05b388ddcc8b43a9acc936a41f42bcf6131a9a83`: только R1/R2 CLOSED_SOURCE, общий PARTIAL / NOT_READY. Новая независимая аттестация всех прежних recipe assertions не выполнялась.

Native overlay `/tmp/qcl-docs-test-routing-worktree`, HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; `ops/git.ts` modified, SHA256 `f1b37ea11c20bd3e64ac7e57ce4d5bc649897a8db9f099ccdc87ada4e4e65764`. Это unpublished bytes, не API actual Root. В них уже есть `GitReader(root,args: readonly string[])`, третий `readGit` и сохранённый `localeCompare`. Native driver SHA256 `268554ff880349939d7577cd07104762cc2d8f446dd597079171985e36c2cae7`, fixture source SHA256 `a3c9baf9f095b230a0d78082fb5769f1f11b84efa3f16a2e440a21e55c311dd2`.

## R1 — after-capture не может выдать обещанный результат для изменённого input

Локатор: design `captureDocsIdentity`, строки 188–205; `withDocsSourceIdentity`, 248–256; control 5 в §6.

`captureDocsIdentity(root,frozen,deps)` обязан отвергать mismatch actual bytes/hash относительно frozen и при ошибке не возвращать identity. Если внутри execute изменились байты внешнего plan при прежнем размере, два graph reads могут успешно совпасть, но after-capture отвергнет actual input. Wrapper по собственному правилу «after получить нельзя» вернёт `failed_identity_unknown`. Control 5 требует для этого же случая `failed_source_changed`, с after mismatch. Эти контракты одновременно не исполняются. То же относится к recipe, когда изменение не проявилось как dirty Git либо речь о внешнем frozen input; dirty отдельно честно даёт unknown.

Минимальное решение владельца: либо отделить bounded observation actual bindings от проверки frozen manifest и вернуть полноценный detached after для сравнения, либо определить typed capture outcome `observed_mismatch` с фактически прочитанными bindings и отдельно `unobservable/error`. Тогда известная смена hash даёт `failed_source_changed`, невозможное наблюдение — `failed_identity_unknown`. Before по-прежнему запрещает execute при mismatch. Нельзя просто изменить control на unknown и потерять различающее свидетельство о реально прочитанных новых bytes. Production dispatch для этого решения не требуется.

## R2 — общий API и порядок graph требуют одного merge-контракта

Локатор: design 48–67; actual `ops/git.ts:24,42–84`; Native `ops/git.ts:33,42–86`, `ops/docs_tests_cli.ts:155–186`; actual callers `ops/release.ts:63`, `ops/solver.ts:352`, `ops/ci.ts:114`.

Design одновременно обещает прежнюю семантику callers и меняет глобальную сортировку `gitlinks` с `localeCompare` на code-unit comparator под прежним `qcl-negf.git-graph.v1`. Допустимый path grammar содержит upper/lower case, точки и дефисы; совпадение двух порядков не является общим контрактом. Production callers сравнивают `JSON.stringify(graph)`, Native driver хэширует именно `JSON.stringify(observed)`. Следовательно это изменение общего source/digest контракта, а не только добавление transport seam. Design не содержит compatibility/migration решения и не учитывает уже подготовленный Native вариант.

Есть также конкурирующий точный API: design `GitRunner(args:string[])` против Native `GitReader(args:readonly string[])`. Оба предлагают третий параметр одного owning symbol. Нельзя независимо применить два patch и считать их согласованными. Mutable runner не заявляет возможность принимать readonly argv; совместимость типов здесь не проверена compiler и не должна подразумеваться.

Минимальный готовый контракт: coordinator выбирает один additive owning seam, предпочтительно совместимый с уже существующим readonly `GitReader`; все вызовы builder используют его, docs runner явно передаётся, fallback запрещён. В этом ticket сохранить общий legacy graph order. Для новой docs identity определить **отдельную detached canonical serialization** с code-unit sorted копиями components/inputs; не менять/mutate возвращаемый owning graph и Native digest. Если действительно нужен общий порядок v1, выделить отдельное owning compatibility решение со всеми consumers и Native owner. Duplicate malformed records можно отвергать независимо от смены сортировки.

## Что в design достаточно определено

Единственный owning builder, сохранение проверок clean/gitlink/URL/nested/orphan, bounded transport refusal без buffered fallback, shared attempt counters, запрет обработки partial stdout, fatal UTF-8, exact frozen byte hashes и поздняя fresh git composition заданы предметно. Один capture использует два owning graph observations; expected/before/after совместно требуют шесть, для N=8 — 216 Git calls по указанной формуле. Это оценка по исходникам, не выполненные calls и не выданный runtime grant.

Wrapper выполняет execute один раз после before, требует after после failure/throw и держит `candidate:null`. Произвольный trusted callback не становится sandbox; design признаёт это. Совпадение source snapshots не доказывает ABA/exclusivity, imports/toolchain closure, process-tree enforcement, durable storage, accepted assembly/schema или физическую приёмку. Deferred production transport/writer/namespace binding остаются blockers. Наличие fake dependency не должно снимать production CLI blocker.

`ops/docs/assemble.py:94–114` действительно принимает URL regex, не покрывающий actual `.gitmodules` URL с `.git`. Правильно оставить это отдельному assembler owner: в этом seam URL normalization не разрешена. Root scientific profiles/Core/Runner и recipe не требуют изменений для устранения двух замечаний выше.

## Метод и ограничения

Только именованные чтения, узкие текстовые поиски, SHA256, read-only Git metadata; записаны лишь этот review и companion identity в `/tmp`. Source/Git/CP/index mutations, scripts/imports/parser/compiler/tests/render/math/native/network/science и subagents — 0. Работа не выдаёт RED/GREEN/typecheck/runtime PASS. Проверено соответствие actual bytes и локаторов; independent reviewer не получил готового диагноза до собственного чтения.

Grant: 8 минут, 1 CPU, 1 GiB, reads ≤2 MiB, совокупный output ≤64 KiB. Именованные чтения/hash/search малы относительно read envelope, но physical I/O, peak RSS и точный transport output не инструментированы; строгий resource-enforcement PASS не заявляется. Initial broad `/tmp` discovery/truncation относится к **designer ledger**, было явно прочитано и не превращено в resource PASS. В данном review broad discovery не выполнялся. Старый DOC04 runtime 5/5 exhausted, product90/source9 history не изменён; нового runtime grant нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Этот design уже I-ready | R1: contradiction capture mismatch/error; R2: API/order merge не определён | Source design review, не execution | изменить |
| Owning builder и строгий transport seam пригодны как основа | Exact `ops/git.ts` и design §1–2 | Production binding отсутствует | сохранить |
| Source identity привязана к actual file bytes и позднему graph | Design §3, SHA256 actual источников | R1 требует typed observation contract; ABA/exclusivity вне seam | изменить |
| R1/R2 прежнего recipe закрыты source-only | Frozen v2 hashes и review 97f01e8b… | Нет нового runtime evidence | сохранить |
| Готовы all-recipe/native/render/assembler/shared-schema/BUILD/science | Отдельные source gaps и not_measured | Узкий review их не закрывает | данных недостаточно |

STOP: два адресных design correction; затем review того же минимального контракта, без реализации или исполнения здесь.
