# RV05-1 — bounded actor lifecycle

READY discovery/design; implementation needs operational contract, not authorized by review.
Trigger: Portal actor _call/open/read/close waits have no deadline; blocked owner prevents cleanup.
Owner Portal with AiiDA execution semantics; exact inputs Portal10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb,
AiiDA69aa1309c8465a838e4778b9dff464a306229f01. Permitted future paths service.py/api.py/exports.py,
selected actor/disconnect tests and service docs; no numerical code.
Invariant: one profile/thread/loop owner, handles close exactly once, no false successful close,
no automatic duplicate submit or science-pass inference. Light theme unchanged.
Minimal design: deadlines per operation/close; outcome-unknown response and operator reconciliation;
compare cooperative bounded backend vs process isolation only if required by interface.
Independent oracle/negative: Event-gated fake operation, close/disconnect under explicit clock cap,
owner event order, guaranteed Event release finally; finite operation positive control.
Checks proposed not executed: selected actor+disconnect fixture, 1attempt, 1CPU/512MiB,
2min wall, <=1MiB logs, <=8MiB tmp; no real AiiDA profile/server, no installs. This is no grant.
Stop: cap, owner lifecycle violation, unknown irreversible submit outcome; don't retry until green.
Dependencies: operation timeout/reconciliation contract; native backend behavior separate.
Migration/docs: document error/unknown outcomes and reconnect/read-before-submit procedure.
Close ticket when design has exact invariant/observable fixture and future authorized targeted
check proves both negative and healthy paths; native responsiveness remains separate measured gate.
