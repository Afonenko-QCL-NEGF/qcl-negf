# Сравнение с реализацией и code review

Статус: статический аудит исходников 2026-10-09. Основание — root
`bce0aee088313fd28b2440f55350980e21ed46bd` и его gitlinks. Файлы компонентов
ниже неизменны относительно начала аудита. Сценарии отказа установлены
чтением кода; новые тесты, builds и VM/solver experiments не выполнялись.
Это целевой review критических переходов и контрактов, не заявление о
проверке каждой строки всех компонентов.

## Что сохранять

Новая архитектура не требует замены научного ядра или всего стека.
В [core solve](../../components/QCLNEGF.jl/src/numerics/reference/solver.jl)
есть независимый in-memory API и callbacks; Runner имеет локальный typed
API. [Final audit](../../components/QCLNEGF.jl/src/numerics/reference/final_audit.jl)
на строках 237–243 разделяет iterative/physical/candidate статусы и честно
оставляет discretization `not_measured`, `scientific_accepted=false`.
Это правильное ограничение одиночного solve, а не дефект, который следует
исправить присваиванием `true`.

Nix preflight четырёх ролей, native nginx check, подготовка closures перед
закрытием admission, CI isolation и independent results readers полезны.
Они уменьшают конкретные риски, но не доказывают runtime нового состава
исходников или научную точку S01.

## Матрица существующее → целевое

| Область | Существующее состояние | Изменение в новой архитектуре | Приоритет |
| --- | --- | --- | --- |
| Физика / API | Независимое ядро, проверки состояния, reference/optimized operators | Сохранить границу; доказать одну stationary point и достаточность её дискретизации | До расширения интерфейсов |
| Конфигурация | Ordered recursive merge, большой полностью merged input; значения условий в нескольких местах | Предметный запрос + protocol + единый resolver + явные физические изменения | Сначала для S01, затем остальные задачи |
| Исследования | Standalone plans и continuation внутри execution; общий evidence DAG отсутствует | Небольшая карточка и AiiDA зависимости; внешний агент создаёт варианты | После минимального научного цикла |
| Results | Независимый reader/export; HTTP читает retrieved AiiDA repository | Ежедневный NFS manifest/brief/full/slices, точная identity попытки | Исправить identity сразу, каталог поэтапно |
| Ресурсы | Estimates и безопасный envelope check; fixed VM RAM; per-job лимиты | Estimate-driven request, study CPU QOS, idle-bound builder/compute handoff; общий deadline отложен | Безопасный минимум до холодного bootstrap |
| Delivery | Локальный CLI есть; root release workflow вызывает его из GitHub Actions | Локальное управление готовым release; CI без infra credentials | До production эксплуатации |
| Workers | Статический inventory; BIOS/QCOW; Windows hooks запускают существующего guest | Общая роль + install profiles + trusted enrollment | Отдельная приёмка трёх backend |
| Документы | Architecture/runbook и датированные отчёты уже частично разделены | Один нормативный корпус, актуальные component contracts, исторические отчёты отдельно | Начать сейчас |

## Конкретные дефекты текущего кода

P1 — риск неверного результата/нарушения lifecycle; P2 — нарушение контракта
в определённом сценарии. Это инженерные приоритеты, не физические verdicts.

### CR01 — P1: размер и содержимое артефакта из разных attempts

**Локаторы:** portal `src/qcl_negf_api/api.py:338–345, 413–415`; AiiDA
`src/aiida_qcl_negf/service.py:80–102, 303–314`.
[Portal](../../components/qcl-negf-portal/src/qcl_negf_api/api.py),
[AiiDA service](../../components/qcl-negf-aiida/src/aiida_qcl_negf/service.py).

`list_artifacts` возвращает все attempts, отсортированные по attempt, с
`attempt` и `calcjob_uuid`. Portal выбирает первый `execution_id/path`,
но открывает файл без attempt. Service в этом случае выбирает published
selection. При attempt 1 размером 100 байт и selected attempt 2 размером
200 HTTP ответ отдаёт первые 100 байт attempt 2 с размером attempt 1.
При одинаковых размерах ошибка identity остаётся менее заметной.

**Решение:** точный locator должен передаваться от списка через URL/token
до открытия и размеров файла. Владелец HTTP — portal, selection — AiiDA,
формат — contracts. Проверка: два attempts одного path с разными размерами
и содержимым; оба читаются по точному locator, selected shortcut согласован.
Удаление старой download панели само по себе не исправляет API.

### CR02 — P1: shutdown может пересекаться с delivery/RESUME

**Локаторы:** platform `ops/worker_lifecycle.py:94–95, 114–115, 153–155`;
`ops/application_release.py:427–429`.
[Worker lifecycle](../../components/qcl-negf-platform/ops/worker_lifecycle.py),
[Delivery](../../components/qcl-negf-platform/ops/application_release.py).

Shutdown берёт `shutdown-N.lock`, delivery/startup — `delivery.lock`.
После подтверждения idle не остаётся сохраняемого «узел выключается»:
пустой случай сразу успешен, completed snapshot удаляется. Между этим
ответом и реальным выключением Hyper-V guest delivery может проверить
ещё работающую VM, выполнить безусловный RESUME и открыть admission.
Новый job тогда получает allocation перед выключением.

**Решение:** в целевом whole-cluster update I14 один serial entry point
закрывает admission, проверяет ручную отмену workflows/jobs и фактическую
остановку всех workers до activation. Admission не открывается до общего
startup/health check. Не переносить старые независимые shutdown/startup/
delivery entry points в новую схему без общего guard. Проверка: interleaving
shutdown → delivery → job admission; до завершения операции узел не
возобновляется. Для обычного worker shutdown вне обновления отдельно
нужен контракт, предотвращающий RESUME до trusted startup; это не основание
строить mixed-version release workflow.

### CR03 — P2: две записи NodeName могут проверять одну VM

**Локаторы:** platform `ops/application_release.py:392–399, 417–425, 201–212`.

Проверяется уникальность names, но не связь `NodeName → target → machine`.
Два worker names с одним SSH target доставляют/проверяют одну машину дважды.
Receipt содержит release identity без подтверждения remote NodeName;
затем второй Slurm node получает RESUME без собственной проверки.
Даже уникальные строки target не защищают от двух aliases одной машины.

**Решение:** enrollment machine identity и remote node identity связываются
с inventory и receipt; конфликт отклоняется до fleet mutation. Проверка:
два names на один target и разные aliases одного enrolled узла.

### CR04 — P2: delivery не имеет собственного конечного времени ожидания

**Локаторы:** platform `ops/application_release.py:31–33, 383–386, 468–470`.

`subprocess.run` не ограничивает timeout/output; SSH не задаёт connect/alive
limits. Зависшие copy/systemctl/SSH удерживают transition lock и закрытый
gate. Ограниченный solver self-check не ограничивает остальные команды.
Внешний GitHub workflow timeout также не подтверждает завершение remote
операции. Намеренное ожидание normal shutdown до безопасной остановки —
другая политика и не основание делать бессрочным release transition.

**Решение:** bounded command adapter и operation deadline; сохраняемый
failed state и возможность повторной сверки. Проверка: stalled child,
потеря SSH после remote mutation, частичный stdout. Новые remote действия
не запускаются лишь потому, что клиент перестал ждать.

### CR05 — P2: identical activation не восстанавливает solver profile

**Локаторы:** platform `ops/application_release.py:290, 295–298, 204–207`.

`same` проверяет application profile и ready record; при совпадении оба
profile setters пропускаются. Если solver profile отсутствует/неверен,
activation его не исправляет; check может пройти, пока expected solver
всё ещё находится в Nix store. При этом заявленная GC-root protection
для solver не подтверждена.

**Решение:** проверять и независимо восстанавливать обе profile identities.
Проверка: правильный app profile + повреждённый solver profile; identical
retry исправляет состояние без изменения release/Code identity.

### CR06 — P2: vocabularies approximate расходятся между core и Runner

**Локаторы:** core `src/domain/research_policy.jl:179`; Runner
`src/composition/scientific_execution.jl:167–168`.
[Core policy](../../components/QCLNEGF.jl/src/domain/research_policy.jl),
[Runner](../../components/QCLNEGFRunner.jl/src/composition/scientific_execution.jl).

Core выдаёт `:approximate` / `:approximate_fixed_point`; research continuation
допускает `:approximately_converged`, которого этот путь не выдаёт. Такой
предшественник не используется там, где старый research контракт допускает
finite approximate state. Это не доказывает неправильный численный результат.

**Решение:** согласовать vocabulary/contract либо убрать эту legacy policy
при пересмотре режимов. Для нового требования S06 нельзя автоматически
разрешить approximate predecessors: eligibility должна соответствовать
объявленному gate. Проверка: каждый реальный core status на границе Runner.

### CR07 — P2: generated overrides не обновляют per-leaf происхождение

**Локаторы:** Runner `src/infrastructure/scientific/definitions.jl:393–421`;
`src/infrastructure/config/configuration.jl:214–235`.
[Definitions](../../components/QCLNEGFRunner.jl/src/infrastructure/scientific/definitions.jl).

После merge с учётом sources код напрямую заменяет mode, температуры и
outputs. Например, source `research_continue` и definition `adaptive_working`
дают effective raw второго режима, но per-leaf history остаётся от source.
Это проблема объяснимости существующей квитанции; версия кода и resolved
plan всё ещё могут позволять воспроизведение.

**Решение:** убрать несколько authorities либо применять generated changes
через один assignment mechanism с origin/reason. Проверка: источник,
variant и axis override отражены в effective values и объяснении.

### CR08 — P2: optical_map не читает сохранённый optical artifact

**Локаторы:** Runner `src/composition/scientific_execution.jl:1294–1327`;
`src/infrastructure/scientific/postprocessing.jl:244–260`.
[Writer](../../components/QCLNEGFRunner.jl/src/composition/scientific_execution.jl),
[Reader](../../components/QCLNEGFRunner.jl/src/infrastructure/scientific/postprocessing.jl).

После stationary commit optional optics записывает отдельный `optical.h5`
и сохраняет его путь в `data["optical"]`. `_optical_series` проверяет этот
locator, но открывает `_analysis_path` и ищет группу `optical` там.
Стандартный `analysis.h5` создан до optional optical work; sidecar не
добавляет в него spectrum. В результате доступный сохранённый spectrum
может сопровождаться ошибкой `saved native optical response is absent`.

**Решение:** читать объявленный optical artifact с его identity/quality и
актуальным schema contract. Проверка: stationary analysis без optical group
и отдельный valid optical sidecar; `optical_map` выбирает sidecar. Это
static finding; fixture/runtime ещё не выполнялись.

Отдельно уточнить смысл `archive.projections`: флаг декодируется/учитывается
в оценке storage, но final caller `scientific_execution.jl:1252` не передаёт
его в `commit_point_artifacts`, где `analysis=true` по умолчанию
(`point_artifacts.jl:754`). Нельзя обещать отключение native analysis
сохранения этим флагом до определения его контракта.

## Дополнительный аудит физической документации

Полные наблюдения о числах, assumptions и локальной публикации приведены в
[документационном контракте](physics-documentation.md#что-обнаружено-в-текущей-физической-документации).
Здесь два конкретных расхождения с кодом, которые следует исправить в
owning Core docs без изменения научных критериев:

- **DOC01 / P2:** `docs/src/theory/09_scba.md:84–91` описывает approximate
  early return при enabled `diagnostic_quality`, но
  `src/domain/numerical_convergence.jl:383–384,463` требует также
  `adaptive_working`. Контрпример: `research_continue+enabled` не получает
  описанный выход. Дополнить условия и scope описания.
- **DOC02 / P2:** `docs/src/theory/18_optical_response.md:85` без ограничения
  baseline заявляет отсутствие e–e рассеяния. При этом
  `src/numerics/reference/kernels.jl:628–631` допускает SPPA e–e, а
  `src/physics/optical_response.jl:494–498` читает соответствующее solution
  без запрета SPPA. Уточнить baseline scope, сохранив явное отсутствие
  δΣ/vertex corrections. Это не установленный дефект gain.

Sources конкретных Δ/Λ, κ, material и alloy чисел в прочитанных паспортах
не установлены на уровне каждого значения. Отсутствие такого locator не
доказывает неверность числа. DOI геометрии не заменяет источник всех
коэффициентов; явно помеченные exploratory значения допустимы по C13.

## Расхождения с новыми требованиями — не баги старого контракта

| ID / требование | Свидетельство | Что необходимо изменить |
| --- | --- | --- |
| GAP01 / I06 | Portal `frontend/src/main.tsx:124–129, 345` требует CPUs/RAM/time, default 4 GiB; Runner `scientific_execution.jl:191–209` проверяет envelope | Использовать прогноз до submission; runtime refusal сохранить |
| GAP02 / R08 | Portal `api.py:83–97`; AiiDA `validation.py:76–82`, `workflow.py:118–122` | Общий study CPU grant и scheduler QOS/account вместо только per-job limits/retry count; общий calendar deadline пока не обязателен |
| GAP03 / R05 | Portal `api.py:177–190` один bearer | Разные principals с сопоставимыми study rights; без deployment credentials |
| GAP04 / I02 | Root `.github/workflows/release.yml:57–75` запускает delivery | Перенести эксплуатационный trigger/credential в local management; CI выпускает artifacts |
| GAP05 / I13 | Platform `tofu/proxmox/main.tf:116, 125–129`: reboot-after-update и fixed RAM | Не изменять capacity работающего node через прямой apply; idle-bound transition с проверкой actual RAM |
| GAP06 / C06 | Research `config/policies/analytical-diagnostic.yaml:16–26` содержит embedding и alloy physical choices | Разделить физическую модель и численный протокол; показать model diff |
| GAP07 / S04 | Runner `src/composition/configured_study.jl:706–744`, `run_comparison_study` запускает methods × repetitions, затем сравнивает | Отдельные команды «создать/исполнить варианты» и «сравнить готовое»; сохранить совместимость legacy API |
| GAP08 / R01–R04 | Portal `main.tsx:345, 540–549, 591–624`: frozen JSON, text results, archive panel; AiiDA `service.py:318–323`: repository access | Предметные формы/карточка и NFS reader; архивный интерфейс перенести из ежедневного пути |
| GAP09 / I07 | Platform `nix/images.nix:8`, `modules/image.nix:3`: BIOS/QEMU/`/dev/vda`; Windows runbook готовит существующую VM | Отдельные install profiles/identity/discovery checks для трёх backend |

Реальное раннее обнаружение ошибок также нуждается в отдельной проверке
всех build entry points. Наличие `site-preflight.nix` и image receipt gate
не доказывает, что любой native/application build проходит их первым.
Root CI на текущем составе запускается main push/manual, без PR trigger;
нужны дешёвые непривилегированные PR checks и отдельный trusted финальный
интеграционный gate. Не следует выполнять произвольный PR на runner с
production доступами.

## Управляемость кода

В model passport `config/model/reference-2019-70k.yaml` — 274 строки и 199
именованных leaf slots при подсчёте unique paths (слои свёрнуты в
`layers[].field`, scalar/list/null учитываются как один slot). Это не 199
независимых физических степеней свободы: там смешаны model, discretization,
algorithm, outputs и runtime metadata. Поэтому автоматическая форма всех
полей не устраняет нагрузку; нужно уменьшить авторский request и оставить
полный resolved input проверяемым.

| Семейство существующих «режимов» | Смысл | Как пересматривать |
| --- | --- | --- |
| `strict_fail_fast`, `research_continue`, `adaptive_working` | Различное поведение inner/outer iterations и допуска рабочего состояния | Сначала явные contracts/статусы; не заменять три алгоритма одним label без проверки поведения |
| `production` / diagnostic purpose | Путь проверки/исполнения с разной применимостью gates | Назвать назначение явно; diagnostic state не превращать в scientific accepted |
| Reference/optimized kernels | Реализация операторов | Эквивалентность проверяется независимым oracle; performance backend не меняет модель |
| Physical approximations / boundary embedding | Может менять физическую задачу | Model variant с явным обоснованием, не performance policy |
| Independent / continuation | Зависимость начальных состояний между точками | Выбор research plan, а не inner solver acceptance |
| Comparison / output profile | Анализ/сохранение | Вывести из перечня solver execution policies |

Полная таблица каждого enum/публичного API и migration входит в этап
рефакторинга; этот review не объявляет все численные policies избыточными.
Часть сложности необходима для объяснимой модели, часть появилась из-за
нескольких authorities и смешанных интерфейсов.

`configuration.jl` содержит 1986 строк, `local_lab.py` — 745,
portal `main.tsx` — 656. Размер сам по себе не дефект. Риск — сосредоточение
разных инвариантов: resolution/defaults/units/validation, host provision/
image state/acceptance и auth/submission/download/presentation.

Рефакторинг нужен по владельцам инвариантов: небольшой resolver и typed
construction; отдельные scientific status contracts; platform command
adapter/transition state; portal study/result views. Не дробить по одному
параметру и не начинать с тотальной переписи. Изменяемый участок сначала
получает проверку конкретного failure scenario, затем меняется и только
после этого переносится между модулями.

## Итог аудита

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Главные package boundaries полезны | Core API, Runner, AiiDA, results и текущая architecture | Реальный runtime нового HEAD не проверен | Сохранить |
| Есть дефекты identity, lifecycle и optical reading, независимо от новой архитектуры | CR01–CR08 и source scenarios | Не выполнены runtime regression tests | Изменить |
| Требования автоматизации не выполнены одной существующей настройкой | GAP01–GAP09 | Наличие частных дополнений на сервере неизвестно | Изменить |
| Один physically justified stationary result пока не установлен этим аудитом | Final audit разделяет уровни; предъявленного production artifact здесь нет | Архивы расчётов не исследованы; отсутствие результата вообще не доказано | Данных недостаточно |
| Стоимость SHA/I/O и реальная capacity неизвестны | Повторные checks видны в коде, hardware inventory отсутствует | Статическое число вызовов не равно дисковым чтениям/времени | Дополнительно измерить |
