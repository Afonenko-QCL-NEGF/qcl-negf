# DEV11 — independent CP-CODE

**Spec compliance: PASS в scope DEV11. Quality: PASS; blocking source findings не обнаружены.** Это приёмка exact consumer implementation и ограниченных engineering fixtures, не all-green component suite, packaged browser, native AiiDA или release/scientific acceptance.

## Reviewed identity и действия

Frozen diff `/tmp/qcl-dev11-review.diff`, SHA256 `775fd77480598ad1be338282957ce62ae989688d88fd0070e63236afea773a98`, 56031B, Portal baseline `36837e98a8d1f85820f2807d0212ec92e73c3c7b`. Producer actual HEAD `5579d55684939495230241f446b7ea07c8ae0224`; Results `fe27a2a9ed065f9afacecc84113311f30d0c68d6`; Contracts `e5c056c47fc3bde3e0ca32866692d740ef9b325c`. Root epoch в author report — e0f244d; последующая root publication не переносит на себя эти fixtures автоматически.

Прочитаны DEV11 owning task, accepted DEV09 consumer contract, Portal AGENTS/CONTRIBUTING, exact diff и owning production/test paths. Независимо проверено: tracked `git diff --binary HEAD` byte-identical tracked portion frozen package; новая frontend test file byte-identical added payload; ровно десять разрешённых paths, без lock/schema/auth/theme/actor-lifecycle edits. `git diff --check` exit0. Reviewer не запускал tests/imports/build/server/browser/solver; standard-library metadata/hash checks не исполняли product packages.

Actual source SHA256:

| Path | SHA256 |
| --- | --- |
| README.md | bae2e93f1ddd8478081f2071186434466fc9f74cf6319031aa9c434b6b401bd7 |
| frontend/src/api.ts | 158c160eae13f9f5a9f0e71ab0e3a7ef35fad8a53a9761c5bde73953b33ed7c1 |
| frontend/src/main.tsx | 6abbc037617f0afda676fb693ad6205f68146049975b3463eda1e45767dd9888 |
| frontend/tests/export-selection.test.ts | 9529b3d28ca2fe2de2e2de306aa6ad36d33582246b9e478fb8f40913032c050f |
| src/qcl_negf_api/api.py | 1c6c76b3365d0b089dcbbafd410044a1a7ae9e0e70fac28e4b0986846c326f5f |
| src/qcl_negf_api/exports.py | 1cca17d802cf2b7a0a4b4ede133107ff19936029ef95a08e7451eefe33ff2ac5 |
| src/qcl_negf_api/service.py | 677d2984478fece3ac8af857563dda79959aefe2d57b1b5cb9d932b66fd2b99b |
| tests/test_api.py | f75bc1cde995ca3e846485f20448fcd13f41e3b00fc4fe4e4540cb350af3f5a0 |
| tests/test_exports.py | 1064ea3a62adf2e0145ad3db3769401e9988bbb2aa0058bf3d1c00b890962f7c |
| tests/test_service.py | cf6e8ca6bf14b6f21168b1d7a5f9db504d43e4b17b511f745954d4ba468d8cad |

## Независимые observations

- `exports.py:95–128`: run canonicalized; producer selection ровно один раз до cache/admission/scheduling; exact4-field response и strict positive attempt/canonical UUID/status whitelist проверены; detached scalar binding создаётся до следующего actor call. Inventory вызывается с обоими resolved selectors.
- `exports.py:129–149`: каждая row обязана иметь exact5-field shape и тот же execution/attempt/UUID. Bool attempt/size, invalid path, NUL, duplicates, negative size и over10000 rows отклоняются; foreign row не фильтруется. Empty rows — missing404, malformed metadata —422; preparation ещё не scheduled.
- `exports.py:158–183`: cache key содержит canonical run/execution/attempt/CalcJob/profile; preparing/ready reusable только при равном freshly observed status. Changed status не переписывает старое entry; busy worker409, иначе новый ID с учётом retained reservation/128 limit. Failed/expired не reuse. Default published-selection switch поэтому не может вернуть чужой archive по старому3-tuple key.
- `exports.py:203–245`: exact frozen plan читается до копирования; plan/open получают оба binding selectors. Worker не обращается к `get_run`, не повторяет default selection и передаёт Results literal frozen status; `failed` при exit0 не становится completed. `unknown`/paused/running остаются nonterminal по unchanged Results `export.py:877`, без нового scientific policy в Portal.
- Existing byte-count checks, source/spool/free-space/receipt-tail guards, failed cleanup, single worker/TTL и download entry lifetime сохранены. Авторизация и Range/If-Range paths не изменены: composite download остаётся привязанным к export ID, single-file selectors/error mapping не переделаны. Existing regression test_api selected-child/capability cases сохранены; composite mismatch422 не меняет existing single-file404.
- `api.py:104–111,486–493`: additive optional/null selectors, strict positive integer и UUID normalization; existing extra/profile rejection сохраняются. `service.py:11–26` добавляет только registry operations в existing actor ownership path. Missing new operation даёт503 через `exports.py:87–93`, без all-attempt fallback.
- `frontend/src/main.tsx:38–110,700–704`, `api.ts:156–175`: выбранный child передаёт attempt+UUID; returned attempt/UUID/status отображаются отдельно от preparation state; download использует exact status.export_id и native anchor. Theme/CSS/auth/token persistence не меняются. Node fixture проверяет client POST/returned identity и native URL/отсутствие Blob; реальный DOM/browser не исполнялся.

## Existing execution evidence — с сохранением failure

Проверены actual receipts, raw logs и log byte sizes. Runtime attribution к frozen candidate опирается также на coordinator freeze и author report; reviewer не повторял execution и не получает independent native-profile evidence из synthetic fixture.

| Packet | Receipt SHA256 | Raw log SHA256 | Наблюдение |
| --- | --- | --- | --- |
| DEV11-GREEN-2 | 336b8e80d80c4a35672cf57c8141a5496054c630867595a4798828f464d22e01 | 5c4a9ee297388dd6dbdf8d04643ce3b6d51264f2bea972b873d57458033422da | exit1;125 passed,1 failed;7.461s;RSS191459328B;900B log |
| DEV11-GREEN-NODE-1 | d8d9c910e7bf223d84cf2d89dd52974a7e8bee4b673a690ffc1e48bbd417dd7b | 9dc634ba4407baa29b3764f2ba102686d4867b6cdff6b6a61a51ed15cd6fb244 |9passed;exit0;.436s;RSS155500544B;1944B log |
| DEV11-TSC-1 | 0597efdbcb8697dd8cae194257e979aed90f3a28c4e958dc48a5aede0bd3359b | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |exit0;no diagnostics;2.234s;RSS323313664B;0B log |

GREEN-2 failure точен: `tests/test_api.py:98–103::test_browser_is_served_from_the_python_package`, GET `/`404 вместо200. Независимо установлено отсутствие `src/qcl_negf_api/static`; baseline и candidate static-mount tail byte-identical (`api.py:522–525`), assertion неизменён. `hatch_build.py:12–14` требует generated assets при distributable wheel. Следовательно source evidence указывает на уже существующий missing-assets precondition этого checkout; baseline runtime не запускался. Этот failure нельзя записать как successful browser/package test. Он не является дефектом changed composite route, но package/browser gate остаётся unresolved до отдельного разрешённого build/check.

Основной composite fixture (`tests/test_exports.py:298–421`) вызывает actual producer functions над synthetic ORM/repositories: common same-size payload AAAA/BBBB, disjoint files, raw-different decoded-equal plans; assertions требуют bytes2/plan2/source2/status2, только C2 opens и ровно один resolve даже при switch после resolve. Последующие cases покрывают cache child switch, same-child late result, busy/TTL, legacy selector forms, invalid/mismatched/foreign selectors и malformed producer rows. Results exporter заменён tiny bounded exporter: это прямое consumer data-flow evidence, не real scientific array/archive validation. Actor fixture доказывает forwarding/owner-thread operations над stub profile, не native AiiDA deployment.

## Решения и границы

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Composite pinning/cache/status/API соответствует DEV09 | Owning source locators и exact frozen diff;125 targeted passes | Synthetic ORM/exporter | сохранить |
| Existing native download/single-file/storage paths сохранены | Narrow diff; retained regression assertions;Node native download9pass | Нет real browser/profile/server | сохранить |
| Whole Python packet прошёл полностью | GREEN-2 raw1failure | Missing generated assets; не замаскировано | данных недостаточно |
| DEV11 source можно принять в reviewed scope | Spec/quality review без blocking source findings | Producer-first coordinated publication/restart; build/native/fullCI gates отдельные | сохранить |
| Scientific acceptance или full release готова | Source/engineering fixtures | Нет numerical/convergence/grid/experimental evidence | данных недостаточно |
