# DOC06 — independent final high review SYMLINK-E1

2026-10-20. **PASS_SOFTWARE_DOC06_UNIT_E1** в узком scope: final test
`e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69`
с unchanged adapter `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`
прошёл 56/0 synthetic source-only unit cases в единственном предъявленном distinct
engineering attempt SYMLINK-E1. Блокирующих замечаний к этому software acceptance
не найдено. Это не приёмка actual selected nine-source snapshot, документационного
смысла, render/native/full Root CI или научной модели.

## Identity и source closure

| Артефакт | Проверенный SHA256 |
| --- | --- |
| E1 `/tmp/qcl-DOC06-SYMLINK-E1/receipt.json` | `eccf5015685c8b0ff3df87fef2672f6fe461124ce9f09c56b0cea68807b034fc` |
| E1 `original.log`,3788B | `a42bb0325226b4244b6e4ed0c85e2a141b5176965021318bcc4238f378136ae8` |
| `/tmp/qcl-doc06-symlink-final-format-binding.json` | `92296ab0940997cfc504e4f2def02d8e26bd678fce57722c550208d654fb001c` |
| `/tmp/qcl-doc06-symlink-format-delta.patch` | `35f73b1ffd0a9f80e0a1cb0f9f85e832cde3289594234676046de5895f6983dc` |
| Managed Root `tests/docs_static_slice_test.ts` | `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69` |
| Managed Root `ops/docs/static-slice.ts` | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| `/tmp/qcl-doc06-local-unit-run-v2.py` | `1222d7d0a03dd39b72fc17be7029ced9e7422273f5ab08dbf48e6bd621f3014d` |
| D `/tmp/qcl-doc06-symlink-preparation-design.md` | `f21dcb464b17c8511eaed0bd60ff6b10722f9416e9005ae3849631f14924dcba` |
| D_R `/tmp/qcl-doc06-symlink-preparation-design-review.md` | `cae997412488ef7e1508a0c8920120d167f7c59b48047f387e354802506f065d` |
| CPP `/tmp/qcl-doc06-symlink-impl-review.md` | `8d6074a6ddf3bdb13436fd4a83e94254daa6abea5f37af393ad86e0c197b01e9` |

Actual managed Root bytes совпадают с E1 fixture_sha256, seed.bindings,
bound_fixture_sha256 и terminal_source_bindings. Adapter/harness hashes также
совпадают на start/terminal и при настоящем readback. Таким образом, прежний CPP
prerequisite «promote reviewed test в managed Root» теперь выполнен с narrow
formatter binding, а не со старым SHA382a88….

Независимо прочитаны complete saved format delta и actual `diff -u` reviewed
ff6f0e… → managed e825f6…: только переносы строк/indent и trailing commas,
без изменения строк, условий, assertions, fixtures, registrations или controls.
Semantic CPP переносится по этому проверенному узкому delta. FORMAT-3 и LINT-3
receipts/raw имеют exit0, complete capture, null guard/stop, exact final test +
adapter SHA и `Checked 2 files`. FORMAT-3 был formatter mutation двух указанных
files, а не отдельный `fmt --check`; его exact final bytes и narrow delta связаны.
Новых format/lint/typecheck/test execution в настоящем review не было.

Read-only Git с GIT_OPTIONAL_LOCKS=0: Root HEAD
`469ef4ec36c1dfb967856108e5f9455429559c15`, dirty coordinator evidence/CP и
untracked DOC06 test/adapter. `components/qcl-negf-contracts` checkout теперь
f4009c9… с `+` к root gitlink d791dea…; это текущий наблюдаемый dirty integration
контекст, не source snapshot, породивший synthetic fixture. Selected DOC06
identity определяется exact test/adapter hashes, а не clean HEAD или текущим
составом submodules. Gitlinks/CP этим агентом не изменялись.

## Runtime evidence и причинность

Raw имеет ровно 56 unique `DOC06 … ok` lines, один header running56 и единственный
согласованный summary `ok | 56 passed | 0 failed (454ms)`. Независимая обработка
текста подтвердила равенство всех56 ordered names исходному GREEN: потерянного,
переименованного или дополнительного случая нет. Count не выведен из exit0.
Оба symlink-negative отображаются ok; source test:491–502 требует именно
`refused` + `symlink_or_invalid_source` после actual adapter call. Test:209–318
сохраняет pre/post topology и actual9-alias/direct-backing read/hash witnesses,
проверенные в CPP; I/O/permission/hash mismatch не мог заменить expected reason.
Следовательно, E1 снимает прежнюю неопределённость о traversal/read/write этого
точного preseed layout в scoped Deno execution.

Receipt: exit0; capture complete; capture_error/guard_error/stop_reason=null;
output_overrun=false; raw byte count3788 совпадает с actual raw. Command сохраняет
read exact2 code files + owned TMP, write owned TMP, один TMP positional argument,
no allow-env/run/net/ffi, no-config/no-npm/no-remote/cached-only. Harness pinned
1222d7… прежний. Runtime hash cdd88d… и sampler16a038… находятся в receipt и
проверялись reviewed harness перед запуском; binary/runtime повторно этим
review не читались и не исполнялись. Local filtered environment не объявляется
future docs-helper clearEnv contract.

| Runtime observation | Значение | Граница утверждения |
| --- | --- | --- |
| Total wall including seed | 2.127s при лимите120s | Recorded harness wall; без hard wall sandbox claim |
| Seed elapsed | 0.001076s | Только preparation interval |
| Sampled process-tree RSS peak | 325976064B при1GiB | Sampled, transient peak/physical proof отсутствуют |
| Sampled owned regular TMP peak | 664534B при8MiB | logical st_size; symlink/physical allocation исключены |
| TMP phases | before_seed1 + prelaunch1 + loop28 + terminal1 =31 | Есть runtime observations обеих дополнительных границ |
| Before seed / prelaunch regular bytes | 0 / 0 | Не total metadata cost |
| Terminal regular TMP bytes | 626708B | Включает retained fixtures/cache; не hard quota |
| Raw output | 3788B при1MiB | Complete, byte count согласован |

CPP + actual harness:148–171,241–267 устанавливают, что эти seed/terminal samples
участвуют в threshold guards и final predicate; это не только receipt fields.
CPU affinity1 задана reviewed launcher и указана receipt; actual CPU consumption
не измерялось как отдельный benchmark.

Seed receipt содержит 13 validated entries, counts10dirs/2links/1file,57 link
bytes, initial regular0, phase=terminal/status=prepared/child_started=true и
source bindings. Поле prepared относится к seed, общий unit pass устанавливают
raw и guard predicates. Physical allocation честно not_measured.

Read-only проверка сохранённых двух fixture trees дополнительно подтвердила:
оба live links имеют exact declared text/type и canonical targets внутри E1 TMP;
в каждом tree все9 selected actual files совпадают с bytes+SHA input receipt,
aggregate literal source payload2260B. Оба input receipts имеют SHA
`3f627e645bdf29aac1e530585ff703e82720ec9e69b45bec54c88d38fbb1164e`.
Negative out directories отсутствуют, что согласуется с no-facts refusal.
Это post-run readback retained evidence, не повтор adapter execution и не
ретроспективное доказательство отсутствия любых hostile namespace races.

Original GREEN raw3cae70… и receipt2b058e… byte-exact сохранены; они остаются
54 passed/2 fixture-creation failures, до adapter. Original DOC06 cap2/2 не
переписан в success. SYMLINK-E1 — отдельный переданный Root finite engineering
attempt1/1; настоящий review не добавляет запуск или retry и не перепроверяет
всю внешнюю историю попыток. Новая попытка этим verdict не разрешается.

## Точный acceptance scope и actual9-source gaps

Принимается конкретный software unit contract на inert **synthetic** fixture
bytes: проверенные source-only extraction/refusal/guard controls и работоспособность
external symlink seeding при unchanged scoped permissions. В raw виден `Check`
и завершённый Deno test run без --no-check; это не отдельный full package/root
typecheck или D1/D2 routing/full aggregate acceptance.

Actual девять selected sources этим E1 не приняты. У retained input receipts
`source_graph_sha256` равен literal `aaaa…`, revision labels берутся из test
constants, а contents — `sources()` test literals. Hashes связывают именно
переданные bytes; они не устанавливают commit→bytes. Adapter прямо говорит это
в header и `buildProjection().receipt.external_binding` (около1039–1047).
Projection остаётся private DEV/source-prototype, coverage partial,
application_release=null/run=null; endpoint не является configuration validator.

Для actual9-source reproducibility ещё отсутствует отдельный evidence set:

- Frozen выбранные component commits/owning files и externally prepared
  canonical snapshot всех9 paths с proven commit→bytes binding; current dirty
  checkout или synthetic revision labels такого proof не дают.
- Actual source-input receipt с real graph/source identity, each path/owner/
  revision/raw SHA/length и полной snapshot inventory. Отсутствие source либо
  неподдержанный construct должно оставаться missing/unsupported/partial.
- Отдельный bounded actual-source adapter invocation с retained raw/receipt,
  facts/source-receipt artifact hashes, caps/diagnostics и before/after source
  binding; повторная projection из тех же bytes и проверка детерминированности,
  если это заявленное reproducibility acceptance.
- Независимое смысловое сопоставление extracted facts с owning API/schema/docs
  и accepted claims; наличие десяти fact classes не означает, что все values
  известны или верны для actual source. Render/link/native/scientific acceptance
  остаются отдельными gates и не выводятся из synthetic56/0.

Эти пункты — missing evidence для более сильных claims, а не blockers узкого
unit pass. Здесь actual-source calculation, parser rerun, docs build/render,
native или scientific проверка не выполнялись.

## Бюджет и итог

Выполнены только read-only source/receipt/raw reads, SHA/diff и ограниченная
постобработка existing tiny fixtures. Использована прежняя source-audit skill
дисциплина; imports/target parsers/runtime/harness/tests/build/network/server/
CI/solver не запускались. Никаких product/CP/Git writes или делегирования;
записаны только этот report и identity. Envelope≤10min/1CPU/1GiB/read1MiB/
report64KiB: conservative source-read bound≤980000B, report+identity<64KiB.
Actual CPU/RSS/physical I/O review-процесса не инструментировались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Final DOC06 synthetic unit56/0 принят | Raw56 unique ordered names + summary; complete receipt; final source hashes | Только exact test/tool/harness/fixture scope | сохранить |
| External symlink correction работает при узком scope | Both negatives ok после real9-byte witnesses; exact seed/source/guard bindings | Не hostile sandbox/security proof | сохранить |
| Original failures сохранены отдельно от E1 | Original raw/receipt unchanged; distinct E1 identity | История budget не сливается | сохранить |
| Actual selected9 sources воспроизводимы | Имеются лишь synthetic2260B trees и literal aaaa graph | Commit→bytes/actual projection evidence отсутствуют | данных недостаточно |
| Docs meaning/render/native/science приняты | Таких evidence в E1 нет | Software unit не закрывает эти gates | данных недостаточно |

STOP: узкий software acceptance передан координатору; новых действий/попыток нет.
