# CR02: durable normal worker shutdown intent

Обычный shutdown публикует protected persistent node intent до DRAIN и capture jobs. Intent
сохраняется после idle/safe ответа, выхода клиента и освобождения lock. Delivery проверяет все
active intents, включая workers вне выбранного pool. Per-node owner охватывает polling; общий
delivery owner удерживается только на коротких capture/finalize участках. Safe technical stop
требует одновременно verified Runner stop receipt и фактического allocation exit. Научный verdict,
job cancellation или выключение VM из этого ответа не следуют.

Startup использует CR03 enrollment/controller authority и bound identity. Требуются complete
captured scope, authorized privileged controller event, та же permanent worker identity, новый boot
и ready bound health. Unknown/orphan capture, неполный legacy intent и прежние CR04 uncertain
admission свидетельства блокируют admission; captured identities и CR04 bytes сохраняются. До RESUME
создаётся uniquely owned marker в existing admission-intent schema. Только этот marker удаляется
после durable resumed record; failed write/unlink требует reconciliation. Child и containing-parent
directory sync охватывают first creation и повтор existing entries после ошибки sync. Контракт
предполагает Linux directory fsync, protected local ancestors и отсутствие privileged concurrent
rename; это не универсальный capability-safe filesystem API.

Изменены десять owning Platform paths: два lifecycle/delivery modules, четыре fixture files, два
Windows callers и два user documents. Model/physics/tolerances, NixOS roles и scientific evaluators
не менялись; новый registry/ledger не добавлен. Actual Windows, scoped sudo/site mapping, protected
inventory, установленная Slurm convention и полная I14 приёмка остаются отдельными deployment gates.

Initial bounded checks сохранили genuine idle-inhibit RED: 21 lifecycle methods прошли; следующая
selection13 выявила три failed methods, которые затем прошли targeted correction. Это 34 distinct
methods, не свежий full suite. Independent whole-source review нашёл missing containing-parent
barrier; namespace RED3 → GREEN9 проверили narrow repair. Первый полный local check дал 22 Deno
passed, 297 Python passed / 5 skipped / 189 subtests / 1 failed: старый native-env fixture принимал
первый CR03 identity SSH за Nix и останавливался до Nix copy. Production не менялся; исправление
только fixture прошло targeted RED → GREEN и high review. Original failed logs сохранены отдельно.

Заключительный full local check на final frozen source: fmt/lint/type checks и 22 Deno tests passed;
Python 3.14.7 / system pytest 9.1.1 — 298 passed, 5 skipped, 189 subtests passed, 1 warning.
Supervisor: 8.602 s / 3427 bytes; отдельно назначен предел 120 s / 8 MiB без CPU/RAM cap.
Dependencies cached, проверка offline; это local environment, не locked release environment. Skip не
означает pass. Fork DeprecationWarning в owned client fixture сохранён. Fixture создаёт только свои
finite Python children/local temporary files; real SSH/Nix/server не выполнялись. NixOS
evaluation/build, Windows execution, production power-loss, CI, deploy, merge и scientific solver не
запускались; scientific attempts 0.

Final ten-path diff SHA256: `7f81fd8167bc7f46609af996cb55eb2d4a939344e179184f225a9e94022707a6`.
Final local check log SHA256: `981eb937fc27708af2ff2c3679e2f00f91d290713c05074551bfece7638d3d69`.
First failed full log SHA256: `3b55d825ad1395ab3aee342a12a5a19d149862984e5804dd07922426030febe3`.
Namespace and native-env focused high reviews не выявили remaining findings; whole review limits
сохранены. Known-secret/private-endpoint scan дополнен independent review; это bounded audit, не
гарантия обнаружения любого неизвестного секрета.

| Утверждение                                    | Свидетельство                                     | Ограничение                                 | Решение             |
| ---------------------------------------------- | ------------------------------------------------- | ------------------------------------------- | ------------------- |
| Safe response сохраняет admission inhibit      | Persistent v2 intent и client-exit fixture        | Local fake commands                         | изменить            |
| Unknown state не очищается по healthy/new boot | Orphan/binding/marker/fault fixtures              | Actual installation не проверена            | сохранить           |
| Namespace barriers предшествуют DRAIN/RESUME   | RED3 → GREEN9 и syscall traces/source order       | No physical power-loss measurement          | изменить            |
| Final local Platform checks проходят           | 22 Deno / 298 Python / 189 subtests; high reviews | 5 skips, local pytest9, engineering scope   | сохранить           |
| Научная/production приёмка установлена         | Таких свидетельств нет                            | Solver/Windows/actual server не запускались | данных недостаточно |
