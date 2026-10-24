# D6 delta ledger — только D5-R1 lifecycle

Bases: D4 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`; D5 `6049f427a10c769b69c2beaaa1374e583d217d6eb68926337204e560b824ed48`; highD5 `bb0319a40211616d36316c0adf04b8b0ac1f9bdefb8c71d274a96aecb3fd5d7d`; highI2 `5b7ec1e5f1fefad767315f539fe637c12c322902c78d542acea16639931ced60`.

| Override | Frozen source locator/problem | D6 exact amendment |
| --- | --- | --- |
| Closure scopes | D4:132–134 + D5:78–81/149; live producer/driver in same cgroup | §1 command descendants / phase driver subtree / whole workload различаются; only outer parent проверяет whole-empty после producer exit |
| Driver finish response | D5:121 `finished.terminal_ref` waits final receipt before required driver reap | §2 `finish-validated`≤16KiB с immutable pre-closure validation_ref и terminal:false; driver exits без ожидания final phase ref |
| Final phase publication | D5:149 generic terminal receipt | §3 exact phase receipt после driver EOF/reap; live setup разрешён, whole_workload_empty=not_claimed |
| Parent control ACK | D5:81 completion-ack.terminal_ref ambiguous | §4 producer setup-closing + parent completion-ack(exit,phase_set_digest); ACK не setup acceptance; final setup receipt создаётся только parent после выхода producer |
| Initial-empty | D5:74 factory may read empty for its own occupied cgroup | §1 outer pre-bootstrap observation + active allocation/birth binding; current membership/limits remain live |
| Workflow claim | D5 client completion vs overall terminal claim | §5 preflight phase позволяет prepare; full docs success требует correct phase receipts+task/job exit0+parent final setup complete/whole-empty |
| Debit/failure finality | Lifecycle adds durable receipts/teardown work | §6 reserves inside existing global deadline/storage/caps;≤442368B lifecycle metadata + separately reserved fallback; no renewal/retry |

Не изменены D4/D5 artifacts, hello-first/capsule/four env, chunk/full pure Capture/projection/secrets, exact12/D2/native16/Git budgets/fixed13/history, one workload cgroup/existing trust root, separate compiler/DEV/GREEN/native/CI/science gates. Все9I2 findings остаются implementation gaps.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Narrow lifecycle cycle описан достижимым порядком | D6 §1–5 | Требует high recheck, не implementation pass | изменить |
| Source/runtime acceptance получены | Product/fixture/CP/target execution0 | Только документы | данных недостаточно |

STOP high recheck; нет иных scope changes.
