# SI05 — independent CP-DESIGN

**Verdict: ACCEPT для frozen восьмифайлового proposal.** Блокирующих замечаний к design не найдено. Это source/manual design review, не применение, CP-CODE, formal-validator success, SI07 forward behavior или runtime/scientific acceptance.

Patch `/tmp/qcl-si05-design.patch`, SHA-256 `36051f34a88546c2ab8f69b0b6d7d996e85962d3214236a4d69cece5ed29f6bb`; checkmatrix `/tmp/qcl-si05-checkmatrix.md`, SHA-256 `fee804255fb56d7d91fadbdf90ea984bdc58378a27a922389fc425ad1c2aab48`. Author report `/tmp/qcl-si05-design-report.md`, SHA-256 `d277c786859d6ee9c82d10bb8c790df9687b1aa72f0e74164386302c469ad743`, прочитан последним после самостоятельного baseline/candidate/scope/UI/link анализа.

## Проверенный материал

Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`; read-only HEAD/status/recursive submodules сняты. До candidate прочитаны существующие четыре SKILL/UI, SI05 handoff, canonical nine-field contract/authority route; architecture и actual root AGENTS сохранены в scope. Все восемь baseline файлов побайтово совпали с actual и committed `965ebed…`. Текущие SKILL/UI не менялись во время review.

Из baseline независимо видны source-level проблемы: Physics opening навязывал archived run source-only вопросу; Results unconditional archive lead не выделял reader/source audit, а последняя sentence фиксировала вечный статус optional RO-Crate; Performance требовал root и содержал timeless caller setting. Это дефекты текста маршрутизации, не наблюдённые agent behavior failures. Существующие discovery descriptions и scientific workflows не перепроектировались.

Exact candidate paths и самостоятельно вычисленные SHA-256:

| Path под `.agents/skills/` | Candidate SHA-256 |
| --- | --- |
| `qcl-research-framing/SKILL.md` | `5c3833087f43e9e639e2b3f3022b1df00682473b8aa2c200b72a0ac53d54e500` |
| `qcl-research-framing/agents/openai.yaml` | `e1ad31b68e4749ffb1bf88de23fd465f27b91e7c94786cef943db25f304c60ae` |
| `qcl-physics-audit/SKILL.md` | `b9a4265d90964efeacfff6eac997f22e9fa9214c3d713ed704191a7dd46127fe` |
| `qcl-physics-audit/agents/openai.yaml` | `f51b508e3ad0a1103c851c0c1ef5aef79e0c63064f9ee02321e7db8a225ae318` |
| `qcl-results-analysis/SKILL.md` | `89bdd7be7b91cb46da1663777a639fab0f6ce738a989c0e0cfa633c92d3da4bc` |
| `qcl-results-analysis/agents/openai.yaml` | `b4974c1c32d462d7d1128a6a058980f1a1b712a3460d83d6925fa0ad78985423` |
| `qcl-performance-audit/SKILL.md` | `597043c2c3a660ae18c84c17ba96729ba393b2e4f53491574af3d156c408ea3b` |
| `qcl-performance-audit/agents/openai.yaml` | `2a8721c4ee8de5fae982cad3f112ff5df1ae2aef6dca633b14ea980733f25836` |

## Semantic dispositions

| Candidate locator | Оценка изменения и сохранённой границы | Решение |
| --- | --- | --- |
| Framing `SKILL.md:12–25` | Optional root canonical route и own brief дают standalone essential content. Source/current/archive/runtime разделены; framing не превращается в выполнение исследования. Known decision/fact/unknown, interview stop, cheapest evidence и scientific questions сохранены | изменить |
| Physics `SKILL.md:8–27` | Source-only модель/код и owning equations достаточны без run; archived model/plan/criteria/data нужны для result claims. Missing source/version ограничивает dependent claim. Raw/mixed, same-state U/G, refinement, independent oracle, calibration/validation и findings уровни сохранены | изменить |
| Results `SKILL.md:8–25,60–63` | Existing immutable data обязательны для result claims; source reader/contract audit возможен без архива. Data-analysis steps явно conditional. Compatible reader, bounded slices, identity/status/failed attempts/derived evidence остаются. Optional RO-Crate lookup у выбранного owner с unknown не является новым gate | изменить |
| Performance `SKILL.md:12–18,32` | Standalone и archive metric contract отделены от current source. Fixed BLAS statement заменён version/caller lookup; scientific equivalence/time-to-accepted-solution, six steps, null/coverage/JIT/RSS/I/O/durability/scaling ограничения сохранены | изменить |
| Все четыре leads и UI | Последнее применимое поручение/retained grant, dependent-only missing, конечный общий envelope и technical predicates сохранены. Invocation не выдаёт solver/setup/build/server/model-change authority и не требует повторного human approval ready bounded check | сохранить |

Дополнительных физических формул, thresholds, schema payload или новых scientific criteria в patch нет. Существующая Performance CPU/wall expression не меняется; имена API/units не переписываются. Root physical integrity, protected inputs, fresh admission/BIND/READY, scientific/resource/CI limits не заменены skill verdict. Canonical девять полей остаются в `docs/system/agent-review-workflow.md:71`; его SHA-256 `8a00d94c2306ffb391887f8e6eaa6d7c6ebc82c55461e5135891147619647dfc`. В SKILL только условный locator, без конкурирующей формы/registry/perpetual approval.

Новая RO-Crate sentence не утверждает implemented/unimplemented status. Bounded search без совпадений в части Results source не использован как доказательство отсутствия optional feature. Конкретный future result audit обязан установить status у выбранного owning source/docs либо оставить unknown.

## Frontmatter, UI и portability

Самостоятельное byte comparison полного frontmatter каждого candidate с baseline подтвердило неизменность, включая exact `name`, `description`, quoting и discovery triggers. Names соответствуют четырём basenames. Непосредственно изменяется body route, а не ширина discovery.

В каждом UI файле удаление единственной `default_prompt` строки даёт byte-identical baseline remainder. Сохранены display/short descriptions и все прочие строки; отсутствующие policy/dependencies/icons не добавлены. Все три string values double-quoted, keys unquoted. Prompt содержит правильный literal `$qcl-…` invocation и реалистичную narrow задачу, не обещает full runtime/science pass. Independent Unicode short-description counts: Framing48, Physics46, Results41, Performance50; все внутри25–64.

Performance prompt «без новых измерений» задаёт предложенный read-only audit; body сохраняет explicit already-authorized bounded-check route. Эта строка не принята за отзыв более позднего/явного direct user grant. Physics/Results prompts соответствуют source-only либо existing-evidence scope; исходные result claims не превращены в source assertions.

Семь SKILL Markdown link occurrences ведут в собственные accepted SI04 refs, реально присутствующие внутри package. Их четыре hashes равны принятым predecessor bytes: Brief `5acf06b…`, Physics `a2b41df…`, Results `ae11f2a…`, Performance `c7a463d…`; SI04 CP-CODE `f1e706cdf6ce8ca82a3bc46bd95967223f6b6d44944d1d7cc581835bbcaca75f` остаётся отдельным входом. Root path текстовый и conditional, standalone не обязан его иметь. Own references содержат essential task content и exact missing-owner route; выдуманный fallback contract/schema не добавлен. Копия standalone runtime не запускалась.

## Фактические checks и ограничения

Прочитаны `skill-creator/SKILL.md`, его `references/openai_yaml.md` и `writing-skills/SKILL.md`. Их общие validator/deployment/microtest/per-skill-repeat рекомендации не расширяют прямое поручение: здесь only manual/source proposal; SI07 имеет ровно8 TOTAL future samples. Не выполнялись validator/YAML imports, initialization/delete-first, 5+ microtests, samples или per-skill permission loops. Никакой новый evaluation grant не создан.

Выполнены read-only Git, text/hash/byte checks: baseline=actual=committed; frontmatter equality; UI other-lines equality; invocation/count review; UTF-8/final newline/no trailing whitespace; `git diff --no-index --check` без diagnostics, exit1 означает наличие diff. `patch --output=-` направлен только в stdout; `cmp` подтвердил точное равенство concatenated eight resulting texts candidate в patch order. Readonly baseline warnings не сопровождались записью. Eight paths — ровно разрешённые SKILL/UI. Script validators и формальные executable checks не запускались, поэтому formal validator PASS не заявляется.

Product tests/imports, Julia/install/build/render/browser, solver/SCBA/Poisson, benchmark/profiler, server/live/CI/Git mutations не выполнялись. Рецензент не менял actual source; единственный новый файл — настоящий отчёт. Resource envelope: один review round, ≤30min, 1CPU/2GiB/128KiB output; CPU time/peak RSS не измерены. Agreement с author report не используется как дополнительное evidence.

До narrow implementation пересверить восемь actual baseline inputs и четыре accepted SI04 refs; drift останавливает только affected application. В active user grant exact I может продолжаться без нового human вопроса, с последующим отдельным CP-CODE. SI07 formal/manual execution и independent fresh candidate/control samples остаются отдельной задачей:4 cases ×2 TOTAL8, одинаковая исходная authorization/caps, no previous-answer/author-diagnosis leakage; никакого переноса этого design verdict на behavior или science.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SI05 design согласует entrypoints с accepted SI04 | Exact8 hashes/patch, independent before/after reading и locators выше | Только frozen proposal | изменить |
| Names/triggers/UI ancillary fields и scientific authority сохранены | Byte equality frontmatter/UI remainder, canonical scoped route | Поведение исполнителя не измерялось | сохранить |
| Standalone работает с локальными refs и exact missing inputs | Seven package-local links, optional root route/essential content | Installed behavior не испытывался | сохранить |
| Formal/forward/runtime/science acceptance получена | Таких executions/samples нет | Отдельные CP-CODE/SI07/runtime/science gates | данных недостаточно |

STOP: один независимый CP-DESIGN round завершён; дальнейших действий не выполнялось.
