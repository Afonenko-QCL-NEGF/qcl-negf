# DOC06 — independent high source/harness CPP

2026-10-20. **PASS_SOURCE_CPP** для frozen test
`ff6f0ec86be1ae7905721848998f8f7e7d22173d35534119f6102317e7fa8ec6` и harness
`1222d7d0a03dd39b72fc17be7029ced9e7422273f5ab08dbf48e6bd621f3014d`.
Блокирующих source findings к этой реализации не найдено. E1 не запускался,
не выделен этим review и не принят; original DOC06 2/2 остаётся исчерпанным.

## Предмет и источники

Primaries прочитаны до author implementation report. Дизайн D SHA256
`f21dcb464b17c8511eaed0bd60ff6b10722f9416e9005ae3849631f14924dcba`; independent
D_R `cae997412488ef7e1508a0c8920120d167f7c59b48047f387e354802506f065d`.
Использована ранее прочитанная qcl-physics-audit дисциплина source binding и
разделения evidence levels; scientific модель не меняется и не проверяется.

| Вход | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-doc06-worktree/tests/docs_static_slice_test.ts` | `ff6f0ec86be1ae7905721848998f8f7e7d22173d35534119f6102317e7fa8ec6` |
| `/tmp/qcl-doc06-local-unit-run-v2.py` | `1222d7d0a03dd39b72fc17be7029ced9e7422273f5ab08dbf48e6bd621f3014d` |
| `/tmp/qcl-doc06-worktree/ops/docs/static-slice.ts` | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| `/tmp/qcl-doc06-symlink-base-docs_static_slice_test.ts` | `382a881675093137e5b42563d17851114e4ffbe8217ba3ead4636999e39cc8c4` |
| `/tmp/qcl-doc06-local-unit-run-v1.py` | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |
| `/tmp/qcl-doc06-symlink-test-delta.patch` | `5aae29fd56abcc65f00df94c399736a09e5f4bad75a3fd74bcd98585bed1d14b` |
| `/tmp/qcl-doc06-symlink-harness-delta.patch` | `2406643c61bf928acc027ea19f7a927d44882fefc7f4930ee27a9371be51520f` |
| `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| `/tmp/qcl-local-julia-guard-v2.py` | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| `/tmp/qcl-doc06-symlink-impl-report.md` | `02c2909c2db67cd7f1f19a9f2c59ee2fe575e9347b76b4bfe1a91fdd3c8663e9` |

Read-only Git с `GIT_OPTIONAL_LOCKS=0` подтвердил managed Root HEAD
`469ef4ec36c1dfb967856108e5f9455429559c15`, прежние восемь gitlinks, dirty
coordinator checkpoint/census/evidence и untracked test/adapter. Ни Git state,
ни checkpoint, ни target source этим агентом не изменялись. Source authority
настоящего review — frozen bytes перечисленных файлов, не clean HEAD claim.

## Проверенные свойства

**Seed layout и namespace.** Harness:44–113 содержит ровно объявленные D
13 non-TMP nodes: 10 directory, 2 symlink, 1 empty regular file. Literal file
link text `../../../../backing/configuration_types.jl` имеет 42 bytes,
directory link text `../backing/core` — 15 bytes, сумма 57. Порядок создаёт
обычные parents перед file/link. `os.open(...O_EXCL,0600)` создаёт empty file;
directories0700; link targets не выводятся из caller/environment.

Harness:65–113 проверяет owner/mode/canonical real attempt/TMP, empty TMP до
seed, exact inventory no-follow, known types, exact readlink, strict target
realpath equality + `is_relative_to(temporary)`, ordinary target type, counts и
zero regular payload. Unexpected entry/type не рекурсируется. Специальные
файлы отвергаются по lstat до чтения содержимого. Нет удаления/reuse чужого
namespace или исправления seed. Ownership/admission/no hostile concurrent
mutation сохраняются external premises, не становятся sandbox proof.

**Child metadata boundary.** Test:209–253 начинает metadata observations с
TMP, затем только fixed fixture root/descendants. Не вызывает lstat/readDir
для `/tmp` либо attempt parent. Их проверки принадлежат launcher:26–27,65–70.
Inventory сравнивает observed type с exact expected до рекурсии; missing/fake/
wrong/dangling/outside/extra seed приводит к exception/test failure до negative
adapter call. `topology()` до и после prepare требует реальный symlink,
точный readLink и canonical target equality; backing ordinary file/directory.

**Healthy bytes и causality.** Test:254–278 использует unchanged
`Fixture.prepare()`, а затем actual Deno.readFile всех девяти selected aliases:
strict text, actual length и actual SHA сверяются с f.text/f.entries.
Каждый non-link selected leaf lstat regular. Direct backing выбранного source
читается отдельно и проверяется text/length/SHA, alias text также сверяется.
Это реальные filesystem witnesses, а не два hash от авторской строки.
File-case PATHS[0] и directory-case PATHS[8] проверяют leaf и ancestor topology.

Test:449–460 вызывает actual unchanged `f.run()` после witnesses и требует
refused + exact `symlink_or_invalid_source` в обоих случаях. Unchanged
Fixture.run сохраняет no-facts-on-refusal. NotCapable, generic io failure,
hash mismatch либо exception не удовлетворяет assertions. Adapter bytes
остались 3dde28…; выбранный в предыдущем source review `selectedPath`
walks lstat компонентов и даёт этот reason, `boundedRead` сохраняет отдельную
leaf protection. Эти проверки оценивают итоговую symlink protection; удаление
одной redundant проверки не обязано само по себе ломать тест, если защита
сохраняется другой.

**56 registrations и other54.** Независимый `diff -u` показал только private
helper insertion и замену bodies двух existing symlink negatives. Дополнительно
простое сравнение текста без target parser удалило из new только helper block
и из обоих файлов эти две named negative sections: остальные bytes совпали
точно. Все 29 literal `Deno.test(` registration sites и их строки совпадают;
literal loops/inputs не изменились. Поэтому исходные 56 registrations/names
сохраняются по source binding и старому raw denominator56. Это не fresh engine
count. Other54 bodies/assertions, fixtures, prepare, ordinary random path и
cleanup exact unchanged. В new нет `Deno.symlink(`, `Deno.rename(`, only/ignore
registrations. Helper сохраняет оба prepared trees при success/failure.

**Permissions/argv.** Harness:3–41,172 сохраняет exact2 code-file read paths +
ownTMP read/write, один TMP argument после `--`, no env/run/net/ffi grants и
прежние runtime flags. Единственный Popen, никакого child runtime fallback.
Сужение harness до DOC06/DENO/SYMLINK-E1 убирает недостижимые иные engines,
не расширяет полномочия. Local filtered env/cache-inside-TMP остаются v1;
future D1/D2 clearEnv/separate-cache этим локальным кодом не реализуются.

**Sampler и actual thresholds.** Harness:148–156 делает actual observation,
обновляет peak/count/phase и ставит reason при regular TMP>8MiB или wall>120s.
До seed и перед Popen:161–171 sampling включён; baseline0 проверяется, любой
reason блокирует child. Terminal observation:241–254 выполняется после drains
и также использует sample_temporary, поэтому fast child или terminal overrun
не получает exit0→pass. Этот reason входит final predicate:267. Exception
sampling/source binding превращается в guard_error/reason. Seed входит в wall
deadline. Existing RSS/output/termination/drain semantics сохранены.

Sampler source hash не менялся: real backing descendants обходятся однажды,
aliases не traversed/не double-counted. Baseline regular0 и link57 не выданы за
total fixture/cache/physical cost. Два tiny retained fixture trees, обычные
bounded serial fixtures и local cache лежат в том же measured TMP. Physical
allocation, hard quota и transient peaks остаются неизвестными. Реальное
runtime/cache consumption устанавливается только отдельным bound attempt.

**Failure retention и bounds.** Harness:158 открывает new original.log exclusive
до seed. Seed/prelaunch exception:193–198 фиксирует failed status,
child_started=false, failed_phase, elapsed; finally сохраняет raw/guard-error/
receipt без pass. Фиксированный seed section состоит из 13 finite observations,
fixed paths/link texts/four SHA bindings, finite numerical fields и небольшого
набора fixed phase/failure strings. До child и terminal:170,250 стоит encoded
≤8192 assertion; failure не включает arbitrary directory listing или exception
text внутрь seed, traceback лежит отдельно. Count/payload/regular0 возвращаются
только после actual validation. Частичная failed seed не объявляется prepared.
Ошибки диска при записи самого receipt остаются возможной unknown/failure,
не могут дать успешный final result; hostile FS mutation не предполагается.

**Source identity.** Harness:60–63 до seed pins adapter и наблюдает test/harness
hashes; terminal:243–248 сравнивает actual hashes со start. Receipt construction
использует уже сохранённые fields и не делает повторные uncaught source reads
при binding failure. Sampler/helper/runtime initial hashes фиксированы и
совпали с прочитанными артефактами. Это stability check, не самостоятельное
доказательство связи start test SHA с reviewed E1 plan: связь устанавливает Root.

**Attempt collision.** Harness:5–10 допускает только literal SYMLINK-E1;
folder.mkdir(exist_ok=False):28 запрещает повторное использование существующего
`/tmp/qcl-DOC06-SYMLINK-E1`, без удаления/repair. Независимое metadata observation
в этом review: directory отсутствует (`ls -ld` вернул ENOENT). Это наблюдение
не reservation; Root должен повторить fresh check перед отдельно выделенным E1.

## Обязательная граница перед E1

Это не source defect, но текущий запуск ещё не bound: harness:3 читает managed
Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, а reviewed test
пока находится в `/tmp/qcl-doc06-worktree`. В managed Root test сейчас имеет
старый SHA382a88…, что независимо проверено. Harness наблюдает start test SHA,
не pins ff6f0e… самостоятельно. Поэтому координатор должен сначала перенести
exact reviewed test bytes, подтвердить Root test=ff6f0e…, adapter=3dde28…,
harness=1222d7… и remaining helper/runtime/attempt bindings в finite E1 receipt.
Не запускать harness против старого test и не выдавать current CPP за эту
ещё не выполненную source promotion/binding.

Source CPP не выдаёт admission/authorization нового attempt. E1 не запущен;
original2/2 exhausted сохраняется. Любой future E1 outcome должен сохранить
original failures и STOP без автоматического rerun. Все S1 caps неизменны.

## Проверки, ограничения и решение

Выполнены bounded source reads, SHA256, diff, metadata ENOENT, read-only Git
и небольшое byte/text comparison. Не исполнялись target runtime, imports,
parser/typecheck/fmt/lint/tests/build, harness, сеть, server, solver или CI.
Source/code/checkpoint не менялись, делегирования нет. Только настоящий report
и identity записаны в `/tmp`.

Бюджет review≤15min/1CPU/1GiB/read2MiB/report96KiB. Консервативный total
source-read bound с повторами/ranges/hashes≤1MiB; report+identity<96KiB.
Actual RSS/physical I/O и CPU hard cap не инструментировались. Source PASS
не доказывает runtime traversal/write compatibility, actual 56/0 или measured
resource outcomes. Physics/convergence/discretization/experiment неприменимы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Implementation соответствует D и D_R | Exact seed, metadata/real9-file/backing witnesses, precise negatives; locators выше | Source-only CPP | сохранить |
| Остальные54 и56 names сохранены | Exact text remainder comparison + diff + unchanged registration sites/loops | Fresh engine count не измерен | сохранить |
| Prelaunch/terminal samples применяют guards | sample_temporary:148–156; prelaunch:161–171; terminal:241–254; final:267 | Sampled guards, без hard quota/peak proof | сохранить |
| Текущий managed Root уже готов запускать E1 | Root test ещё SHA382a…; harness root:3 | Нужны promotion/final binding и отдельное выделение E1 | изменить |
| Revised DOC06 успешно56/0 | Нового runtime receipt нет; original54/2 сохранён | E1 этим CPP не запускался/не разрешён | данных недостаточно |
| Actual Deno compatibility/resource outcome | Есть проверенный source recipe | Только отдельно bound E1 | дополнительно измерить |

STOP: report/identity координатору, без source promotion, checkpoint edits или E1.
