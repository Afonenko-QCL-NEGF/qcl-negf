# SCI08-R1 production I1

Статус: **IMPLEMENTED_SOURCE_REVIEW_PENDING**, не ENG_READY/GREEN/S1/SCI_READY.
Sole writer изменил только пять production src файлов в owning Runner worktree;
commit, Root/CP, fixtures/schema/provenance/tools не менялись. Runner HEAD остаётся
fefaa27f194bfddf85dd51a0e255beef2218c06d; root наблюдён c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0.
Git submodule metadata root снята; Gitlinks остаются источником состава проекта.

Применены accepted D1+D2+D3 и engineering plan v3. Actual RED2 receipt SHA
1ae6c4cd1ac24f82dbc43558f9f145654468347e4a9b91ef81563ff2ed59714c
сохраняет behavioral RED (healthy forecast passed, Bool assertion failed).
RED1 bootstrap failure остаётся consumed, не переименован в RED. C08 exhausted8/8.

## Изменения и source API mapping

| Contract | Owning API / source |
| --- | --- |
| Exact checked forecast | point_artifacts::_checkpoint_storage_forecast_bytes; unchanged heuristic C+4*(128*NE*Nk*Nb²+ΣK+F) |
| Actual writer preflight | _checkpoint_storage_preflight → commit_point_artifacts before generation/stage/HDF5 |
| Checked budget/free | _storage_budget_used, _storage_free_permit, readers injected only via private kwargs; invalid scalar refuses before reader |
| Strict raw classification | linux_resources::_strict_resource_integer finite/unlimited/unknown/malformed/out_of_range; legacy parser unchanged |
| Strict ancestry and CPU | _strict_cgroup_ancestors rejects unknown/traversal/missing ancestor; _strict_cpuset_count merges intervals without expansion; exact fld quota workers |
| Strict probe | probe_hardware(resource_policy=:campaign_strict) requires known explicit physical/available inputs; _standalone_probe_hardware preserves old body and keyword types |
| Strict phase | _native_phase_request(...;resource_policy) → _native_phase_memory_permit! checks known directory/burst/bounds/current, width and required-byte overflow |
| Entry remains closed | _scientific_resource_preflight called first by execute_scientific_plan, unconditional strict needs_guard/needs_admission |
| Envelope propagation | entry captured envelope passed explicitly to strategy and reservation; two-arg reservation compatibility retains optional default only for omitted standalone calls |
| D3 fixture seam | _record_native_phase!(...;proc_root) → _native_phase_journal(...;proc_root); default /proc, directory-only get!, lazy strip/read/catch unchanged |

Exact current source SHA256 and frozen fixture comparisons находятся в identity;
complete.patch содержит полный **production** I1 diff, не pre-existing fixture diff.
Все пять frozen fixture hashes совпали с reviewed engineering plan v3, 349 nominal
assertions/31 logical groups/5 includes неизменны. Это не runtime pass count.
Actual O1/O2, envelope/policy и selected fake reader paths описаны отдельно в caller-traces.

## Проверки и границы

Выполнены только чтение source/text/Git metadata, source edits и SHA256 comparisons.
Runtime/parser/compiler/format/lint/tests/Julia/Pkg/network/native/build calls=0.
`git diff --check` намеренно не запускался в рамках запрета format/lint; source diff
просмотрен вручную. Нет установки пакетов, solver/SCBA/Poisson, benchmark или native
campaign. Физика, configschema, модель, thresholds, Nb/grid/window/channels не менялись.
Использованы TDD source workflow и inherited finite plan: failing behavioral receipt
прочитан; GREEN зарезервирован только Root после независимого high CPP.

Remaining gaps:
1. Независимый high CPP этого production candidate ещё отсутствует. Source syntax,
   package loading,349 runtime assertions и actual resource usage не проверены.
2. Root GREEN1 READY и однократный untouched GREEN ещё не выполнены; нет rerun grant.
3. R2/R3/P1/P2/A1/C1 technical bindings, all-write storage enforcement, leases,
   freshness/identity/native admission отсутствуют. Campaign entry остаётся closed.
4. Forecast — прежняя эвристика, не доказанный physical/HDF5 upper bound; вне адресных
   chains остаётся unchecked arithmetic (scientific recovery closure+reserve,
   minimum-output+reserve, generation/attempt counters и другие owners).
5. Strict probe намеренно не подменяет отсутствующие explicit physical/available
   inputs host fallback. Real production strict resource authority/admission ещё
   не интегрирована. CPU ratio field observational Float64; worker bound exact fld.
6. Source fake-only trace не OS sandbox/syscall proof. Journal defaults не являются
   admission credentials. Physical I/O/RSS не измерены; logical reading estimate
   приблизительный, поэтому ресурсный cap не объявляется измеренно доказанным.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Checked scalar/source call chains реализованы | 5-file production diff + identity + actual O1/O2 traces | High CPP/runtime pending | изменить |
| Frozen five fixtures сохранены | SHA256 exact equality with plan v3 |349 nominal, not runtime | сохранить |
| Strict campaign не допускает execution | First entry seam + unconditional pending-bindings refusal | Нет full S1 guard | сохранить |
| GREEN/ENG_READY/full scientific acceptance достигнуты | Исполнение в I1 отсутствует | Root CPP/READY/GREEN required | данных недостаточно |

STOP: source I1 передан отдельному independent high review. Никакого GREEN вызова.
