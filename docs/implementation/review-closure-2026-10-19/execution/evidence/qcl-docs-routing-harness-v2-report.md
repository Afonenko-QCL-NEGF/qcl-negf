# Routing harness v2 — точная коррекция R1/R2

Исправлены только два замечания high review
`/tmp/qcl-docs-routing-harness-review.md`, SHA256
cf055fe95961e674834565bf13080de67ce640edb7fd66136b3dc31fef5bb995.
Все v1 artifacts сохранены. Execution/target parser/import/tests/native/network,
product/checkpoint/commit/push=0. RED не запускался, READY/acceptance не созданы.

R1: reviewed_module больше не использует SourceFileLoader/exec_module.
Он читает source bytes ровно в один buffer, проверяет SHA256 этого buffer,
передаёт эти же bytes в compile с explicit source filename,
dont_inherit=True, optimize=0 и исполняет code в свежем types.ModuleType.
Явно установлены __file__, __package__='', __loader__=None, __cached__=None,
ModuleSpec с origin и has_location. .pyc не читается и не пишется этим путём.
Это относится только к двум trusted guard dependencies с прежними pinned hashes;
fixture/production helper/target этим механизмом не исполняются. Guard source
checks до/после сохранены. Это code binding, не adversarial sandbox.

R2: READY schema теперь имеет обязательное поле red_predecessor_ref.
Для RED оно null; GREEN требует exact {path,sha256} на canonical owned regular
`/tmp/qcl-docs-routing-red-acceptance-v2.json` (≤32KiB). Acceptance имеет exact
schema и ACCEPTED_RED/diagnostic/interpretation literals, binds genuine RED
receipt/raw refs и фактические **те же** v2 harness/plan/fixture/runtime identities.
Оба будущих calls используют одну v2 harness/plan пару; никаких guessed future
hashes или наследования v1 attempt нет. Root создаёт acceptance только после
независимой проверки реально сохранённого RED evidence.

GREEN до reservation независимо читает retained RED receipt и original raw:
фиксированные `/tmp/qcl-DOCS-ROUTING-RED-1/receipt.json` и `original.log`,
canonical/owner/type/size/hash, обязательное наличие всех проверяемых observations.
Проверяются positive nonzero exit без signal, stop/error=null, complete capture,
no overrun, exact command/cwd/env/limits/dependencies/source/runtime/harness/plan,
helper=null и RED predecessor=null. Sample count≥2; wall/RSS/TMP observations
должны укладываться в прежние пределы. Raw digest/size должны совпасть и с
receipt, и с acceptance; точный считанный raw buffer хешируется повторно.

Из original bytes удаляются только ANSI control sequences для diagnostic match.
Требуется ровно один literal
`Module not found "file:///tmp/qcl-docs-test-routing-worktree/ops/docs_tests.ts"`,
один `Module not found` и один `error:` marker. Unknown/ambiguous layout блокирует
GREEN; никакого automatic rerun/alias/format relaxation. Root ACCEPTED_RED
assertions без genuine receipt/raw или с guard failure недостаточно. Trusted
Root acceptance остаётся active handoff, не криптографической аутентификацией
от same-user подделки. Одни diagnostic substrings также не заменяют независимое
прочтение Root полного original report: accepted interpretation обязана
подтверждать expected missing module only.

Точные READY/acceptance fields и symbolic actual-hash values опубликованы в
v2 plan. На RED missing-module load failure не превращается в227 executed tests;
nominal227/observed=null и review-required unit semantics сохранены.

Single frozen Deno argv, нулевые script read/write/env/run/net/ffi grants,
clearenv DENO_DIR/TMPDIR/HOME, caps120s/1CPU/1GiB sampled RSS/16MiB owned TMP/
2MiB raw, оба exact attempt names и no retries не менялись. Before/after source
checks сохранены; runtime hash проверяется только перед child, не заявляется
новая terminal runtime measurement. Полный лог и retained TMP не удаляются.
Resource metrics остаются sampled с возможным overshoot, не hard peaks/quotas.

Проверка этой коррекции — textual source read и deterministic artifact generation.
Никакой compile/exec/import самого harness, guard dependencies или target,
selftest/parser/typecheck/runtime не запускался. Подготовительный Python только
обрабатывал текст и JSON метаданные. Named source reads reserve≤512KiB<2MiB;
physical I/O/CPU/RSS не измерялись. Owned output artifacts<128KiB.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 связывает executed guard bytes с source SHA | exact buffer→SHA→compile→fresh ModuleType source | Runtime не выполнен; trusted guard source предпосылка сохраняется | изменить |
| R2 запрещает GREEN без принятого genuine RED | mandatory READY ref и direct receipt/raw checks | Root authority и полная интерпретация retained evidence внешние | изменить |
| Command/permissions/caps/count claims сохранены | v1→v2 только R1/R2 source correction и plan bindings | Source-only; GREEN/full CI/native acceptance отсутствуют | сохранить |
| Исправленный harness принят | Только author correction artifacts | Требуется тот же независимый high re-review | дополнительно измерить |

STOP для повторного high source review. Ни один engineering call не разрешён
данным author report.
