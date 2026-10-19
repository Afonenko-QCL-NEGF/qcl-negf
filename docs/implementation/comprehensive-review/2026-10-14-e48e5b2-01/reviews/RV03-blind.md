# RV03 · Blind source views

Состав S и frozen overlay из source-receipt; candidate RV03 не читался. Denominator задан coordinator до чтения: dependency6, context2, job/data2, deployment/storage2 =12 edges. 4 views независимы от installed/archive overlay; source-only review, без imports/tests/server.

## Dependency 6

1. Runner→Core: Runner Project sources URL/tag и compat0.2.0; `src/core_api.jl` explicit import bindings; Core `src/QCLNEGF.jl` exports. Односторонняя numerical dependency, same Julia process, не отдельный service.
2. Results→Contracts: pyproject dependency; native.py imports ARTIFACT_SCHEMA_CONTRACTS/CONTRACT_SET/NATIVE_SCHEMA_VERSION из Contracts artifacts.py. Reader проверяет format/role, не решает transport.
3. AiiDA→Contracts: pyproject dependency; validation.py вызывает schema_validator/scientific_plan, producer counterparts Contracts __init__/messages. Formats не заменяют physics acceptance.
4. Portal→AiiDA: pyproject и service.AiidaService import_module aiida_qcl_negf.service; service operations/handles заданы AiiDA.
5. Portal→Results: pyproject dependency; exports.py calls export_snapshot, Results export.py receiver. HTTP/exports spool меняет state, не scientific arrays.
6. Root→Git-selected components: ops/git.ts::sourceGraph связывает ls-tree HEAD, .gitmodules, child HEAD/clean state, rejects nested/orphan/mismatch. Receiver component HEADs по receipt. Tag/package version не точный gitlink.

## Context 2

7. Browser→Portal: frontend/api.ts fetch `/api/v1`; api.py routes, final conditional StaticFiles mount root. Frontend wheel payload condition существенен: отсутствие static directory не вызывает mount.
8. Portal actor→AiiDA: one ThreadPoolExecutor(max_workers=1), dedicated event loop/load_profile; open/read/seek/exit delegated owner thread; AiiDA service.open_artifact opens selected retrieved repository. Отдельный repo не отдельный actor process.

## Job/data 2

9. AiiDA Calculation→Runner: calculation.py prepare_for_submission creates frozen plan.json and cmdline run-plan execution-id/attempt. Receiver Runner CLI→execute_scientific_plan_staged/configured execution; consumed state/plan identity обязательны. Configured API route не тот же entry argument as scientific plan.
10. Runner generation→AiiDA retrieved→Results: point_artifacts/file repository commits and result directories; CalcInfo retrieves result subtree; AiiDA parser/service select repository; Results native reader requires current native4.0 metadata/role/SCBA diagnostic closure. Metadata DAG не исключает file lifecycle/recovery cycles.

## Deployment/storage 2

11. Platform application closure→Portal/AiiDA services: nix/application loads uv workspace/source overlays/frontend; modules/application starts immutable profile qcl-negf-api и verdi daemon, initializes bounded mutable AIIDA_PATH. Derivation source properties не факт boot/deploy.
12. Mutable owners: storage.nix dedicated NFS /srv/qcl-negf/jobs; cluster.nix matching worker/control path plus /scratch; persistent-state binds AiiDA+PostgreSQL+Slurm controller state; application profile separate immutable closure. NFS exchange не backup, scratch не durable archive, OS replacement не data-disk destruction authorization.

## Source/target

Frozen docs/architecture.md implemented baseline и docs/system/architecture.md target owner matrix совместимы по scientific/data ownership. Target §§Локальная эксплуатация предполагает local serialized operational interface; actual workflow/source delivery следует отдельно не выдавать deployed compliance. Retention/restore/boot acceptance не установлены. Предложение сохранять компоненты, связывать model/config/format owner через exact source locators, проверять конкретные lifecycle contracts вместо общего DAG pass.
