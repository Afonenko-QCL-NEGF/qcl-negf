# Read ledger — RED diagnostic source erratum

Учёт ведёт logical full-file charges, не физический I/O. Каждое `cat`, `rg`, `sed`/`nl` extract и `sha256sum` conservatively списывает полный underlying regular file. `wc -c`, directory names, existence checks и Git metadata вынесены в reserve. Чтение payload archive/cache/owned-TMP/runtime отсутствует.

| Путь/группа | Полных чтений | Charge, B |
| --- | ---: | ---: |
| using-superpowers SKILL,3192 B | 1 | 3192 |
| systematic-debugging SKILL | 1 | ≤16384 |
| root docs/architecture.md,5501 B | 1 | 5501 |
| retained receipt.json,2724 B | 3 | 8172 |
| retained original.log,765 B | 3 | 2295 |
| red-v2-identity.json,2548 B | 2 | 5096 |
| design-v2-identity.json,5064 B | 1 | 5064 |
| red-v2-review-identity.json,2539 B | 1 | 2539 |
| fixture,38723 B (rg1; extract4; hash1) | 6 | 232338 |
| design-v2.md,17745 B (rg1; hash1) | 2 | 35490 |
| design.md,17703 B (hash1) | 1 | 17703 |
| red-v2-report.md,9578 B | 1 | 9578 |
| red-v2-review.md,9428 B | 1 | 9428 |
| red-report.md,11082 B (rg1; extract1; hash1) | 3 | 33246 |
| harness-v2-identity.json,890 B | 1 | 890 |
| harness-v2-report.md,6298 B (cat1; hash1) | 2 | 12596 |
| harness-v2-review.md,8446 B (cat1; hash1) | 2 | 16892 |
| engineering-plan-v2.json,9979 B (cat1; extract1; hash1) | 3 | 29937 |
| RED-1-intent.json,82289 B | 1 | 82289 |
| RED-1-result.json,82773 B | 1 | 82773 |
| local-unit-run-v2.py,21924 B (extract2; hash1) | 3 | 65772 |
| design-v2-review.md,3299 B (cat1; hash1) | 2 | 6598 |
| generated report/ledger/identity verification reads reserve | — | ≤65536 |
| Git/metadata/name-discovery/residual accounting reserve | — | ≤131072 |

Консервативный суммарный bound ≤983040 B <1048576 B. Reserved bytes не считаются измеренными физическими reads. Никакой source payload не запускался. Named source/output hashes фиксируются в identity.

Output limit64KiB: три generated deliverables проверяются по сумме actual stat sizes. Tool transcript bytes не инструментированы; несколько batch outputs усечены, соответствие суммарного transcript лимиту не заявляется. Нет утверждения physical CPU/RSS/wall peaks. Requested envelope10min/1CPU/1GiB выполнялся как source-only task scope; процессный limiter/measurement не устанавливался.
