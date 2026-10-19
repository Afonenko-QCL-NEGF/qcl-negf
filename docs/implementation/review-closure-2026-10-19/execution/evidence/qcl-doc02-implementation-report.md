# DOC02 — narrow exact-text implementation freeze

**DONE: frozen для независимого CP-CODE.** Exact approved seven-file text применён; no new design. Два owning component worktrees и один root runbook path. Git stage/commit/push/PR не выполнялись.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d` не менялся. Selected root Core gitlink остаётся f5b73369…; для новой Core ветки использован прямо порученный опубликованный/merged `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`. Новый root composition не объявлен. Runner base — selected `23860d9e660a3cddf6cb5203d449d1b62f3745a1`.

Frozen proposal `/tmp/qcl-doc02-candidate/full.patch` SHA-256 `cc0bc5f923da2bda21b5680e7fba03529504aba81c611ef2308369b356e4af2e`, manifest SHA-256 `68b28c09af6ccd821559577375a43bd1a460e53e213869cb45dd71ff0577d942`; accepted independent design `/tmp/qcl-doc02-design-review.md` SHA-256 `bf9d86f545cab99e580f9fb6bd2d3524ea77aac7ad207236b0f41d7c1af81c9c`. Все D artifacts сохранены без записи. Manifest/identity — разовые evidence inventories, не поддерживаемый состав source.

Применены уже прочитанные architecture/root AGENTS/using-git-worktrees/verification skills и DOC02 handoff; прочитаны qcl-physics-audit, full approved patch и CP-DESIGN. Scientific derivation не перепроектировалась; missing raw production artifact не восполнялся.

## Изоляция и exact files

Native app worktree tool привязан к root repository; использован согласованный component Git fallback. С scoped escalation созданы `/tmp/qcl-doc02-worktrees/QCLNEGF.jl` и `/tmp/qcl-doc02-worktrees/QCLNEGFRunner.jl`, обе ветки `codex/review-closure-reader-routes`, от разных owning bases выше. Existing Core f7, Portal262, Runner checkout и SCI05 worktree не сбрасывались и не переключались.

| Path | Baseline SHA-256 | Applied candidate SHA-256 |
| --- | --- | --- |
| `components/QCLNEGF.jl/docs/src/theory/09_scba.md` | `bebcc84f6fa12a92429fea005083cb6729477f1beb089e21cf42df187f75449f` | `a1a3c438c14ff0d967a6890df3e7d3abf7ed7fb95e422ecb81ceef6c2350b004` |
| `components/QCLNEGF.jl/docs/src/theory/12_validation.md` | `f170915f4b3d9af9557dd4ab6cc63c14b01159fb659e29e1f1be814860746cb0` | `be55b03e7a228aebad88b24410d2633cd575ae63211a01ff4187f2c1bb95755b` |
| `components/QCLNEGF.jl/docs/src/developer/traceability.md` | `3b8e5a006f60c599ae2568fd67fbf98abe6579682b962be0ed86446448c3811f` | `5b860110779f106dc0ff1b97935c612f436987b1cb3e3b62a5a7b766885c0ca1` |
| `components/QCLNEGFRunner.jl/docs/src/user/configuration.md` | `f45dfd4d8f47b516d4b17a55ad8c62ffd4da89025fa465d8825a984091ddd042` | `5f1fb2243240a957a1d765af0b8dee4f44a7e105dcea35889c725843bacf4cbf` |
| `components/QCLNEGFRunner.jl/docs/src/user/results.md` | `65890eae23d10cd46cfa7fc596aba1828d6bebd6d635756a69a886847c3d2f2a` | `a1efe47c40fee8873239ef2c8f99b9058781dcdc19d4102fbcc078a38cfeff28` |
| `components/QCLNEGFRunner.jl/docs/src/api/public.md` | `70dce87e93adebcad66ab9696ba82571f53b44b7c0fc9968dce4ed91053c7d14` | `e59e1231197ed92823d691353ddc21dafe0b62252d586cf4018b2f331cda05dd` |
| `docs/single-server-deployment.md` | `6c13cf7c8a912b8d9ad03adc6333d30d78da9a75b64f1ab20e34c4061bbbdd20` | `8f659f7ee6dc3a5ff89acba052b1eadbcbeb2436fa6429d47d8dd400948da242` |

До записи все семь actual docs равны D baseline, а шесть component docs на requested worktree bases совпали побайтово с тем же baseline. 28 frozen source witnesses сверены с Git objects, Core/Runner witnesses дополнительно сверены с новыми bases. Root runbook запись допущена только после повторной baseline equality.

## Фактические статические проверки

Итого **226/226 static PASS** в `/tmp/qcl-doc02-implementation-identity.json`: preflight79 + exact after-copy7/хэши; whitespace/newline/fences; сохранение старых explicit anchors и @docs/@meta; отсутствие новых executable docs blocks; 33 added Documenter refs; 19 added links (14 selected Git-object occurrences и 5 relative targets); component HEAD/status/diff и исходные шесть docs unchanged; root skills/AGENTS guards unchanged; exact permitted component changed-path scope. UTF-8 прочитан без ошибки. Это текстовая проверка refs, не Documenter execution.

`git diff --check` в двух owning worktrees и по root runbook: каждый exit0, stdout/stderr пусты. Frozen baseline `git apply --whitespace=error --check full.patch`: exit0, stdout/stderr пусты. Fresh `git diff --no-index --check baseline candidate`: **exit1**, stdout/stderr пусты. Raw command receipts находятся в identity и `/tmp/qcl-doc02-noindex-raw.json`.

**E1 сохранён и исправлен в новой evidence записи:** frozen author report сообщал no-index exit0, который независимый reviewer и этот implementation не воспроизводят. Здесь записан реальный exit1 без diagnostics; исходный report не переписывался. Наличие diff не выдаётся за whitespace failure, а no-index exit1 не переименован в exit0.

Synthetic Decimal arithmetic: mixed step = 0.001, raw residual = 0.49999999999999750000000000001249999999999993750000. Это только scalar illustration, не Julia/QCL run. Fixture source содержит exact17/23 и first/second.yaml; source override expectation рассмотрен по accepted patch и fixture, не исполнен. @ref/@docs/API/source link availability не означает behavioral или scientific pass.

Две ошибки новых /tmp helper scripts сохранены: `/tmp/qcl-doc02-preflight-first-error.txt` (неучтённый owner Root, до любых source/worktree writes) и `/tmp/qcl-doc02-static-helper-first-error.txt` (false assertion при детекции --no-index аргумента). Raw no-index receipt сохранён; исправлены только helper mappings/argument checks. Candidate не менялся, implementation candidate round один. Итоговый verification helper exit0.

## Frozen patches

| Owner | Patch | SHA-256 |
| --- | --- | --- |
| QCLNEGF.jl | `/tmp/qcl-doc02-implementation-patches/QCLNEGF.jl.patch` | `fc2fe0353c15f0a52fcfb2c50e4b85fcf51decfbc429be198b2c17c6d0ddb1ae` |
| QCLNEGFRunner.jl | `/tmp/qcl-doc02-implementation-patches/QCLNEGFRunner.jl.patch` | `960331cc77967759882b4767b99be576e0c83bbcb5f6164681f3d8ce60c5af62` |
| root | `/tmp/qcl-doc02-implementation-patches/root.patch` | `0431f95b7b37db8c5789bd35e51247401a79457d56193c7b6932c0d956c34358` |

Identity `/tmp/qcl-doc02-implementation-identity.json` содержит source witness hashes, exact baseline/candidate hashes, source status/diff proofs, guards и raw статические exit codes. This report `/tmp/qcl-doc02-implementation-report.md`.

Scope: researcher raw/mixed/fresh final U/G route; developer exact17/23 assigning-source/effective-plan boundary; operator verified current/previous/error/import-as-new-attempt route. Прежняя expert/optical справка сохранена, quantitative gain validation не обещана. Runbook не получил скопированных numerical formulas или новых science gates.

Budget: ≤30min,1CPU/2GiB/128KiB output, один exact candidate round. CPU time/peak RSS отдельно не измерены. Не выполнялись product imports/tests/Julia/docs render/build/browser/server/solver/SCBA/Poisson/profiling/benchmark/CI. HTTP/public link availability и browser readability не проверялись. Resource cap и static refs не являются numerical/runtime/native/scientific acceptance.

SI03/04/05, original/private checkout, checkpoint/other docs/SCI05 files не записывались. Core/Runner existing HEAD/status/diff сохранены; все skill files и root AGENTS byte-hash guards unchanged. Чужие Root/Portal/Core jobs/ветки/receipts не изменялись. Git metadata дополнена только двумя разрешёнными worktrees/branches. Root final HEAD перепроверен.

STOP after freeze: separate independent CP-CODE, owning commits/publication/gitlinks — координатор.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact7 approved DOC02 docs применены | Candidate bytes/hashes +3 separate patches | CP-CODE/publication впереди | изменить |
| Existing expert/source/skills/foreign state preserved | @docs/@meta/anchors и guards; source HEAD/status/diff равны | Worktree Git metadata разрешённо дополнена | сохранить |
| Reader/source references доступны | 33 refs/19 links/28 source witnesses/static example | Не Documenter/browser/runtime acceptance | сохранить |
| E1 author no-index exit0 воспроизведён | Fresh exit1/no diagnostics, dry apply exit0 | Frozen original не исправлялся задним числом | изменить |
| Numerical/native/scientific acceptance получена | Таких runtime receipts нет | Соответствующие этапы не выполнялись | данных недостаточно |
