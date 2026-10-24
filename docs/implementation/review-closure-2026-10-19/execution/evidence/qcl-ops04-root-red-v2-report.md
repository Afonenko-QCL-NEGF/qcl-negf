# OPS04.S Root T1/T2 — phase 1 RED source v2 freeze

Статус: **test-source frozen для отдельного high review; execution/observed RED отсутствуют**. Эта source-only continuation закрывает названный в v1 отсутствующий CLI seam по принятому addendum, без изменения production. Ранее сохранённые v1 report/identity/patch не изменялись; их SHA256 сверены перед v2 freeze.

Source authority: Root `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, isolated local clone `/tmp/qcl-ops04-root-worktree`, branch `codex/review-closure-depot-byte-binding`. Фактические final HEAD/status/submodules проверены: только два modified test files, восемь неинициализированных selected gitlinks. Current coordinator Root d4113 не переносился в этот checkout; его gitlink/evidence-only продвижение не подменяет зафиксированный source authority. Protected original `/home/tolya/Загрузки/qcl-negf` не изменялся. No submodule init/update/network. Attempt identity не является новым ручным revisions lock.

Принятые design inputs:

- D2 `/tmp/qcl-ops04-source-design-v2.md`, SHA256 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147`.
- D2 independent review SHA256 `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`.
- CLI seam `/tmp/qcl-ops04-cli-seam-design.md`, SHA256 `93ffbbcdd50770295f2f21e1a9befc47acc63231279b1ff79aebf48e7cc69a7f`, сверён перед continuation.
- Separate high review `/tmp/qcl-ops04-cli-seam-design-review.md`, SHA256 `626159c6307b5664025d800f7d3d8101fb1ab55a4bd8a809f76b4aa949e653d5`, APPROVE, сверён перед continuation. Его ограничение порядка чтения остаётся в original report.

## Источник изменений и различающие controls

Только `tests/solver_test.ts` и `tests/application_cd_test.ts`. Прежний helper/cache corpus v1 сохранён целиком, новые tests добавлены после него. Никаких source-grep controls, production exports/implementation, subprocess harness или high-level validator injection. Dynamic module export casts задают принятые `captureDepotMetadata`, `runSolverBuildCli`, `runApplicationCdCli` signatures без missing-export type error на baseline, где этих функций пока нет. Отсутствующий seam должен различаться будущими healthy runtime fixtures; отрицательные fixtures сами по себе не считаются наблюдением RED.

`tests/solver_test.ts` additions:

- Instrumented low-level opener передаёт bytes production capture loop. Ровно один open/close, stat до read, requests равны оставшейся части 65537-byte storage; positive short reads с UTF8 codepoint, разделённым между syscall returns; exact65536+EOF accepted. Sentinel65537 rejection без следующего read, максимум65537 returned bytes.
- Close после stat/read/no-progress/decode/size/nonregular outcomes; original stat/read/open errors сохраняются. Nonregular stat не вызывает read. No real FIFO или hostile path-race guarantee.
- Default capture с настоящими временными regular files: Unicode roundtrip, invalid C3-28/truncated multibyte, BOM, raw NUL, directory rejection и empty-string capture (semantic JSON validation далее).
- Actual named solver CLI: прежний `[DEPOT_JSON, --profile ..., --test-workers ...]`, HTTPS/file counts1/2, single opener, independent actual argv digest/observation, штатное inherited stdout. Invalid argv/options/unknown flags, encoding, raw bound, wrong component, malformed metadata, wrong lock → reject и ровно0 execute callbacks, opened descriptor count matched closes.

`tests/application_cd_test.ts` additions:

- Actual named CLI healthy assembly с настоящим file capture A. **На первом application build callback** исходный pathname атомарно заменяется валидным B; повторное opening сразу ломает fixture. Subsequent prefetch и solver build обязаны использовать A URL/hash; independent SHA256 actual outgoing JSON сверяется с argv digest и returned raw/produced observation.
- Ожидаемый causal order: open→graph→lock→application→prefetch→solver→path-info→graph→copy. Capture flags true для application/solver/prefetch/path-info, inherited для copy. Literal ssh-ng username-only URI остаётся одним argv element. Existing release digest независимо вычислен от literal graph + application/solver closures.
- Production writes `.pending` и делает rename в owned TMPDIR; final manifest читается, fields/identity/returned value проверяются, pending отсутствует. До copy никаких manifest writes. Это не проверка Nix execution или реальных output contents.
- B captured до начала, array-shaped path-info и no-cache healthy route; во время application callback изменяются dependency object functions и вложенный borrowed graph. Поздние dispatch/recheck обязаны использовать заранее captured function refs и собственный graph snapshot.
- Invalid argv/cache/encoding/size/graph/JSON/lock → reject, ровно0 execute callbacks, final и pending отсутствуют. Действительный sourceGraph default read-only Git probes не названы execute: fixtures инъецируют только readonly identity reads и не запускают subprocess.
- Изменившийся graph на обязательном recheck после path-info блокирует copy/writes. Existing pending collision сохраняет prior bytes и не создаёт final output, проверяя штатный createNew и отказ rename чужой попытки.

## Freeze, проверка и ограничения

`git diff --check` завершился exit0 после final source additions. Это whitespace check; formatter, typecheck, imports и execution не выполнялись. Target parsers/Deno/Nix/Julia/tests/build/install/network/server/stage/commit/push/children/checkpoint writes: **0**. Production три owning файла сохранили baseline SHA256. C08/science не затронуты, Root остаётся sole checkpoint writer.

Continuation envelope ≤25min/1CPU/2GiB/read≤3MiB/output≤96KiB. Ресурсная cumulative telemetry не инструментирована; envelope не выдан за measured usage. Только чтение текстов/SHA/Git metadata/diff, source записи и attempt artifacts в `/tmp`. Новый runtime grant/slot не создан. Перед будущим единым root RED packet координатор проверяет exact prepared Deno/toolchain, selectors/counters и owned TMPDIR write permission; PATH equivalence не предполагается. Nix fromJSON/hashString assertion, actual default Git/Manifest identity integration, native outputs/import origins/full suites/scientific acceptance здесь не исполнялись.

Freeze hashes:

| Файл | SHA256 |
| --- | --- |
| tests/solver_test.ts | d26512392d63eaccf44ab7711ea07b1b6c8a15a3fb3108afd47c1ccacbf9d542 |
| tests/application_cd_test.ts | bd92a82d858ea17d1a124f2a9d257a76329f7f1630e423aad5ba1840c1982f85 |
| ops/solver.ts unchanged | bc513f610cce976d108e17902ebd423c434992ba0edb91e2bdc3da2e5f3c247f |
| ops/application_cd.ts unchanged | 91989d0171e011f4518e178e247d4f7a466d08bd02b7931308a202c4354ee9ce |
| nix/solver.nix unchanged | 16c99da166ee2d9afc7d238fa317e43f0bcc71e2eccb8de3ff11e97b70aa858f |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| V1 CLI seam ambiguity addressed in regression source | Accepted named seam + bounded capture/actual CLI causal fixtures above | No runtime/observed RED; adapter implementation awaits phase2 | дополнительно измерить |
| Prior helper/cache corpus and v1 receipts preserved | v1 hashes unchanged; appended source only | Review must assess combined v2 source | сохранить |
| Production unchanged | Owning file hashes equal original cfc38e1 baseline | No fix implemented | сохранить |
| Native/release/science acceptance established | No execution receipts | Source-only phase | данных недостаточно |

**STOP: v2 test source frozen; separate high CPP before coordinator bounded RED. No phase2 implementation or execution activated by this report.**
