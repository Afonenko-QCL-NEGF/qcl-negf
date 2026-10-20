# DOC04 I-Root — частичный source-only handoff, STOP для high review

Изолированный worktree `/tmp/qcl-doc04-root-recipe-worktree`, ветка
`codex/review-closure-doc04-root-recipes`, неизменный HEAD
`b07974b8e46bf8afdf1740947b842669a62a5ccc`.
Исходный checkout не изменён. Только три разрешённых новых файла;
Git index не изменён, commit/PR/CP не создавались. Submodules в новом worktree
не инициализированы: gitlinks сохранены, включая Core9f4a96d и Runnerfefaa27.
Их owning profile PR не переделывались. Нужный Core guard читался через immutable
`git show 9f4a96d...:docs/make.jl` из существующего component repository.

## Сделано

- Сначала записан основной dedicated fixture source для strict CLI, layout,
  frozen operator bytes, caller-marker rejection, cap/deadline/partial logs.
  Затем реализация. Дополнительные filesystem и blocked CLI controls добавлены
  после исходной реализации: полную последовательность runtime TDD не заявляю.
- `docs/public/make.jl`: explicit pilot-only; Base path/ancestor/symlink/layout,
  absent BUILD, VERSION1.13.0 и active project guards до `using Documenter`;
  typed `Module[]`, точный sitename, checkdocs=:none, frozen pages, остальные
  kwargs D1+D2+D3. Index LF literal принадлежит recipe. Runtime math отсутствует.
- `ops/docs.ts`: strict logical CLI, новые private attempts без reuse/cleanup;
  только blocked receipt; exact8f05 chapter check, извлечение index literal
  без исполнения Julia; metadata guards и bounded staged tree byte inventory;
  injectable finite child drains с deadline/caps и раздельными exit/drain/errors.
  Descendant termination и resource measurements остаются null.
- Dedicated source controls включают empty/file/dangling BUILD, ancestor symlink,
  wrong owner, overlaps, lexical prefix trap, staged payload symlink, cap/deadline,
  self-authored admission и сохранность receipt при повторном вызове.

## Почему это частичная реализация

Источник `ops/docs/assemble.py` SHA256
`58d47789da8af18a66136676228c7398fcd50c8797838e8614c8aa07f3d64fda`
публикует чистые `load_pilot_plan`, `transform_page`, `validate_payload`,
`validate_asset_entry`, `prepare_catalog`; полного admitted assembly entrypoint
нет. `prepare_catalog` всегда возвращает blocked и bundle_bytes=None при любой
переданной schema. `ops/docs/math-render.mjs` публикует `renderMathBatch`,
но полного cross-runtime chain/serialization API это не задаёт.
Согласно поручению API не выдуман; partial result сохранён вместо нового цикла.

Также existing `sourceGraph(requireClean=true)` использует unbounded buffered
`ops/process.ts:run`. Этот runner не вызван из finite preflight, source graph
остаётся null + concrete blocker. Это явный оставшийся пробел, а не проверенный
clean graph. Все BUILD invocations остаются blocked; admission path не читается
как доверенное разрешение, никакие caller booleans не принимаются.

Не завершены и не заявлены:

1. Admitted bounded sourceGraph runner binding и полный plan validation через
   accepted adapter API, source/recipe/effect identity manifest/recheck.
2. Фактическое staging всех owning source trees/assets, operator write/readback
   mapping и before/after recovery hash receipt. `operatorSources` готовит exact
   byte mapping в памяти; это не выполненный staging.
3. Full nested/dynamic docstrings/transitive import/cache proof, installed
   Documenter/toolchain identity и полный assets/license/runtime CSS binding.
4. External fresh inventory/admission/ownership/exclusivity/process-tree grant
   binding; ни path, ни существование receipt это не устанавливают.
5. Dispatch трёх Julia recipes, adapter assembly/catalog, final payload checks,
   source graph/input recheck и immutable candidate receipt. Они не скрыты за
   dummy subprocess, marker status или fallback schema.
6. Meaningful before/after source-change orchestration control и actual Julia
   guard sentinel harness. TS layout controls не доказывают исполнение Julia guards.
7. Production-wiring finite runner: spawn failure receipt, sink/cancellation
   completion, externally proven descendant stop и output/scratch caps требуют
   отдельного binding/review. Helper не является production process sandbox.

## Проверки, пределы и ledger

Только source inspection, Git/path metadata, hashes и text diff whitespace checks
для каждого нового файла через `git diff --no-index --check /dev/null PATH`.
Все три text checks без диагностик. Это не parser/lint/format/typecheck/test pass.
Target execution, Deno/Julia/import/compiler/parser/formatter/linter/tests,
render/build/native/network/science =0. Runtime RED/GREEN не выполнялись, поэтому
новые controls — только reviewable source. Независимый review ещё не выполнен.

Первичная worktree creation получила read-only .git sandbox failure; повторена
та же разрешённая операция через approved escalation и успешно создала только
названный изолированный worktree. Это не auto-review rejection. Original prior
broad-read failure и его historical receipts не изменены.

Read ledger: named source inventory (designs/reviews/AGENTS/architecture/API/tests/
recipes/plan) имеет совокупный размер282640B на final inventory pass. Reads
зачислены консервативным общим резервом **2080880B**: семь полных passes этой
совокупности1978480B плюс102400B на skills, immutable Core extract и repeated
small generated-source edits/extracts. Это upper bound source bytes, не measured
physical I/O/RSS. Дорогие деревья/install payload/science data не читались.
В исходном первом cwd снята metadata identity по обязательной инструкции; она
не использована как выбранный source. Свежий isolated HEAD/status/gitlinks
перепроверены. Read budget3MiB, output128KiB соблюдены по conservative reserve и
размеру patch/report/identity; CPU/RAM enforcement физически не измерялось.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Operator recipe соответствует точным API/path literals | new docs/public/make.jl; frozen D1/D2/D3/path contract | Source only, guard/import/render не исполнялись | сохранить |
| Каноническая recovery глава сохранена | source SHA8f05...de49; operatorSources immutable byte binding | Фактическое staging/readback ещё отсутствует | дополнительно измерить |
| Caller marker не создаёт BUILD READY | buildBlockers + CLI blocked receipt source | Fixture execution не выполнялось | сохранить |
| Полный finite orchestrator реализован | Только helpers и blocked CLI source | Missing bounded graph/admission/assembly APIs, шаги выше | изменить |
| BUILD/native/public/scientific acceptance выполнены | Нет execution receipts | Все эти этапы не исполнялись | данных недостаточно |

STOP. Частичный source handoff для независимого high review; не SOURCE PASS и
не READY. Продолжение требует закрыть конкретные owning API bindings и затем
отдельно допустить соответствующие fixture/runtime этапы.
