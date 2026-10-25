# DEV15/DEV16 — independent CP-CODE

**Вердикт: scoped CP-CODE PASS.** Shared fail-closed schema provenance implementation, approved assigning-source prose и selected102assertions согласованы с accepted D15v2. Блокирующих source findings не обнаружено. Reviewer Julia/import/test/build/solver/server/Git/source writes не выполнял; проверены исходники, exact byte/hash mappings и saved root runtime evidence.

## Immutable binding

- Runner HEAD `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, Contracts `26cacbe1688fee0af300d0949fc6b94e55a29f4a`. Reviewed branch `codex/review-closure-schema-provenance`.
- `/tmp/qcl-dev16-full.diff`: SHA256 `8b7d735e6b1026dc921e77e797a437cfd3f21ea1a650443be3b26b07c9a8c22d`,34,555B. Каждая из10sections независимо reconstructed из current tracked/new-file diff, whole package byte-equal. Другие компоненты/parallel changes не входят в scope.
- Accepted `/tmp/qcl-dev15-design-v2.md` SHA256 `61c07b249740e435b9b4c2e2becfdaf558ad96304e275adcda370f652df9a1c6` и saved v2 PASS review прочитаны после source/API inspection.
- `/tmp/qcl-dev16-report.md` verified SHA256 `094108571cab99fdfdd82534b08687664f82a9156a1ea79650e842f35e417866`; report не заменяет source/runtime evidence.
- Все7 entries `/tmp/qcl-dev16-code-hashes.json` independently rehashed match. Key verifier hash `8bdb801a6e9b5419735c1248b3efc9a01900e2f6335c359693cf2e4dee7fcf09`; loader `96da51af912890bb001c03c9400f95151c67f630dd248b4263bff4c7b93c710d`; resolver file `b07516d1fa1b9f7918efd4fa9096327be45af5ea32233ba15a9e88bf225daebb`.
- `git diff --check` exit0. Full CONTRIBUTING check/test/docs не запускались reviewer; explicit bounded card scope не расширялся.

## Source-first YAML/include check

Actual locked YAML package `Project.toml` declares0.4.17; read `src/YAML.jl:53–88,142–156` and `constructor.jl:139–215`. AbstractString load→IOBuffer→custom Constructor, поэтому `YAML.load(String(copy(bytes)), constructors)` source-supported и не открывает pathname. YAML strict duplicate error внутри mapping catch становится ConstructorError; wrapper catches его и форматирует known error.

`flatten_mapping` делает duplicate checking условным на !merged_mapping. Поэтому один strict_unique_keys не закрывает metadata ambiguity. Verifier34–51 проверяет merge-tag keys **до** YAML.construct_mapping; custom constructor применяется recursively. Только metadata=true запрещает merges. Custom schema parser metadata=false сохраняет прежние YAML merge semantics; schema duplicate checking без merge соответствует прежнему `_load_yaml_mapping`.

Прочитан `_package_path`: loaded Runner pkgdir, не caller cwd/build path. Base.loading::_include3066ff читает selected include path и передаёт filename в include_string. Runner module include configuration_contract загружает tools через package path. Tools1–4 определяет shared module с SHA/YAML only, bottom direct-program guard вызывает main лишь для непосредственно запущенного файла; нет verify/main/exit в module import, __init__, schema path accessor или provenance lookup. Native relocation не доказывается одним source reading/теплым import.

## Integrity, modes и same captured bytes

`tools/verify_schema_provenance.jl:96–166` проверяет mode/conflicts, source/version nonempty strings, nonempty sha mapping, оба required payload names, safe basenames и lowercase64hex digests. Declared payloads не ограничены только run.schema: loop захватывает и проверяет **каждый** declared файл. Schema directory symlink redirection и file realpath escape rejected79–94/65–76. Selected bytes read once, SHA вычисляется на этих bytes и они же возвращаются snapshot.files. Metadata читается заново каждый call; success cache/mtime shortcut, repair, network/Git/latest fallback отсутствуют.

Workspace mode требует explicit root и same realpath Runner component; сравнивает каждый declared payload с canonical selected Contracts bytes. Auto основан на resolved Runner placement components/QCLNEGFRunner.jl + .gitmodules у candidate root, не cwd/active project. В detected workspace missing/drifted Contracts не переходит в standalone. Standalone проверяет packaged declared hashes без sibling dependency; source URL/version — descriptive, не authenticity/version lock. Source/Gitlink publication binding остаётся root gate.

**Обязательная actual snapshot trace:** `configuration_contract.jl:49` получает snapshot,50–52 bundled branch выбирает snapshot.files["run.schema.json"],63 передаёт **эту bytes variable** в strict parser,68–73 оставляет Draft/keyword validation. Parser копирует vector перед String conversion; packaged content pathname не перечитывается. isfile/realpath классифицируют alias, не заменяют captured content. Runtime helper-race assertion дополняет, не заменяет этот source trace.

Caller custom schema_path не получает canonical identity: package verification всё равно выполняется первой; custom path читается отдельно56 и проходит тот же прежний semantic Draft/keyword checker. Matching packaged bytes не дают bypass для unsupported custom keywords. Это сохраняет supported custom YAML merge behavior без metadata merge loophole.

## Typed/frozen routes и assigning-source semantics

`configuration.jl:1757–1762::_resolve_configuration` добавляет только accepted private root keyword и shared verify как **первое executable statement** до _expect_keys/Unitful conversion. Публичные loader/validator signatures не добавляют bypass. `configuration_sources.jl:31–91` использует schema loader до source merge и resolver после validation; `snapshots.jl:30–33::load_scientific_plan` прямо вызывает тот же resolver; configured runtime consistency также достигает его. Earlier frozen fingerprints/raw structure/output-policy reads остаются прежними. Здесь не добавлена JSON-schema validation historical frozen plans; обещанная граница — до typed resolution/solver, не до любого dictionary read.

`configuration_source` body independently unchanged: get(history), missing/empty→nothing, otherwise last(history). Prose правильно различает assigning identifier, physical data source и полный origin chain; explicit filenames и existing #generated: markers не теряются. Merge17→23/reverse→17/base64 источник проверяется отдельно от numerical equality; absent/empty recorded history не выдаёт typed constructor origin. Existing generated freeze/load fixture source остаётся unchanged anchor; отдельно не выполнялась и не присваивается этим102assertions.

## Canonical copy и exact DEV15 prose

Packaged run schema byte-identical Contracts canonical: SHA256 `62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b`. Results contract set также byte-identical `bd14c6a62d35543b29e9473c8e388a3790524364c52b4d64922a74278c6fb2c1`. Actual metadata digests matched independently. Parsed schema vs Runner HEAD становится равен после удаления единственного нового energy_chunk.description; constraints/defaults не изменены. PROVENANCE меняет только run digest, не source/version/results digest; второй source lock не создаётся.

Mapping `/tmp/qcl-dev15-applied-prose-map.json` verified SHA256 `cea5ca69c8ac7010791da330e5c2e2ac430bd40419b6a87a6151f59f021e91c3`. Три accepted fenced blocks3.1/3.2/3.3 извлечены independently и дословно найдены в actual docstring/guide/newMD. Block hashes без terminal newline совпали b723d4…/a0b347…/e76b24…; все3 full-file hashes также match. Function body не меняется. Main-branch external link на новый prose файл требует owning publication; локальный target существует. Outside-src file не объявляется Documenter-rendered/navigation page. Accepted status sentence честно остаётся DEV16 target до published owning review; последующее обновление publication status отдельно, не silent переписывание approved blocks.

## Selected runtime evidence

Root `/tmp/qcl-DEV16-GREEN-1/{receipt.json,original.log}` inspected after completion. Exactly two includes в одном процессе: schema_copy_provenance и existing merge-order fixture. Actual fixture hashes1d56940eb6202f8b957ed43ce8aa94d1b20a566a80a1d32805ee79ca2c56088f /09fa7cccc6ec8c701cf86135ce6d50c5ca1881323d8b91e9729846b75f8e9cbb independently match current files.

- **80 schema provenance +22 merge order =102 passed**, exit0, wall25.006s.
- Sampled process-tree RSS828,452,864B, tmppeak57,838B, log308B, stopnone, raw_capture_complete=true/errornull.
- Actual argv Julia1.13.0 selected executable, startup-file=no, threads1, check-bounds=yes, copied prepared project. Receipt labels genericCPU/BLAS1/offlineprepareddepot/no setup/solver/fullCI; full separate loader/native relocation receipt не подразумевается.
- Envelope120s/1CPU/2GiB sampledRSS/16MiB tmp/2MiB output; RAM/output/disk monitor не hard-cgroup guarantee. Prior cold timeout RED1 и missing-module semantic RED2 не стираются. Root owns finite attempts; reviewer runs0, нового rerun не требуется.

Negative fixtures используют temporary copies: one-byte packaged drift, stale/missing payload/canonical, malformed/duplicate metadata including valid-hash merge ambiguity, unsafe paths with otherwise complete metadata, symlink escape, extra declared file, no cache, CLI streams/options, actual loader precedence до unsupported keyword, actual resolver provenance failure до wrong-dimension error, custom merge positive. All earlier merge assertions сохранены; added missing/empty source history checks не переписывают typed value. Direct CLI main тестируется без subprocess; process-level CLI, run-plan, cold installed Nix/relocation не measured.

## Границы

Schema-copy integrity не является model adequacy, convergence, physical gates/discretization/experimental acceptance. Runtime auto проверяет selected on-disk copies, не universal hostile-filesystem authenticity/OS writer closure. Snapshot-to-parse защищает потреблённый content этого call; source binding/publication и controlled writers остаются существующими gates. No import-time fatal/no success cache подтверждены source и выбранными fixtures; full native deployment/full CI не выполнены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Fail-closed packaged/canonical bytes enforced | shared verifier source +80passing controls | on-disk identity, publication отдельно | сохранить |
| Parser использует verified snapshot | actual49→52→63→String(copy(bytes)), mutation/no-cache control | no native relocation/race campaign | сохранить |
| Metadata merge bypass закрыт без custom-schema regression | actual YAML0.4.17 +metadata-only check+negative/positive fixtures | strict metadata policy scope | сохранить |
| Typed/frozen entry boundary preserved | actual resolver first guard +source callers+direct-method fixture | no full frozen CLI process | сохранить |
| DEV15 semantics/prose verbatim | unchanged get/last body,3exactblocks,22merge assertions | generated-marker anchor source-only | сохранить |
| Scoped DEV15/16 CP-CODE ready | frozen byte equality +102pass savedrootpacket | no solver/fullCI/native/science acceptance | сохранить |
| Scientific/native/full release acceptance | corresponding evidence отсутствует | integrity tests не заменяют required gates | данных недостаточно |
