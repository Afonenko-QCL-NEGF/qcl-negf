# SI05 correction candidate — four SKILL + UI

Exact future paths `.agents/skills/qcl-{research-framing,physics-audit,results-analysis,performance-audit}/SKILL.md` and corresponding `agents/openai.yaml`; current files untouched. Existing names/descriptions/UI fields retained; no new tools/icons/policy, implicit discovery preserved.

Framing после first paragraph: «Единица работы — один scientific question/decision. В доступном checkout используй общий task contract для immutable handoff; standalone brief сохраняет scope, unknowns, output и finite stop. Неизвестные future budgets локализуй; их отсутствие не блокирует подготовку brief». Scientific hypotheses/boundary steps не удалять.

Physics заменить «Начать с физического утверждения и реальной модели архивного запуска»:

> Начать с конкретного физического утверждения. Для source-only проверки установить выбранный source, assumptions/conventions и path/symbol; archive не обязателен. Для вывода о сохранённом результате установить реальную архивную модель, frozen plan, run/attempt и compatible reader. Missing archive blocks лишь result claim. Unit — одно уравнение/оператор/критерий; output distinguishes source finding and measured evidence.

Results last sentence заменить: «Наличие RO-Crate проверяй по выбранному Results source и actual export; legacy statement не устанавливает нынешнюю поддержку. Unit — bounded inventory/comparison property; immutable handoff сохраняет compatible reader и original hashes; data insufficiency закрывает зависимый claim без new run».

Performance перед result table: «Для source-only задачи выдай bounded observability/cost-mechanism audit без численного speedup verdict. Unit, declared evidence scope, output и finite stop задаёт current task contract; недостающий профиль не блокирует independent source review». Existing same scientific contract и permission paragraph неизменны.

Existing `default_prompt` replacements:

- framing: «Используй $qcl-research-framing, чтобы подготовить проверяемый научный запрос QCL-NEGF с границами, свидетельствами и явными неизвестными.»
- physics: «Используй $qcl-physics-audit для source-only или архивной проверки формул, кода и научных свидетельств в порученном scope.»
- results: «Используй $qcl-results-analysis для ограниченного анализа готовых архивов QCL-NEGF с совместимым reader и проверкой сопоставимости.»
- performance: «Используй $qcl-performance-audit для анализа стоимости и пробелов измерений при неизменном научном контракте.»

Standalone references include versioned owner/source lookup notice and essential task fields; do not copy model formulas/tolerances/schema. Future formal validator and forward ticket separate SI07. READY docs-only proposals; behavior not_measured.
