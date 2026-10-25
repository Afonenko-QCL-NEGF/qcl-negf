# DOC07 C2 — final focused independent CPP cycle8

**REQUEST_CHANGES.** F1, F2, F4, F5, F6 закрыты по исходникам и причинным regression pairs. F3 закрыт частично: новый assigning guard сохраняет обход через emitted used-status и добавляет отказ для допустимого redacted record. Ниже два подтверждённых source counterexamples F3a/F3b. Это не измеренные runtime outcomes. Reviewer не исполнял target и не разрешает cycle9 либо дополнительный тест.

## Точный immutable input

Worktree `/tmp/qcl-doc07-c2-worktree`, HEAD `d791dea33f4628cf23c0b8552ebee9e51d7dd605`; read-only Git status содержит только untracked module и C2 test, submodules отсутствуют.

| Артефакт | SHA256 |
| --- | --- |
| Actual module53586 B | `6e3f6d8ed2e6a0d7e637c48edc87820c62776755803f4d4b62a3961f8b2429bd` |
| Actual tests52988 B | `ef51509e7b2db13196e5e243193492235d82b516bbc9d93deeb9369000bdc95f` |
| Первые40274 B test, independently hashed | `72240eab26305f63aeeec06197a7f64802c111a83cd3ef8aae603c5e89ae71f9` |
| Prior review | `471cbdffa269970d14ff114ff9b2d66053f6b96c15f25cf9a711d7673c2f99d2` |
| Module delta | `8586a3e13b02999d142628f0fb97ba9c07cb270833a2fcf9c59fb759f9b2fa9d` |
| Regression delta | `84a81aa4aa306a6ced21a99753d8dab519d3473aaa6f5c58e4ba07523bd485de` |
| Full module / tests patches | `683f3581a3a1bb2c51ee497703775e161acd189b05182a33d5ae2de030aca0f4` / `8554da6239d94557cd398f3b1f44ffa24567dccfe69f56a868e1930d881e4d8b` |
| Author report / identity | `6a2efdf710e32bb27d57c261d27e69c254d55a8c2609a7cf8a581f8171d6dccb` / `a6cffe88e2f8d15b2bbfc52fc3386929d7633b50da3f036b2575899fdb1fec34` |
| Frozen D2 | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| Frozen canonical DOC03 | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Unchanged C1 schema / tests | `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241` / `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177` |

Первичными были unchanged D2/canonical, actual code/test deltas и исходники. Авторский report прочитан после них. Проверка focused: неизменённые части v1 переиспользованы из полного independent CPP; все изменённые пути сверены с принятыми clauses. Pointer-only erratum733b не меняет C2. Private `point_passports`/`snapshot_files` рассматриваются как согласованные checked in-memory owner inputs R6, без новой public schema/trust root.

## F3a — P2: emitted unknown used выбирает устаревшую declared assignment

**Локатор:** `model_help.py:878–903`; `_last_assignment`:526–533. Ключевой predicate:

`phase = "used" if item["used"]["status"] == "known" else "declared"`.

Источник authoritative last assignment выбирается по тому, что View решил показать, вместо наличия retained snapshot/assignment. Между тем numeric availability и assigning provenance — независимые поля canonical InputView:510–538. Conservative unknown в emitted used не делает уже имеющуюся runtime assignment отсутствующей.

**Source-reproducible counterexample без исполнения:**

1. Взять `case()`; исходная frozen plan assignment — config_file/public height. Оставить frozen plan, selected context и declared Atom без изменений.
2. В exact retained Snapshot заменить height.assigning на допустимый known record `{status:"known",kind:"execution_strategy",source:null,rule:"fixed_strategy"}`. Это уже существующий producer rule и supported RawAssigning shape; не требуется private path или новая физика. Переиздать snapshot bytes/digest и производные index size/hash. Для чистой пары можно оставить origin claims пустыми и обновить соответствующий retained claim record: actual-origin View остаётся unknown и не используется как proof.
3. Emitted View.used сделать `{status:"unknown",atom:null,evidence:null}`. Сохранить прежний View.assigning config_file/public height с exact `frozen_plan:/assignment` Evidence. Остальные scalar/source/context/causal bindings сохранить согласованными.
4. `_view` пропускает numeric comparison для unknown used. :878 выбирает declared, `_last_assignment` возвращает старый plan record; :882–892 принимает прежние kind/source/rule и разрешает frozen-plan Evidence. Существующая и отличающаяся snapshot assignment лишь не добавляется в allowed set на :898; она не вызывает отказа. Старый public assigning record проходит.

**Требуемый исход:** такая попытка stale assigning attribution должна отвергаться. При наличии actual retained assignment её authority не выбирается public status flag. Существующий healthy frozen-plan Evidence должен сохраняться, когда он действительно соответствует последней assignment, либо когда допустимый declared-only fallback установлен отсутствием runtime evidence, а не желанием скрыть used value.

**Неизмеренный regression contract:** сравнить ту же retained runtime assignment с used known/unknown; истинная последняя assignment с exact snapshot Evidence должна оставаться корректной в обеих ветвях, а старая отличающаяся plan assignment — некорректной в обеих. Отдельно сохранить original same-source frozen/snapshot healthy pair и настоящий missing-snapshot declared-only healthy. Новая точка выбора authority не должна выводиться из Atom equality или значения emitted status.

## F3b — P2: допустимая redacted assignment с точным Evidence отвергается

**Локатор:** `model_help.py:880–881`, unconditional `target.get("status","known") == "known"` внутри ветви, которая обслуживает и `assigning.status="redacted"`.

Canonical:510–538 и C1 `RawAssigning`/`Assigning` разрешают status redacted, source=null. Evidence у redacted может быть nonnull; это безопасная связь с закрытым producer record без публикации private path. C1 явно требует known Evidence и unknown null, но не запрещает Evidence для redacted. Новый guard превращает любой такой genuine raw target.status=redacted в ошибку.

**Source-reproducible healthy record:**

1. Взять `case()` и заменить raw height.assigning на `{status:"redacted",kind:"config_file",source:null,rule:null}`. Никакого private pathname не добавлять. Переиздать exact Snapshot и необходимые dependent hashes/Evidence.
2. View.assigning задать теми же status/kind/source/rule и exact Evidence `execution_input:/inputs/0/assigning`. Used может оставаться known с прежним Atom и новым правильным snapshot digest; actual value_origin остаётся unknown.
3. `_last_assignment` возвращает этот точный raw redacted record. :880 отвергает его исключительно из-за status, хотя projection соответствует bytes и privacy contract. Замена на Evidence=null обходит всю новую ветвь и не является исправлением проверки согласованного Evidence.

**Требуемый исход:** exact genuine redacted projection принимается при соблюдении source=null и соответствующего kind/rule/Evidence; known не должен фабриковаться из redacted. Wrong leaf/source/status projection и private-path disclosure по-прежнему отвергаются. Нужна paired redacted healthy/contradictory control без weakening публичной C1 ветви. Это binding/privacy correction, не новое разрешение на private source attribution.

F3a и F3b относятся к незакрытому target-last-assignment finding, а не к пересмотру D2. Все counterexample outcomes здесь выведены из source control flow; код fixtures/reviewer не исполнялся и не изменялся.

## Остальные пять findings

| Finding | Actual correction и независимые controls | Source verdict |
| --- | --- | --- |
| F1 all-fragment semantics | :697–772 обобщает `_fragment(...,payload=bytes)`, проверяет retained Bundle equality и вызывает static semantic проверки для каждого payload fragment. New tests: selected safe/query и второй unselected safe/query/selector; exact hashes/annotation associations переизданы, selected identity не подменяется. | закрыт |
| F2 known identity erasure | :938–954 сохраняет known receipt source revision и сравнивает каждый emitted scalar включая null. Tests: четыре null mutations при retained identity и genuine missing evidence/null healthy. | закрыт |
| F4 causal selector scope | :852–868 требует exact required/supplied location sets для known. Tests сохраняют required steps и добавляют unrelated `/context`; original missing/replacement controls сохранены. | закрыт |
| F5 normal multipoint index | :281–334 и :800–849 отделяют shared child/execution/attempt от endpoint point, проверяют actual point membership/точный passport pointer, per-entry bytes/hash/size/inventory/context и selected alias. Aggregate проверяется до per-file decode. Новые healthy P1/P2 endpoint пары имеют разные declared и used, а sibling mismatch переиздаёт согласованные outer bytes/digests. Wrong point/passport/inventory/missing sibling/count/aggregate controls различающие. | закрыт в согласованном checked private layout |
| F6 declared passport | :774–797 проверяет known RawInput.declared Atom строгим kind/value/unit comparison с соответствующим point passport; used не приравнивается declared. Rehashed value/unit/kind negatives, distinct used, unknown declaration и genuinely missing passport healthy сохранены. | закрыт |

Private multipoint additions не обещают arbitrary plan reflection: owner по-прежнему supplies checked original frozen bytes, exact point associations и bounded original snapshots. `snapshot_files.inventory` — owning observation, не новый доверенный public boolean. Missing sibling proof fail-closed; valid sibling другого point больше не противоречит endpoint selection сам по себе. Проверка не устанавливает actual AiiDA/parser production integration.

Тестовый40274-byte prefix действительно сохранён byte-exact, не только по утверждению автора. Добавления не ослабляют прежние unknown ordering, source/mapping, review association, origin phase или full-chain assertions. D2:178 resolver порядок и origin proof paths не менялись по существу, кроме использования точного point passport для declared Evidence. No runtime GREEN claim по source tests делать нельзя; новые tests не содержат counterexamples F3a/F3b.

## Пределы и обязательный STOP

Source-only rereview: полный module delta, appended regression delta и actual changed ranges, named canonical/C1 shape clauses, точные hashes, original-prefix hash и read-only Git identity. Conservative current logical read charge2MiB ниже4MiB; cached prior evidence не перечитывалась целиком. Physical I/O/CPU/RSS не измерялись. Выход ниже128KiB. Runtime/import/parser/typecheck/tests/format/build/network/solver/server/children/Git mutation/product/checkpoint writes:0. Записи — только этот report и companion identity.

Original engineering cap8 исчерпан. Этот REQUEST_CHANGES фиксирует blocker и **не** разрешает автоматическую девятую правку, замену frozen tests, дополнительный runtime или silent change контракта. Shared DOC07 runtime used3/4 сохраняется по coordinator provenance; reviewer потребил0. Если coordinator выбирает дальнейшую engineering работу, её finite replan должен быть отдельным явным решением; этот отчёт сам такого grant не создаёт. Научная модель/criteria и native/public/finalCI gates не затрагиваются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1/F2/F4/F5/F6 имеют causal source repairs | Exact delta, controls и локаторы выше | Runtime и production integration не измерены | сохранить |
| F3 target-last-assignment полностью закрыт | F3a bypass и F3b false rejection в новом guard | Source trace, не executed failure | изменить |
| Candidate готов к полной C2 source acceptance | F3 остаётся открытым, cap8 исчерпан | Нет разрешённого automatic repair loop | данных недостаточно |
| Public/native/scientific acceptance выполнена | Свидетельств нет | Private software helper и synthetic fixtures | дополнительно измерить |

STOP — REQUEST_CHANGES, F3a/F3b; no execution, no cycle9 grant.
