# DEV24 — final independent receipt review

Вердикт: **PASS для адресного public synthetic G1 scope**. Новый actualAPI auth-counter oracle прошёл 14 cases; два existing export-controls дали ещё 11 cases. GREEN-2 подтверждает ранее одобренный source diff и закрывает узкий gap отсутствовавших explicit zero facade counters. Блокирующих замечаний к этому пакету не найдено. Это не full release/security/scientific acceptance.

Рецензент сначала прочитал actual cache/selector fixtures и owning source, затем GREEN-2 receipt/raw и исторический GREEN-1. Новые imports, tests/reruns, установки, Git mutations, server/solver actions не выполнялись. Единственный новый файл рецензента — этот отчёт. Наблюдаются два выполненных DEV24 packets, то есть 2/2 разрешённых calls потреблены; автоматического следующего запуска нет.

## Identity и целостность

Root workspace `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, фактический HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`. Portal HEAD `d28d076c83611278153752d94cc3729d91b32667`, branch `codex/review-closure-rejection-controls`, status только ` M tests/test_api.py`.

| Артефакт | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-DEV24-GREEN-2/receipt.json` | `2bc6444cc375c543606bba248f897503e41a51e5e09934bf73f229768b70bf52` |
| `/tmp/qcl-DEV24-GREEN-2/original.log` | `acf37d54d2d43d454b84392b412e86651d972c9cee58e8d3bce7f35b4149bead` |
| `/tmp/qcl-dev24-auth-code-review.md` | `243fb8ecf2245e0c8d77463a16465777d3f0d74fd1e6daa6f9b3feea83b7e77f` |
| Portal `tests/test_api.py` current/receipt | `88d91cb17904398618bc79b92cbae956c91603075ad2cc1cbd5b27893d810c8d` |
| Portal `tests/test_exports.py` HEAD/current/receipt | `d5bc95bd27346030cab6f60681fd21580b8ea2d70abb3757562e4bd1ed40ac8a` |
| Portal `src/qcl_negf_api/api.py` | `d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63` |
| Portal `src/qcl_negf_api/service.py` | `b4dd4da7da85bdfca7993da3928dcf720f78e4f3ca8e70e27a2df36b79d01ef3` |
| `/tmp/qcl-DEV24-GREEN-1/receipt.json` | `1a804be7a8d04b53cf2c418dedf5640e3ccd61b52851da4b25dcd95db0448b3e` |
| `/tmp/qcl-DEV24-GREEN-1/original.log` | `ccd9d26d5af2b916b82f6f94841bc4fd578b4c40ed5a7f96ad78bee59c969429` |
| `/tmp/qcl-dev24-first-review.md` | `0a1255c3870792a830887e363b9ea514756f24376af593c6f7c0886cd94a2eea` |

GREEN-2 receipt называет ровно три полных function addresses: `tests/test_api.py::test_rejected_bearer_never_reaches_service_facade`, `tests/test_exports.py::test_export_pins_inventory_plan_payload_status_and_cache` и `tests/test_exports.py::test_export_invalid_selectors_precede_preparation` под `components/qcl-negf-portal/`. Все три fixture hashes совпали с actual files; общий hash test_api совпал с CP-CODE. Production auth/service hashes также не изменились. `git diff --check` снова exit 0. Статическое CP-CODE доказательство сохранности baseline остаётся применимо: current без единственного блока 98–149 имеет SHA256 `55efd325a3a3c97a8799a6eec8341c6eeaf78e8b0c18a3ec740b23ed1c9ebb9e`, одинаковый с old HEAD и GREEN-1 test_api; повторная hash-проверка stripped file совпала.

## Runtime witness и знаменатель

GREEN-2 raw: `25 passed in 3.58s`, 25 точек и `[100%]`, 99 bytes. Receipt: exit 0, 4.853 s wall; sampled peak process-tree RSS 169848832 bytes; 65 completed owned-TMP samples, sampled owned TMP peak 0 bytes; `raw_capture_complete=true`, capture error/guard error/stop reason — null, envelope overrun — false. Размер raw независимо подтверждён `wc -c` (99). Receipt envelope: 90 s, CPU affinity count 1, sampled RSS 1 GiB, temporary 16 MiB, output 2 MiB; заявленная подготовленная locked `.venv` Python 3.14.7 с owning editable imports. Рецензент проверяет сохранённое свидетельство, не исполняет эти imports повторно.

| Пакет/case group | Число pytest cases | Проверенное свойство |
| --- | ---: | --- |
| GREEN-2 auth-counter function | 14 = 7 routes × 2 credentials | Каждый missing/wrong bearer request возвращает 401 при `facade_calls == []`; следующий healthy bearer request достигает exact ordered boundary и ожидаемого status |
| GREEN-2 pinned export/cache function | 2 = switch-after-resolve False/True | Один resolved attempt удерживает inventory, exact frozen plan, payload, recorded status; exact identity reuse даёт тот же export ID, другой attempt — новый ID; старые status/bytes сохраняются |
| GREEN-2 invalid-selector function | 9 | Неверные типы/диапазоны/UUID, конфликт attempt/CalcJob и отсутствующие children отказывают с ожидаемым exception до repository-open events и создания entries |
| GREEN-1, исторический packet | 50 | 14 selected function addresses из original command, status/rejection/locator/metadata/contract controls по first-review scope |

Итого **75 case executions в двух packets**; это не 75 независимых свойств или full suite. Embedded healthy HTTP control внутри каждой из 14 auth cells входит в тот же pytest case и отдельно в итог не прибавляется. GREEN-2 сам содержит 3 selected function addresses и 25 cases; GREEN-1 — 14 addresses и 50 cases.

## Проверка оракулов по source

Auth (`tests/test_api.py:98–147`): counter append до delegate, все callable synthetic facade members обёрнуты, assertion exact-empty сразу после отрицательного request, reset отсутствует. Actual `create_app` и HTTP handlers используются без auth monkeypatch. Healthy expected statuses: list 200, submit 202, inventory 200, GET artifact 200, HEAD artifact 200, authorize 200, kill 200. Exact sequences: `[list_runs]`, `[submit_plan]`, `[list_artifacts]`, `[get_artifact_metadata, open_artifact]`, `[get_artifact_metadata]`, `[get_artifact_metadata]`, `[kill_run]`. Каждое релевантное имя требуется ровно один раз, GET metadata идёт до opener. Actual auth source `api.py:187–200`, download auth `213–228`, protected handlers `341–375`, `426–432`, `492–504`, GET/HEAD auth-before-metadata `516–526` согласуется с oracle. Injection не создаёт real AiidaService (`144–150`). Эта проверка измеряет request→public facade boundary; реальный actor/profile/jobs не участвовал.

Cache (`tests/test_exports.py:298–418`): actual `ExportStore` импортирован; fixture вызывает actual `aiida_qcl_negf.service` operations через wrappers, а ORM node/children/repositories синтетические. Wrappers записывают operation и kwargs до delegate (`360–364`). Export writer подменён synthetic publisher; это не проверка real compression/архивного scientific content. Оба child имеют одинаковую semantic plan JSON, различающиеся exact bytes и payload/status. Assertions закрепляют attempt 2/C2/failed, exact payload/files/plan source/plan bytes, единственный initial selection call, exact pinned selectors всех downstream calls, events только C2. Затем exact cache reuse и переключение на attempt 1 подтверждаются новым ID и сохранностью прежнего status. `exports.py:132–178` разрешает/валидирует binding+inventory до cache lookup `187–195`; `service.py:202–219` берёт recorded status выбранного child.

Invalid selectors (`tests/test_exports.py:448–463`): девять literal cases и ожидаемые exception types, затем немедленно `source.events == [] and store._entries == {}`. Это runtime rejection до payload/preparation в изначально пустом store. Отказ invalid input до доступа к уже тёплому cache отдельно не параметризован; отсутствие обхода валидатора через cache поддержано owning source order (selection/validation до lookup), а healthy warmed-cache behavior — отдельными двумя cases. Такой совмещённый source/runtime вывод не следует выдавать за отдельный измеренный warmed-cache negative case.

## Исторический GREEN-1 и предел переноса

GREEN-1 raw подтверждает `50 passed in 1.13s`; receipt wall 4.992 s, exit 0, RSS 167157760 bytes sampled, 67 TMP samples, raw 99 bytes complete/no guards/errors/overrun. Его root `c43935567df010d43cab9bcd8d851a9ed976a8d7` и component identities из first-review не переписаны в текущие. Через `git ls-tree` подтверждены historical Portal `ff1e25f22eed2cb6f48ba11c1ba0a52495e7f363`, AiiDA `312ed8a6363103d05a971d14ac9cbcca1c782358`, Contracts `26cacbe1688fee0af300d0949fc6b94e55a29f4a`, Results `17574ca4c5495f74d86ed9bef51c60dea8265062`.

Сравнение historical→current Portal/AiiDA/Contracts/Results commit ranges показывает только CONTRIBUTING.md в каждом компоненте; runtime source не менялся между этими committed refs. Current AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`, Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`, Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Original API test definitions сохранены byte-exact после additive auth change. Current AiiDA test SHA256 `ae339e892c9058afc55926203e8ddc4f1daa1106e34f7080f88bee54f814a8c9`, Contracts test SHA256 `0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7` совпали с GREEN-1. Поэтому исторические named controls остаются релевантным свидетельством, но не объявляются повторно исполненными на root HEAD 965ebed; новое runtime свидетельство относится только к трём GREEN-2 addresses.

Ресурсные metrics — sampled RSS/logical owned TMPDIR st_size, не hard cgroup/disk quota и не доказательство transient peaks. Zero sampled TMP не означает нулевой I/O/physical storage или отсутствие explicit temporary paths вне TMPDIR. Сопоставление receipts/hashes не является независимым повторением выполнения.

Native TLS/private credentials/ownership, audit-log sanitization/access, real AiiDA actor/profile/broker/jobs, полный HTTP/security corpus, full CI/release, numerical convergence/physics/discretization/experiment не проверялись. Вывод G1 ограничен public synthetic software boundaries и названными controls; отсутствующие измерения не превращены в pass.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Новый auth gap закрыт на selected seven-route boundary | Source CPP exact hash + GREEN-2 receipt/raw 14 cells с empty negative/exact healthy calls | Synthetic facade; real actor не измерен | сохранить |
| Exact attempt/cache controls прошли | GREEN-2 2 pinned + 9 invalid cases; actual ExportStore/producer source locators | Synthetic ORM/repositories/export publisher; warmed-cache negatives не отдельный runtime case | сохранить |
| GREEN-1 50 cases остаются историческим evidence | Original receipt/raw/hashes, test byte equality, doc-only committed source differences | Не rerun на current root | сохранить |
| Лимит DEV24 targeted calls исчерпан | Два законченных packets, 2/2 calls | Новый run требует нового порученного бюджета | сохранить |
| Full native/security/scientific acceptance достигнута | Таких evidence нет | За пределами этого gate | данных недостаточно |

STOP: final receipt review завершён; rerun или дальнейших изменений нет.
