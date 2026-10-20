# D6 — focused high lifecycle recheck

**Вердикт: PASS_SOURCE для D6 lifecycle amendment и начала source-only I2B.**
Блокирующий D5-R1 закрыт на уровне контракта: finish-validation ACK не требует
закрытия ещё живого driver, phase closure не требует пустоты общего cgroup,
а final setup receipt создаёт outer parent после producer/participants exit.
Новых блокирующих design findings в этом focused scope нет.

Предыдущий D5 review с CHANGES REQUIRED остаётся неизменяемым историческим
артефактом. D6 — точное дополнение, а не его переписывание. Все I2 R1–R9
остаются открытыми замечаниями к неизменённой реализации. Это не implementation
PASS, не build/compiler/test result, не native READY и не execution grant.

## Неизменяемые входы и фактический selected source

| Вход | Проверенный SHA256 |
| --- | --- |
| D6,22616B | `80509e2b9fc8725a6309733c6857a75657a640addcc7047e5199d21002ddbcc6` |
| D6 delta ledger,2833B | `9f1269f782a9534ff30b50f44e72a3cc836630eb7c663efbb1e5052a3c6d6932` |
| D6 identity,8368B | `8f4d8cee0262fa81fedefad33f8d805c83ffdb87b07f12b634e29e85e0a6c666` |
| D5 | `6049f427a10c769b69c2beaaa1374e583d217d6eb68926337204e560b824ed48` |
| D5 high review | `bb0319a40211616d36316c0adf04b8b0ac1f9bdefb8c71d274a96aecb3fd5d7d` |

D6 и ledger/identity прочитаны целиком. D4/D5 и собственные I2/D5 reviews
сохранены из предшествующих проверок; D5/D5 review hashes перепроверены.
Selected `/tmp/qcl-docs-test-routing-worktree` повторно имеет HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`, status5tracked+6untracked и8
прежних uninitialized gitlinks. Native Python/driver/pure helper/current fixture
hashes повторно совпали с I2; source edits не сделаны. Coordinator HEAD из D6
не подменяет selected source.

Ни scripts/target imports/parser/compiler/lint/formatter/tests/runtime/native/
network/server/build/solver/CI, ни source/fixture/CP/git writes не выполнялись.
Только read-only source/Git/hash observations и эти два review artifacts.
Консервативный новый read bound<1MiB (<4MiB), output<24KiB (<128KiB), wall<10min
(<12min). CPU/RSS/physical I/O не измерены. Субагенты не привлекались.

## Почему D5-R1 теперь закрыт в дизайне

**Command scope:** D6:9–21 явно сохраняет одну admitted workload cgroup со
всеми setup/driver/command участниками. Command owner доказывает EOF/own
descendants closure/supervisor ACK+reap, продолжая общие guard/events checks;
он не вызывает whole-empty при живом setup/driver. Setup participants — pinned
identities, не произвольный список исключений. Unknown identity запрещает pass.

**Driver finish:** D6:25–46 заменяет прежний `finished.terminal_ref` exact
`finish-validated` с bounded actual validation_ref и `terminal:false`,
`phase_closure:'pending'`, `setup_closure:'pending'`. Это receipt проверки
digest/plan/report/capture/source, без утверждения cleanup. Driver после
matching reply закрывает protocol и выходит; final phase/setup ref не ждёт.
Для positive validation exit0, для rejected exit1. Отказ durable publication
не создаёт фиктивный ref. Таким образом путь reply→driver exit достижим.

**Final phase:** D6:50–74 требует сначала driver stdout/stderr EOF, descendants
closure и reap, затем durable final phase receipt и client phase-complete.
Setup/broker, client и pinned task/job leaders в этот момент могут быть живы;
в receipt ровно `whole_workload_empty:'not_claimed'`. Client не принадлежит
закрываемому driver subtree и потому может получить outcome и выйти.
Positive preflight — prerequisites-only; check/docs phase не доказывает setup
closure. После первой фазы live setup допускает только следующую заранее
выданную фазу с сохранённой freshness/allocation, а не повторный token/retry.

**Setup shutdown:** D6:77–113 задаёт producer setup-closing с phase-set digest,
затем parent completion-ack с `disposition:'exit'`, без будущего final setup
ref. Parent не ждёт task/job exit перед этим ACK; producer не ждёт whole-empty
перед своим выходом. Затем outer parent отдельно закрывает producer и всех
оставшихся workload participants, дренирует/reap-ит, проверяет actual populated=0
и events, публикует final setup receipt. Producer не ACK-ает документ,
созданный после его выхода. `await_terminal()` возвращает именно parent-owned
final setup ref. Здесь нет await-ref/exit цикла.

**Actors/consumer:** D6:17,94,98,117–120 учитывает client/task/job/control
participants в той же allocation до их closure; только outer trusted parent
снаружи. Client phase exit позволяет underlying ops-ci/job продолжить и
завершить уже порученную работу. External wrapper получает underlying job
exit0 и отдельно final setup complete; final success не выводится из одного
client exit. Для direct check/docs parent ждёт task return и final setup proof.
Если actual installation не имеет такого wrapper, блокируется конкретный
native attempt; source contract не заменяется permanent refusal.

**Initial empty:** D6:21 снимает вторую форму самопротиворечия: начальную
пустоту проверяет parent до gated attach/exec. Native factory получает bound
observation и проверяет provenance/current membership/limits/authority; ей не
требуется увидеть пустой cgroup, содержащий её саму.

## Ошибки, дебиты и retained evidence не ослаблены

D6:34,64,73,96,111,124–130 сохраняет fail-closed outcome при wrong/partial ACK,
unexpected EOF, lingering descendants, OOM/guard/source/drain/storage/transport
failure. До matching completion ACK parent EOF — cancellation, после ACK
producer EOF только ожидаемый переход к reap, а не evidence success. Cancel/
deadline остаются действующими до завершения; budget не продлевается.
Unknown ownership не разрешает signal foreign processes или объявить allocation
освобождённой. Independent parent fallback остаётся после producer loss.

Предельный lifecycle metadata reserve посчитан последовательно:
131072+16384+32768+16384=196608B/phase; две фазы393216B; final setup32768B и
whole-empty evidence16384B дают442368B. Второй durable fallback требует ещё
442368B; lifecycle wire/history≤32768B резервируется отдельно в existing caps.
Это не дополнительный grant и не actual storage measurement. Полный schedule
с existing raw/command/index/startup/transport/failure debits должен fit в
actual storage/control metadata2MiB/history256KiB и исходный deadline до child.

При delivery failure после durable phase publication нельзя переписывать
immutable phase evidence. D6:73,96,119,128 требует прекратить следующие phases
и fail overall setup/consumer claim; ранее записанный positive phase receipt
сам по себе не повышает overall result. Writer должен сохранить эту границу
в finalizer и controls, включая failure после send/до client exit. Формулировка
`no positive phase` в D6:128 относится к разрешённому дальнейшему положительному
outcome, не к удалению/перезаписи уже сохранённого receipt.

## Точный I2B контракт для одного writer

Governing stack: D3, затем D4 overrides, D5 capsule/protocol/data contracts,
затем **D6 lifecycle overrides**. При конфликте terminal-empty/finished/
completion-ack применяется D6:19,25,88–113. Приоритет не распространяется на
ослабление остальных D4/D5 predicates. Не создавать новую trust architecture,
child cgroups или новый public schema ради terminal lifecycle.

Разрешённый source scope тот же: native Python/driver, узкий injected GitReader
seam, два native manufactured fixtures; tasks/ops-ci/workflows только при
необходимой D4/D5/D6 wiring correction. Exact12/three tools/nine pure exports,
D2 dedicated argv/maps/permissions, native16 closure, fixed13 seed, ancestral227/
current230 и original I1/I2/RED evidence сохраняются. Scientific/components/
server/platform/gitlinks/CP не входят в этот проход. Обычный healthy native
route при валидном trusted handoff обязателен.

Все I2 findings сохраняются как acceptance checklist реализации:

| I2 finding | Обязательство I2B, остающееся открытым |
| --- | --- |
| R1 | Active factory/context/broker/leader/ordered phases→actual executor; no permanent stub |
| R2 | Guarded first-fork lifecycle; multiplex cancel/drains; actual durable raw receipts/fallback; D6 scope-specific closure |
| R3 | Startup/capsule secrets отделены от allowlisted durable intents/logs; exact redaction spies |
| R4 | Closed exact unions/sequence/deadline, chunk≤32KiB,24MiB ledger, full pure Capture, compact finish-validation/phase/setup refs |
| R5 | Actual fixed16 HEAD/blob/working SHA binding; Git budgets/full schedule; owning sections/trimEnd/NUL; no default output bypass |
| R6 | Single owner reserve/debit before writes; bounded census allocation; disjoint storage; literal seed targets/modes |
| R7 | Trusted retained tool/runtime/KaTeX/count readers+registration; actual guard authority/delegation/freshness/control reserve |
| R8 | Independent exact Step translation; base parent-held pre-routing env; dedicated D2 maps unchanged |
| R9 | Paired manufactured source matrix: healthy dispatch exactly once, refusal zero forbidden dispatch, retained original/partial evidence |

Дополнить source matrix D6:130: две фазы на одном producer, preclosure ACK→driver
exit→final phase receipt, live setup без whole-empty claim, producer exit→outer
whole-empty, loss/timeout/cancel до и после ACK, lingering participants и
consumer rejection validation/phase refs вместо final setup ref.

Writer публикует immutable source report/identity/complete patch с actual hashes,
native16/full schedule/debit/coverage mapping и remaining gaps, затем STOP для
независимого CPP. Новые fixture counts — nominal source inventory с новыми
hashes;8+8/current230 не становятся observed результатами. Source-only I2B не
исполняет compiler/parser/tests или DEV controls. Root отдельно связывает
последующие finite compiler/DEV/pure GREEN планы. Native kernel/tool/wrapper
evidence и final CI/science остаются отдельными gates; source PASS их не
наследует и не расходует.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D5-R1 имеет достижимый terminal порядок | D6:25–113 explicit ACK/exit/phase/setup sequence | Только design, source не исправлен | сохранить |
| Живые setup/client/job учтены без ложного empty | D6:9–21,94–120 one workload + outer parent | Actual guard/ownership evidence позже | сохранить |
| Raw/failure closure и budget сохранены | D6:34,64,96,124–130 | Complete implementation schedule ещё нужен | сохранить |
| I2B можно начать по точному контракту | D3/D4/D5+D6 overrides и checklist выше | Один source-only writer, затем CPP | изменить |
|9I2 findings закрыты или native READY получен | Selected I2 source unchanged; execution0 | Review design не implementation/build/runtime | данных недостаточно |

STOP для Root назначения одного medium I2B writer. Новых execution/CP actions нет.
