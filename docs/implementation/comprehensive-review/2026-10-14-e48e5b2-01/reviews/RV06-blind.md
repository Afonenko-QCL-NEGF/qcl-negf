# RV06 blind-first primary answer

Candidate/fixes не читались. S=e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1; Platform P=4ce214e29b72276157b10a9267e2f30fef4ac66f, clean status. Denominator frozen L1–L7; native cells not_measured. Только source reading, без исполнения.

L1: application_release::lifecycle_owner/deliver_cli и worker_lifecycle::shutdown_step/startup используют controller delivery.lock; shutdown имеет также per-node flock и освобождает общий lock на Runner pause/verify-stop. Отдельный CLI activation использует activation.lock, не delivery.lock. Поэтому отсутствие любого второго публичного mutation writer не следует из shared orchestrator lock: activation child/direct entrypoint требует отдельного рассмотрения, включая смерть parent при живом child. Local flock не distributed lease.

L2: activate удаляет ready record до изменения application/solver profiles, пишет allowlist/service.env, ready=false, запускает службы, health/self-check, затем ready=true. guard требует совпадение release, ready и open admission. Это source crash barriers; actual crash cuts между publications не измерены.

L3: unresolved_deliveries/lifecycle_guard сохраняют запрет retry при pending mutation, admission intent, requires_reconciliation или cluster-update marker. _deliver_pool_owned закрывает gate до quiesce и opens только после verified node envelopes/rechecked authority. close_after_failure оставляет open=None при отказе закрытия; unknown не positive proof.

L4: _shutdown_owned_poll сохраняет capture intent до drain; объединяет pending scope с active jobs. Удаление job допускается только после pause+verify-stop и отсутствия в final_active. Исчезновение squeue само по себе не proof. Orphan capture не становится safe по пустому retry.

L5: startup требует same enrollment/new boot для normal shutdown, complete scope, authorized event; drain/activation/check предшествуют RESUME. Независимый startup-admission-intent публикуется до RESUME и удаляется последним после resumed publication. Ошибки сохраняют reconciliation; actual power/client crash unmeasured.

L6: direct activation требует selected closed admission, returning-worker exception ограничен worker. Initial preparation — отдельный protocol, не старый safe-stop proof. Stale/missing/foreign gate не обеспечивает admission.

L7: bootstrap_build::main сохраняет exclusive original receipt; evaluation_only отличается от strict nginx pass. build_admission::admit требует свежий snapshot/idle queue/host reservations, допускает production sharing CPU лишь отдельно от RAM contract. Admission не resource reservation и не four-role boot acceptance.

Прочитанные tests содержат fake run/authority fixtures и один forked OWN fake client shutdown test; наличие tests не M04 pass. M09–11 native/backends/live drift остаются not_measured. Наиболее существенный следующий вопрос: authority/locking всех activation entrypoints и surviving remote child; никакого native отрицательного свидетельства здесь нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Unknown не подразумевает admission | P application_release::_deliver_pool_owned/close_after_failure/lifecycle_guard | Runtime не проверен | сохранить |
| Исчезнувший job сохраняет proof obligation | P worker_lifecycle::_shutdown_owned_poll | Runner receipts не исполнялись | сохранить |
| Общий controller flock не доказывает единственного writer глобально | P main activation.lock vs lifecycle_owner delivery.lock | Native parent/child unknown | дополнительно измерить |
| Все seven properties адресованы source reading | L1–L7 выше | Не seven passing executions | сохранить |
