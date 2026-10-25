# Docs-routing harness v2 — независимый high re-review R1/R2

Вердикт: **PASS_SOURCE_R1_R2** для exact frozen v2 artifacts. Новых blocking
findings в проверенной delta нет. Это принятие исправлений исходников, без
разрешения execution, READY, source I или последующих engineering calls.

| Артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-docs-routing-local-unit-run-v2.py`,21924 B | `0061c27ec61bf8ca15d6e94d304db695072b12adc3fe6ca8ddef2ee254df82e7` |
| `/tmp/qcl-docs-routing-engineering-plan-v2.json`,9979 B | `5147cab0a8df1d50fb908b3c247e8c7b0e11852ee01a990f8a35228b3e70157a` |
| Author v2 report,6298 B | `adbe4ed2aa3f96246ea68a5d49972eff10a4aa3a2007b3fe5e0fc7a473e4378d` |
| Author v2 identity | `910d1f6550f9c329144e694d66615d6ce2f026a8426e2a0f934a7f3146576c3f` |
| Original independent R | `cf055fe95961e674834565bf13080de67ce640edb7fd66136b3dc31fef5bb995` |
| Frozen fixture | `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` |

Проверены exact textual v1→v2 diffs, actual source regions и v2 plan/report.
V1 harness `4dbc78e81ff40f4a70e317dce8e7538dfe5f0f68f458896a8bf910309fae2920`
и v1 plan `e21b6446c4a83275e0b3877c2d32271a887ce2ea48baafe3bf5d424157cb0591`
сохранены. D1/D2 и accepted fixture review остаются прежними основаниями;
повторного полного fixture/production integration review не было.

## R1 закрыт

Harness:61–74 читает dependency source один раз в `source`, проверяет SHA256
этого buffer и передаёт именно этот buffer в
`compile(source,str(path),'exec',dont_inherit=True,optimize=0)`. Код исполняется
в новом ModuleType; explicit file/package/loader/cache/spec metadata установлены.
Ни SourceFileLoader, ни source module .pyc в этом пути не используются.
Это устраняет обнаруженный в v1 разрыв source hash→executed guard code и
автоматическую запись cache самим прежним loader.

Вызовы235–236 относятся только к двум pinned trusted guard dependencies.
Target/fixture/production helper этим механизмом не компилируются. Предварительные
dependency checks234 и терминальные source checks324–327 сохранены. Обычные
stdlib imports по-прежнему опираются на trusted Python runtime; adversarial
sandbox/полная runtime closure attestation этим изменением не создаются.
Исторические cache identities и результаты не пересматривались.

## R2 закрыт

Exact READY schema204–205 теперь требует `red_predecessor_ref`. RED218 требует
null. GREEN230 вызывает accepted_red до runtime/guard imports и permanent
GREEN reservation239. Поэтому отсутствие/несовпадение predecessor блокирует
GREEN до создания его attempt directory.

`accepted_red`:87–128 устанавливает цепочку:

- Exact bounded canonical owned regular acceptance path с hash; exact acceptance
  schema, ACCEPTED_RED, fixed diagnostic/interpretation.
- Same scope/RED attempt и фактические v2 harness/plan/fixture/runtime identities
  в acceptance и retained receipt; v1/другой harness replay не подходит.
- Fixed canonical owned retained RED receipt/raw paths с size/hash; required
  receipt observations присутствуют. Positive nonzero child exit, helper=null,
  RED predecessor=null, exact argv/cwd/env/limits/dependency hashes обязательны.
- Guard/capture errors и stop_reason должны быть null; capture complete,
  no output overrun, sample_count≥2, sampled wall/RSS/TMP в пределах. RED остаётся
  nominal227/observed_engine_tests=null.
- Raw size/hash согласованы с receipt и acceptance; actual raw buffer читается
  и хешируется повторно. После удаления ANSI CSI требуется ровно один expected
  missing-module URI diagnostic и по одному Module not found/error: marker.

V2 plan явно требует Root inspection настоящего полного raw/receipt перед
созданием acceptance. Набор substrings не доказывает отсутствие любой иной
ошибки; это сохранённая внешняя обязанность независимой интерпретации полного
original report. Произвольный same-user JSON не становится аутентифицированной
Root authority. Unknown formatting fail closed; оно не разрешает rerun,
alias attempt или автоматическое ослабление matcher.

Actual RED и GREEN используют одну неизменную пару v2 harness/plan. Receipt336
сохраняет predecessor refs для GREEN; RED получает null. Circular future hash
binding не введена: реальные receipt/raw/acceptance hashes создаются только
после будущего RED, без изменения plan и исходников.

## Сохранённые условия и пределы

Textual delta сохраняет exact singlefile Deno command212, empty script grants,
полную замену child env246, две exact attempt identities, no retries,
120s/1CPU/RLIMIT_CPU, sampled1GiB RSS/16MiB TMP/2MiB raw и byte-preserving
capture/failure handling. Runtime hash проверяется только до child233;
terminal runtime measurement не заявляется. Никакая версия не измерена.

RED остаётся compiler/loader missing expected module evidence, не227 executed
assertions. GREEN требует отдельного source I/import-purity high review,
fresh Root READY и принятого genuine RED; затем отдельного результата review
полного TAP227/names/counters/exit/guards/source bindings. Guard return0 и
review-required receipt не означают unit pass. Pure GREEN не закрывает actual
task/workflow/CLI integration, native admission/build/full CI/scientific gates.

Read-only inventory: Root HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`,
исходный dirty status сохранён; все8 gitlinks перечитаны без обновления.
Fixture worktree HEAD `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, status только
untracked fixture. Helper, acceptance, RED/GREEN attempt directories отсутствуют.
Architecture/применимые основания прочитаны в исходном review и не менялись
этим re-review. Guard/parser/compile/exec/import/test/runtime/native/network=0;
product/checkpoint/index/commit mutations=0.

Консервативный reserve named reads≤256KiB<2MiB; physical I/O/CPU/RSS не измерены.
Созданы только requested v2 review и identity, суммарно<96KiB. Проверка исходников
и diff не заменяет runtime проверку failure/cleanup/resource predicates.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 exact buffer связывает код guard dependencies с SHA | Harness61–74,235–236; exact diff | Trusted Python/stdlib premise; execution0 | сохранить |
| R2 требует accepted retained RED до GREEN reservation | Harness77–128,204–239; v2 plan | Root authority и full diagnostic interpretation внешние | сохранить |
| Focused command/caps/count semantics сохранены | Exact v1→v2 diff,212,246,336–340 | Sampled guards, возможный overshoot, не hard/adversarial proof | сохранить |
| RED/GREEN либо native/full-CI acceptance выполнены | Execution0; отсутствующие attempt dirs | Только source acceptance | данных недостаточно |

STOP. PASS_SOURCE_R1_R2 не является runtime approval и не создаёт READY.
