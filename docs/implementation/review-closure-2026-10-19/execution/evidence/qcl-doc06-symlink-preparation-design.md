# DOC06 — external symlink fixture preparation D

2026-10-20. Отдельный focused ultra source-only envelope≤15min/1CPU/1GiB,
read≤2MiB/report≤96KiB. Product/adapter/test/harness edits и target execution не
выполняются. Independent high D_R, затем source/harness CPP, затем только отдельно
порученный конечный engineering E1. Original DOC06 RED+GREEN cap2/2 исчерпан;
этот D не добавляет попытку и не превращает failed GREEN в pass.

## 1. Подтверждённый failure и scope

Primary frozen witnesses:

| Input | SHA256 |
| --- | --- |
| `/tmp/qcl-DOC06-GREEN-1/original.log`,5423B | `3cae707b9a921a38e820cbb83ca0c7a73437048ed7b86fce27ae803b7d854b54` |
| `/tmp/qcl-DOC06-GREEN-1/receipt.json` | `2b058e3083a35824321936074e58db5f2f328dee0954bbbc97428c3a164c4fa1` |
| `/tmp/qcl-doc06-local-unit-run-v1.py`,9515B | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |
| Root `tests/docs_static_slice_test.ts`,30378B | `382a881675093137e5b42563d17851114e4ffbe8217ba3ead4636999e39cc8c4` |
| Root `ops/docs/static-slice.ts`,43061B | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |

GREEN raw:56 tests,54 passed/2 failed. Оба failed cases выбрасывают NotCapable в
`Deno.symlink()` (test382,388), требующем unscoped read/write; adapter call ниже
ещё не выполнен. Это не доказательство defect/pass production adapter.
Receipt capture complete, no guard error/stop/overrun; exit1. Raw/receipt/v1
harness остаются byte-exact неизменными. Новый adapter edit не требуется.

Сохраняются все56 test registrations/имена и смысл обоих negatives, остальные54
bodies/assertions и Fixture.prepare/обычный random fixture path. Никаких ignore/
only/filter/catch-NotCapable-as-pass. Новый helper добавляет preconditions и
healthy permission witnesses, не заменяет отрицательный вызов adapter mock-ом.

## 2. Единственное решение: два fixed externally seeded дерева

TMP — существующий единственный explicit harness-owned argument Deno.args[0].
Новых args/env/descriptor selectors нет. Внешний trusted launcher после создания
**нового уникального** TMP, до scoped Deno subprocess, создаёт ровно:

```text
TMP/prepared-symlink-file/
  backing/configuration_types.jl                    # empty regular file,0B
  snapshot/runner/src/application/configuration_types.jl
      -> ../../../../backing/configuration_types.jl
TMP/prepared-symlink-directory/
  backing/core/                                    # real empty directory
  snapshot/core -> ../backing/core
```

Все показанные parents — real directories, не links. Snapshot roots остаются
обычными directories; link-file target лежит вне snapshot, но внутри того же
prepared fixture/TMP. Directory-link target также внутри того же fixture/TMP.
Relative link texts фиксированы, не caller data. Link-file text42 UTF-8 bytes,
directory-link text15 bytes, итого57 link-payload bytes. Preseed создаёт10
non-TMP directories,2 symlinks и1 zero-byte regular file; научных/target bytes,
копии source tree, внешних объектов или arrays в seed нет. Все actual fixture
literal sources пишет сам проверяемый trusted test через Fixture.prepare.

Trusted local launcher реализует finite seed обычными os/pathlib metadata calls
и `os.symlink`, без импорта test/adapter/source parser или дочернего процесса.
Future Deno parent helper может сделать те же metadata operations в уже существующем
parent global read/write capability; scoped child не получает этих privileges.
Оба решения означают один exact layout, не альтернативы runtime выбора.

До seed launcher проверяет свежий owned attempt/TMP, real canonical ancestors,
отсутствие обоих prepared roots, отсутствие коллизий. Новый attempt/TMP создаёт
с0700, backing regular file exclusive0600, real directories0700. Existing path,
symlink ancestor, неверный owner/type или отказ metadata не исправляются удалением
чужого дерева. У trusted launcher есть право создавать лишь эти nodes в своём
новом TMP; metadata/path checks не являются adversarial sandbox/ownership proof.
Ownership/admission и отсутствие concurrent untrusted mutation остаются external
harness obligations. Не переходить к arbitrary path/symlink target из environment.

После seed launcher lstat проверяет две **реальные** links, ожидаемые обычные
target types и точные relative link texts; strict realpath каждого link должен
совпасть с указанным backing target и компонентно лежать внутри canonical TMP.
Не использовать startsWith(TMP) без separator. Проверить finite exact seed
inventory и baseline regular bytes0; unexpected entries/links/targets block before
Deno child. Directory target не dangling; file target существует как regular file.

## 3. Точная test delta: никаких symlink creation/rename в child

Только Root `tests/docs_static_slice_test.ts`:

1. Добавить private `preparedSymlinkFixture(kind, body)` с literal
   kind=`file`/`directory`, выбирающим два exact names выше. Конструировать
   `new Fixture(fixedPreparedDir,sources())`; ordinary `fixture()` с
   Deno.makeTempDir и его54 cases остаётся unchanged. Prepared helper не создаёт
   links, не rename/delete source nodes и не пытается fallback в random fixture.
2. До `f.prepare()` проверить canonical TMP и fixture roots/ancestors как real
   dirs; exact lstat link.isSymlink=true, target.isFile/isDirectory как положено,
   realPath(link)=exact expected target, всё внутри TMP. Missing/regular fake link,
   wrong/dangling/outside target, extra mutated seed или metadata/permission error
   означают **test failure**, не expected adapter refusal и не skip.
3. Выполнить существующий `Fixture.prepare()`. Его ordinary write helper делает
   mkdir/writeFile; file fixture пишет PATHS[0] через existing leaf link, directory
   fixture пишет PATHS[8] через existing core ancestor link. Остальные8 selected
   fixture sources и receipt создаются обычным путём внутри этого же fixture.
   Не вызывать Deno.symlink/Deno.rename и не заменять link обычным файлом.
4. Healthy real-filesystem witnesses после prepare: link всё ещё lstat symlink;
   read через selected alias и прямой backing path возвращает **точные те же**
   ordinary literal bytes из f.text[PATHS[0]]/f.text[PATHS[8]]; byte lengths и SHA
   совпадают с соответствующей уже созданной receipt entry. Для directory case
   selected leaf regular file, а именно core ancestor symlink. Прочитать/сверить
   все9 selected literals с f.entries before negative call, чтобы fixture не был
   missing-source/hash-mismatch trick. These reads/writes разрешены существующим
   ownTMP scope; неизвестная способность traversal/read/write не считается pass.
5. В обоих existing named Deno.tests вызвать prepared helper и `f.run()`; требовать
   status=`refused` **и exact reason=`symlink_or_invalid_source`**. Fixture.run
   сохраняет existing assertion, что facts.json при refusal не появился. Generic
   `io_or_input_failure`, NotCapable, hash mismatch или любая exception — failure.
   Оба результата должны исходить от actual unchanged generateStaticSlice.
6. Prepared fixture trees оставить после success/failure для harness receipt/
   sampler и source-review; это конечные2 trees. Generic54 cases сохраняют existing
   cleanup-on-success/retention-on-failure. Не добавлять blanket cleanup TMP или
   менять сохранение original raw. Не выполнять optional mutation после каждого
   case, не повторно использовать prepared trees для второго unit attempt.

Source binding: adapter selectedPath215–236 walks each component via lstat и даёт
symlink_or_invalid_source для leaf или ancestor; generateStaticSlice1063–1116
проверяет receipt/snapshot/output и source hashes. Поэтому precise reason плюс
healthy witnesses отличают intended protection от fixture permission accident.
Не добавлять production test hook. Existing positive regular-file tests и их
известные source assertions остаются independent healthy adapter path; новый
negative helper не должен вызывать дополнительный positive adapter run.

## 4. Точная launcher/harness delta и accounting

Будущий local writer создаёт **новый** `/tmp/qcl-doc06-local-unit-run-v2.py` из
frozen v1 с minimal source delta: fixed seed helper/validation, before/after seed
sampling/receipt section и вызов seed перед Popen. v1 не редактировать. Retained
RawCapture/sampler helpers и runtime identity прежние; нужная новая версия harness
получает свой hash/CPP, не alias под старым receipt. Test получает свой новый hash,
adapter обязан сохранить SHA3dde28…8594b byte-exact.

В existing try сначала открыть original.log exclusive, затем seed+validate+
sample, затем единственный scoped child Popen. Seed ошибки обрабатываются existing
failure-retention path: process=None, bounded original log/guard error/receipt,
seed.status=failed и child_started=false; no unit pass и no automatic repair/retry.
Started/deadline охватывает и seed, не только child. Existing raw draining,
post-drain output-overrun, termination и failure semantics сохраняются.

Receipt добавляет небольшой private seed section, encoded≤8KiB: phase/status,
relative entries/types/link texts/expected relative backing targets, lstat/realpath
checks, link_payload_bytes57, regular_payload_bytes0, dirs10/links2/files1,
prelaunch measured regular bytes/sample, seed elapsed/failure, child_started,
test+adapter+harness+sampler hashes. Exact actual target paths остаются private;
публичный формат не создаётся. Metadata fields фиксируются по наблюдению, не
самообъявлением prepared=true. Raw child output остаётся byte-preserving;
preparation logs/error отдельно связаны receipt, не выдаются за Deno test output.

Existing sampler суммирует regular-file logical st_size, excludes symlinks и
не traverses directory symlink. Backing targets находятся в **обычных** backing
subdirectories того же TMP, поэтому:

- file target bytes учитываются один раз через real backing file; alias не
  считается второй regular copy;
- directory target subtree также traversed через real backing/core один раз;
  alias snapshot/core не удваивает scan и не скрывает payload вне TMP;
- initial regular seed payload0 B, link texts57 B и directory/symlink inode/
  allocation overhead отдельно задекларированы, не подставляются в regular-file
  metric как измеренный0. Physical allocation/quota остаётся not_measured.

Сделать sample после seed **до** Popen и финальный sample после child/drains,
помимо existing50ms loop; сохранять max/count с явным phase coverage. Seed не
создаёт запас вне8MiB sampled logical TMP envelope и не получает extra grant.
После child также остаются конечные2 literal fixture trees и runtime deno-cache
в local v1 layout; они входят в тот же sampler scope8MiB. Новые witness9-file
reads имеют bounded source fixture size, без target imports. До live E1 source
CPP должен подтвердить finite aggregate prepared payload+existing fixtures/cache
и no unexpected arrays. Sampled8MiB/RSS guard не становится hard quota или proof
transient peaks. Seed link nodes57 bytes/13entries не являются всей fixture cost.

Local v2 сохраняет existing local v1 filtered environment и его честные limitations;
это не claim выполнения будущего docs-helper clearEnv contract. Script capabilities
не меняются. Future helper обязан сохранить D1/D2 exact environment самостоятельно.

## 5. Narrow override future docs-helper D1/D2

Immutable docs-routing D1 SHA
`fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270`
и D2 SHA
`bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70`
не меняются. Единственный preparation override: future `ops/docs_tests.ts` в unit
mode после создания OWN_DOC06_TMP и до DOC06 child готовит/проверяет этот fixed
layout в **OWN_DOC06_TMP**; отчёт preparation — existing dedicated step receipt.
`docs:preflight` не исполняет test и не изображает seed уже измеренным/выполненным;
missing source recipe/owned capability остаётся prerequisite, actual seed refusal
блокирует child перед unit pass. Новый descriptor input/loader env/публичная schema
не нужны: paths выведены из единственного уже принятого TMP capability.

Future scoped child contract остаётся D1/D2: exact trusted test+adapter read,
own TMP read/write, exactly one TMP positional argument после `--`,
no allow-env/run/net/ffi и no workspace-wide grant, selected runtime/argv flags
не ослабляются. Local E1 сохраняет command/flags frozen v1; future helper сохраняет
свои D1/D2 flags/clearEnv=true with only DENO_DIR, отдельный admitted cache.
Для future layout seed payload находится в owned TMP, cache — в уже отдельном
runtime-cache domain; местный v1 cache-inside-TMP не копировать молча в него.

D2 units map получает final reviewed test SHA и expected_tests=56 при неизменном
count; не считать old SHA382a… binding после edit. Reporter/count validation,
base-only/full distinctions, empty loader_env и no hidden version execution
сохраняются. Seeding authority родителя не передаётся child как permission.

## 6. Controls, E1 proposal и stop

Source/harness CPP проверяет before-live:

| Control | Required observation |
| --- | --- |
| Missing seed / ordinary file instead of link / wrong target / dangling / outside TMP | preparation/precondition failure до actual negative; no fallback/skip |
| Seed collides with existing prepared root | launcher refuses до child; original evidence retained |
| Healthy seed |2 actual links, exact real targets; ordinary write/read+hash9 selected literals succeeds; symlink survives prepare |
| Leaf vs ancestor purposes | Leaf symlink at PATHS[0]; directory ancestor core at PATHS[8], selected leaf real; actual adapter refusal reason exact in both |
| Adapter symlink check removed/mutated | Tests cannot pass just on NotCapable/io_or_input_failure; body reaches unchanged adapter |
| Permissions/argv | Exactly2 trusted code files+ownTMP read, ownTMP write, one TMP arg; no widened capabilities, no child symlink/rename |
| Count/other cases | All56 named tests remain, other54 bodies/assertions unchanged; no filter/ignored/only |
| Sampler/retention | Real backing bytes sampled once, no outside subtree; seed/terminal samples, honest symlink/physical-metric limits; all failure receipts/raw retained |

Controls здесь спроектированы, не выполнены. Это source/harness correction,
не scientific repair. Из-за исчерпанного original2/2 допустимо предложить **одну
отдельную distinct engineering E1**, только после independent D_R и source/harness
CPP по уже данному human engineering-resource grant и отдельному receipt.
Предлагаемый finite envelope E1: один запуск revised harness,≤120s total including
seed,1 CPU affinity, sampled process-tree RSS≤1GiB, sampled owned regular TMP
≤8MiB, raw output≤1MiB с прежним stop threshold/drain policy. Лимиты не hard quota;
любая невозможность нужного guard — honest failure/block. Immutable input/runtime/
helper hashes обязаны совпасть fresh binding. Нет source imports вне trusted
2code files и fixtures inert bytes, science/CI/server0.

E1 не автоматический третий DOC06 run в original envelope. Если E1 не successful
56/0 либо preparation/capture/guards/source binding неизвестны — сохранить failure
и STOP, без автоматической четвёртой попытки, permission widening или замены
negative purpose. Данный D **не выполняет** E1 и не выдаёт его approval receipt.
Credentials, если получены coordinator для другого scope, не имеют роли в local
fixture test и не читаются/копируются этим агентом.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
|54/2 GREEN остановился на fixture creation | Raw+receipt exact hashes, NotCapable stack382/388 | Не adapter verdict | сохранить |
| Внешнее seeding снимает child symlink API prerequisite | Exact tree/prepare/witness/adapter reason contract | Revised source и E1 ещё не проверены | изменить |
| Child privileges можно оставить прежними | Всe node/targets внутри existing TMP, no child symlink/rename | Runtime traversal compatibility пока не измерена | сохранить |
| DOC06 всё56 passed | Таких новых runtime receipts нет | Original failed retained; cap2/2 exhausted | данных недостаточно |

STOP: frozen D/identity для independent high R, source/harness CPP перед отдельно
bound E1. Никаких actual source edits/executions этим этапом не было.
