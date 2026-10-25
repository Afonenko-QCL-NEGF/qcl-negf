# DOC07 C2 RED v2 — focused independent source review

Вердикт: **PASS_SOURCE**. F1–F5 из review `0c18812ea0c942bcc69a412fbc145ea8b970412dc3bf554481f5187a5befaae3` закрыты различающими source controls. Новых блокирующих замечаний в исправленном delta не выявлено. Допустим следующий уже выделенный Root-only RED; это не runtime PASS и не дополнительный grant.

## Exact input и authority

Actual base: `d791dea33f4628cf23c0b8552ebee9e51d7dd605`. Read-only `GIT_OPTIONAL_LOCKS=0` HEAD/status/submodule inventory: только `?? tests/test_model_help_bindings.py`, submodules отсутствуют.

| Артефакт | SHA256 |
| --- | --- |
| Actual test, 40274 B | `72240eab26305f63aeeec06197a7f64802c111a83cd3ef8aae603c5e89ae71f9` |
| Preserved v1 test, 31977 B | `71d6428f935ffe85ce70f9af2dd30fa480cf030e20ef96c9111e24e5cde22e7b` |
| `/tmp/qcl-doc07-C2-red-v2.delta.patch` | `6cbe7c8c6960ca80a04820fc0e5130cf5f770b3afd1e5ba9e1ef9c4c9d209356` |
| `/tmp/qcl-doc07-C2-red-v2-full.patch` | `0996d855b41dc2942c357141eb74bb192a469c2fc6dc0bac42e1b0e5039c3950` |
| Author report | `3a7093100c23594e0e4376976c877a0e766738aaeeb85a28207291e889290d90` |
| Author identity | `3eb9101061e11418a885ee35650d748f793157f5b62ff1297e4085e34884302e` |
| Frozen D2 | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| Frozen canonical DOC03 | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Existing C1 schema | `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241` |
| Existing C1 tests | `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177` |

Primary authority: D2 R6:131–145 private routines/checked detached inputs, R2:178 finite reason order, R4:201–207 exact requested mapping и независимые declared/used, R5:219 exact owning source/recipe review; frozen canonical proof obligations. Нормативная C2 часть не меняется DOC06 source-fact pointer erratum. Review опирается на actual delta/source, не на авторское заявление о закрытии; повторного handwritten C1 validation не требуется.

## Проверка закрытия

| Finding | Actual source locator и различающее свидетельство | Решение |
| --- | --- | --- |
| F1: stale outer hashes и несогласованный TEMP scalar маскировали guard | `repack`:241–281 переиздаёт fragment/payload/descriptor/file/bundle/publication/View hashes. При id mutation также заменяет descriptor id/path и View descriptor, оставляя requested selection id неизменным; :530–536 проверяет именно selected identity. `reauthor_reference`:284–305 обновляет authored annotation bytes, claim PublicRef, retained snapshot/receipt, public-review source ref, used Evidence/index digest. Condition duplicate :554–559 теперь представлен и в authored annotation, и в claim без stale-byte причины. TEMP :698–726 сначала имеет 70 K, exact frozen-plan/snapshot selectors, authored mapping/ref и проходит healthy validation; затем удаляется только mapping с корректным repack. | закрыт |
| F2: nonempty review tuple мог заменять exact association | :765–792 сохраняет другие reviews, но удаляет required parameter association либо подменяет source/revision/recipe; source replacement устраняет вторую review с тем же key, исключая случайный duplicate-key отказ. Receipt-byte mutation сохраняет старый digest. Исходная exact association предварительно healthy. Bool/nonempty shortcut теперь не различает ожидаемые исходы. | закрыт |
| F3: full chain мог сводиться к count>=2 | :795–808 сохраняет два Evidence и настоящие requirements, но заменяет runtime step на duplicate planning Evidence или существующий unrelated snapshot selector с действительным container digest. :811–827 при полном наборе steps отдельно повреждает requirements revision/hash/source bytes. Требуются exact chain membership и owning source proof. Missing-step/missing-universe controls сохранены. | закрыт |
| F4: absent claim vs unavailable source precedence | :368–378 для каждого missing annotation/parameter/graph проверяет `origin_not_recorded` при absent claim и `source_unbound` при present claim, без известного раннего mismatch. Это прямо различает требуемый порядок D2:178. Ранние N/A/value/override/conditions и ContractError tamper controls сохранены. | закрыт |
| F5: declared phase имела только negative | `case(claim_phase=...)`:87–88,140–143 формирует согласованные phase fields до кодирования retained claim bytes. :830–849 принимает declared bound/ok и фиксирует exact reference/annotation/parameter, phase, frozen-plan value/condition Evidence, assignment и claim receipt Evidence. Used positive :342 и declared→used negative :432 сохранены. Blanket declared→unknown больше не проходит. | закрыт |

Эти witnesses используют tiny authored literals, stdlib encoding/hash и источники самого fixture. Production semantic helper не используется для expected scalar, hash, selector или reason. Reauthor/repack изменяют synthetic evidence до вызова target; они не ремонтируют actual archive или production proof. Opaque review receipt не получает новую grammar/signature и не превращается в `reviewed=True`; exact source/recipe association остаётся owning detached input.

Замена TEMP mapping не вводит новый physical default или новую unit conversion: 70 K уже находится в том же исходном frozen point и snapshot. Declared positive использует существующую фазу и existing Evidence container. Generic private validation signatures, public serialized shape, source trust boundary, научная модель и допуски не расширяются.

## Сохранение и ограничения

Delta сохраняет прежние raw tamper/missing source, safe paths/URI, historical identity, alias/key/index, docs-unavailable и independent declared/used controls; изменены только test fixtures/helpers. Existing C1 hashes и v1 review/test hashes подтверждены. Отсутствие implementation остаётся ожидаемым source-level основанием initial RED; target import/collection в этом review не выполнялись, поэтому фактическая причина будущего RED ещё не измерена. Даже фактический missing-module RED не докажет semantic guards.

Source review не обещает исчерпывающую mutation coverage и не подтверждает scientific attribution или native/public acceptance. Checked owner bytes/context/allowlists и opaque owning review association остаются предпосылками private seam; это не разрешение untrusted filesystem/network lookup или выбора другого actor. Нового public format, parallel lock или публичного API не появляется.

Named read ledger: cached frozen DOC03/D2 и v1 source/review; actual v2 delta и changed helper/control ranges; narrow D2 authority ranges; author identity/report; exact artifact/C1 hashes и read-only Git identity. Conservative cached charge 2 MiB + текущий packet 1 MiB = 3 MiB, меньше 4 MiB envelope. Это upper accounting выбранных logical reads, не physical I/O/RSS/CPU telemetry. Выход меньше 64 KiB. Target imports/parsers/tests/build/network/Git mutation/solver/children: 0. Записи — только этот report и companion identity.

Shared DOC07 runtime остаётся 2/4 по coordinator accounting; reviewer потребил 0. Explicit source engineering cap8 не сбрасывается: fixture v2 — allocated cycle6; implementation cycle7 и максимум один owning repair cycle8 остаются отдельными действиями Root. Этот verdict не выделяет девятую правку, дополнительный тест или автоматический rerun.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1–F5 устранены на уровне test source | Exact v2 SHA, причинные пары и локаторы выше | Исполнение ещё не измерено | сохранить |
| Existing C1 и original evidence сохранены | Exact hashes и read-only status | Публикация вне scope | сохранить |
| Следующий finite Root RED может различить точку начала | Отсутствующий helper, новые immutable fixtures | Пригодность к исполнению не означает semantic GREEN | дополнительно измерить |
| Native/public/scientific gates пройдены | Свидетельств нет | Synthetic source-only review | данных недостаточно |

STOP — PASS_SOURCE; runtime и product не изменены.
