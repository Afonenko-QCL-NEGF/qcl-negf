# RV03 · Независимый source review

Первичные источники/12-edge denominator прочитаны и выводы сохранены в `RV03-blind.md` до candidate. Candidate SHA256 `656bc552fc15751bca1e059a7a029ca993ab2e44ee5bc88f2022c1df5e893c31`. Four views: dependency6/context2/job-data2/deployment-storage2. No runtime/build/import/tests. Commits/full component composition — source-receipt; frozen baseline/target hashes проверены RV16.

**Verdict:** owner/view выводы обоснованы в selected scope; поправить один существенный consumer locator и два небольших source locator gaps. Runtime и полный cycle graph честно unknown. Ни DAG, ни defaults не выданы за deployment или научную приёмку.

| Severity / locator | Finding | Проверяемая коррекция |
|---|---|---|
| P2 · `RV03.md` Job/data/release, AiiDA→Runner row | Producer `calculation.py:100` запускает `run-plan`, но consumer приведён `execute_configured_run` из configured_execution.jl, не фактический receiver этого CLI edge. Оговорка «full trace partial» не заменяет уже доступный прямой consumer | Указать Runner `src/cli.jl::_cli_heavy`, run-plan branch 74–85 → `execute_scientific_plan_staged(load_scientific_plan(...),...)`; configured entry сохранить отдельным boundary, без приписывания CLI вызова |
| P3 · `RV03.md` Deployment/storage, application closure row | Symbol `mkPythonEnvironment` находится в Platform `flake.nix:25`, импортирует `nix/application.nix`; locator `nix/application.nix::mkPythonEnvironment` сам по себе не воспроизводим | Два locators: `flake.nix::lib.mkPythonEnvironment` + `nix/application.nix` expression |
| P3 · `RV03.md` Context Browser→Portal row | Consumer API и payload hook названы, но Browser producer source отсутствует; hook — package producer, не сторона Browser request | Добавить Portal `frontend/src/api.ts:87` fetch `/api/v1${path}`; `api.py` routes+conditional StaticFiles receiver |

Independently checked: Runner core_api explicit imports и Core exports; Results model/native imports Contracts constants, Contract definitions; AiiDA validation imports Contracts validator; Portal actor imports AiiDA service и forwards handles; Portal exports local Results import; Root sourceGraph validates Gitlinks versus child HEAD; AiiDA frozen plan/attempt→Runner CLI; Runner commit/native metadata→retrieved/Results reader; Platform environment/services и NFS/controller/scratch ownership. Source code supports direction/state, но не actual installed graph. `save_runtime_checkpoint!`, `commit_point_artifacts`, `multipart.receive` symbols существуют. Browser/deployment correction нужна для воспроизводимой two-side chain, не для смены архитектуры.

M06 12 declared rows имеют locators, однако row-count не 12 independently closed contracts: CLI receiver correction явно нужен. M12 full SCC/fanout remains `not_measured`. Researcher/operator/developer actions присутствуют. Target owner matrix совместима с baseline, однако complete target local-management implementation не проверена; candidate это не объявляет pass. Sections <8 KiB. Alternatives сохраняют scientific/format/resource/presentation owners; новый service не объявлен необходимым по одному DAG.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Four views и selected owners различимы | 12 primary source edges в blind file | Full dynamic/process graph не измерен | сохранить |
| AiiDA плановый запуск прослежен к Runner | calculation.py run-plan; cli.jl actual branch | Candidate consumer был другой entrypoint | изменить |
| Source closure не deployed compliance | Platform source modules и frozen target | Нет boot/import/native receipts | данных недостаточно |
| Storage/data lifecycle нельзя вывести из metadata DAG | NFS/scratch/controller-state source + receipt-based artifacts | Restore/runtime неизвестны | сохранить |

## Round1 scoped recheck

Candidate SHA256 `d9aaf1c7437b3ad060fcc25c65a558626f0559c892893825964dbe1488cd0685`: CLI producer→_cli_heavy→execute_scientific_plan_staged; flake.nix::lib.mkPythonEnvironment→nix/application.nix; Browser frontend/src/api.ts::api→HTTP routes добавлены и совпадают с первичными source locators. Три findings закрыты. Staged→Core полный trace честно partial; граф не расширялся, runtime не проверялся.

## Round2 scoped metric recheck

Candidate SHA256 `22f15550e7126495340d0ec179c86ffe952fbbb9bac92d34fbd580e257d8503f`: source-locator coverage explicitly administrative; canonical M06 source→build→import/runtime closure `not_measured`. Counts do not confer closure pass. Changed metric sentence only checked; source graph not repeated. Prior findings and original reviewed hashes retained.
