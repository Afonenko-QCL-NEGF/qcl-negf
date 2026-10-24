# DEV07 I1 → v2: E1/E2 errata, source/comment only

2026-10-19. Основание: independent CP-CODE source/math PASS
`/tmp/qcl-dev07-absolute-code-review.md`, SHA256
`169a8563adb1693d0f93f8626187349f0f21596a79d46a3d9309c6f284af3e11`,
и bounded checkpoint `/tmp/qcl-checkpoint-SCI05-N1-E5-DEV07-errata.json`.
Это один разрешённый errata pass; functional assertions/helpers/formulas,
physics, gamma_n и tolerances не изменялись.

**E1.** Исправлены только полные строки комментариев test inventory и
соответствующий prose/table block в appended DEV07 subsection. Перенесены
точные независимые conservative ceilings reviewer: LO744, IFR544,
acoustic268, alloy280; все <992<1024. LO denominator явно считает три
squares и два adds; 19 real operations в qz block ограничиваются24.
Иные executable bytes test не менялись.

Побайтовое свидетельство: сохранён I1 test
`/tmp/qcl-dev07-absolute-i1-test-byteproof.jl` с original SHA256
`b85514cab4c32cb22acef0b0ecd66d070beb0ec6d44949d64a0ca20a171e96af`.
Из before/after удалены только полные строки с префиксом
`^[[:space:]]*#` через sed; `cmp` вернул0. SHA256 обоих retained functional
текстов одинаков:
`e0aa8a0358102fa89bf2ede8acd38584b3297c565c47dc524366ec166049e9c2`.
Ручной exact diff подтверждает единственный comment block; stripped bytes
не выдаются за Julia parse/runtime test. Полный narrow errata diff:
`/tmp/qcl-dev07-absolute-impl-v2-errata.diff`, SHA256
`8871389eca0668381239554eb5c025acf3637a9c0105dadafce756b9d3439717`.
Docs изменены только в appended inventory paragraph/table.

**E2 — отдельный provenance erratum.** Root `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`
в original I1 identity обозначает historical D1/read context. Время того
original author root observation неизвестно; его нельзя отождествлять с
I1 `frozen_at_utc=2026-10-19T18:20:02Z`. Original I1 metadata не переписаны.
Свежий фактический `git rev-parse HEAD` root дал
`cfc38e1761f24caf436d938f378dbcdbf71a28f0`; timestamp readback command
`2026-10-19T18:26:51Z`. Core source HEAD и root HEAD gitlink одинаковы:
`7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`.
Root dirty status/submodules дополнительно сохранены read-only в
`/tmp/qcl-dev07-absolute-impl-v2-root-status.txt` и
`/tmp/qcl-dev07-absolute-impl-v2-submodule-status.txt`.

Original I1 report/identity/patch сохранены byte-exact, SHA256 повторно
совпали: report `db33af90259a022ffa89a5f1832800463e7497d86a07c848f650b8ee23ae5a64`,
identity `e4ddbb67f1a6202a0e142abe0012ab1f1182ca2952f0ae1f6fc52999a4a0f499`,
patch `561d2a3643ad95be37e50bb76dd9a86e388386e419ced4744427d387c67f7316`.

Новый пакет `/tmp/qcl-dev07-absolute-impl-v2-{report.md,identity.json,patch.diff}`.
Source/patch hashes в v2 identity. Whitespace checks tracked diff/new test
прошли. Imports/Julia/parser/tests/build/network/server/Git
stage/commit/push/children не выполнялись; runtime counter остаётся0/2,
SCI05 и protected original не затронуты. Ресурсный cap10min/1CPU/1GiB,
read1MiB/output32KiB не расширялся; точный OS I/O не измерен.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| E1 inventory уточнён без functional changes | Exact comment diff и cmp stripped bytes0 | Не runtime receipt | сохранить |
| E2 historical/fresh root context разделён | Fresh cfc38e1 readback + timestamp; same Core7324 | Время old observation неизвестно | сохранить |
| I1 freeze сохранён | Три исходных SHA256 совпали | Отдельный v2 не заменяет raw history | сохранить |
| Runtime/scientific PASS | Свидетельств нет | Нужны отдельные gates | дополнительно измерить |

**STOP frozen:** дальнейшие exactdiff review и подтверждение independent
reviewer принадлежат координатору перед local BIND. Никакого нового runtime.
