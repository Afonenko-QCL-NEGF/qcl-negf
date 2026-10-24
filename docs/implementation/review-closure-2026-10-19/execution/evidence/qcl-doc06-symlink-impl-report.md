# DOC06 — external symlink preparation implementation handoff

2026-10-20. Source-only I по D `f21dcb464b17c8511eaed0bd60ff6b10722f9416e9005ae3849631f14924dcba` и high D_R `cae997412488ef7e1508a0c8920120d167f7c59b48047f387e354802506f065d`. Нового runtime/import/parser/typecheck/format/lint/test/network/build/commit/CP call нет. Исходный DOC062/2 исчерпан; engineering E1 **не запускался**, требует отдельного Root finite binding после CPP. Старый GREEN54/2 остаётся failed fixture-preparation result, не adapter verdict.

## Identity и scope

| Artifact | SHA256 |
| --- | --- |
| Adapter, без изменений | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| Test base сохранён `/tmp/qcl-doc06-symlink-base-docs_static_slice_test.ts` | `382a881675093137e5b42563d17851114e4ffbe8217ba3ead4636999e39cc8c4` |
| Новый `/tmp/qcl-doc06-worktree/tests/docs_static_slice_test.ts` | `ff6f0ec86be1ae7905721848998f8f7e7d22173d35534119f6102317e7fa8ec6` |
| Frozen old `/tmp/qcl-doc06-local-unit-run-v1.py`, unchanged | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |
| Новый `/tmp/qcl-doc06-local-unit-run-v2.py` | `1222d7d0a03dd39b72fc17be7029ced9e7422273f5ab08dbf48e6bd621f3014d` |
| Test delta `/tmp/qcl-doc06-symlink-test-delta.patch` | `5aae29fd56abcc65f00df94c399736a09e5f4bad75a3fd74bcd98585bed1d14b` |
| Harness delta `/tmp/qcl-doc06-symlink-harness-delta.patch` | `2406643c61bf928acc027ea19f7a927d44882fefc7f4930ee27a9371be51520f` |

Test writer работал только в isolated `/tmp/qcl-doc06-worktree`; managed Root/canonical/CP/gitlinks/commits не менялись. Original raw/receipts, v1 harness, sampler и accepted adapter не перезаписаны. New harness — отдельный source file из frozen v1, не alias старого hash.

## Test delta: точная causality

Все56 registrations/names сохранены. Other54 bodies/assertions, source fixtures, `Fixture.prepare`, обычный random `fixture()` и cleanup-on-success/retain-on-failure неизменны. Изменены только две existing symlink-negative bodies и добавлен private `preparedSymlinkFixture`.

Helper принимает только literal file/directory kind и выводит fixed prepared paths из единственного existing TMP positional capability. Никаких новых args/env inputs, `Deno.symlink`, `Deno.rename`, repair/delete/fallback/skip/catch-NotCapable нет.

До source preparation helper проверяет canonical real TMP/root/все внутренние ancestors; exact finite no-follow inventory и тип каждого node. Неизвестный node отвергается **до** рекурсивного traversal, special file не читается. Проверяются real link, exact relative readLink text, strict realPath==expected backing, обычный target type и baseline file0B. Проверки child начинаются с TMP; `/tmp`/attempt parent не читаются.

Обычный неизменённый `Fixture.prepare()` пишет через existing link: file alias PATHS[0] или core ancestor PATHS[8]. После него link topology повторно проверяется, все9 actual selected files read/hash/length сверяются с f.entries и strict decoded authored literal. Каждый non-link selected leaf lstat regular. Отдельно direct backing bytes проверяются strict text/length/SHA против entry; alias exact text также подтверждён. Witnesses проверяют actual filesystem bytes, а не два hashes от f.text.

Только затем вызывается unchanged actual `f.run()`, сохраняя existing no-facts-on-refusal assertion. Теперь оба negatives требуют **refused + exact `symlink_or_invalid_source`**. Generic io failure/NotCapable/exception/hash mismatch не является success. Это усиление причинности, не weakening assertion. Дополнительных positive adapter invocations нет; healthy witnesses — только metadata/ordinary read-write/hash. Оба finite prepared trees сохраняются при success/failure.

## Новый local harness

Единственный поддерживаемый argv contract для будущего Root binding:

```text
<reviewed Python> /tmp/qcl-doc06-local-unit-run-v2.py DOC06 SYMLINK-E1 DENO tests/docs_static_slice_test.ts
```

Это **не executed command**. Whitelist запрещает другой task/kind/attempt/test selector; path `/tmp/qcl-DOC06-SYMLINK-E1` создаётся exclusive, повторный вызов collision не repair/reuse. Новые attempt/TMP directories0700, backing file exclusive0600, seed dirs0700. `/tmp` canonical/type проверяется launcher, fresh owned roots owner/mode/type/canonical тоже проверяются. Ни caller/environment-provided symlink target, ни произвольная source tree copy не принимаются.

После exclusive original.log, до единственного Popen, launcher создаёт exact seed layout:10 dirs,2 symlinks,1 empty regular file,13 non-TMP nodes. Link texts42+15=57B; relative targets совпадают D. Exact no-follow inventory/type/owner/mode/readlink/strict realpath+component containment и baseline regular0 проверяются после создания. Unexpected entry/type/target/metadata/collision означает failure без child/repair/retry. Existing outside attempt collision до ownership не даёт права писать/чистить чужое дерево.

Seed status/phase/counts/link text/relative backing/lstat/realpath observations, elapsed/failure, child_started и hashes записываются в private bounded≤8KiB receipt section. `prepared` устанавливается только после topology validation и prelaunch sample. Seed/prelaunch failure до Popen проходит existing failure path: child_started=false, guard-error/raw/receipt retained, no pass. Public format не вводится.

Started/deadline охватывают seed. Добавлены **before_seed**, **prelaunch** и **terminal** sampler observations плюс прежний50ms loop. Каждый обновляет max/count/phase coverage и **действительно проверяет** logical TMP8MiB и wall120s. Prelaunch reason блокирует child; terminal overrun после drains не даёт exit0→pass. Terminal sampling/source-binding exception превращается в guard failure. Bound start test/adapter/harness hashes сравниваются с terminal observations; ошибки binding не вызывают uncaught повторное чтение source при receipt construction. RawCapture fallback/drains/post-drain output-overrun/RSS/termination/exit criteria сохранены.

Adapter hash pinned3dde…, old runtime/sampler/helper full hashes сохранены; test/harness start hashes observed до seed, terminal stability проверяется отдельно. Root должен связать новый test/harness hashes с finite E1 plan. Capabilities child byte-for-byte прежнего argv: read только два trusted code files+ownTMP, write ownTMP, один TMP arg, no env/run/net/ffi grants. Local v1 filtered environment/cache-inside-TMP сохранены. Future docs-helper D1/D2 clearEnv/separate cache не реализуются и не подменяются этим local harness.

## Accounting и пределы

Sampler по-прежнему суммирует regular st_size no-follow. Оба backing targets — ordinary descendants TMP, поэтому payload после prepare учитывается один раз через backing; alias symlinks не удваивают/не скрывают outside payload. Baseline regular0, link57B и10dir/2link/1file metadata **не объявлены всей fixture cost**. После prepare остаются ровно два tiny9-file trees с receipts; остальные cases как прежде finite serial. Deno cache находится в том же sampled TMP. Physical/inode allocation/quota и transient peaks not_measured;8MiB/RSS guards sampled, не hard quota.

Witness reads ограничены tiny sources() и9 expected paths; inventory обход только exact declared nodes. Missing/changed/fake/wrong/dangling/outside seed — precondition failure, не adapter success. No scientific arrays/solver/build/fullCI. Runtime Deno traversal/write compatibility остаётся именно различающим свидетельством будущего E1, сейчас неизвестна.

Выполнены только source/text/Git-diff/SHA операции, просмотр design/review/v1/sampler и delta. Никакой Python/Deno parse/import/compile/test harness не исполнялся. Conservative named logical reads <1.5MiB при2MiB grant, delivered code/deltas/report/identity <128KiB. Kernel physical I/O/CPU/RSS не инструментированы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Child symlink API prerequisite удалён | Exact two external seeds + helper metadata/9-file/direct hash witnesses | Runtime traversal не измерен | изменить |
| Negative purpose сохранён/усилен | Same2 names, actual adapter + exact reason, no-facts assertion | Ещё нет нового runtime result | сохранить |
| Seed/terminal samples участвуют в guards | Pre-Popen reason block; final reason входит exit criteria | Sampled metrics не hard quotas | сохранить |
| DOC0656 passed / E1 accepted | Нового run receipt нет; original2/2 exhausted | Требуются high CPP и отдельный Root finite E1 | данных недостаточно |

**STOP для independent high CPP; E1 не запускать без Root binding.**
