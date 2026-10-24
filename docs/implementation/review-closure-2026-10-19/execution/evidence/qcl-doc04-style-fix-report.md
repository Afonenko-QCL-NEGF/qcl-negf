# DOC04: narrow style routing repair

2026-10-20. Этап — изменение исходника по существующему RED; runtime GREEN не заявлен. Единственный изменённый source: `/tmp/qcl-doc04-root-worktree/ops/docs/math-render.mjs`. MainRoot, tests, failed logs, shared checkpoint и предыдущие reports не изменялись. Runtime/tests/import/build/network/commit calls=0.

## Identity

Actual HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; status: untracked `ops/docs/`, `tests/docs_math_test.mjs`, `tests/test_docs_assembly.py`; восемь submodules uninitialized. Input SHA256 точно совпал с поручением: `585dfa5bd02c7968d089d2b746d611c4d137487232c7c20e2639851ee5450433`. Before snapshot сохранён отдельно `/tmp/qcl-doc04-style-fix-before.mjs`.

After SHA256 `663c712d01db3bdc4bca66d3bb58b9aa6bbffd850c8961e1560c30292fd1aba5`, 20769 bytes. Delta `/tmp/qcl-doc04-style-fix.patch`; full single-source addition patch `/tmp/qcl-doc04-style-fix-full.patch`; exact hashes и machine identity — `/tmp/qcl-doc04-style-fix-identity.json`. Full patch относится только к owning source этого задания, не к остальному DOC04 graph.

Указанный `qcl-doc04-root-design.md` отсутствует; найдены и использованы `/tmp/qcl-doc04-design.md`, design review и точный accepted math contract `/tmp/qcl-doc04-katex-binding-design.md` §5. Он требует отклонять resource/dynamic styles и сохранять строгую property/value grammar. Прочитан предоставленный corrective source review `/tmp/qcl-doc04-root-code-v2-review.md`.

## Причина и минимальная правка

Предоставленный actual RED `/tmp/qcl-DOC04-NODE-GREEN-2/original.log`: 14 pass/1 fail, test `tests/docs_math_test.mjs:217`, assertion 232–233. В прежнем `externalizeStyles` строка 372 проверяла все значения атрибутов regex `javascript:|data:|blob:|url(` до вызова `declarations()`. Поэтому третий style fixture `background:url(https://example.org/x)` давал `unsupported_markup` и прерывал цикл, хотя assertion ожидает `unsupported_style`.

Единственная правка строк 372–374: общий resource guard применяется при `name !== "style"`; style всегда проходит существующий обязательный `declarations(original, important)` ниже. Атрибуты, разрешённые словарём, namespaces, class grammar, unknown/on* rejection, entity decoding и malformed markup guards не менялись. CSS allowlist, URL/escape/expression/var/important checks, context conflict checks, caps, hashes, output policy не менялись.

Поведение по исходнику для всех шести fixtures:

| Style | Доказательство маршрута после правки |
| --- | --- |
| `height:1em!important` | `declarations` initial forbidden `!` → unsupported_style |
| `color:var(--x)` | initial var regex → unsupported_style |
| `background:url(https://example.org/x)` | initial url regex → unsupported_style; прежний ранний unsupported_markup устранён |
| `height:expression(alert(1))` | initial expression regex → unsupported_style |
| `height:NaNem` | LENGTH grammar false → unsupported_style |
| raw `height:\31 em` | initial backslash regex → unsupported_style |

Последние три cases не имели отдельного runtime результата в failed test, поскольку цикл остановился на третьем; их вывод здесь статический. Дополнительной обнаруженной причины сбоя этих fixtures нет.

Отсутствие расширения принимаемой CSS grammar следует из обязательного `declarations`: URL и dynamic grammar отвергаются начальным guard; javascript/data/blob требуют двоеточия в value, которое отвергает declaration regex `[^:;]+`; остальные варианты отвергает закрытый property/value allowlist. До принятия и сериализации обязательны все прежние проверки. Нестилевые resource values по-прежнему отвергаются исходным regex с unsupported_markup. Декодирование сущностей остаётся до routing и сохраняет собственный unsupported_markup contract.

## Проверка и границы

Прочитаны failure stack, actual source и unchanged test; diff содержит одну conditional repair. `git diff --no-index --check before after` не вывел whitespace errors. Обычный `git diff --check` тоже пуст, но source untracked, поэтому самостоятельным свидетельством его проверки не является. Никакого formatter/linter/parser/import/test здесь не запускалось. Tests SHA256 остался `a3e47d219238e9e0b6be4b64ef42154a7057e4ac79776621f3bca84f58acc6a7`. Original RED log сохранён с SHA256 `6a76be27dbcc18af6b9d967d5a68f93e25daaf2b7dd226c09506b994be3bd9dd`.

Независимый CP-CODE review и отдельный Node call принадлежат координатору; прежний PASS_SOURCE не переносится автоматически на новый SHA. Функциональный результат after, browser/CSP/layout, release/native/science не измерялись. Никакой новой попытки или восстановления исчерпанных unit slots этот repair не создаёт.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Причина неверного error code установлена | Actual RED stack → прежняя строка 372 → mandatory declarations | Только source causality и предоставленный before runtime | изменить |
| Unsafe styles продолжают отвергаться | Existing forbidden regex + declaration/property/value allowlist; изменён только style routing | After runtime отсутствует | сохранить |
| Tests и failed evidence сохранены | Unchanged test/log SHA256, отдельный before snapshot | Не новая независимая runtime проверка | сохранить |
| After functional GREEN | Не измерено | Нужны separate CP-CODE и отдельно выделенный coordinator Node budget | дополнительно измерить |

STOP: source-only handoff; дальнейших действий нет.
