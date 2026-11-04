# Наблюдаемый выбор: metadata budgets, provenance и поздняя интеграция

Статус: evidence-only draft для Root/privacy review, 2026-11-04. Код и infrastructure оставлены как
есть. Новые tests, solver, PG, build и benchmark не выполнялись. Этот разбор дополняет отчёты04/05;
он проверяет решения по первичным user records, видимым действиям инструментов, Source и receipts,
не восстанавливает внутренний ход мыслей.

## Ответ на основной вопрос

В выбранном A/B подграфе преимущественно разрабатывалась **инженерная инфраструктура научного
приложения**: конечный admission metadata, filesystem/actor guards, сериализация, identity joins,
output lifecycle и provenance. Это не расчёт scattering, SCBA/Poisson или физической наблюдаемой.
Доменная часть существенна: consumer обязан связать конкретные QCL plan/result/state declarations и
сохранить происхождение отрицательного результата. Но сама ручная модель W, механизм terminal ledger
и большинство transport/path guards — общие инженерные механизмы, а не следствия физического
уравнения. Называть весь проект «только general-purpose кодом» было бы неверно; вывод относится к
этому ограниченному подграфу.

Документированное обоснование локальных решений есть: реальные отказы, cost inventory, конечная
allowance card, отрицательные controls, независимая арифметическая поправка. Однако в этой выборке
**нет сравнительного свидетельства**, что именно такая полнота ручного nonrefundable учёта была
необходима для ближайшего полезного исследовательского пути. «Exact patch имеет корректный конечный
контракт» и «этот слой стоило разрабатывать в таком объёме до сквозной эксплуатации» — разные
утверждения. Первое частично подтверждено; второе остаётся архитектурным вопросом, а не
установленным оправданием сложности. [D01–D05]

## Метод и предел достоверности

Перед чтением primary session journal измерен:519123914B,495.08MiB. Использовалось потоковое чтение
отдельных JSONL records с ограниченными окнами/селекторами; каждое выводимое текстовое поле не
превышало500 символов. Полный журнал, raw messages и inputs не экспортировались. Для выбранных
records сохранены в этом отчёте только line/time, парафраз и SHA256 исходной строки с завершающим
newline. Времена ниже — UTC. Локатор самого journal удерживается в private inventory; home/session
identifiers сюда не перенесены.

Из анализа исключены private analysis/reasoning, их summaries и encrypted content. Некоторые
аргументы межагентных сообщений в primary log зашифрованы; они не расшифровывались и не служат
доказательством содержания поручения. Видимый agent final report — сообщение о результате, а не
первичный trace его внутренних tool actions. Где исполнение подтверждает receipt, это отмечено
отдельно. Текст публичного commentary подтверждает объявленное намерение, но не автоматически
завершённое действие.

Это последовательная ретроспективная проверка с доступом к предыдущим04/05, поэтому её независимость
меньше blind review. Отсутствие найденного сравнения альтернатив в ограниченной выборке не означает,
что его никогда не было. Scope: A/B accounting, границы Native/L, fixture→actual join, identity и
reviewer corrections; не census всех решений недели.

## Требования менялись; поздний текст нельзя переносить назад

Первое user поручение27 октября запускало программу упрощения с широкими полномочиями на необходимые
изменения, builds/checks, synthetic jobs и установку; routing делегировался исполнительному плану.
[J01] В initial commit `69d841fdd0fa84f835803560faf80bcfd682679c` исполнительный план требовал
переиспользовать native Nix/systemd/Slurm/backend API. Это основание оценивать цену собственных
mechanisms; одновременно первоначальная программа уже включала независимые consumers, provenance,
recovery и несколько backend. Она не была задачей «сделать только solver».

30 октября пользователь прямо разрешил самостоятельно менять странные лимиты по собранным фактам.
[J02] Это контрсвидетельство против версии «любое увеличение cap нарушило исходный запрет».
Разрешение не указывало модель W и не объявляло всякий новый formal guard необходимым prerequisite.
Происхождение раннего A16 как конкретного числа в этой выборке не реконструировано.

31 октября primary question-reply user envelope подтверждает единоличное администрирование. [J03]
Это сужает гипотезу о нескольких независимых администраторах. Оно не доказывает отсутствие foreign
VM, shared storage, повреждённых inputs или конкурентных процессов и само по себе не отменяет
identity/ownership checks.

2 ноября пользователь исключил обновление приложения при работающих jobs. [J04] Это **действительное
сужение прежнего требования**: initial `project-simplification` line71 допускал отдельные
совместимые web/docs updates без остановки science; commit
`2ff7baa92ad3b4886646e825d54b61fe4f95339a` заменил это whole-cluster maintenance после остановки
jobs. Исполнительный `codex-execution` в этих двух commits побайтно одинаков; изменение находится в
`project-simplification` и operator documentation. Приписывать maintenance-only самому исходному
плану было бы ошибкой. [S01–S03]

3 ноября пользователь поставил в приоритет развёртывание кластера и пробное исследование при
отсутствии ближайшего sudo; затем запросил самодиагностику полезности и чрезмерной детализации.
[J05–J06] Это приоритет результата и требование анализа. Оно не делает прежние подтверждённые
integration failures выдуманными. Но продолжение деталей как обязательного критического пути
требовало связи с этой основной целью; одной локальной корректности patch для этого недостаточно.

## Что видно в действиях3 ноября

В17:16 commentary сообщил о genuine вычислительном проходе и новом барьере Results128: около145MiB
workspace accounting. В17:32 был объявлен следующий join: настоящий final→Results→AiiDA→readback.
[A01] Сохранённый producer receipt подтверждает CLI exit0/305.704с; физическая приёмка из него не
следует. Results receipts подтверждают конкретные closed160/16 metadata reads и selected logical
bytes0. [D01, D06]

Это показательный поздний interface mismatch: Source и fixtures уже существовали, а genuine metadata
впервые показали несовместимые lifetime/workspace allowances. Называть его чисто fixture noise
нельзя. Но также нельзя доказать, что любая более ранняя integration попытка непременно его
обнаружила бы: точного контрфактического запуска нет.

После потери terminal status full Results attempt3 commentary17:43 отказался считать suite успешным.
Следующий **видимый tool call** создал конфигурацию durable attempt4; итоговые receipts4/5/6
сохранены. Это подтверждённая смена способа supervision, а не только обещание «учесть ошибку».
Причина исходной потери terminal не установлена. [A02, D07]

В18:19 видимый tool call записал основание interruption attempt5 после independently reproduced
environment failure. В18:21 другой call зафиксировал Source freeze после узкой fixture
correction;18:22 call запустил attempt6 с trusted fixture parent и exact dependencies. Здесь есть
последовательность «наблюдение→различающий control→изменение fixture/environment→реальный повтор»,
при сохранённых production guard и failed originals. [A03–A04, D07]

По A32 primary agent final18:03 сообщил REFUSED/HOLD;18:09 Root tool call прочитал report/analysis.
Это прямое свидетельство того, что failed diagnostic был принят как input следующего решения, но
root journal не содержит его внутренних execution calls. Их заменяет не предположение, а сохранённый
diagnostic receipt. A32 отказал до Results; logical debit lower bound49434257W, wall5.638с,
instrumented whole-process RSS180.5MiB. Opaque heap remained unknown. [A05, D02]

Далее18:24 передана finite card,18:28 reviewer подтвердил исправленную offline арифметику,18:29
публично объявлено начало scoped implementation.18:41 сообщено о frozen implementation,18:46
независимый final подтвердил43PASS и отдельно отсутствие full-suite/actual128/512/Native pass. Это
наблюдаемый design/review цикл, но ни его наличие, ни43PASS не означают оптимальность выбранной
архитектуры. [A06, D03–D05]

В18:43 видимый readonly SQL tool call проверил состояние исходного CalcJob с
`SHOW transaction_read_only`; он не создавал missing outputs. Fresh driver был подготовлен отдельно.
В19:02 финальное сообщение всё ещё признавало отсутствие готовности к пробному исследованию. После
user audit запроса19:04 tool call19:11 зафиксировал prepared-not-run состояние, отсутствие active
native operation и read-only дальнейшие действия. [A07–A08, D08, D10]

## Матрица: выбор, предположение или изменение scope

Категория **explicit reasoned choice** здесь означает доступное внешнее обоснование выбора; не
утверждение о private thinking.

| Предмет                                                                  | Наблюдаемое основание                                                                           | Классификация и предел                                                                                                                            |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Увеличить selected A и B конечным образом                                | Genuine A16/A32 refusals; Source inventory; accepted one-context card                           | **Explicit reasoned choice.** Числа128/512 подкреплены этим operand, а не произвольным «пока не пройдёт». Actual fit ещё неизвестен.              |
| Считать полный ручной W accounting обязательным для любого первого trial | Есть подробные local contracts, но нет сравнения стоимости с более узким scope/native isolation | **Unsupported assumption**, если заявляется такая универсальная необходимость. Это не доказательство ненужности каждого guard.                    |
| Сохранить public actor/Root/default16                                    | Scoped Source и controls; первый lookup `min(MAX_METADATA, remaining//4)`                       | **Explicit reasoned choice:** lifetime не расширяет privileged per-call authority. Не зафиксировано actual privileged leakage.                    |
| Принимать результат только после successful close/readback               | Constructor/late-close controls, типизированная creator/source identity                         | **Explicit reasoned choice** для заявленного provenance contract. Не физическая сходимость и не Native qualification.                             |
| Обосновывать текущий scope immutable исходным планом                     | User caps permission, sole administration и maintenance-only narrowing                          | **Requirement broad/narrow.** Последнее применимое поручение меняет прежний scope; запрет на live updates нельзя задним числом объявить исходным. |
| Предположить, что mocks/unit GREEN гарантируют genuine join              | Actual consumers отказали;43PASS имел explicit Source/L scope                                   | **Опровергнуто как гарантия.** Не установлено, что такой гарантией пользовались сознательно.                                                      |
| Утверждать «решение не осмысливали» или «агент понимал все alternatives» | Есть документы, reviews, commentary; часть private сообщений opaque                             | **Unknown thinking.** Возможна только оценка предъявленного обоснования и действий.                                                               |

## Ручной W и Native isolation отвечают на разные вопросы

Owning Source: AiiDA base `336358dfd10c698e4b4a71d8c93562aaa8ee7182` плюс frozen overlay `061dd7cf`;
это не installed/publication claim. Symbols: `native_actor.py::_Reads`,
`native_backend.py::_Operation`/`_Packet`,
`saved_sources.py::_NativeLedger.reserve`/`_native_readback`. [D04]

Source `_Reads`/`_Operation` списывает оценки metadata до работы, B `_NativeLedger.reserve`
удерживает shared credit, а failure terminal и nonrefundable. Это даёт наблюдаемый controlled
refusal и ограничивает заявленный pipeline. Native filesystem/actor/namespace checks проверяют
authority, identity и состояние ресурсов. Они не являются измерением памяти, как и W не является
доказательством namespace isolation.

Finite card для одного context/RowKey дала A≤67491741W, main B≤516954064W и offline≤297959080W. B512
— **536870912W logical allowance**, не512MiB измеренной RAM. В модель входят фиксированные
Results160MiB, binder96MiB, A lifetime128MiB, copies/aliases/output/readback. Их сумма не есть
resident peak. Реальный process RSS, физический IO и repeated logical debits имеют разные scope.
[D02–D04]

Независимый reviewer нашёл omitted offline projection10672W; original revision сохранена, offline
total исправлен, main total не изменился. Это конкретная польза formal review. Но корректность суммы
не доказывает, что сумма — минимально необходимая operational abstraction. Source остаётся opaque к
части ORM/interpreter/native heap; его unknown не заполняли0. [D03]

Вопрос из05 о native process/cgroup limits остаётся вопросом. Такие limits сами не устанавливают
конкретный QCL creator, StateRef и неизменность bytes; удаления identity guards из него не следует.
Обратное утверждение — что каждую ручную forecast/copy charge невозможно заменить более простым
bounded input contract или native resource boundary — тоже здесь не доказано. Сравнительного
design/evidence нет в рассмотренных материалах; официальные OSS references вынесены в отдельный
отчёт12.

## Цена тестов и исправление требований к evidence

Результат Results1604PASS/49SKIP подтверждает exact corrected suite. Earlier full4/5 потребовали
около32.6мин wall до final6; часть усилий ушла на socket path, trusted ancestor и права
intentionally mutable fixture copy. Реальные guard failures полезно отличать от нарушения условий
самого теста. Полный AiiDA suite не GREEN:15 failures совпали с baseline; это attribution, не
разрешение их игнорировать. [D05–D07]

Таким образом review был полезен на двух уровнях: находил actual accounting/lifecycle defects и
предотвращал false-pass attribution. Хуже подтверждён третий уровень — ограничение необходимости
очередного слоя и порядка работ. В выбранной хронологии новый actual join оставался открытым после
локальных43PASS; этот факт важнее увеличения числа проверок.

Для дальнейшего независимого анализа уже есть дешёвые различающие материалы: initial/maintenance
Source diff; первичные user records; A32 failed receipt; corrected card и review finding; unchanged
Source hashes при environmental controls; prepared-not-run manifest. Они позволяют спросить, какие
guards находились в ближайшем пользовательском call graph, какие защищали заявленный failure mode, и
где локальный completion подменял operational readiness. Нового implementation плана или запуска эти
вопросы не разрешают.

| Утверждение                                | Свидетельство                                         | Ограничение                                          | Решение                  |
| ------------------------------------------ | ----------------------------------------------------- | ---------------------------------------------------- | ------------------------ |
| В этом подграфе много общей инфраструктуры | Source symbols, W/lifecycle/transport model           | Есть QCL-specific identity semantics; не весь проект | сохранить различие слоёв |
| Требования были неизменно противоречивы    | Initial plan и более поздние user changes различимы   | Не все решения недели исследованы                    | изменить такое обобщение |
| 128/512 полностью произвольны              | Refusals, finite card, reviewer correction            | Runtime fit не доказан                               | отвергнуть это обобщение |
| Ручная модель такой полноты необходима     | Только local correctness, без сравнительного evidence | Native alternative не оценена этим отчётом           | данных недостаточно      |
| Source/L успех означает готовую науку      | Explicit gaps, prepared driver                        | Нет завершённого full typed/Native/scientific gate   | не утверждать            |

## Локаторы и hashes

Первичный journal не публикуется. `J`/`A` ниже — line numbers его JSONL records; timestamps и
парафразы даны выше. Hash относится к одной raw record строке, не ко всему растущему journal. `D` —
локальный packet; его private operational contents не являются приложением к публикации.

| ID  | Record line / UTC timestamp       | SHA256 raw record                                                  |
| --- | --------------------------------- | ------------------------------------------------------------------ |
| J01 | 9 / 2026-10-27T19:03:45.327Z      | `9b5c45fa0d3cf721deb08255b303fb3dafdbb06b8dc38f2905b62b4d27a1691a` |
| J02 | 49466 / 2026-10-30T14:03:09.672Z  | `ee337ae10992eba835c35a5aa3a680193e45c6c22b408e3ccc92c17f11729550` |
| J03 | 72526 / 2026-10-31T17:55:39.032Z  | `cd2b2f3d6ddecb2662ab8d22b2a1d3315096ced24e4433a33b002ff2d1f10b8d` |
| J04 | 104921 / 2026-11-02T15:46:53.204Z | `837f4004ac05ba4827d09c015601b459b8222c6b6481c7cd3990e18a0ad63d7c` |
| J05 | 118007 / 2026-11-03T15:12:53.926Z | `7f90d5a435706a6ba6260fea49e7f4b74ad2f02f3a8c2dfa0894c2d8a2ed2149` |
| J06 | 122539 / 2026-11-03T19:04:52.717Z | `aba117c0e188df51a0d1a7851800e8b8b9438c347b50de202e0762e35a59d1d1` |
| A01 | 120147 / 2026-11-03T17:16:10.623Z | `1e548a93fffb912ec410cebccbcc4a3c4d9b44218e36c68c26c9205f99989b58` |
| A01 | 120684 / 2026-11-03T17:32:31.469Z | `4ed1ee5e9d390ebe0a77da5d7344e1d5a0240d739f73ded7bf88ebfb94fe4110` |
| A02 | 120906 / 2026-11-03T17:43:01.378Z | `285fbec7082cdeb4d76fbb8501c6d2fbc9bd746244225aef2c5b79400edc56fc` |
| A02 | 120907 / 2026-11-03T17:43:17.968Z | `1f18ca001b63f8cf1be1eca40ce6dac50f0b8db2ae278a9c72dcde4cf9d198f9` |
| A03 | 121588 / 2026-11-03T18:19:07.287Z | `7fd7969c0dde94d1fccf42e993ced040b2860c6ea42f1b437f2cc734c6c36dc6` |
| A04 | 121654 / 2026-11-03T18:21:55.727Z | `18ee864506f154ba16e1c1dfc1b8fb24fb7128f5668de5cf1861906da0c813a7` |
| A04 | 121673 / 2026-11-03T18:22:52.169Z | `9ef29ce7afbefd7bbded3e5c8962a09f7d3ea80300606219f239e7b9edbb753f` |
| A05 | 121248 / 2026-11-03T18:03:14.337Z | `53254c006228513ff25d8a66fc826709c83613dce0fb2f9dd73e1698e85bd078` |
| A05 | 121300 / 2026-11-03T18:09:45.454Z | `d408ab98a5e280271068ccb2c95c0228cffc59bf734e4b741294233f006f7c79` |
| A06 | 121716 / 2026-11-03T18:24:13.871Z | `7ab4a8e215561c082a5610ba4ec94fbe3ad32355a0df88fe30668cbcb176ab30` |
| A06 | 121828 / 2026-11-03T18:28:31.811Z | `70adbe6898085c429a77e180c3fd3d8cdd4c1333fddf65e00a08330f175ef555` |
| A06 | 121864 / 2026-11-03T18:29:38.292Z | `393a9f1b75e04ab56dbdf330de3d3766e8ab5da6b45ceec26fe42c926a1f739d` |
| A06 | 122096 / 2026-11-03T18:41:15.409Z | `03c84d4a41f530c48f97c9b514770adedeec3ac32cb294441b64ebc16d5728cc` |
| A06 | 122204 / 2026-11-03T18:46:01.272Z | `4600196805d0f297348cee443887e39ae8259631b637e2f5f8bbc050f30cb5d1` |
| A07 | 122165 / 2026-11-03T18:43:52.903Z | `e69ed482b4d38181b3695230d76171dbf073d5b94e08b33597e95b781ec08e85` |
| A08 | 122497 / 2026-11-03T19:02:41.427Z | `e2badefa0749b6325ce0dcd774535a7f0b852a6e7720483fdb3dcd7b86531567` |
| A08 | 122744 / 2026-11-03T19:11:42.625Z | `f23a8e0f05730d63667e42ac2bb06554e3368535a60e2a808ecb9bf1547af5c7` |

Исторические Source версии (hash файла, извлечённого read-only из Git):

| ID  | Commit / path                                                                                       | SHA256                                                             |
| --- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| S01 | `69d841fdd0fa84f835803560faf80bcfd682679c:docs/implementation/codex-execution-2026-10-27.md`        | `a589668d561726652250730e96ba67eb272813faae4d811e012750f4abba9b29` |
| S02 | `69d841fdd0fa84f835803560faf80bcfd682679c:docs/implementation/project-simplification-2026-10-27.md` | `ab945b0190548ca4f8f82dd8ea083199af6caf63fe4be2907b96b2ce78b90b99` |
| S03 | `2ff7baa92ad3b4886646e825d54b61fe4f95339a:docs/implementation/project-simplification-2026-10-27.md` | `e37f22090c2f93474d66d6c133185a938afe7fbd94a94b0a868779ce547bfa83` |

Префиксы локальных packets, относительно корня repository:

- `P` =
  `.build/P04-P05-Root127-AiiDA-actual-final-allowance-20261103/interop/actual-capture-attempt1`
- `A` = `.build/P07-Root127-selected-access-actual-lifetime-measurement-20261103`
- `C` = `.build/P07-Root127-selected-access-allowance-card-independent-review-20261103`
- `I` = `.build/P07-Root127-selected-access-scoped-allowance-implementation-20261103`
- `IR` = `.build/P07-Root127-selected-access-scoped-allowance-independent-review-20261103`
- `R` = `.build/P04-P05-Root127-actual-final-Results-arena-independent-review-20261103`
- `F` = `.build/P04-P05-Root127-Results-full-durable-20261103-`
- `D` = `.build/P07-Root127-A128-B512-fresh-typed-chain-20261103`
- `B` = `.build/session-evidence-publication-20261103/drafts`
- `N` = `.build/P07-Root127-original-calcjob-readonly-status-20261103`

| ID  | Локальный source                                                             | SHA256                                                             |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| D01 | `P/producer-receipt.json`                                                    | `01a727c843e18c4a8196cd9335c0f492529cb37e3b2956735a1a54fd4fc1552d` |
| D02 | `A/analysis.json`                                                            | `12dd1de00c8e54984e53c8c48c975b79f44b86681c6ba33097465b17be4a74c9` |
| D02 | `A/report.json`                                                              | `d7390b664d7111dd1cfb63e9376ae083b904b4ea7381644f10cdc337bacebd70` |
| D03 | `C/decision.json`                                                            | `50d395edf55e9f4674734ce293c1b587b99fc14994ce8c83b3a752cbff6699d7` |
| D04 | `I/source-freeze.json`                                                       | `061dd7cf4c6fd053f11328ad942d07660dbcad33e68ac465961a68585a7f5bf4` |
| D04 | `I/REPORT.ru.md`                                                             | `4fec3ca4fd47c335d4d2fe60d642ff4e2484807b05fa955f41b8936420130879` |
| D05 | `IR/decision.json`                                                           | `3d5d2d9689b1572b94f88eac9020f5686144cfd273531c555e5e23dbce93c4e4` |
| D06 | `R/verification.json`                                                        | `f06c3b4501eeb019990840efc0852dc0cc93fed54c669c1cf707a95e3a992e00` |
| D07 | `.build/P04-P05-Root127-Results-full-durable-20261103-attempt4/receipt.json` | `6d92b49c09238f697a2ca1133a5a43dfc132498723feb8e82231f59bba1833d2` |
| D07 | `.build/P04-P05-Root127-Results-full-durable-20261103-attempt5/receipt.json` | `4682bc46174833ba1a50a7cdd728bd473a9c95206251a2738828e87ad30c7944` |
| D07 | `.build/P04-P05-Root127-Results-full-durable-20261103-attempt6/receipt.json` | `7fe4a48e5a829db185edbac48b29a171d4d292868dafca06f22c8825e406ac86` |
| D08 | `D/manifest.json`                                                            | `4464844ecb2607c6ef9d506de28d0d4cf38c939de73da35360f7970b7daf82bd` |
| D09 | `B/04-integration-failures-and-testing.md`                                   | `22c98148dbf6457d4dd83000df15a20c737dce2e095f579a69b7e34d9c1471b0` |
| D09 | `B/05-process-findings-and-analysis-questions.md`                            | `24b0e68d199fb0c958ebf89c9ec3b95bf49c5286567e86e0b3e7e4e06da0fb58` |
| D10 | `N/receipt.json`                                                             | `0f3ab03b02b48161a52bfb784e94f4b2aa59d5e3fc3beb71f7019d805a63c15d` |

Текст содержит только парафразы выбранных требований/действий. Operational IP/UUID, home paths,
session identifiers, private reasoning и содержимое inputs/arrays не публикуются. Итоговый
Root/privacy review ещё требуется.
