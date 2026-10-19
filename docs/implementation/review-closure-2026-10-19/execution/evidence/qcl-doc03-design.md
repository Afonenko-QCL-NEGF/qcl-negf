# DOC03 — canonical model/source help и статическая публикация

Дата: 2026-10-19. Этап: **D**, проект интерфейса для independent CP-DESIGN.
Автор: `gpt-6.1-sol`, роль `ultra` по brief координатора. CP-DESIGN этим
документом не закрыт. Отдельный reviewer назначается координатором.

## 1. Задача, полномочия и исходники

Дать человеку и агенту одно содержание справки по модели, параметру и источнику,
с точной привязкой к selected source. Сохранить Documenter, существующие Julia
API и принятую физику. Различать смысл модели, происхождение численного значения,
последнее назначение входа и фактически использованный вход конкретного attempt.
Объём — проект контракта/публикации, а не реализация сайта или документации.

Авторский envelope: до 60 минут, 1 CPU, 2 GiB, чтение до 4 MiB, вывод до 128 KiB.
Выполнены чтение Git/source/docs и ограниченная обработка метаданных стандартной
библиотекой. Не выполнялись Git mutations, target imports, install, build,
tests продукта, browser/server/native/CI или solve. Изменены только файлы `/tmp`.
Защищённый исходный checkout `/home/tolya/Загрузки/qcl-negf` не изменялся.

Immutable normative base: root
`9d8cf0cad32743791cc3b80ac7c2a948dab02f48` в
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Первый `git status --short` показывал чужие изменения Core/Runner gitlinks,
checkpoint, deployment runbook и execution receipts; это не часть DOC03.
Полный status, recursive status и file SHA256 вынесены в соседний
`/tmp/qcl-doc03-source-identity.json`. Это receipt чтения, **не новый source lock**.
Для повторения исходной композиции первичны `git ls-tree <root> components/`
и Git objects; рабочий HEAD компонента не подставляется автоматически.

| Компонент | Selected gitlink root 9d8cf0c | Наблюдавшийся более новый source |
| --- | --- | --- |
| Core | `f7b108bef206d2b2dc5afe0306b2dff60d27ac59` | checked `90f1048d290d6ec9518754e288333c694fe874de`, SCI05 C1 runtime candidate, не selected gitlink |
| Runner | `23860d9e660a3cddf6cb5203d449d1b62f3745a1` | DOC02 authored/published head `9378396a3681c1eddf2c62f16674834fc4465583`, не selected gitlink |
| Contracts | `02a564b78dc9c5e19eacf496bc8c891361eafaab` | selected |
| Research | `1eacefcd81a50e245ea9da74a0b717b33818c61e` | selected |
| Portal | `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d` | selected |
| Platform | `b067723c82382689bff5cc366981c56e99b926f8` | selected |

DOC02 routes читались отдельно как согласованный источник reader journeys:
Core author head `239d76bb59c955b32888eeaec518d6e465b4178d`, Runner author head
`9378396…`. Published journal сообщает merge commits `45dddf3a…` и `6dc1d05b…`;
это journal facts, а не доказательство включения их в root 9d8cf0c. Никакого
следования `main/latest` нет. Перед DOC04 coordinator выбирает новый опубликованный
root с нужными gitlinks; build receipt не наследуется с другой композиции.

Прочитаны root AGENTS/architecture, DOC03, autonomy, P1 PERM14/18,
physics-documentation, документационная методика и owning CONTRIBUTING/Portal
AGENTS. DOC01 normative disposition: R11=`implement`, D10=`conditional` для
pilot/pins/serving, C06/R10 exact interfaces решает owning D+R. Исторические
PLAN/standby заголовки handoff не отменяют active EXEC из brief. Уже принятое
включение DOC07 не требует нового согласования с оператором. Изменение физики,
новый registry/toolchain/service/trust boundary сюда не входят.

Scientific scope сохраняется: S1 0 mV/period, lattice/LO 70 K, LO/acoustic/
impurity/IFR/alloy, electron–electron=none; справка по существующим expert
операторам не обещает их включения в этот расчёт. Fixed light действует на
Portal, docs и все loading/error/help states. Ни docs completion, ни hosting
всего corpus не являются prerequisite научного S01.

## 2. Что установлено по source

1. Root `ops/git.ts:sourceGraph` уже получает `qcl-negf.git-graph.v1` из Git
   gitlinks, проверяет checked-out revisions и clean source. `ops/release.ts`
   вкладывает этот graph в `qcl-negf.release.v2`; application release directory
   именуется SHA256 точных bytes `release.json`. Root commit, application
   release digest и documentation bundle digest — разные идентичности.
2. Root `julia/Manifest.toml` выбирает Julia `1.13.0` и Documenter `1.17.0`,
   package UUID `e30172f5-a6a5-5a46-863b-614d45cd2de4`, tree
   `56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`. Root `julia/Project.toml`
   выбирает Core/Runner через workspace paths. Standalone Runner docs имеют
   другую source selection (`Core v0.2.0`); она не подходит для release pilot.
3. Selected Core/Runner `docs/make.jl` используют Documenter, `prettyurls=false`,
   `doctest=true`, `checkdocs=:exports`, `warnonly=false` и импортируют пакеты.
   Root `ops/ci.ts` уже передаёт `QCL_NEGF_PROJECT=<root>/julia` в owning docs
   tasks. Build может импортировать/precompile и выполнять executable examples;
   это отдельный BUILD stage, не source-only extraction и не просмотр страницы.
4. Runner `src/application/configuration_types.jl:configuration_source` возвращает
   последнюю запись истории или `nothing`. `_deep_merge!` хранит absolute source
   filenames. Generated assignment markers и `application:auto_exact` объясняют
   назначение, не научный источник и не весь effective causal chain.
5. Contracts `run.schema.json:/properties/production/properties/energy_chunk`
   требует integer>=1 и явно не назначает schema default. Core
   `src/numerics/optimized/production_contracts.jl:ProductionOptions` отдельно
   задаёт typed default 64. Равные числа не устанавливают одинаковое происхождение.
6. Scientific plan имеет `model_revision=transport-contract-v2`, fingerprints,
   execution `resolved_configuration`/`provenance.sources` и point passports.
   Runner `_point_resolved_raw` применяет оси отдельно. Один `model_revision`
   не доказывает root release/source identity; planned value не доказывает used
   value после runtime planning. Missing execution snapshot остаётся unknown.
7. Research `config/model/reference-2019-70k.yaml` хранит Δ=0.10 nm, Λ=9.0 nm,
   fixed screening 0.20 nm^-1 и **56 mV**, а не принятый S1 0 mV. DOI в run
   description относится к геометрии/легированию, не подтверждает автоматически
   все material/scattering values. Это reference fragment, не паспорт S1 attempt.
8. Portal `api.py:create_app` ставит authenticated `/api/v1/…` routes и затем
   `app.mount('/', StaticFiles(..., html=True))`. Platform
   `modules/application.nix` проксирует `/` к API. Документационного mount нет.
   CSP — same-origin без внешних scripts/styles. Frontend `main.tsx` загружает
   frozen JSON plan; физического field configurator в selected source нет.
9. AiiDA service уже читает bounded frozen input/retrieved plan в actor
   (`get_export_plan`) и хранит optional WorkChain `release_id` при submission.
   Этот portable label сам по себе не равен Git SHA. Нужен сохранённый release
   manifest/receipt, который связывает именно этот label с graph; current
   deployment defaults для historical run не подходят.

Это source observations, не native/import/browser/scientific доказательства.

## 3. Варианты и выбранный минимальный путь

| Вариант | Три journeys DOC02 | Стоимость/ограничения | Решение |
| --- | --- | --- | --- |
| Static hub с тремя входами + existing Documenter search по каждому разделу + bounded JSON fragments | Исследователь идёт к SCBA/final assessment; разработчик к configuration_source/energy_chunk; оператор к recovery/runbook. Один hub связывает главы и reference | Нет общего cross-corpus ранжирования; три осмысленных входа и прямые anchors уже достаточны для pilot | **Выбрать** |
| Единый search adapter поверх inventories/search indexes всех generators | Полезен, когда reader question нельзя разрешить по разделу; мог бы объединить symbol/config/operator lookup | Ещё один index compatibility layer; нужно version isolation, ranking, snippets, offline/cold-cache controls. `objects.inv` не содержит value origin | Отложить до наблюдаемого gap DOC05 |
| Markdown/math renderer и поиск внутри React либо новый docs framework | Единая оболочка | Повторная реализация @ref/@docs/math/source links/theme и второй independently edited corpus | Не выбирать |

Выбранные URLs — proposed, сегодня не реализованы:

```text
/docs/<source_revision>/index.html
/docs/<source_revision>/core/theory/09_scba.html#researcher-scba-route
/docs/<source_revision>/core/theory/12_validation.html#researcher-final-route
/docs/<source_revision>/runner/user/configuration.html#developer-configuration-route
/docs/<source_revision>/runner/user/results.html#operator-recovery-route
/docs/<source_revision>/operator/recovery.html
/docs/<source_revision>/help/fragments/<fragment_id>.json
/docs/<source_revision>/bundle.json
```

`source_revision` — полный 40-hex root commit из existing graph. Это source URL,
не application release digest. Run разрешает его только через его retained
binding. Hub имеет три task links и обычные links на model/API/config references;
разделы сохраняют собственный offline search. Нового live Julia service, docs
VM, CMS, workflow DSL, общего model registry или research cache нет.

## 4. Один canonical source на каждый факт

«Один source» означает единственное owning место для каждого атомарного факта,
а не вручную поддерживаемую универсальную таблицу вместо владельцев.

| Факт | Canonical owner/source | Что материализуется |
| --- | --- | --- |
| Julia documented signature, units, effects/errors | Core/Runner docstring + typed declaration и проверки соответствующего symbol | Documenter @docs; fragment с source refs и extraction status. Documented signature не выдаётся за runtime method inventory |
| Declarative type/required/default/constraint | Contracts owning JSON Schema, `description` и существующие validation rules | Field reference по JSON Pointer. Schema default отсутствует — `not_assigned`; typed default хранится отдельным fact |
| Модель, assumptions, conventions, formula IDs, applicability/ограничения | Existing Core Markdown chapters/models/traceability | Full HTML; короткое authored пояснение в **одном** owning `docs/help/fragments.json` с refs в эти главы. Формулы не копируются в JSON/React |
| Источник конкретного material/model value, условия/uncertainty | Research `docs/help/value-origins.json` и выбранный parameter-set YAML | Value-origin annotation с public source refs; численные значения читаются из owning YAML, повторного набора чисел в help нет |
| Последний assigning source | Runner recorded provenance того же plan/execution/leaf | Sanitized structured assignment. `configuration_source` — один из inputs адаптера, не вывод scientific origin |
| Planned/used inputs, point axes, runtime resource override | Runner frozen point passport + retained execution input/strategy snapshot | Bounded projection. Plan и used snapshot различаются. Отсутствующие части не реконструируются по default или совпадению числа |
| Presentation и serving | Portal/Platform | Чтение этих bytes, ссылки и unknown/error states; никаких физических формул или новых критериев в UI/scheduler |

Proposed authoring files содержат только короткий текст/семантические refs и
provenance annotations. Это не model registry: нет API выбора модели, вычисления
derived input или live resolution. Если fact уже имеет canonical текст, annotation
ссылается на него. Изменение поведения сопровождается owning docstring/schema.

Первый help slice: IFR, fixed screening, LO и masses/band offsets выбранного
reference parameter set; DOC06 fixed API/config slice — `configuration_source`
и `production.energy_chunk`. Наличие этого slice не означает coverage всех
активных leaves. Unknown mapping виден явно, а не молча связывается по имени.

## 5. Exact proposed contract

Contracts владеет одним schema resource `model-help.schema.json` (Draft 2020-12)
с `$defs` для bundle, fragment и view. Все описанные objects имеют
`additionalProperties:false`; версия `v1` принимает только перечисленные поля.
Это proposed format после CP-DESIGN, а не существующий Contracts API.

Общие типы:

- `Sha1` — `[0-9a-f]{40}`, `Sha256` — `[0-9a-f]{64}`.
- `Id` — `[a-z][a-z0-9._-]{0,127}`; один fragment на URL/response.
- `PublicRef` = `{component, revision, path, selector, sha256}`. Component — один
  из source graph paths или `root`; revision ровно выбранный commit владельца;
  path — нормальный repo-relative POSIX file из input allowlist; selector —
  `{kind: 'symbol'|'anchor'|'json_pointer'|'file', value: string}`; file selector
  имеет пустое value. SHA256 относится к полным source bytes, не к вырезке.
- `DocRef` = `{section, path, anchor}`: section=`core|runner|research|operator`,
  path — allowlisted relative `.html`, anchor — существующий ID либо `null`.
  URL строится только относительно exact `/docs/<source_revision>/`.
- `Origin` = `{status, kind, locators, note}`. status=`known|unknown|not_applicable`;
  kind=`publication|measurement|interpolation|fit|research_assumption|code_policy|unknown|not_applicable`;
  locators — массив `{title, uri, location}`. URI только `https:`/`doi:` без
  credentials/query secrets; location — точная формула/таблица/раздел/страница.
  Для unknown: kind=unknown, locators=[], note обязателен. Known исследовательское
  допущение допускает locators=[], но note называет явное owning assumption;
  наличие DOI не превращает kind в measurement. `note` — plain text.
- `Atom` = `{kind, value, unit}`. kind=`quantity|integer|number|boolean|enum|null`;
  value — scalar JSON соответствующего типа, finite numbers only; unit —
  canonical строка единицы, `1` для dimensionless, `null` при неприменимости.
  Никаких массивов, объектов, NaN/Inf. Known-null отличается от отсутствия.
- `Fact` = `{name, status, text, sources}`. name — один из десяти классов:
  `signature`, `units`, `default`, `constraint`, `effects`, `errors`,
  `formula_origin`, `value_origin`, `assigning_origin`, `effective_origin`.
  status=`known|partial|unknown|not_assigned|not_applicable`; text — plain text
  или null; sources — PublicRef[]. Unknown/partial не считается extraction pass.
  Default facts явно называют контекст schema/typed constructor/example; known
  dynamic/default невозможно получить по одному имени/пустой history.

### 5.1 `bundle.json`: output build, input static server/help resolver

| Поле | Тип/точное содержание |
| --- | --- |
| `format` | const `qcl-negf.docs-bundle.v1` |
| `sources` | existing `qcl-negf.git-graph.v1` object из `sourceGraph`: format, revision, sorted components[{path,revision,url}]; generated, не новая таблица pins |
| `schema` | PublicRef на Contracts `model-help.schema.json`, selector file |
| `generator` | `{name:'Documenter', version:'1.17.0', uuid, git_tree_sha1, julia_version:'1.13.0', project_sha256, manifest_sha256, recipes:PublicRef[], toolchain_lock:PublicRef}`; uuid/tree как в §2 |
| `fragments` | descriptors `[{id, file, sha256}]`, unique id/file; file ровно `help/fragments/<id>.json` |
| `files` | `[{path, media_type, bytes, sha256}]` всего публичного payload, включая HTML/CSS/JS/fonts/math/search/JSON; unique normalized paths; `bundle.json` исключён из self-hash списка |
| `aliases` | `[{from, to}]` version-local DocRef; aliases должны иметь реальную сохранённую HTML page/anchor, не только запись в index |

Идентичность manifest — SHA256 exact UTF-8 bytes `bundle.json`; хранится во внешнем
build/publication receipt, не рекурсивно внутри самого manifest. Application
`release.json` не редактируется задним числом ради добавления docs digest.
Production publication receipt связывает existing `release_id`/retained release
manifest SHA256, sources.revision и bundle SHA256. Для standalone source docs
application binding может отсутствовать; тогда UI не заявляет installed release.

### 5.2 Static fragment: output Core/Research + bounded extraction

| Поле | Тип/содержание |
| --- | --- |
| `format` | const `qcl-negf.model-help-fragment.v1` |
| `id` | Id: например `model.ifr` или `config.production.energy_chunk` |
| `source_revision` | root Sha1, равен bundle.sources.revision |
| `title`, `summary` | plain text, max 160 / 1600 Unicode characters; summary authored один раз в owning source |
| `scope` | `baseline|variant|operator_only|outside_study`; scope привязан к documented model context, не выводится из feature наличия |
| `meaning_source` | PublicRef owning Core/Runner scientific/API explanation |
| `full` | DocRef полного owning объяснения |
| `related` | DocRef[] учебных/формальных/API продолжений, максимум 12 |
| `equations` | `[{id, doc}]`, id существующего equation ID (например EQ-KIFR-001), doc=DocRef; формулы здесь не повторяются |
| `inputs` | `[{path, schema_source, facts, value_origin}]`; path — whitelisted dotted config leaf, schema_source=PublicRef с JSON Pointer, facts=Fact[], value_origin=Origin |
| `api` | `[{symbol, source, doc, facts}]`; public symbol, PublicRef, DocRef, Fact[] |
| `assumptions`, `limitations` | массивы короткого plain text, по максимум 12×400 chars; длинный вывод остаётся в full |

`facts` покрывают все десять классов для fixed slice; неприменимое явно
not_applicable, отсутствие annotation/extraction явно unknown/partial. В
static fragment `assigning_origin`/`effective_origin` описывают **семантику** и
source функции, без частных значений или истории конкретного run. Для numeric
leaf нет автоматического DOI или pseudo-formula из его имени.

### 5.3 Run view: output read adapter, input человек/агент/Portal

Новый proposed authenticated endpoint:
`GET /api/v1/runs/{run_uuid}/model-help?fragment_id=…&execution_id=…&point_id=…&attempt=…&calcjob_uuid=…`.
Все selectors bound к одному существующему run; execution/point обязательны;
attempt и calcjob_uuid выбираются по уже действующим правилам AiiDA selection.
Неоднозначность не разрешается выбором первого result. Нет path/query URL от
пользователя, batch всех leaves или обхода actor ownership.
UUID канонический полный; execution/point имеют existing scientific identifier
grammar, fragment_id — Id, attempt — положительный integer. HTTP 401 сохраняет
existing auth; malformed selectors — 422, absent run/execution/point — 404,
ambiguous/conflicting attempt selection — 409, actor unavailable — existing 503.
Для существующего context unknown/incompatible/unavailable binding возвращается
HTTP 200 с typed status/reason и fragment=null: это metadata о недоступности,
а не successful scientific/help binding. Неизвестный syntactically valid fragment
даёт unavailable/fragment_missing; static JSON URL для него отвечает 404.

| Поле | Тип/содержание |
| --- | --- |
| `format` | const `qcl-negf.model-help-view.v1` |
| `context` | `{run_uuid, execution_id, point_id, attempt, calcjob_uuid, plan_fingerprint, scientific_fingerprint, configuration_hash, model_revision}`; SHA256 fingerprints от exact frozen plan; attempt/calcjob/configuration_hash допускают null только когда evidence отсутствует |
| `binding` | `{status, release_id, release_manifest_sha256, source_revision, bundle_sha256, reason}`; status=`bound|unknown|incompatible|unavailable`; unknown scalar fields=null; reason — enum ниже |
| `fragment` | `{id, url, sha256}` либо null; url только allowlisted static JSON того же exact source revision; содержимое не переписывается в API |
| `inputs` | bounded `InputView[]` только paths из fragment.inputs; максимум 32 |

`InputView` имеет **ровно** `{path, declared, used, assigning, effective_origin}`:

- `declared` и `used` = `{status:'known'|'unknown', atom:Atom|null,
  evidence:Evidence|null}`. Known требует atom и evidence. Unknown требует оба
  null. `declared` читается из retained frozen point-resolved configuration;
  `used` — только из retained execution input/strategy snapshot того же attempt.
  Plan или current default не заполняет missing used. Point axes читаются из
  point passport/explicit axis mapping Runner, не из template первой точки.
- `assigning` = `{status:'known'|'unknown'|'redacted', kind, source, rule, evidence}`.
  kind=`config_file|generated_assignment|typed_constructor|execution_strategy|point_axis|unknown`;
  source=PublicRef|null; rule=allowlisted producer rule ID|null;
  evidence=Evidence|null. Known должен иметь source или rule и evidence;
  unknown имеет kind=unknown и null поля. Private source path означает redacted,
  source=null; его basename/absolute path не возвращаются. Presence of a scalar
  не разрешает kind=typed_constructor. Последняя recorded assignment не заменяет
  историю полного effective origin.
- `effective_origin` = `{status:'known'|'partial'|'unknown', evidence:Evidence[]}`.
  Полное known требует всех применимых retained planning/runtime steps; missing
  chain даёт partial/unknown, даже если assigning известен.
- `Evidence` = `{container, sha256, selector}`. container —
  `frozen_plan|execution_input|execution_strategy|release_receipt`; sha256 — exact
  bounded metadata bytes, selector — allowlisted JSON Pointer внутри них.
  Raw file paths, handles/ORM objects и свободные server URLs не возвращаются.

Причины binding: `ok|source_binding_missing|wrong_release|bundle_missing|unsupported_version|fragment_missing`.
`fragment=null` при unknown/incompatible/unavailable: нельзя показывать current
карточку как помощь этого run. Отдельная явная ссылка «Справка текущего релиза»
возможна вне run-bound карточки с соответствующей подписью.

Будущий Runner adapter — владелец projection/field mapping и `used` semantics.
Для новых attempts выбран один bounded output `result/model_help_inputs.json`
(<=64 KiB), создаваемый в существующем persistence path. Его exact top-level
поля: `{format, context, source_binding, phase, inputs}`. Format — const
`qcl-negf.model-help-inputs.v1`; context как выше; source_binding —
`{status, release_id, release_manifest_sha256, source_revision}` с
status=`bound|unknown`, nullable неизвестными identity fields. Bound возможен
только по retained source receipt именно этого execution, не current deployment.
Phase=`planned|solver_input`; solver_input означает значения, фактически
переданные при входе в solver, **не** scientific acceptance или доказанную
постоянность derived quantities на всех итерациях.

Каждая snapshot inputs запись имеет те же path/declared/used/assigning/
effective_origin, но без полей evidence: declared/used={status,atom}, assigning=
{status,kind,source,rule}, effective_origin={status,steps}. Steps — bounded массив
`{kind,source,rule}`, kind=`configuration_merge|point_axis|execution_strategy`,
source=PublicRef|null, rule=allowlisted producer ID|null. Статусы и atom/source
invariants сохраняются. Это исходная scalar projection; API добавляет Evidence
по SHA256 **всего закрытого snapshot** и JSON Pointer записи. Поэтому нет
циклического self-hash. Для external strategy step отдельный Evidence допустим
лишь при наличии retained metadata bytes; одного имени rule недостаточно, чтобы
назвать causal chain полным. В phase=planned used всегда unknown.

Runner снимает solver_input после применения point axes и execution strategy,
по тем же arguments/options, которые передаёт solve; никакого второго resolver
ради help. Adaptive/derived величина без соответствующего retained свидетельства
остаётся partial/unknown. Snapshot покрывает только allowlisted fragment leaves,
не копирует всю конфигурацию. Serialization/size failure означает недоступность
help snapshot и явный diagnostic; scientific status не подменяется help status.

Добавление требует coordinated Runner/Contracts/reader diff после CP-DESIGN;
сегодня output не существует и не заявлен проверенным. AiiDA/Portal используют
existing bounded artifact read path/actor и allowlisted logical name, не
произвольный файл. Для historical/no-snapshot run допускается bounded projection
declared из существующего frozen plan; used остаётся unknown. Нет full HDF5,
arrays/logs, costly derivation или повторного solve для заполнения справки.
Новый output не меняет scientific-plan schema, fingerprints или scientific
identity существующих результатов. Старые artifacts не дописываются.

### 5.4 Unknown example и совместимость

Пример — authored **reference help**, не observed S1 run:

```json
{
  "path": "physical.interface_roughness_height",
  "value_origin": {
    "status": "unknown", "kind": "unknown", "locators": [],
    "note": "Источник конкретного Δ=0.10 nm в reference parameter set не подтверждён; DOI геометрии его не устанавливает."
  }
}
```

При известной assignment к public Research YAML можно показать этот source
отдельно. Если есть только frozen plan, `declared` содержит 0.10 nm с evidence,
`used` остаётся `{status:'unknown',atom:null,evidence:null}`. Unknown не блокирует
сам по себе exploratory вариант, не становится published/measured и не доказывает
scientific acceptance. У typed energy_chunk=64 отдельно видны constructor
default и `schema default: not_assigned`; отсутствующая history не выбирает первый.

v1 consumer принимает только известные const format и проверенные bytes/hash;
unknown major/неподдерживаемый format -> incompatible, без best-effort reinterpretation.
Никакой совместимости по package `0.2.0`, `transport-contract-v2`, одинаковому
fragment ID или числу. Default rule — exact graph equality. Старый run с известным
graph использует его retained bundle; если bundle отсутствует — unavailable.
Future explicit compatibility mapping потребует отдельного reviewed contract;
сегодня его нет. Unknown source run остаётся unbound, даже если release_id совпал
по тексту с current label. Redirect на latest не исправляет несовместимость.

## 6. Allowlist, пределы и сборка

Input allowlist build: selected component `docs/src/**`, explicit docstring/type
source paths для fixed slice, Contracts schema resources, explicit Research
public configuration + `docs/help/value-origins.json`, reviewed Root operator
chapter. Path list точная и versioned в recipe; glob всего worktree/archives нет.
Наличие private path в source metadata не разрешает публикацию его basename.

Public output allowlist: перечисленные manifest HTML/CSS/JS/fonts/math/search,
images SVG/PNG/WebP, approved JSON fragments/catalog и optional inventory.
Запрещены symlinks, абсолютные paths, `..`, backslash, NUL/control chars,
URL-decoding traversal, dotfile directories, private inventory, .git, .aws,
logs/receipts с private targets, arrays/HDF5, depots, source maps с machine paths,
credential/query/token bytes. SVG/HTML/JS только из selected reviewed recipes и
public authored source; нет dynamic user HTML. Статическая карточка plain text,
React не рендерит arbitrary HTML. Links на первоисточники не загружаются автоматически.

Пределы proposed публичного catalog: manifest<=2 MiB, fragment<=32 KiB,
<=256 fragments/пилот, max help response<=64 KiB. Files listing содержит byte counts;
любой overrun — replan соответствующего artifact, не truncation посреди JSON.
Runtime reads используют меньший из этих пределов и existing actor/API limits.
Actual HTML/assets budget DOC04 задаётся по measured BUILD admission и manifest;
этот design не утверждает размер или скорость ещё не собранного corpus.

Выбран **existing Documenter 1.17.0** с root Julia 1.13.0 manifest. Hub/catalog
collector — небольшой source-only adapter на existing locked Deno toolchain из
root/platform flake, без нового generator dependency или network access. JSON
Schema extraction использует normal JSON, remote `$ref` не fetch. Для Julia
fixed slice DOC06 распознаёт лишь заявленные source constructs; unsupported
dynamic expression возвращает partial/unknown и source locator. Target modules,
extensions/plugins/config evaluation не импортируются. `objects.inv` и готовый
Documenter search index допускаются как generated link/index inputs после
проверки их version/schema в DOC04, не как provenance чисел.

Prerequisites DOC04 (проверить, не запускать здесь):

1. Новый published clean root с DOC02/Contracts/help source gitlinks и locked
   workspace; `sourceGraph()` до/после build совпадает. Recipe/source hashes и
   Project/Manifest hashes входят в receipt. Root 9d8cf0c сейчас dirty/mismatched
   для реального `sourceGraph()` release build и не является ready build input.
2. Проверенный existing Julia executable/depot matching manifest; exact installed
   version/tree Documenter и package import effects. Deno executable/version/store
   identity сверяются с selected root/platform flake lock. Сейчас installed paths
   и binary versions **не измерены**, нельзя назначить найденный PATH `deno` pin.
3. Прочитать source/API **pinned** Documenter для local math/fonts/search и theme;
   сохранить fixed-light без switcher/OS auto-dark, local assets. Не выдумывать
   HTML kwargs по документации latest. Required CDN/font/math downloads должны
   быть закрыты локальными pinned assets в recipe; отсутствие pin блокирует
   этот render, не ведёт к установке latest.
4. Импортирующий render выполняется только в DOC04 BUILD envelope на fresh
   builder admission. Existing docs command с QCL_NEGF_PROJECT использует root
   workspace. Без него standalone task может instantiate другую композицию.
   Не использовать full `deno task test` или CI как обёртку pilot.
5. Проверить все executable jldoctest/@example/import/precompile effects до
   render. Обычные fenced snippets — текст. Solver/SCBA/Poisson в build/view
   запрещены; executable examples, если нужны, получают отдельный bounded
   contract. Нет изменения scientific gates ради успешной сборки.
6. Three pilot slices: Core физическая глава/SCBA route, Runner API/config route,
   Root operator recovery chapter. Небольшой reviewed operator HTML создаётся
   existing Documenter из authored public chapter; весь исторический deployment
   runbook или execution receipts автоматически в public docs не копируются.

## 7. Serving, anchors, offline и UI

Owning Platform передаёт immutable documentation bundle path; Portal монтирует
его **на `/docs` до последнего `/` static mount**. Nginx может продолжать
существующий `/` proxy: отдельный nginx alias в pilot не нужен. Это сохраняет
same-origin headers/CSP и не добавляет альтернативный auth/serving путь.
Нет serving arbitrary filesystem root или user-controlled directory.

Public docs содержат только public allowlist source; auth API остаётся protected.
Request `/docs/<rev>/missing.html` -> docs 404, не Portal index; `/api/v1/…`
не попадает в docs. Даже при отсутствующем documentation directory prefix
резервируется и возвращает docs unavailable/404 до Portal catch-all. Startup
binding проверяет manifest/hash/schema once без Julia; ошибочный docs bundle
не должен выключать unrelated API или давать ложный help pass.

`/docs/<rev>/…` immutable URL получает immutable cache/ETag по payload hash;
API view сохраняет existing no-store. `/docs/current` — необязательный explicit
deployment redirect к конкретному source revision, отдельно опубликованный с
activation receipt. Run-bound ссылки его не используют. Не менять pointer
самовольно после preview acceptance.

Existing headings/explicit @id сохраняются; DOC02 anchors проверяются только
после выбора соответствующих gitlinks. Fragment anchors не передаются серверу:
old `#anchor` сохраняется реальным alias element в owning HTML. File aliases
также реальные pages/redirects; их targets остаются в той же версии, если
явная migration не заявлена. Retained old bundles обслуживаются по exact URL;
удалённая неизвестная версия -> явный 404/unavailable, без перенаправления на
current. Source links могут идти на exact public commit и требовать интернет;
чтение главы, math/fonts/search/direct anchors от него не зависит.

Offline означает cold-cache browser с заблокированной **внешней** сетью при
доступном локальном origin; при копировании bundle поддерживается локальный
HTTP static preview. `file://` не обещается: search/fetch может иметь другие
ограничения. Все internal links и assets relative к version prefix; без CDN,
external fonts/search analytics или service worker, подмешивающего другую версию.
CSP не ослабляется глобально ради docs. Если pinned math renderer конфликтует
с existing CSP, DOC04 подбирает source/asset recipe; новая trust/CSP exception
возвращается на review до publication.

DOC07 UI: светлая «Модель и источники» рядом с существующей submit form и на
странице selected run/point. Статический reference доступен без запуска plan;
used карточка требует точных retained selectors/binding. Сохраняются введённые
plan bytes и submission behavior. Панель показывает summary, declared/used,
assignment/value origin и full link; full docs открываются отдельной страницей,
iframe и новый field configurator не нужны. Keyboard focus, close/return,
contrast/loading/error/unknown states проверяет DOC05. Простой просмотр не
вызывает resolve, derive, hash full result, Julia или solve.

## 8. Acceptance — пять обязательных отрицательных случаев

Ниже **будущие** проверки/controls, сегодня они не исполнялись.

| Случай | Инъекция/вход | Требуемое наблюдение | Positive control / evidence |
| --- | --- | --- | --- |
| Wrong release | Run receipt связан с graph A, установлен bundle B с тем же fragment ID | binding incompatible/wrong_release; used help B не показан и не fallback current. Если retained A есть, разрешён exact A | Совпадающие receipt/graph/manifest/fragment SHA дают bound; сохранить JSON/network/UI receipts |
| Missing source | Manifest/fragment обещает known PublicRef, но выбранный Git blob/selector отсутствует или hash иной | Build binding validation отказывает этому required fragment/bundle; не создаёт ссылку якобы known. Historical run без source receipt возвращает source_binding_missing | Существующий exact blob + selector проходит source check; fake missing source control не смешивать с допустимым unknown value origin |
| Private path | История assignment `/private/site/…`, traversal/symlink либо source-map с machine path в output | Публичный build исключает/отклоняет unsafe payload; dynamic assignment redacted без absolute path/basename. API selector не допускает file path | Public Research repo-relative source разрешён; проверить exact response bytes и output manifest, без вывода secret contents |
| Unknown origin | Δ=0.10 nm задано явно, DOI значения отсутствует; assignment существует | Значение/assignment видны отдельно, value origin unknown, used unknown без execution evidence. Никакого 0/выдуманного DOI/measured status и запрета exploratory только из help | Known value source с точной таблицей/формулой отображается как соответствующий kind; пустая history energy_chunk=64 остаётся unknown assignment |
| Catch-all routing | Direct `/docs/<rev>/…#anchor`, missing docs asset/page, docs directory absent, API URL и root UI | Valid direct page/anchor работает; docs misses дают docs 404, не Portal HTML200; API auth и existing root UI сохранены | Cold-cache direct known page + asset, authenticated API и root navigation; route tests + browser offline/light receipts |

Дополнительные bounded controls: unsupported format/version, wrong manifest hash,
nonexistent fragment, malformed schema, no/multiple selected point, generated
axis override, auto_exact strategy, historical run, unavailable bundle, target
module sentinel без side effect при DOC06 source-only extraction. Request/load
help не увеличивает счётчик запуска solver/build. Никаких numerical accuracy
claims из этих tests. DOC05 отдельно проверяет cold cache, offline math/fonts/
search, dark/light OS + saved preference при неизменно светлом сайте, focus и
потребление exact bundle. DOC04 build exit не заменяет эти observations.

## 9. Handoff после independent CP-DESIGN

1. Contracts I medium: один shared schema с primitives/fixtures и bounded
   validation, negative+healthy controls; отдельный owning PR, затем published
   root gitlink. Не изменять scientific-plan semantics ради help.
2. Core/Research/Runner I medium: owning short fragments/refs/value annotations;
   source-only fixed slice DOC06; separate declarations/assignments и выбранный used snapshot
   adapter. Недостающий runtime/source input блокирует только его claim/field.
3. DOC04 I medium + BUILD admission: existing pinned Documenter recipe, light
   local asset closure, hub/catalog и public manifest/receipt для трёх slices.
   Imported render и static extraction имеют отдельные receipts. Один candidate
   и corrections только в конечном DOC04 envelope; в этой D нет build grant.
4. Portal/Platform I medium DOC07/serving: mounted prefix до catch-all, bounded
   protected run view, same canonical JSON для человека/агента; если нужна
   дополнительная AiiDA/Results read projection, она идёт через existing owner/
   actor/metadata limits отдельным owning diff, без нового сервиса.
5. Independent CP-CODE и DOC05 подтверждают фактические routes/bytes/browser
   behavior. Preview не является production serving pass; OPS binding и
   deployment остаются отдельными gates. CI-once на final ready source сохраняется.

Это последовательность готовности и владельцев, не запуск реализации автором D.
Новый interface вопрос возвращается D; уже принятое включение help не выносится
повторно оператору. Missing pins/import facts блокируют соответствующий build,
а статическая contract/content работа продолжается. Никакой claim переносом
source facts в runtime/native/scientific pass не закрывается.

## 10. Самопроверка и итог

Автор проверил scope against DOC03 acceptance, canonical ownership, consumer/
producer поля, пять negatives, различение unknown/known-null/default, exact source
vs newer candidate, отсутствие source/runtime/scientific смешения. Source hashes
позволяют independent review того же набора. Это авторская проверка текста;
fresh reviewer и CP-DESIGN verdict ещё требуются. Tracked diff не создавался;
никакого product/render/browser/numerical test pass не заявлено.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing Documenter и source graph достаточны для минимального documentation artifact | Root ops/git.ts/release.ts, julia locks, selected owning docs/make.jl; §§2–3 | Asset closure/theme/import effects ещё не измерены | сохранить |
| Exact help contract может сохранить всех владельцев и три вида происхождения | §4; schema/fragment/view fields §5; Runner provenance source | Proposed contract, не implemented API; historical used/source может отсутствовать | изменить |
| DOC07 включён текущим scope, новый физический configurator не нужен | DOC01 R11/D10 dispositions, P1 PERM14, selected Portal main.tsx | Per-field UI/editing вне этого минимального design | сохранить |
| Historical help нельзя привязывать по текущему default/model_revision | Selected scientific plan/source/assignment code; §5.3–5.4 | Retained release receipt не исследован для конкретного run | данных недостаточно |
| `/docs` перед Portal static mount устраняет silent fallback по проекту | Selected api.py mount order, Platform proxy; §7 и routing negative | Runtime/production nginx/browser пока не проверялись | дополнительно измерить |
| Unknown source не становится 0, DOI или measured/used evidence | Origin/InputView invariants и unknown negative | Не устанавливает scientific applicability Δ/Λ или S1 acceptance | сохранить |
| DOC03 D готов для независимой оценки | Frozen report + source identity SHA256; весь acceptance checklist | Автор не закрывает собственный CP-DESIGN; реализации/CI/native/solve не было | дополнительно измерить |
