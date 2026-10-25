# DOC06 — независимое high review external symlink preparation D

2026-10-20. Verdict: **PASS_SOURCE_DESIGN**. Блокирующих замечаний к frozen D
`f21dcb464b17c8511eaed0bd60ff6b10722f9416e9005ae3849631f14924dcba` не найдено.
Это принятие узкого source-дизайна для последующего writer/CPP, не принятие
revised implementation, runtime, engineering E1 или scientific результата.

## Граница и identity

Выполнено только чтение выбранных исходников/документов/старых receipts,
проверка SHA256 и запись настоящего review с identity в `/tmp`. Target runtime,
imports, parser, typecheck, tests, build, сеть, сервер, solver и full CI не
запускались. Исходники, v1 harness, sampler, original GREEN и sole checkpoint
не редактировались. Вложенные агенты не создавались.

Selected checkout: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`;
наблюдаемый HEAD `469ef4ec36c1dfb967856108e5f9455429559c15`. Это контекст,
а selected test/adapter являются dirty untracked source overlay и привязаны к
байтам ниже. Наблюдаемый `git status --short`: untracked test/adapter; изменения
checkpoint/census и дополнительные review/evidence artifacts принадлежат
координатору; `components/qcl-negf-contracts` имеет untracked содержимое.
Gitlinks прочитаны через `git submodule status --recursive`; ни один не
обновлялся. Git-команды были read-only по назначению; первые команды запущены
без явного `GIT_OPTIONAL_LOCKS=0`, поэтому не выдаю это за forensic proof
отсутствия optional index refresh. Следующие административные чтения должны
пользоваться этим флагом. Изменений Git refs/index мной не запрашивалось.

| Первичный вход | SHA256 |
| --- | --- |
| `/tmp/qcl-doc06-symlink-preparation-design.md` | `f21dcb464b17c8511eaed0bd60ff6b10722f9416e9005ae3849631f14924dcba` |
| `/tmp/qcl-doc06-local-unit-run-v1.py` | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |
| `tests/docs_static_slice_test.ts` | `382a881675093137e5b42563d17851114e4ffbe8217ba3ead4636999e39cc8c4` |
| `ops/docs/static-slice.ts` | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| `/tmp/qcl-owned-temp-sampler-v2.py` | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| `/tmp/qcl-DOC06-GREEN-1/original.log` | `3cae707b9a921a38e820cbb83ca0c7a73437048ed7b86fce27ae803b7d854b54` |
| `/tmp/qcl-DOC06-GREEN-1/receipt.json` | `2b058e3083a35824321936074e58db5f2f328dee0954bbbc97428c3a164c4fa1` |
| `/tmp/qcl-docs-test-routing-design-v2.md` | `bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70` |

Все перечисленные SHA проверены локальным `sha256sum`, а не перенесены только
из author identity. Architecture, Root AGENTS, canonical review workflow,
role policy и qcl-physics-audit прочитаны как инструкции source-аудита;
физические уравнения не являются предметом этого инженерного изменения.

## Независимая цепочка свидетельств

1. **Наблюдение:** original GREEN действительно имеет 54 passed/2 failed.
   Raw errors указывают `Deno.symlink` в test:382 и test:388; `f.run()` находится
   после этих statements. Receipt имеет exit1, complete capture, null guard/stop.
   Следовательно, эти два результата не проверили adapter и не являются его
   отрицательным verdict. Изменение fixture preparation причинно адресует именно
   этот prerequisite. Старый failed результат должен оставаться failed.

2. **Вывод о namespace:** D:35–78 задаёт два literal prepared roots в новом TMP,
   реальные parents и backing targets. Относительный file target из
   `snapshot/runner/src/application` поднимается на четыре уровня к fixture root;
   `../backing/core` из snapshot — к directory fixture root. Оба разрешаются
   внутри того же TMP. Размеры текстов 42+15=57 UTF-8 bytes; layout содержит
   10 directories, 2 links и 1 empty regular file, всего 13 non-TMP entries.
   Exact inventory + no-follow types + exact link texts + strict canonical target
   equality исключают ordinary fake links, dangling/wrong/outside target и
   unexpected special files до child. Ownership/no concurrent hostile mutation
   остаются явными premises, metadata не объявляется hostile sandbox proof.

3. **Вывод о capabilities:** внешний launcher использует собственный os.symlink,
   future parent — уже принятые global read/write D1 capabilities. Child не
   вызывает symlink/rename и получает прежние два code-file read paths, TMP
   read/write, один positional TMP argument, без env/run/net/ffi. Весь alias и
   target namespace помещается внутрь этого read/write domain. Это согласованный
   source-дизайн; совместимость actual Deno traversal/mkdir/write/realPath со
   scoped grant здесь не измерена и остаётся свойством E1.

4. **Вывод о causality:** test:134–170 `Fixture.prepare()` пишет literal bytes и
   строит entries из них. D:89–106 требует проверять topology до prepare,
   сохранённый symlink после prepare, alias/backing byte identity, SHA/length
   всех девяти selected sources до adapter. Значит, missing/hash-corrupt fixture
   или permission accident не заменяет symlink-negative. Adapter:221–235
   `selectedPath` проверяет lstat каждого компонента; leaf-file и ancestor-core
   cases соответствуют разным topology paths. D:107–111 требует actual
   `f.run()`, refused и точный `symlink_or_invalid_source`; adapter:1063–1116
   независимо проверяет snapshot/receipt/output/source identity. Existing
   `Fixture.run()` сохраняет отсутствие facts.json при refusal. Generic I/O
   refusal, NotCapable или exception не удовлетворяют критерию.

5. **Вывод о retention/accounting:** D:112–116 оставляет оба дерева, остальные
   54 cases сохраняют прежний cleanup contract test:196–211. Sampler source
   `sample_owned_temporary_bytes` использует entry.stat(follow_symlinks=False),
   суммирует только regular st_size и не спускается через directory symlink.
   Оба backing находятся в обычных descendants TMP: file bytes и directory
   subtree попадают в сумму один раз через backing, aliases не дают дубликата.
   D:151–171 честно различает baseline regular0, 57 link bytes и неизвестные
   physical/inode/cache costs. Seed и terminal samples закрывают очевидный
   пропуск fast-child; их значения должны участвовать в guards, см. CPP ниже.

6. **Вывод о failures:** D:64–78,89–93,135–149,210–217 требует fail closed до
   negative assertion/spawn при collision, missing/wrong seed, metadata/type/
   permission failure; без fallback, удаления чужого дерева, skip и повторной
   попытки. Новый raw открывается exclusive до seed; seed failure имеет
   child_started=false и отдельные preparation evidence. Неудачное создание
   собственного attempt directory нельзя чинить reuse чужого attempt.

7. **Вывод о future helper:** D:177–202 является узким unit-mode override,
   который не меняет D1/D2 descriptor/schema. D1:46 уже предоставляет parent
   global read/write; D1:141–154 задаёт прежний child scope. D2 §4 сохраняет
   clearEnv=true и единственный DENO_DIR с отдельным admitted cache; local v1
   filtered env/cache-inside-TMP не переносится молча. D2 count связывается с
   новым final test SHA и 56 registrations; старый source SHA после правки не
   является binding. Preflight не делает скрытый seed/runtime probe и не
   выдаёт подготовку за выполненный unit pass.

## Условия последующего source/harness CPP

Следующие пункты — обязательные проверки соответствия уже сформулированному D,
а не дополнительные runtime попытки и не блокирующие findings к этому D:

- Child helper проверяет ancestors **внутри TMP**, начиная с canonical TMP и
  спускаясь к prepared nodes. Проверка `/tmp` либо parent attempt directory
  через child lstat/readDir потребует чужой scoped capability и недопустима.
  Проверка внешних canonical ancestors принадлежит launcher по D:64–71.
- Exact seed inventory проверяется no-follow; special files отвергаются до
  чтения их содержимого. Перед child topology имеет ровно объявленные nodes;
  после prepare каждый non-link selected leaf остаётся regular и healthy.
- SHA/length witnesses используют actual read bytes всех девяти files и
  соответствующие f.entries; нельзя сравнивать только два вычисления от f.text.
  Link/realPath assertions реально исполняются перед отрицательным adapter call.
- Prelaunch seed sample и terminal sample обновляют max/count **и проверяют
  threshold**. Если prelaunch wall deadline уже истёк или bytes>8MiB, child не
  стартует; terminal overrun не даёт exit0→pass. Само добавление receipt fields
  недостаточно. Возможность guards и finite aggregate payload/cache должна быть
  подтверждена source CPP; sampled guard не становится hard quota.
- Revised hashes фиксируются до E1 и проверяются на стабильность; adapter
  остаётся byte-exact. Other54 bodies/assertions, registrations, limits,
  drain/error handling и failed raw остаются неизменны. Нельзя выдать удаление
  одной из нескольких защит adapter за обязательный mutation-test failure:
  leaf boundedRead также independently запрещает symlink; invariant — итоговая
  невозможность принять такой source.

Runtime controls здесь не выполнялись. Исчерпанный original DOC06 2/2 не
расширяется. E1 должен иметь отдельный human grant/binding, source/harness CPP и
новую attempt identity; этот PASS_SOURCE_DESIGN сам не разрешает и не запускает
E1. Все S1 caps и science/CI/server exclusions сохраняются.

## Ограничения и бюджет

Review source-only, независимый от автора D по выполнению анализа; использовал
авторский текст D как предмет, а не как oracle. Нет runtime или adversarial
namespace proof. Полнота physics gates/сходимость/дискретизация/эксперимент к
этому scope неприменимы и не получали pass. Source-read conservative bound
включая repeated/ranged/hash reads: ≤1MiB, ниже 2MiB grant. Report+identity
значительно ниже 96KiB. Wall grant≤15min; тяжёлых процессов не было; CPU/RSS
не измерялись как hard caps и не заявляются измеренным результатом.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| External seed сохраняет узкий child scope | D:35–111; v1 argv; test Fixture.prepare; exact internal targets | Actual Deno traversal не измерен | сохранить |
| Leaf/ancestor negative имеют различающую causality | Topology/9-file healthy witnesses + precise refusal; selectedPath/Fixture.run | Revised code ещё не написан и не прошёл CPP | сохранить |
| Seed failure/retention/sampler спроектированы достаточно | D:64–78,112–171; sampler no-follow source | Нужно проверить guard application в final CPP; physical peaks неизвестны | сохранить |
| Revised DOC06 имеет 56 passed | Нового runtime receipt нет; original 54/2 сохранён | Original2/2 исчерпан; E1 этим review не разрешён | данных недостаточно |
| Actual runtime compatibility и guards выполнены | Только source design | Отдельный bound E1 после CPP | дополнительно измерить |

STOP: отчёт и identity передаются координатору; checkpoint и target source
остаются его ответственностью.
