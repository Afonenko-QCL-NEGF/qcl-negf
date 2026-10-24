# DOC06 schema correction I1: independent high source CPP

2026-10-20. Verdict: **PASS_SOURCE_CPP_I1**. Блокирующих source findings не
найдено. Принято соответствие узкой source-реализации reviewed D и сохранность
прежних controls. Не установлены compiler/type correctness, unit GREEN,
actual projection/meaning acceptance или какой-либо native/scientific gate.
Этот verdict не является новым execution grant.

## Exact input identity

Worktree `/tmp/qcl-doc06-schema-fix-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`, изменены только два owning Root paths.
Все8 submodules здесь не initialized (prefix `-`), gitlinks соответствуют HEAD;
они не обновлялись. Exact actual authority — ранее frozen nine-source snapshot,
а не отсутствие component working files в этом worktree.

| Input | Bytes | SHA256 |
| --- | --- | --- |
| ops/docs/static-slice.ts candidate | 48269 | aa476aabdb044b020040816fdf7c2f7983082d28f6c15b01ccf1cbae307998ee |
| tests/docs_static_slice_test.ts candidate | 45959 | ec4f0d5c323bf3c1d81c5073516c1b7648e0aba3e49c14b4cbdd8a65e6d41e04 |
| complete patch | 24954 | 31f2192473c1ee7c1a0ca5c837545cb2222e4fbd0709fdbf0a685cddd45d4174 |
| author identity | 3811 | 9cef061f6f6e4268dba89689382deed7a8bf8ecde1ac07a428c47f58a2b78bcd |
| author report | 8492 | a79587069a6d68f452472b69ae77b447bfcda611dd33aa13ee2b8e4388947556 |

Candidate и complete patch hashes независимо пересчитаны. Дополнительно actual
`git diff -- ops/docs/static-slice.ts tests/docs_static_slice_test.ts | sha256sum`
дал тот же complete patch SHA: report соответствует именно увиденному diff.
`git show HEAD:… | sha256sum` подтвердил baseline adapter
`3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`
и baseline tests `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69`.

Reviewed D SHA `3a655b213799ce5ead32a1acec7aa0f05cd1effb8d2750e76fb10d271fac818b`
и independent D review SHA
`e224495073190f73277fefb7189d3c40f814e7c846dab1a7d14470cfaa2605ce`
совпадают с принятой постановкой. Причины M1/M2/M3 сохранены в meaning review
`4c35b2517718e3b9a137047a45652c4924de7e21ae3ad9041cd8d1e90df56861`;
старые actual output bytes не редактировались и не переименовываются в success.

## Primary source и M1 classifier

Selected Contracts schema SHA62df4ac2…e58b, root allOf`:179–423` и
production`:1420–1441` повторно сверены как первичные источники. Пять реальных
footprints: run→algorithms, run→algorithms, run→run, execution→algorithms,
scattering→physical. Actual leaf содержит integer/minimum1/description/no own
default и production required membership. Никакой target parser не запускался.

Candidate adapter`:564–605` читает literal root required до проверки composition.
Root type/required проверяют shape; successful membership имеет `/required`.
Поздний selected-context failure не перезаписывает это independent наблюдение.
Missing source получает source_missing и `/required`, а не fabricated false.

Root allOf принимается только после проверки nonempty array, ordinary object
items, allowed keys if/then, наличия обеих clauses, ordinary clause с единственным
properties, nonempty own-key dictionary и отсутствия production в любой стороне.
`else` и дополнительные item/clause keys отклоняются. Root anyOf/oneOf/if/not
не разрешены generic root allowlist; root `$ref` отдельно отклоняется.
Scalar/boolean item/clause и missing/empty shape откажут через object()/explicit
checks. `failurePointer` перед каждым шагом даёт locator проверяемой структуры.

Actual unrelated nested predicates, refs и combinators остаются opaque значениями
под другими immediate properties: `:568–600` их не вызывает и не разрешает.
Это scope classifier source syntax, не вычисление предикатов или валидация instance.
Footprint фиксируется в source order, поэтому та же raw source даёт тот же
порядок evidence. Selected production/leaf пути по-прежнему проверяют unsupported
keywords/ref siblings, local-only refs, cycles/hops и scalar shape (`:608–683`).
Неподдержанные selected contexts не превращаются в known/default-absence.

Успешные прямые type/minimum/required/default/description declarations извлекаются
после classifier. Combined constraint источники содержат resolved leaf и
resolved production required pointer (`:993–996`). Последний строится из
production.location (`:643–647`), не hardcoded canonical name, поэтому existing
escaped JSON pointer semantics сохраняется. Offending extra-key segments
экранируются `~→~0`, `/→~1` (`:512,531–534`). Ref targets сохраняют исходную
escaped pointer spelling как source locator, тогда как lookup декодирует сегменты.

`schema-validation-coverage` (`:1006–1017`) всегда partial; successful footprint
получает authored-context и текст об отсутствии predicate/full validation;
unsupported получает dynamic-unknown+reason. Нет application_release/run или
complete coverage promotion. Отсутствие own default keyword ограничено recognized
direct leaf (`:958–968`), не подменяет actual assignment или numeric origin.

## M2/M3 text, status и mode

Units success копирует literal description. Failure branch`:945–956` различает
description_absent от всех остальных reasons; source_missing/unsupported не
называются отсутствием данных. Текст effects`:1018–1029` при failure не обещает
несуществующую цитату и не утверждает unsupported scheduling meaning.

Effects success имеет partial/authored-context с exact description source;
formula-origin success`:1039–1050` — not_applicable/authored-context; failure
обоих — unknown/dynamic-unknown+reason. Это соответствует D и устраняет mismatch
M3. Formula/threshold rationale не извлекаются из идентификатора. Core default,
fixture explicit value, synthetic17/23 и неизвестный effective/assigning instance
origin остаются разными контекстами; их код diff не меняет.

## Controls и объём изменения

`git diff --numstat`: adapter119 insertions/27 deletions; tests162 insertions/
0 deletions. Независимый
`git show HEAD:tests/docs_static_slice_test.ts | cmp -n 35095 - tests/…`
завершился exit0. Это подтверждает **каждый byte старого canonical test prefix**,
а не только имена или количество: старые assertions, external preparedSymlinkFixture,
sentinels и baseline control meanings сохранены.

Manual source expansion новых registrations:

| Группа | Count | Отличающее свидетельство при будущем исполнении |
| --- | --- | --- |
| Unrelated conditional positive | 1 | Direct declarations/default absent, two constraint sources, partial footprint, authored modes, all10/null identities, facts+receipt determinism |
| Selected production in if/then | 2 | Обе стороны fail closed и exact production pointer |
| Unknown item keys | 2 | else и escaped extra key не игнорируются |
| Root-wide clause keys | 5 | required/additionalProperties/not/ref/escaped key отказывают с exact locator |
| Root anyOf | 1 | Context unknown при independent root required |
| Selected production/leaf combinators | 2 | Preserved selected failure + reason-aware unknown text |
| Escaped required source | 1 | Resolved leaf и required locators p~1~0q |
| Direct false root membership | 1 | Literal membershipfalse, selected context остаётся unknown |
| Description absent/source missing | 2 | Reason/text/mode/status distinction, independent typed79/example31 |
| No composition | 1 | Explicit partial validation coverage even without allOf |

Всего новых18; вместе с previously reviewed baseline56 это static expansion74.
Discovery не выполнялся. Positive/negative root pairs не могут пройти за счёт
тотального «всё unknown»: positive требует known direct declarations; negative
не может пройти за счёт общего refusal, поскольку assertSchemaUnknown требует
partial projection и independent facts. Новые controls используют inert source
strings и trusted adapter API; remote `$ref` в unrelated branch остаётся bytes.

Tests не исчерпывают все malformed classifier shapes (например empty array или
boolean item отдельно не зарегистрированы); их source branches проверены выше.
Это не обещание полного arbitrary-schema coverage и не основание расширить scope.
Runtime исходы всех74 и actual5-branch output ещё должны быть отдельно измерены.

Diff не меняет bounded parser/caps/read permissions/file identity/symlink checks,
fresh output/pending publication, CLI, target-loading capability или shared shape.
Новые footprint/extra source rows проходят существующие fact text/JSON output
caps; overrun по-прежнему refuse, не truncation. Новый eval/import/run/net/env/FFI
path отсутствует. `git diff --check` exit0 подтверждает только whitespace;
formatter/compiler/parser/test correctness из этого не следует.

## Limits и завершение

Этот review выполнял только inert source/diff/metadata/SHA/cmp/Git reads и
собственные report/identity writes. Target/parser/compiler/formatter/harness/
tests/Deno/native/network/solver execution0. Source/product/checkpoint/Git/
original packet writes0. Conservative logical source read upper1.5MiB≤3MiB;
wall<15min; CPU/RSS/physical I/O reviewer не измерялись. Report<128KiB.
Подагенты не использованы. Отдельный Root executor сохраняет counters и grants.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| M1 classifier/declaration separation соответствует D | Candidate:564–690; exact actual schema footprints | Source reasoning, не actual rerun | сохранить |
| M2/M3 reason/status/mode исправлены в source | Candidate:945–1050, paired regression assertions | Новые output artifacts ещё отсутствуют | сохранить |
| Baseline56 controls/capabilities сохранены | Exact35095B prefix cmp, bounded two-path diff | Tests ещё не выполнялись | сохранить |
| New74 registrations прошли | Только static18+baseline56, no discovery | Нет unit/compiler evidence | дополнительно измерить |
| Actual schema facts/meaning приняты после исправления | Candidate source only | Нужен отдельно разрешённый bounded engineering packet и meaning review | дополнительно измерить |
| DOC03/render/native/science/full release готовы | Таких evidence нет | Source CPP не заменяет эти gates | данных недостаточно |

STOP: PASS_SOURCE_CPP_I1; только own review/identity. Никаких retries, новых
product calls или дополнительного source round этот verdict не разрешает.
