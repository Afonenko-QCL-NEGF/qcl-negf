# DEV15 v2 — второй/final CP-DESIGN review

Вердикт: **PASS CP-DESIGN**. Единственная C1 correction закрыта; передача
DEV16 medium исполнителю допустима без нового human question и без третьего
design round. Implementation/runtime evidence остаётся отдельным CP-CODE.

Проверены exact artifacts:

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-dev15-design-v2.md` | `61c07b249740e435b9b4c2e2becfdaf558ad96304e275adcda370f652df9a1c6` |
| `/tmp/qcl-dev15-design-v2.diff` | `0c79146919870c46bfc8fa0ba6c876d181ed052dd0a5e068755af06065365850` |
| `/tmp/qcl-dev15-design-v2-response.md` | `a8b800b90a56ba16d00f38fe25b3b73fcdc7491ecfd3266bbe74a3ab03390898` |
| Original и preserved round1 | оба `662f0bdf5d51df3cf4e907645a56da6d125eb64e99db21429096e74bd8393c82` |

## C1 и неизменность принятого контракта

V2 docstring/guide/source matrix теперь определяют last recorded assigning-source
identifier, filenames для explicit leaves и `#generated:` identifiers для
generated overrides. Guide непосредственно объясняет existing
`physical.lattice_temperature` marker и freeze/load history preservation.
Lookup по-прежнему не выводит typed/schema default, physical data source либо
полную effective-origin chain. Это соответствует Runner0c
`configuration_types.jl:216–221`, `definitions.jl:387–462` и existing
`generated_scientific_configuration_provenance.jl:32–38,100–110`.

V2 diff оставляет прежними shared verifier API/module layout, CLI options/status,
workspace/standalone/auto modes, оба runtime seams, private root keyword,
custom-schema compatibility, no-cache/same-captured-bytes и finite two-invocation
envelope. Уточнены обязательные source-reading и CP-CODE snapshot-flow evidence;
нет новых product paths/public APIs/scientific acceptance criteria.

Source epoch исправлена явно: historical eb59809/e5 observations сохранены,
round2 rebind root04e/Contracts26 выделен отдельно. Независимо повторены
`git rev-parse HEAD`, root gitlink и Runner status: root
`04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6` выбирает Contracts
`26cacbe1688fee0af300d0949fc6b94e55a29f4a`; Runner clean на
`0c53c6d0f68e0b25fce79388db831da6fc3ae856`. Старый selection mismatch больше
не объявляется current blocker. Publication/G1 receipts остаются coordinator-owned.

## Source-bound YAML checkpoint: прочитан, без исполнения

Независимо прочитаны prepared files
`.build/local-julia-int01/depot-1/packages/YAML/M5j6t/`:

- `Project.toml:3` — version0.4.17, совпадает с root Manifest YAML entry
  (git-tree-sha1 `9c685a6e94e255019e2bf9486318147cd42fe34a`).
- `src/YAML.jl:142–143` —
  `load(input::AbstractString, args...; kwargs...) = load(IOBuffer(input), args...; kwargs...)`.
- `src/YAML.jl:87–88` — IO overload forwarding custom constructors; default
  tokenstream overload использует SafeConstructor.
- `src/YAML.jl:153–156` — `load_file` открывает pathname; не использовать его
  для verified bundled schema snapshot.

Exact SHA256 `src/YAML.jl`:
`24f6e5c7475945658b3bf8625cacaa7c2443726547e0679acd86ff4584d936cb`;
`src/constructor.jl`:
`4650446782dcdbe53928affe5dd183d0d0643bb07a04bf7ef4d7c6664d0e8f07`.

Исполнитель может использовать `YAML.load(String(copy(bytes)), constructors)`
со source-confirmed overload; parser не должен обращаться обратно к pathname.
Этот read-only checkpoint не является доказательством runtime behavior.

Обязательная implementation/CP-CODE деталь существующего требования strict
metadata: `constructor.jl:183–206` вызывает `flatten_mapping(node)` и проверяет
duplicate keys только при `!merged_mapping`. Следовательно,
`strict_unique_keys=true` один не доказывает универсальное duplicate rejection
для PROVENANCE с YAML merge tags. Для metadata-only parser нужно явно reject
merge tags до flatten либо использовать иной подтверждённый strict путь. Это
реализация уже принятого fail-closed metadata контракта, не новое API/правило
научной приёмки. Не распространять metadata-only запрет на caller-supplied
custom schemas: их существующую YAML parsing semantics сохранить. В CP-CODE
нужен differentiating fixture metadata с merge-tag/duplicate ambiguity;
он входит в тот же proposed schema suite и не добавляет Julia invocation.

Сохраняется прежнее CP-CODE условие: source trace actual
`_load_configuration_schema` → verified snapshot bytes → strict parser;
helper-only mutation assertion не заменяет этот trace. Frozen-plan route
покрывается source reachability + actual resolver fixture; полный process-level
frozen-plan execution здесь не заявлен.

Никаких product writes/imports/Julia/tests/build/install/SSH/spawns этот review
не выполнял. Подтверждённые координатором INT01 module imports не пересчитывались
и не приписываются reviewer как собственное измерение.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| C1 generated-marker prose закрыт | Exact v2 diff + Runner0c primary sources | Runtime не запускался | сохранить |
| Ранее принятые seams/API/modes сохранены | Полный scoped v2 diff | Implementation впереди | сохранить |
| Current source selection исправлен | Root04e gitlink Contracts26, Runner0c clean | Publication receipts отдельно | сохранить |
| In-memory YAML overload доступен | Locked0.4.17 source, exact signatures/hashes | Metadata merge-tag strictness должен доказать fixture | изменить в реализации |
| Design готов к DEV16 | C1 closure + accepted invariant contract | Runtime/CP-CODE ещё не закрыты | сохранить |
