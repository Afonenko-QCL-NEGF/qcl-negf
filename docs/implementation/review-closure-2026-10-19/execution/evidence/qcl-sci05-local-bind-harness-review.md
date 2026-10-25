# SCI05 — coordinator source BIND и local C08 harness review

2026-10-19. **PASS в узкой области source BIND + bounded normal-stop tooling для harness v3.** Продуктовые шесть файлов byte-identical принятому CPP2. Конкретный output-threshold defect v1 устранён в v2; nominal cleanup reserve исправлен в v3. Вердикт относится к `/tmp/qcl-julia-c08-run-v3.py` SHA256 `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112`, не к v1/v2. Hard realtime deadline, hard RSS/TMP/output quota или доказанный transient peak этим review не установлены.

До первого вызова координатор обновляет fresh admission/BIND на v3 и ждёт завершения обоих SI07 T05 checks. Старый admission с120s/2GiB — исторический, не latest READY. Этот отчёт не выполняет вызов и не заменяет его runtime receipt. C08 consumed=0 по предоставленным исходным receipts; этим review C08 calls=0, Julia/import/test/build/network/solver/native calls=0. Только read-only source/diff/hash/Git checks; ни один harness/helper не импортировался и не исполнялся. Единственный новый файл — этот отчёт; budget≤15 min /1 CPU/1 GiB/output≤64 KiB. Дополнительные агенты не создавались.

## Source identity и prepared environment

Фактический owning Core `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`: HEAD `90f1048d290d6ec9518754e288333c694fe874de`, status пуст, recursive submodule status пуст, `git diff --check` успешен. Parent ровно `239d76bb59c955b32888eeaec518d6e465b4178d`. `git diff --name-status 239d76b...90f1048` содержит ровно шесть разрешённых путей, включая новый узкий test. Original frozen source ref из binding — `1b8fda18881007f7c0c7f68758c7dbf42b44dfc6`; source equality установлена фактическими SHA файлов, а не только сообщением о cherry-pick.

| Фактически прочитанный Core file | SHA256, равный CPP2 |
| --- | --- |
| `src/QCLNEGF.jl` | `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| `test/numerics/final_audit_evidence.jl` | `6a2e954230c119a92e11e70c5bc8d31376fc06e209faa907429b9f6ee13455b5` |

DEV05 `test/numerics/final_state_alignment_oracle.jl` имеет прежний SHA `81fbb258f86c1760ed2ffb7964e189518fd1ec7608921e42080c969c4a55f852`; diff этого файла между parent/integrated source пуст. Изменений public exports/types/API сверх принятого CPP2 нет.

Root фактически продвинулся concurrently до `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`. Status: modified Core gitlink, execution checkpoint и `docs/single-server-deployment.md`; untracked execution evidence/journals/source-binding публикации DEV22/DOC02/SCI05. Фактические submodules: Core `+90f1048d...`; Runner `23860d9e660a3cddf6cb5203d449d1b62f3745a1`; AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`; Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; Portal `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; Research `1eacefcd81a50e245ea9da74a0b717b33818c61e`; Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Unrelated root overlay не входит в этот tooling verdict. Root/gitlink publication readiness не выводится из чистоты owning Core.

Prepared project `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.build/local-julia-int01/import-phase-1/environment/julia`:

- `Project.toml` SHA `859c6e7b2aedf4b58cd48731ea9a3970d70a43e018796472ec99550d186fdafe`, `Manifest.toml` SHA `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47`; оба фактически byte-equal выбранным root `julia/{Project,Manifest}.toml`, readonly mode0444.
- Manifest QCLNEGF path=`../components/QCLNEGF.jl`; sibling `environment/components` — symlink на actual root/components. `readlink -f` разрешает Core именно в HEAD90f1048 checkout выше. Аналогичный Runner path относится к actual selected Runner, без второй копии исходников.
- Runtime executable `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/.build/julia/bin/julia` существует с executable mode, SHA `02618fb870c4b0f35976837605b39026b55ed998fc51dfe1edb95ae928c85d4f`. Версия1.13.0 здесь взята из source-bound prepared receipt, бинарник не запускался для новой проверки.
- Existing depot `.build/local-julia-int01/depot-1` содержит packages/artifacts/compiled/registries. Их наличие не доказывает успешный import всех fixtures; missing dependency при C08 — stop без install/setup. Ни instantiate, ни package operation не выполнялись.

Binding artifact `/tmp/qcl-sci05-main-source-binding.json` SHA `b6324270c5f9ce0159dfdde9a8eaac9e4f1a65b9d6078e22648aca8ab764ddae`; historical local admission `/tmp/qcl-sci05-local-admission-bind.json` SHA `0e275b9cd15a4be6e926bd62106fb4aa00c473eb8cc7790b6016cee121b11d62`. Его observed memory/affinity/storage и old first_call_limits не заменяют обещанный fresh rebind перед запуском. Текущий review сам новых host admission measurements не делал.

## Harness chain, найденные и исправленные несоответствия

| Версия | Проверенный SHA256 | Disposition |
| --- | --- | --- |
| Previously reviewed `/tmp/qcl-julia-targeted-run-v5.py` | `a37e9dd52f6c49181f80a956e2de334ff08d6c52653f7c7baae28a08ee7c98f0` | База read-only comparison |
| C08 v1 | `0fd90162b4a5e5704080fdd3c55869438969ea75b8e5ba6c41bce868e646add3` | Исторический concrete defect сохранён |
| C08 v2 | `d638c22900ad6d9674110a10310c1174c1fa48b96275eb77bd7f767e2dca6be7` | Исправлен post-drain threshold, trigger590 ещё не даёт30s reserve |
| C08 v3 | `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112` | Принятая source/tooling версия этого review |
| RawCapture helper `/tmp/qcl-local-julia-guard-v2.py` | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` | Тот же hash-bound RawCapture, без запуска parent/child CLI |
| Owned TMP sampler `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` | Тот же read-only stat/no-follow sampler |

**F-output, устранён:** в v1 строка122 после capture drain всё ещё вычисляла `captured_bytes > 2*1024**2`, хотя stop threshold73 и receipt127 уже задавали8MiB. Лог3MiB при прочих successful условиях давал ложный output_overrun/exit1. V2 diff ровно одной строки меняет2→8MiB. V3 наследует исправление: early stop8MiB−128KiB, post-drain overrun>8MiB и recorded limit8MiB согласованы. Raw bytes не обрезаются ради pass.

**F-time/reserve, исправлено в области bounded normal stop:** v1/v2 wall trigger590 оставлял10s до10min, но code имеет sequential waits3+5+5+optional5+final5, номинально до23s. Это делало заявленную grace≤10 неподтверждённой. V3 diff к v2 состоит ровно из CPU rlimit570/575, wall trigger570 и recorded wall570. Теперь nominal explicit-timeout path≤570+23=593s **плюс** sampling/read/write/scheduling overhead, с30s reserve до campaign10min. Это консервативный normal-stop budget, не доказанный hard deadline600s. Первоначальное описание590+≤10s больше не относится к принятому harness.

Ни resource predicate correction, ни output correction не меняют продуктовый test/evaluator, accepted bounds, acceptance thresholds или scope SCI05. Original v1/v2 не переписывались; проверяющий их не исправлял.

## Фактические v3 predicates и пределы

`science.md:273–275` задаёт общий SCI05/08 cap8 processes≤10min/2CPU/4GiB/log8MiB в prepared source-bound runtime, missing deps=stop без install/build. V3 использует более узкий single child affinity1, Julia threads1/BLAS1 и trigger570s. Monitor/capture принадлежат отдельному Python process; affinity1 относится к Julia child, не утверждение о жёсткой общей CPU quota всех процессов.

V3 source:

- Строки26–33 выбирают existing runtime/project/depot, `--startup-file=no --threads=1 --check-bounds=yes`, `foreach(include, ARGS)`, offline Pkg/no auto-precompile, generic CPU, BLAS/MKL/OMP threads1 и owned TMPDIR. Setup/build/solver command не добавлен. Target first call координатора — только `components/QCLNEGF.jl/test/numerics/final_audit_evidence.jl`; harness технически принимает список trusted component fixtures, поэтому exact argv должен войти в fresh BIND/receipt.
- Строки34–37 создают собственный process group, child CPU affinity1 и per-process RLIMIT_CPU soft570/hard575. Это не общая process-tree CPU quota; descendants наследуют affinity, но индивидуальные CPU limits не превращаются в aggregate accounting.
- Строки66–82 sampled process-tree RSS>4GiB, owned logical TMP bytes>16MiB, wall>570s, raw output>8MiB−128KiB либо capture error вызывают stop own group. SIGTERM/short wait/SIGKILL сохраняют original raw output. Никаких чужих job/VM operations.
- Строки87–131 выполняют drain/fallback, сохраняют raw-capture/guard failures, bytes/stop_reason/limits/fixture/harness hashes. Exit0 требует process exit0, отсутствия stop_reason/capture/guard/output errors и complete raw capture. Exit0 всё равно не scientific acceptance.

Ограничения сохранены явно:

1. RSS и TEMP **sampled**, примерно50ms между завершениями циклов; scan overhead добавляется. Нет hard cgroup memory cap, disk quota, доказательства transient peak или покрытия explicit paths вне TMPDIR. TEMP считается по logical st_size regular files, symlinks excluded; это не physical disk allocation.
2. Raw output threshold тоже sampled и drain может превысить8MiB; это честный failure с сохранением original bytes, а не hard byte quota. Log readback/receipt overhead не включён в доказанную hard-time bound.
3. RawCapture thread non-daemon. `finish(5)` не уничтожает зависший reader; при удерживаемом pipe или блокировке I/O завершение Python может задержаться сверх nominal593s. V3 не обещает hard realtime600s или bounded arbitrary-kernel/I/O-failure cleanup. При incomplete capture/unknown process outcome нужен координаторский stop/reconciliation, не автоматический повтор.
4. Source/runtime/admission может измениться после этого чтения: fresh rebind проверяет hashes/HEAD/paths, актуальные ресурсы и общий remaining SCI05/08 cap перед единственным first invocation. Текущая historical admission запись120s/2GiB не годится как fresh v3 limit claim.

Эти ограничения не скрыты и соответствуют уточнённому поручению о normal-stop eligibility; переносить этот PASS на строгую hard-quota/deadline гарантию нельзя. Новых blockers именно для read-only source/tooling eligibility v3 после двух конкретных corrections не найдено.

## Решение и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Integrated Core воспроизводит принятый CPP2 | Actual six-file SHA equality, HEAD90f1048 parent239d76b, clean owning status | Root/gitlink publication имеет отдельный dirty overlay | сохранить |
| DEV05 не изменён | Old SHA81fbb258..., empty parent/integrated diff этого test | Runtime DEV05 не повторялся | сохранить |
| Prepared project выбирает actual owning source | Copy-equal root locks, Manifest relative path + actual components symlink, runtime SHA | Наличие prepared depot не доказывает import success | сохранить |
| C08 v3 tooling source eligible с bounded normal-stop reserve | Hashd454f205..., output predicates8MiB согласованы, trigger570/CPU570–575, nominal≤593s+overhead | Sampling/non-daemon/I/O не дают hard600s/quota guarantee | сохранить |
| First invocation уже READY/выполнен | C08 calls0, old admission имеет исторические limits | Нужны promised fresh v3 BIND/admission и завершение T05 pair | дополнительно измерить |
| Runtime/scientific acceptance установлена | Такого evidence нет | Этот review не запускал Julia/tests/solver | данных недостаточно |

STOP. Единственный output — этот review. Дальнейшее исполнение остаётся у координатора в уже принятом общем finite grant.
