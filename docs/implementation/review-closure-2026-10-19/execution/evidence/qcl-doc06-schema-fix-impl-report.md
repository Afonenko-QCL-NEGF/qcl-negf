# DOC06 schema-context correction: I, source-only round 1

2026-10-20. Статус: **SOURCE_ONLY_AWAITING_INDEPENDENT_HIGH_CPP**.
Выполнена согласованная source-правка в изолированном worktree; executable correctness не заявляется.

HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`, branch `codex/review-closure-doc06-schema-context`, worktree `/tmp/qcl-doc06-schema-fix-worktree`. Initial git status был пуст; final status содержит только два порученных файла. В этом свежем worktree восемь submodules не инициализированы (prefix `-`); gitlinks присутствуют, source authority для actual анализа — frozen snapshot. Submodule update не выполнялся. Другие checkout, sourceRoot main, CP, originals и счётчики не менялись.

## Источники и порядок

Прочитаны accepted D `3a655b213799ce5ead32a1acec7aa0f05cd1effb8d2750e76fb10d271fac818b`, high D review `e224495073190f73277fefb7189d3c40f814e7c846dab1a7d14470cfaa2605ce`, M1/M2/M3 meaning review `4c35b2517718e3b9a137047a45652c4924de7e21ae3ad9041cd8d1e90df56861`; baseline architecture, implementation entrypoint и relevant snapshot schema/route regions. Snapshot не менялся и target-код не исполнялся.

Сначала appended regressions: tests SHA `ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04`, adapter в тот момент всё ещё baseline `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`. Затем source patch. Все bytes canonical test baseline `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69` остались точным prefix финального файла, включая external preparedSymlinkFixture и все старые assertions/registration names. Дополнительных RED вызовов не было: существующие actual A1/A2 — отрицательное semantic свидетельство исходного поведения. Новые регрессии ещё не выполнялись.

Применены executing-plans и test-driven-development в рамках explicit source-only задания. Ruling: команды skill, запускающие tests/скрипты workspace/commit, не выполняются, потому что explicit stage запрещает execution и Git writes; required fresh review ведёт Root. Это не TDD RED→GREEN или готовая runtime приёмка.

## Содержание

- Root `/required` извлекается до selected context checks и сохраняется при последующем failure.
- `allOf` проходит только nonempty array → exact if+then → exact properties → nonempty unrelated immediate own-key scopes. Opaque nested values не интерпретируются. `production` в любой стороне, extra keys/rootwide clauses и неподдержанные selected/production contexts остаются fail closed.
- Deterministic failure pointer содержит escaped сегменты; local refs/sibling/cycle/hop и bounded parse guards сохранены. Combined direct constraint cites resolved leaf и resolved production `/required`.
- Новый partial constraint context `schema-validation-coverage` сообщает footprint и отсутствие predicate/full instance validation. No-allOf case тоже explicit partial; all10 и run/release null остаются.
- Default absent ограничен отсутствием own keyword в recognized direct leaf. Description failure отделён от description_absent. Effects/formula интерпретация условна: success authored-context, failure unknown/dynamic-unknown с reason и без обещания цитаты.

## Финальные source identities

| Файл | Bytes | SHA256 |
| --- | --- | --- |
| `ops/docs/static-slice.ts` | 48269 | `aa476aabdb044b020040816fdf7c2f7983082d28f6c15b01ccf1cbae307998ee` |
| `tests/docs_static_slice_test.ts` | 45959 | `ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04` |

Patch: `/tmp/qcl-doc06-schema-fix-impl-complete.patch`, SHA256 `31f2192473c1ee7c1a0ca5c837545cb2222e4fbd0709fdbf0a685cddd45d4174`.
Identity: `/tmp/qcl-doc06-schema-fix-impl-identity.json`.

## Новые regression registrations

Старые56 сохранены по exact byte-prefix; добавлены18, статическое раскрытие всего74, в пределах заявленного envelope87. Test discovery не выполнялся. Имена:

- `DOC06 unrelated root condition preserves direct declarations with partial validation`
- `DOC06 root conditional selected production fails closed in if`
- `DOC06 root conditional selected production fails closed in then`
- `DOC06 root conditional rejects unknown item key: else`
- `DOC06 root conditional rejects unknown item key: item escaped extra`
- `DOC06 root conditional rejects root-wide clause key: required`
- `DOC06 root conditional rejects root-wide clause key: additionalProperties`
- `DOC06 root conditional rejects root-wide clause key: not`
- `DOC06 root conditional rejects root-wide clause key: $ref`
- `DOC06 root conditional rejects root-wide clause key: x/y~z`
- `DOC06 root anyOf keeps direct required independent`
- `DOC06 unsupported selected context preserves failure locators: production allOf`
- `DOC06 unsupported selected context preserves failure locators: leaf anyOf`
- `DOC06 escaped resolved production required uses its source pointer`
- `DOC06 direct root membership false remains literal under unsupported context`
- `DOC06 description failure keeps absence and unavailable distinct: description_absent`
- `DOC06 description failure keeps absence and unavailable distinct: source_missing`
- `DOC06 no root composition still states partial validation coverage`

## Self-review и ограничения

Текстовый diff перечитан. `git diff --check` exit0: только whitespace check, не formatter/parser/compiler. Проверен точный baseline-prefix старых tests; целевые imports/API/caps/permissions/symlink/helper/sentinel код не менялись. `git diff --numstat`: adapter119 insertions/27 deletions; tests162 insertions/0 deletions. Нет утверждения, что controls прошли; новые tests требуют единственного разрешённого будущего GREEN у Root после CPP/READY.

Source edit round1; code correction rounds0; предел2. Source/read cap4MiB: conservative logical reads≤2MiB (включая diff и repeated source чтения), report cap128KiB; wall<15min. CPU/RSS/physical I/O не измерялись; использовались короткие последовательные read/text-edit команды, без parallel heavy jobs. 1 CPU/1GiB ограничения не расширялись. Нет Deno/formatter/parser/typecheck/test/harness/native/network/solver execution. Нет Git mutation/commit/push. Старые unit2/2, E1 1/1, actual2/2 не сбрасывались. Будущие product calls — только Root по отдельному finite envelope.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Source M1 correction authored | schemaProjection narrow classifier, independent rootRequired, combined source locators | Нет execution; нужен independent CPP | изменить |
| Source M2/M3 correction authored | reason-aware units, conditional effects/formula status/mode | Outputs ещё не получены | изменить |
| Старые controls сохранены | Canonical tests exact prefix; diff source guards/caps | Не означает, что тесты прошли | сохранить |
| Runtime/actual semantic acceptance выполнена | Выполнений0 | GREEN и actual calls принадлежат Root | данных недостаточно |
| DOC03/render/native/science приёмка установлена | Таких gates здесь нет | Source-only stage | данных недостаточно |

STOP для independent high CPP; дальнейших edits/commands product здесь нет.
