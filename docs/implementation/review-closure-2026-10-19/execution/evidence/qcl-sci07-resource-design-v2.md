# SCI07 D2 — baseline-consistent admission и chronology erratum

2026-10-20. Narrow source-only override к immutable D1, не новая resource policy.
Применять D1 с заменами ниже; остальные sections, все7 SCI08 tickets,
scientific model/caps и native prerequisites сохраняются. D1/raw/ledger/identity
не переписываются. Runtime/native/parser/import/tests/build/network/server/code/
checkpoint/Git mutations не выполнялись. Статус **needs_admission/needs_guard**.

## 1. Frozen inputs и подтверждение review

| Input | SHA256 |
| --- | --- |
| D1 `/tmp/qcl-sci07-resource-design.md` | `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635` |
| D1 source ledger | `cf625aefd68f7335e34a5cb07900ee743e8e6ba45142bd79dbe99c26824fedfe` |
| D1 identity | `0d652cf597008ce67957d99c22e81a3ad147e31fd1ce620ed2dbdcff2b6b2479` |
| Independent high R | `48f97407846b4b179de2442e1295e8cc2028ed7d4e3ca9c2f28c8079ac5d4e67` |

R1 подтверждён сверкой с D1§6 и immutable Runnerfefaa27
`point_artifacts.jl536–545`, `scratch_execution.jl47–53,74–79`: total-budget
check включает used, free-space check требует только дальнейший growth/reserve.
D1 смешал эти baselines и мог ложно отказать при достаточном headroom. Это
conservative false refusal/неоднозначность реализации, не найденный cap bypass.
R2 подтверждён отдельным чтением **обоих** immutable Root trees e22 и469 ниже.
Проверка review не включает новый native observation или запуск scalar tests.

## 2. R1: замена admission inequality D1§6 и уточнение input obligations

Вместо одной строки `existing resident + ... <= min(total authority, remaining
free/quota, attempt bound)` применять **отдельные baseline-consistent predicates**.
Это также уточняет baseline Capacity row D1§4 и exact-fit правило D1§8.

Для каждого явно обозначенного attribution/authority scope и accounting view:

- `E` — уже materialized attributable resident на том же snapshot/epoch. Уже
  созданный stop payload, preallocated blocks и published/pending files входят
  сюда согласно своей logical/physical view; они не future growth.
- `U` — disjoint outstanding **ещё не materialized** growth reservations этого
  scope, кроме нового operation. Уже записанная часть переносится U→E, не остаётся
  одновременно в обеих величинах. Reservations других scopes учитываются в их
  authority/remaining-headroom mapping один раз.
- `P` — proposed **дополнительный** growth нового operation до его максимального
  simultaneous peak, сверх E/U; includes pending/receipt/pointer tails без credit
  за ещё не выполненный prune/replacement.
- `S` — ещё не materialized stop growth, не включённый в E/U/P. Disjoint stop
  payload/metadata уже занятый или зарезервированный другой строкой не прибавляется
  повторно. Time/CPU/read/write stop budgets сохраняют собственные D1 predicates.
- `G = U + P + S`, `T = E + G` — checked nonnegative finite sums; overflow,
  неизвестная единица/coverage/epoch или пересечение reservations отказывает.

**A. Total resident authority/cap:** `T <= A`, где A — **полный** assigned total
resident allowance того же scope/view, не remaining. Проверить отдельно attempt
cap128/256GiB, applicable assigned owner/per-FS total authority и shared campaign
sum≤2TiB по D1. Campaign E включает retained finals/failures/copies завершённых
jobs, campaign U/S — outstanding obligations всех scopes, а не только нового job.
Concurrent peak/lifetime и FS aliases/cross-FS copy rules D1 сохраняются.

**B. Independent incremental capacity:** `G <= H`, где H — **уже оставшийся**
allocatable physical/quota headroom соответствующего filesystem/quota domain
после materialized usage и disjoint protected/other reservations, но **до списания
ровно этих U/P/S**. E не добавляется в левую часть B и не вычитается из H второй
раз. Actual available/free уже исключает current allocated usage; quota remaining
уже исключает current quota usage в своём scope. Hard quota(total) и quota
remaining не взаимозаменяемы. Нет общего min между A и H. Min нескольких H допустим
лишь после доказанного совпадения domain/units/baseline; logical bytes, allocated
physical bytes и inodes проверяются раздельно, с собственным growth bound.

H обязан иметь provenance baseline. Canonical consumer input — remaining headroom
**before this scope's unmaterialized reservations**. Если retained authority
предоставляет уже net headroom `Hnet`, которое вычло идентифицированное подмножество
R из этих будущих U/S, нормализовать `H = Hnet + R` только при exact same-epoch
reservation IDs/coverage и доказанном disjointness. Равносильный контроль:
`G - R <= Hnet`, где0≤R≤G. R нельзя одновременно добавлять к H и снимать с G
в одном predicate; реализация использует canonical G≤H, второй вид только oracle.
Если baseline/IDs неизвестны — needs_admission, никакого guessed add-back.

R содержит лишь ledger booking, ещё не отражённый физическим расходом. Реально
materialized/preallocated bytes находятся в E и уже исключены из actual free;
их нельзя add-back как «reservation». Other-owner reservations не add-back в
текущий scope. Protected host/foreign/build/site reserves также не вычитаются
повторно, если уже учтены в authority Hnet: вход хранит перечень applied items.
Произвольный caller H/status не proof authority; signed/fresh BIND D1 обязателен.

Quota hard рассматривается только как total-domain bound на **полный current
quota usage этого domain**+его disjoint будущий growth. Нельзя вычислять quota
remaining из одного E attempt, если в quota domain есть другие данные. Потребитель
remaining input использует actual quota remaining и declared reservations, не
реконструирует чужую usage по догадке. Для inode capacity те же baseline правила
в counts; bytes и counts не складываются.

ПереносU→E после actual write сохраняет total accounting, но не является новым
budget grant. Snapshot free/quota и ledger reconcile должны описывать совместимое
состояние/in-flight bound по D1. Ни sampled observation, ни исправление double
charge не доказывает enforceable cap или исключение конкурирующих writers.

## 3. R1: exact-fit/one-byte-short source oracles

Это literal арифметика для SCI08-R2/P1/C1 controls, **не actual GiB availability**
и не выполненные тесты.1GiB=1073741824bytes; one-byte-short означает минус1byte,
не округлённый GiB. Старые pointer/receipt/pre-prune/overflow/unknown controls D1
сохраняются. Все остальные predicates считать удовлетворёнными только внутри
этого manufactured oracle.

| Case | Given | Required result |
| --- | --- | --- |
| Различающий double-debit | E=90GiB,U=4GiB,P=8GiB,S=3GiB,A=128GiB,H=40GiB | G=15GiB,T=105GiB; A и B проходят, хотя E>H. Старое105≤40 ошибочно отказывало |
| Exact total cap | Те же E/U/P/S,H=40GiB,A=105GiB | Total exact-fit проходит; incremental отдельно проходит |
| Total one-byte-short | Предыдущая строка, только A=105GiB−1byte | Отказ total predicate до writer; H не менялся |
| Exact remaining headroom | Те же E/U/P/S,A=128GiB,H=15GiB | Incremental exact-fit проходит; total отдельно проходит |
| Headroom one-byte-short | Предыдущая строка, только H=15GiB−1byte | Отказ incremental predicate до writer; A не менялся |
| Уже net reservation | E/U/P/S прежние;Hnet=11GiB, применённый R=U=4GiB;A=128GiB | H=15GiB,G=15GiB passes; эквивалентно G−R=11GiB≤Hnet. U не debit второй раз |
| Net one-byte-short | Предыдущая строка, только Hnet=11GiB−1byte | H=15GiB−1byte, incremental отказ; никакого silent add-back большего R |
| Materialized stop | Stop payload уже включён в E; будущий S=0 для этих же bytes | Не прибавлять тот payload ещё раз; отдельно зарезервировать лишь действительно будущие stop tails |
| Unknown/overlap/mismatched baseline | Нет reservation IDs/epoch, R внеG, materialized bytes выданы заR или unknown counter | Fail closed до operation, no numeric0/unlimited/fabricated fit |

Для physical view P/S должны быть proven physical upper bounds с metadata/
allocation overhead; logical uncompressed inventory не выдается за exact free
space demand без owning mapping. Paired inode/logical/physical controls используют
свои единицы. Все7 tickets сохраняются; у SCI08-R2/P1/C1 добавить именно эти
baseline normalization и scalar-pair controls, не новые scientific assertions.

## 4. R2: точная chronology и новое forensic handoff binding

D1 описывает **initial** published Root e22 и selected owning overlay, что было
верно на первом наблюдении. В его identity `metadata_snapshot_later.head` уже
содержит469; поле `metadata_snapshot_later.published_gitlinks` было получено для
**e22**, указанного в `published_root`, а не для later HEAD. Такое соседство
неоднозначно. Оно не является `git ls-tree 469`. Не исправлять historical bytes;
этот D2 задаёт явный erratum и independent derived tree binding.

2026-10-20 source-only повторно установлен actual managed HEAD
`469ef4ec36c1dfb967856108e5f9455429559c15`. Read-only `git ls-tree` каждого **exact
ref** дал:

| Component | Initial published e22 | Later published469 |
| --- | --- | --- |
| Core | e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee | 9f4a96d032ad868ec010ce92d915bb81087c8d92 |
| Runner | 1acc165650fd4f4c2d49605cc679f90e3f6fcdae | fefaa27f194bfddf85dd51a0e255beef2218c06d |
| Platform | f5bc368654414039f7368bb19ca3201fa7f29f9d | f729e2681224d6537538179ab760fefefd575003 |
| AiiDA | d8f8092ca1c76523d85384b4bac8198d8bfa736b | d8f8092ca1c76523d85384b4bac8198d8bfa736b |

Другие4 gitlinks неизменны между этими refs; exact8-entry raw tree outputs
сохранены в D2 identity как forensic observations. Это **Git-derived evidence**,
не второй вручную поддерживаемый composition lock. Named owning pins и source
hashes D1/R совпадают с actual469; source resource audit не переносится на иные
коммиты. Для handoff считать469 опубликованным source graph observation, а не
продолжать называть эти Core/Runner/Platform refs неопубликованным overlay.

469 не объявляется final ready release, clean coordinator state, installed runtime
identity или native resource admission. D1§10 «нет final graph/admission» следует
читать так: published469 graph теперь установлен; **final Code/release/plan/runtime
BIND и SCI07 admission не установлены**. D1 initial e22/candidate statements
сохраняются историческими. Оngoing coordinator files/Contracts/untracked code не
становятся science input и не редактируются этим D2.

Coordinator сообщил частичные READ_NATIVE observations: подключён hypervisor,
32CPU/12VM configuration/storage observations, matching historical named VM IDs
stopped; control/compute SSH NoRoute. Этот агент не читал их raw/native receipts
и не проверял host/allocation ownership. Эти сообщения не заменяют fresh actual
worker/cgroup/NFS/quota/counters/leases/stop proof, не дают разрешения начать VM,
отменять jobs или reclaim disks и не принимаются как32 available CPUs/READY.
D1 missing-input status уточняется как отсутствие **полного scientific admission**,
а не отрицание существования любых новых platform observations у coordinator.
Никакие private hosts/credentials/inventories в этот source packet не копируются.

## 5. Preserved scope, ресурсный предел и STOP

Без изменений:0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy,
electron_electron=none;13attempts/936executionnode-hours,72h per attempt,
concurrency≤2, one threaded process/node, BLAS1; W1 128GiB/2TiB writes/4TiB reads/
1GiB logs; остальные9 256GiB/4TiB/8TiB/1GiB; shared2TiB/44TiB/88TiB/13GiB.
Stop reserves внутри caps, no physics/grid/basis/window/mixing/threshold edits.
Все7 SCI08 tickets conditional source-I ready после принятия D2/highR; native
proof и отдельные finite test/fault grants не выданы. Исчерпанный C08 не
открывается ссылкой на его fixtures, source correction не расходует новый test.

D2 envelope≤10min/1CPU/1GiB/read1MiB/report96KiB. Читались D1/R/hash metadata,
два коротких immutable Runner source ranges и два exact Git trees; full-file
charge/read ledger в identity. Target execution/native/parser/tests/build/network/
server/code/checkpoint edits0. D1/source ledger/identity/review preserved unchanged.
Physical I/O/RSS не измерены; не выдавать source result за enforced native cap.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 double-debit неоднозначность устранена | Separate T≤A иG≤H, exact normalization иscalar pairs§2–3 | Source contract/oracles не исполнены | изменить |
| R2 chronology уточнена без смены owning source | Exact git ls-tree e22/469 итаблица§4 | Published source graph не runtime/final release proof | изменить |
| Частичные native observations дают SCI07 READY | Полного allocation/storage/counter/stop admission нет | Нативное свидетельство агентом не проверялось | данных недостаточно |
| Семь SCI08 tickets/S1 scope сохраняются | D1 + узкие overrides§2–4 | needs_admission/needs_guard остаются | сохранить |

STOP: frozen D2/identity/delta для того же independent high R; никакого runtime
или SCI08 implementation этим документом не начато.
