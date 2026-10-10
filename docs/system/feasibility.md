# Допустимость требований и опыт других проектов

Статус: критическое исследование 2026-10-09. Выводы о переносе опыта —
наши предложения, а не утверждения авторов источников о QCL-NEGF.
Hardware measurements, benchmarks и развёртывания не выполнялись.

## Главная оценка направления

Риск проекта — принять готовность инфраструктуры за движение к научному
ответу и сделать всё удобство обязательной предпосылкой первого расчёта.
Из исходников видно, что локальный вычислительный путь уже отделён от
кластера. Следовательно, очередная общая перепись системы не является
необходимым условием S01. Это инженерный вывод из API, не доказательство
корректности solver или отсутствия всех прежних научных результатов.

Рекомендация: оставить полный согласованный объём релиза, но поставить
научный рубеж перед расширением GUI/универсальной автоматизации. Если
дешёвая предметная проверка обнаружит проблему уравнений или результата,
разработка интерфейсов для массового sweep приостанавливается до её
локализации. «Нужен ещё один framework» должно иметь различающее основание.

## Согласованность и контрпримеры

| Напряжение требований | Контрпример | Уточнение / решение |
| --- | --- | --- |
| Весь цикл одним релизом и быстро получить физический результат | Новый editor, agent API, три installer и clean rebuild становятся prerequisite каждого solve | Один релиз с независимой поэтапной приёмкой; S01 идёт на минимальном научном пути |
| Максимум RAM и все посторонние VM активны | Сумма их реально необходимой памяти плюс compute превышает physical RAM | Защищённые floors/reserves и measured admission; «максимум» ограничен ими |
| Большой swap и предсказуемая scientific performance | Рабочие Green arrays постоянно fault на SSD; RAM формально хватает виртуально, CPU-часы расходуются на ожидание | Swap не включается в Slurm RealMemory; заданный pressure предел и измеряемое сравнение |
| Только декларативность и автоматический безопасный handoff | Desired builder=on/compute=off применён параллельно; compute ещё не остановлен | Стандартные declarations плюс один serial lifecycle protocol, не скрытая bash policy |
| ISO стирает различия платформ | Hyper-V Gen2 требует UEFI, текущий image BIOS; cloned static IP конфликтует | Одна гостевая роль, несколько install/boot/network profiles и доверенный enrollment |
| YAML прозрачен и содержит сотни expert настроек | Dropdown/форма из полной schema лишь переносит ту же нагрузку на GUI | Короткий domain request + versioned protocol + раскрываемый complete input/diff |
| Максимальная свобода агента и неизменная задача | Агент меняет scattering/окно и называет полученный convergence успехом исходной задачи | Свободные явные numerical variants; смена физической модели — отдельное научное решение |
| Minimal evidence и удобный объяснимый результат | Файл с числом J без V/T, units и статуса нельзя корректно сравнить | Сохранять интерпретационные metadata; big trajectory и checkpoint отдельно/опционально |
| Локальная эксплуатация и cold start из GitHub | GitHub/upstream недоступны во время первого скачивания dependencies | Daily operations используют локальный ready release; cold source bootstrap имеет явно проверяемые внешние prerequisites |
| Clean wipe без старого состояния и restore acceptance | Пересборка успешна только благодаря прежнему depot/DB; restore старой DB незаметно возвращает старый system state | Удалить QCL state; проверить cold bootstrap; restore тестировать на новом disposable state |
| Одна актуальная спецификация и независимые repos | Восемь копий требований редактируются отдельно | Нормативный root корпус + owning component API docs, ссылки вместо копий |

По последнему решению обновление кластера выполняется после ручной отмены
оператором всех jobs/queue с остановкой всех QCL workers, hard stop допустим.
Поэтому mixed-version LAN activation и migration старой очереди не входят
в задачу. Обычный ресурсный handoff для сборки остаётся idle-bound.

Опыт распределённых @home/BOINC, HTCondor и native AiiDA retrieval рассмотрен
отдельно в [стратегии результатов](results-and-postprocessing.md). Вывод:
повторно использовать Runner commits + AiiDA metadata + NFS, не создавать
новый workunit server и не заменять Slurm ради передачи файлов.

## Что действительно уже является готовым инструментом

**Повторно используем готовые механизмы.** AiiDA WorkChain даёт сохранённое
исполнение/control flow, Slurm — allocation и accounting, NixOS — services,
OpenTofu/Proxmox — VM. Их повторная реализация в Runner/portal была бы лишней.
AiiDA workflows описаны в [официальной документации исходников](https://github.com/aiidateam/aiida-core/blob/main/docs/source/topics/workflows/usage.rst).

**Единого бесплатного готового инструмента под весь контракт не установлено.**
Это ограниченный вывод проверки перечисленных кандидатов, не доказательство,
что такого инструмента нигде нет. Ни один из проверенных вариантов одновременно
не даёт наш QCL kernel, карточку исследования, bounded agent API, NFS semantics,
учёт общего бюджета и передачу RAM между PVE VM.

| Кандидат | Что можно взять | Почему не заменяет всю систему |
| --- | --- | --- |
| Open OnDemand | Готовый HPC вход к уже настроенному scheduler | Не задаёт физическую постановку QCL и resource handoff PVE; полезен при потребности в общем HPC desktop/files/jobs UI |
| AiiDA WorkGraph | Graph/control flow поверх AiiDA | Дополнительная dependency и workflow abstraction; простое отображение links не требует его внедрения |
| Community Semaphore + Ansible | Локальные task template/API/log для штатных операций | Workflows/часть executor функций платные; нужен один сериализованный entry point, deployment и secret boundary |
| AWX | Развитая бесплатная automation среда | Operator требует Kubernetes; эксплуатационная цена для одного сервера пока не оправдана |
| Cockpit/libvirt | Управление Linux/libvirt host | Не единая штатная панель Proxmox/Hyper-V и не научный каталог |
| nextnano.NEGF | Предметная QCL конфигурация и UI patterns | Коммерческое решение противоречит free-only выбору; научную эквивалентность всё равно нужно проверять |
| ErwinJr2 | QCL layer editor, profile, state/transition visualizations | В репозитории NEGF остаётся TODO; существующая rate-equation physics не заменяет наш NEGF контракт |
| Kwant | Хороший programmable model→solver pattern | Документированный tight-binding transport API не является готовой реализацией нашей QCL SCBA/Poisson модели |

Источники: [Open OnDemand cluster integration](https://osc.github.io/ood-documentation/latest/installation/add-cluster-config.html),
[WorkGraph](https://aiida-workgraph.readthedocs.io/en/latest/),
[Semaphore templates](https://semaphoreui.com/docs/user-guide/task-templates),
[Semaphore security](https://semaphoreui.com/docs/introduction/security-model),
[AWX Operator](https://github.com/ansible/awx-operator),
[Cockpit VM feature](https://cockpit-project.org/guide/195/feature-virtualmachines.html),
[nextnano.NEGF](https://www.nextnano.com/resources/download_code_NEGF.php),
[ErwinJr2 repository](https://github.com/ErwinJr2/ErwinJr2),
[ErwinJr2 physics](https://erwinjr2.readthedocs.io/en/latest/manual/physics_quantum.html),
[Kwant introduction](https://www.kwant-project.org/doc/1/tutorial/introduction).
Проверка лицензии и точных pinned dependency версий проводится при выборе
каждого нового пакета; похожий screenshot не является критерием внедрения.

## Архитектурные альтернативы

Для физической помощи и учебника новый инструмент не нужен: Core/Runner
уже используют Documenter, а root CI собирает оба сайта из общего Julia
workspace. Дополнение — статический release artifact, локальные assets и
контекстные карточки из owning текста. Локальное serving и fixed light ещё
не реализованы/не проверены; подробности и альтернативы в
[документационном контракте](physics-documentation.md).

1. **Сохранить существующий специализированный стек и упростить границы —
   рекомендуемый вариант.** Минимальный domain layer над AiiDA/Slurm, независимые
   Julia API и results, стандартные infrastructure operations. Больше всего
   сохраняет существующую работу; требует исправить cross-component contracts.
2. **Заменить исследовательский frontend готовым HPC/workflow frontend.**
   Open OnDemand/WorkGraph уменьшают generic UI код, но domain form, material
   sources, numerical protocol и научные summaries остаются нашей работой.
   Оправдано только после probe на двух собственных сценариях, включая failure.
3. **Убрать AiiDA, оставить Slurm + Julia + NFS каталог.** Для одной точки это
   проще; для всей согласованной цели придётся заново писать persisted state,
   retries, dependency graph и execution identity. Допустимый fallback, если
   measured operating cost AiiDA превысит пользу, но не очевидная экономия
   полного релиза. Новая general workflow engine не предлагается.

Количество репозиториев и название framework не определяют качество границ.
Возможная консолидация проводится по dependency/lifecycle и реальной стоимости
координации, а не потому, что один репозиторий кажется удобнее агенту.

## Ресурсы: что подтверждают стандартные инструменты

Согласована пара отдельных больших VM по очереди. Альтернативная mixed VM
снимает переключение VM, но `nix build` client внутри Slurm allocation не
переносит daemon builders туда автоматически. `--exclusive` исключает другие
Slurm jobs, но не внешний daemon; всю зарегистрированную RAM запрашивают
отдельно. CI isolation также ослабевает. Это следует из
[Nix daemon](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-daemon.html),
[cgroup inheritance](https://docs.kernel.org/admin-guide/cgroup-v2.html) и
[Slurm sbatch](https://slurm.schedmd.com/sbatch.html).

Постоянно активная пара с auto-ballooning сложнее выбранного варианта: Slurm
может обещать RAM, которую balloon затем отнимет. В PVE алгоритм работает
с текущей host memory usage и running VM; выключенная большая VM не получает
предварительную reservation. Сумма minima не доказывает safe startup.
Это вывод из [pvestatd](https://raw.githubusercontent.com/proxmox/pve-manager/master/PVE/Service/pvestatd.pm)
и [AutoBalloon](https://raw.githubusercontent.com/proxmox/pve-manager/master/PVE/AutoBalloon.pm);
конкретное поведение установленных PVE/guest versions ещё надо измерить.

`swappiness` задаёт относительную стоимость paging, а не выбор «сначала чужую
VM». `memory.low` — best-effort protection; oversubscribed protections также
не создают RAM. Поэтому swap-настройка не заменяет floors/admission.
[Kernel VM settings](https://docs.kernel.org/admin-guide/sysctl/vm.html),
[cgroup memory protection](https://docs.kernel.org/admin-guide/cgroup-v2.html).

Study CPU grant можно строить на QOS `GrpTRESMins`, `NoDecay`, `UsageFactor=1`,
`PriorityType=priority/multifactor` и accounting enforcement `safe/qos`.
`NoDecay` не является account flag; все retries сохраняют одну QOS без reset.
Цена — SlurmDBD/SQL и правильная привязка
всех submissions. `safe` резервирует возможность завершиться в рамках
выделенного time limit, поэтому слишком щедрый per-job limit может оставить
реально короткий job в PENDING. Общий deadline сейчас отложен пользователем.
Если его введут позднее, deadline не следует подменять одним
HTTP timestamp: `sbatch --deadline` с конечным time limit позволяет scheduler
удалить job, который уже не сможет завершиться к сроку.
[QOS](https://slurm.schedmd.com/qos.html),
[resource limits](https://slurm.schedmd.com/resource_limits.html),
[deadline](https://slurm.schedmd.com/sbatch.html#OPT_deadline).

## Истории научного OSS: что применимо к нам

### Quantum ESPRESSO

В статье 2009 года QE представлен как модульная система взаимодействующих
программ с самостоятельной постобработкой; PWgui создаёт input и показывает
его текст. Авторы оговаривают, что корректный синтаксис не гарантирует
физически осмысленную постановку. Это опыт развития уже существовавшего
научного кода, а не аргумент сперва строить идеальную общую платформу.
Применение: сохранить core/results границу и прозрачный input, а GUI
обосновывать конкретным исследовательским действием.
[Giannozzi et al., 2009, §§2, 3.1, 4.9–4.10](https://arxiv.org/pdf/0906.2569).
Позднейший обзор отдельно обсуждает modularization и interoperability:
[Giannozzi et al., 2017](https://arxiv.org/abs/1709.10010).

### GPAW / ASE

Обзор GPAW 2024 описывает programmable calculator и использование общей
внешней ASE среды для многих сценариев. Разные representations имеют разные
возможности: общий API не делает методы взаимозаменяемыми. Урок для QCL —
не привязывать Julia к portal/cluster и не называть различные физические
приближения одинаковой «оптимизацией». SCF convergence также не доказывает
достижение полного базиса.
[GPAW overview, §§II, IV](https://arxiv.org/pdf/2310.14776),
[GPAW convergence documentation](https://gpaw.readthedocs.io/documentation/basic.html).

### MOOSE

MOOSE вырос в framework для multiphysics applications с domain input,
типизированными параметрами и раздельной SQA документацией. Полезны
владение правилом, input validation и traceability requirements→checks.
Однако framework V&V не является доказательством собственной QCL модели;
его документ отдельно отсылает к зависимостям и physics applications.
Копировать весь nuclear SQA процесс маленькой команде было бы новым источником
нагрузки. Берём короткую трассировку и разделение verification/validation.
[Permann et al., 2020](https://arxiv.org/abs/1911.04488),
[MOOSE input](https://mooseframework.inl.gov/application_usage/input_syntax.html),
[framework VVR](https://mooseframework.inl.gov/sqa/framework_vvr.html).

### Контрпример репутации и воспроизводимости

Bosoni et al. отмечают, что DFT codes широко применялись десятилетиями до
систематической межкодовой проверки precision в 2016 году. Их расширенная
работа строит reproducible workflows для конкретных equations of state и
обсуждает переносимость результата. Межкодовое согласие само по себе не
проверяет новую наблюдаемую и не является экспериментальной валидацией.
Вывод для нас: AiiDA provenance и framework pedigree не заменяют отдельные
QCL operator oracles, discretization study и сопоставимые условия.
[Bosoni et al., Nature Reviews Physics 2024](https://arxiv.org/abs/2305.17274).

## Практики больших IT проектов без копирования их масштаба

Из Linux применимы небольшие логически самостоятельные patches, объяснение
проблемы/эффекта и отдельное обоснование refactor. Из Kubernetes — владелец
ресурса с identity, observed/desired state и проверяемые критерии перехода
из эксперимента в поддерживаемую возможность. KEP связывает сложное изменение
с test plan/readiness/graduation criteria. Для нас достаточно короткого
решения и requirement IDs, без SIG hierarchy и нового control plane.
[Linux patch guide](https://www.kernel.org/doc/html/latest/process/submitting-patches.html),
[Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/),
[owners/dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/),
[KEP process](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md).

Не вводить общую абстракцию до второго реального потребителя. Не проверять
каждый полный HDF5 при выводе строки каталога. Не смешивать source/build/
service/scientific gates одним success flag. Не выпускать routine refactor
как полную новую архитектуру. Эти правила — предлагаемый метод работы,
обоснованный найденными в нашем коде failure scenarios.

## Конфигурационные идеи смежных solver

MOOSE domain blocks и AiiDA-QE `get_builder_from_protocol` показывают путь
«короткая постановка → явный полный builder». COMSOL разделяет Study/Solver
и показывает изменения defaults; parameter continuation отличается от
batch Cartesian sweep и solver accuracy. Такие UX идеи переносим, а методы
адаптации/допуски выводим из наших уравнений и наблюдаемых.
[AiiDA-QE quick start](https://aiida-quantumespresso.readthedocs.io/en/stable/get_started/quick_start.html),
[COMSOL study solver configurations](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.005.html),
[COMSOL changes from defaults](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.108.html),
[COMSOL sweeps](https://www.comsol.com/support/knowledgebase/1250).
В документации CST SAM подтверждается организация связанных simulation
tasks, но публичных материалов недостаточно, чтобы переносить конкретный
adaptive stopping criterion в QCL:
[CST systems modeling](https://www.3ds.com/products/simulia/cst-studio-suite/electromagnetic-systems-modeling).

## Итог

Для сети без DNS admin mDNS допускает имена `.local` на локальном link без
обычного DNS server. Multicast/клиентская поддержка не гарантированы для
данной LAN, поэтому controller/storage endpoints и inventory mappings
остаются обязательным стабильным путём.
[RFC 6762, §§1, 3](https://www.rfc-editor.org/rfc/rfc6762.html),
[Avahi](https://github.com/avahi/avahi).

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Готовые инструменты покрывают большую часть общей инфраструктуры | AiiDA/Slurm/NixOS/PVE и проверенные GUI | Нет проверенного turnkey QCL полного контракта | Сохранить и повторно использовать |
| Требования достижимы поэтапно | Разделённые owners и штатные механизмы | Общая трудоёмкость без team/capacity данных не оценена; срок не обещан | Изменить порядок реализации |
| Zero custom orchestration не обоснован | Cross-layer handoff/enrollment counterexamples | Часть может покрыться стандартными Ansible modules; deadline отложен | Дополнительно проверить узкий adapter |
| «Нет ни одного физического результата» не установлено этим аудитом | Прочитан код и журнал инженерных проверок | Scientific archives здесь не исследованы | Данных недостаточно |
| SSD swap и расширение 100 ГБ условно возможны | Зависит от реальной storage topology и свободного места | Нет свежего inventory; swap performance неизвестна | Дополнительно измерить |
