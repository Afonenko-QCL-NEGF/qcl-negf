# DOC07 C1: source-only schema handoff

Изменён только новый owning resource `/tmp/qcl-doc07-contract-worktree/src/qcl_negf_contracts/schemas/model-help.schema.json` (28857 bytes). Base Contracts `12fc26462bbab3df76904c6deb01f8c6596de7be`, branch `codex/review-closure-model-help-contract`; submodules отсутствуют. Initial/final status: существующий untracked `tests/test_model_help.py`; после работы дополнительно untracked schema. Test file SHA256 неизменён: `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd`.

Canonical DOC03: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/system/physics-documentation.md`, SHA256 `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`. Frozen design `/tmp/qcl-doc07-contract-plan-v2.md`, SHA256 `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b`. Реализация выведена из этих нормативных исходников; contents теста не читались, файл только хеширован.

Schema SHA256 `cbca63eac4ce22ece53e5275b5ce458508edf9ab1d467aad28d9a8348534a3a0`.
Full patch `/tmp/qcl-doc07-C1-schema-full.patch`, SHA256 `ede3357bdbbf265aadb06064b0cc38d69f01c48c286094777ed3de1f4d8e1987`.
Identity JSON `/tmp/qcl-doc07-C1-schema-identity.json`.

## Contract locators

- DOC03:324–360: Draft 2020-12 resource, closed objects, shared SHA/Id/refs/Origin/Atom/Fact forms.
- DOC03:366–406: Bundle/Fragment complete inventories, generator pins (source facts:226–228), ten Fact coverage via independent contains constraints; repeated contexts разрешены.
- DOC03:412–450: ReferenceValueOrigin, applicability, ValueOriginView/Binding, origin claim/assignment receipt/condition objects.
- DOC03:504–538: selected-child View context, inputs, declared/used states, assigning/effective origin, Evidence.
- DOC03:556–574: local Snapshot context and raw input forms без API identity/Evidence/value_origin fields.
- DOC03:619–637: detached Index exact entries/status/reason/path grammar; bytes не ограничены 64KiB, чтобы сохранить oversized invalid entry.
- DOC03:663–675: actor UUID/attempt mandatory, typed input_status.
- Canonical clarification:978–1036: R1 repeated Fact contexts; R2 Origin/Atom/ValueOriginView matrices; R3 Binding/input_status reason and fragment-null matrices, independent identity retention.
- Canonical clarification:1038–1084: R4 retained mapping, R5 query-free public reviewed locator policy, R6 private semantic helper; C1 не выдаёт их proof по schema validity.

## Source decisions and limits

Top-level oneOf использует пять exact format discriminators. Каждый concrete object закрыт additionalProperties:false; reusable conditional/ref wrappers не закрывают поля повторно. Все refs локальны, loader/__init__.py неизменён. Разрешены truthfully available/ok+inputs=[] и unbound fragment=null при сохранённых known identity scalars. Effective chain known не определяется cardinality evidence. URI prefix проверяется только синтаксически; URI parser/query-free/provenance policy принадлежит C2. Normalized safe path checks, keyed uniqueness, graph equality, dynamic fragment id/file/url/hash equality, retained mapping, source/release/origin proof и byte caps остаются semantic/owning boundaries; они не считаются пройденными.

Выполнены read-only Git/text/hash и source writes; `git diff --no-index --check /dev/null <schema>` завершился 1 (no-index сообщает наличие нового файла), diagnostic output пустой; замечаний whitespace нет. JSON/parser/import/eval/tests/build/network/solver не запускались, runtime slots не израсходованы, commit/PR отсутствуют. Проверка синтаксиса JSON и Draft202012Validator остаётся за Root после independent high CPP. C2 не реализован. Научная корректность, сходимость и experimental acceptance не проверялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| C1 resource реализован по frozen contract | Schema/patch hashes, нормативные локаторы выше | Source-only, без parser/schema runtime | изменить |
| Fixtures сохранены без изменений | Exact approved test SHA256 совпадает | Тесты не читались и не исполнялись мной | сохранить |
| Runtime принятие C1 пока неизвестно | Только source whitespace check без diagnostics | Нужны independent CPP и Root-only GREEN | дополнительно измерить |
| Source/release/context/origin binding нельзя выводить из schema validity | DOC03:452–475,643–661; clarification:1038–1084 | C2 остаётся отдельным этапом | данных недостаточно |
