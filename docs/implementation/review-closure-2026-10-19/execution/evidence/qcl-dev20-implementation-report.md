# DEV20 implementation handoff для GREEN1

Статус: **реализация написана, GREEN not_measured автором**. Root сообщил semantic RED-1: actual hook stale input и changed output cases, 2 failed / 0 errors, `RuntimeError not raised`, 0.745 s. Это release для production реализации; native wheel/browser/CI/scientific gates отдельно.

## Frozen binding

Portal baseline поручения `b9a876aa22d84dc13435bf970728b033d1345ba8`; owning DEV19 v2 SHA `dbf2d4808a84cb97d1a656532aaf4c7271598195076ce084ca62d88a36e68cc9`; accepted review SHA `4f0aec0141c92ddd2fbd407fc7685ef77e348f305bda98da8f563465a20780a9`.

| Артефакт | SHA-256 |
| --- | --- |
| `hatch_build.py` | `d8393b11add6af03825f587181d32ced35bdc50d9cefd9552ad56b12f47c747f` |
| `frontend/tools/asset-receipt.mjs` | `e471dda9e68176d965b6cf560f0ae578b7f397de9083fa118caef1f5d17ae8e3` |
| `frontend/package.json` | `dce393b2af93a6f6aa7c3189a65c0ae6b11e9245566bebcbf2a262faecb6f46d` |
| `tests/test_build_assets.py` | `c229bc16514930887abe5bc69102e8fa1156618e9bbdd6dd91c6e2320e6f1240` |
| `/tmp/qcl-dev20-implementation.patch` | `6c6f5e8fecfb009c67d6963ef5349621d347251f6640c1c78c072a2e68007c3d` |

Full source patch содержит ровно четыре вышеуказанных Portal paths; тест сохранён byte-exact от RED freeze. README, owning design, `.gitignore`, Vite config и `test_ci_environment.py` не менялись: existing ignored generated roots и `emptyOutDir:true` уже соответствуют D. Package JSON изменяет только значение `scripts.build`, dependencies/lock не меняет.

## Реализация и причины

`hatch_build.py::verify_frontend_assets` — отдельный stdlib Python reader: canonical receipt/schema/key order/duplicate/nonfinite rejection, strict row types/digests/path order, complete recursive inventory, exact Nix config-only bytes transform, TS/Vite lock compatibility и byte-for-byte source/output comparison. Hook вызывает его только для noneditable wheel; никаких Node/package target imports/network/rebuild. Existence-only fallback удалён. Failure messages имеют публичный reason без source/env contents. Recursive Nix basename/cleanSourceFilter не воспроизводится: missing C2 row отказывает по inputs.

`frontend/tools/asset-receipt.mjs::buildFrontend/verifyFrontend` экспортирует только документированный imported runner seam; direct CLI roots выводятся из tool location и accepts только build/verify. Local subprocesses получают current Node executable, local compiler paths, production environment; npm version query не устанавливает dependencies. Source `.env*`, inherited VITE_*/NODE_OPTIONS и unsafe filesystem отказывают.

До runner проверяются layout markers, literal selected output, lstat segments/device и весь существующий selected tree, включая symlinks/special/.git. Затем wrapper удаляет и пересоздаёт только selected root пустым. Old receipt доверие не требуется; foreign/effective outDir не очищается. После tsc/Vite снимаются source/toolchain и новый payload, source сверяется ещё перед publish. Missing/new output отказ не усыновляет старые assets.

Receipt публикуется last: random exclusive-created regular temp, flush/fsync, atomic rename и directory fsync где поддержан; postpublish ordinary verify. Ошибка пытается убрать только собственный temporary/final stamp через повторную safety check, не удаляя новый payload; cleanup diagnostic не заменяет исходную ошибку. Temporary name становится owned только после успешного exclusive open. Build errors сохраняют command exit code для CLI; auto retry нет.

## Проверки и ограничения

Автор прочитал applicable AGENTS/architecture/development DEV19/20, contributor rules, D v2 и accepted review. Runtime target code/imports/tests/Node/npm/tsc/Vite не исполнял; installs/builds/Git/server/solver не выполнял. Source проверен последовательно текстовым чтением, SHA-256 и standalone diff; независимый reviewer здесь не привлекался, поэтому независимость CP-CODE проверки ниже отдельного review.

Root executor владеет GREEN1 full-file execution с selected prepared Node24 PATH и общим исходным finite L-PY budget. Изменение тестов для сокрытия отрицательных результатов не делалось. Если GREEN1 выявит failure, сохраняется original evidence и дальнейший repair scope согласуется с root; самостоятельного run/fix loop нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Baseline existence-only guard не различает stale input/output | Root semantic RED-1: 2 failed, 0 errors | Raw execution receipt хранит root | изменить |
| Source связывает recipe/input/output и fail-closed wheel gate | Frozen Python/Node implementation и неизменённые independent tests | GREEN1 автором не измерен | дополнительно измерить |
| R1 reset не зависит от предыдущей receipt | Known-root safety + clean/recreate до runner; negative matrix | Trusted serialized filesystem, не защита от concurrent replacement | дополнительно измерить |
| C2 missing source row не скрывается filter imitation | Full hook inventory + exact config transform | Совместимость будущих Nix trees не обещана | сохранить |
| Native wheel/browser/full CI/scientific acceptance получена | Таких запусков нет | Эти gates not_measured | данных недостаточно |

STOP: source frozen; ожидать root GREEN1/review, не исполнять tests и не продолжать autonomous corrections.
