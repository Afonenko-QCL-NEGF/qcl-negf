# DOC06 local unit harness v1 — independent source review

**PASS_SOURCE — fixed DOC06 harness delta сохраняет принятые capture/guard predicates.** Call readiness остаётся условным: exact исправленный fixture, source/harness/runtime/operation binding и finite counter принадлежат Root. Этот review не запускает тест, не закрывает fixture R1 и не допускает full CI.

## Exact packet

| Input | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc06-local-unit-run-v1.py`,9515 B | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |
| parent `/tmp/qcl-root-local-unit-run-v1.py`,9477 B | `eb55de0a1c668723871ea1ae142630df43b024d164fd9564f36be3df68187195` |
| accepted parent review | `dca5d87440947cd27ae518a2a8054d934538ecc0c7f97db7df4622ebbc19b0ab` |
| `/tmp/qcl-doc06-local-unit-harness-identity.json`,604 B | `96d2c216d43d2e03dabf01011dff1e7381f4e9c75c6645d361525da4b8aa2d75` |
| RawCapture helper | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| owned-temp sampler | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| cached `/tmp/qcl-pinned-deno-test-help.txt`,14912 B | `780289de4c03cddc3fe7a17f9e47db5171f3326c4b5be0a0924f5da76b530df0` |

Новый harness прочитан полностью; полный text diff к parent прочитан. Parent review прочитан полностью; actual helper/sampler hashes совпадают с уже принятыми pins. Их code/runtime не импортировался. Большой executable hash reviewer не перечитывал под4MiB cap: Deno pin `cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c` согласован с поручением/parent evidence и literal нового harness; сам harness сравнивает actual runtime bytes перед launch.

## Scope, args, permissions и env

Allowlist теперь ровно `DOC06/DENO` и ordered fixture `tests/docs_static_slice_test.ts`; другие task/kind/fixtures отказывают до Popen. Attempt ASCII predicate и exclusive `/tmp/qcl-DOC06-ATTEMPT` directory сохранены; прежние raw не перезаписываются. Source path должен разрешиться в существующий fixed root/tests file. Нет shell command interpolation, установки или auto-discovery suite.

Executed argv — exact pinned Deno2.8.3 `test --cached-only --no-remote --no-npm --no-config`, два явно названных trusted code read paths и own TMP read; write только own TMP; нет allow-env/run/net/ffi. Ровно один owned TMP path передаётся после `--`; cached help:12 содержит `deno test [OPTIONS] [files]... [-- [SCRIPT_ARG]...]`. Help:39/88/94/95/112–127 подтверждает используемые flags и разделение capabilities. Tests проверяют ровно один Deno.args[0], абсолютный `/tmp/...`, без env/temp/worktree fallback.

LD/Python/Node injection keys удаляются как прежде. Новый pass удаляет **все inherited DENO_ keys** перед заданием собственного DENO_DIR в sampled TMP и DENO_NO_UPDATE_CHECK. Scope не получает сторонний Deno preload/config/env-injection через эти keys; --no-config исключает автоматическое config loading. Permission boundary не доказывает сама по себе отсутствие target eval/dynamic module loading в будущем adapter: code review остаётся обязательным. Test сейчас импортирует только future trusted adapter и подаёт source bytes как data.

PY/NODE branches остаются текстом parent, но недостижимы после exact tuple allowlist. Их присутствие не создаёт дополнительные допустимые calls. Сам process не становится полноценной OS/native sandbox или чужой security boundary.

## Bounds, RawCapture и truthfulness

Разрешённые delta resource literals: RLIMIT_CPU120/125, wall-stop trigger120s, affinity1, sampled RSS1GiB, sampled owned TMP8MiB, raw1MiB с прежним128KiB stop reserve. Receipt literals соответствуют actual predicates. Никакого увеличения scientific/CI бюджета.

RawCapture helper и sampler pins, construction-before-poll, error checking, byte-preserving log, partial-write fallback, TERM→3s wait→KILL, finally kill/drain/fallback, post-drain overrun predicate и final all-guards-success exit condition **не изменены**. Child exit0 отдельно не считается harness PASS. Unknown/incomplete capture/guard/stop/overrun сохраняет failure и original bytes, без silent truncation. Sampled TEMP/RSS не объявлены hard quota или transient peak proof.

120s — начало stop, не absolute end-to-end hard wall; cleanup/drain и I/O могут добавить время, как в accepted parent review. Per-process RLIMIT_CPU не общий cgroup CPU-time budget. Prelaunch assertions/hash/missing file могут завершиться до собственного receipt; coordinator обязан сохранить outer raw/intent и классифицировать, не resubmit автоматически. Unique attempt folder не реализует общий RED/GREEN counter: он внешний.

## Binding до sole first RED

Harness hardcoded Root — `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`. При проверке actual managed Root HEAD `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, test и adapter оба отсутствуют. Reviewed test находится в `/tmp/qcl-doc06-worktree` на frozen Root514. Поэтому invocation сейчас остановится на prelaunch fixture assertion, а не на planned missing adapter. Это **не intended readiness RED** и не основание тратить call.

Root должен сначала исправить fixture R1 из отдельного `/tmp/qcl-doc06-red-review.md`, получить narrow review и выполнить уже разрешённый exact placement/binding; проверить desired adapter absence для RED, pins/helper/runtime, operation uniqueness и finite counter. После запуска raw должен подтверждать именно expected missing-module failure; assertion/permission/typecheck/guard/resource failure имеет собственный verdict. Переход на другой root HEAD сам по себе не переносит old full acceptance.

Известный generic CI routing без mandatory owned args остаётся отдельным D ultra вопросом; этот fixed local argv его не исправляет и не разрешает full CI. Future GREEN требует exact adapter source review/import closure и собственного binding.

## Actions/read ledger

Reviewer runtime/import/parser/test/network/build/children/product edits/checkpoint/Git mutations/C08/science —0. Только text/hash/metadata и эти `/tmp` review artifacts. Общий ledger **524941 B** source upper bound для обоих DOC06 reports приведён в `/tmp/qcl-doc06-red-review.md`; он включает каждый diff/search/hash pass по полному размеру named input и существенно ниже4MiB. Повторно не суммировать его как два отдельных бюджета. Physical I/O/RSS не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Fixed DOC06 argv/owned TMP/permissions correct по source | Full harness + help12/39/88/94/95/112–127 | CLI не запускался reviewer | сохранить |
| Capture/sampler/kill/drain composition unchanged | Полный parent diff + actual helper pins | Inherited sampled/cleanup caveats остаются | сохранить |
| Sole first RED ready к запуску сейчас | Managed fixture отсутствует, test R1 ещё открыт | Нужны narrow correction и Root binding | дополнительно измерить |
| FullCI/native/scientific acceptance | Таких receipts нет | Local unit source review имеет узкий scope | данных недостаточно |

**STOP. PASS_SOURCE harness; call pending exact corrected-fixture placement/binding, full CI не admitted.**
