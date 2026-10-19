# SCI05-N1 Results — frozen source candidate, encoding blocker

2026-10-19. Этап I: подготовлен первоначальный source candidate по принятому
SCI04-D2 §6 SCI05-N1 Results, §8.3–8.8/§9. **CP-SOURCE not_ready:** кодировка
HDF5 attributes требует отдельного exact design. Координатор поручил freeze и
STOP; fixed-only ветка не принята как норматив D2. Runtime evidence отсутствует.

## Identity и владение

Root selected HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`, workspace
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`; Results selected/current
`e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae` был clean. Создан отдельный component
worktree `/tmp/qcl-sci05-results-worktree`, branch
`codex/review-closure-final-audit-reader` от exact e2fdeda; HEAD не изменён.
Корневые unrelated изменения и original dirty checkout не редактировались.
Root Git/submodule status снят; scientific arrays и архивы не читались.
Results AGENTS.md отсутствует; CONTRIBUTING прочитан. Прочитаны root AGENTS,
architecture, implementation entrypoint, canonical review workflow, relevant
P1 science SCI05/SCI06/C08, применимый qcl-results-analysis и frozen D2/review.
Using-superpowers исключает dispatched subagent. Дочерние агенты не создавались.

Норматив D2 SHA256 `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`,
independent review `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1`;
status clarification `a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8`.
Consumer использует prepared Contracts commit
`12fc26462bbab3df76904c6deb01f8c6596de7be`, final_audit.py SHA256
`1c19ba7f27912c739b349fb7c517a9030be3c4f50c4b75932c08d0c02f3219d1`;
frozen binding JSON SHA256
`db59ad83d49aa9f4bf5943ca6ac1bdc5c7e18b9049720fc8170c88b553ec8e9d`.
Root selected gitlink Contracts ещё старый: prepared source и selected root
не смешиваются и runtime binding этим отчётом не объявляется.

## Подготовленная source-реализация

- `native.py::_read_final_fixed_point_audit`: private native path с internal
  hard links, exact single dataset, scalar fixed S/UTF8/itemsize1..65536,
  no chunks/compression/filters/external/virtual storage; same-type low-level
  scalar read сохраняет storage bytes до right-padding/NUL checks. Scalar cap
  не увеличивает physical I/O grant. JSON/schema/status interpretation передан
  pure Contracts helper.
- `state.py::_validated_final_fixed_point_audit`: точная pair-проверка,
  identity against commit и native point identity, explicit commit-null reject,
  legacy both absent→not_recorded, recovery absent→not_applicable/
  not_a_final_state. Constructor хранит wrapper только в private
  `_final_fixed_point_audit`; новый public API/source key/CLI отсутствует.
- Private constructor sidecar pass проверяет declared optional HDF5
  physics.analysis и recovery/checkpoint owners: safe path, собственный SHA,
  native contract, equality optional present copy либо запрещённый final record
  в checkpoint. JSON recovery reference не является HDF5 checkpoint и не
  открывается этим pass. Все sidecar SHA/HDF reads идут через существующий
  `_BudgetStream/_IOBudget`; cap-short приводит к отказу. Дополнительные
  full-owner hashes могут увеличить стоимость конструктора; новая квота не
  создаётся. Numeric arrays не читаются.
- Existing `verify_recovery_bundle` и prior-final verification вызывают те же
  private checks внутри уже существующих HDF passes; новый public return shape
  отсутствует. У этого existing API нет maximum_io_bytes; данной работой новый
  публичный budget argument не добавлен.
- `diagnose_stored_equilibrium`, physical formulas/thresholds и numerical
  fixtures не изменены. Reader не реконструирует fresh map.

## Конкретный blocker

D2 §8.3 фиксирует record_json dtype, но не storage dtype четырёх attributes:
group.schema, dataset.units/logical_axis_order/description. High-level
`attrs.get`/`attrs[name]` для произвольного vlen payload может выделить память
до проверки длины. Physical byte accounting само по себе не доказывает bound
на такую аллокацию.

Текущий `_audit_attribute` имеет только fixed scalar S ≤512 branch, читает
значение после dtype/shape preflight и отвергает vlen до value-read. Это
**временный source candidate с явным encoding gap**, а не утверждённое
ограничение D2 или доказанная совместимость с Runner. Координатор подтвердил
отдельный ultra design до окончательного CP-SOURCE; до нового READY brief
правки запрещены. Требуется согласовать actual producer encoding и bounded
consumer contract, затем source review/ограниченный runtime.

Pre-existing metadata identity reader `_json_scalar` остаётся прежним; новый
формат identity-storage этим scope не введён. Исходный point identity pass
и новый exact equality не доказывают общий bound всех старых vlen metadata.

## Подготовленные controls и фактические проверки

Новый owning файл `tests/test_final_fixed_point_audit.py` содержит literal
format fixtures и stdlib JSON encoding, без product final-audit encoder,
Contracts test imports, solver или scientific arrays. Assertions описывают:
healthy measured0/right padding; finite error0; both-absent legacy/recovery;
one-sided/null/recovery record rejection; wrong attempt/state/seq/plan;
independent native point identity; semantic mismatch; malformed JSON/UTF8/NUL;
bad type/rank/size/schema/units/axis/description/children before payload;
storage-feature preflight; physical HDF metadata accounting; automatic private
constructor cache; sidecar equality/recovery rejection и общий cap.

Ни один из этих assertions не исполнялся. Отдельного executed filter mutation
control нет; nofilters guard пока подтверждён чтением source. Synthetic tests
не доказывают совместимость реального producer archive и scientific acceptance.

Выполнены read-only Git/text/hash operations и `git diff --check` (exit0).
Не запускались Python, product imports, HDF5 runtime, pytest, Julia,
SCBA/Poisson, installation/build/network/server. C08 processes consumed этой
работой: **0**; corrective runtime rounds: **0**. Stage/commit/push не выполнялись.
Первый worktree add без escalation получил read-only Git metadata error;
scoped escalation для exact requested worktree затем завершилась успешно.

## Frozen outputs

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| src/qcl_negf_results/native.py | 15479 | 4c4faee51d55abda3532e5bfba165388690fdb6891df9bb30a82e4f9e1a14fb9 |
| src/qcl_negf_results/state.py | 29544 | 57af749bbc0c5179707871ee43e75db01da2017faa242d08bd888c2aab8ef224 |
| tests/test_final_fixed_point_audit.py | 15935 | c4011d8df6ee6f49f6120ceb09bded4f9a92ba9bd25bbe533d698082429e0a0d |
| /tmp/qcl-sci05-results-patch.diff | 28658 | 46ca0c6f56dc884bf7cf08e1d9319621fadf104fdab1d6d6384559b535790f1e |

Patch включает tracked diff и untracked test file; source files остаются
незакоммиченными в изолированной ветке. Identity manifest:
`/tmp/qcl-sci05-results-identity.json`. Independent source review координатор
назначает отдельно; автор не закрывает его сам.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Final-record bounded layout/pair/state validation подготовлены | Frozen native.py/state.py + Contracts12fc API | Source candidate; attrs contract pending; runtime не выполнен | изменить |
| Legacy/recovery и optional-copy semantics выражены | Private helpers + literal controls | Assertions не исполнялись | дополнительно измерить |
| Metadata и sidecar reads входят в действующий cap StateReader | Existing BudgetStream reused; constructor own SHA/HDF pass | Additional-owner I/O нужен при наличии sidecars; общий old-vlen bound не доказан | сохранить |
| Fixed-only attributes — принятая норма D2 | D2 фиксирует только content этих attrs | Producer encoding/strict bound не frozen; coordinator design pending | данных недостаточно |
| Scientific/numerical acceptance или runtime PASS достигнуты | Новых runtime/artifact receipts нет | Source и fixture code этого не доказывают | данных недостаточно |

STOP: freeze по прямому поручению координатора. Новые source edits, execution,
stage/commit/push до нового READY brief не разрешены.
