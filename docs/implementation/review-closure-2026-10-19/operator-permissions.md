# Согласованные разрешения оператора: пакет P1

**Дополнение 2026-10-24: принято упрощение контроля ресурсов.** Действует
[ресурсная поправка](resource-policy-2026-10-24.md) для initial/production S1.
Исторические PLAN/standby ниже не отменяют позднейшие активированные grants;
их повторное утверждение не требуется. Scientific criteria и technical BIND
с fresh admission сохраняются; поправка сама по себе не является runtime READY.

Подготовлен и согласован **2026-10-19**. Статус: **approved_standby**.
Оператор явно утвердил B, выбрал G1 и S1 с уточнением «без электрон-электронного
рассеяния»; точные ответы приведены в decision table ниже. Сейчас действует
**PLAN**; product code, tests/imports/install/build, server и solver не выполняются.
Отдельным запросом пользователь поручил публикацию handoff и public review
в отдельном docs-only PR; это не activation общих DEV/BUILD/OPS/SCI/MERGE прав.
Согласованный пакет остаётся **approved_standby** до отдельной команды
начать исполнение. Подтверждение пакета и команда начать — разные решения.

Вход: [главный handoff](README.md), [действующие правила проекта автономии](autonomy.md),
[инфраструктура](platform-worker.md), [научный каталог](science.md),
[документация и инструкции](documentation-instructions.md).
Документ уточняет условия будущей активации; не создаёт второго workflow,
issue tracker или source lock. Operator decisions и runtime bindings затем
ссылками входят в один coordination checkpoint.

## Что уже установлено и не требует повторного вопроса

- Полный scope review, работающий подключённый кластер, выдаваемый дистрибутив
  worker с инструкцией, convergence studies и попытка физической приёмки.
- Финансовый compute cap пользователем не установлен. Свежие CPU/RAM/storage,
  конечные попытки и stop criteria обязательны; общий бюджет не умножается на агентов.
- Выбранная Sol и роли: design/docs `ultra`, implementation `medium`,
  coordination/audit/independent review `high`. Другая модель молча не выбирается.
- Физика, scientific truth и scope не меняются ради pass. Foreign VM/jobs,
  исходные arrays/provenance, secrets и fixed light theme защищены.
- Сервер недоступен; сообщение пользователя об отсутствии работ после review
  не устанавливает live state. Сейчас probes не выполняются.

## Как устроено условное разрешение

Оператор утверждает **класс действий + область + условия + конечный envelope**.
Перед каждым действием координатор и независимый reviewer привязывают это
разрешение к фактическим source/targets/resources и сохраняют receipt.
Hash будущего релиза — вычисляемый факт, а не новый вопрос о намерении оператора.
Разрешение не требует выдумать hash или допустить unknown как pass.

**Согласованное уточнение autonomy:** для утверждённых B/G1/S1
пунктов CP-OPS и CP-SCI имеют human policy approval здесь, затем техническую
стадию `BIND/READY` на конкретных данных. Новый вопрос человеку не нужен, если
все утверждённые predicates доказаны и scope/envelope сохранён. За пределами
этих полномочий требуется новое решение оператора. CP-START по-прежнему
требует отдельной команды начать.

Недостающий измеримый факт агент добывает сам в active read scope. Недоступный
факт останавливает зависимую операцию. Новый target за пределами разрешённого
множества, изменение физической цели/доверия, destructive exception или
превышение конечного envelope требуют нового конкретного решения.

## Полный список решений

Ниже зафиксированы **утверждённые B/G1/S1**, пока без активации EXEC.
G0/G2 и S0/S2 сохранены только как невыбранные альтернативы; они прав не дают.

| ID | Предмет | Предлагаемое условное разрешение | Граница / что останется оператору |
| --- | --- | --- | --- |
| PERM01 B | Scope и старт | Все 75 карточек; обратимые internal design choices решают owning D+R. Начало только отдельной командой | Новый domain/scientific target, отказ от required backend, конфликт primary requirements |
| PERM02 B | DEV и окружение | Root + восемь owning components, изолированные `codex/` branches/worktrees, code/docs/AGENTS/skills по плану, local commits, locked env и meaningful checks | Unrelated edits, global account/config/security changes, dependency/model drift ради запуска |
| PERM03 B | Draft publication | Push собственных feature refs, focused draft PR, обновление existing PR6 и handoff docs ref; root выбирает опубликованные gitlinks | Нет force/shared-history rewrite, сторонних сообщений, нового repository/публикации private inputs |
| PERM04 G | Merge | **Выбран G1:** coordinator merge owning/root PR после independent CP-CODE, required checks/protections и exact reviewed head | Public release не входит; bypass protections/force запрещён |
| PERM05 G | Public release | **G1:** подготовить весь release dossier и частную доставку, финальный public publish отдельно оператору | G2 не выбран. Новый публичный канал/аккаунт/домен, секреты, перезапись published tag/artifact не разрешены; partial release нельзя выдавать за full |
| PERM06 B | READ_NATIVE | Bounded чтение already trusted QCL site, protected inventory и existing credentials без вывода secret bytes; fresh admission перед операцией | Нет проб по недоступному серверу сейчас, auto-accept host key, произвольного нового endpoint |
| PERM07 B | BUILD | Fresh safe maximum CPU/RAM на designated builder, preflight namespaces/privileges, immutable builds и private candidate staging; finite B-envelope ниже | Foreign allocations, disk reserve, privileged access outside approved builder/targets, build counter/space overrun |
| PERM08 B | Rehearsal и fresh install | Создать/установить named campaign-owned isolated VM/volumes в approved QCL pool; Proxmox, существующий Arch/libvirt route и обе required Windows/Hyper-V machines | Нельзя выбрать неизвестный physical disk; unsupported host оставляет backend pending, scope не уменьшается |
| PERM09 B | Maintenance и ресурсы | Самостоятельно выбрать безопасное окно при отсутствии protected workloads; pause/resume writers, backup, stop/reboot/resize QCL VM, update/rollback, native checks и возврат production allocation | Ни foreign VM/jobs, ни offline enrolled node не исключаются молча; потребность прервать чужую/старую работу — оператору |
| PERM10 B | Operator cancellation | Явно поручить агенту роль operator для cancel **jobs текущей кампании**, включая owned WorkChains/retries/CalcJobs/Slurm, после durable-state проверки | Updater сам cancel не начинает. Старый S01 и прочие не принадлежащие кампании jobs защищены до отдельного решения |
| PERM11 B | Backup/restore | Coordinated capture/offhost copy/verify и isolated restore; затем conditional replacement/rollback при доказанной recovery | Existing persistent DB/repository/NFS не удалять; OS rollback не означает DB rollback; полный wipe физического хоста не разрешён |
| PERM12 B | VM/disks cleanup | Удалять лишь созданные этой кампанией disposable test VM/blank volumes/temporary build paths по ownership manifest, после сохранения receipts; штатный checkpoint prune по принятому protocol | Не physical disks, existing root/data/scratch неизвестного владельца, scientific finals/failed raw/original logs, foreign Nix GC roots; failed restore target сохраняется до diagnosis |
| PERM13 B | Trust/secrets | Использовать существующие trusted roots и credentials в их scope; new-worker enrollment/host keys можно привязать к trusted provisioning evidence | Новый controller/cache trust root, неподтверждённая rotation, scope expansion credentials, отключение TLS/SSH/signature checks — отдельное решение |
| PERM14 B | Документация/help | 59/59 requirement dispositions без повторного опроса, docs pilot/prototype; включить truthful model/source help DOC07 по owning contract | UI не владеет формулами/thresholds; unknown явно unknown; новый registry/generator stack/domain product — отдельно |
| PERM15 S | Научная цель | **0 mV/period, lattice/LO 70 K**; пять механизмов LO/acoustic/impurity/IFR/alloy, **electron–electron = none**; declared dose/model/boundary из science | Добавление e–e, новые bias/T/dose/scattering/embedding/boundary и finite-bias/optics/experimental validation не входят |
| PERM16 S | Criteria/pilot | Делегировать evidence-based SCI03 design/freeze автору ultra + независимому high; pilot с заранее frozen measurement contract и existing strict gates | Не одобрение неизвестных допусков. Missing bound блокирует acceptance; ослабление criteria/смена target accuracy priority — отдельное решение |
| PERM17 S | Scientific catalog | **Выбран S1 без e–e:** весь conditional каталог **13 attempts /936 execution node-hours**, включая 2 R и 1 H; caps ниже | Не автоматические retries; новые waves/лимиты — отдельно. S0/S2 не выбраны |
| PERM18 B/S | Review/CI/stop | Independent technical checkpoints без per-ticket human approval; общий до5 author/review cycles; **один** final full CI на final ready source | No silent CI rerun, no acceptance с load-bearing defect. Identical failure/unknown outcome требует stop/reconciliation, не duplicate |

## B: конкретные границы инженерной автономии

### Source и late binding

Eligible source — reviewed owning commits принятого handoff, связанные опубликованными
gitlinks выбранного root candidate. Root/компоненты берутся из existing project
remotes; изменение remote organization/path требует решения. Разрешение переживает
обычные reviewed fixes внутри scope, но не переносит receipts на другой source.
PUBLISH не требует ждать DEV25/full release; INT02 исполняет publication,
DEV25 только проверяет порядок и receipts.

Eligible operational targets — QCL ресурсы утверждённого private site и
назначенного test pool. Существование VM с похожим именем не доказывает ownership.
Coordinator записывает exact inventory generation, VM IDs, disk serial/st_dev,
network/host IDs, candidate/source/artifact hashes и phase actions в BIND receipt;
R независимо сопоставляет с protected inventory и ownership evidence.
Неразмеченный target остаётся blocked, его нельзя самовольно объявить QCL-owned.
Новый test object выбирается только из already approved allocator/pool и
сохраняется в campaign ownership manifest; неизвестные ranges/quotas — missing input.

Окно выбирается агентом только при доказанно idle required QCL pool либо после
разрешённой остановки campaign-owned jobs. Foreign/old workflows и pending retry
не считаются пустой очередью. Cancel выполняет отдельный operator-step агента
через штатные interfaces, затем updater проверяет empty/cancel proof; в updater
не добавляется автоматический cancel. Старый saved S01 не принадлежит новой
кампании по умолчанию. Unknown submit/stop требует reconciliation по persisted IDs.

### Maintenance phases и recovery

В один conditional packet входят capture/pause/resume → verified external backup →
isolated restore → resource handoff/build → конкретный update/install →
post-boot/Slurm/NFS/staging/fault readback → reopen/production allocation.
Prerequisites привязаны к фазе: результат restore не нужен для разрешения первого
restore; successful restore нужен перед production replacement.
При отказе admission остаётся closed, original receipts сохраняются; rollback
выполняется только к совместимому verified состоянию с теми же trust/storage bounds.

Принятая цель planned maintenance — **нулевая потеря подтверждённых persistent
данных**. In-memory progress не называют persistent; для остановки campaign job
требуется verified durable checkpoint/terminal raw и documented resume semantics.
RPO/RTO измеряются с границами из OPS10. Числовой SLA восстановления пока
**не вводится**: ограничения длительности операций ниже — stop bounds, а не SLA.
Перед обещанием конкретного RTO оператор получает измерение и отдельный target.
Утверждённый B явно заменяет требование OPS10 о предварительном numeric
`RPO_target/RTO_target`: goal — нулевая потеря confirmed persistent данных,
RTO — measured-only. Отсутствие numeric RTO SLA не блокирует capture/restore;
`meets recovery-time objective` без принятого target не заявляется.

### Общий B-envelope

Утверждённый B расширяет conservative one-build attempt исходного плана:

- Не более **3 различающихся heavy build attempts**, каждый ≤12 h, вместе ≤36 h
  charged build wall time. Новый attempt только после конкретного диагноза,
  reviewed исправления и fresh admission. Два последовательных одинаковых
  failure fingerprints останавливают affected build; оставшиеся slots не
  разрешают слепой повтор. Одна параллельная Nix build job; CPU/RAM максимум
  по безопасному admission, без отмены чужих jobs.
- **100 GiB additional resident server build/store/depot/image copies** — общий
  peak cap, включая failed outputs и conversions. Logs ≤64 MiB, telemetry≤16 MiB
  внутри peak. Счётчики attempts и peak не сбрасываются при смене исполнителя.
  Cleanup только PERM12; scientific storage в этот build cap не входит.
- Preflight: 1 attempt ≤20 min/output≤8 MiB по OPS05, до heavy stage.
  Необходимость нового исправленного preflight после изменённого candidate —
  новый diagnostic attempt с сохранением отказа; максимум 3 за B-envelope.
- Backup/copy/restore: по 1 attempt ≤2 h, общий packet≤6 h, output≤16 MiB;
  byte cap — измеренный полный payload + verified sidecars/copy peak + site reserve,
  до mutation численно frozen и не выше разрешённой capacity.
- Installation/fault limits OPS11–14 сохраняются: Proxmox fresh install≤90 min,
  libvirt≤90 min +fault45 min, Windows install/scenarios≤2 h/host;
  owned engineering jobs максимум2 попытки, до2CPU/2GiB/10 min, staged≤1 GiB.
- Targeted DEV/docs/forward checks — исходные L-PY/L-JL/L и SI07 envelopes;
  среда готовится INT01 отдельно. Один общий targeted test slot, без скрытого
  full suite/bootstrap. Author/review до5 cycles не увеличивает test counters.
- Final full CI **1 dispatch ≤180 min** на final ready ref, runner standard
  4CPU/8GiB. Failure сохраняется; автоматический rerun не разрешён.

Привилегии namespaces, private staging, guest/disk/networks и cleanup scope
заносятся в BIND до исполнения. Недостаточный cap — blocked/replan/proposal,
а не ENOSPC/OOM как штатная остановка или тихое увеличение лимита.

## G: выбран G1 для публикации и слияния

| Выбор | Полномочие после отдельного EXEC |
| --- | --- |
| **G1 — approved_standby** | B draft publication + conditional merge component/root PR; final public release требует отдельного решения. Частная выдача готового worker bundle/guide допускается B |
| G0 — не выбран | Только own feature push/draft PR; merge и public release остаются оператору |
| G2 — не выбран | Как G1, плюс immutable public releases существующего проекта после всех required source/native/backend/restore/final-CI gates; эти дополнительные права не выданы |

Для merge: exact reviewed head, clean intended diff, independent CP-CODE,
required repository checks, branch protections, отсутствие out-of-scope changes.
Компоненты интегрируются до final source freeze. Root merge strategy выбирается
так, чтобы sole final CI/native/runtime receipts относились к окончательному
source; merge после CI не переносит автоматически full acceptance на новый HEAD.
Если protections требуют несовместимого порядка, агент фиксирует conflict и
готовит конкретное решение; обход protections или второй full CI не подразумевается.

Только при отдельном будущем выборе G2 дополнительно: version/tag по existing project policy, exact source и
immutable bytes/hashes/manifest, release notes/guide, no private/secret inputs,
actual required backend outcomes, verified recipient/download readback. Scope
частичного deliverable должен быть явно объявлен; full release при required
unknown не публикуется как accepted. Новый package registry/channel/account,
перезапись tag/release и сообщения людям сюда не входят.

## S: научная автономия и конечные ограничения

Выбранная цель берётся из [scientific milestone](../../system/scientific-milestone.md),
а не ставится заново: stationary thermal equilibrium 0 mV/period и70 K.
Сохраняются physics/model/scattering и exact declared parameters science.md,
включая current sheet `4.5e14 m^-2` как явно declared value с provenance caveat.
По прямому уточнению оператора **electron–electron scattering = none** во всех
B0/E1/P1/K1/W2/W3/R/H. Пять сохранённых механизмов — LO, acoustic, impurity,
interface roughness (IFR), alloy. Это совпадает с исходным `e–e none` science.md
и не меняет baseline, не удаляет один из пяти каналов. Подключение e–e в ходе
исправлений или refinements потребует отдельного научного решения.
Primary paper/DOI/units/assigning history агент сверяет сам; библиографическую
ошибку исправляет по evidence. Новое физическое значение или dimensional
interpretation требует отдельного scientific decision, не silent correction.

SCI03 может freeze критерии технически только при полной цепочке model→equation→
observable→weights/units/near-zero→error budget→bound→independent review.
Existing strict gates не ослабляются. Недоказанный bound остаётся unknown;
это не разрешение назначить удобное число. Pilot допускается для недостающего
measurement при заранее frozen измерительном контракте; он не physical pass.
Criteria version после pilot не применяется к нему задним числом: нужны
held-out H и незатронутые independent controls. Спор о научной цели/accuracy
priority возвращается оператору; спор о вычисляемом факте решается свидетельством.

### S1 — утверждённый полный conditional catalog без e–e

**13 attempts /936 execution node-hours**, каждый ≤72 h; это ceilings,
не обещанный расход или сходимость. W1 B0/E1/P1/K1 =4/288; W2 W/Z/B/A/Q =5/360;
W3 C =1/72; cause-specific R =2/144; held-out H =1/72.
Условия переходов/дельты точек и stop fingerprints — science.md, без additions.
B0 первым; refinements для accuracy ждут его релевантной convergence closure.
Модель/criteria/plan identities frozen до submit; каждый submit max_attempts=1.

Не более **2 одновременных executions**, один node/threaded Julia process на
execution, BLAS1; при одном доступном worker — serial. CPU и RAM каждой allocation
не выше fresh Slurm/cgroup/node limits после host/foreign reserves; точные числа
coordinator численно фиксирует до submit и считает actual/allocation core-hours.
Неизвестные ресурсы не заменяются максимумом «по паспорту».
После первого scientific submit finite charged wall allowance всего каталога
≤936 h, независимо от parallelism; ожидание недоступного сервера не расходует
compute и не разрешает бессрочный polling. Каждый активный job имеет deadline.

**Ресурсные бюджеты всего S1, редакция 2026-10-24:** resident/log — конечные
space budgets; cumulative I/O — monitored planning/early-stop budgets с возможным
зафиксированным техническим overshoot. Это не scientific tolerances и не measured capacity.

| Подмножество | Resident disk space /attempt | Monitored writes /attempt | Monitored reads /attempt | Log space /attempt |
| --- | --- | --- | --- | --- |
| W1: 4 attempts | 128 GiB | 2 TiB | 4 TiB | 1 GiB |
| W2/W3/R/H: 9 attempts | 256 GiB | 4 TiB | 8 TiB | 1 GiB |
| Вся кампания, shared budgets | **2 TiB current resident disk** | **44 TiB writes** | **88 TiB reads** | **13 GiB logs** |

Resident включает retained/pending/final/temp/retrieval/export copies, filesystem
overhead и суммарный peak; logs входят в storage. Final/failed raw и receipts сохраняются.
До запуска SCI07 проверяет консервативные оценки attempt/audit/checkpoint, actual
allocation/quota/reserves и RAM/CPU/tasks/time controls обычного рабочего пути.
SCI08 закрывает его конкретные recovery/containment defects, а не exhaustive native
proof. Shared telemetry учитывает producer/readers, protocol/hash reads по фактическому
coverage; missing coverage = unknown+gap, не pass и не требование custom VFD/NBD.
Точная atomic cumulative per-byte гарантия больше не требуется; порядок preflight,
early stop и kernel backstops — в [принятой поправке](resource-policy-2026-10-24.md).
Actual reserve/quota/capacity могут быть ниже budgets. Нельзя уменьшать physics/grid/
basis/window/channels ради ресурсов; неизвестный W2/H payload не наследует W1 budget.

После двух одинаковых последовательных failure fingerprints affected wave
останавливается. Дальше возможны независимые source/design/oracle tasks;
новый solve только после resolution и из оставшегося slot. Arbitrary new
solver-method/mixing variant и расширение13/936/byte/concurrency ceilings
этим grant не разрешаются. Успешный process не заменяет physics verdict.

### Альтернативы

- **S0:** только W1: 4 attempts/288 node-hours, ≤72 h/attempt; concurrency≤2;
  W1 128 GiB/2 TiB writes/4 TiB reads/log1 GiB per attempt; shared resident1 TiB,
  writes8 TiB/reads16 TiB/logs4 GiB. R/H/W2/W3 требуют нового решения.
- **S2:** scientific design/primary sources/existing-data analysis, новых SCBA/
  Poisson runs нет. DEV oracle checks только по соответствующим B limits.

S permission не доказывает physical acceptance. Negative attempt/report —
допустимый итог, а не право менять задачу или повторять бесконечно.

## Что действительно останется спросить позже

1. Trusted access/protected inventory, если их нет в доступных источниках;
   assignment test pool/destination, если оператор ещё не объявил эту область.
2. Старые/чужие jobs, неизвестное ownership, новый target/network/disk вне pool;
   physical disk wipe, потеря persistent data, force/shared-history rewrite.
3. Новый trust root/неподтверждённая key rotation/credential scope; несовместимые
   branch protections; public release при G0/G1 либо новый channel при G2.
4. Новая physics/model/goal/weaker criteria/required backend reduction,
   materially conflicting requirement и числовой recovery SLA при его введении.
5. Превышение finite ceilings/непредусмотренная costly variant, second final
   full CI, либо невозможность продолжить безопасно в принятом scope.
6. Недоступность принятой Sol/effort capability: новую model или fallback
   `ultra` на другой уровень нельзя выбрать молча; independent ready tasks
   продолжаются. Глобальные настройки аккаунта не меняются.

Hash/VM state/available RAM/queue/primary paper bytes/derived exact criterion
сами по себе не новые operator choices. Missing evidence остаётся blocker
лишь для claims/операций, которым оно обязательно; другие ready tasks идут дальше.

## Запись решений

Источник — прямой ответ пользователя от **2026-10-19** на три вопроса
`request_user_input_async`, call ID `call_20fe81a2d18242509e046a77f78f8b87`,
items 0/1/2. Время внутри суток не фиксировалось и не выдумывается.
Ответы получены явно; это не автоматическая отправка предвыбранных вариантов.

| Группа | Утверждённое содержание | Статус | Основание |
| --- | --- | --- | --- |
| B | PERM01–03/06–14/18 + B-envelope, без запуска | **approved_standby** | Item0: «Утвердить базовый пакет B (рекомендуется)» |
| G | **G1** conditional merge; public release отдельно | **approved_standby** | Item1: «G1: автомерж; публичный выпуск согласовать отдельно (рекомендуется)» |
| S | **S1 без электрон-электронного рассеяния**, весь finite catalog + criteria/pilot delegation и S1 caps | **approved_standby** | Item2: «S1, но без электрон-электронного рассеяния» |
| EXEC | Отдельная команда начать | **not_activated** | Текущий режим PLAN |

Данный ответ не содержит команды начать: **EXEC не активирован**, режим PLAN.
Уточнение S1 сохраняет baseline `electron–electron=none`, иных изменений
предложенных scope/числа attempts/caps пользователь не указал.
При дальнейшем изменении содержания approval на новые права не переносится.
Existing approved policy/grants не переспрашивать при каждом CP или resume.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| B/G1/S1 согласованы | Прямые ответы items0/1/2, PERM01–18 | approved_standby; EXEC не активирован | сохранить |
| Late binding позволяет автономность | Evidence predicates и BIND до действия | Unknown target/trust/resource не разрешён | сохранить |
| Все будущие результаты уже приняты | Разрешения без execution | Native/physical evidence отсутствует | данных недостаточно |
