# OPS04 Platform T2/T3 Phase1 RED — независимое source review

2026-10-20. **REQUEST_CHANGES: два P2 замечания к различающей силе T3 test source.** Production baseline не признан дефектным и менять его для этих замечаний не требуется. T2 и write-side controls имеют meaningful healthy/negative witnesses; unrelated malformed healthy fixture не найден. Runtime/syntax/import/RED/GREEN не измерены.

Reviewer выполнил только text reads/searches, read-only Git metadata/diff и SHA256. Target imports/parsers/Python/pytest/Node/Deno/Nix/build/network/native/server/children/Git mutations и product/test source edits:0. Единственные outputs — этот report и identity. Объявленные20min/1CPU/2GiB/read4MiB/output96KiB — envelope, не измеренная cumulative telemetry.

## Source identity и порядок

Сначала прочитаны принятый D2 T2/T3 и независимый D2 review, затем фактические protected reader/writer/cache functions Platform и old/new test bodies/diff; авторский phase1 report прочитан после source assessment. Прочитан Platform CONTRIBUTING; отдельного AGENTS.md в изолированном component root нет. Ранее принятые root AGENTS/architecture/ownership boundaries сохраняются.

Actual worktree `/tmp/qcl-ops04-platform-worktree`, HEAD/base `b067723c82382689bff5cc366981c56e99b926f8`; status — только modified tests/test_application_release.py и tests/test_node_enrollment.py. Recursive submodule status пуст. Production targeted diff пуст и hash совпадает с selected baseline. Авторская inventory+256/-3 подтверждается actual numstat: Application57 additions/3 deletions, Enrollment199 additions/0 deletions; старые три удалённые строки заменены расширенной literal table/subTest case index, исходные negative values сохранены.

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-ops04-source-design-v2.md` | `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147` |
| `/tmp/qcl-ops04-source-design-v2-review.md` | `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42` |
| `ops/application_release.py` | `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0` |
| `tests/test_node_enrollment.py` | `68c56e1f6d86966a7e9ad7294bef550f2a74511d131dd067ae11ad1569000a00` |
| `tests/test_application_release.py` | `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6` |
| `/tmp/qcl-ops04-platform-red-patch.diff` | `b5aa36236fa373c709b6428198afbbf40c54895e2fa2c06fd8dbd365ea3bddef` |
| `/tmp/qcl-ops04-platform-red-identity.json` | `ad764c8dc849e046205536936783992fca26d06537ff018704351599b5f3fd31` |
| `/tmp/qcl-ops04-platform-red-report.md` | `c103de9ae30afb15d38eece1f60d423c5b4821d9f66b96514ab3bdade5d4d252` |

## Findings — полный коллированный набор

### F1 — P2: protected reader fixtures не различают writable access mode

Локаторы `tests/test_node_enrollment.py:211–245` (особенно222–223), `FakeProtectedFS.open:122–141`; actual production `protected_directory:344–359`, `read_protected_file:368`.

Fixtures проверяют O_NOFOLLOW всех opens и leaf O_NONBLOCK; отдельные non-directory negatives проверяют O_DIRECTORY. Но ни новые, ни сохранённые reader assertions не проверяют `(flags & os.O_ACCMODE) == os.O_RDONLY`. Fake open хранит flags, но access-mode semantics не исполняет. Поэтому конкретный source mutant O_RDONLY→O_RDWR в directory/leaf opens продолжит возвращать те же synthetic bytes, owner/mode facts, close counts и удовлетворит всему новому набору. Он нарушает требуемый readonly protected-reader contract и может иначе вести себя на реальных permissions.

Минимальное owning test correction: независимое наблюдение access mode у всех opens, выполненных reader path, через O_ACCMODE comparison; O_RDONLY часто равен0, поэтому bit-truthiness для O_RDONLY недостаточна. Healthy literal reader должен пройти, writable-mode mutant — нарушить assertion. Не навязывать O_RDONLY writer leaf: write-side контролируется отдельно. Production менять не требуется; новый syscall/permission policy не вводится.

### F2 — P2: «at most limit+1» overflow test маскирует over-read собственным EOF

Локаторы `tests/test_node_enrollment.py:179–183,226–232`; actual production `read_protected_file:374–383`.

Oversize fixture содержит **ровно65537** bytes и единственный fragment997; assertion суммирует доставленные bytes и получает65537. Fixture EOF сам запрещает прочитать больше. `requested` сохраняется в fs.reads, но не проверяется. Конкретный mutant заменяет production `n=min(4096,limit+1-len(chunks))` на постоянное `n=4096`: все нынешние healthy0/1/65536 cases остаются корректными, overflow case всё ещё читает ровно65537, закрывает descriptors и выдаёт ValueError. На input65538+ тот же mutant при последнем read способен получить bytes сверх limit+1. Этот ограничивающий predicate и есть проверяемый контракт; текущая fixture его не различает.

Минимальное owning test correction: сохранить exact-bound success и existing65537 negative, добавить overflow input с независимым tail **длиннее limit+1** (достаточно limit+2), в full-read и fragmented variants; assert rejected outcome, fd closure и actual total не больше65537, с ожидаемым boundary witness. Можно дополнительно проверять записанные requested sizes против независимого remaining budget. Не вычислять expected через production helper и не увеличивать bound. Реальный large read/FIFO/native run не нужен. Production менять не требуется.

## Подтверждённая различающая сила остальных controls

T2 `tests/test_application_release.py:1096–1166`:19 shared rejected literals и7 сохранённых regressions сопоставлены чтением с Root `/tmp/qcl-ops04-root-worktree/tests/application_cd_test.ts:102–151`. Named, explicit-empty и percent-encoded password, malformed authority, whitespace/control/NUL/DEL/leading-dash/nonstring cases содержатся явно. Rejection проходит real deliver_cli, требует ValueError с cache context, unchanged gate и **no callback calls**. Значения URI не выводятся в subTest metadata; используются synthetic cases. Existing closure/no-cache/hash/fetch-failure/no-quiesce controls сохранены.

Семь positives вызывают actual prefetch_controller_closures с fake command callback: HTTPS, SSH/ssh-ng username-only, percent-encoded colon username, file/absolute/local URI. Они требуют exact two argv arrays copy→path-info, original cache URI одним элементом, exact two hashes и неизменённый manifest. Поэтому blanket username/@ ban и URI rewrite не удовлетворяют healthy controls. Release digest/mirror equality принадлежит Root; Platform не дублирует его. Это существующая password-separator parity, не query/username secret detector, новый scheme allowlist или trust root.

T3 использует actual `ops.read_protected_file`, `ops.load_enrollment`, `ops.freeze_ssh_trust`. `BoundaryProtectedFS` наследует hand-authored inode/syscall facts; scripted read fragments/write outcomes/fsync faults не воспроизводят production acceptance loop. Product loop и trusted_stat остаются под проверкой. Реальные privileged namespace, FIFO, socket, root owner или filesystem persistence не симулируются как observed native proof.

Positive0/1/65536 bytes в full/fragmented variants проверяют exact returned bytes, read sum, nofollow/nonblock и descriptors. FIFO/socket/directory leaf требуют type rejection до read и nonblock/nofollow flags. Root/ancestor/leaf uid/group/other writable negatives требуют отсутствие read и closure. Symlink fake сам отвергает type, но независимый nofollow-open wrapper наблюдает flags на attempted failing syscall: missing O_NOFOLLOW не скрыт fake rejection. Root/ancestor O_DIRECTORY negatives имеют failed-open-aware close accounting. Invalid path cases требуют no opens. Empty raw reader legal, semantic enrollment/known_hosts consumer rejects empty — корректно разные уровни.

Writer positive310–325 включает обычный полный write и progressing1/2/3/4/remaining: exact snapshot bytes/SHA256,0600 leaf/0700 directory, file→directory→parent fsync sequence, sum written и complete/unique fd closure. Прогрессирующие short writes правильно healthy, не failure. Scripted zero, prefix+zero и prefix+exception требуют exception, retained exact original partial prefix, no fsync и closed descriptors. Fsync failures1/2/3 требуют exception, retained full attempt bytes и точный ordered attempted-fsync prefix; failed call входит в observed sequence, это корректно. Invalid empty/oversize/nonbytes frozen input запрещает namespace mutation/opens.

Сохранённый `EnrollmentTests.test_source_trust_substitution_does_not_change_late_transport_snapshot:666–691` продолжает проверять late SSH и NIX_SSHOPTS на один frozen path, неизменные original snapshot bytes/SHA и отсутствие reread substituted source. Этот source witness не доказывает реальный SSH/Nix transport, trusted-root post-freeze integrity или signatures.

## Дальнейшая граница и решение

Имя phase RED не означает обязательный red результат: production Python guards уже соответствуют многим новым assertions. Source review не должен искусственно ломать production ради expected failure. После correction нужен новый frozen source hash/patch/identity и независимый narrow review; этот report не расходует и не увеличивает конечный coordinator budget. Latest assigned local plan — два Python RED/GREEN calls по90s/1CPU/1GiB sampled RSS/32MiB TMP/2MiB raw — ещё не выполнялся reviewer. Точный selector, environment/runtime/source hashes, fresh intent/counter и failure classification остаются coordinator scope. Старое design text60s не выдаётся здесь за текущий runtime receipt или новое разрешение.

OPS04.N остаётся unknown: fresh server inventory/admission, native permissions/syscall/transport/content/signature/import/test-contract receipts не получены. OPS03 OS/provisioning/prepare-role и CR04 atomic admission residuals этим test-source delta не закрыты. Final CI/full release/science не выполнены и не наследуются от source PASS части T2/T3.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| T2 password separator/username parity различается | Exact literal tables и actual callbacks1096–1166 | Source only; не native store/credential evidence | сохранить |
| Reader действительно открывает readonly | Product source O_RDONLY, но assertions только nofollow/nonblock | F1 writable-mode mutant проходит | изменить |
| Reader bound maxlimit+1 различается | Overflow fixture226–232 | F2 EOF наcap маскирует over-read | изменить |
| Progressing writes healthy, failures сохраняют prefix | Actual writer310–354 + scripted syscall outcomes | Не native durability/root/FIFO proof | сохранить |
| Existing regressions не удалены | Actual +256/-3 и full delta | Runtime не выполнялся | сохранить |
| Runtime RED/GREEN/native/fullrelease/science доказаны | Receipts отсутствуют | Source-only stage; counters не расходованы | данных недостаточно |

**STOP. REQUEST_CHANGES только F1/F2 test source; reviewer execution=0.**
