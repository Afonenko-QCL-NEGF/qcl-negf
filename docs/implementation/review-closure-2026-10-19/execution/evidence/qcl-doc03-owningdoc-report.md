# DOC03 — owning documentation candidate для независимого CP-CODE

Дата: 2026-10-19. Единственный writer изменил только
`docs/system/physics-documentation.md` в managed root
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Исходный checkout `/home/tolya/Загрузки/qcl-negf` не изменялся.
Staging/commit/push и другие Git mutations не выполнялись.
CP-CODE автором не закрыт; необходим отдельный reviewer `high`.

## Source и принятый scope

Published root: `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`.
Owning file был чистым и равен Git blob этого root, SHA256
`434ad2513188d52c915ea2de5dee92b4257711abad3e19d51be47f31f2b7da20`.
Foreign staged pointers/checkpoint/raw/runbook не затрагивались.
Новые component HEAD не подставлялись в датированную source basis.

Прямой источник переноса — exact D2:
`/tmp/qcl-doc03-design-v2.md`, SHA256
`01bd504b382062ad896280e58dca4588e67f725e5deb72f350eae99c91aca625`.
Independent CP-DESIGN PASS:
`/tmp/qcl-doc03-design-v2-review.md`, SHA256
`accfdda98914e3f1ab235b82cc5849d91af6d05bfa0561e610817e46eaf2555a`.
Восемь D1/D2/source/review/freeze inputs повторно сверены и остались неизменными.
Новых semantic/scientific/UI решений не принималось; DOC07 code не создавался.

## Exact body mapping

Перенесён единый D2 body от `## 2. Что установлено по source` до
`## 9. Handoff` (exclusive). Source observations, route alternatives, owners,
весь typed contract, R1/R2 corrections, limits, serving и controls сохранены.
Body восстанавливается побайтово из owning документа обратным применением
записанных heading/link/text mappings. Полная карта и hashes:
`/tmp/qcl-doc03-owningdoc-body-mapping.json`.

| D2 блок | Anchor в owning документе |
| --- | --- |
| §2 source facts | `model-help-source-facts` |
| §3 route alternatives | `model-help-publication-route` |
| §4 ownership | `model-help-canonical-sources` |
| §5 common format/types | `model-help-formats` |
| §5.1 bundle | `model-help-bundle` |
| §5.2 fragment | `model-help-fragment` |
| §5.2a reference/actual value origin | `model-help-value-origin` |
| §5.3 actor-enriched run view | `model-help-run-view` |
| §5.3a local snapshot/capture/mappings | `model-help-local-snapshot` |
| §5.3b retrieval/index/actor/retry retention | `model-help-retrieval` |
| §5.4 unknown/version compatibility | `model-help-compatibility` |
| §6 allowlist/pins/prerequisites | `model-help-build` |
| §7 serving/offline/light/UI | `model-help-serving` |
| §8 five negatives | `model-help-negative-controls` |
| D2 focused controls | `model-help-point-retry-controls` |

Контракт обёрнут одним разделом `model-source-help-contract`; headings получили
нужную иерархию и явные anchors. Ссылки `§2`, `§5.2a`, `§5.3b` заменены на
локальные named anchors. Вне этих mapping ровно четыре body substitutions:

1. Proposed format после CP-DESIGN обозначен принятым implementation contract;
   существующий Contracts API не заявлен.
2. «Новый capture ingress … этим D2» заменено «… этим контрактом».
3. Ссылка на общие invariants D1 заменена ссылкой на invariants этого контракта.
4. Удалены две operational строки о dirty/mismatched root; требование clean
   published source/checked gitlinks в prerequisites сохранено.

Абсолютные `/tmp` пути, author/review logs и source-status записи не перенесены
в owning документ. Датированный статус перед прежним текстом и короткий вводный
блок поясняют: CP-DESIGN разрешил implementation, а schemas/adapters/serving
и runtime/scientific acceptance пока не установлены. Source facts связаны с
root 9d8cf0c; прежний аудит относится к bce0aee и не объявлен новым current audit.

Все исходные bytes документа, включая 12 прежних headings, ссылки, обозначения,
формулы и историческую таблицу решений, сохраняются. Добавлены только эти два
статусных/вводных блока и transplanted technical body. Это проверено обратным
удалением добавлений при генерации и exact hash/mapping проверкой после записи.

## Выполненные проверки

- Exact D2 и PASS review hashes, восемь immutable input hashes.
- Полный transplanted body hash и обратное преобразование к exact D2 body.
- 16 явных anchors уникальны; 12 исходных headings сохранены.
- Проверены все локальные Markdown links/anchors: missing нет. External URLs
  проверены только по синтаксису; сеть не использовалась.
- `git diff --check -- docs/system/physics-documentation.md`: exit 0, без вывода.
- Read-only `git apply --check` перед записью и `git apply --reverse --check`
  после записи: exit 0. Patch соответствует текущим owning bytes.
- Owning документ не staged. Allowed diff path ровно один; автор не писал
  остальные repository paths.

Первый write потребовал sandbox escalation для managed worktree вне writable
roots. Automatic review разрешил точный уже проверенный owning-doc write;
отказов или новых пользовательских approvals не было. Запись ограничена одним
разрешённым файлом с проверкой baseline hash перед mutation.

Imports, установка, tests продукта/численные tests, docs render/build, browser,
network, native/server, CI и solver не выполнялись. Проверки — только
source/Markdown/links/diff/format. CP-DESIGN PASS не превращён в runtime pass.

## Frozen artifacts

- Owning file SHA256:
  `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`.
- `/tmp/qcl-doc03-owningdoc-patch.diff`, SHA256
  `86813476770580907c17fac00c2368404c518addab55fab4c9f8cfa1c6cddf6a`.
- `/tmp/qcl-doc03-owningdoc-identity.json`, SHA256
  `3c5bfc530e2fa2cea2ea13bd4d0545b8701ef3bcf600d2a6f539037c516f6575`.

Body mapping JSON — обязательный input отдельного CP-CODE; identity содержит его
SHA256, команды/checks и точные before/after file bytes. Generator script в `/tmp`
не является product code, не включается в публикацию и не требуется читателю.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Принятый D2 technical contract перенесён без semantic redesign | Exact reversible body mapping и восемь immutable hashes | Независимый CP-CODE ещё требуется | сохранить |
| Прежний текст, formulas, links и anchors сохранены | Original bytes retention + 12 headings, static checks | External link availability не проверялась | сохранить |
| Source/runtime/scientific statuses разделены | Новый implementation status, сохранённые unknown/controls/gates | Реализация и runtime controls не выполнялись | сохранить |
| Candidate готов к отдельному review | Owning hash, patch, identity, mapping | Commit/publication не выполнялись | дополнительно измерить |

**STOP после freeze.**
