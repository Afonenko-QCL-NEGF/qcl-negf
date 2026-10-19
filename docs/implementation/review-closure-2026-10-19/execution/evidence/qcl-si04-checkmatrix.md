# SI04 — three-route dispositions и preservation checklist

Статус **author design candidate**; это static/source review, не independent CP-DESIGN,
не формальная SI07/forward behavior приёмка. Before tree `/tmp/qcl-si04-baseline`,
after tree `/tmp/qcl-si04-candidate`; ровно четыре reference paths, без SKILL/UI edits.

## Каждая reference: все три маршрута

| Reference | Current source-only | Immutable archive | Standalone installation | Решение |
| --- | --- | --- | --- | --- |
| `qcl-research-framing/references/brief.md` | `.agents/skills/qcl-research-framing/references/brief.md:13` — code/model question без обязательного run; selected refs и evidence level | `.agents/skills/qcl-research-framing/references/brief.md:14` — archived identity/frozen plan/reader compatibility; current defaults не подставляются | `.agents/skills/qcl-research-framing/references/brief.md:15` + `.agents/skills/qcl-research-framing/references/brief.md:17` — essential task content доступен без root; конкретный missing owner doc | изменить |
| `qcl-physics-audit/references/physics-checks.md` | `.agents/skills/qcl-physics-audit/references/physics-checks.md:12` — independent source/formula/discretization question без raw; source не runtime pass | `.agents/skills/qcl-physics-audit/references/physics-checks.md:13` — archived model/criteria/source, version-compatible reader, current audit отдельно | `.agents/skills/qcl-physics-audit/references/physics-checks.md:14` + `.agents/skills/qcl-physics-audit/references/physics-checks.md:16` — supplied fragments/refs; точный недоступный commit/path, без install/fabrication | изменить |
| `qcl-results-analysis/references/comparison.md` | `.agents/skills/qcl-results-analysis/references/comparison.md:11` — reader/format source check без result claim | `.agents/skills/qcl-results-analysis/references/comparison.md:12` — archived declaration выбирает compatible primary reader; transport/native compatibility отдельно | `.agents/skills/qcl-results-analysis/references/comparison.md:13` + `.agents/skills/qcl-results-analysis/references/comparison.md:15` — available package/version может быть достаточен, root не обязателен; missing reader/data точно ограничивает claim | изменить |
| `qcl-performance-audit/references/telemetry.md` | `.agents/skills/qcl-performance-audit/references/telemetry.md:12` — observability/hypotheses, без выдуманных measurements | `.agents/skills/qcl-performance-audit/references/telemetry.md:13` — archived producer/runtime/metric contracts/actual logs/counters; scientific comparability до speedup | `.agents/skills/qcl-performance-audit/references/telemetry.md:14` + `.agents/skills/qcl-performance-audit/references/telemetry.md:16` — supplied metadata+compatible reader и exact owning gap; без profiler/install | изменить |

## Before/after preservation

| Требование / исходная проблема | Before | After / evidence | Disposition и предел |
| --- | --- | --- | --- |
| Неизвестные не угадывать; framing не заменяет выполнение анализа | Brief: unknowns/domain questions/stop rules; SKILL narrow trigger | Brief table сохранён по предметам, ownership/evidence/stop/resume уточнены; все 4 SKILL+4 UI hashes неизменны | сохранить; целый skill behavior не тестировался |
| Один canonical task contract | Старый scientific brief table мог читаться как competing form | Ссылка locator на existing nine-field contract и явное «предметные подсказки/не вторая форма»; standalone essential content без registry | изменить; mandatory field schema не копируется |
| Scope/grants, no automatic expensive stage, already authorized route | Existing SKILL/root autonomous boundaries | Во всех refs сохранён scope; нет нового perpetual approval flow, missing только dependent; current поручение важнее historical context | сохранить; документ не выдаёт grant |
| Physics applicability и independent oracle | Physics table содержал spectral/FDR equations в skill | Вопросы units/conventions/Green/PSD/spectral/conservation/current/energy/equilibrium/windows/observables сохранены; формулы перенесены в owning locator, а не переписаны | изменить; новые physics equations/thresholds не создавались |
| U/G/raw residual/final checks и invariant model | Root + physics SKILL; reference generic checklist | Явно сохранены source/metadata/runtime/science, raw-versus-mixed, same-state U/G, independent oracle, no criteria/model drift | сохранить; fresh-map measurement не выполнялось |
| Current lookup не archived source | Physics/comparison/telemetry root `efb687...` и line locators стояли рядом с current language | Fresh path/symbol map датирован 2026-10-19; old snapshot отдельно; actual selection через Git, не новый manual revision table | изменить; map dated, будущая доступность требует recheck |
| Legacy multipart limit не universal export ceiling | Comparison fixed byte cap + «current README declares native version» | Numeric cap/schema/version copies удалены; owning archive dispatcher + legacy transport + native reader + declaration support названы раздельно | изменить; старый archive не был дан, чтение не запускалось |
| Version-compatible primary reader | Generic «find reader» without route | `archive.py::receive/verify_archive`, `multipart.py::receive`, `state.py::StateReader`, `native.py::validate_native_handle`, declarations из selected owner | изменить; source availability не runtime compatibility witness |
| Inventory/comparability/negative attempts/derived proof | Comparison original identity/physics/discretization/method/result/cost rows, near-zero absence | Все 6 groups сохранены; archived definitions и reader version раздельно; failed/paused statuses/derived/ranges и HDF5 slices/evidence intact | сохранить |
| Performance semantic boundaries | Telemetry old detailed table смешивал code observations/defaults/proposed cadence | Current symbol map без line numbers/default constants; process-inclusive/nesting/coverage/identity/null/JIT/peak/durability scopes сохранены | изменить; численной performance claim нет |
| Historical absence production data/sampler не current fact | 2026-09-28 snapshot negative inventory/source observation | Отдельный historical section сохраняет дату/root и ограниченность; не выводит отсутствие пользовательских artifacts или current collector | сохранить; новый production inventory не проводился |
| Proposed measurement не observed config/grant | Telemetry old cadence/buffer/overhead numeric proposals | Minimal measurement questions и owners сохранены, fixed proposed numbers не копируются; finite caps от порученного contract/admission | изменить; никакого profiler/calibration/benchmark |
| No duplicated formula/threshold/schema payload | Physics algebra, comparison schema/cap constants, telemetry fixed buffer/cadence values | Содержательный manual review: только вопросы, symbols и owner pointers; нет equation blocks/threshold assignments/schema field tables | изменить; это semantic review, не regex behavior score |
| Standalone exact gaps | Old «find root/request source» could block any work | Essential content and supplied-material route in all 4; exact archived owner path/version named; missing only dependent claims | изменить; existing SKILL wording addressed later SI05 |
| Portable relative Markdown links | References depended conceptually on full root, mostly code paths | Every new relative Markdown link is `../SKILL.md`, resolves inside own minimal copied package; root/owner paths explicitly textual optional locators | сохранить; root docs сами в standalone bundle не включались |
| External primary bibliography | Physics/performance links date2026-09-28 | Exact external URL set unchanged; dates/abstract-only limit maintained | сохранить; новой web проверки нет |
| Archive/source provenance and physical/durability protections | Root AGENTS/P1/PORTABILITY | Originals untouched, no archived scripts/migrations, no reinterpret missing0; whole source/physics gates not replaced by skill verdict | сохранить |
| SI04 scope только refs | Four paths allowed, SKILL/UI SI05 separately | Exact four proposal paths; eight protected SKILL/UI hashes unchanged, root/native files untouched | сохранить |

## Static cases — ожидаемый route, не forward samples

| Вход | Ожидаемое действие/вывод | Ограничение / решение |
| --- | --- | --- |
| Source-only Core question без archive | Physics/brief source route, selected source + independent oracle reasoning | No mandatory run; runtime/science unknown; сохранить |
| Старый multipart transport с неизвестным native layout | Establish transport+native declared versions separately; require compatible reader evidence | Current README/main не fallback; gap только dependent interpretation; сохранить |
| Standalone skill + fragment paper/source, root нет | Essential task fields + supplied material audit; name unavailable owner document/version | Не fabricated formula/schema, no auto install; сохранить |
| Telemetry null/absent CPU/RSS/JIT | Preserve missing/coverage scope; report observability gap | Not0/not pass; propose only bounded measurement if needed; сохранить |
| Active already-authorized read/check | Execute within assigned stage/budget and technical prerequisites | No repeated human approval; missing only dependents; сохранить |
| Historical `/home`/`/tmp` report locator after clone | Use dated source receipt/PORTABILITY mapping and original object/hash | Absolute path не обещание наличия; missing original не reconstruct; сохранить |

`PORTABILITY.md` original review corpus не модифицирован. Его missing frozen root
`docs/system/README.md` остаётся unavailable; отсутствие private/native/raw inputs
не заполняется reference текстом. SI04 не принимает научных claims historical review.
