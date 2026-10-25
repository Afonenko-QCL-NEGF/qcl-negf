# DOC07 C1 v2: collated F1/F2 source repair

Ровно один source repair round после independent REQUEST_CHANGES `/tmp/qcl-doc07-C1-schema-review.md`, SHA256 `a323b9b88128ba3ed3caa60020726e60d336c7c16b21644394a6db303734a812`. Base `12fc26462bbab3df76904c6deb01f8c6596de7be`, isolated `/tmp/qcl-doc07-contract-worktree`, branch `codex/review-closure-model-help-contract`. Canonical DOC03 SHA `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` и frozen D2 SHA `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` не менялись.

F1: View.allOf теперь для input_status.status invalid/unavailable требует для каждого существующего inputs[].used status unknown, atom null, evidence null. Declared не меняется; inputs=[] допускается; documentation availability не связывается с input_status. Основание: DOC03:513–518,1033–1036; independent review F1. Append-only tests проверяют все пять unavailable/invalid reasons, второй input, сохранение known declared, пустую проекцию и обратный healthy control unavailable docs + available known used.

F2: Sha1/Sha256/Id/ScientificId/Uuid/LeafPath, exact descriptor file/served fragment URL/index path и DocRef .html suffix используют `(?![\s\S])` вместо permissive `$` для строгого конца. Это отрицательный lookahead на любой следующий character, переносимый между ECMAScript и штатным Python regex backend; Python-only `\z` не добавлен. Верхние length/allowed character границы не изменены. Pointer и RelativePath не превращены в security allowlist: нормализация/контролы/allowlists остаются C2. URI prefix тоже не превращён в URI parser. Основание: DOC03:333–342,394–399,619–637, canonical selector grammar; independent review F2. Новые tests парно проверяют exact healthy instances и суффиксы LF/CR/CRLF/NUL/U+2028/U+2029 для всех затронутых token families, плюс healthy 1/128-character Id/ScientificId и negative 129-character boundary.

Только schema изменён и tests append добавлен. Original tests bytes 31628 сохранены exact prefix: `cmp -n 31628 /tmp/qcl-doc07-C1-tests-v1.py tests/test_model_help.py` exit 0; original source SHA `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd`. Существующие fixtures/assertions не редактировались. Original schema `/tmp/qcl-doc07-C1-schema-v1.json` SHA `cbca63eac4ce22ece53e5275b5ce458508edf9ab1d467aad28d9a8348534a3a0`; original report/patch/receipts сохранены.

| Artifact | SHA256 |
| --- | --- |
| schema,29608B | `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241` |
| tests,34439B | `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177` |
| `/tmp/qcl-doc07-C1-schema-v2-full.patch` | `858e22de3b3cb7db5b556a7f013372ade44c6445b0b3aeb383f8e532b885d0fb` |
| `/tmp/qcl-doc07-C1-schema-v2.delta.patch` | `1168aa87664b1e8c8a5bef6b01c9bb3559bfef4d931e1fe58faff69b50e7e4c7` |
| `/tmp/qcl-doc07-C1-tests-v2-full.patch` | `182a97de7b42c6fa217ce04b61b47c36a3983fa76022b2d539bb4b5217f1781c` |
| `/tmp/qcl-doc07-C1-tests-v2.delta.patch` | `60e13945d9dc8786fb552cc19591cf7fab564780e19ddda417bd4cf6a466aa70` |

Identity: `/tmp/qcl-doc07-C1-schema-v2-identity.json`.

Git metadata/sha/cmp/source diff checks выполнены. Обе `git diff --no-index --check` между original и v2 вернули 1 (изменения присутствуют), diagnostic output пустой; whitespace findings нет. Status: только untracked schema и tests; submodules отсутствуют. Target imports/parser/schema execution/tests/eval/build/network/commit не выполнялись, runtime calls=0, shared DOC07 runtime counter остаётся Root-owned used1/4. Нет runtime/metaschema/regex portability measurement: portability выше — source-level выбор стандартной конструкции, не test-pass claim. C2/provenance/science acceptance не затронуты.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 expression добавлен для каждого input | View.allOf delta + appended paired controls | Runtime ещё не исполнялся | изменить |
| F2 exact end выражен portable lookahead | Schema delta + appended suffix/length controls | Runtime/backend не измерен | изменить |
| Approved tests сохранены exact prefix | cmp exit0, original SHA | Добавленные regression cases требуют review/runtime | сохранить |
| C1 принят runtime/семантически | Новых runtime свидетельств нет | Separate high R, затем Root-only GREEN; C2 отдельно | дополнительно измерить |

STOP source-only.
