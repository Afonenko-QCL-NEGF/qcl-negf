# RV07-1 — composite export exact attempt

READY discovery/design; implementation stage not granted.
Trigger: inventory all attempts + execution-only filter/default per-call child selection and cache.
Owner Portal with AiiDA selection interface; source Portal10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb,
AiiDA69aa1309c8465a838e4778b9dff464a306229f01. Paths Portal exports.py/api.py/export tests;
AiiDA service.py/selection tests/docs. Separate owning PRs, then published root gitlinks.
Invariant: plan, inventory, raw bytes, status, export cache identify one exact immutable child;
legacy raw/failed attempts preserved; ambiguity never science pass; no changing physical model.
Minimal design: resolve selected attempt once, exact UUID throughout inventory/plan/open/status/cache;
explicit selector user API vs published default behavior must be specified before code READY.
Independent oracle: two attempts equal lengths/different payloads, same/disjoint paths, selected2,
selection changes during export. Expected selected bytes2 only or explicit rejected ambiguity.
Positive one-attempt compatibility; negative foreign/mismatched UUID/bool attempt never payload.
Future check proposal 1attempt selected synthetic suite,1CPU/1GiB,5min wall,16MiB tmp/2MiB logs;
no live AiiDA/server/import install. Current permission only review/design, no fixture execution.
Stop: cap or absent operational API decision, not rerun-until-green. Migration/docs: declared
selection fallback and cache identity version. Closure: owner contract agreed, negative bytes
oracle and valid one-attempt route checked in future authorized source-bound environment.
