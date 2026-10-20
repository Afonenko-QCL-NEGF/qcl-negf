# DOC07 C1 v2 — независимое focused corrective source review

2026-10-20. **PASS_SOURCE: F1/F2 закрыты; новых замечаний в corrective delta не найдено.** Source eligible для Root-only bound GREEN в первоначальном finite DOC07 plan. Parser/metaschema/regex backend/test runtime не запускались reviewer; actual GREEN pending. Source PASS не означает C2 semantic proof, publication/native/science acceptance и не добавляет runtime slots.

## Identity / scope

Actual isolated `/tmp/qcl-doc07-contract-worktree`, HEAD `12fc26462bbab3df76904c6deb01f8c6596de7be`; status — только untracked schema и tests. Сначала сопоставлены original F1/F2 с accepted canonical/D2 boundary и actual v1→v2 source delta, затем новые tests/helper source, после этого author report. Existing loader и прочие schemas/source не менялись. Никаких imports/parsers/Python/pytest/Node/Deno/Nix/build/network/children/product/checkpoint/Git mutations. Outputs только report+identity.

| Артефакт | SHA256 |
| --- | --- |
| `model-help.schema.json`,29608B | `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241` |
| `tests/test_model_help.py`,34439B | `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177` |
| Original test prefix31628B, повторно хеширован | `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd` |
| Schema full patch | `858e22de3b3cb7db5b556a7f013372ade44c6445b0b3aeb383f8e532b885d0fb` |
| Schema delta | `1168aa87664b1e8c8a5bef6b01c9bb3559bfef4d931e1fe58faff69b50e7e4c7` |
| Test full patch | `182a97de7b42c6fa217ce04b61b47c36a3983fa76022b2d539bb4b5217f1781c` |
| Test delta | `60e13945d9dc8786fb552cc19591cf7fab564780e19ddda417bd4cf6a466aa70` |
| Author v2 identity | `379be977fc7036e21a31e3013b6852a0d6af5345a601bd6bce1df8d7ee3642f8` |
| Author v2 report | `53091d811cbc366586b1ec0c43fddd98cc67c6db1045c758a0ef1a919595c09c` |
| Original independent review | `a323b9b88128ba3ed3caa60020726e60d336c7c16b21644394a6db303734a812` |

Canonical SHA `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`, D2 `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` и accepted D2 review `f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231` остаются normative basis. Scope narrow: исходный полный review не заменён третьим пересмотром contract.

## F1 CLOSED — View status cross-guard

`model-help.schema.json::View.allOf` добавляет отдельный conditional для input_status.status invalid/unavailable. `then.inputs.items.properties.used.properties` требует statusunknown/atomnull/evidencenull для **каждого** input. Base View/InputView/EvidencedScalarState уже требуют соответствующие поля и закрывают objects; отсутствие duplicated required/type в conditional не создаёт обхода.

Known declared не затрагивается; empty inputs[] допустимы. Conditional проверяет input metadata status, а не documentation binding: unavailable docs/bundle_missing и fragmentnull не обнуляют available/known used. Existing bound/nonbound fragment conditional, reason enums и все scalar/status/null matrices сохранены.

Новые `test_review_unavailable_used_guard_covers_every_input` проверяют все пять invalid/unavailable reason pairs, healthy unknown used с known declared, второй input с независимым path, затем known-used mutation именно во втором input и empty projection healthy. Поэтому implementation, проверяющая только первый input либо запрещающая все invalid/unavailable documents, не удовлетворяет паре assertions. Отдельный `test_review_unserved_documentation_preserves_available_known_used` сохраняет обратную independent-axis healthy branch. Tests вызывают actual schema validator; expected outcome не вычисляется из schema condition или product helper. Существующий original status matrix также сохранён.

Это schema shape invariant одного документа по canonical1033–1036/D2R3, не новая C2 inferencing policy. Реальная availability/snapshot validity и selected-child proof остаются C2/owner.

## F2 CLOSED — strict token end

Точные token patterns Sha1/Sha256/Id/ScientificId/Uuid/LeafPath и descriptor file/served fragment URL/index path/DocRef .html suffix заменяют permissive dollar boundary на `(?![\s\S])`. После required token/suffix этот negative lookahead отрицает любой следующий character, включая LF/CR и Unicode separators. Это стандартная regex конструкция, без Python-only end escape. Raw JSON source escape bytes проверены: двойные backslashes корректно кодируют regex `\s`/`\S`, а не literal backslash sequence. Runtime portability не измерялась.

Прежние allowed characters и длины40/64/UUID/Id1..128/ScientificId1..128 не меняются. DocRef suffix сохраняет requirement .html без нового arbitrary path cap. Pointer и RelativePath не превращены в public/path-security allowlist; их normalization/control/selector safety по-прежнему C2. Новых physical bounds, unit registry или URI policy не добавлено.

Новые suffix controls имеют independent literal LF/CR/CRLF/NUL/U+2028/U+2029 для всех затронутых token families через полные healthy document factories. `assert_bad` сначала валидирует healthy, deep-copies его и меняет только выбранное поле; это не self-fulfilling regex oracle. Healthy1/128-character identifiers и negative129 boundary не позволяют отвергнуть все strings или уменьшить прежний cap ради GREEN. Cross-document equality для изменённого fragment id не требуется C1 и этим test не объявляется доказанной.

## Preservation и ограничения

Actual deltas ограничены двумя source corrections и append-only tests. Original31628B test prefix exact hash совпал; ни existing assertions, ни factories/error types/loader не правились. Five oneOf branches, closed fields, Origin/Atom matrices, ten Fact contains/repeated contexts, declared maxima, Index oversized-invalid byte observation, assignment/effective/value-origin shape и C2 separation остаются как в original review.

После правки actual parser/validator test не выполнялся reviewer; это reasoning по source и paired controls. Initial missing-resource RED сохранён отдельно и не становится behavioral pass. Root owns original4-call plan (сообщён used1/4), exact runtime/source/harness/operation/counter binding и sole pending GREEN; этот report не расходует/не возвращает попытку и не разрешает автоматический retry. Public-source/URI/query-free/provenance/graph/mapping/hash equality/full origin chain/byte/finite guards и owner integration остаются C2/отдельными gates. Scientific status не следует из schema/test validity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 действует на every input без стирания declared | View conditional + second-input/empty/independent-docs controls | Actual validator run pending | сохранить |
| F2 exact end не пропускает LF suffix | Standard negative lookahead + suffix/length healthy pairs | Parser/backend execution не измерена | сохранить |
| Старые contracts/tests не ослаблены | Exact prefix SHA и precise deltas | Узкая source review | сохранить |
| C1 GREEN/C2/public/native/science доказаны | Новых receipts reviewer нет | Separate bound runtime/proof/owner gates | дополнительно измерить |

**STOP. PASS_SOURCE F1/F2 closure; reviewer executions=0.**
