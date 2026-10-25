# DEV23 — README cancellation semantics

Этап: точечное authored documentation по готовому контракту, без изменения API или поведения.
Owning component: `qcl-negf-aiida`. Единственное изменение в managed worktree:
`components/qcl-negf-aiida/README.md`, раздел `Cancel a run`, строки 159–179.

## Исходная identity

- Managed root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
- Component branch: `codex/review-closure-cancellation-contract`.
- Component HEAD из задания координатора: `5579d55684939495230241f446b7ea07c8ae0224`.
- Git HEAD/status/gitlinks агентом не запрашивались: root executor является единственным Git writer и ведёт source receipt. Указанный HEAD не выдаётся за самостоятельно снятый.
- Frozen service candidate SHA256 повторно проверен: `5f7e9b28f9007255e3de319fff43e48143d4c23a9c9487164ecda92ebac8c762`.
- Frozen cancellation fixture SHA256 повторно проверен: `8b276505d190811526bd6d308acb09bf0b00317c36be14a92861236141204809`.
- Прочитаны root AGENTS/architecture, component CONTRIBUTING/README/service API, development.md::DEV23 и применимые role/entrypoint sections.

## Изменение

Добавлен краткий английский раздел с существующим `kill_run(run_uuid)` и примером наблюдаемого `finished`, с локальными ссылками на service API, `service.py::kill_run` и `workflow.py::attempt_decision`. Кодовых блоков, исполнимых примеров, новых endpoint или диагностических команд не добавлено.

Раздел описывает refreshed terminal parent summary без fabricated `killed`; already-terminal fast path; public-safe `RuntimeError` при daemon/check/dispatch/refresh/unconfirmed failure; unknown cancellation, отсутствие auto retry/resubmit и второго submit после lost acknowledgement; сохранение initial lookup semantics. Native all-process/Slurm proctrack stop и final staging/recovery receipt оставлены отдельными OPS gates. Finite retry limits, eligibility rules, immutable plan/attempt markers и `--no-requeue` сохранены.

## Статические проверки

Выполнена stdlib text/hash проверка без импорта owning Python package:

- После удаления вставленного раздела README совпадает с исходным файлом побайтно по UTF-8 тексту; иных правок README нет.
- Все три добавленные локальные ссылки разрешаются в существующие файлы; `kill_run` и `attempt_decision` найдены как source symbols.
- `#SBATCH --no-requeue` и `qcl-negf-attempt-v1:` найдены в неизменяемом для этого агента `calculation.py`.
- Нет trailing whitespace; сохранены terminal newline и число Markdown fences.
- Повторные service/cancellation-test SHA256 совпали с frozen identity.
- Patch построен стандартным unified diff от исходного README; проверен полный добавленный hunk. Объём patch меньше 32 KiB.

Выполнение статической проверки: exit 0. Markdown rendering, удалённые URL и runtime semantics этой проверкой не установлены. Imports AiiDA/проекта, tests, daemon/profile, solver, Slurm/native cancellation, server/network и Git не выполнялись. Научное окружение не поднималось, численные проверки не выполнялись. Независимый review и bounded tests остаются у root executor; этот отчёт не выдаёт их за пройденные.

## Frozen output

| Артефакт | SHA256 | Bytes |
| --- | --- | ---: |
| README before, `/tmp/qcl-dev23-readme.before.md` | `0cfb04d64e01def176ab946c4b7740cb0c995287f20abc8c649e5f6cbb0b7486` | 10972 |
| README after | `490e49b686047d45d64b20f61984506bd3d48dd8c8f1227d6477a4b7f6ab96fb` | 12261 |
| `/tmp/qcl-dev23-docs.patch` | `bdc75ea725e966f8e82c3ce4f8c45f4598cbe70adee1b25f2ce9be8f46335c6f` | 1631 |

SHA256 самого отчёта публикуется отдельно в `/tmp/qcl-dev23-docs.sha256`, чтобы не создавать self-hash.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| README описывает готовый truthful parent-state contract | Frozen `service.py::kill_run`, SHA256 выше; README `Cancel a run` | Runtime тесты агентом не выполнялись | изменить |
| Действующие retry/immutable submission boundaries не расширены | Только README insertion; `workflow.py::attempt_decision`; `calculation.py` markers | Самостоятельный Git diff/status не снимался | сохранить |
| Parent summary не закрывает native-stop/staging/recovery gates | DEV23 interface/stop; явная оговорка README | Реальные OPS receipts отсутствуют в этом scope | дополнительно измерить |
| Нужные ссылки/format проверены | Три локальных file links, source-symbol и whitespace/fence checks, exit 0 | Rendering и remote URLs не проверялись | сохранить |

После создания frozen artifacts автор останавливается; публикации Git/PR этим агентом нет.
