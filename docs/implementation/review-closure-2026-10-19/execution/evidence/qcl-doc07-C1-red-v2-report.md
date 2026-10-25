# DOC07 C1 RED-source v2: corrective cycle 1

Закрыта source-strength проблема R1 из independent high review
`/tmp/qcl-doc07-C1-red-review.md`, SHA256
`412d4bdaef6aed837faad9748f77b04b7215f00d2cf7b5a389fa69b8df4ca0d2`.
Три cap+1 negative rows теперь уникальны, поэтому duplicate rejection не может
маскировать отсутствие соответствующего maxItems:

- fragments: после pilot.0…255 добавляется pilot.256 с file help/fragments/pilot.256.json;
- View inputs: после physical.public_leaf_0…31 добавляется physical.public_leaf_32;
- Index: после P-0…P-9999 добавляется P-10000 с соответствующим новым logical path.

Здоровые base templates и остальные поля сохранены. Conditions-cap control
не изменён: его appended pilot.condition уже отличался от pilot.condition-0…11.
Это source reasoning по конкретным данным; executed mutation result не заявлен.

Также выполнена явно предложенная неблокирующая coverage рекомендация high R:
новый `test_all_accepted_fact_statuses` параметризует inputs/api и ровно пять
принятых Fact.status (`known|partial|unknown|not_assigned|not_applicable`). Каждый
positive проходит через validator и имеет paired invalid status=pass control.
Новых условий смысловой согласованности status/text/sources не вводится.

v2 source — 637 строк, 31628 bytes, 29 test functions (source count, не collection).
Owning HEAD остаётся `12fc26462bbab3df76904c6deb01f8c6596de7be`, branch
`codex/review-closure-model-help-contract`; изменён только untracked test source
`/tmp/qcl-doc07-contract-worktree/tests/test_model_help.py`. Tracked tests diff
exit0; SHA256 test_contracts.py прежний 0231b4…63fd7. `git diff --no-index --check
/dev/null tests/test_model_help.py` дал пустой output и exit1 (new-file difference);
whitespace diagnostics отсутствуют.
Production, loader, C2, original checkout и root/checkpoint не изменялись.

Original v1 report/identity/patch сохранены без overwrite. Дополнительно frozen
exact v1 source скопирован в `/tmp/qcl-doc07-C1-red-v1-test_model_help.py` и имеет
прежний SHA256 c2fdf6…bf684. `/tmp/qcl-doc07-C1-red-v2-delta.diff` содержит только
новую параметризацию и три cap-negative substitutions. Все hashes ниже.

| Артефакт | SHA256 |
| --- | --- |
| v2 test source | `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd` |
| v2 full patch | `40e169b6b54f65439b8a77bd0639dcdbf13a54d04a71b1e5b3c931410e1e6389` |
| v1→v2 delta | `9d085d04d81bb0392ed35a151ef3711d19f0b50599cf11bad6960066bb1f20dd` |
| preserved v1 source | `c2fdf66a51a5b772e270cd520e1c560794c11a39c191bfe2ed8abc61e33bf684` |
| preserved v1 report | `844f6e1f9124237a27241be4984b23cafa102c355073369a604b2aadb50ea68a` |
| preserved v1 identity | `90b1caebc279461d7b209916a8e2d3822949776a8608d4ba9737b29bc0164cb9` |
| preserved v1 full patch | `45d7cb0e2184363932da4ec5b5160b55cb453605a7935a562f9e404984b34d92` |

Только text/Git/hash/copy/diff/read и source/artifact writes. Python, imports,
parsers, schema validation, pytest/collection, installation/network, children,
commit/push/main и production implementation не выполнялись; runtime calls=0.
Logical read estimate <0.3 MiB при cap1 MiB, physical Git/fs I/O не измерялся.
All prior v1 shape-vs-proof limits действуют. RED ещё не наблюдался; C2 не начат.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 isolated cap+1 negatives подготовлены | Exact v2 source/delta, новые id/path/point | Source-only, требуется narrow R | сохранить |
| Accepted Fact.status domain покрыт test source | Paired parameterization всех5 statuses в inputs/api | Runtime/collection ещё нет | дополнительно измерить |
| Старые tests/v1 artifacts/production сохранены | Hashes, tracked diff exit0, narrow delta | Не scientific/runtime acceptance | сохранить |
| Observed RED или GREEN уже получен | Runtime calls=0 | Нужен Root после narrow independent R | данных недостаточно |

STOP: narrow high source R, затем Root sole RED в уже заданном finite budget.
