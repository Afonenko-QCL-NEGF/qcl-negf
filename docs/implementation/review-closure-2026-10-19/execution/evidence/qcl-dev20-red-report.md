# DEV20 tests-only RED handoff

Статус: **tests authored; runtime RED not_measured автором**. Production implementation не начиналась. Semantic RED должен выполнить root executor; до отдельного semantic RED release работу остановить.

## Binding

Выбранный root: named managed worktree `review-closure-exec/qcl-negf`.
Portal baseline из поручения: `b9a876aa22d84dc13435bf970728b033d1345ba8`.
Root владеет Git evidence/checkpoints; автор Git commands/mutations не выполнял.

| Артефакт | SHA-256 |
| --- | --- |
| `docs/package-identity.md` | `dbf2d4808a84cb97d1a656532aaf4c7271598195076ce084ca62d88a36e68cc9` |
| `/tmp/qcl-dev19-design-v2-review.md` | `4f0aec0141c92ddd2fbd407fc7685ef77e348f305bda98da8f563465a20780a9` |
| `tests/test_build_assets.py` | `c229bc16514930887abe5bc69102e8fa1156618e9bbdd6dd91c6e2320e6f1240` |
| `/tmp/qcl-dev20-red.patch` | `df4c354ef2bc18137ab59515f4cba894f9a777219bd8a0ddc479160fef5e4348` |

Изменён только разрешённый `Portal/tests/test_build_assets.py`. Frozen standalone add-file patch: `/tmp/qcl-dev20-red.patch`. README/docs/production source/test_ci_environment.py не изменялись автором.

## Различающие проверки

Python `WheelReceiptTests` вызывает actual `CustomBuildHook.initialize` через установленный Hatchling constructor (interface source прочитан по selected `.venv/lib/python3.14/site-packages/hatchling/builders/hooks/plugin/interface.py`; execution/import не выполнен). Это не stub и не доказательство native wheel build. Fixture receipt вычисляется независимо от production code: все inventories и canonical bytes создаёт тестовая stdlib фабрика в tiny public temp tree.

Первый semantic RED packet: `WheelReceiptTests::test_wheel_rejects_stale_frontend_inputs` и `WheelReceiptTests::test_wheel_rejects_changed_asset_bytes`. В baseline существующий guard принимает old index/JS: ожидаемый RED — `RuntimeError not raised`, а не ImportError/отсутствующий verify symbol. Fresh/editable positive controls различают явное отсутствие reject от сломанного import.

Python cases: fresh; changed TS/lock/output bytes; missing stamp/asset; extra hidden output; input rename; hidden/tests/public/nested-dist input rows; malformed/incomplete/duplicate/noncanonical/bool-byte receipt; altered digest; lock/toolchain mismatch; editable/sdist без release identity; unsafe output symlink с foreign sentinel. C2 создаёт nix-dist receipt из patched source, возвращает exact original config для hook и требует `inputs` rejection при добавленном `src/dist/entry.ts`.

`GeneratorLifecycleTests` импортирует реальный скопированный generator и injects только документированный BuildRunner. Это запускает Node harness, но не actual npm/tsc/Vite: runner обслуживает version/command results, payload создаётся synthetic write. Каждый Node child имеет timeout 10 s; root обязан ограничить общий packet своим ресурсным бюджетом. Node отсутствует — explicit assertion, не skip/pass. Generator отсутствует — explicit assertion; это отдельный пока неразрешённый implementation gap, не substitute semantic RED.

R1 matrix для обоих modes: old valid/missing/corrupt stamp + old payload, zero-exit no selected output и output только в другом root, selected root empty перед первым compiler, outputs rejection, no new receipt, Python hook missing/payload refusal, byte-identical foreign sentinel. Positive runner пишет новые selected index/JS; receipt и independent hook связывают именно новые bytes. Nix hook получает отдельный Portal fixture с исходным config и переносом только selected dist. Отдельный unsafe symlink требует runner calls=0 и неизменный foreign sentinel. Compiler failures/source mutation не должны публиковать receipt.

## Ограничения и stop

Автор не запускал target imports, tests, Node, npm, compiler, Vite, native wheel, installs, lock refresh, Nix, workflows, server, solver или Git. Выполнены чтение и текстовое создание/правка единственного теста, SHA-256 и standalone diff. Никакой passing/RED runtime claim не сделан. Parent/root исполняет конечный бюджет; полнота browser/native/scientific acceptance здесь не заявлена.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Тесты различают stale assets от existence-only acceptance | Два direct actual-hook negative tests; independent fresh receipt | Runtime RED root ещё не измерен | дополнительно измерить |
| R1/C2 имеют public tiny discriminating fixtures | Generator lifecycle matrix и exact hook projection negative | Node/hook tests автором не запущены | дополнительно измерить |
| Production contract реализован | Production files автором не менялись | Реализации ещё нет | данных недостаточно |
| Дальнейшие source writes допустимы | Нужен semantic RED release от root | До release STOP | сохранить |
