# DOC07 C2: final collated correction cycle8/8

Исполнена одна correction F1–F6 после independent high CPP `/tmp/qcl-doc07-C2-impl-review.md`, SHA256 `471cbdffa269970d14ff114ff9b2d66053f6b96c15f25cf9a711d7673c2f99d2`. Только owning module и append-only regressions в `/tmp/qcl-doc07-c2-worktree`. Base `d791dea33f4628cf23c0b8552ebee9e51d7dd605`; branch `codex/review-closure-model-help-bindings`.

Нормативные inputs неизменны: D2 SHA `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b`, preserved canonical SHA `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`. Применимые clauses: D2 R6:131–145, R2:178, R3:181–197, R4:201–212, R5:219; DOC03:452–475 origin proof,510–538 assigning/causal/Evidence,556–574 Snapshot,615–636 Index. Авторский single-point limitation v1 не использован как изменение договора.

## Полный collated correction

| Finding | Изменение source | Независимая regression pair |
| --- | --- | --- |
| F1 Bundle all-fragment semantics | Bundle проверяет собственные retained bytes и вызывает общий `_fragment(...,payload=exact_bytes)` для каждого descriptor, включая unselected; static fragment proof отделён от selected retained fragment record | Safe selected Bundle vs fresh-hash query Bundle; второй safe unselected fragment vs query или invalid selector в нём, при согласованных payload/descriptor/bundle/publication/annotation associations |
| F2 known identity erasure | View каждый identity scalar сравнивает с exact known retained value, включая null только при отсутствии факта; receipt сохраняет known source revision даже при missing graph blob | unavailable docs healthy + null каждого из четырёх known scalars rejected; truly absent release/source/bundle/manifest proof healthy с null |
| F3 target-leaf assigning | Известная assigning projection соответствует последней raw assignment конкретного leaf; Evidence разрешён только для этой selected snapshot assignment либо совпадающей frozen point assignment | Healthy existing frozen-plan Evidence и exact selected snapshot Evidence; matching unrelated execution_strategy step rejected |
| F4 extra effective Evidence | known chain требует и coverage, и membership: exact required/supplied location sets равны; duplicates не создают coverage | Exact two-step known chain healthy; extra hash-valid execution_input:/context rejected, старые same-cardinality replacement controls сохранены |
| F5 multi-point Index | Index-wide context отделён от endpoint point; каждый member point связан со своим frozen passport, snapshot bytes/hash/size/context/inventory; проверяются selected alias и aggregate до payload decoding | Complete P1/P2 index с разными declared/used Atom, validate endpoint P1 и P2; wrong attempt/execution/nonmember/cross-associated sibling/passport/inventory/duplicate/count/aggregate/missing sibling rejected |
| F6 Snapshot declared passport | Общие snapshot semantic contents сравнивают known declared Atom каждого raw leaf с его frozen point passport; used не приравнивается declared; unknown не заполняется | Freshly rehashed known declared value/unit/kind mutants rejected; distinct used healthy; unknown declaration healthy, в том числе отсутствующий passport proof |

Для F1 unselected fixtures authored annotation и review associations переизданы через fixture-only helper; внешний hash не маскирует URI/selector failure. F5 sibling-payload negative заново связывает index/inventory digest/size с реальными bytes другого point: намеренное нарушение остаётся в point association. Aggregate negative имеет два реальных typed-invalid файла по4MiB+1 с верными inventory/hash; каждый индивидуально bounded, суммарно>8MiB, payload JSON не исполняется/не парсится до aggregate guard. Это runtime allocations test source, автор их не выполнял.

## Checked private multipoint layout

Root подтвердил имена и границу in-memory layout в этой correction; новых public fields/formats/receipts/registry/trust root нет.

- `retained.point_passports[(execution_id,point_id)]` — existing Evidence в exact original frozen_plan bytes. Проверяются container/hash, actual frozen point id/execution membership и точный `/points/<index>/configuration` selector для этой точки. Подмена pointer на sibling не становится ownership proof от одного наличия Evidence.
- `retained.snapshot_files[logical_path]` — original closed `{bytes,sha256,inventory:{bytes,sha256}}`. Inventory — detached факт owning retrieved inventory; helper сверяет его с entry и measured raw bytes/digest. Каждый valid snapshot проверяется на child execution/attempt, собственный point/configuration hash и declared passport. Selected endpoint metadata alias должен иметь те же оригинальные bytes, что и selected entry.
- Index не сравнивает sibling point_id с endpoint selection.point_id. Общие child/execution/attempt/model/plan/scientific context остаются одинаковыми; point/configuration passport проверяются отдельно. Missing mandatory sibling proof fail-closed. Legacy one-point `metadata.execution_input` fallback сохранён.
- Никакого endpoint/global/current fallback при отсутствии точного fragment mapping не добавлено; doc availability и declared/used по-прежнему независимы. Frozen claims/origin branches не ослаблены.

## Immutable artifacts

| Artifact | Bytes / SHA256 |
| --- | --- |
| `src/qcl_negf_contracts/model_help.py` |53586 / `6e3f6d8ed2e6a0d7e637c48edc87820c62776755803f4d4b62a3961f8b2429bd` |
| `tests/test_model_help_bindings.py` |52988 / `ef51509e7b2db13196e5e243193492235d82b516bbc9d93deeb9369000bdc95f` |
| Preserved `/tmp/qcl-doc07-C2-impl-v1-model_help.py` |46827 / `ca2c6656484fd99a2a58815ba97f0eb85369591f287368ffe05109764b014d1a` |
| Preserved `/tmp/qcl-doc07-C2-impl-v1-test_model_help_bindings.py` and exact new test prefix |40274 / `72240eab26305f63aeeec06197a7f64802c111a83cd3ef8aae603c5e89ae71f9` |
| `/tmp/qcl-doc07-C2-impl-v2-full.patch` |`683f3581a3a1bb2c51ee497703775e161acd189b05182a33d5ae2de030aca0f4` |
| `/tmp/qcl-doc07-C2-impl-v2.delta.patch` |`8586a3e13b02999d142628f0fb97ba9c07cb270833a2fcf9c59fb759f9b2fa9d` |
| `/tmp/qcl-doc07-C2-impl-v2-regressions.delta.patch` |`84a81aa4aa306a6ced21a99753d8dab519d3473aaa6f5c58e4ba07523bd485de` |
| `/tmp/qcl-doc07-C2-impl-v2-tests-full.patch` |`8554da6239d94557cd398f3b1f44ffa24567dccfe69f56a868e1930d881e4d8b` |

Identity JSON: `/tmp/qcl-doc07-C2-impl-v2-identity.json`. Старые reports/patches/receipts сохранены. Frozen test assertions не редактировались: `cmp -n 40274 preserved-test current-test` exit0. C1 schema SHA `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241`, C1 test SHA `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177`, loader SHA `41b5b746bbf28cd0e60bb85bc927f1c55ba0ac2695f3271b875f83c057a744d1` unchanged.

## Проверки и границы

Выполнены только text/hash/Git metadata/source writes и diff checks. Оба no-index --check вернули1 из-за differences, diagnostic output пустой. Final status: два untracked owning files (module и C2 test), HEAD unchanged, submodules отсутствуют. Ни target imports, ни parser/schema execution, pytest/collection, typecheck/formatter, network/build/solver/commit, Root/checkpoint writes не выполнялись. Новый code предназначен для будущего guarded runtime; source author его не вызывал.

Current envelope30min/1CPU/2GiB/read4MiB/output256KiB. Чтение cached D2/canonical/previous source reuse, новый reviewer report, source hash/diff/selected checks; conservative current logical read charge2MiB <4MiB. Historical cached charges не являются повторным чтением в этом packet. Physical RSS/CPU/I/O не измерялись. Source engineering cycle8/8 исчерпан: автоматического девятого correction нет. Root runtime DOC07 used3/4 неизменён; sole remaining GREEN — только Root после independent high source R. C08/native/finalCI/science limits не менялись.

Сохраняются явные owning boundaries: selected child и original inventory provenance, source extraction/allowlists и opaque review association исходят от owner; pure helper проверяет их exact relationships, не подпись/доверие из текста. C1/finite precondition остаётся caller-owned. Structured public pointer sources читаются как JSON; symbol extraction не заменена Julia evaluator; научная интерпретация и unit normalization остаются owning producer. Ни source correction, ни будущий software GREEN не создаёт production known-origin capture или scientific acceptance.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все шесть collated source findings обработаны | Trace и exact module/regression hashes выше | Нужен independent high R; runtime не запускался | изменить |
| Frozen assertions/C1/loader/исторические artifacts сохранены | Prefix cmp0 и unchanged hashes | Root publication отдельно | сохранить |
| C2 semantics/runtime приняли | Новых runtime свидетельств нет | Sole GREEN ещё не выполнялся | дополнительно измерить |
| Production/native/scientific acceptance достигнута | Свидетельств нет | Owner boundaries и отдельные gates выше | данных недостаточно |

STOP после final source correction.
