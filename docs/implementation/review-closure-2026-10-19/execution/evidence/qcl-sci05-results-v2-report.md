# SCI05-N1 Results v2 — initial completion по принятому attribute profile A

2026-10-19. Подготовлен и заморожен source candidate для independent high review.
Encoding blocker первоначального partial freeze закрыт отдельным D+R и adoption
координатора; данная реализация ещё не имеет CP-CODE/runtime PASS. Исполнений не было.

## Принятый вход и preservation

Норматив SCI04-D2 SHA256
`d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` остаётся прежним.
Полностью прочитаны engineering profile/recipes/controls:
`/tmp/qcl-sci05-attribute-encoding-design.md` SHA256
`1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206`,
independent review SHA256
`95518b6b9150b27ec490f2e30e5015511b300769fc3ed9443010591c1a010916`,
coordinator READY `/tmp/qcl-checkpoint-attrs-design-ready.json` SHA256
`0806a115cb0515e4cba7f20131e32cdb44b0158ebb8a3f136197a95c4c6337fc`.
Adopted profile A является explicit engineering cap/method; он не выводится
из старого D2 dataset paragraph и не меняет portable JSON/scientific schema.

Worktree `/tmp/qcl-sci05-results-worktree`, branch
`codex/review-closure-final-audit-reader`; фактический HEAD/base
`e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Prepared Contracts
`12fc26462bbab3df76904c6deb01f8c6596de7be`; root selected
`9d8cf0cad32743791cc3b80ac7c2a948dab02f48` не обновлялся этой работой.
Source identity/Git status/recursive submodule status перепроверены в owning
worktree; submodules отсутствуют. Root/original dirty checkout не изменялись.

Первоначальные partial-freeze artifacts сохранены byte-exact, hashes повторно
проверены:

| Artifact | SHA256 |
| --- | --- |
| /tmp/qcl-sci05-results-report.md | f0baf6232f46095199c84c3951132d272224837d29fefd471cc77c47b73661f1 |
| /tmp/qcl-sci05-results-identity.json | d252c817ccdb4997656a7845f38168c93eeaa9bc7f371e44646029fc26d3d0ac |
| /tmp/qcl-sci05-results-patch.diff | 46ca0c6f56dc884bf7cf08e1d9319621fadf104fdab1d6d6384559b535790f1e |

Initial source bytes восстанавливаются initial patch от exact base. Старый
отчёт остаётся историческим NOT_READY, не переписан задним числом.

## Изменение относительно initial candidate

`native.py::_audit_attribute` теперь открывает только известное имя через
`get_id`; удерживает тот же AttrID, file datatype и dataspace до raw read.
До NumPy dtype/value-buffer allocation проверяются atomic STRING, non-vlen,
SCALAR/shape(), width L..65536, ASCII/UTF8 charset и три разрешённых pad modes.
`_read_audit_attribute_bytes` синтезирует scalar S<N>, читает
`attribute.read(target,mtype=datatype)` и сохраняет все N storage bytes через
`tobytes()`. High attribute getter, arbitrary filetype→NumPy dtype и auto mtype
в этом пути отсутствуют.

Снимается только допустимый right suffix (NUL для NULLTERM/NULLPAD, space для
SPACEPAD); любой оставшийся NUL corrupt. Charset-specific strict decoding и
exact constant comparison не допускают first-NUL truncation, normalization,
case folding или leading whitespace. Canonical N=L без terminal NUL разрешён.
`ExitStack` регистрирует каждый полученный ID немедленно и закрывает их в
обратном порядке при success/preflight failure/read failure/value failure.
Четыре attrs читаются последовательно на том же исходном budgeted handle.

Область — только schema/units/logical_axis_order/description новой final-audit
группы. Historical generic attrs остаются прежними. `state.py` byte-exact
совпадает с initial candidate: private cached pair/native-state binding,
legacy/recovery behavior, optional analysis/checkpoint checks и same physical
I/O budget сохранены. Public API/source keys/CLI, JSONschema/status mapping,
formulas/thresholds и stored-equilibrium reducer не менялись.

## Подготовленные controls и их пределы

К initial literal record/identity/equality/recovery/budget controls добавлены:

- Genuine fixed H5A fixtures с явными file/memory type, scalar space, ASCII/UTF8,
  N=L/L+1/65536 и NULLTERM/NULLPAD/SPACEPAD. Independent fixture metadata и raw
  readback assertion проверяют реальные type/space/width/pad/bytes перед вызовом
  product reader; expected constants не получаются из product encoder.
- Genuine NULLTERM expected+NUL+X и interior-NUL fixtures. Writer использует
  same-type H5Awrite и требует raw readback exact equality, чтобы сам fixture
  не мог скрыть adversarial suffix conversion-ом.
- Малые genuine scalar vlen ASCII/UTF8, с value-read/allocation sentinel до
  product raw helper. Большие vlen heaps не нужны и не создаются.
- Genuine NULL/one-element/rank-two space; numeric/compound/array/opaque type;
  width<L и65537; missing each required attr. Invalid charset/padding и absurd
  width дополняются bounded metadata adapter с guard и cleanup assertions.
- Strict invalid UTF8/ASCII; prefix/suffix/leading/wrong case/exact-value
  controls; retained same type identity/read count и закрытие all3 IDs на
  success/preflight/raw-read error/wrong-value paths.

Большие fixed attr fixtures используют modern file format/track_order для
поддержки dense attribute storage; writer/readback metadata predicates остаются
обязательными. Эти controls **подготовлены, но не исполнялись**.

Actual pinned Julia String producer → independent Python native round-trip
остаётся отдельным required runtime evidence координатора. Его нельзя заменить
Python-manufactured fixtures. Source/D+R dispatch не доказывает actual linked
native HDF5 behaviour; версии/paths Julia/Python libs должны попасть в receipt.

## Фактические проверки и стоимость

Выполнены только текстовые/Git/hash операции и `git diff --check` (exit0),
проверен diff разрешённых paths. Python/imports/HDF5 execution/tests/Julia/
setup/build/install/network/server/solver =0; stage/commit/push=0; children=0.
C08 calls этим initial completion не расходованы; оставшиеся общие calls2
не расширялись. Новый finite scope ≤25min/1CPU/2GiB/read2MiB/output64KiB соблюдался
адресными source reads; runtime RAM/CPU не измерялись.

Per-attribute value allocation bound исходит из fixed atomic scalar и Ncap;
NumPy/raw/decode copies добавляют постоянный множитель. Это не whole-process RSS
или hostile-native-metadata sandbox proof. Общий physical stream budget в
StateReader учитывает metadata и additional-owner SHA/HDF passes, не подменяется
суммой logical string widths. Tiny insufficient cap должен отказать;
underbudget→skip/success не добавлен. Existing `_json_scalar` historical identity
path остаётся прежним и не получает новый глобальный memory-bound claim.

## Frozen source

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| src/qcl_negf_results/native.py | 16498 | 532fbedf8b1b296e0fb5bc026788a522bf92aeee94ae1192ca651e2e34a407e5 |
| src/qcl_negf_results/state.py | 29544 | 57af749bbc0c5179707871ee43e75db01da2017faa242d08bd888c2aab8ef224 |
| tests/test_final_fixed_point_audit.py | 27164 | 8d9b6b1dae1cc271494e26773be9a2c0551acfda578c7d10c8713b797208c082 |
| /tmp/qcl-sci05-results-v2-patch.diff | 41146 | fb936c596a035670426ad64c90c4c97a2e0a663dfd663c34a594e51a2853a55e |

Patch включает полную initial реализацию и profile-A completion от exact
Results base, включая untracked owning tests. Identity manifest:
`/tmp/qcl-sci05-results-v2-identity.json`. Один writer; independent reviewer
назначает координатор на этот exact immutable source набор.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Profile A реализован на source пути четырёх attrs | Frozen native.py + adopted design/review hashes | CP-CODE независимым reviewer ещё не принят | изменить |
| Scalar/vlen/padding/cleanup controls готовы | Frozen literal tests с genuine type/raw assertions | Не исполнялись, linked native behaviour unknown | дополнительно измерить |
| Private pair/legacy/recovery/I/O integration сохранены | state.py SHA byte-exact initial; unchanged Contracts helper | Runtime/producer round-trip pending | сохранить |
| Runtime/scientific acceptance уже установлены | Нет runtime receipts/arrays | Source/fixture code не доказывает scientific результат | данных недостаточно |

STOP. Initial completion source frozen; до нового READY brief правки и
исполнение не продолжаются. Следующие gates: independent high source review,
source-bound targeted runtime/actual producer transport в оставшемся общем cap.
