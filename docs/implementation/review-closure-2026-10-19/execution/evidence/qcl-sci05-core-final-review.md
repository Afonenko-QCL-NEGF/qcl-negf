# SCI05-C1 Core — final independent CP-CODE evidence review

2026-10-19. **PASS scoped software CP-CODE для exact Core HEAD `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c` относительно base `239d76bb59c955b32888eeaec518d6e465b4178d`.** Ранее принятые CPP2/E1 source contracts связаны с clean committed source и двумя успешными bounded runtime receipts:287/287 новых checks и5+925 compatibility checks. Новых блокирующих замечаний в заявленном Core scope нет.

Вердикт может использоваться координатором для G1 software gate PR12 на **этом exact source**. Remote PR head/base/состояние merge здесь не проверялись и не изменялись. Это не Runner persistence/native integration acceptance, не final CI/release и не S1 scientific acceptance. Attribute profile A имеет отдельный design verdict и не является частью Core acceptance.

Review≤15 min /1 CPU/2 GiB/read≤2 MiB/output≤32 KiB. Сначала целиком прочитаны primary raw/receipts call5/call6, затем actual source/hash binding, intent и coordinator journal. Единственный новый файл — этот отчёт. Новых imports/tests/solver/build/network/Git mutations/source edits/children нет; additional C08 calls=0. Применена ранее прочитанная source/result evidence граница `qcl-physics-audit`.

## Exact source и reviewed lineage

Actual owning checkout `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`: HEAD7324d98...; branch `codex/review-closure-final-audit-integration`; status пуст; recursive submodule status пуст; `git diff --check` успешен. Diff base239d76b→HEAD содержит ровно пять production source paths и один новый narrow test; existing compatibility/DEV05 tests не входят в diff.

Commit chain прочитан локально:90f1048 (`Retain bounded raw final-audit evidence and independent algebra oracles`) →e86ac74 (`Disambiguate broadcast syntax in final-audit oracle`) →7324d98 (`Honor realness rejection and exact neutral algebra in audit controls`). `git diff e86ac74 HEAD -- src` пуст: E1 не менял production. Никакие submodule versions не обновлялись этим review.

| Current file | Фактический SHA256 |
| --- | --- |
| `src/QCLNEGF.jl` | `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| `test/numerics/final_audit_evidence.jl` | `ede25dde26d72c313fb15e8bfcc515e8d29673b41336535c760a6eb0113309e9` |
| Unchanged `test/numerics/fresh_candidate_residual.jl` | `8ab459b5be0c39f96839b862aad38e1dbcd6a8dc633770838fd239c8a871a6a0` |
| Unchanged DEV05 `test/numerics/final_state_alignment_oracle.jl` | `81fbb258f86c1760ed2ffb7964e189518fd1ec7608921e42080c969c4a55f852` |

Frozen `/tmp/qcl-sci05-main-source-binding-v3.json` SHA `55cfadcf3e4c6e26a9872d7d36874f135e5caddabcc85e377679673b1f875c69` перечисляет те же шесть file hashes и integrated HEAD7324d98. Его state `C08_5_pending`/calls4 — исторический prelaunch snapshot, а не итоговый result. Actual raw/receipts ниже устанавливают последующие outcomes.

Принятые source reviews сохранены: CPP2 `/tmp/qcl-sci05-core-code-review-v3.md` SHA `e317a4a23a68d510f0e4a85b9da2fd3ecc43ea2eed4563a0fa7f433e172826fa`; E1 `/tmp/qcl-sci05-engineering-E1-review.md` SHA `5142b8450c548cb89d1df91f87b99020b8fde9aba09450f764cf799136cbe618`. Production hashes совпадают CPP2; final test совпадает E1. Поэтому source conclusions не перенесены на неизвестный новый code diff.

Root actual HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48` остаётся integration checkout с unrelated concurrent documentation/evidence и gitlink overlay. Actual submodules: Core `+7324d98...`; Runner `9378396a3681c1eddf2c62f16674834fc4465583`; AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`; Contracts `+12fc26462bbab3df76904c6deb01f8c6596de7be`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; Portal `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; Research `1eacefcd81a50e245ea9da74a0b717b33818c61e`; Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Clean Core не подменяет clean/final-ready root requirement.

## Primary runtime evidence

| Receipt / raw | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-SCI05-C08-CORE-5/receipt.json` | `faed9a3a869f52faae643452217dde768359a41990f5a534d187e38ecf41b431` |
| `/tmp/qcl-SCI05-C08-CORE-5/original.log` | `8ed3eebc7a0e4709747759e53a5c56a3b231acc87289234c510cccd6374f09e3` |
| `/tmp/qcl-SCI05-C08-COMPATIBILITY-6/receipt.json` | `3ffb22e07a2bbd4b94c5a73faf4247c72f115fdca3f7af1584a52d2bfeab3551` |
| `/tmp/qcl-SCI05-C08-COMPATIBILITY-6/original.log` | `a46c429ddd0f7fe9a7bf875c066fb9575c3f9856b138143c18e79f745e6bf4b6` |

**Call5:** exact fixture SHA ede25dde..., accepted harness v3 SHA `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112`, ordinary `foreach(include,ARGS)` без known-red outer wrapper. Семь raw summaries:

| New narrow test block | Pass/Total | Проверяемая граница |
| --- | --- | --- |
| Dyson witnesses/nonfinite inventory | 26/26 | Separate global/max/ratio aggregations, coordinates/ties/nonfinite witnesses |
| Near-zero additive-floor/measured-zero | 24/24 | Additive1e−14 и meaningful measured0, без max-floor замены |
| Frozen complex matrix/weighted number/candidate | 28/28 | Independent inverse2/complex scalar graph, weights/adjoint, λ masking/raw Σ; E1 realness rejection |
| Poisson literal/gauge enclosure | 21/21 | Residual/ζ/gauge bounds, exact neutral projected numerator, sign/h²/scale/density/norm mutants |
| Overflow finite ratio0 mapping | 89/89 | Same-pass finite0/error status, actual Inf tags, per-field mutants и healthy zero |
| Template/availability/charge | 76/76 | Required inventory, unavailable/null, signed/nonfinite charge/history/context |
| Public validation/raw rU/assessment transport | 23/23 | Actual provided U/n, raw-vs-mixed/changed-density distinction и failure outcome |

Итого287/287. До E1 diagnostic имел21pass+1error matrix и16pass+1fail Poisson; теперь именно эти блоки дают28/28 и21/21, остальные counts26/24/89/76/23 сохранены. Изменённые expectations не просто удалили failures: source E1 сохранил old controls и добавил meaningful typed-error/reference assertions, что подтверждено предыдущим independent source review.

Call5 receipt: exit0, wall25.912s, sampled peak RSS697806848 B, sampled owned TEMP0 B, raw1234 B; raw_capture_complete=true, raw_capture_error/guard_error/stop_reason=null, output_envelope_overrun=false. GREEN относится к этим executed assertions, а не выводится только из exit code.

**Call6:** raw5/5 `Independent resonant scalar oracle requires the fresh candidate Dyson gate` и925/925 `Final state U G alignment`. Receipt содержит exact hashes обеих unchanged fixtures из таблицы source и тот же accepted harness. Набор5 проверяет fresh-vs-stored narrow-pole Dyson и прежний strict candidate gate. DEV05 source содержит literal gate inventory, manufactured same-state U/G/density и fresh-map lineage, stale/predicted-U substitutions; это функциональная compatibility/regression проверка на той же production instrumentation, не повтор S1 experiment.

Call6 receipt: exit0, wall45.271s, sampled peak RSS984412160 B, sampled owned TEMP0 B, raw284 B; raw_capture_complete=true; raw_capture_error/guard_error/stop_reason=null; output_envelope_overrun=false. Таким образом,925 old assertions не были переписаны ради нового producer, а narrow old primitive также сохранил результат.

## Runtime/source binding и guard scope

Оба receipts выбирают один и тот же absolute executable
`components/QCLNEGFRunner.jl/.build/julia/bin/julia`, `--startup-file=no --threads=1 --check-bounds=yes`, prepared project `.build/local-julia-int01/import-phase-1/environment/julia`, root cwd и exact relative fixture paths. Harness source d454... ранее independently reviewed и не изменился; он задаёт existing offline depot, generic CPU, no auto-setup, BLAS/MKL/OMP threads1 и child affinity1.

При final readback executable SHA `02618fb870c4b0f35976837605b39026b55ed998fc51dfe1edb95ae928c85d4f`, prepared Project SHA `859c6e7b2aedf4b58cd48731ea9a3970d70a43e018796472ec99550d186fdafe`, Manifest SHA `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47` совпадают прежнему prepared binding. Prepared locks фактически byte-equal selected root `julia/{Project,Manifest}.toml`; Manifest relative Core path через `environment/components` symlink разрешается именно в current clean owning Core выше. Runtime label Julia1.13.0 согласуется с imported Core source exact-version guard. Это обычный trusted source-bound prepared-runtime evidence chain; сами C08 receipts не являются независимой byte-level attestation всех загруженных native libraries/compiled images.

Prelaunch intent5 SHA `58a55a1426c5217be8c402734130339d7ac04f2619d45031b6334db92223a3d4` фиксирует HEAD7324d98, fresh observation17:53:26.544677UTC, available RAM12421373952 B/TMP16155840512 B и call5/8. Intent6 SHA `63fe869820350a3090499194ab204293e5c72e9c3ab5c5fbbda1e8ee56252ab3` фиксирует тот же source, observation17:57:30.812938UTC, RAM12442402816 B/TMP16155627520 B и call6/8. Они предшествуют соответствующим receipt starts. Historical `/tmp/qcl-sci05-local-admission-bind.json` на old HEAD90f1048/120s/2GiB не использован как fresh final READY.

Guard limits в обоих receipts: wall trigger570s, per approved source child CPU570/575, affinity1, sampled tree RSS4GiB, owned logical TMP16MiB, raw8MiB. Actual completed runs существенно внутри этих bounds. Отсутствие stop/errors подтверждено primary receipts; proof fault-injection всех guard branches этим результатом не заявляется. Sampling≈50ms+scan overhead не даёт hard cgroup/quota/transient peak proof; explicit paths вне TMPDIR не покрыты этим sampler. Drain сохраняет raw и может превысить trigger; non-daemon/I/O caveats и отсутствие hard realtime600s остаются прежними. Ни CPU-wide campaign quota, ни native server admission из local receipt не выводятся.

## Original failures и конечная extension provenance сохранены

Эти GREEN receipts не стирают историю:

| Original attempt | Raw SHA256 | Receipt SHA256 | Outcome |
| --- | --- | --- | --- |
| C08-CORE-1 | `7bf8efd9db1986388edb93f2918266e105d03bf34566574283bf455b4fb671bf` | `72a3d601d394a8be429022f63226eb5102785411e476f4cd9ce7bd80ebe094aa` | ParseError, assertions не измерены |
| C08-CORE-2 | `55996891e3287948b43d922f6ee683000df531e9c367d29af0cae98295d17693` | `9d5b4129c634bd6e4f1407516401ba7e4259f92eee8ad3f83788b8b8566ea7cd` | Known DomainError162 |
| C08-DIAGNOSTIC-3 | `3ea0c064402917a29df4abae74447c4d17078865469fd62ef7d6cbfd3efc0ece` | `15c50c17b266692734fc58afcb806c0613a0cd7fe67734734f1f3c543328fd93` | All7 blocks,275pass/1fail/1error |

Фактические hashes этих original файлов повторно совпали ранее принятым evidence. Diagnostic выявил два independent-test defects; E1 repair был разрешён **отдельным конечным engineering extension**, а не скрытым новым циклом внутри исчерпанных2/2. Checkpoint `/tmp/qcl-checkpoint-SCI05-engineering-E1.json` SHA `706dff1aaf6c9332da00ad434c314a0cb4591d3ac8ded2460d8ba3f2c5f3eaee` сохраняет original2 consumed2 +additional1/effective3 и stop после E1. Base model/S1 caps/γ/strict limits не изменены. Calls5 и6 соответствуют двум указанным в extension targeted recheck/compatibility slots.

В общей последовательности SCI05/08 через call6 consumed6/8, включая separate Contracts call4. Этот review не выделяет remaining2 для новых Core corrections и не запускает ещё один test. Further Core corrective loops E1 не разрешает; новое semantic issue — concrete blocker/отдельное решение координатора.

Coordinator publication journal `/tmp/qcl-sci05-core-publication-journal.json` SHA при чтении `099f46e981c31ac5830df6ae1e91b88eed1a8e8d3d8625ba8f995925f8bef898` имеет local head/base/file binding и progress push intent для PR12. Это secondary publication context, не primary runtime evidence и не доказательство фактического remote push/merge. Никаких GitHub/network действий проверяющий не делал.

## Что закрыто и что остаётся отдельно

Закрыт software CP-CODE scope SCI05-C1: append-only same-pass raw evidence instrumentation, прежние ratios/API/strict arithmetic, owning single Poisson solve, actual producer context, explicit availability/error/zero handling и подготовленные independent literal/mutation controls с now measured targeted runtime + preserved compatibility.

Остаются открытыми/отдельными:

- Core record — **internal template без portable state_identity**. Отсутствие придуманных IDs намеренно; Runner должен добавить шесть actual identity fields, transport обеих копий, затем Contracts/Results independently validate exact identity/equality/encoding/budgets. Core287pass не закрывает Runner/Results/native persistence.
- Shared production map kernels остаются общим physics risk; tiny literal residual/Poisson/number oracles и DEV05 функциональная assembly не являются independent device-physics oracle.
- Tests manufactured/tiny, не full S1: нет нового scientific run/SCBA convergence equilibrium0mV/70K/all5/e–e none result, discretization error budget, resource feasibility длительного запуска или experimental validation. Нет inference «все physical gates прибора пройдены» из fixture passes.
- Native deployment/services/worker/trust/staging/restore, server resource admission, integrated release source composition и final ready source реального release требуют своих gates. Это local prepared environment evidence.
- Full suites/build/CI этим packet не выполнялись; finalCI submissions=0 в порученном контексте, никаких новых submissions этим review. CI-once policy не расходуется targeted calls5/6 и не считается закрытой.
- G1 remote PR12 exact head/base/checks/eligibility и любое merge действие остаются у координатора; PASS этого отчёта ограничен local exact7324d98 software evidence.

## Итог и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact Core готов к scoped software CP-CODE/G1 | Clean7324d98, CPP2/E1 SHA chain,287/287 +5/5 +925/925 primary raw | Только указанный source/scope, не remote publication proof | сохранить |
| Compatibility/DEV05 сохранены | Unchanged fixture SHA и call6 primary summaries | Tiny functional oracle, не full-device scientific validation | сохранить |
| Guard/raw/source runtime evidence достаточно для этих bounded checks | Complete raw, no guard/capture/stop errors, prepared command/path/hash/intent chain | Sampled resources/native libraries не hard attestation | сохранить |
| Failures и original cap+E1 extension сохранены | Original1/2/3 hashes, checkpoint706dff..., effective3 | Further Core corrective loop запрещён E1 | сохранить |
| Portable persistence/native/release/science acceptance закрыта | Core намеренно не связывает portable identity; таких receipts нет | Owning Runner/Results/native/science/finalCI gates отдельны | данных недостаточно |

STOP. Никакой новой реализации, проверки или публикации этим review не выполнялось.
