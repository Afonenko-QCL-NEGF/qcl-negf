# D5 delta ledger к D4 / I2 CPP

Immutable base D4 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`, highD4 `ca5a8d36b04ff6e5f52817da420b6fb3ca92e95d9e70e45c1ea6f44f74b9fb48`, highI2 `5b7ec1e5f1fefad767315f539fe637c12c322902c78d542acea16639931ced60`. Source-only; sourcepatch/execution/CP=0. Полный входной overlay и hashes в identity.

| Delta | Before / source locator | D5 exact decision | Compatibility / limit |
| --- | --- | --- | --- |
| D5-1 hello order | I2 `native.py:680–685` server-first challenge, CPP R4 | D5 §2 hello-first; никакого challenge/fetch-binding operation | D4 hello exact keys и peer/live-token checks сохраняются |
| D5-2 отсутствующие attempt/source при4env | D4:60/64–73; I2 client получает от challenge | Exact≤4096B base64url canonical capsule в прежнем PHASE_TOKEN; parent-held PhaseBinding и независимый server lookup | Явное private env-value codec amendment; names4/public descriptor не меняются; capsule не authority |
| D5-3 active factory route | I2 CPP R1/R7, `setup_main:694–708` always refusal | §3 exact constructor→ActiveDocsAttempt→readers→ACK→leader gate→broker→driver→native executor→terminal | Existing opaque trusted parent остаётся runtime prerequisite; valid route не может быть permanent stub |
| D5-4 secret-bearing intent | I2 `native.py:642–649`, CPP R3 | §4 ephemeral startup/ACK и explicit redacted bootstrap/phase intents; digest сырого random bytes | Нет tokens/nonce/capsule/env в persisted raw/log/receipt; no historical rewrites |
| D5-5 большие full captures/finish | I2 `cli.ts:90–99`, CPP R4 | §5 chunks decoded≤32768B/encoded≤49152B, ticket/offset/SHA; total≤24MiB; §6 finish≤128KiB summary/ref/SHA | Full pure Capture preserved/hydrated with cap; native originals независимы; no arbitrary path read |
| D5-6 full binding ACK | I2 `native.py:656–657` partial ACK | §3 setup ACK all source/input/runtime/request/deadline/peer fields; accepted compare capsule digest/scope/nonce digest | No self-signed authority; no READY transfer from stale preflight |
| D5-7 durable finalization | CPP R2/R6, capture partial write/timeout cleanup | §3/6 guarded lifecycle с первого fork, parent fallback, prewrite reserve, terminal-empty+reap | При dual storage failure typed unknown; no invented retained_ref/pass |
| D5-8 inherited base env | CPP R8, Step.clearEnv=false vs native env map | §3 parent pre-routing inherited snapshot; dedicated maps exact D2 | Snapshot не durable; отсутствующий snapshot blocks, no silent empty env/ambient fallback |
| D5-9 finite implementation matrix | I2 CPP R1–R9 | §7 exact nine-row source correction/control map для одного I2B | Controls не запускаются D5/I2B; new fixture hashes/counts separately frozen |

Preserved: exact12/three tools, pure9exports/Capture, D2 argv/maps, sourceGraph flat graph/Git sections/trimEnd/NUL, native16, Git512/8MiB/60s, fixed13 seed, failure retention, historic227/current230 distinction, compiler/DEV/GREEN/native/final CI/science gates. Не менялись sources, fixtures, checkpoints, server/platform/runtime и historical artifacts.

Уточнения D4: capsule codec и bounded chunk/finish projection требуют high R; focused D4 SOURCE PASS не объявляется приёмкой D5 или I2B. Runtime resource metrics/actual parent integration не получены. Root parent steer разрешил bounded hydration как design choice; новых native attempts/grants этим не создано.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Narrow missing contract конкретизирован | D5 §2–6 | Требует independent high R | изменить |
| Девять I2 implementation findings закрыты кодом | Product writes0 | Только карта будущей коррекции | данных недостаточно |
| Scientific/public contract расширен | Preserved list + D5 §1 | Private transport изменён явно | сохранить |

STOP; только D5.md + delta-ledger.md + identity.json.
