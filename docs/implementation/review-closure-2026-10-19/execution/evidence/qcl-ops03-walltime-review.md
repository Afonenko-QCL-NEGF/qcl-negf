# OPS03 GREEN3 — bounded source/cost diagnosis

**Вердикт: поддерживается ONE replacement full same-suite packet с wall180s / affinity1 CPU, при отдельном exact root checkpoint.** Source fix не предлагается. GREEN3 — interrupted/incomplete test outcome, CP-CODE остаётся открыт. Evidence поддерживает finite cumulative suite cost, а не observed hang в последнем control; завершение нового пакета заранее не доказано.

Применён qcl-performance-audit: прочитаны SKILL.md и relevant telemetry guidance. Scope — local synthetic engineering fixtures, не solver/benchmark/production performance; scientific equivalence здесь не устанавливается и physics не меняется. Reviewer не выполнял tests/imports/helper/Git/native/product edits.

## Identity и actual outcome

Production SHA1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0; tests application SHA f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21, unchanged. Selected worker tests hashes совпадают с prior packet.

GREEN3 receipt SHA a9180a1dbe71c129e936dc71f46337abf28e182a0f500489302243442c358bab (2514 B); original.log SHA74b1b131de868e32b49d91a020e20cf85f5c10ec4576fb4a22e3267ba6220a70 (205 B). Receipt declares harness16e908e64bfc6fd9a4467897b9eade95cd8a353535610c52144c2ca912e41b75, sampler16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e, 1207 samples/no guard or raw error. Wall90.044s, exit−15, stop wall_time_limit, RSS87875584 B sampled, TMP74388 B sampled, raw complete/no overrun. Sampler failure прежнего GREEN2 не повторился. Raw не содержит test summary или failures, только 72+72+45=189 dots; оставшиеся outcomes unknown.

## Последний control и свежесть progress

AST-only reconstruction, без pytest collection/import: classes в порядке source, unittest methods alphabetically, inherited methods включены. Predicted selected total234 соответствует уже измеренному GREEN1 denominator234. Prefix:

| Class | Method indices |
| --- | --- |
| ApplicationReleaseTests | 1–51 |
| I14UpdateTests | 52–76 |
| EffectiveRuntimeMaskTests | 77–88 |
| I14WholeRepairTests | 89–123 |
| I14SlurmInfinityTests | 124–162 |
| OPS03LifecycleOwnerTests | 163–189 |
| OPS03WholeRoutingTests | 190–192 |
| OPS03LocalIdentityTests | 193–202 |
| OPS03StoppedIdentityTests | 203 |
| WorkerLifecycleTests | 204–213 |
| ShutdownIntentTests | 214–234 |

189 dots означают completed pass-reports данного prefix при этом collector order. Это reconstruction, не сохранённый verbose nodeid stream; независимая retained metadata согласуется с ним: единственный retained active fixture принадлежит whole_update с local journal pending и whole_cluster_update `phase=fleet_health,node=controller,status=running,open=false`, pending_command absent; последние completed command phase records — controller fleet-health systemctl/timeout/systemctl/findmnt. Следующий #190 — `OPS03WholeRoutingTests.test_o03_whole_update_calls_real_local_helper_without_self_ssh_or_reacquire` (:3668). Его реальные source settings/parent-owned helper и local health точно соответствуют этим artifacts.

Retained fixture directory `/tmp/qcl-OPS03-GREEN-3/tmp/tmpyt3pk61b` имеет filesystem **birth** 2026-10-19 15:47:47.908161835 UTC, mtime15:47:48.138751971. Release record mtime15:47:48.163380; final retained whole receipt mtime15:47:48.290542; packet recorded15:47:48.299197. Packet started15:46:18.256297. Поэтому latest fixture появился примерно через89.652s от начала и лишь за0.348s до nominal90s cap; свежий receipt опубликован непосредственно у stop. Mtime само по себе не является start/duration, поэтому дополнительно проверен birth. Не наблюдается control, который сам зависал90s; exact syscall at SIGTERM неизвестен.

## Retained JSON inspection bound

Найдено6 tiny JSON, суммарный logical size25189 B; первичное чтение плюс повторное selected receipt reading для last command phase metadata всего48217 B (<128KiB). Выведены только selected lifecycle/phase/node/pending/status metadata и SHA, **ни snapshots/base64/config contents не выводились**. Config JSON не использовался для private parameter disclosure. Arrays/archive extraction/remote не читались.

Selected evidence:

- whole receipt23028 B SHA720092f866ec9b5ee48eed2ad76610047fcc48c7456b8b74f39b3846bf0a9ea2;
- local lifecycle intent564 B SHA35f1f6e1db8fd15099c46b79bfb3d0e5522eab205bfd20c6f0a3227d8d09d8f3;
- local phase receipt588 B SHA3c3dd561c2ba5a39271a157c2c68dfec665f339538d54d85f8817973234504fe.

Original pending artifacts сохранены; никакой cleanup/reconciliation по времени не выполнялся.

## Cost support и предел вывода

Факты source:

- I14 post-RESUME production loop :2860–2871 ограничен10 iterations, sleep≤1s. `test_f4_postresume_changed_or_down_never_opens` (:2370) явно задаёт10 NOT_RESPONDING returns для одного negative subcase; `test_f4_postresume_wait_and_exact_idle` (:2354) требует2 промежуточных returns. Оба inherited дважды (I14WholeRepair + I14SlurmInfinity), около24s intentional polling ожидания при достижении этих ветвей, сверх durable receipt/command work. Эта часть уже лежит до #163; она стала достижима после representation repair, поэтому GREEN1 failed53s не прогноз успешной suite.
- Prefix содержит много real filesystem publishers/fsync, PID/inode checks, bound scans и повторных full whole-flow fixtures, плюс O08 десять real fork/SIGKILL cuts и O09 fault matrices. Фиктивны только command/system services, не durable file work.
- Native command cleanup fixtures имеют finite .8s/1s timeout, .2s reserve; O/fork handshakes poll/join5s, startup/shutdown3–5s и cleanup watchdogs. Remaining #190–234 controls используют bounded fakes/handshakes, fixed cases; не обнаружен новый unbounded polling loop. O03 fake Commands не запускает real Nix/SSH/solver/Slurm, а completed findmnt — fake response. Real filesystem syscalls всё же не имеют математического wall bound.

Оценка planning, не измерение: простая189/234 extrapolation90s даёт примерно111s, но стоимость методов неоднородна; тяжёлые inherited polling/fault prefixes уже пройдены, оставшиеся45 methods имеют finite fixture scope. **Ожидаемый порядок полного пакета ~110–140s**, с неизвестным разбросом CPU/filesystem/sampler overhead; 180s — конечный stop envelope с запасом, не обещание completion. CPU time/IO/per-test durations в GREEN3 отсутствуют; не объявляется измеренный bottleneck, speedup или гарантированный upper bound. RSS/TMP observably далеко ниже caps, это sampled facts, не hard peak proof.

## Один различающий replacement packet

Предлагается root-owned **ONE call7**, historical six calls сохраняются, по переданному latest engineering grant и separately recorded technical extension; без нового author/product round:

- Те же exact frozen production/tests и все три selected files в одном процессе; **не subsets вместо failed suite, не skip/xfail/loosening assertions**.
- Wall180s, affinity1 CPU, CPU RLIMIT soft180/hard185 (если сохраняется current harness CPU guard), sampled process-tree RSS1GiB, owned TMP16MiB, raw nominal2MiB/unchanged early threshold+full drain, exact same accepted race-safe sampler. No setup/install/network/native/science/fullCI.
- `pytest -vv --durations=0 -p no:cacheprovider` с новым exclusive basetemp/attempt identity. Full raw даёт started nodeid, completed outcome и terminal durations; receipt связывает exact command/harness/sampler/fixture hashes. Existing tests сами не редактируются ради телеметрии. 234 name/outcome+duration rows ожидаемо малы относительно2MiB, но raw cap остаётся enforceable и overrun failure честным.
- Stop на180s/RSS/TMP/output/guard/identity drift; preserve original raw/receipts/TMP. Любой interrupted outcome снова incomplete, не pass. При повторном stop — STOP и отдельный exact last-node/source diagnosis, без автоматического rerun/ещё большего cap. При failures — конкретный traceback/source ticket, не цикл до green.
- Raw complete summary всех234 selected methods и exit0/no guard остановки нужны для local runtime gate. Только это вместе с independent source review может закрыть CP-CODE; native/provisioning/prepare role gap/CR04 admission residual остаются отдельными gates.

| Утверждение / фаза | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Sampler GREEN2 defect вызвал GREEN3 stop | 1207 samples/no guard error, explicit wall stop | Нет attribution всех costs sampler | сохранить fixed sampler |
| Последний O03 завис90s | #190 reconstruction + fresh fixture birth/receipt у cutoff | Exact active syscall неизвестен | данных недостаточно для hang claim |
| Cumulative finite fixture work объясняет исчерпание90s | 189 reports, inherited bounded polling и durable/fork work | Нет per-test timings | дополнительно измерить ONE180s verbose packet |
| Product требует нового fix | Новый source defect не установлен | Последние45 outcomes unknown | сохранить source |
| CP-CODE/native/science готовы | Полного test summary нет | Separate gates сохраняются | данных недостаточно |

Никакого reviewer execution/import/collection/native/Git/product/harness mutation. Только bounded text/metadata/AST/hash inspection и этот /tmp report. STOP после предложения, packet запускает только coordinator с exact bound receipt.
