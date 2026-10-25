# DEV12 owning documentation — CP-CODE TEXT packet

Статус: **awaiting independent CP-CODE TEXT**. Автор D/ultra.
Принятый v2 technical contract перенесён в owning Portal docs; это не DEV13
implementation/runtime acceptance. Product code/tests этим автором не менялись.

## Immutable inputs и output

- Portal base `6ff9f6100623c578028506d43a39972dbfbc00dc`, branch
  `codex/review-closure-actor-lifecycle`, создана root coordinator.
- Accepted `/tmp/qcl-dev12-design-v2.md`, SHA256
  `fa3ca630f7b44ef9d72582ff91ced2e0c671f0986cecb4e20cddf5b294255712`.
- Independent CP-DESIGN PASS `/tmp/qcl-dev12-design-v2-review.md`, SHA256
  `e55a503c0a01bbfdd171d6681ff0299c614ea554bcb3c93e317b08fe273c3da5`.
- Frozen docs-only `/tmp/qcl-dev12-owningdoc-review.diff`, SHA256
  `8b8c00eb39d32ea6423ac68352b99c1f89ae210f0b9dc09397eb3101330f878b`,
  676lines/60885B. Includes tracked README patch and no-index new doc patch;
  no git stage/commit/branch mutation used.

| Owning path | Output SHA256 | Size |
| --- | --- | --- |
| `docs/actor-lifecycle.md` | `d824d97a1f6bdd99e7c6cce321e11b9773467242e5c7c359440e8eb8689b2376` | 648lines/57002B |
| `README.md` | `5cdbd01a34e700bcac4f2e5913e09e9c05e731d73b0a96b2f640e18b16bca0b8` | 179lines/21970B |

Writes в managed worktree выполнены только для этих двух файлов через
require_escalated exec, потому что worktree находится вне writable roots.
Approvals review разрешил обе записи; interactive human confirmation не
запрашивалась. Первая запись создала docs directory; вторая убрала только
найденную лишнюю EOF blank line. Принятый v2 и старые candidates не менялись.

Shared branch имеет concurrent separate DEV13 code/test writer. Последний
status показывал также `M tests/test_stream_disconnect.py` и untracked
`tests/test_actor_deadlines.py`; это не файлы и не изменения этого автора.
Frozen documentation diff не включает эти paths и не утверждает whole-worktree
freeze для их текущих bytes.

## Exact body mapping

Новый header/§1 формулирует accepted target, source observations baseline,
отсутствие runtime acceptance, physics/light boundaries. Исторический root
receipt, grants, `/tmp` paths, handoff traffic и review-round response исключены.
Техническое тело — accepted v2 §2–12 включительно, без нового поведения.

| Accepted v2 locator | Owning doc locator | Content |
| --- | --- | --- |
| §2 line54 | §2 line26 | observations, alternatives, one owner/mailbox |
| §3 line82 | §3 line54 | invariants |
| §4 line101 | §4 line73 | exact types/signatures/nullability |
| §5 line189 | §5 line161 | settings/defaults/domains/rationale/deadline source |
| §6 line222 | §6 line194 | actor state/admission |
| §7 line256 | §7 line228 | complete operation table |
| §8 line287 | §8 line259 | unknown/fence/reconnect/no cross-crash guarantee |
| §9 line333 | §9 line305 | actor artifact lease/disconnect |
| §10 line376 | §10 line348 | export lease/common close |
| §10.1 line430 | §10.1 line402 | deadline-aware old-lock admission/coalesced cleanup |
| §11 line554 | §11 line526 | HTTP mapping/headers/compatibility |
| §12 line595 | §12 line567 | owner/FS Event controls and all4ASGI cells |

Exhaustive 15 editorial substitutions recorded verbatim in
`/tmp/qcl-dev12-owningdoc-body-mapping.md`, SHA256
`34b2760f4823a5999546a5a1f93241e2c895bac5741d4fc63917e05bd7a97bba`.
Они меняют campaign-only labels candidate/DEV13/DEV09/DEV11/R1 на target-contract
wording и убирают ложный pre-CP-DESIGN статус names; технические решения не
меняются. Дополнительно удалена одна пустая строка на EOF, сохранён один newline.

Text verifier прочитал фактический owning doc, обратил **каждую** из15
декларированных замен (count1), нормализовал только final newline и сравнил
всё technical body с accepted v2 input. Итог exit0: byte-identical reconstructed
body. Это проверка переноса текста, не product/runtime test.

README narrow delta:

- line16: relative link `docs/actor-lifecycle.md`, accepted target и отделение
  implementation/fault verification от design.
- line132: cooperative callback behavior сохранено; целевой close `stopping`
  и actual writer/lease completion; timeout не означает backend/process stop.
- Другие README API/science/export sections не менялись; settings остаются
  в owning lifecycle doc, duplication существующей scientific policy нет.

## Фактически выполненные проверки и ограничения

1. Read-only HEAD/branch/status; Portal AGENTS/CONTRIBUTING/README; accepted v2
   и independent PASS receipt прочитаны. Branch не переключалась.
2. До записи built-in Python file-text transformation, без imports и без
   исполнения archive/product code; каждый exact replacement assert count1.
3. `cmp -s` owning doc/prepared text и README/prepared text — exit0.
4. Обратное exact-body comparison — exit0,15 replacements+EOF policy.
5. `git diff --check -- README.md` — exit0/no output.
6. `git diff --no-index --check /dev/null docs/actor-lifecycle.md` — exit1/no
   diagnostics: no-index new-file difference, не whitespace failure. Дополнительный
   text check подтверждает balanced fenced code и no trailing whitespace.
7. Первый format receipt был exit3 с
   `docs/actor-lifecycle.md:649: new blank line at EOF.` (tool chunk0b8acf).
   Удалена одна final empty line; current check повторён без diagnostics.
8. README relative target существует и читается; новых external links/anchors
   нет. Diff прочитан и содержит только два authorized documentation paths.
9. Scratch patch generation final exit1 — expected no-index new-file diff.

Tests/imports/build/install/SSH/solver/spawn/stage/commit/push=0. Численные,
ASGI, Event-fault и native backend проверки не выполнялись. Product behavior
можно принять только отдельным DEV13 CP-CODE на exact implementation source.
Текст не добавляет hard process-exit guarantee, durable idempotency, supervisor,
scheduler cancellation или новый scientific критерий. Existing light-only UI
и physics сохранены; визуальные surfaces эта docs task не меняет.

## Review question

На accepted v2/PASS и frozen docs-only diff проверьте: сохранён ли exact technical
contract без campaign-only assumptions и нового поведения; явно ли отделён
target от baseline; совпадают ли types/settings/states/HTTP/unknown/fence/cleanup/
all4ASGI requirements и README claims с accepted input; корректны ли paths/format?
Результат — отдельный CP-CODE TEXT, без tests/build/import/SSH/product writes.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning technical body соответствует accepted v2 | Exact reverse mapping exit0 и15-row map/hash | Independent CP-CODE TEXT ожидается | сохранить |
| README отражает target и truthful deferred cleanup | Два review diff hunks, relative target read | Не runtime acceptance | изменить |
| Документ различает baseline/design/runtime | Header/§1, exact v2 limitations и fault requirements | DEV13 implementation отдельно | сохранить |
| Только authorized docs изменены этим автором | Two-path immutable diff, no staging/Git mutation | Shared writer отдельно меняет tests/code | сохранить |
