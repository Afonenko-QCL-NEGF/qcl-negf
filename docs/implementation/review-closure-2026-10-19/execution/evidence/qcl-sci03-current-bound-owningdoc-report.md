# SCI03 §5.3 — owning Research documentation transfer

2026-10-19. D Sol ultra; source-only docs transfer. **READY FOR SEPARATE HIGH CPP;
STOP FREEZE.** Это отчёт автора, не независимый CPP и не разрешение на Results I,
runtime, native/scientific acceptance.

Принятый D SHA256 `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7`;
CP-DESIGN high R SHA256
`fa1311a4bf16f08f6e417590b77b7e6179aa9320907934fbd4496ebc059ca4a9`.
Оба исходных файла сохранены; hashes повторно совпали после переноса.

Создан отдельно разрешённый Git worktree Research:
`/tmp/qcl-sci03-current-bound-doc-worktree`, branch
`codex/review-closure-current-bound-contract`, HEAD/base
`1eacefcd81a50e245ea9da74a0b717b33818c61e`.
Baseline `git status --short` был пуст; recursive submodule status пуст (standalone
Research не содержит submodules). Source checkout Research в integration root и
protected original checkout не редактировались. Git escalation для worktree add
была принята. Stage, commit и push не выполнялись.

Единственный owning diff — `docs/equilibrium-measurement-contract.md`: +439/−0.
Добавлен appendix «Дополнение к §5.3» вне прежних reviewed-body markers:
A.1 theorem/weights/units/signs; A.2 dataset/identity prerequisites; A.3 exact
additive namespace/status/null/near-zero contract; A.4 twelve streaming norms,
finite workspace/I/O/report guards; A.5 literal noncommuting complex 2×2
positive/negative oracle и finite-t table; A.6 границы будущего I/R.

Формула, original criteria, S1 model/all-five/e–e none, field/window/grid,
scientific tolerances, unknown εJ_abs/H и uncertainty interpretation сохранены.
Новых API signatures, scalar definitions, fixture values или scientific решений
не введено. Report fields и resource allowances перенесены из принятого D.
Три неблокирующих уточнения R сохранены: old fields/semantics без обещания
битовой идентичности после tile adaptation; independent μ bracket/status/stop
checks; actual operation-chain/libm check для fixture policy 512u. Уменьшение
tile не выдаётся за byte-identical actual I/O.

Operational /tmp paths, historical root dirty state/source observations,
текущий C08 consumption и author/reviewer resource receipts в product text
не копировались. Public appendix явно помечен **target, not implemented** и
не переносит physical acceptance в UI/scheduler. Дословные theorem/report/
streaming fragments и все adaptations перечислены в body-mapping.json.
Четыре literal modulus/norm table cells экранированы для Markdown; math не менялась.

Проверки документации:

- `git diff --check`: exit0, без whitespace errors.
- `git diff --numstat`: 439 additions, 0 deletions, ровно один owning path.
- SHA256 первых 45385 bytes target равен полному baseline SHA
  `758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f`.
  Это сохраняет прежний reviewed body, preamble, anchors и исходные links
  буквально. BEGIN/END markers остались на строках17/428.
- Mechanical `diff -u` D:33–116↔target:474–557,
  D:204–279↔target:596–671 и D:283–336↔target:680–733 не показали различий.
- Проверены headings A.1–A.6, парность 30 fence lines и literal table escaping.
  Новых Markdown links/URL нет; старые preserved prefix. Network URL checking,
  rendered docs build и target parser не запускались.
- Final HEAD/branch повторно проверены; final status — только modified owning
  document. Staged diff, commits, pushes и consumer Results edits отсутствуют.

Frozen owning file: 78562 bytes, SHA256
`61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c`.
Frozen patch SHA256
`c99fd8c983caaed04239cc20b58c9480fb992316f5fdff1d9136395c114bfbfc`.

Выходы:
`/tmp/qcl-sci03-current-bound-owningdoc-report.md`,
`/tmp/qcl-sci03-current-bound-owningdoc-identity.json`,
`/tmp/qcl-sci03-current-bound-owningdoc-patch.diff`,
`/tmp/qcl-sci03-current-bound-owningdoc-body-mapping.json`.
Deliverable report/identity/patch/mapping суммарно остаются в64 KiB; полный
owning file включает preserved45385-byte baseline и33177-byte additive text.

Envelope этого переноса: ≤20 min/1 CPU/2 GiB, source reads≤3 MiB/output≤64 KiB.
Читались известные text files/ranges, D/R, Git metadata и hashes; repository-wide
source-content scan не выполнялся. Точная filesystem-byte telemetry, включая
Git checkout I/O, отсутствует: read-byte cap не объявляется ретроспективно
измеренным. Исходный D/R read-cap receipt gap сохранён и не исправлялся прозой.
Imports/target parsers/tests/HDF/Julia/solver/build/network/server/children=0;
C08 consumption=0. Численные проверки не выполнялись: задача docs-only.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Принятый technical contract перенесён в owning Research | D/R hashes, body-mapping, exact-fragment diff | Авторская проверка; отдельный high CPP ещё нужен | сохранить |
| Старый body, anchors, model/criteria сохранены | +439/−0; prefix SHA равен baseline | Нет runtime/renderer проверки | сохранить |
| Results instrumentation реализована и проверена | Изменён только Research document | Consumer owning I/M1 впереди, не заявлен pass | данных недостаточно |
| Runtime/science READY получены | Только source-only documentation transfer | Native arrays/admission/accuracy/H неизвестны | данных недостаточно |

Coordinator выполняет отдельный high CPP, затем publication Research PR и
отдельный consumer Results M1/I. Этот агент ничего не stage/commit/push/submit.
**STOP FREEZE.**
