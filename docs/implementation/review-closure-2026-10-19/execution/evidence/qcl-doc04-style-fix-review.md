# DOC04 narrow style error routing — независимый high source review

2026-10-20. **PASS_SOURCE.** Narrow fix исправляет установленный маршрут ошибки style attribute, сохраняя принимаемый набор и остальные static-markup/style guards. Новых findings в точном delta не найдено. **Actual new run pending**: этот verdict не является after GREEN или новым runtime/corrective budget.

Reviewer прочитал actual failed raw сначала, затем receipt, actual diff/source/test и авторский report последним. Target execution/import/parser/Python/Node/Deno/tests/render/build/network/children/product/checkpoint/Git mutations=0. Только read-only text/Git/hash operations и report/identity writes. Порученные10min/1CPU/1GiB/read1MiB/output32KiB не представлены как измеренная cumulative telemetry.

## Exact binding

Worktree `/tmp/qcl-doc04-root-worktree`, HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; status — untracked ops/docs/ и два tests, без новой staged/committed revision. Actual diff against отдельно retained before source содержит ровно одну conditional routing change.

| Артефакт | SHA256 |
| --- | --- |
| Before math source `/tmp/qcl-doc04-style-fix-before.mjs` | `585dfa5bd02c7968d089d2b746d611c4d137487232c7c20e2639851ee5450433` |
| After `ops/docs/math-render.mjs`,20769B | `663c712d01db3bdc4bca66d3bb58b9aa6bbffd850c8961e1560c30292fd1aba5` |
| Unchanged Node test | `a3e47d219238e9e0b6be4b64ef42154a7057e4ac79776621f3bca84f58acc6a7` |
| Unchanged assemble.py | `58d47789da8af18a66136676228c7398fcd50c8797838e8614c8aa07f3d64fda` |
| Unchanged pilot-plan.json | `cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50` |
| Unchanged Python test | `2207f3bce01e55774b2a4f3a5930fbb5cc880b84fe6e1b38afeafab3a2a548ca` |
| `/tmp/qcl-doc04-style-fix.patch` | `e937e55b066d43b136cd5fa5320b8dfe220c9538f9f0776b5eb4d6ce15acfd9e` |
| Full single-source patch | `7e938108b652efa20a3a6f9e2dce415b70767ef2d8a692844ab62e0456ad6700` |
| Author identity | `76ceea158b1ffcd29aa86654d8b2840910becea32deec70dc62043d028119b84` |
| Author report | `abd7b3548ade867732e4db58f0f84b9c1abcba63e1fd1049ec9c63c07d8b3048` |
| Original NODE-GREEN-2 raw | `6a76be27dbcc18af6b9d967d5a68f93e25daaf2b7dd226c09506b994be3bd9dd` |
| Original NODE-GREEN-2 receipt | `cd36c8e6be39a96d566fde51e1738c8138ab5af8adadfc8e76bac942cf857572` |

Primary accepted DOC04/KaTeX contracts и CPP2 `/tmp/qcl-doc04-root-code-v2-review.md` SHA `b259f5b8c5f03055b159938e5dbba1c7f1b555e617b207fd0375eecb43809bc6` остаются scope authority. Новый source не наследует автоматически прежний whole-source verdict; здесь checked именно этот delta.

## Наблюдение и причина

Provided actual raw сообщает15 tests/14 pass/1 fail. Failure в `tests/docs_math_test.mjs:217`, assertion232–233 ожидает code unsupported_style, а captured error имеет unsupported_markup из прежнего externalizeStyles372. Receipt: exit1,0.447s,3301 raw bytes, raw_capture_complete=true, raw_capture_error/guard_error/stop_reason=null, без output overrun. Runtime binary и Node test hash зафиксированы receipt. Это before measurement, не execution reviewer.

Первые два style-loop cases отвергаются ожидаемым code; третий `background:url(https://example.org/x)` попадает в общий attribute-resource regex до mandatory declarations(). Поэтому цикл прекращается на несовпадении code. Последние три style-loop cases тогда не получили самостоятельного runtime результата. Нельзя приписать этому raw успешную проверку всех unsafe-style variants.

Actual fix `math-render.mjs:372–374` добавляет `name !== "style"` к прежнему общего attribute guard. Allowed attribute vocabulary/on*/entity/namespace/class checks остаются раньше/рядом. Каждый принятый style attribute обязательно хранится в attrs и на387–397 проходит `declarations(original, important)` до удаления style/создания external class/CSS. Обхода этой проверки delta не добавляет.

## Почему previously rejected input не становится accepted

Для **не-style** attributes прежний resource regex и unsupported_markup branch byte-equivalent; URL/scheme markers в разрешённых SVG/MathML scalar attrs по-прежнему отвергаются. Unknown/resource attribute names, active tags/on* handlers, malformed/duplicate attrs, namespaces и class grammar не менялись. Неверный entity decode по-прежнему unsupported_markup до style routing.

Для **style** принимаемый язык определяется обязательным unchanged declarations297–324:

- URL(), expression(), var(), CSS escapes/backslash, ampersand/angle brackets/`!` отсекаются в initial forbidden-style predicate;
- каждое поле имеет закрытый `property:value` формат; двоеточие внутри value запрещено, поэтому javascript:/data:/blob: value не становится разрешённым scheme;
- property допускается только finite length allowlist, три color properties, position или border-style с закрытыми value grammars; неизвестный property, включая scheme-name в позиции property, отвергается;
- literal url( не может пройти ни эти value grammars, ни initial predicate;
- competing important context/shorthand/all guards продолжают работать до generated rule;
- style attr не сериализуется обратно; deterministic class/external CSS/ordered declaration/caps checks сохранены.

Следовательно стиль, который раньше отклонялся общим scheme/url predicate, не удовлетворит unchanged declarations language. Меняется **classification** такого failure с unsupported_markup на established unsupported_style, что соответствует accepted style contract и immutable test. Это не обещание сохранить прежний ошибочный code для style URL и не ослабление rejection. Для обычных safe styles путь принятия, generated bytes/hash и geometry semantics не меняются.

Все шесть literal test styles статически получают unsupported_style: !important, var(), URL, expression(), NaN length, escaped CSS length. Никакая из этих строк не исполнялась reviewer. Hash-before-import, trustfalse/stricterror/fresh macros, authored sizing deny, full/partial stylesheet context metadata, markup/style/aggregate caps и output mapping вне delta и сохранены.

## Границы решения

No test/tolerance/fixture/error-code assertion change; failing raw/receipt и before snapshot сохранены. Не добавлены scheme/resource exceptions в output, новые CSP allowances или public license claims. Это narrow classification repair, не третий полный DOC04 contract review.

Actual after syntax/lint/unit/render result ещё не получен в этом поручении. Выполнение требует отдельного coordinator source/runtime/operation/counter binding и выделенного конечного grant; PASS_SOURCE не восстанавливает исчерпанные slots и не разрешает autorerun. Full OFL/schema/final materializer/vendor/native BUILD/browser/CSP/offline/public/science gates остаются open, как в CPP2.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Неверная style error classification устранена в source | Raw stack372 + unchanged test232 + exact conditional diff | Actual new run pending | сохранить |
| Scheme/resource attrs и unsafe styles продолжают reject | Non-style прежний predicate; mandatory closed declarations | Source proof, не общий hostile-CSS/browser oracle | сохранить |
| Accepted input set не расширен | Прежний forbidden marker несовместим с unchanged accepted style grammar | Scope — точный delta | сохранить |
| Tests/failed evidence сохранены | Exact hashes выше | After GREEN не измерен | сохранить |
| Functional/public/native/science acceptance доказаны | Таких after receipts нет | Нужен отдельный bound coordinator run; прежние gates открыты | дополнительно измерить |

**STOP. PASS_SOURCE для after SHA663c712d…; reviewer executions=0.**
