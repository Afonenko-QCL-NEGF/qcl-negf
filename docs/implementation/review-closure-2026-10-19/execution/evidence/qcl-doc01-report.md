# DOC01 — authored candidate для independent CP-CODE

Дата: 2026-10-19. Авторская роль: `gpt-6.1-sol`, `ultra`, по explicit task
brief/coordination capability. CP-DESIGN одобрен отдельным reviewer; CP-CODE
этот автор не закрывает. Никаких subagents, imports, environment setup,
docs builds, browser/server/native/scientific execution не выполнял.

Source: root `e0f244d075dd49874ba4f3847f4efa693f3b3622`, branch
`codex/review-closure-exec`. Первоначальный root был чистым, восемь direct
submodule revisions совпали с gitlinks. После начала появились чужие execution
receipts и Core/AiiDA diffs; автор их не менял и не принимал.

## Exact owning diff paths

1. `docs/system/README.md`
2. `docs/system/requirements.md`
3. `docs/system/comprehensive-review.md`
4. `docs/system/architecture.md`
5. `docs/system/release-roadmap.md`
6. `docs/system/requirement-dispositions-2026-10-19.md` (новый sanitized appendix)

Кандидат включает датированный override неизвестного выбора S01 через
P1/PERM15–17, truthful help DOC07 через PERM14 без повторного operator approval,
historical-only wipe/clean-install scope D04/D06/D07 с защитой persistent данных,
campaign-only operator cancellation после durable proof, все три backend и обе
required Windows machines. Historical П не превращается в принятый exact API.
Implementation/native/scientific evidence для каждого ID в DOC01 = unknown.

Исходные 59 строк requirements сохранили original text/status/acceptance cells;
добавлены только explicit ID anchors. Original `Q:Lnn` связаны с неизменённым
Git blob `e0f244d…:docs/system/requirements.md`, SHA256
`aaf01fe9b803a0aa34ba5ae9e71559606482e2ad96c3314388dc6c6667096e0d`.
Historical per-ID primary message locators unknown и не выдуманы. P1 call ID и
новая EXEC запись не выдаются за первичный provenance всех старых решений.

## Bytes и применение

- Author candidate patch: `/tmp/qcl-doc01.patch`, SHA256
  `0452d6f36e54fddf5b1504ad271bcedd0cac1ed021d21fa37075b9e752db9095`.
- Exact candidate files: `/tmp/qcl-doc01-candidate/` (шесть basenames).
- Full review package создан root, включая untracked appendix:
  `/tmp/qcl-doc01-review.diff`, SHA256
  `bfae8e75c3f3322bd5f0c5df038fb1a68d0c7ba7ad2dee46b6fa38765708eb06`.
- Per-file hashes и checks: `/tmp/qcl-doc01-check.json`.
- Candidate generator и static checker:
  `/tmp/qcl-doc01-author.py`, `/tmp/qcl-doc01-check.py`.

Первый native `apply_patch` был остановлен пользователем после ожидания
approval ~438s. Operation ID не был возвращён. Reconciliation показала пустой
diff и original requirements SHA256, т.е. частичная mutation не установлена.
После сообщения coordinator автор подготовил только `/tmp` candidate; root
выполнил exact-byte I/O в worktree. Автор проверил совпадение всех шести
native файлов с candidate и reverse-apply check. Patch повторно не применялся.
Коммитов/push этим автором нет.

## Реально выполненные checks

| Команда / check | Outcome | Предел |
| --- | --- | --- |
| `git rev-parse HEAD`, `git status --short`, `git submodule status --recursive` | e0f244d0, первоначально чистый root, восемь gitlinks совпали | Не live/import/native identity |
| `sha256sum docs/system/requirements.md` до mutation | original Q `aaf01fe9…` | После anchors текущие bytes закономерно другие |
| `git apply --check --whitespace=error /tmp/qcl-doc01.patch` до root I/O | exit0 | Applicability/added whitespace, не смысл |
| `python3 /tmp/qcl-doc01-check.py` final | exit0; 59 original IDs =59 appendix IDs в исходном порядке; original row mismatches0; Q line locators совпали;139 local links/anchors, missing0 | stdlib source/text only, не продуктовые imports/tests |
| `git apply --reverse --check --whitespace=error /tmp/qcl-doc01.patch` после root I/O | exit0; все6 native bytes =candidate | Не authorisation повторного apply |
| `git diff --check --` шесть owning paths | exit0 | Новая whitespace diff, не historical originals |
| `git diff --no-index --check /dev/null …/requirement-dispositions-2026-10-19.md` | exit1 как различие /dev/null; stdout/stderr пусты, whitespace defects0 | Untracked file проверен явно, обычный tracked diff его не включает |
| `git diff --name-only -- docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01` | пусто | Patch не меняет archive paths; полного повторного hash pass148 здесь не было |
| Final newline, trailing whitespace и balanced fenced blocks в шести candidate files | pass | Markdown source format; rendering/browser не проверялись |

Отрицательные результаты harness сохранены в tool transcript: первый запуск
checker читал already-applied current file вместо immutable original и получил
SHA assertion; исправлен на `git show e0f244d…:…`. Следующий checker ошибочно
запрещал существующую extra blank line at EOF, затем не учитывал normal exit1
у `git diff --no-index --check`; проверки исправлены без изменения candidate.
Final successful checker содержит явную проверку expected return code и пустого
whitespace output. Ни один из этих harness outcomes не был product test.

## Ограничения и next state

Смысл 59 dispositions требует independent CP-CODE. Не измерены implementation,
native/backend, runtime, physical/iteration/discretization outcomes. Exact APIs,
generator/pins, criterion bounds, resources/admission/READY принадлежат owning
tasks. Historical primary messages unknown. Никакие public release, wipe,
cancel или science права не выводились из этого текста.

Новые docs ссылаются на `execution/checkpoint.json`, принадлежащий coordinator
и пока untracked в source: перед публикацией сохранить этот receipt либо
согласованно скорректировать ссылку. Author не изменяет этот чужой файл.

Envelope: чтение bounded text без HDF5/распаковки; исходный 30min reading packet
и author checkpoint≤90min, включивший ожидание approval. CPU/RAM peak не
инструментировались и не выдаются за измеренный benchmark. Native mutating
tool больше не вызывался после указания parent. Corrective semantic rounds0;
independent CP-CODE — следующий шаг, не commit/push.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все59 requirements получили disposition | Original Q/59 ID equality, row mismatches0, appendix | Count не доказывает смысл; independent review ожидается | сохранить |
| Approved S01/help/backend scope сохранён | P1/PERM08/14–17 + DOC07/OPS13, датированные overrides | Нет API/native/scientific acceptance | сохранить |
| Historical wipe остаётся current default | D04 original против P1/PERM11–12, уточнения D06/D07/roadmap | Existing persistent данные защищены, destructive exception отдельно | изменить |
| DOC01 доказывает implementation/science | Только exact bytes и static checks | Для всех59 implementation/native/science =unknown | данных недостаточно |
