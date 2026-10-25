# DOC07 D2: narrow independent high CP_DESIGN review

2026-10-20. **PASS / CP_DESIGN APPROVED** на D2 SHA256
`20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b`
и canonical append patch SHA256
`fc9cf40c2a19c7d98369dca72af0922f37906635f0003cb14a57525cc2bee2f5`.
Замечания предыдущего R закрыты. Packet готов как frozen design basis для
отдельного C1 I medium после Root binding утверждённых bytes; runtime calls,
publication, C2 semantic implementation и integration gates этим review не
исполнялись и дополнительных grants не получают. STOP.

## 1. Exact inputs и preservation

| Объект | Проверенный SHA256 |
| --- | --- |
| D2 plan,55468B | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| D2 identity.md,14344B | `528ecfc40d1c1453321b768553387bd5d31672e42c571a62cd52bec71e427eb2` |
| Canonical proposal patch,9797B | `fc9cf40c2a19c7d98369dca72af0922f37906635f0003cb14a57525cc2bee2f5` |
| Original primary DOC03,88916B | `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb` |
| Canonical candidate,97722B | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Added canonical text | `491c0894ef50774d4d88aec8bf762243a11b567fe2b7dad86f1061d7346d68de` |
| Preserved D1 plan | `44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8` |
| Preserved D1 high R | `7b0c262a1368d53cd98ed964ba46ae3f037de4f5c9b3dd9ab0d89a8d6ceeebdb` |

Primary root file hash/size unchanged; targeted `git status --short --
docs/system/physics-documentation.md` empty. Contracts HEAD remains
`12fc26462bbab3df76904c6deb01f8c6596de7be`, component clean. Root checkpoint,
other source and Git composition не менялись рецензентом.

`cmp -n 88916 primary candidate` exit0. Candidate bytes после этого prefix
совпали cmp с clarification.txt. Regenerated labelled `diff -u primary candidate`
имеет ровно frozen patch SHA fc9c…e2f5. Patch содержит только EOF addition,
новый anchor `model-help-doc07-v1-clarifications`; прежние967 lines/anchors/
format contracts сохранены. Patch не применялся. Ранее reviewed five-format
inventory и owner boundaries остаются; source facts locator исправлен226–228.

## 2. Закрытие R1–R6

| Вопрос | D2/canonical clarification | Verdict |
| --- | --- | --- |
| R1 | Все десять classes обязательны, repeated contexts допустимы; нет exact-ten/max10/name uniqueness | Закрыт |
| R2 | Полные Origin/Atom/ValueOriginView matrices, unknown≠not_applicable, known-null≠missing, boolean≠numeric, finite boundary до schema | Закрыт |
| R3 | Closed binding/input_status reason maps, bound nonnull proof identities+fragment; unbound сохраняет known verified scalars | Закрыт |
| R4 | Только exact requested retained Fragment+Bundle+selection proof; отсутствует proof→inputs=[]; declared/used independent | Закрыт |
| R5 | Query-free public-emission pilot, no stripping/fetch/secret heuristics/new registry; reviewed source provenance обязателен | Закрыт |
| R6 | Private pure internal helpers, no IO/child selection/derive/re-export/новый receipt API; missing vs corrupt proof различены | Закрыт |

**R2.** bound ValueOriginView имеет known Origin/nonnull binding/reasonok и
все четыре primary452–463 proofs. unknown имеет unknown Origin/kind/[]/note,
null binding и ровно пять accepted non-ok reasons; not_applicable отдельный
применимый branch, а отсутствие receipt не становится N/A. Не добавлены
обязательный DOI, автоматическое measurement attribution или unit registry.
Quantity unit строковая/canonical по owning mapping; finite/duplicate-key
boundary остаётся отдельной от Schema.

D2 задаёт конечный reason priority для нескольких missing proofs. Hash/context
tamper attempted claim отвергается; законный override/scientific applicability
mismatch даёт unknown, не ложную атрибуцию. Это разбор accepted reasons, не новый
provenance source и не разрешение backfill из equality/history/current default.

**R3.** documentation bound/ok требует nonnull release_id/release-manifest SHA/
source revision/bundle SHA/fragment descriptor и semantic receipt→graph→bundle→
fragment proof. unknown/source_binding_missing, incompatible/wrong_release|
unsupported_version и unavailable/bundle_missing|fragment_missing всегда имеют
fragmentnull. Известные verified retained identity scalars на этих branches
не стираются. Actor UUID/attempt context обязателен после selected child.

Input available/ok, invalid/snapshot_invalid и unavailable/четыре accepted
reasons отделены от documentation binding/value_origin/science. Missing/invalid
used snapshot не заполняется plan/default. Available означает verified selected
metadata, а не полноту scalar projection; available/ok с inputs=[] допустим при
missing safe mapping. Это не ложный unknown snapshot и не scientific pass.

**R4.** Mapping теперь не свободный in-memory список и не current/global leaf
registry. Требуются exact UTF-8 Bundle/Fragment bytes, manifest digest/graph,
descriptor id/file/hash, requested id/source revision и привязка к retained
selected run/execution source/release receipt. Голого verified=true недостаточно.
Каждый projected path должен принадлежать этому exact fragment.inputs.

Отсутствующая/необслуживаемая public documentation может давать unbound fragment,
но checked retained bytes могут обосновать внутренний path slice. Verified used
selected-child snapshot не исчезает из-за served-docs availability. Declared и
used доказываются каждый отдельно; origin proof не наследуется от известного
числа/assignment. При отсутствии exact mapping inputs=[], current/first fragment
и весь plan не используются. Historical A не получает B/current context.

Фраза D2 «URL в View остаётся null» читается по его явной closed matrix и
canonical text как **fragment=null**, без nullable URL внутри descriptor и без
нового URL field. Нормативная shape здесь однозначна; нового D3 не требуется.

**R5.** Непустой или пустой query component/delimiter препятствует pilot emission;
URI не sanitizes stripping и не fetch. https/doi shape, userinfo/control запреты
не выдают automatic public/known origin. Query-free path тоже может содержать
private token: D2 правильно требует exact authored public source revision/hash,
versioned input allowlist reviewed recipe и retained owning source/build review
evidence. Нового доверенного URI registry/capture ingress/secret detector нет.
Harmless-query support не оставлено выбором текущему I; future reviewed recipe
contract отдельный. Это accepted public-output ограничение primary343–349,
728–741, не изменение physical value/model и не новая trust authority.

**R6.** Helper входы detached/bounded/checked; стандартный schema loader остаётся
dependency-free и existing optional validation extra offline. Private code
проверяет cross-document proof, не создаёт его. Missing proof остаётся accepted
unknown; доказанное противоречие/false bound отвергается existing ContractError.
Effective-chain known нельзя вывести из evidence.length>0. Public serialization,
receipt/capture formats и __init__ API не добавлены.

## 3. Compatibility и следующий C1

Новые clarification paragraphs не заменяют старые public fields или meanings.
Один schema resource/five distinct const-format branches/closed nested objects
и source-vs-value-vs-used distinctions сохранены. Canonical append повторяет
существенные R1–R6 нормы; operational /tmp candidate locators остаются только
в review packet, не в добавленном product prose. Prefix/schema-only no-binding
caveat сохранён и усилен явно, без scientific acceptance claim.

C1 medium получает конечный schema/shape contract без menus R4/R5. Existing
loader/schema test patterns применимы; new artifact не реализован и schema
validator не запускался. Перед runtime — Root exact binding и отдельный finite
targeted budget; этот PASS не расходует test call и не создаёт новый envelope.
C2 semantic proof implementation, owner integration, publication, browser/light/
offline/math и native BUILD остаются собственными gates. Positive shape fixture
с literal statusbound не заменяет positive semantic proof fixture.

## 4. Выполненные действия и ограничения

Только explicit text/Git read/hash/cmp/diff/rg на названных DOC07 artifacts и
primary document. Scope narrow, старый полный R не выполнялся заново. No patch
apply, product edits, imports/parsers/schema validator/tests/network/children/
Nix/Julia/build/solver/server/Git mutation/checkpoint writes. Единственные записи
— этот review и identity. Envelope≤15min/1CPU/2GiB/read2MiB/output64KiB.
Conservative repeated logical text ledger<1.5MiB; physical filesystem/Git object
I/O не инструментирован. Execution tree content не искался.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D1 R2/R3/R4/R5 ambiguity закрыта | Exact D2 matrices/retained proof/query emission policy | Code/fixtures ещё нет | сохранить |
| R1/R6 и full inventory сохранены | D1→D2 diff, private helper boundary/five formats | Предыдущее source review, не runtime | сохранить |
| Primary byte prefix не менялся | Full88916-byte cmp и regenerated patch SHA | Patch ещё не применён/не опубликован | сохранить |
| C1 medium design basis готов | No alternatives, frozen D2+canonical patch | Root exact binding/runtime budget отдельно | сохранить |
| Schema validity устанавливает bound/source/science acceptance | D2 явные separate proof/owner gates | Shape-only evidence недостаточно | данных недостаточно |

**PASS exact20e712…dcb8b / patchfc9cf4…ee2f5. STOP; ready C1 medium design only.**
