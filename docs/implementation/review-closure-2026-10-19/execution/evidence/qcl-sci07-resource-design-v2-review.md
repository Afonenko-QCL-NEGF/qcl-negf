# SCI07 D2 — focused independent high source review

**Вердикт: PASS_SOURCE.** R1 и R2 закрыты узкими overrides; новых blocking findings в correction scope не выявлено. D1+D2 составляют принятый source contract для условного SCI08 source I. Native admission, BUILD/science READY и новые test/fault grants этим review не выданы; **needs_admission/needs_guard** сохраняются.

| Frozen input | SHA256 |
| --- | --- |
| `/tmp/qcl-sci07-resource-design.md` | `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635` |
| Prior R `/tmp/qcl-sci07-resource-design-review.md` | `48f97407846b4b179de2442e1295e8cc2028ed7d4e3ca9c2f28c8079ac5d4e67` |
| D2 `/tmp/qcl-sci07-resource-design-v2.md`,16555 B | `fc78a0c77394f4d12a1c5633b7e4acb587429667abc106f5aa72c1dc4dd9d010` |
| D2 delta `/tmp/qcl-sci07-resource-design-v2-delta.json`,970 B | `2c8974770340f32233ff825009fc9c099ddc20f9534012262d21d4ed2d896667` |
| D2 identity `/tmp/qcl-sci07-resource-design-v2-identity.json`,4795 B | `62d497cf6c52ac2ed0a9870a98f6d41d424673d2ab2070a5251c8a298d101a9b` |

D1 ledger и identity сохраняют прежние SHA `cf625aefd68f7335e34a5cb07900ee743e8e6ba45142bd79dbe99c26824fedfe` / `0d652cf597008ce67957d99c22e81a3ad147e31fd1ce620ed2dbdcff2b6b2479`; original report и D1 не переписаны. Новый файл — явно additive override, не потеря исторических bytes.

## R1: baseline и reservation normalization

Прочитаны D2 полностью, D1§6:233–245 и prior R1/R2. D2:34–48 определяет disjoint current E, unmaterialized U, proposed incremental P и unmaterialized S. Materialized/preallocated stop bytes уже в E; U→E не создаёт новый grant. G=U+P+S, T=E+G, overflow/unknown scope/view/epoch/overlap fail closed. Поэтому existing materialized bytes не списываются повторно как future growth.

D2:50–65 разделяет **total authority** T≤A и **remaining growth headroom** G≤H. Attempt128/256GiB, owner/per-FS constraints и campaign2TiB проверяются отдельно; нет прежнего min(total authority, remaining headroom). Logical, allocated physical и inode views не смешиваются; historical final/failure/copy residency входит в campaign E, outstanding obligations всех jobs — в campaign reservations. FS aliases/copy lifetime rules D1 сохранены.

D2:67–93 устраняет net reservation ambiguity: H относится к одному доказанному baseline до списания рассматриваемых U/P/S. Hnet допускает add-back только идентифицированного same-epoch disjoint R из ещё не materialized U/S. H=Hnet+R и G−R≤Hnet эквивалентны, но нельзя применить обе коррекции одновременно. Materialized/preallocated bytes, чужие reservations и protected reserves повторно add-back не получают. Unknown baseline/IDs блокирует admission; это не новый trust registry и не caller boolean authority. D1 checked-arithmetic requirement распространяется на normalization intermediates, включая Hnet+R.

Total hard quota относится к полному usage своего quota domain, а не к одному attempt E (83–88). Actual quota remaining и actual free имеют собственные coverage/reservation baselines; отсутствие полного domain mapping не реконструируется по догадке. Совместимый snapshot/in-flight reconcile остаётся required; sampled availability не превращается в hard enforcement.

Literal source oracles (95–119) корректны без выполнения: E90+U4+P8+S3=105GiB, G15GiB. Total exact-fit A105GiB и independent headroom exact-fit H15GiB проходят свои predicates. Уменьшение только соответствующей границы на1byte отказывает; другая граница не меняется. Net case Hnet11GiB,R4GiB даёт H15GiB и G−R11GiB, а Hnet−1byte отказывает. Таким образом отрицательные cases не маскируются одновременным изменением двух caps. Manufactured example не объявляет actual capacity. Unknown/overlap/materialized-as-reservation controls и stop-tail separation сохранены.

R1 **closed**. Минимальный SCI08 перенос теперь определён без выбора baseline по усмотрению writer.

## R2: immutable chronology

Независимо выполнены read-only `git ls-tree` **обоих exact refs**, а не mutable index:

| Component | e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b | 469ef4ec36c1dfb967856108e5f9455429559c15 |
| --- | --- | --- |
| Core | e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee | 9f4a96d032ad868ec010ce92d915bb81087c8d92 |
| Runner | 1acc165650fd4f4c2d49605cc679f90e3f6fcdae | fefaa27f194bfddf85dd51a0e255beef2218c06d |
| Platform | f5bc368654414039f7368bb19ca3201fa7f29f9d | f729e2681224d6537538179ab760fefefd575003 |
| AiiDA | d8f8092ca1c76523d85384b4bac8198d8bfa736b | d8f8092ca1c76523d85384b4bac8198d8bfa736b |

Остальные четыре Contracts/Portal/Research/Results gitlinks неизменны между refs. D2:123–153 и identity chronology соответствуют этим actual tree observations: D1 identity old published_gitlinks относится к initial e22, не к later head469. Published469 source graph установлен; final Code/release/plan/runtime BIND и scientific admission от этого не возникают. Список в review — forensic evidence, не поддерживаемый параллельный lock. R2 **closed**.

## Preserved scope и пределы

D2:167–174 сохраняет0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy и electron_electron=none. Сохраняются13 attempts/936 execution node-hours,72h/attempt, concurrency≤2, один threaded process/node, BLAS1, per-attempt128/256GiB resident и2/4TiB writes,4/8TiB reads,1GiB logs; shared2TiB/44TiB/88TiB/13GiB. Stop budgets остаются внутри этих caps. Physics/grid/basis/window/mixing/thresholds не меняются.

Все семь D1 SCI08 tickets сохраняются; baseline controls уточняют только R2/P1/C1. Их условная source readiness включает прежние gates: named owning Results consumer interface перед его I, complete bounded I/O/native coverage, fresh authority/allocation/FS/quota/counters, stop/quiescence proofs и independent source review. Missing mechanism остаётся needs_guard; missing facts — needs_admission. Source I может реализовать fail-closed behavior и tiny fake/literal controls; никакого source-only native pass не появляется. C08 exhausted не открывается ссылками на его fixtures; runtime calls отдельно bind/authorize coordinator.

Partial hypervisor READ metadata не является BUILD/science admission. Сообщённые coordinator CI host-key mismatch и role NoRoute — конкретные native blockers, а не новая authority D2. Их raw receipts reviewer не читал и factual/native verdict не устанавливает; это не ослабляет сохранённый refusal до fresh complete admission. D2 отдельно различает существование partial observations и отсутствие полного scientific admission.

## Учёт

Target runtime/import/parser/typecheck/tests/build/network/server/native calls/CP/product edits/Git mutations=0. Только source/text/hash/Git-tree metadata и два requested review artifacts. Primaries уже были прочитаны в D1 review; это focused correction rereview, не повтор полного source audit.

Named underlying content charge226071 B до создания report: каждое hash/ranged read начислено полным файлом. Conservative bound393216 B с reserve для Git metadata, filename lookup и generated-artifact hash reads, <2MiB. Начальный filename-only `rg --files /tmp` нашёл три candidate paths и получил permission-denied на чужих private directories; содержимое тех directories не читалось. Дальнейшие чтения — только явно named paths. Physical I/O/CPU/RSS не измерены. Envelope≤10min/1CPU/1GiB/output96KiB.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 total vs remaining baseline однозначен | D2§2–3, independent arithmetic выше | Source controls не исполнялись | сохранить |
| R2 chronology соответствует Git authority | Exact e22/469 ls-tree и D2§4 | Published graph не final/native BIND | сохранить |
| Seven tickets/model/caps сохранены | D1+узкие D2 overrides, immutable D1 hashes | Source I conditional; native/test prerequisites separate | сохранить |
| Native/BUILD/science READY установлен | Никаких native facts reviewer не измерял | Partial READ и reported blockers не admission | данных недостаточно |

STOP. PASS_SOURCE относится к D1+D2 correction contract; reviewer не запускает SCI08/native/tests и не меняет shared checkpoint.
