# SCI08-R1 I1 — actual caller traces (source only)

Candidate Runner fefaa27f194bfddf85dd51a0e255beef2218c06d + source hashes in identity.
Это inspected source path, не runtime result. Frozen fixtures349 nominal/31 groups.

## O1 — scientific entry действительно использует fixture seam

`src/composition/scientific_execution.jl:436–449` вводит keywords policy/envelope
и вызывает root `_scientific_resource_preflight(resource_policy,envelope)` первой
инструкцией тела. Символ импортирован `scientific_workflow.jl:29` из родительского
QCLNEGFRunner. Это тот же root symbol, который вызывает frozen strict fixture O1.
`native_phase_telemetry.jl:237–245` проверяет policy и envelope; campaign-strict
с missing envelope отказывает needs_admission, с envelope — needs_guard/needs_admission
без флага bypass. Return возможен только standalone. Поэтому strict refusal
предшествует plan decode:452, root mkdir:459, plan-path/write:463ff, execution
mkdir:667, strategy:672 и problem construction после:686. Под typed entry нельзя
передать произвольный fake plan: fixture проверяет actual shared seam, actual
ordering дополнительно установлено этим caller trace. Scientific solve не запускался.

Captured envelope: entry:447 → preflight:449 → `resolve_execution_strategy(config;
envelope)`:672 → `auto_strategy.jl:512` forwarding envelope в select_execution_plan;
reservation:679 → function:175–184. Actual chain нигде не читает default второй раз.
Двухаргументный private reservation сохраняет прежних standalone callers через
optional default argument:176; actual entry всегда передаёт третий аргумент.
Policy entry:446 → phase callback:969 → native constructor:143–151 → permit:156–159.
Strict entry сейчас закрыт, поэтому эта propagation — source binding для дальнейшей
интеграции, не свидетельство допустимого S1 launch. Hardware strategy до closed gate
недостижима; её legacy default probe не объявлен strict campaign admission.

## O2 — checkpoint writer действительно использует fixture seam

`commit_point_artifacts` в `point_artifacts.jl:816–818` validates budget/reserve;
root mkdir:823 остаётся отдельным допустимым эффектом. Actual call:825 вызывает
`_checkpoint_storage_preflight(solution,reserve_bytes)`:554–557, тот же root symbol,
который frozen O2 вызывает с tiny structural solution. Он валидирует reserve,
получает forecast через adapter:547–552 → scalar core:532–545 и checked-add reserve.
На malformed dimensions/unknown/overflow нет возврата к budget/free checks:826–827.
Generation enumeration:828, identity:835, staging mkdir:846 и первый checkpoint
writer:852 расположены после preflight. Ни malformed-dimension fake solution, ни
huge dimensions не передаются typed real commit; source seam trace подтверждает
ordering, positive O4 возвращает tiny literal и tested continuation только при GREEN.
Не заявляется no-filesystem-effect: root mkdir:823 предшествует forecast. Не заявляется
all-HDF5-write enforcement: slab/growth/retention относятся R2/R3/P2.

Storage adapters: budget:568–572 validates budget/reserve/additional до storage_reader;
scalar core:559–566 validates used и делает checked used+reserve+additional. Free:581–583
validates required до available_reader; core:574–578 validates available до comparison.
Diskstat reader:580 сохраняет raw available до validated Int conversion. File scan:523
validates каждый filesize перед checked accumulation. No fabricated0/unlimited.

## O3/O4 — actual phase callback, strict unknown refusal

`native_phase_telemetry.jl:149–152`: checked positive width → actual memory permit →
fixed-pool min → continuation у caller. Strict path resolves explicit membership через
`linux_resources.jl::_strict_cgroup_ancestors`, без legacy root fallback. Memory permit
требует directory:160, known nonnegative burst:164–170, valid max для каждого ancestor
и хотя бы один finite hard bound через `_strict_memory_bounds`:171, finite current
для каждого applicable bound:180–183 и checked current+burst для каждого bound:186–188.
Unknown бросает ArgumentError до GC:197 и pressure writer:230. Overflow бросает
OverflowError до GC. Known insufficient использует прежний GC/resample и checked
required:201 для pressure evidence:224; permit только required<=limit. Exact fit и
burst0 при известных current допустимы. Clean cache credit остаётся0.

## Five includes — fake-only resource and boot read source proof

- checked_storage_forecast: scalar cores; budget/free tests явно inject tiny readers.
  Actual `_storage_available`/diskstat не вызывается выбранными fixture calls.
- strict_campaign_resource_admission: `fixture` строит proc/self/cgroup literal
  `0::/fixture.slice/solver.scope`, cgroup root/slice/leaf и finite literals. `phase`
  и `probe` передают **оба** явных roots. Конструктор читает только
  fake_proc/self/cgroup; ancestor chain=[fake_cgroup/fixture.slice/solver.scope,
  fake_cgroup/fixture.slice,fake_cgroup]. Strict probe получает explicit physical/
  available/host/thread/vendor inputs; strict path не вызывает Sys memory fallback
  или BLAS.vendor. Memory/CPU reads строятся только из этих fake roots.
- execution_resource_contract: width fixture:133–169 explicit fake_proc/fake_cgroup;
  constructor → legacy `_process_cgroup_path(fake_proc)` → `_resource_read` fake
  self/cgroup. Chain тот же leaf/slice/root. Directory=nothing return в permit
  исключает memory reads; attempted/completed counters относятся actual callback.
- linux_process_resource_probe: все probe/callback calls в frozen file имеют
  explicit temporary proc/cgroup roots; physical override и vendor literal исключают
  host total-memory/vendor reads. Первые два probes получают MemAvailable из fake
  proc/meminfo (8388608/6291456kB, оба ненулевые), поэтому Sys.free_memory fallback
  недостижим; третий probe передаёт available_memory_override=6GiB. Legacy malformed/max controls
  сохраняются, strict sibling refuses unknown. No production default call invoked.
- native_phase_resource_contract:16 `fake_proc=dirname(proc)`; callback:23 передаёт
  fake_proc и root cgroup. Membership0::/group → [root/group,root]. Event sink:28
  вызывает actual recorder с proc_root=fake_proc → recorder:45 передаёт в journal
  → journal:21 lazy `get!(...,directory)` → boot read:24
  `joinpath(fake_proc,"sys","kernel","random","boot_id")`. Initial literal A
  создаётся fixture:17–21; direct cache-hit:68 тоже получает fake_proc. A→B не меняет
  String directory key, session/clock и не повторяет read. `finally` очищает только
  owned root. Production callers без keyword сохраняют /proc default и
  strip/read/catch→boot_unknown, sequence0/session/anchors/row schema.

Это source coverage fixed five includes, не syscall capture или executed assertion.
General default production paths по-прежнему читают настоящие OS inputs; они не
исполнялись. Unbounded native/proc access не разрешается этими helper controls.
