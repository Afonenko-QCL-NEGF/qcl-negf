# Docs routing D3 — исполнимые source-адаптеры и независимый native gate

2026-10-20. Source-only архитектурный контракт для I2. Применяется поверх D1/D2 и их high R; не утверждает actual native readiness. Никаких solver/build/final CI, probes, target imports/parse/typecheck/tests, установки или серверных действий. Только этот D3, identity и read ledger. Единственный оставшийся pure GREEN принадлежит Root. Новые product-unit calls этот D3 не добавляет; два compiler-only source checks возможны только при отдельном точном плане Root.

## Основания и граница

Selected source — isolated `/tmp/qcl-docs-test-routing-worktree`, HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`; dirty overlay состоит из четырёх tracked routing edits и двух untracked helper/fixture files. Helper SHA256 `bdc1684faffa4e6606b1667675f335768e3eb6216ae64b5842d2431460063356`; historic RED fixture SHA256 `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3`. Root HEAD автора в основном workspace — `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; он не подменяет selected source.

Выбранные восемь gitlinks прочитаны через `git ls-tree HEAD components/`; source authority остаётся Git, отдельный lock не создаётся. Owning platform — `f729e2681224d6537538179ab760fefefd575003`, читается в `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-platform`. В основном workspace platform другой; его предварительное чтение не используется для утверждений о selected API.

Primary источники:

- Root `ops/git.ts:39–103`: `git()` использует `--no-optional-locks`, clearEnv и `GIT_OPTIONAL_LOCKS=0`; `sourceGraph(root,requireClean)` выводит flat graph из gitlinks, сверяет HEAD/clean всех восьми компонентов и `.gitmodules`. Не заменять его вторым вручную составленным manifest.
- Selected platform `ops/bootstrap_build.py:57–147` `_CommandOwner`, `:150–286` `_command_supervisor`, `:290–380` `run(argv,seconds,cap)`: private subreaper, baseline/ancestry/UID/birth ownership, pidfds, dispatch gate, cleanup/ACK, deadline и combined output bound уже существуют. `run` не принимает cwd/env; child наследует их; capture в памяти декодируется с replacement, при cap обрезается; RAM/TMP/retained-tool reader не реализованы. Это lifecycle reference, **не** готовый docs executor и не hard resource authority.
- Selected platform `ops/build_admission.py:58–131`: `admit(snapshot,profile,now,resources)` и result `qcl-build-admission-result.v1`, expiry `captured_at+60`; `read_snapshot` ограничен 1MiB. `docs/build-admission.md` прямо отделяет input consistency от authorization/resource lock. Этот формат — host build admission, не tool identity и не unit ownership token. Не добавлять к нему invented docs/tool поля.
- Root bounded engineering `/tmp/qcl-docs-routing-local-unit-run-v2.py`: exact `--execute`/scope/attempt + fresh Root handoff, actual hashes, exclusive0700 directories, affinity/RLIMIT_CPU, prelaunch/terminal observations и retained receipt/raw. Its process-group cleanup и50ms RSS/TMP guards явно sampled; escaped descendants/hard RAM/disk не доказаны. `/tmp/qcl-docs-routing-engineering-plan-v2.json` сохраняет эту границу.
- DOC06 `/tmp/qcl-doc06-local-unit-run-v2.py:44–113,148–174,240–263`: 13-node fixed seed, no-follow inventory, prelaunch/terminal debit. Его ambient filtered env и cache-inside-TMP **не** переносятся в D2 dedicated route. Accepted symlink D/high R определяют два fixed trees и56 registrations.

## Решение и owning paths I2

Недостаёт локального source API, а не только доступа к серверу. I2 должен добавить **Root-owned** `ops/docs_tests_native.py` (trusted launcher/storage/supervisor/retained readers) и `ops/docs_tests_cli.ts` (тонкий protocol driver, использующий существующий pure helper и owning sourceGraph). Это integration tooling Root; platform formulas/production admission/installed services не меняются. Если потребуется вынести general supervisor в platform, это отдельный owning PR с опубликованным gitlink; в I2 такое расширение не требуется.

`ops/docs_tests.ts` остаётся self-contained pure API без импортов и import-time side effects; его девять exports и positive synthetic fixtures сохраняются. Tasks check/docs:check/docs:preflight переходят на native launcher, который реально имеет validate→plan→supervise→capture→aggregate route. Отсутствующий active handoff даёт конкретный blocked; наличие валидного handoff вызывает настоящий executor. Stub, всегда возвращающий blocked независимо от входа, недопустим.

Допустимо узкое backwards-compatible расширение `ops/git.ts`: `sourceGraph(root, requireClean, executable = 'git')`, `git(root,args,executable='git')`; executable передаётся только в Command.executable, args/clearEnv/env/graph checks сохраняются. Native driver всегда подаёт exact absolute Git, выбранный active harness; существующие consumers сохраняют default. Это не четвёртая tool-entry descriptor: Git принадлежит существующему Root read-only source protocol и отдельно связывается native closure/handoff. Без exact executable binding route blocked, PATH fallback запрещён.

## Native closure: совместимость с exact12 descriptor

D1/D2 `qcl-negf.docs-test-inputs.v1`, exact12 `source_files`, deno/node/python, loader_env={} и synthetic pure fixtures **не менять** ради нового adapter. Не добавлять четвёртый tool, optional metadata keys, arbitrary schema names или normalized booleans в persisted inputs.

Native closure — отдельный **private handoff attachment**, не новая product/public schema, не второй revision lock. Его fixed path set: все12 descriptor sources плюс `ops/docs_tests_native.py`, `ops/docs_tests_cli.ts`, `ops/git.ts`, `ops/process.ts`; если native file импортирует дополнительный local code, он входит в этот fixed reviewed closure до CPP. Python stdlib/runtime closure относится к tool observation, не бесконечному source list. Native reader сверяет каждый путь с blob того же actual final Root HEAD (`git cat-file`/`ls-tree`), actual regular no-link working bytes и actual SHA; оба CLI files и transitively imported source должны быть committed. Clean graph обязателен. Attachment сохраняет derived `(Root HEAD, graph digest, path,blob,SHA)` и actual driver/supervisor/tool/Git bytes hashes; commit-derived list не поддерживается вручную между релизами. Перед/после и перед каждым child — равенство всего binding. Source overlay в текущем2bb поэтому пока не native-ready.

Pure `parseInputs/preflightInputs` знают свои12 entries; attachment проверяет production adapter до вызова pure Ready. Pure manufactured metadata не получает native privilege и может оставаться synthetic. Source CPP обязан отдельно проверить **реальную** CLI closure/entrypoint/task wiring, а не приписывать её sole GREEN. Native binding с другим source SHA не применяется к reviewed source; final count56/15/20 устанавливается по actual final test bytes/selected tool report contract, не по synthetic7/observed output.

## Trusted retained reader и active handoff

Существующего general persisted tool-identity/admission-trust API не найдено. Нельзя объявить `normalized-tool-identity`, `externally_measured:true`, `fresh:true`, `limits_enforced:true` accepted format. I2 вводит только private adapter protocol с typed observations; authority приходит от уже порученного, active trusted Root/operator/CI setup процесса, как в bounded engineering harness, а не от содержимого caller JSON или ownership файла само по себе.

Точные private in-process API native owner (не JSON authorization endpoint):

```python
read_bound_regular(ref, maximum, expected_owner, expected_parent) -> BoundBytes
# os.open O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC, fstat regular, bounded read(max+1),
# SHA от ЭТОГО buffer; close на всех outcomes; ancestors проверены no-link.

bind_native_context(parsed, active: ActiveDocsAttempt, now_utc, monotonic) -> BoundContext
# ActiveDocsAttempt — созданный active launcher object, не deserialize(inputs).
# scope ('docs-units-only'|'full-root-check'|'prerequisites-only'), attempt,
# exact input/ref/source/native closure/runtime/Git hashes, caller uid,
# exclusive storage roots, permitted limits, deadline, external_guard adapter.

read_tool_observation(name, ref, active) -> ToolObservation | Refusal
read_katex_observation(ref, active) -> KatexObservation | Refusal
read_reviewed_unit_binding(name, final_test_sha, active) -> ReviewedUnit | Refusal
```

`BoundBytes` содержит actual bytes/hash/stat identity. ToolObservation содержит exact executable canonical path/hash/version, measured command/exit/raw refs и producer attempt/source binding. Reader принимает **только exact контракт конкретного producer**, зарегистрированный в reviewed native code/active handoff; opaque arbitrary `schema` из descriptor не выбирает parser. Для уже имеющихся local engineering receipts validator использует их реальные exact fields/hash/raw predicates (v2 harness показывает образец), не переименовывает их в general tool schema. Таких accepted retained Node24/Python3.14/Git observations и CI producer binding здесь нет: actual full route blocked до их подготовки. D3 не придумывает их future hashes/versions/format и не использует Deno RED receipt как Node/Python version evidence.

Для будущего CI setup public native source adapter — `make_active_docs_attempt(...)`: вызывается trusted setup кодом после actual inventory/admission и измерения tools; возвращает opaque context, проверяет actual caller (`getuid/geteuid`, `/proc` birth identity supervisor), scope/attempt/deadline и exact byte refs. CLI handoff file — retained audit attachment, **не** самостоятельная authority: native entry требует active inherited control pipe от этого setup; EOF/cancellation/replay/unknown producer ⇒ refuse before dispatch. При интерактивном отдельно порученном запуске этот pipe создаёт тот же trusted Root launcher после review/READY; исходная `--execute` инструкция должна уже существовать. Workflow не может создать admission самим флагом. Нет fallback «same-user JSON⇒trusted».

Clock: producer timestamp и deadline имеют finite values, no future; host admission expiry ровно owning60s и пересчитывается owning `admit`, без продления. Root READY-consistency window как у existing engineering300s не означает freshness host admission. Monotonic budget начинается до metadata/preparation; wall UTC служит audit, не deadline clock. Если clock/expiry/producer/active principal неизвестны, native context отсутствует. External guard API ниже связывает live resource allocation; host snapshot сам не является lock.

Pure Metadata разрешено строить **только после** всех native readers и live binding: synthetic fields служат адаптацией результата уже выполненных проверок, не доказательством. Native proof хранится отдельно; projected booleans никогда не принимаются из descriptor/pipe JSON от недоверенного caller.

## Protocol и точные capabilities

Native launcher запускает bound Deno driver только после предварительной byte/metadata/admission проверки. Driver имеет permissionless stdio protocol, кроме exact `--allow-run=ABS_GIT`, необходимого owning sourceGraph; no read/write/env/net/ffi/run=python/global-run. Module source loading Deno отдельно от script permission; native closure обязательно source-reviewed. Driver environment clear, ровно admitted DENO_DIR и фиксированный PATH к единственному admitted Git parent если существующему Command resolution это нужно; Git вызов в любом случае absolute. Эти env относятся к private driver, **не** dedicated units D2. Native launcher bootstrap interpreter должен сам совпасть с admitted Python path/hash прежде side effects; ambient `python3` только запускает проверку, mismatch blocks. Tasks не передают Deno unlimited `--allow-run` и не дают supervisor execution capability unit children.

Private bounded NDJSON control protocol, closed set, one outstanding request:

```ts
type Request =
 | {op:'preflight'; input:string} // descriptor raw <=32768 bytes
 | {op:'prepare'; input_sha256:string; plan:Plan}
 | {op:'execute'; index:number; step:Step}
 | {op:'finish'; aggregate:unknown};
type Response =
 | {kind:'metadata'; metadata:Metadata; binding_digest:string}
 | {kind:'prepared'; binding_digest:string; seed_ref:Ref}
 | {kind:'capture'; index:number; capture:Capture; evidence_ref:Ref}
 | {kind:'refused'; phase:string; code:string; retained_ref:Ref|null};
```

Это private transport между двумя уже bound reviewed processes; не persisted schema/trust root. Request maximum — descriptor32768, прочие requests131072B; metadata/ref responses131072B. Capture response имеет отдельный предел `6*per_step_log_bytes+65536` (JSON worst-case escaping), stdout+stderr actual bytes совместно≤per_step_log_bytes; retained raw refs обязательны. Обе стороны читают incremental bounded buffer, не unlimited readline/readAll; serialized protocol/cache bytes входят в private transport budget active envelope. No arbitrary argv execution. Textual captures для existing pure interface возвращаются только после bounded raw bytes+fatal UTF8 decode; invalid UTF8 retained and failed. Native side независимо сравнивает index/step с единственным plan, полученным от exact driver по своему input/source binding; units/paths/env/limits не выбираются caller selector. Unknown op/index/duplicates/out-of-order/request-after-finish ⇒ cancel/retain/fail. Frames read bounded line-by-line; response shape/byte caps fixed before allocation; no JSON output смешанный с raw child stdout. Raw streams отдельные exclusive files.

`prepare` только для unit mode. Preflight остаётся read-only относительно unit fixtures: никакого seed/child/version/import/unit; только retained/files/Git binding и current guard availability. Preflight **не запускает Deno/Node/Python probes**: driver — initial route process, sourceGraph разрешённый read-only Git. Никакого скрытого bootstrap. Workflow preflight завершается до heavy bootstrap/prepare; полная проверка повторяет binding/admission непосредственно перед первым child. Старый preflight не переносит истёкший grant через долгую подготовку.

## Supervisor и storage lifecycle

Native API:

```python
prepare_owned_storage(ctx) -> StorageLease
seed_doc06(lease) -> SeedObservation
execute_step(ctx, lease, step, *, cancel_fd) -> NativeCapture
close_attempt(ctx, captures, source_observation) -> RetainedAggregate
```

`StorageLease` opaque, не создаётся из arbitrary path. После полного preflight exclusive attempt0700 и child node/python/doc060700, original stdout/stderr/receipt files0600 через O_EXCL. owned_tmp_root/cache/precreated dirs должны быть distinct canonical owned roots из active handoff. До seed нет child; seed/collision/type/permission failure пишет child_started=false, сохраняет raw/error/partialinventory, не удаляет дерево и не repair/retry. Terminal files атомарно публикуются внутри own retained attempt; существующее имя никогда не перезаписывается. Cleanup fixture contract test остаётся owning; supervisor сохраняет attempt, raw, DOC06 prepared trees и measurements при любом outcome.

Lifecycle из OPS04 перенести узко для docs: fresh private per-step subreaper, owner baseline/ancestry+uid/birth+pidfd, parent pins supervisor identity **до dispatch gate**, terminal cleanup и ACK. Не импортировать private `_command_supervisor` и не вызывать `bootstrap_build.py` CLI с пользовательским argv. Новая реализация принимает только validated Step: absolute executable, exact argv/cwd/clearEnv/env D2; `Popen(...,cwd=...,env=exact_map,close_fds=True,stdin=DEVNULL)`; base alone explicit inherited environment. Control FD и cancellation FD не наследуются unit child. Cancellation/parent EOF triggers owned descendants TERM→KILL bounded cleanup; no global killpg/process-wide subreaper; foreign/baseline processes не signal. Ownership ambiguity, cleanup/drain deadline или still-owned descendant ⇒ failure/unknown, never passed. Budget reserve включён в same deadline, после основного child времени для cleanup не добавляется.

Concurrent nonblocking stdout/stderr drains немедленно пишут actual bytes в separate exclusive original streams, считают combined step и aggregate debit; не используют `communicate()` unbounded. При output threshold stop, но bounded cleanup/drain продолжается в общем capture reserve. Если полный stream не помещается finite retention envelope, сохранить bounded prefix + exact observed/discarded bytes where known, capture_complete=false; никогда не prefix→complete. Partial write, storage full, drain exception, invalid UTF8, signal/nonzero, unknown closure сохраняются в receipt и останавливают следующие steps. Для success нужны оба EOF, all owned producers reaped, no cap/truncation/drain/cleanup failure, actual raw hashes/lengths. Memory strings допускаются лишь после bounded retained read.

Resource API active external guard:

```python
external_guard.inspect_binding(ctx) -> GuardBinding
external_guard.attach_private_supervisor(pidfd, expected_birth, limits) -> GuardLease
external_guard.observe(lease, phase) -> GuardSample
external_guard.close_and_verify_empty(lease) -> GuardTerminal
```

Existing backend такого API не реализует; I2 должен реализовать native backend для Linux **делегированного заранее существующего private cgroup v2**, без sudo/systemctl/установки/создания новой службы. Parent verifies exact owned delegated path + live `cgroup.controllers`, CPU quota and actual membership: required `cpu.max = 100000 100000` for descriptor cpu=1, `memory.max = limits.ram_bytes` (≤1073741824), `memory.swap.max = 0`, `pids.max` positive admitted integer≤256. All controls must be writable in already delegated boundary and reread equal before dispatch; supervisor+all child descendants belong to this boundary. Attach before gate via cgroup.procs; close verifies `populated=0` and relevant memory.events. CPU affinity/RLIMIT_CPU из local harness остаются дополнительными; они не подменяют RAM/cgroup. Нет delegation/permission/known path/working hard caps⇒blocked до unit spawn. Shared qcl-build.slice — outer host bound, не доказательство unit1CPU/1GiB; произвольный `limits_enforced` не принимается. Root не принимает чужой cgroup path из descriptor.

TMP: единый active attempt ledger включает node+python+doc06 + CLI Deno cache + runtime HOME/TMP (если они вообще используются) + raw/receipts/control output; disjoint roots не освобождают от суммарного debit. D2 descriptor caps max32+32+8MiB регулируют соответствующие fixtures; отдельные cache/retention caps задаёт active envelope, без default/unbounded области. For success enforce remaining aggregate allowance до каждой записи/seed и prelaunch/terminal measurements, debit failures too. Bounded no-follow census regular payload и all-entry lstat включаются в ledger; no link traversal/double debit alias. Sampled TMP guard честно tagged sampled-stop, не hard disk/transient peak. В active policy должны быть явно приняты trusted source/no adversarial namespace и возможный overshoot; если требуется hard disk quota, backend обязан иметь заранее подготовленную quota/mount boundary, иначе blocked. D3 не меняет RAM cap на sampled-only ради выполнения. Missing physical metrics остаются not_measured.

## DOC06 fixed preparation и counts

Внутри own doc06 TMP реализовать ровно accepted13 nodes: десять real0700 dirs, два links с texts `../../../../backing/configuration_types.jl` и `../backing/core`, один empty exclusive0600 regular file. Exact names/paths — `/tmp/qcl-doc06-symlink-preparation-design.md:35–78` и `/tmp/qcl-doc06-local-unit-run-v2.py:44–58`. No arbitrary target input; strict realpath внутри canonical doc06TMP, links verified lstat/readlink, exact inventory/types/ownership. Baseline regular0, link text57B, inode/physical metadata не объявлять0. Before-seed, after-seed/prelaunch, loop и terminal samples обновляют **и проверяют** global/step thresholds и deadline; overrun before launch ⇒ child_started=false. Complete seed observation ≤8192B retained with native/input/source/count binding.

Child argv/env строго D2: два code-file read paths+ownTMP, ownTMPwrite, one TMP arg after `--`, только DENO_DIR; нет child symlink/rename/global read/write/run/env grants. Healthy topology/9-source witnesses остаются в actual DOC06 test. Сохраняются56 test registrations/15Node/20Python как source-reviewed declarations final source; actual report обязан independently показать exact expected counts и zero applicable failure/skip/todo/ignore/cancel. Base composite semantics прежние, не engine count.

## Failure retention, cheap seams, handoff I2

`runChecks` должен возвращать уже накопленные captures даже когда initial/per-step/terminal `executor.sourceGraph()` throws. Весь orchestration включает binding calls в retained-failure boundary; initial failure ⇒ all captures null, terminal failure ⇒ completed captures byte-exact сохранены, aggregate failed + source_stable=false/unknown + typed reason. Не подменять unknown stable=false как измеренное изменение source. Finalization `finally` сохраняет outcome при transport/reader failures; новый throw не затеняет original child failure/capture. Это требование retention, severity existing review Root решает отдельно.

Source-I2 разрешает только перечисленные owning paths плюс exact task/workflow wiring и narrowly reviewed fixture typing delta. Контракт cheap seams: instrumented bounded reader; short writes/drain failures/output overflow; pre-gate cancellation; stale refs/unknown producer; no delegation; wrong cgroup/membership; wrong topology; seed sample overrun; sourceGraph throws initial/terminal. Часть покрывает existing227 fake fixtures, native seams могут быть source-reviewed injected unit doubles в том же sole GREEN slot при Root source CPP; новых обязательных product calls нет. Реальный cgroup/process isolation и tools не объявляются выполненными из doubles. Если дополнительные focused native tests нужны для уверенности, Root планирует отдельный finite scope; D3 сам попытки не выдаёт.

Frozen historic RED bytes/hash и exact erratum ancestry неизменны. Два proposed explicit nonnull capture assertions около631/760 — допустимое узкое **усиление** current fixture typing перед GREEN после independent source CPP; historic RED сохраняет свой SHA04589… и227 nominal/null observed. Current GREEN fixture имеет новый actual SHA и отдельную reviewed mapping к historic registrations/assertions. V3 predecessor validator должен различать ancestral fixture hash и current reviewed narrowing-format-only hash; запрещены wildcard equivalence, ослабление assertions, no-check и переписываниеRED. Proposed patch bytes отдельно hash-bound; D3 не применяет его. Любое изменение registrations/semantics требует нового решения, не grandfathering.

I2 output: reviewable source diff, native closure record derived from final commit, task/workflow order, exact parser/transport limits, typed unknown/retention, bound source CPP и remaining GREEN plan. Текущий2bb dirty overlay/partial native availability не READY для CI. Native source implementation может быть полностью reviewable при отсутствии свежего исполнения: гипервизор partial read-only, CI key unconfirmed и control/compute NoRoute остаются **runtime evidence gaps**, тогда как отсутствующие readers/backend/closure/wiring — **source gaps** и не списываются на сервер.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| OPS04 даёт пригодный lifecycle, не готовый docs executor | selected platform f729 bootstrap_build.py owner/supervisor/run | cwd/env/raw/RAM/TMP API отсутствуют | изменить |
| Exact12 pure contract можно сохранить | separate committed native closure same Root HEAD; current helper SOURCES | Current overlay не final clean source | сохранить |
| Caller JSON не устанавливает native trust | owning admission docs + active inherited control/opaque context | CI producer/tool observations ещё отсутствуют | данных недостаточно |
| I2 имеет конкретный исполнимый путь | native launcher+stdio driver+exact sourceGraph+supervisor/storage API | Source implementation/CPP ещё не выполнены | изменить |
| Fresh native/full CI доказаны | Новых native receipts нет; existing local sampled harness не production backend | Отдельные binding/runtime gates | дополнительно измерить |

STOP. Нет source patches, CP edits, новой execution authority, product calls или final CI dispatch. Перед I2 нужен независимый high D3 review.
