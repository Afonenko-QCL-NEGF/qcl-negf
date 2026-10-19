# RV09 correction round1 receipt

Scope: две review corrections, без source/science/test changes и без выполнения предложенной команды. T03.3 разделяет diagnostics return и assessment gate failure; selected Contracts check явно negative-only, принятие matching valid commit unknown. Denominator остаётся 18 properties / 6 packets.

| Artifact | Old SHA256 | New SHA256 |
| --- | --- | --- |
| RV09.md | `bc110846f1b12f09393d8bf42eaa60ae113b02947ea808038755db10266f775c` | `03586f8c3dd5b974e7c79ba166902b7ed9987b7a7ff0dac8d28e328458b49ccd` |
| fixes/RV09-selected-check.md | `e40f9fe1dc2214884c80d4acaa61bf62694d36a82c37f185388deef5b81f8c70` | `ac155c26432e386143bbfa528c87b24538958e66c316159ee949b925e665523c` |
| cards/RV09-properties.md (unchanged) | `a673849693a4cc2973298f56d751d8148efeb7893b6376b36986bfcff5c20637` | `a673849693a4cc2973298f56d751d8148efeb7893b6376b36986bfcff5c20637` |
| fixes/RV09-oracle-gaps.md (unchanged) | `9257709e4d294466565b5cd4a47ddccc517938cb7f7d90e2114b60b16b0940c5` | `9257709e4d294466565b5cd4a47ddccc517938cb7f7d90e2114b60b16b0940c5` |

Scoped diff: cards/RV09-round1-correction.diff SHA256 `acbdc17a780db550eb5ff061b98773049e4c1bab7aa9478d3622989aeec31d24`.

Source recheck: C3108150dd1b6b1377470b384b15c26e272fe5c5d src/numerics/reference/poisson.jl:50–63; src/numerics/reference/validation.jl:636–640,751–775. K923e0c6cd9cbbe63bd1fb9c77892ef171385ed76 tests/test_state_identity.py:7–18. No numerical/runtime verdict; M02/M05 remain not_measured.

Writer round1 began 2026-10-14 18:43:53 UTC; completed 2026-10-14 18:46:29 UTC (156s shared writer envelope including source review and text/hash validation). Limit ≤5min, 1 CPU / 1GiB; only lightweight text/hash reads/writes, CPU/RSS not_measured. Independent scoped recheck pending docs_inventory.

Verification: all three touched source locators byte-match git show exact component commits; 18 unique property IDs retained; maximum report section 3663 bytes; exact selected command and finite budget unchanged. No numerical or runtime checks executed.
