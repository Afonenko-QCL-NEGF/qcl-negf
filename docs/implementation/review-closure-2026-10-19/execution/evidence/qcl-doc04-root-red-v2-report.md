# DOC04 Root — corrective Phase1, cycle1, v2

Исправлены только четыре замечания к **исходникам** Python unit-тестов из
`/tmp/qcl-doc04-root-red-review.md`, SHA256
`4c7b969ce90fef61e427780edbc84d5b8700189b8a9e4ecc6da4b51698907863`.
Node math test оставлен побайтово неизменным. Imports, target/test parsers,
Python/Node/Julia execution, tests, render/build, network, children, Git
stage/commit/push не выполнялись. Product files по-прежнему отсутствуют.

Рабочий root остаётся `/tmp/qcl-doc04-root-worktree`, HEAD
`cfc38e1761f24caf436d938f378dbcdbf71a28f0`, ветка
`codex/review-closure-docs-presentation`; восемь submodules не инициализированы.
Новый parent batch8 HEAD не перенесён в этот frozen baseline. Его network TLS
failure не затрагивался. Protected original не изменялся.

## Точный delta

| Finding | Изменение исходников | Различаемая ошибка |
| --- | --- | --- |
| F1 | `test_resource_scanner_checks_css_and_static_worker_edges:245`: healthy classic script теперь вызывает `new Worker("assets/worker.js")`; MiniSearch остаётся worker-relative. Для каждого missing font/worker/importScripts target используется отдельная копия полного healthy payload. Добавлен старый wrong-root URL `worker.js` как negative. | Scanner с ошибочной JS-file-relative базой перестаёт получать healthy fixture, а correct document-relative resolver не краснеет по посторонней причине. |
| F2 | `PRIMARY:49`, `AVAILABLE_PRIMARY:68`, tests195/213: независимые literal expected Core/Runner/Root paths и output URLs по accepted D §1; available set не извлекается из plan. Есть отдельные source и URL one-field mutants для каждого из трёх slices; availability negative сохранён. | Wrong primary path/URL не переопределяет собственное ожидание. Mutant path добавлен в available, чтобы binding reject не маскировался missing-source ошибкой. |
| F3 | `test_font_license_policy...:310`: отдельный private synthetic `.woff2` / `font/woff2` / `katex-fonts` / OFL-1.1 metadata healthy control; MIT negative меняет только SPDX attribution. Missing notice и wrong notice hash проверяются отдельно. Generic CSS controls сохранены. | Blanket reject всех fonts и отказ из-за несогласованной CSS/font категории больше не удовлетворяют паре healthy/negative. |
| F4 | Test-only `ScriptReferences:76`, config assertions121: точное сохранение известного input BaseURL `.`; один config file; local relative output script URL разрешается от page URL и обязан ссылаться на этот generated file ровно один раз. Script-only combined HTML/generated payload проходит existing static closure, удаление config даёт missing_resource. Unknown/duplicate config negatives сохранены. | Wrong BaseURL, orphan config, wrong/missing HTML reference и несуществующий script target не удовлетворяют positive assertions. Generated filename/hash naming не навязаны как новый контракт. |

Root-relative primary_sources развернуты явно из owners accepted D:
`components/QCLNEGF.jl/docs/src/theory/09_scba.md`,
`components/QCLNEGFRunner.jl/docs/src/api/public.md`,
`components/QCLNEGFRunner.jl/docs/src/user/configuration.md`,
`docs/public/operator-recovery.md`. Соответствующие URLs/anchors имеют literal
ожидания. Existing final-assessment и Runner operator-route anchor требования
сохранены. Новой slice, schema, модели, CSP/trust policy или renderer нет.

F4 добавляет только исходники test-side stdlib HTMLParser/urljoin/urlsplit
наблюдения; эти imports и parser **не выполнялись**. JS не eval. Проверка
отсутствия inline scripts/events/styles и theme alternatives сохранена.
Существующий CSP не расширяется; browser/CSP runtime pass не заявлен.

Synthetic font/notice bytes — private validator policy fixtures; это не реальные
font bytes, полный raw OFL или admitted license closure. HTTP403 original evidence
и public-font blocker сохранены. Font publication не объявлена разрешённой.

## Frozen outputs и проверки

| Файл | Bytes | SHA256 |
| --- | ---: | --- |
| `tests/test_docs_assembly.py` | 19642 | `ecacc18239241c45ac1ed9c4e7c4935cfd20919cc88ac236a69ffa435bdf038e` |
| `tests/docs_math_test.mjs` | 9405 | `7ae60b15740e7e9790318f8724d364f2a9ce567b2a0480cf13c988172966aef3` |
| `/tmp/qcl-doc04-root-red-v2-patch.diff` | 29916 | `cd53b2d774fcae5845f8ec97436f177e3fecd61eee1c2eac3a977e999fa17a29` |

V2 patch — полный reviewable diff двух additions относительно exact baseline.
`git diff --no-index --check` не дал whitespace findings; exit 1 у no-index diff
обозначает наличие additions, не test status. Git status содержит только два
untracked test files. Hash исходников math test не изменился.

Оригинальные `/tmp/qcl-doc04-root-red-{report.md,identity.json,patch.diff}` не
перезаписывались: повторно подтверждены SHA256 соответственно `e60d7643…`,
`fda4daaf…`, `7ccff023…`; полные значения приведены в v2 identity. Их v1 test
sources восстанавливаются из original frozen patch. V2 — отдельный correction
artifact, не задним числом исправленный первоначальный результат.

Readiness RED остаётся **ожидаемым, не измеренным**: отсутствуют adapter modules
и plan; collection/import failure ещё не доказывает поведенческие assertions.
Нужен high review v2 до отдельно разрешённого bounded RED. Runtime identity
requirements прежние: exact Python3.14/Node24 executable paths/version/SHA256 и
supplied immutable KaTeX root с existing module/CSS hashes. Actual BUILD требует
fresh admission, toolchain/import audit и asset/license closure; missing DOC03
schema отдельно блокирует final serialization. Sole CI и science не расходованы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1–F4 получили различающие source controls | Exact v2 patch/identity и delta выше | Пока не независимый approval или runtime proof | сохранить |
| RED и syntax подтверждены | Нет таких measurements | Этот grant запрещает исполнение/parser | дополнительно измерить |
| Original failed/frozen evidence сохранено | Повторные SHA256 трёх original artifacts | V2 — новая identity | сохранить |
| Public bundle/license/native/browser ready | Нет full required receipts | Missing OFL/schema/admission не закрыты | данных недостаточно |

**STOP: v2 test sources frozen; high review до bounded RED.**
