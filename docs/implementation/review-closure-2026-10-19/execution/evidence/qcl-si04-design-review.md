# SI04 — независимый CP-DESIGN

**Verdict: ACCEPT для frozen proposal из четырёх references.** Блокирующих замечаний к этому дизайну не найдено. Это не принятие целого skill bundle, SI05/SI07, implementation/CP-CODE, runtime или scientific acceptance.

Exact patch `/tmp/qcl-si04-design.patch`, SHA-256 `ebc09a7219751c09fa5eadcb007129bea19c3fdccfe63325b1bb638569f452c3`; checklist `/tmp/qcl-si04-checkmatrix.md`, SHA-256 `d863d651a1950ce20870e49feaac75ee0fd1edbc1071b273180ef0258550c45f`. Author report `/tmp/qcl-si04-design-report.md`, SHA-256 `d91c6da2191120417b977ae9c2a1937a8c5b417211ec26d0527e76d6012aebcd`, прочитан после самостоятельного baseline/candidate/primary-source прохода.

## Материал и независимый baseline

Начальный root HEAD `c43935567df010d43cab9bcd8d851a9ed976a8d7`; сняты HEAD/status/recursive submodules. Прочитаны actual AGENTS, architecture, SI04/05/07 handoff, historical PORTABILITY, canonical nine-field contract и все четыре SKILL с текущими references до candidate. Scope — только source/text review, не научное исследование или исполнение найденных команд.

Самостоятельно установлены baseline gaps: references Physics/Results/Performance связывали map с историческим root `efb687…`, при этом current lookup и чтение конкретного архива не были достаточно разделены; standalone мог ошибочно требовать root; Physics reference содержала локальную копию spectral/FDR формул; Results фиксировал transport ceiling/версии рядом с generic reader advice. Это наблюдения о тексте, не найденные дефекты solver или архива. Framing brief не должен создавать конкурирующую обязательную task форму.

Четыре baseline файла побайтово совпали с actual refs и committed refs `c439355…`. Candidate содержит только четыре разрешённых reference paths. Самостоятельно вычислены следующие SHA-256:

| Reference под `.agents/skills/` | Baseline | Candidate |
| --- | --- | --- |
| `qcl-research-framing/references/brief.md` | `b98635fb4df9ac2c4671523c7c1d88ebd163d78284f9422df4572dba4746e271` | `5acf06b37185d31f25b8b52a08bd62d6dfe2d5e8d5244afc9da1eedf272a9f0e` |
| `qcl-physics-audit/references/physics-checks.md` | `6fcba7b193003ae315e6158f47528f5ed87b45d78c457a01c305154c7aa4c315` | `a2b41df68de6ced8921e43a8f46bb123b84381fe9cc30441211cc8d306d5fb29` |
| `qcl-results-analysis/references/comparison.md` | `4e7aa8013da33e0ee0f47ab4c00b5471b28cb0aae7fbb93c3c2162acf1e5ff78` | `ae11f2a66bbc43289f64ef850180d5bf165ca77b1a24e95fed8c2df008a9860f` |
| `qcl-performance-audit/references/telemetry.md` | `1b7168a1bb12525f6e8c7677266ed3adb64faafebf6e1a7816337cb8df399d1b` | `c7a463d9e5397f331b1b4ab5a73c2c19daf02c42c4c0ae70e1193d3efc1fe7d5` |

Во время review координатор продвинул root до `965ebed95d2b627423805d10c46d0ae8dd425e9d`. Самостоятельный diff всех component HEAD против selected gitlinks `c439355…` показал ровно `CONTRIBUTING.md` в семи components и отсутствие committed delta в Core. Проверяемые production/source/docs paths от этого не изменились; Core dirty `docs/src/development/review_oracle_contracts.md` не использован как scientific/source-map oracle. В конце actual четыре refs всё ещё равны baseline. Продвижение Gitlinks — параллельная работа координатора, а не действие рецензента. Gitlinks остаются authority состава; таблица наблюдений этого отчёта не второй lock.

Canonical contract SHA-256 `8a00d94c2306ffb391887f8e6eaa6d7c6ebc82c55461e5135891147619647dfc`; PORTABILITY SHA-256 `9d8a287e5888e6d6bc9bc419f0d226650b94c8c2d42535f68737e770a2821daa`. Необходимый missing original frozen `docs/system/README.md`, private inventories/native receipts/raw arrays не реконструированы. Current direct grants приняты из trusted coordinator assignment, не выведены из historical PLAN prose.

## Dispositions четырёх references

| Reference / candidate locator | Независимая оценка трёх маршрутов и invariants | Решение |
| --- | --- | --- |
| Brief `brief.md:9–23,43–62` | Current code/model вопрос допускает source-only; archive требует archived identity/plan/reader compatibility; standalone сохраняет essential task content без root и без нового registry. Subject hints отделены от canonical nine-field authority; unknown и local stop сохранены | изменить |
| Physics `physics-checks.md:8–22,24–64` | Source-only не требует run; archived equations/criteria привязаны к его версии; supplied fragments можно анализировать без полного checkout. Формулы удалены из skill reference в пользу Core owner anchors; applicability, raw/mixed distinction, same-state U/G, независимый oracle, no model/grid/tolerance drift сохранены | изменить |
| Results `comparison.md:7–29,48–77` | Current source reader audit отделён от result claims; transport/native declarations и archived producer выбирают compatible reader. Другая reader revision допустима при установленной совместимости. Standalone installed package может быть достаточен; no auto install/import/upgrade. Current README не объявлен source старого run; missing contract не получает permissive fallback | изменить |
| Performance `telemetry.md:8–34,36–125` | Source-only выдаёт observability/hypotheses, не speedup; archive трактует реальные counters по archived units/scope; standalone работает с предоставленным и точным missing owner locator. Process-inclusive/nesting/coverage/null/JIT/peak/durability ограничения сохранены; старые defaults/cadence/overhead proposals не превращены в текущие факты или grant | изменить |

Все refs сообщают essential вопрос/owner, immutable inputs, scope/invariants, oracle/evidence level/check protocol, dependencies, finite common budget/stop и output/limits/resume обычным текстом. Они ссылаются на один canonical контракт при доступном root, а не создают новую обязательную форму или perpetual approval. Already-authorized path сохранён; missing блокирует dependent claim/action, не весь доступный аудит. New solver/profile/build/install/server этап не разрешается ссылкой или готовым brief.

Физические формулы, численные thresholds/transport ceilings и schema payload в candidate не дублируются. Сохраняются предметные вопросы и precise owner pointers. Дата 2026-09-28/root `efb687…`, пределы bibliography reading и историческая negative inventory явно ограничены своей эпохой; они не утверждают отсутствие current production measurements. Frozen arrays/исторические отчёты не меняются.

## Проверенные первичные locators

Независимый targeted source lookup подтвердил в фактически выбранных owning sources:

- Core `_acceptance_metric_metadata` в `src/numerics/reference/acceptance_metadata.jl:439`; Documenter IDs `traceability`, `acceptance-metadata-registry`, `eq-validation-residuals`, `validation-spectral-sum`, `theory-limitations`; numerical-policy и Research scientific-inputs существуют. Это owner markers, не обычные Markdown fragments и не уже построенный сайт.
- Results `archive.py:271–291` содержит `verify_archive`, `receive` и отдельный legacy multipart dispatch; `multipart.py:226` — legacy `receive`. `native.py:174–190` требует declared supported contract/schema/version без legacy-layout fallback. `StateReader`, `verify_recovery_bundle`, `validate_model`, `canonical_bytes`, cumulative history/selected witnesses и Contracts `require_contract_set` найдены в названных modules. Поддержка legacy transport не доказывает поддержку legacy HDF5; candidate это явно различает.
- Runner results IDs `native-result-formats`, `solver-quality-contract` существуют. Timing/memory symbols, producer begin/end calls, native journal/admission, hardware reports, calibration, point artifact verification, scheduled/configured BLAS setters существуют по candidate map. Текущие line numbers не перенесены в reference как вечные locators.
- Contracts `telemetry.py::TELEMETRY_SCHEMA/TABLE_FIELDS`, Results `CpuCoverage/TelemetryWriter/_publish`, AiiDA `scheduler_options`, execution CalcJob/Parser и service artifact functions присутствуют. Их наличие не названо production counter coverage или performance pass.

Это source/static подтверждение доступности и описанной границы, не проверка конкретного archive reader execution. Научных архивов для этого review не предоставляли.

## Формат, portability и ограничения

Patch headers содержат ровно четыре owned references. `patch --output=-` направлен только в stdout; `cmp` подтвердил точное равенство полученных четырёх текстов candidate в порядке patch. Baseline readonly warnings не сопровождались записью/обходом прав. Проверены UTF-8, final newline, trailing whitespace; `git diff --no-index --check` без whitespace diagnostics, exit 1 из-за наличия diff. Author 108/108 self-check не принят за независимый behavioral результат.

Все новые local Markdown links — `../SKILL.md`, разрешаются внутри существующего собственного skill package. Root/owning paths текстовые, условные versioned lookup locators; standalone не обязан иметь эти каталоги и точно описывает недоступный owner path/commit. Mandatory `/home` или `/tmp` ссылок в candidate нет. Portable package content самостоятельно оценён по relative path structure; удалённую авторскую temporary standalone copy рецензент не воспроизводил. External bibliography URLs/статьи новой network-проверкой не проверялись.

Четыре SKILL и четыре UI metadata файла прочитаны/hashed, Git diff по ним отсутствовал. Physics archive-first opening и Results RO-Crate sentence в untouched SKILL — известные dependent SI05 entrypoint gaps. Они не блокируют этот references-only proposal и не объявлены исправленными SI04. До acceptance всего bundle SI05 должен согласовать entrypoints; SI07 отдельно проверяет format/forward samples. Здесь не получены новые agent behavior samples.

Review использовал только read-only Git/text/hash/source commands; product imports, Julia, Python/Deno suites, installation, render/browser, Nix/build, solver/science, profiling/benchmarks, server/live и CI не выполнялись. Рецензент не делал Git mutations и не менял actual source; единственный новый файл — этот отчёт. Grant: один review round, ≤45 min, 1 CPU/2 GiB/128 KiB output. CPU time/peak RSS не измерены и не объявлены telemetry pass.

Перед implementation повторно сравнить четыре live refs и защищённые SKILL/UI inputs; drift блокирует только dependent application. После применения exact accepted text нужен отдельный CP-CODE. Новая composition publication не наследует runtime/scientific acceptance из этого design.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Четыре refs дают корректные current/archive/standalone routes | Exact hashes, самостоятельный manual/source review и dispositions выше | Только frozen reference design | изменить |
| Owner authority и научные/resource gates сохранены | Canonical contract, versioned reader boundary, no duplicated formulas/threshold/schema, no new runtime grant | Derivation/measurements здесь не выполнялись | сохранить |
| Standalone lookup не требует root и не фабрикует отсутствующее | Essential fields, package-local links, точные missing owner/version cases | Whole SKILL entrypoints требуют SI05 | сохранить |
| Skills/runtime/science прошли acceptance | Таких samples/receipts не создавалось | SI05/SI07 и отдельные runtime/science gates впереди | данных недостаточно |

STOP: один independent CP-DESIGN round завершён; дальнейших действий не выполнялось.
