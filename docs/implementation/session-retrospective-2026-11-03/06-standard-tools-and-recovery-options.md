# Готовые инструменты и небольшой выбор дальнейшего пути

**Это документ для обсуждения, не новый implementation plan.** Пользователь остановил изменения.
Ничего из перечисленного не устанавливается, не удаляется и не запускается этим PR.

## Почему задача не требует изобретать собственный кластер

Основная вычислительная форма в текущей architecture — один execution на одном worker с одним
threaded Julia process. Независимые executions могут идти на разных workers; continuation points
остаются внутри execution, чтобы не терять численную инициализацию. Это уже описано в
[architecture](../../architecture.md). Такой workload хорошо соответствует обычным batch-job
механизмам. Специфичны физическая модель, solver, checkpoint/state semantics и scientific
acceptance, а не сам факт постановки задачи в очередь.

Готовые инструменты покрывают значительную часть инфраструктуры:

| Потребность                                                              | Уже существующий механизм                                           | Чего он сам не доказывает                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Очередь, выбор worker, CPU/RAM allocation, отмена                        | Slurm jobs, sbatch/squeue/sacct/scancel                             | Сходимость NEGF, правильность input и final                                            |
| Набор независимых одинаково устроенных расчётов                          | Slurm job arrays; при различающихся resources отдельные submissions | Что continuation-dependent points можно сделать независимыми                           |
| Учёт/ограничение процессов задачи внутри guest                           | Slurm task/proctrack/jobacctgather + cgroup v2/systemd              | Физическую reservation RAM на hypervisor и защиту foreign VM от произвольного admin    |
| Постановка внешнего scientific executable, transfer/retrieval/provenance | AiiDA CalcJob, scheduler/transport plugins, Parser                  | Scientific acceptance; полный результат, если plugin неправильно определил outputs     |
| Воспроизводимые packages и declarative guest services                    | Nix/NixOS, systemd                                                  | Backup mutable AiiDA/PG/NFS и атомарность любой внешней PVE mutation                   |
| Изоляция worker, фиксированная память, lifecycle VM                      | Proxmox/libvirt, guest agent                                        | Работоспособность текущего выбранного image и конкретные host reserves                 |
| Scientific state/physics diagnostics                                     | QCL Core/Runner/Results                                             | Здесь действительно нужен собственный scientific code и независимые criteria/reference |

Официальные источники проверены при составлении документа:
[Slurm job arrays](https://slurm.schedmd.com/job_array.html),
[Slurm cgroup v2](https://slurm.schedmd.com/cgroup_v2.html),
[AiiDA calculations usage](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/calculations/usage.html).
Они подтверждают capabilities инструмента; это не evidence корректности нашей установленной версии.
Документация может обновиться, поэтому installed source/version надо сверять отдельно.

Job arrays относятся к похожим batch tasks, каждый остаётся обычным Slurm job. Это не команда
распараллелить любой bias sweep: зависимости continuation должны остаться в том же execution, как
требует модель. Cgroup plugin взаимодействует с systemd и может ограничивать/учитывать jobs, но
нельзя складывать configured memory как будто это physical host RAM. AiiDA предоставляет lifecycle
external executable, а QCL-specific binding нужен только там, где типовые interfaces действительно
не выражают required scientific provenance.

## Три варианта, которые можно оценить без новой большой архитектуры

### A. Один известный worker и прямой научный executable

Задача: отделить работоспособность numerical application от scheduler/provenance/UI. Inputs,
immutable Source, frozen plan, criteria, stdout/stderr и output path остаются явными. Это
диагностический baseline, не приёмка кластера и не автоматическое разрешение нового scientific
solve.

Польза: меньше одновременно неизвестных компонентов. Ограничение: не проверяет remote Slurm/AiiDA
путь; не должен стать ещё одним постоянно поддерживаемым runtime или обходом требований к научному
provenance.

### B. Slurm с фиксированными ресурсами на существующих VM

Задача: один известный worker, честный actual full fixed RAM/host budget, Slurm/cgroup limits после
guest reserve; standard job lifecycle и existing Runner executable. Admission, host/foreign safety,
cleanup и result integrity сохраняются. Dynamic ballooning, дополнительные hypervisors и развитой UI
не объявляются поддержанными.

Это наиболее прямой кандидат для первого полезного кластерного пути, поскольку conservative/fixed
fallback уже разрешён исходным
[планом](../project-simplification-2026-10-27.md#52-proposed-per-host-protocol). Но это рекомендация
для анализа, а не установленный факт: текущий installed route может требовать конкретного owning fix
и проверенного maintenance transition. Нельзя просто изменить флаг admission или стирать paid
journal.

Различающее evidence: один заранее определённый controlled synthetic job на actual installed image с
trace submit→allocation→execute→final→independent read; отдельный normal/abnormal cleanup и исходные
host/guest limits. Пробный scientific solve после такого evidence — отдельное frozen scientific
действие, без изменения grids/tolerances ради удобства.

### C. Сохранить обязательным полный AiiDA/Portal/dynamic путь

Польза: сразу богаче provenance/UI и online resource protocol. Цена: текущие
integration/closure/qualification gaps остаются на критическом пути, ещё до первого полезного
исследования. Это допустимый осознанный продуктовый выбор, но его нельзя скрывать за утверждением
«иначе научный кластер невозможен».

Для выбора нужны необходимость каждого custom layer и estimate оставшихся конкретных gaps, а не
число пройденных tests. Нынешний9-case dynamic design имеет два независимых blocker; Source29 ещё
design-only. Их нельзя считать закрытыми или обещать малую стоимость дописывания.

## Что предложено, а что оставлено на решение

Предложение координатора: будущий анализ начать сB, используяA только как диагностический baseline
при необходимости. AiiDA не выбрасывать; определить, какие его гарантии пользователь действительно
требует на самом первом trial, и довести уже существующий adapter, если provenance обязателен.
ВариантC не продолжать по инерции.

Сейчас не выбираются окончательно ни новый stack, ни язык, ни переписывание. Прежние numerical
inputs/scattering/basis/grids/tolerances и independent reference сохраняются. Существующие data
disks и scientific provenance не удаляются; физические результаты не экспортируются этим отчётом.
Пользователю не предлагается вручную рецензировать весь накопленный Source: сначала нужен маленький
понятный эксплуатационный contract и независимый review именно его necessity/call graph.

| Утверждение                                                | Свидетельство                                                               | Ограничение                                | Решение                             |
| ---------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------- |
| Для основной кластерной формы есть стандартные инструменты | Official Slurm/AiiDA docs; current one-node threaded execution architecture | Не гарантирует наш installed configuration | сохранить native механизмы          |
| Полный custom dynamic framework обязателен                 | Original plan допускает fixed reservation; independent necessity review     | Fixed route тоже не принят                 | изменить предмет следующего анализа |
| ВариантB уже работает                                      | Actual end-to-end evidence ещё нет                                          | Нужны конкретные prerequisites             | данных недостаточно                 |
| Надо прямо сейчас строить новый stack                      | Такого решения пользователь не принимал                                     | Current task — evidence и помощь в выборе  | сохранить остановку                 |
