# Platform и дистрибутив worker: автономный implementation handoff

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Чекбоксы обозначают будущую работу; подготовка плана не разрешает её выполнение.

**Goal:** закрыть инженерные замечания, получить проверенный cluster на одном релизе и выдаваемый пользователю дистрибутив нового worker с инструкцией установки, затем передать измеренную готовность научному исполнителю.

**Architecture:** Platform владеет OS/VM lifecycle, ресурсами, delivery, trust и restore; Runner — checkpoint/staging, AiiDA — workflow provenance, Root — source graph и сборкой релиза. Один локальный controller owner сериализует изменения; native backend gates независимы. Физическая приёмка остаётся в научном пакете handoff.

**Tech Stack:** существующие NixOS/Nix, Python stdlib, Deno/TypeScript, OpenTofu, Ansible; Proxmox, Linux/libvirt и Windows/Hyper-V. Никакого нового orchestration daemon или второго source lock.

**Spec:** [requirements](../../system/requirements.md), [roadmap и roles](../../system/release-roadmap.md), [rebuild](../../system/rebuild.md), [runbook](../../single-server-deployment.md), [RV06/RV11–15](../../system/autonomous-review-engineering.md), [RV18](../../system/autonomous-review-docs-skills.md).

## Граница поручения и фиксированные входы

Этот файл — **только план**. В этой работе не запускались SSH, server probes, tests, builds, установки или solver. Product code, AGENTS, Git config/settings и сервер не менялись. Пользователь подтвердил отсутствие новых серверных работ после review; свежая установленная runtime identity неизвестна. Старое наличие private inventory не доказывает доступность хоста.

Оператор согласовал [P1: B/G1/S1 без e–e](operator-permissions.md), статус
**approved_standby**, не EXEC. Для OPS приоритет имеют P1 late binding,
3×12 h build envelope, G1 merge, operator-role cancellation только campaign
jobs и measured-only RTO. Остальные prerequisites и native evidence сохраняются.

Проверенный локальный source: root `93880c23bca889ddcb8b98edb995080b332dd99f`; Platform gitlink `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`. Начальный `git status --short`: только чужой для этого пакета untracked `docs/implementation/review-closure-2026-10-19.md`. Все восемь gitlinks сняты штатным `git submodule status --recursive`; они остаются в Git, здесь не создаётся новая таблица блокировки ревизий. Рабочий checkout: `/home/tolya/.codex/worktrees/review-closure/qcl-negf`.

Существующий private inventory связан со старым source `5060e10`; его содержимое не публикуется и не принимается за fresh evidence. Fresh access/admission, depot, release/image manifests, hardware и disk identity пока **unknown**. Эти пробелы блокируют зависимые OPS, но не самостоятельную локальную разработку после DEV grant.

Все пути далее относительно root. Префикс `P/` означает **существующий** `components/qcl-negf-platform/`; новые пути прямо помечены «предлагается». Перед исполнением сравнить выбранный immutable root/gitlinks с этим locator и повторно проверить символы. Любое изменение owning component публикуется отдельным PR; root обновляет только опубликованный gitlink.

## Роли, разрешения и общий бюджет

Каждая OPS-карточка назначается на сохранённую модель **Sol**: **D = ultra**, **I = medium**, **R = high**, **audit/coordinator = high**. D пишет контракт; I исполняет готовые шаги; R получает первичные source/fixtures/receipts без готового диагноза. Effort не является CPU grant. Если заданный effort нельзя подтвердить, записать ограничение координатору.

| Контрольная точка | Кто закрывает и что она разрешает |
| --- | --- |
| CP-DESIGN | Coordinator после независимого технического review точного design artifact. Не operator approval. |
| CP-CODE | Coordinator после review diff и bounded targeted checks. После future DEV grant готовая I-задача с принятым D выполняется без повторного вопроса пользователю. |
| CP-NATIVE | Технический coordinator/reviewer gate внутри active BUILD: source candidate, fresh admission и успешный дешёвый preflight проверены перед heavy build/rehearsal. Не новый operator вопрос и не production grant. |
| CP-RELEASE | Coordinator проверяет опубликованные refs, identity chain, матрицу gates и фактический final CI. Не даёт права применить release. |
| CP-OPS | Human policy approval B уже дан в P1. После EXEC coordinator+R закрывают technical BIND на phase/candidate/source/targets/disks/window/backup/rollback. При выполненных P1 predicates нового human approval не нужно; вне scope требуется решение. READ_NATIVE/BUILD имеют отдельные границы. |

Новые trust roots/cache keys, неподтверждённая rotation, credential scope и destruction вне B disposable targets требуют отдельного решения. New-worker host keys/enrollment внутри B допускаются только по trusted provisioning evidence. Foreign VM защищены; host-key/TLS/signature checks не отключаются. DEV/NATIVE сами не означают OPS: policy approval даёт P1/B, затем technical BIND и отдельный EXEC. Missing input останавливает dependent operation; независимые tickets продолжаются.

Общая [policy автономии](autonomy.md) задаёт CP-START. Сегодня действует **PLAN**: DEV/BUILD/OPS и G1 согласованы в P1, но **не активированы**. Утверждённые caps не доказывают фактическую capacity или прохождение внешнего gate.

Согласованные пределы **approved_standby P1/B**, не текущая активация: L — на карточку до 4 targeted Python invocations по 1 CPU/2 GiB/60 s/1 MiB либо 2 Deno invocations по 2 CPU/4 GiB/120 s/2 MiB, без install/full suite; общий DEV cap устанавливает coordinator для всех агентов вместе. N — максимум **3 различающихся build attempts ≤12 h каждый, вместе ≤36 h**, один параллельный Nix build, не более 100 GiB **дополнительного resident peak** server artifacts/store/depot/image copies, включая failed outputs; retained logs≤64 MiB/telemetry≤16 MiB внутри peak. Новый attempt — только diagnosis+reviewed fix+fresh admission; два одинаковых failure fingerprints останавливают affected build. CPU/RAM — fresh safe maximum с protected reserves, не laptop profile. Ни одна карточка не сбрасывает общий allowance/counters.

При timeout/ENOSPC/identity drift/unknown mutation сохранить original logs и receipt, остановить зависимый этап. Известный отказ допускает новую attempt после диагноза и reviewed fix в оставшемся P1 allowance, без повторного вопроса. Исчерпание finite cap требует нового поручения; unknown outcome требует trusted reconciliation, не blind retry. Final CI — ровно один full dispatch для final ready source ref; reruns отсутствуют.

## Review focus и общие output contracts

- Смешанный controller parent/child ownership: standalone и owned activation не должны обходить общий lock или брать его повторно; OPS02–03.
- Старый manifest/depôt/compiled assets: версия пакета не заменяет source/derivation/content binding; OPS04–07/16.
- Успешный service restart при DOWN/DRAIN, неполном worker inventory или живом workflow retry не открывает admission; OPS08–09/14.
- Hash-valid backup с несовпадающими DB/repository поколениями и неучтённым общим filesystem не принимается; OPS10.
- Новая Windows VM не считается установленной по наличию Start/Shutdown wrapper; каждый backend проходит boot/network/enrollment/job/fault gates; OPS11–15.

У каждого ticket output: reviewable owning diff/design, exact selected source, таблица assertions и evidence, команда/attempt/deadline, фактический outcome (`pass`, `failed`, `unknown`, `not_measured`, `blocked`), ограничения и следующий dependency. Private raw logs, targets, disk identities, keys и enrollment остаются в private site. Public report содержит sanitized hashes/статусы; release/image checksums публичны, если сами артефакты публичны. Receipt — evidence конкретного запуска, не второй source lock и не scientific pass.

### Readiness по промежуточным outputs

Карточка с несколькими ролями не является неделимым dependency gate.
Суффиксы `.D/.I/.N` обозначают accepted design, reviewed code и native receipt
внутри той же task; `.S` — source/trust subset. Это не дополнительные task IDs.

| Выход | Требует | Разблокирует |
| --- | --- | --- |
| OPS04.S source/depot/trust inputs | CP-SOURCE, доступные metadata, READ_NATIVE при remote read | OPS05 preflight и source design; не ждёт нового build |
| OPS05 preflight receipt | OPS01, OPS04.S, scoped BUILD namespaces/paths | CP-NATIVE, затем OPS06 heavy build |
| OPS04.N contents/import proof нового output | OPS06 output; BUILD self-check scope | Release/native identity checks; не prerequisite собственного build |
| OPS07.D distribution manifest/controller contract | OPS04.S и source design | OPS11.D/12.D/13.D boot/format choices |
| OPS14.D shutdown/order contract | OPS02/08 accepted source contracts | Backend design и OPS14.I source fixtures; installed VM не нужна |
| OPS11.D/12.D/13.D backend choices | OPS07.D, OPS14.D где применимо | OPS07.I assembler/recipes и backend I; это не native acceptance |
| OPS07.N выдаваемые images/bundle | OPS07.I + backend choices, OPS06 build, CP-NATIVE | Backend installation; candidate staging в named BUILD/OPS scope |
| OPS11/12/13 installation receipt | OPS07.N, соответствующий I, fresh target admission + BUILD rehearsal либо CP-OPS | OPS14.N fault/normal shutdown matrix |
| OPS14.N → OPS16 → CP-RELEASE | Required installed backends/native receipts, one final CI | OPS17 full-release handoff |

Backend I использует OPS14.I, если меняется общий shutdown код, но не ждёт
OPS14.N. Один writer сериализует общий код. Missing backend hardware блокирует
его native output, а не готовые source/design outputs других карточек.

## OPS01 — свежие inventory, admission и readiness inputs

**Роль/owner:** audit high; D ultra для формы недостающего collector, I medium для его реализации; R high. Owner Platform/private site. **Paths:** читать `P/docs/build-admission.md`, `P/ops/build_admission.py`, `P/examples/access-inventory.md.example`, `P/examples/private-site/`, `P/docs/host-storage.md`, `P/docs/host-network.md`; collector и private inventory — **предлагаемые** private-site paths, не public Git. **Input/deps:** выбранный root/gitlinks, отдельный grant на fresh remote collection; от старого `5060e10` брать только перечень полей для повторной проверки.

**Interfaces/output:** защищённый `qcl-build-admission.v1` JSON с `captured_at`, complete host inventory, configured max RAM всех VM, `roles`, idle builds/runner/Nix, whole queue, `temporary_bootstrap`, owned QEMU PID и `builder_memory.source=RssAnon|Pss_Anon|stopped`. Параллельно private access/storage/network inventory с generation/capture time, management routes, verified fingerprints, disk serial/st_dev, volumes и ownership QCL/foreign/protected/unknown. Sanitized readiness table показывает по отдельности source, access, resources, storage, secrets provisioner, depot, manifests, backup и backend hardware.

- [ ] После CP-START+READ_NATIVE на named trusted site измерить факты; CP-OPS для read-only collection не нужен. SSH failure не превращать в stopped/zero/undeployed. Проверить действительность credentials без вывода secret bytes.
- [ ] Зафиксировать installer seed и offline artifact route; unknown ownership, disk «100 ГБ» без назначения, незнакомый источник builder — blocker до teardown.
- [ ] Проверить positive: полный свежий snapshot; negative: >60 s, future time, FIFO/symlink/>1 MiB, пропущенная foreign VM, неверный PID/VM, raw RSS вместо anonymous, nonempty queue, заменённый PID. Collector должен прерываться без admissible snapshot.

**Будущая существующая команда:** `python3 P/ops/build_admission.py --snapshot PRIVATE/admission.json --profile production-build --vcpus CPU --memory-mib MIB` (`P/` раскрыть в полный component path). Выход сохраняет resolved resources и memory credit; helper ничего не измеряет и не резервирует. **Cost:** source L; fresh collection 1 attempt ≤10 min/2 MiB, read-only после grant; admission snapshot переснять ≤60 s непосредственно перед apply. **Stop/gate:** missing facts блокируют только dependent operation; не начинать SSH из текущего plan. CP-DESIGN/CP-CODE для collector, READ_NATIVE для конкретного site collection; новая trust identity требует CP-EXCEPTION, без auto-accept host key.

## OPS02 — D: единый owner controller activation и owned child

**Роль/owner:** D ultra, независимый R high, audit high; I этой карточки отсутствует. Platform. **Paths/input:** `P/ops/application_release.py::{lifecycle_owner,lifecycle_guard,activate,deliver_cli,_deliver_cli_locked,main}`, `P/ops/worker_lifecycle.py::{shutdown_step,startup}`, `P/tests/test_application_release.py`, `P/tests/test_worker_lifecycle.py`, `P/tests/test_worker_shutdown_intent.py`; immutable baseline выше. **Deps:** OPS01 source identity, runtime inventory не нужен.

**Наблюдение:** standalone CLI `activate`/`prepare-initial` используют `activation.lock`; whole update — `delivery.lock`. Controller activation вызывается как SSH child при удержании parent lock. Простая замена lock filename создаёт self-deadlock; `--owned true`, PID без поколения или user-provided parent UUID не являются authority.

**Design output:** предлагается `P/docs/lifecycle-ownership.md` с state/transition таблицей и accepted API. Предпочтительное решение: `lifecycle_owner(runtime, *, operation, release_id, deadline) -> LifecycleOwner` выдаёт process-local opaque capability; публичный `activate(...)` сам приобретает общий owner, приватный `_activate_owned(..., *, owner: LifecycleOwner)` принимает только живой capability того же процесса/runtime/lock inode/boot/release/deadline. Parent delivery вызывает controller child **локально в том же процессе**, без mutating SSH к себе; readonly identity authority продолжает проверяться. Remote worker activation получает собственный node-local owner и existing bound attempt/identity; capability не сериализуется в JSON/env/CLI и не переносится через SSH. Если chosen design иной, до CP-DESIGN описать столь же проверяемую authority без forgeable bypass.

- [ ] Разделить short capture/finalize shutdown ownership и unlimited Runner wait; один общий controller writer, отдельный per-node normal lifecycle owner, ожидание не удерживает общий owner.
- [ ] Установить before/after: profile/env/allowlist/ready/admission publishers, durable intent, dead parent, lock contention, prior unknown, crash between phases, identical repair solver GC root, deadline inheritance.
- [ ] Определить migration: существующие unresolved receipts/markers остаются блокирующими; `activation.lock` не очищает `delivery.lock` authority. Совместимость публичных CLI сохраняется, новый unsafe owned flag отсутствует.

**Acceptance:** R проверяет state machine и один executable fake scenario standalone-vs-update contention, parent-owned local activation без reacquire, forged/stale owner rejected до mutation, crash never opens gate. **Future commands:** только read/diff на D; fixture execution относится к OPS03. **Cost/gate:** source review ≤60 min/один design artifact; CP-DESIGN coordinator, без CP-OPS и без native Windows. Это отдельное design решение, его нельзя неявно поручить I medium.

## OPS03 — I: реализация ownership и crash/retry fixtures

**Роль/owner:** I medium по принятому OPS02, R high, audit high; D ultra только при реальном contract change. Platform. **Paths:** `P/ops/application_release.py`, `P/ops/worker_lifecycle.py`, `P/tests/test_application_release.py`, `P/tests/test_worker_lifecycle.py`, `P/tests/test_worker_shutdown_intent.py`, принятый OPS02 document. **Deps:** CP-DESIGN OPS02 + future DEV grant; hardware/access/admission не prerequisites.

**Interfaces/output:** точные `LifecycleOwner`, standalone wrapper и `_activate_owned` из принятого D; общий owner всех controller mutations, отдельный bounded node lock, unchanged release/Code/attempt semantics. Existing CLI `qcl-negf-release activate --manifest RELEASE --role controller` остаётся standalone; parent вызывает private helper, не этот CLI под собственным lock.

- [ ] Сначала добавить regression: два процесса с разными entrypoints, contender fail before profiles; parent helper не вызывает второй flock; arbitrary object/foreign runtime/release/expired/dead-parent context rejected.
- [ ] Реализовать routing и guard до первого изменения; не обходить protected enrollment/identity/trust/admission checks.
- [ ] Проверить fault points после application profile, solver profile, Code allowlist, service.env, ready:false, service start, ready:true и final publication; original bytes/unknown сохраняются. Повтор идентичного релиза ремонтирует только повреждённый GC root и сохраняет immutable Code UUID.
- [ ] Проверить shutdown captured intent и startup при конкурирующем update; ожидание durable stop не блокирует независимый shutdown capture, orphan intent не снимается.

**Будущие команды** из component directory: `python3 -m unittest discover -s tests -p test_application_release.py`; затем выбранные `test_worker_lifecycle.py` и `test_worker_shutdown_intent.py` тем же discover. **Expected receipt:** assertions + counts/command logs/source hash, без real Nix/SSH/services. **Cost:** L, максимум четыре invocations суммарно; один implementation pass и один review repair в пределах DEV cap. **Retry/stop/gate:** необъяснённый deadlock/guard regression — вернуть D с локатором; CP-CODE coordinator. Native tests в OPS09, source change не ждёт Windows hardware.

## OPS04 — source → derivation → contents → imports и trust

**Роль/owner:** D ultra для точного evidence contract, I medium для адресных guard fixes, R/audit high. Root/Platform с owning tickets в Portal/Runner. **Paths:** root `ops/git.ts`, `ops/solver.ts`, `ops/application_cd.ts`, `nix/solver.nix`, native locks; `P/ops/application_release.py::{manifest,prefetch_controller_closures,read_protected_file,freeze_ssh_trust}`, `P/modules/cache.nix`, `P/tests/test_application_release.py`, `P/docs/application-cd.md`. **Deps:** OPS01 source; OPS03 для lifecycle integration, не для независимого hash fixture.

**Interfaces/output:** existing `qcl-negf-release-v1` (`sources`, exact application/solver paths, two closure `narHash`, `release_id`, optional credential-free cache URI), depot `qcl-negf.julia-depot.v1`, derived source graph. Предлагаемый evidence table связывает imported module/file origin и commit с native suite/profile/worker args/Julia factory+phases, lock hashes, derivation/output/content hash; Portal static assets связываются с owning source/package-lock. В manifests не добавляется ручной список ревизий вместо Git.

- [ ] Различить reuse native output, воспроизводимость declared bytes и новый full-release verdict. Carry-forward допустим лишь для того же derivation, verified contents и native test contract; original producer/source/failed logs неизменны.
- [ ] Positive: правильные signed closures/imports. Negative: те же `0.2.0` из другого commit, stale assets, wrong manifest/closure, missing narHash, credential URI, changed factory/profile, untrusted key, corrupted local store. Cache failure/hash mismatch до gate/service mutation.
- [ ] Проверить protected file FIFO/symlink/oversize и frozen known_hosts; late SSH/Nix calls используют тот же trusted snapshot. Новую host key/key rotation не принимать автоматически.

**Future existing commands:** root `deno task graph`; `nix path-info --json APPLICATION SOLVER`; `nix-store --verify-path APPLICATION SOLVER`; immutable `SOLVER/bin/qcl-negf self-check` через owning `solver_self_check` (300 s, Julia/BLAS 1). Source/trust subset OPS04.S не ждёт нового native output: read-only metadata существующего store допускается READ_NATIVE, новые build/import/self-check — BUILD на назначенном store. OPS04.N закрывается после получения output OPS06. **Expected:** self-check `qcl-negf-self-check-v1/completed`, `scientific_accepted=false`; exact imports/content evidence, а не exit-only. **Cost:** L; native self-check 1/closure ≤300 s, ≤2 GiB/1 thread, output≤1 MiB, без SCBA. **Gates:** CP-CODE; trust вне approved provisioning/roots — CP-EXCEPTION. M07 two rebuilds — отдельный grant, не automatic retry/final CI.

## OPS05 — дешёвый four-role preflight и строгий nginx

**Роль/owner:** I medium по существующему contract, R/audit high; D ultra при изменении контракта. Platform/private site. **Paths:** `P/ops/bootstrap_build.py`, `P/nix/site-preflight.nix`, `P/tofu/build-images.ts`, `P/docs/nginx-preflight.md`, `P/tests/test_bootstrap_build.py`, `P/tests/infrastructure/images_test.ts`, root runbook. **Deps:** OPS01 fresh inputs + OPS04.S exact depot/site source + active BUILD для bounded preflight, включая named namespaces/privileges. CP-NATIVE закрывается по результату OPS05, а не требуется для её начала; не начинать full image build.

- [ ] Проверить реальные absolute executable paths, systemd PATH/cwd, builder identity, owner root+8 Git indexes (`GIT_OPTIONAL_LOCKS=0`), resolved flake inputs/generated lock и те же runtime modules/`mkSolver` args.
- [ ] Получить drvPath всех `storage/control/compute/ci`, затем только фактический nginx.conf writer `^out`; тест фактическим nginx `-t` в явно разрешённых isolated mount/network namespaces. Engineering certificate заменяет только объявленные TLS directives; production key не читается.
- [ ] Positive: native syntax success и нули warn/error/crit/alert/emerg. Negative: missing certificate, wrong ExecStart/reload config, changed role derivation/config hash, disabled namespace, missing executable, warn output, writer success без actual test. Cache-hit gixy output missing = `not_measured`, не zero.

**Future existing command** из root (пути сначала измерены):

```sh
deno task bootstrap:preflight --receipt PRIVATE/ATTEMPT/preflight.json preflight \
  --site PRIVATE/SITE --nix /run/current-system/sw/bin/nix --check-nginx \
  --openssl MEASURED_OPENSSL --mount MEASURED_MOUNT \
  --nginx-namespace '["/run/current-system/sw/bin/sudo","-n","/run/current-system/sw/bin/unshare","--mount","--net","--propagation","private"]'
```

**Output:** `qcl.bootstrap-preflight.v1/status=pass` с four-role derivations, writer/output/config SHA256, actual executable/ExecStart, test SHA256, bounded raw diagnostics/counters. Evaluation-only не pass. **Cost:** 1 attempt≤20 min, каждый helper≤60 s/1 MiB, общий output≤8 MiB; admitted builder ресурсы, до 1 GiB дополнительных конфиг-артефактов внутри N. **Stop/gates:** любой mismatch останавливает heavy stage; исходный отказ сохраняется; namespace privilege явно включён BUILD либо запрашивается scoped CP-EXCEPTION, технический review CP-CODE, результат входит в CP-NATIVE. Full NixOS system build не заменяет этот gate.

## OPS06 — production-build по свежему максимуму и immutable native build

**Роль/owner:** I medium, R/audit high; D ultra для resource policy change. Platform/Root/Runner. **Paths:** `P/ops/build_admission.py`, `P/ops/bootstrap_build.py`, `P/ops/build-profiles.json`, `P/modules/builder.nix`, `P/tofu/bootstrap/`, root `ops/solver.ts`, `nix/solver.nix`, Runner launcher; private site resources. **Deps:** OPS01/04.S/05 pass и CP-NATIVE на exact source; CP-OPS отдельно для resize/reboot builder. OPS04.N нового output следует после build, не блокирует его начало.

**Resource contract:** production-build — временный bootstrap; `local-debug` остаётся laptop 4 CPU/8 GiB. Выбрать все свежие безопасно доступные host CPUs; shared CPUs допустимы только временным profile. RAM: сумма max allocations всех других running VM + target builder ≤ host total −8192 MiB; `MemAvailable ≥8192+8192+max(target−credit,0)`, `credit=max(0,min(configured,RssAnon|Pss_Anon)−256)` MiB. Foreign/pnetlab не останавливать; guest RAM не считать свободной по balloon. VM vCPU/RAM = Nix resources; shared slice RAM=guest−2048 MiB, Nix jobs=1, cores=vCPU, swap=0. Julia compile использует весь admitted CPU, test-worker limit — по измеренной памяти; не подделывать `Sys.CPU_THREADS`.

- [ ] Создать новую persistent systemd attempt/unit с immutable bytes, source, InvocationID, одним deadline; samples связывать с InvocationID. Повторно снять admission перед применением reviewed saved plan.
- [ ] Подготовить pinned depot, hash-prefetch local file до cold sandbox; сохранить archive вне Git и достаточно места для store copy. Native import/suite проверяют полный declared contract без scientific solve.
- [ ] Отслеживать CPU/RSS/I/O/GC/OOM и прогресс; на 15/30/60 min далее ≤30 min записывать phase, resource headroom и remaining deadline. Нет progress/рост памяти без объяснения — stop/diagnosis, не увеличение grant.

**Future existing root commands:** `deno task --cwd components/QCLNEGFRunner.jl bootstrap`; `deno task solver:depot ARTIFACTS/ATTEMPT`; `deno task solver:build ARTIFACTS/ATTEMPT/solver-depot.json --profile production-build --test-workers WORKERS`. Depot preparation требует явно measured `JULIA` path как в runbook. **Outputs:** original unit/logs/terminal state, depot/native receipts, actual native contents/imports, telemetry, disk accounting. Count одним `du -B1 -s` roots store/releases/artifacts с history; QCOW добавить только sparse delta `max(0,size−blocks*512)`. Root accounting failure не повод пересобирать: separate read-only verifier и composite receipt сохраняют failed main unit.

**Cost/gates:** каждый build attempt≤12 h из общего P1/B cap3/36 h и resident peak100 GiB all copies; перед сборкой free disk≥planned additional peak + site reserve, порог reserve фиксируется CP-NATIVE. Identity drift/OOM/100 GiB/deadline — stop. Не выключать чужие jobs. После build вернуть measured production VM/slice distribution, final CI `standard` 4 CPU/8 GiB, compute handoff только после этого; receipt показывает actual resources до/после. Engineering build не deployment/science pass.

Обычный builder/CI ↔ compute resource handoff ждёт idle/empty queue и не отменяет исследования. При необходимости VM poweroff/reclaim действует отдельный reviewed provider plan для **всех QCL-owned затрагиваемых VM**, с остановкой/повторным boot/readback по enrollment; service stop не доказывает освобождение RAM. Невозможность подтвердить host free memory после stop блокирует увеличение builder, foreign VM продолжают работу. Recovery/open admission после обратного handoff требуют свежих OS/release/Slurm проверок OPS09/14.

## OPS07 — выдаваемый worker artifact и воспроизводимые recipes

**Роль/owner:** D ultra (формат delivery), I medium, R/audit high. Platform с Root composition. **Paths:** существующие `P/nix/images.nix`, `P/flake.nix::lib.mkImages`, `P/modules/{image,cluster,release}.nix`, `P/tofu/build-images.ts`, examples/private-site; **предлагаются** `P/docs/worker-distribution.md`, `P/examples/worker-site/`, `P/ops/worker_distribution.py`, `P/tests/test_worker_distribution.py`. **Deps:** OPS07.D требует только OPS04.S/source inputs; backend OPS11.D/12.D/13.D принимает этот manifest contract и возвращает boot/format choices. После их review — OPS07.I assembler/recipes; OPS07.N actual artifact build требует OPS05/06 и CP-NATIVE. Finished native backend install не prerequisite artifact.

**Interfaces/output:** `qcl-negf-worker-distribution-v1` — предлагаемый manifest, не существующий API: schema, release_id, source-graph artifact hash, native lock/depot references, architecture, role=worker, boot mode/generation, root format, filenames, byte counts/SHA256, Nix derivation/output/narHash, required host features, compatible controller contract, recipe/config hashes и nonsecret enrollment prerequisites. Предлагаемый public bundle содержит root QCOW2 и при принятом Hyper-V route VHDX, exact build recipe, sanitized config template, checksums, install/rollback README; secret bytes/enrollment/private targets в bundle отсутствуют. Writable machine-id/SSH host keys должны генерироваться на first boot, не клонироваться из image.

- [ ] Отделить reusable worker base от site configuration: explicit controller/NFS endpoints, NodeName/UID/GID/resources/MAC/interface и scratch mapping задаются template; secrets передаются runtime. First boot DRAIN/no-submit до trust/enrollment/release checks.
- [ ] Поддержать build из опубликованного source + private site без скрытого существующего depot/path; cold recipient получает instructions по trusted artifact route или pinned recipe. Не объявлять raw Nix store path downloadable distribution.
- [ ] Positive: template→artifact→manifest hash roundtrip. Negative: duplicate node/machine identity, secret в Nix path, bad size/hash/format/boot generation, stale source/build receipt, wrong controller release, missing scratch. Сканирование package не выводит секреты.

**Future existing command** из `P/`: `deno run --allow-read --allow-run=nix --allow-write=OUTPUT tofu/build-images.ts SITE PROXMOX_BASE.json ARCH_BASE.json OUTPUT --preflight-receipt PREFLIGHT.json` (использовать `-` вместо ARCH_BASE для four-role only). **Expected existing outputs:** `images.json`, `proxmox.tfvars.json`, optional `arch-libvirt.tfvars.json`, actual SHA/bytes QCOW2; новый distribution assembler публикует свой distinct manifest. Его CLI реализовать и зафиксировать после D; не выдавать proposed command за существующий.

**Cost:** L; native conversions/build только в N, один serial image/conversion pass≤2 h remaining, disk включает исходник+выход+staging. **Gates/stop:** CP-DESIGN/CP-CODE/CP-NATIVE; candidate staging на declared lab/private destination входит BUILD/OPS и не ждёт final CP-RELEASE. Public release/public artifact publication — отдельный CP-EXCEPTION после required release gates. Где: persistent `ARTIFACTS/RELEASE/worker-distribution/` на builder, immutable trusted HTTP(S)/offline medium назначается оператором; receipt фиксирует реальный destination, verification on recipient и checksums. Без доставляемого файла/URL/medium дистрибутив не завершён.

## OPS08 — I14: source/fault closure whole-cluster maintenance

**Роль/owner:** D ultra для остаточного policy gap, I medium по existing I14, R/audit high. Platform; cancellation owner AiiDA/оператор. **Paths:** `P/ops/application_release.py::{deliver_cli,_deliver_cli_locked,stop_update,fleet_health,finish_update}`, `P/ops/aiida_update_check.py`, `P/tests/test_application_release.py`, `P/docs/application-cd.md`. **Deps:** OPS03/04.S для source/code; native deployment OPS09 отдельно с OPS04.N proof.

**Contract:** operator вручную отменяет **все QCL** верхние `qcl_negf.plan`, `qcl_negf.execution_restart`, paused/waiting retries, CalcJobs и Slurm queue; update ничего не отменяет за него. Foreign jobs/VM не трогать; если они попали в общем controller queue и мешают safety gate — stop/operator resolution. Полный enrolled pool содержит offline nodes: исключение узла требует отдельного trusted retirement до update. Existing `stop-update` останавливает worker execution/slurmd, **не VM poweroff и не RAM reclaim**; обычный resource handoff VM остаётся отдельным действием.

- [ ] Перед mutation verify local controller authority, full enrollment, closures hashes, installed capabilities, original healthy IDLE registration; fresh cancellation recheck до/после restart и перед gate.
- [ ] Fault fixtures: missing/NULL process state, неполная pagination/один workflow type, submit после snapshot, offline node, foreign DRAIN/reason, unknown cgroup member, daemon replacement, failed stop/copy/activate, RESUME response lost, NFS/root_squash write/fsync failure. Ни одного later dispatch/open по предполагаемому успеху.
- [ ] Проверить durable intent и `requires_reconciliation`, один общий owner и global deadline, original→own DRAIN→measured stop→same-generation IDLE chain. Hard stop только positively bound singleton daemon+полная process/cgroup proof; empty/unknown proof запрещает kill.

**Future existing command** после CP-OPS, не source fixture: `sudo qcl-negf-release update --manifest PRIVATE/release.json --pool PRIVATE/pool-v2.json --enrollment PRIVATE/enrollment.json --delivery-timeout-seconds 1800 --command-timeout-seconds 360 --command-output-bytes 1048576 --delivery-output-bytes 8388608`. **Expected:** private `delivery-attempts/UUID.json` (`qcl-negf-delivery-attempt-v1`, whole_cluster_update, required_nodes/worker_stop/fleet_health/cancellation_check), public redacted delivery-report; open только после полного health. **Cost:** L; native bound 1 attempt/1800 s, command≤360 s, 1/8 MiB caps. **Gate:** CP-CODE; production CP-OPS обязателен с exact release/window/rollback/backup. Retry known failure после диагноза, unknown только reconciliation, ручного удаления blocker недостаточно.

## OPS09 — native production activation, сервисы и cluster transport

**Роль/owner:** I medium, R/audit high; D ultra при неожиданном interface gap. Platform/private site. **Paths:** existing modules/application/cluster/storage/release, `P/docs/operations.md`, `P/ops/slurm_maintenance.py`, `P/ops/slurm_job_evidence.py`, release receipts. **Deps:** OPS01/04–08, CP-OPS на конкретные VMs/release/window, backup OPS10 create/verify; для полного release restore rehearsal должен быть принят.

- [ ] Boot storage/control/compute/CI из measured images; не форматировать persistent disks. Проверить actual current+booted OS identity, protected mounts, UID/GID/NFS ownership, runtime secret ownership, PostgreSQL/AiiDA UUID/Code path, API/TLS/auth, scheduler registration/resources и CI isolation.
- [ ] Применить один release по OPS08 после manual cancellation. Доказать всех workers stopped **до первой** activation и exact same release после, API/daemon restart и no stale queued retry. OS/migration changes идут отдельно reviewed maintenance, не притворяются routine activation.
- [ ] На каждом worker выполнить owned synthetic batch и отдельный bounded `srun hostname` callback test; batch exit не доказывает port range. Проверить scratch→NFS atomic publication и hash/attempt selection. Exit0/self-check ≠ SCBA/Poisson/science verdict.
- [ ] Negative/fault: missing mount must inhibit service, wrong key/UID, cache trust fail, network loss, mixed profile, DOWN NotResponding после restart, full queue/foreign drain, changed boot during health, user cannot sudo/admin/private secrets. Fail closed и original receipt retained.

**Future existing commands:** `qcl-negf-release check --manifest RELEASE --role controller`; worker role аналогично; `sudo qcl-negf-worker-lifecycle startup --node NODE --target ENROLLED_ROUTE --enrollment PROTECTED`; `srun --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=256M --time=00:00:30 --nodelist=NODE hostname` после admission тестового окна. Maintenance resume (не reopen gate):

```sh
python3 P/ops/slurm_maintenance.py --expected EXPECTED.json --expected-sha256 EXPECTED_SHA \
  --worker WORKER.json --worker-sha256 WORKER_SHA --scontrol IMMUTABLE_SCONTROL \
  --squeue IMMUTABLE_SQUEUE --systemctl IMMUTABLE_SYSTEMCTL \
  --runtime-json PROTECTED/release.json --gate SHARED/admission.json \
  --lock PROTECTED/delivery.lock --out NEW_ATTEMPT
```

Expected/worker records root-owned regular ≤64 KiB, hashes frozen; worker observed≤60 s, current=booted OS, matching boot/runtime/registration, exact `Not responding [slurm@TIMESTAMP]`. Иной DOWN/DRAIN reason отвергается. Receipt подтверждает same-generation exact IDLE/zero allocation после bounded poll; admission остаётся closed.

**Outputs/cost:** per-node boot/service/runtime/Slurm/NFS receipts и test job ID; one attempt≤90 min total, synthetic jobs≤2/node×30 s×1CPU/512 MiB, self-check≤300 s, metadata≤16 MiB, staged bytes≤64 MiB (large staging отдельно по OPS14 budget). Physical stop collector before/after≤20 s/128 KiB each, требует actual before PID/start-tick proof. **Stop/gates:** любой stale identity/unknown/queue — admission closed, trusted reconciliation; CP-SOURCE/CP-NATIVE проверяют candidate до воздействия, CP-OPS разрешает конкретное изменение. Эти receipts идут в будущий final CP-RELEASE после OPS16. Не объявлять «cluster работает полностью» до OPS10–16 и обязательных backend cells.

## OPS10 — согласованный backup и isolated restore с RPO/RTO

**Роль/owner:** D ultra для site recovery boundary, I medium, R/audit high. Platform/private site. **Paths:** `P/ops/state_archive.py`, `P/modules/state-archive.nix`, `P/tests/test_state_archive.py`, `P/docs/state-archive.md`, private recovery log. **Deps:** OPS01 storage/identity, OPS04.S known immutable versions. Pausing/capture/resume production writers требует своего CP-OPS на эти действия. Первый isolated restore: verified archive+external medium, explicitly named BUILD rehearsal VM/disk/networks и cleanup; при выходе за этот grant отдельный scoped CP-OPS. Результат ещё не выполненного restore не prerequisite его разрешения. Public/source review не ждёт remote access.

**Interfaces/output:** coordinated archive содержит AiiDA profile/repository, PostgreSQL dump, Slurm state, manifest SHA/bytes/source/PG physical size/secret **references**/NFS reference; external NFS dataset и secrets recovery отдельны. Same-server archive не offhost backup. Restore target — пустая отдельная state disk/database, same pinned PG major/application/UID, no automatic bootstrap/API/daemon/Slurm, один authoritative controller.

- [ ] Before create остановить все writers/submission paths, дождаться/вручную отменить очередь по своему scope; measured archive/repo/database sizes; `--writers-paused` — проверенное operator declaration, не автоматический oracle.
- [ ] Copy archive+sidecar на external medium; verify copied bytes и trusted hash. Отдельно NFS file/dataset manifest и runtime-secret recovery, без Git массивов.
- [ ] На isolated target восстановить, проверить AiiDA status/storage, Computer/Code UUID, representative repository objects, NFS job locators; bootstrap retain UUID and reject wrong solver. Не подключать второй writable controller к production NFS/queue.
- [ ] Negative: hash/path traversal/link/duplicate member, DB/repo generation mismatch, wrong PG major, nonempty target, shared filesystem insufficient space, lost sidecar, ENOSPC/kill midcopy/pg_restore; failed target остаётся offline, очистка/новая disk требуют отдельного решения.

**Future existing commands:** `qcl-negf-state-archive create PRIVATE/controller-ATTEMPT.tar.gz --source-revision ROOT_SHA --disk-budget-bytes BYTES --writers-paused`; `qcl-negf-state-archive verify PRIVATE/controller-ATTEMPT.tar.gz`; `qcl-negf-state-archive restore EXTERNAL/controller-ATTEMPT.tar.gz --disk-budget-bytes BYTES --writers-paused`. **Admission:** per-st_dev extraction+file copies+PG; PG reserve≥2×physical DB+1 GiB, ≥64 MiB filesystem headroom+4096/file, retained archive входит budget; недостаток не лечится удалением originals.

**Cost:** L; create/copy/restore по одной attempt, ≤2 h/операцию и общий cap≤6 h, exact byte budget после измерения, output≤16 MiB. P1/B явно заменяет prerequisite numeric RTO SLA: goal — нулевая потеря confirmed persistent data, RTO measured-only. До BIND установить boundary `t_last_consistent`, incident detection, restore start, service verification; отсутствие numeric SLA capture/restore не блокирует. Receipt измеряет RPO=`incident−last_consistent`, RTO=`verified_service−incident`; active-job loss/foreign state отдельно. `Meets recovery-time objective` без принятого target не заявляется. CP-RELEASE и production replacement требуют actual isolated rehearsal, не fixture extraction.

## OPS11 — Proxmox worker: fresh install, boot и native faults

**Роль/owner:** D ultra для consumer installer surface, I medium, R/audit high. Platform. **Paths:** existing `P/tofu/proxmox/`, `P/ansible/proxmox-images.yml`, `P/ops/{image_reader,image_stage}.py`, `P/tests/test_image_transfer.py`, `P/tests/test_proxmox_storage_contract.py`; **предлагается** отдельный worker-only provider example/recipe, поскольку current proxmox module требует ровно four roles. **Deps:** D принимает OPS07.D и возвращает boot/format choice; I по accepted D; installation ждёт OPS07.N + OPS01 target/storage/network, BUILD для declared isolated test VM либо CP-OPS для enrolled/production VM. Shutdown acceptance OPS14.N следует после install.

- [ ] D выбрать single-worker install route, не передавать one-node map в current four-role provider. I добавить адресный пример/adapter с same pinned provider, existing bridge/datastores, unique VM/MAC/disk serial, independent replaceable root+scratch; не ослаблять protected storage/control или TLS.
- [ ] Fresh install из delivered checksum-pinned artifact, provider plan review no unrelated delete/replace, boot current+booted identities и first-boot unique keys; controller/NFS reachability, DNS/MTU/time, callback ports, scratch serial/mount и hard memory after reserves.
- [ ] Enrollment из verified provider/guest/host-key observations; DRAIN до matching release/node health; tiny batch+srun, staged result/readback, normal shutdown/return и controlled force loss в dedicated test VM. Никакого принятия только по `tofu validate`/API running.
- [ ] Negative: checksum/size/header fail, partial transfer/ENOSPC, existing corrupt image/symlink, wrong datastore, VMID collision, disk ownership unknown, stale NodeName, duplicate machine-id, host-key mismatch. Existing-file receipt только после verified staging.

**Future existing commands:** Ansible `ansible-playbook -i PRIVATE/inventory.ini -e @PRIVATE/image-transfer.yml P/ansible/proxmox-images.yml --check`, затем apply без `--check` в declared BUILD rehearsal scope либо CP-OPS; production/enrolled target только CP-OPS. Existing four-role `tofu -chdir=P/tofu/proxmox plan -var-file=PRIVATE/proxmox-staged.tfvars.json`; новый single-worker CLI пометить/документировать после D. **Outputs:** actual import file ID/SHA/bytes, raw boot/network/job/shutdown proof, installer receipt с backend/version/VM identity и artifacts. **Cost:** L; native 1 fresh install≤90 min, staging≤4×300 s для four-role или≤300 s one image +local verify reserve; guest CPU/RAM/disk из admission, no foreign VM stop. Blocked Proxmox hardware блокирует этот backend, не OPS03/12/13 source work.

## OPS12 — Linux/libvirt worker: fresh install и независимая приёмка

**Роль/owner:** D ultra если расширяется beyond Arch, I medium, R/audit high. Platform. **Paths:** existing `P/tofu/arch-libvirt/{main,variables,versions}.tf`, `P/tofu/arch-libvirt/site-base.json.example`, `P/tofu/build-images.ts`, `P/docs/infrastructure.md`; **предлагается** `P/docs/linux-worker-install.md` и focused provider fixtures. **Deps:** D принимает OPS07.D и возвращает format/boot choice; I по accepted D; install ждёт OPS07.N и OPS01 native host readiness, BUILD для declared isolated domain либо CP-OPS для enrolled/production domain. OPS14.N следует после install. Слово Linux не расширяет verified support автоматически на все дистрибутивы.

- [ ] Сохранить existing Arch/libvirt route; generalized Linux prerequisites/version range обозначить candidate до measured host acceptance. Явно проверить KVM access, existing LAN bridge без hidden NAT, libvirt system URI/trust, storage capacity/ownership, qemu guest tooling и nested virtualization если применимо.
- [ ] Из delivered QCOW2 создать unique root overlay и separate scratch; current fixed `arch-worker` names/serial/enrollment не клонировать для второго узла. Parameterization names/NodeName/serial входит I-task, before/after fixture не трогает foreign domains/pool.
- [ ] Fresh boot→unique machine/host keys→network/DNS/time/NFS/callback→trusted enrollment→DRAIN/release checks→batch+srun/staging→normal shutdown/return и forced worker loss. Root replacement сохраняет scratch только по проверенному serial; scratch не backup.
- [ ] Negative/fault: image hash fail, pool symlink/path collision, missing bridge/KVM, unsupported qemu/boot mode, low host RAM, NFS interruption, URI host-key mismatch, changed guest boot midprobe. Hardcoded 30 GiB/12vCPU/512GiB defaults из existing example не считать fresh measurements.

**Future existing commands:** `tofu -chdir=P/tofu/arch-libvirt init -backend-config=path=PRIVATE/state/arch-libvirt.tfstate`; `tofu -chdir=P/tofu/arch-libvirt validate`; `tofu -chdir=P/tofu/arch-libvirt plan -var-file=PRIVATE/arch-libvirt.tfvars.json -out=PRIVATE/worker.tfplan`; apply exact saved plan после свежего admission в declared BUILD rehearsal scope либо CP-OPS; production/enrolled domain только CP-OPS. **Outputs:** provider plan hash/actual domain identity, image+root+scratch identity, verified guest/service/job/fault receipts и installer docs. **Cost:** L; one install≤90 min, smoke/fault≤45 min, bytes≤image+root/scratch declared allocated peak+reserve; reserves native host определяет operator. Unknown hardware блокирует native cell только этого backend; source PR и Proxmox/Hyper-V work продолжаются.

## OPS13 — Windows/Hyper-V: настоящий installer, отдельно от wrappers

**Роль/owner:** D ultra для boot/installer contract, I medium, R/audit high. Platform. **Paths:** existing `P/windows/{Start-QclWorker,Shutdown-QclWorker}.ps1`, `P/docs/windows-workers.md`; **предлагаются** `P/windows/Install-QclWorker.ps1`, `P/windows/Test-QclWorkerHost.ps1`, `P/windows/worker-config.json.example`, `P/tests/test_windows_installer.py` и native PowerShell fixtures. **Deps:** D принимает OPS07.D и OPS14.D lifecycle contract и возвращает boot/format choice; I — accepted D, OPS02/03 и нужный OPS14.I source output, не OPS14.N. Install требует OPS07.N и fresh Windows admission. BUILD rehearsal/CP-OPS явно перечисляет **каждую** разрешённую Windows машину; один согласованный packet может покрыть обе и conditional phases. OPS14.N после install, не prerequisite install.

**Interfaces/output (предложение до D):** installer принимает protected nonsecret config path + expected manifest SHA256, explicit VMName/switch/root/scratch destinations/controller endpoint/NodeName/resources; dry-run default и отдельное Apply. Secrets/trusted enrollment не скачивает и не генерирует за пользователя. Preflight возвращает machine/Windows/Hyper-V versions, virtualization capability, free RAM/disk, switch, disk path identity, collision checks; no VM creation при failed preflight. Current Start-QclWorker запускает **существующую** VM и не считается installer.

- [ ] D разрешить несовпадение current legacy BIOS QCOW2 и Hyper-V boot generations: либо tested Generation 1 BIOS+IDE boot VHDX, либо отдельный reviewed UEFI/GPT Generation 2 artifact. Не просто переименовать QCOW2 в VHDX; conversion tool/output derivation/version/hash включить в distribution. Secure Boot decision явный, не молчаливое отключение.
- [ ] I создать VM, attach separate root/scratch, explicit vSwitch/MAC/CPU/RAM/no arbitrary overcommit, boot order/guest drivers/time/network и idempotent ownership receipt. Existing unrelated VM/path never overwritten; partial creation остаётся inspectable и не удаляется blind retry.
- [ ] Native на обоих required hosts: install from fresh directory, boot/network/NFS/callbacks, trusted enrollment+DRAIN, release check/batch+srun/staging, Windows Start→Shutdown ordering и changed-release return. Nested Hyper-V support измерить на outer host, Administrator не доказательство.
- [ ] Negative: unsupported hardware/nesting/Windows edition, no vSwitch, incompatible generation, manifest/hash mismatch, malicious path, existing VM/disk, insufficient RAM/disk, interrupted convert/create, network loss, bad host key. Native unavailable = backend `blocked/not_measured`, не весь independent DEV blocked.

**Commands:** текущие PowerShell param blocks изучены; installer CLI ещё **предлагается**, его синтаксис публикуется CP-DESIGN до I. Для существующих wrappers будущий вызов: `powershell.exe -NoProfile -File Start-QclWorker.ps1 -Controller ROUTE -Node NODE -WorkerTarget WORKER -Enrollment /protected/enrollment.json -EnrollmentId UUID -VmName VM`; Shutdown имеет те же первые enrollment arguments без VmName. **Cost/gates:** L для source/fake fixtures без Windows; native one install+scenario set/host≤2 h, guest allocation по fresh host reserves, output≤16 MiB. First-use trust — CP-EXCEPTION; Windows policy/Admin/VM changes — named BUILD rehearsal либо CP-OPS для production воздействия. Missing hardware не требует приостанавливать source changes и не является acceptance.

## OPS14 — normal worker shutdown, recovery и fault matrix

**Роль/owner:** D ultra для неразрешённого host ordering, I medium, R/audit high. Platform с Runner/AiiDA owning tickets для durable data. **Paths:** `P/ops/worker_lifecycle.py`, tests worker_lifecycle/shutdown_intent, Windows scripts/docs; Runner `stage_result_tree`, `verify-stop`, Results readers — отдельные component tickets. **Deps:** OPS14.D требует только OPS02/08 accepted source contracts; OPS14.I — готовый D и релевантный OPS03/08 code; лишь OPS14.N требует выбранный installed backend OPS11/12/13. Не ждать native matrix для выпуска design/source output. Concurrency не увеличивает общий allowance.

**Contract/output:** existing `qcl-negf-shutdown-intent-v2` сохраняется до `resumed`; normal shutdown DRAIN, захватывает **всех** RUNNING/COMPLETING owners и ждёт pinned Runner durable pause/terminal proof **и** allocation exit. Никакой свободный successor worker не нужен. Startup — authenticated root through scoped sudo, same enrolled permanent machine/new boot, delivery текущего релиза, fresh registration перед RESUME. Нормальное ожидание не имеет arbitrary total timeout; acceptance observation window конечен и при исчерпании оставляет узел DRAIN с unknown, не force poweroff.

- [ ] Матрица per backend: idle/repeated shutdown, two owners/несколько jobs, slow checkpoint, temporary NFS/controller loss, job завершился между capture/pause, исчезший job без receipt, no free worker, client death, v1 migration/orphan capture, startup response lost, changed release return, power loss. Последний сценарий даёт только периодическую recovery по durable checkpoint, не гарантию последнего in-memory state.
- [ ] Windows отдельно доказать timeline GPO→proof on permanent node→guest/VMMS/network stop на обеих машинах. `MaxGPOScriptWaitPolicy=0` — candidate policy, не доказательство ordering. При отрицательном результате отдельный D native preshutdown service; finite service timeout не заменяет unlimited safe-stop contract.
- [ ] Проверить pinned execution/attempt/solver/output comments, original arrays/checkpoint hashes independent Results reader, before/after physical PID/cgroup stop. Не подменять Runner proof scheduler disappearance и не объявлять safe_stop scientific_accepted.

**Future existing commands:** `sudo qcl-negf-worker-lifecycle shutdown --node NODE --target ROUTE --enrollment PROTECTED`; startup симметрично. Runner: `PINNED_SOLVER pause SHARED_OUTPUT --execution-id ID --attempt N`, затем `PINNED_SOLVER verify-stop SHARED_OUTPUT --execution-id ID --attempt N` от job owner. Physical read-only collector:

```sh
python3 P/ops/slurm_job_evidence.py --mode before --expected EXPECTED.json \
  --expected-sha256 EXPECTED_SHA --scontrol IMMUTABLE_SCONTROL --out NEW_BEFORE
python3 P/ops/slurm_job_evidence.py --mode after --expected EXPECTED.json \
  --expected-sha256 EXPECTED_SHA --scontrol IMMUTABLE_SCONTROL \
  --before NEW_BEFORE/proof.json --before-sha256 BEFORE_SHA --out NEW_AFTER
```

EXPECTED привязан к actual numeric job ID, UID3000, immutable slurmstepd, exact cgroup, machine/boot. Before непустой и содержит PID/start_ticks; after доказывает исчезновение/смену ticks каждого исходного PID и unpopulated subtree вместе с terminal scheduler state. **Cost:** each native backend observation≤60 min, one controlled loss/test VM; engineering fixture job≤2CPU/2GiB/10min/attempt, 2 attempts maximum **включая recovery**, staged payload≤1 GiB, all grants shared. Real SCBA здесь запрещён. **Gates:** source CP-CODE, native CP-NATIVE, production host shutdown/fault CP-OPS. Недоказанное ordering блокирует auto-shutdown этого backend, manual documented route остаётся отдельным решением.

## OPS15 — инструкции пользователя: fresh install, update и rollback

**Роль/owner:** D/document author ultra, I medium для примеров/инструментов, R/audit high. Platform/Root docs. **Paths:** existing `P/docs/{infrastructure,windows-workers,operations,image-transfer,application-cd,state-archive}.md`, root deployment runbook; proposed worker-distribution/Linux install docs OPS07/12 и installer examples OPS11/13. **Deps:** accepted interfaces OPS07–14; native missing cells явно отражены, инструкции source не ждут hardware.

- [ ] Выдать один entry README внутри bundle: что скачать/какой checksum/куда сохранить, supported host matrix, finite disk/RAM prerequisites, explicit controller/NFS endpoints, secrets provisioner, trust enrollment и DRAIN; отдельные разделы Proxmox/Linux/Windows с **fresh** install и first successful test job.
- [ ] Описать manual initial install как поддерживаемый маршрут, если automation backend ещё candidate. Для каждого шага команда/GUI location, expected observation, safe stop при failure и сохраняемый receipt; Start wrapper не появляется под заголовком fresh installer.
- [ ] Дать upgrade на конкретный release по I14: manual QCL cancel, all workers stop, service/release gates, operator signal. Дать rollback: immutable previous closure/OS generation + matching runtime identity; отдельно DB schema/state, потому что OS rollback не откатывает DB. Если предыдущий schema incompatible — isolated restore, не автоматический downgrade.
- [ ] Clean reinstall выбирает только replacement root по serial; persistent data/state/scratch защищены, initial-format flags после первого install выключаются. Retire/re-enroll отдельный trusted flow. Никаких copy-paste secret/private addresses в public examples.
- [ ] Независимый reader проходит с blank config и delivered files: все local links/commands/placeholders resolvable, recipe/source/manifest соответствуют, download checksum verified на recipient. Public docs fixed light/local assets; deployment guide не переносит science criteria в UI.

**Outputs:** user-ready guide, command/GUI transcript dry-run и observed native annotations, compatibility/recovery matrix, exact where/how delivery receipt. RV18 отдаёт ссылку на owning versioned guide и source-bound artifact; новый docs hub не условие source fixes. **Future checks:** targeted Markdown links/format и bundle manifest fixture; команды installer берутся из accepted help/param blocks. **Cost:** docs review≤60 min, L при изменении assembler; no full suite/build. **Gates:** authoring CP-DESIGN/CP-CODE, owning docs PR — PUBLISH, candidate guide с bundle — declared BUILD/OPS staging; completed guide/receipts входят в final CP-RELEASE. Public release отдельно CP-EXCEPTION; новая credential/trust identity также CP-EXCEPTION. Документ не заявляет неисполненные native steps успешными.

## OPS16 — freeze source, одна final CI и release evidence

**Роль/owner:** audit/coordinator high, I medium для exact publication actions, R high; D ultra только для policy change. Root/Platform. **Paths:** `ops/git.ts`, `ops/{release,application_cd,publish,ci}.ts`, `.github/workflows/ci.yml`, root gitlinks, owning component PRs. **Deps:** ready component code/docs, OPS04 source binding, required native cells OPS05–15 и separate science readiness. G1 merge и B OPS согласованы в P1/approved_standby; до EXEC действий нет. Merge strategy обязана сохранить final-source identity для sole CI.

- [ ] Опубликовать component refs отдельными PRs, проверить remote availability каждого selected commit; затем root exact gitlinks, clean targeted diff, lock/source graph. PR state/remote heads/protections перечитать на final ready stage.
- [ ] Отделить инженерный reuse от final acceptance нового HEAD. Изменённый root/source после freeze инвалидирует относящиеся к нему claims; untouched native derivation можно carry-forward только OPS04 с original proof.
- [ ] Перед registration/CI fresh empty queue/build idle, final resources standard, CI user isolation/no sudo/trusted Nix/admin private access. PAT у администратора, jobs получают только short-lived runner registration token.
- [ ] Dispatch **один** full workflow final ref; retain run ID, `head_sha`, logs/artifacts/timeout/result. Не запускать interim full CI «проверить как идёт» и не rerun при failure. Repair требует нового явно рассмотренного release decision, а не автоматического цикла.

**Future existing commands:** root `deno task graph`; published root CI: `gh workflow run ci.yml --ref FINAL_REF -f scope=full`; только read followup `gh run view RUN_ID --json headSha,status,conclusion,url`. Workflow существует как `.github/workflows/ci.yml`, full timeout 180 min; `runner-smoke` 5 min не full acceptance и не добавляется в этот single-CI allowance автоматически. `deno task release RELEASE_DIR --build` — separate artifact build, не CI dispatch.

**Outputs/cost:** CP-RELEASE dossier с source/PR identities, exact CI run/expected head_sha, artifact checksums, known limits и native matrix; один CI≤180 min, ресурсы runner standard 4CPU/8GiB/shared slice, output по workflow retention+private accounting. CP-NATIVE build grant и CP-OPS deploy остаются отдельными. Failure CI сохраняется как failure; coordinator возвращает конкретный ticket, не выдаёт green по отдельным subset checks.

## OPS17 — доставка, работающий cluster и передача physical attempt

**Роль/owner:** coordinator/audit high, независимый R high; I medium для разрешённой delivery verification, D ultra только при новом interface. Root/Platform; следующий physical attempt принадлежит научному пакету handoff. **Deps:** OPS01–16, source/model/results/AiiDA tickets соседних пакетов, final CP-RELEASE и CP-OPS BIND. B/G1/S1 без e–e approved_standby; EXEC не активирован, fresh bindings/native readiness ещё не получены. Public release отдельно оператору.

- [ ] Проверить delivered bundle на destination/recipient: actual URI либо offline medium и filenames, measured bytes/SHA256, immutable manifest/source/native receipts, user guide, trust-key fingerprint out-of-band. Простое наличие artifacts на builder не завершает delivery.
- [ ] Выпустить acceptance matrix: storage/control/CI и **каждый enrolled worker**, backend/host/OS boot/service/release/enrollment/network/batch/srun/staging/stop/recovery/restore cells с attempt/locator/outcome; offline node не скрывается. Missing required Windows machine означает partially accepted release, не «полностью работающий cluster».
- [ ] Проверить production allocation после bootstrap (host/foreign reserve, VM max RAM, Slurm RealMemory физическая RAM без swap, builder standard), no hidden old-state dependency, clean source→artifact→runtime chain, one authoritative controller, verified backup/isolated restore и rollback readiness.
- [ ] Передать научному исполнителю `runtime-ready` packet: exact release/solver/import identities, actual active workers/resources/storage capacity, admission state, scientific Code UUID и run output route, checkpoint/stop/recovery semantics, known backend limits. Packet не содержит новых физических defaults и не открывает scientific admission сам.
- [ ] Только после EXEC и technical CP-SCI READY по уже принятому P1/S1 без e–e coordinator запускает **порученную** physical convergence attempt через штатный Runner/AiiDA; frozen plan/run/attempt связываются с runtime и S1 accounting. Повторное одобрение model/catalog не требуется внутри P1. Infrastructure exit0/job completion не сходимость; критерии задаёт scientific owner. Нерелевантный backend blocker допускает early exploratory run по его собственным gates, не full-release acceptance.

**Interfaces/output:** предлагаемый sanitized `runtime-readiness.json` — evidence projection, с refs на owning source graph/release manifest/individual receipts, статусом каждого gate, freshness и unresolved inputs; это не новый source authority. Public delivery guide+checksum links, private operational appendix и таблица ниже. **Cost:** final readback 1 attempt≤30 min/8 MiB, no solver до scientific grant; physical CPU/RAM/wall/output/attempts задаются отдельным общим бюджетом, не N. **Stop/gates:** identity mismatch, stale admission, unknown mutation, missing backup/operator input — dependent gate blocked; scientific negative result сохраняется, model/tolerances ради pass не меняются.

## Покрытие review и зависимости на соседние пакеты

| Review / требование | Закрывающие карточки и необходимое evidence | Что само по себе не закрывает замечание |
| --- | --- | --- |
| RV06, CR02–05, I14 | OPS02 D → OPS03 I; OPS08 source/fault → OPS09/14 native | Второй lock filename; согласие агентов; fake Nix/SSH |
| RV11 | OPS10 coordinated restore; OPS14 stop/durable bundle с Runner/Results owner | Slurm disappearance, exit0, receipt без arrays/attempt |
| RV12 | OPS08 cancel all parent/retry/jobs, OPS09/14 physical stop/readback | Finish parent без stop job; hidden duplicate submit |
| RV13 | OPS01 inventories/ownership, OPS05/09 roles, OPS10 actual restore, OPS11–13 cold install | Old inventory; tofu validate; same-server backup |
| RV14 | OPS04 exact source/import/derivation/contents, OPS06/07 receipts, OPS16 final CI | Package version; новый root наследует old full acceptance |
| RV15 | OPS01 protected inputs, OPS04 trust/rejected paths, OPS07 no-secret artifact, OPS08 scopes | Disabled host keys/TLS/signatures; CI admin credentials |
| RV18 / I07–I09 | OPS07/15 versioned owning guides/local light assets; OPS11–14 backend matrix | Wrapper вместо installer; docs hub вместо boot |
| Полный cluster → science | OPS17 measured runtime packet → scientific package frozen attempt | Engineering self-check или «работает» вместо convergence |

Runner/Results RV11 и AiiDA RV12 код меняется в owning component по своему ticket; OPS не переносит туда Platform lock. Portal/RV18 owner получает versioned public docs/source binding и сохраняет fixed light theme. Отсутствие archive/HDF5 не блокирует source-only OPS02–08/11–15; архив нужен только claim о конкретном расчёте.

## Открытые входы: что запросить ровно перед зависимым gate

- [ ] После отдельного EXEC использовать уже согласованный B/DEV на owning paths/targeted L checks; CP-DESIGN OPS02 и independent review до OPS03. Принятые права повторно не спрашивать.
- [ ] Fresh доступ к конкретному site и approved read-only collector; актуальные host/VM/storage ownership, pnetlab/foreign reserves, actual builder PID/RAM/CPU/disk, queue/idle, maintenance exclusivity.
- [ ] Immutable published source/gitlinks/locks; actual depot URL/hash/receipt, old native contents proof и manifests либо бюджет cold build; ни old `5060e10`, ни `93880c23` не выдаются за installed runtime.
- [ ] BUILD: единый finite preflight/build/rehearsal envelope, targets/namespaces/privileges/private staging, attempts/deadline/resources/output/disk reserve/stop, кто наблюдает progress. CP-NATIVE — внутренний evidence gate перед heavy stage; BUILD не production OPS.
- [ ] CP-OPS: exact inventory generation/VM IDs/candidate+source hash/window/existing backup hash+medium/disk serials/allowed phase actions/rollback. Capture/pause/resume и production replacement имеют свои prerequisites; один packet может дать conditional phases. First-use fingerprints/cache trust, credential/destructive exceptions явно CP-EXCEPTION; foreign resources не включать по умолчанию.
- [ ] Proxmox target/bridges/datastores, Linux/libvirt host capability, обе required Windows machines и nesting/edition/vSwitch/boot generation; unavailable hardware отмечается по backend, не блокирует независимый source scope.
- [ ] Принятый B goal zero loss confirmed persistent data и измеряемые RPO/RTO без numeric RTO SLA; exact isolated target/disk/external copy/NFS+secret recovery boundary определить до BIND.
- [ ] Destination, retention и recipient для дистрибутива, trusted publication/offline copy route и проверка SHA на получателе.
- [ ] Final CI registration credentials у администратора, final ready ref и один dispatch; после runtime readiness технический CP-SCI READY на approved S1 без e–e, без повторного human approval каталога.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| План опирается на текущие public interfaces | root `93880c23`, Platform `6c5b11f`, проверенные source/argparse/param blocks | Сервер не читался, команды не исполнялись | сохранить |
| Controller ownership требует отдельного D/I closure | `application_release.py::main/lifecycle_owner/deliver_cli`, разные lock и self SSH child | Предложенный helper ещё не реализован/принят | изменить |
| Existing I14 source имеет полный enrolled barrier | `deliver_cli/_deliver_cli_locked`, required_nodes/worker_stop/fleet_health | Не VM poweroff; native production не доказан | дополнительно измерить |
| Дистрибутив и три installer backend требуют самостоятельной выдачи | `nix/images.nix`, `tofu/proxmox`, `tofu/arch-libvirt`, Windows wrappers | Hyper-V installer отсутствует, fresh hardware unknown | изменить |
| Production readiness и convergence сейчас не установлены | Fresh admission/depot/runtime/native/restore receipts отсутствуют | Old inventory/review не заменяют новые факты | данных недостаточно |
