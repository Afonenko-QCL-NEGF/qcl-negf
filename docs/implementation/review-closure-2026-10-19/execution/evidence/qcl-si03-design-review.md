# SI03 — независимый CP-DESIGN review

**Verdict: ACCEPT для narrow proposal-only CP-DESIGN.** Блокирующих замечаний к frozen patch не найдено. Это принятие дизайна маршрутизации; не CP-CODE, применение, публикация, runtime/native/scientific acceptance или grant на исполнение соседних этапов.

Проверяемый patch: `/tmp/qcl-si03-design.patch`, SHA-256 `b3bb0dca45047edc67373f141ed0feedc820246f1b268bc7db8a05fd96edb340`. Checklist: `/tmp/qcl-si03-checkmatrix.md`, SHA-256 `aefe407f5621b1b7044b6dbb39e17ebc001001dfc5d19ca34d8fde7ceaaeaa86`. Author report прочитан последним, после самостоятельного baseline/candidate/source прохода: SHA-256 `e8e51588fca9146678a87c519e39ff0f225170957a275378863529cc14c03a0a`.

## Исходники и независимость

Исходный root HEAD при начале чтения: `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`; сняты `git status --short` и `git submodule status --recursive`, признаны чужие dirty/untracked изменения. До чтения author report самостоятельно прочитаны root AGENTS, architecture, восемь исходных CONTRIBUTING, SI01–07 handoff, autonomy/P1 и canonical workflow. Сначала установлен дефект baseline: универсальные install/test/docs инструкции не различают текстовую правку и исполнение кода; затем проверен предложенный route.

Gitlinks именно `9f8b08bb…`, а не наблюдаемые component HEAD, использованы для проверки происхождения baseline. `git show <selected commit>:CONTRIBUTING.md | cmp` дал побайтовое совпадение всех восьми baseline с выбранными gitlinks; root baseline также совпал с `9f8b08bb…:AGENTS.md`. При начальном чтении все девять live файлов совпали с baseline. Во время review координатор продвинул root до `c43935567df010d43cab9bcd8d851a9ed976a8d7`; это наблюдение о параллельной работе, не новый источник состава frozen proposal и не авторское Git действие рецензента. Baseline и proposal не заменялись.

Canonical working inputs, прочитанные в этом review: `docs/system/agent-review-workflow.md` SHA-256 `8a00d94c2306ffb391887f8e6eaa6d7c6ebc82c55461e5135891147619647dfc`; `docs/system/skills-and-instructions-review.md` SHA-256 `a683b0b9b34de7a83736db15eb3864d93e387a30f80b682671a618040067e38d`. Активное разрешение и accepted predecessor SI01/SI02 приняты из trusted coordinator assignment; первичный пользовательский transcript EXEC отдельно не воспроизводился. Текст historical PLAN не принят за отмену последующего разрешения.

## Проверка дизайна

Candidate root `AGENTS.md:32` вводит ровно восемь классов: docs, source audit, metadata/existing data, targeted check, environment, build/full suites, live/native, science. `:35` ссылается на существующие canonical девять полей и route, без новой обязательной формы. Ссылки соответствуют заголовкам `agent-review-workflow.md:71` и `:175`. Строки `:50–59` сохраняют already-authorized path, dependent-only blockers, общий ресурсный предел, BIND/READY/fresh admission и CP-EXCEPTION. Нет разрешения считать unknown pass или получить runtime/science verdict из source/build exit.

Из candidate AGENTS удалён только добавленный раздел; результат `cmp` идентичен baseline целиком. Поэтому все прежние требования физики, нормировки/весов/units/near-zero, oracle/reference независимости, provenance, модели/сетки/каналов/допусков сохранены побайтово. В частности сохранены safe measured maximum с reserve и production return; four-role NixOS плюс strict nginx preflight; executable/flake/builder/index ownership; `GIT_OPTIONAL_LOCKS=0` для административного read-only Git; fresh admission; original failures/new attempt; native reuse только по derivation/content/test contract; раздельные engineering/signature/staging/guest/restore/final-CI/science gates; один final CI; fixed-light. Новая защита old S01, foreign jobs/VM и existing disks/data не ослабляет их. P1 глобальные ресурсы не умножаются на агентов.

Документационный exception во всех восьми компонентах ограничен текстом/links/format. Executable examples, recipes и behavior/API/schema/config/data changes требуют relevant checks; code не получает универсального освобождения от тестов. Full suites и environment/build остаются отдельными assigned stages с finite envelope; missing runtime является ограничением проверки. Это не обязательство каждый code change автоматически прогонять full suite.

| Owning disposition | Первичный locator и проверенный смысл | Решение |
| --- | --- | --- |
| Root | Candidate `AGENTS.md:32–59`; original целиком сохранён; canonical nine-field authority остаётся единственной | сохранить |
| Core | Candidate `components/QCLNEGF.jl/CONTRIBUTING.md:3–16`; `deno.json:3–5`, `tools/ci.ts:19–39`: TS check отдельно от Julia tests/docs и возможного instantiate; все physics/API/Runner clauses сохранены | изменить |
| Runner | Candidate `components/QCLNEGFRunner.jl/CONTRIBUTING.md:3–16`; аналогичные `deno.json`/`tools/ci.ts:19–39`; corruption/units/identity/restart/one-way dependency сохранены | изменить |
| AiiDA | Candidate `components/qcl-negf-aiida/CONTRIBUTING.md:3–33`: targeted pytest, install/full suite/build разведены; non-integration group не объявлен source-only; plan bytes/provenance/staging ownership сохранены | изменить |
| Contracts | Candidate `components/qcl-negf-contracts/CONTRIBUTING.md:5–21`: relevant positive/rejected-input tests; format revision/producer-reader compatibility и no-exit acceptance сохранены | изменить |
| Platform | Candidate `components/qcl-negf-platform/CONTRIBUTING.md:8–27`; `deno.json:4–5` включает Deno/Python tests; `tests/slurm-vm.nix:2,39–43` строит и boots guests. Five host evaluations сохранены отдельно от four-role preflight; private inputs/admission обязательны для dependent checks | изменить |
| Portal | Candidate `components/qcl-negf-portal/CONTRIBUTING.md:3–17`; `scripts/ci.ts:25–27`, `frontend/package.json:12`, `frontend/tools/asset-receipt.mjs:10–13`: npm ci/tests/typecheck/build раскрыты; локальный `AGENTS.md` существует и сохраняет fixed light/security/owner rules | изменить |
| Research | Candidate `components/qcl-negf-research/CONTRIBUTING.md:8–25`; `README.md:43–57`, Runner `src/cli.jl:66,74`: structural checks/semantic plan/transport solve разделены; matching Runner, научная justification и immutable result provenance сохранены | изменить |
| Results | Candidate `components/qcl-negf-results/CONTRIBUTING.md:5–24`; `README.md:173–184`: настоящий Julia SCBA producer явно вынесен из документационного/Python unit route; reader/contract/identity safeguards сохранены | изменить |

## Фактические проверки и пределы

Выполнены только чтение, ограниченный поиск, Git metadata, hashes, `cmp`, static diff whitespace review. Patch dry-run применим ко всем девяти baseline файлам. Дополнительно `patch --output=-` направлен только в stdout, затем `cmp` подтвердил точное равенство конкатенации всех девяти полученных текстов с candidate в порядке patch. Исходные файлы не записывались. Read-only warnings от patch означают immutable права baseline; обхода записи не выполнялось. `git diff --no-index --check` не дал whitespace diagnostics; exit 1 означает наличие diff. Воспроизведение исходных bytes и checkmatrix не считается behavioral proof.

Новые ссылки root ведут в существующий canonical документ и его два заголовка; Portal link локален компоненту; прежние README/infrastructure locators существуют. Новых absolute workspace ссылок в proposed инструкциях нет. Standalone component instructions не требуют локального root checkout для самого docs-only exception. Доступность внешних GitHub ссылок по сети не проверялась.

Никакие product modules не импортировались. Julia, pytest/Deno suites, environment setup, docs render, browser, Nix evaluation/build, solver, profiling/benchmarks, server/live probes и CI не запускались. Ресурсный grant: один review round, ≤45 min, 1 CPU/2 GiB/128 KiB output; peak RSS/CPU time не измерены и не объявляются pass. Никаких Git mutations, native source edits и scientific attempts рецензент не выполнял. Единственный новый файл — этот отчёт.

Перед narrow implementation повторить byte comparison девяти owning inputs с baseline; при изменённом CONTRIBUTING остановить только его применение и разрешить delta, не перезаписывать чужое. Изменение component HEAD само по себе не инвалидирует неизменившийся CONTRIBUTING; состав нового root определяется его Gitlinks, а не таблицей наблюдений. После owning commits нужен отдельный CP-CODE/diff/link check и публикация в своих PR; этот review не переносится автоматически на изменённые bytes.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SI03 design сохраняет все исходные gates и добавляет корректный action route | Exact patch hash, whole-root byte preservation, девять dispositions выше | Только frozen текст и canonical working inputs | сохранить |
| Docs-only correction не требует Julia/install/full suite; code checks остаются meaningful | Восемь qualified contribution routes и проверенные command effects | Behavior исполнителя не испытывался | изменить |
| Новый состав root/full release/native/science принят | Таких receipts этот review не создаёт | Нужны отдельные owning/technical/scientific gates | данных недостаточно |

STOP: один независимый review round завершён; дальнейшие действия не выполнялись.
