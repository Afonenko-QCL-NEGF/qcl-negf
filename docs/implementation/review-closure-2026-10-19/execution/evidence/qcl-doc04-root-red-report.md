# DOC04 Root — Phase 1, исходники RED-тестов

Работа остановлена после подготовки двух неизменяемых файлов тестов. Исполнение,
парсинг Python/Node, target imports, рендер, сборка, Julia/Documenter и scientific
проверки **не выполнялись**. RED — ожидаемый следующий outcome, не наблюдавшийся
результат. Product implementation не написана.

Изолированный local clone `/tmp/qcl-doc04-root-worktree` создан с `--no-hardlinks`
из рабочего root; checkout — exact `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, ветка
`codex/review-closure-docs-presentation`. Submodules не инициализированы. Исходный
checkout с foreign dirty gitlinks и protected original не изменялись. В конечном
status только два untracked теста. Git stage/commit/push не выполнялись.

Применён TDD skill к написанию тестов. Его требование наблюдать RED не объявлено
выполненным: прямой phase-1 grant запрещает запуск. Тестовые API ниже — routine
pure seams для принятого дизайна; новая модель, CSP, trust policy или renderer
не выбирались. Независимого review этого патча ещё нет.

## Неизменяемые выходы

| Файл | Bytes | SHA256 |
| --- | ---: | --- |
| `tests/test_docs_assembly.py` | 13960 | `4c0f3f10d952be0e38c3c3c3caa098af14e0e126720428dd16ae574dc3106422` |
| `tests/docs_math_test.mjs` | 9405 | `7ae60b15740e7e9790318f8724d364f2a9ce567b2a0480cf13c988172966aef3` |
| `/tmp/qcl-doc04-root-red-patch.diff` | 24131 | `7ccff023590d62ff8e8959015cb44d1b24fded2276c6074b965e0f8949f0d440` |

Patch сформирован read-only `git diff --no-index /dev/null <file>`; exit 1 здесь
означает наличие добавленного файла, не test verdict. Проверка `--check` для
каждого untracked файла не дала whitespace findings. Syntax/runtime не проверены.
Отдельные literal fixture files не понадобились: fixtures помещены в сами тесты,
в сумме 23365 bytes. Исходный код продукта не добавлялся.

## Контроли и предлагаемые pure seams

Python seam `ops/docs/assemble.py`:
`DocsError.code`, `transform_page`, `validate_authored_source`, `load_pilot_plan`,
`validate_primary_sources`, `validate_source_binding`, `validate_payload`,
`validate_asset_entry`, `prepare_catalog`.

Проверяются известные head/config nodes и отказ для неизвестных/повторных inline
nodes; сохранение article текста, anchor/model/equation IDs и exact TeX hash;
plain span inline math только с reviewed mapping, display p.math-container;
никакого dollar regex по произвольному коду/тексту. Literal raw excerpt — synthetic
source fixture, а не якобы retained real build. Узлы привязаны к прочитанному
pinned `HTMLWriter.jl:1068–1143,2388–2390`; complete package tree не верифицирован.

Проверяются три primary slices, required anchors, missing primary source,
неизменность existing `qcl-negf.git-graph.v1`; local page/anchor/font/static worker
closure; CDN, blob/dynamic worker, inline script/event/style, stored theme и OS
preference branch; private paths/maps/arrays/symlinks; pins/hash/licenses и
отдельный отказ MIT для KaTeX fonts. Healthy synthetic license не заявлена как
реальная OFL. Отсутствующая DOC03 schema даёт `blocked`, `bundle_bytes=null`,
`fragments=[]`, `coverage=[]` без fake origin. Новой DOC03 schema в root нет.

ESM seam `ops/docs/math-render.mjs`:
`renderMathBatch`, `externalizeStyles`, `validateMathMapping`.

Будущие unit-тесты используют реальный pinned ESM по обязательному явному
`DOC04_KATEX_ROOT`; sha256 проверяется до target import. Module hash
`cd4b290a4ecf5068161d6a87745655aa74eb18a6e939fa2872d26520ce261b88`, CSS
`df9ef84e97d38557de02183e238f8ddfd10988b37741492e12c3157bc856011e`, версия
0.16.8. Верификация этих bytes выполнена только `sha256sum`. Node не запускался.

Контроли: supported fraction/superscript/stretch math с MathML; wrong module
hash перед sentinel import; wrong version; full literal denied commands set;
comments/escaped backslashes; unknown TeX/sizing, cross-expression macro state;
UTF-8 limit и maxExpand через built-in macro repetitions; additional properties,
source hash/selector/multiplicity mismatches; ordered duplicate declarations,
units, semantic MathML/SVG; !important conflict/dynamic styles/active markup.
Math-only unit result не повышает font license: ожидается `not_evaluated`.
Публичная OFL closure, fonts и browser CSS equivalence этим не принимаются.

## Ожидаемый RED и следующий gate

На frozen baseline отсутствуют `ops/docs/assemble.py`, `ops/docs/math-render.mjs`
и `ops/docs/pilot-plan.json`. Если запускать сейчас, первоначальный RED будет
ошибкой отсутствующего adapter при collection/import. Это ожидаемая readiness
ошибка, **не** доказательство поведенческого failure. После independent review
координатор должен отдельно принять finite engineering unit DEV plan, отметить
эту границу и добиться meaningful behavioral RED прежде product implementation.
Если для harness понадобится иной seam — это отдельный reviewed тестовый diff,
а не скрытая правка frozen исходников.

Для будущего разрешённого запуска нужны точные absolute executable path,
version и executable SHA256 Python 3.14 и Node 24 из выбранного root toolchain
(`flake.nix`, `pyproject.toml`); существование/идентичность runtime не измерены.
Обычные будущие команды: Python unittest discovery только
`test_docs_assembly.py`; Node `--test tests/docs_math_test.mjs` с exact supplied
`DOC04_KATEX_ROOT`. Здесь они не выполнялись. Deno/Julia/Documenter не требуются
этим pure unit файлам. Нельзя оборачивать их full `deno task test`/CI/build.

Фаза 2 остаётся gated отдельным high review точного конечного плана локального
unit DEV запуска; actual DOC04 BUILD требует fresh native admission, toolchain,
import audit и полной license/asset closure. Raw OFL HTTP403 evidence сохраняется,
его отсутствие не меняется на MIT или pass. Missing DOC03 bundle schema отдельно
блокирует serialization. После реализации требуются CPP и GREEN; текущий отчёт
не подменяет ни один из этих gates.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Исходники pure unit controls готовы к независимому review | Exact test hashes и patch выше | Не выполнены syntax/import/tests | сохранить |
| Frozen baseline ещё не реализует адаптеры | Exact cfc38e1, отсутствует `ops/docs` | RED не запускался | дополнительно измерить |
| KaTeX source/API input связан с exact supplied module | Addendum/review hashes в identity; module/CSS sha256sum | Runtime/renderer не исполнялись | сохранить |
| Public bundle/fonts готовы | Нет full OFL/schema/admission receipts | Нельзя утверждать publication pass | данных недостаточно |
| CSP/theme/math equivalence подтверждены runtime | Таких measurements нет | Нужны unit/build/browser stages | дополнительно измерить |

**STOP: tests frozen, product implementation не начиналась.**
