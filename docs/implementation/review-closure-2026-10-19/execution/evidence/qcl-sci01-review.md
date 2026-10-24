# SCI01 — независимая проверка пяти saved originals

Дата анализа: 2026-10-19. Reviewer /root/reviewer, gpt-6.1-sol high.
Этап: bounded analysis существующих metadata; `qcl-results-analysis`.
Вопрос: что известно о terminal/final/raw старого S01? Новых наблюдений сервера нет.

**Вывод:** identity и исторические submit/RUNNING подтверждены выбранными
original bytes. Terminal outcome, final raw completeness и научная приёмка
этого run по выбранным пяти inputs не установлены. Это не диагноз solver failure.
С coordinator `/tmp/qcl-sci01-saved-audit.json` существенных расхождений нет.

## Inventory до содержательного чтения

Префикс originals — `.build/server-resume-20261012-recovery/` preserved checkout.
Размеры проверены до JSON decoding. Все hashes независимо вычислены reviewer
и совпали с A/RV01. Никакие найденные архивные scripts не исполнялись.

| Artifact suffix | Bytes | SHA256 |
| --- | ---: | --- |
| canonical-update-ROOT-recovery-attempt4/ROOT-result.original.json | 51840 | 4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3 |
| freeze600-ROOT-recovery-attempt1/owning-plan.native-original.json | 46353 | 4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9 |
| S01-memory-status60-ROOT-attempt2/early-status-derived.json | 7978 | d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90 |
| S01-submit-ROOT-recovery-attempt1/installed-submit-stdout.original.bin | 1444 | bd40aaae80a2a5e9816555fa1a340a8253014428e8ddf99040b0cea50ed4b976 |
| S01-memory-status60-ROOT-attempt2/control.transport.native-original.json | 43521 | 1f8762528996ce904f181a721f0f463d3b33f2c4d66fb7ebf2634aae41b848cb |

Unique original bytes =151136. Повторные bounded reads использованы для hash,
decoding и selected fields; это не утверждение, что суммарный I/O равен unique size.
Суммарный metadata I/O существенно ниже 64MiB. Decoded transport stdout:
22339bytes, SHA256 `51c8eafb765c69ee2a2a01c2eb22c82333c212f451aa1617d4e405c6b09555e5`.
Он JSON-decoded в памяти; arrays/extraction отсутствуют. Primary original
transport и secondary derived status сохраняют разную evidential роль.

## Паспорт и точные selections

- Plan hash — inventory выше; `/schema=qcl-negf-scientific-plan-v2`,
  `/model_revision=transport-contract-v2`, `/maximum_solver_runs=1`, одна
  execution `execution-1`, одна point `point-1`. Имя фиксирует thermal equilibrium
  candidate 0mV/70K; название не доказывает физическое состояние.
- Plan `/fingerprint=6cf97badf6578a4f2853f497409cd2d215a8b0f020d18074892e2176e21102ee`;
  `/scientific_fingerprint=49ed42000d616857f4e11cf56f7350d9c7ffdb8550e494cf8b53725761e9ed8a`.
  Submit original подтверждает эти поля, `/input_PLAN_sha256` и
  `/input_provenance_verified=true` как statements producer.
- Submit `/submitted=true`, `/submitted_UUID=dfb75b38-6019-4861-b868-f51648c71f02`.
  Его `/Slurm_job_ID=null` не подменён нулём: JobID появляется в позднем status.
- Derived status `/RUN_UUID` совпадает с original transport decoded
  `/aiida/RUN_UUID`; `/aiida/plan_sha256` совпадает с hash frozen plan.
- Derived `/CalcJob` и original decoded `/aiida/CalcJob` согласны:
  UUID `bb7b9d59-863f-440e-b687-b83ac596f9bb`, attempt1,
  execution-1, JobID `1`, process_state `waiting`, exit_status `null`.
  Saved scheduler_state `running`, process_status указывает RUNNING.
- Original decoded `/aiida/root/is_terminated=false`; derived
  `/CalcJob/retrieved_UUID=null`, `/CalcJob/result_UUID=null` относятся к тому
  snapshot, а не к текущему состоянию. Transport capture bounds
  `/local_before_epoch`–`/local_after_epoch` соответствуют
  2026-10-13 17:46:21.771927–17:46:24.009806 UTC.
- Derived `/Slurm/fields/JobState=RUNNING` при `/ExitCode=0:0`.
  Ни этот scheduler field, ни scheduled EndTime не являются terminal outcome.
- Canonical receipt `/native_owned_closure/runtime/release_id=
  qcl-5d779b52-s01-20261012`, `/runtime/ready=true`, `/gate/open=true`,
  `/delivery_report/status=completed`. Это technical delivery/runtime claims,
  не scientific process completion. `/scientific_accepted=false` и
  `/full_release_CI_accepted=false` сохранены буквально.
- Derived `/final_HDF5_assumed=false` означает, что final HDF5 не следует
  предполагать. Это не inventory отсутствующих файлов и не доказательство,
  что final HDF5 нигде не существует.

## Identity и пределы source evidence

Current audit root `e0f244d075dd49874ba4f3847f4efa693f3b3622` и выбранные
сейчас component gitlinks не объявлены producer старого scientific run.
Архивная review campaign имеет собственный historical source receipt;
RV01 — вторичное summary, независимо сверенное с пятью originals.
Frozen plan/model revision и fingerprints устанавливают declared identity,
а не imported Julia binary/source. Installed runtime release label выше
не заменяет core commit, derivation и import provenance.
Decoded transport содержит `/aiida/owning_sources/{service,validation,workflow,
calculation,data}` с path/hash metadata. Это сведения об owning AiiDA modules,
не доказательство imported solver source. Его identity в этом packet остаётся
unresolved; source/installed/imported/scientific assertions не смешиваются.

## Пять уровней свидетельств

| Уровень | Verdict | Основание и ограничение |
| --- | --- | --- |
| Execution | Historical submit и RUNNING observation подтверждены; terminal/current unknown | Exact originals, capture2026-10-13; metadata не является live probe |
| Итерационная сходимость | not_measured | Нет выбранного final residual и согласованной final U/G; waiting/exitnull не convergence evidence |
| Физические gates | not_measured | Нет выбранных raw gate measurements; receipt scientific_accepted=false не указывает причину и не доказывает physics failure |
| Достаточность дискретизации | not_measured | Нет refinement evidence; название модели/plan size не criterion |
| Экспериментальная validation | not_measured | Нет comparable experiment и uncertainty; equilibrium verification отдельно от validation |

## Сопоставление с coordinator audit и границы

Сначала reviewer закрепил own observations сообщением coordinator, затем
прочитал `/tmp/qcl-sci01-saved-audit.json`. Inventory/hash/decoded stdout,
run/attempt/plan identity, release/gates и evidence-vector согласны.
Уточнение report: 151136 — unique input size, не полный измеренный I/O;
no final/raw inventory относится только к named set, не ко всему filesystem.

Не выполнялись remote probes, cancel/resubmit, solver/import/build/tests,
HDF5 reads, arrays, extraction либо изменение originals. Старый S01 защищён.
Полного поиска raw/terminal artifacts не было. Единственная начальная
ошибочно широкая shallow `ls` вывела имена соседних saved entries; содержимое
этих файлов не читалось и listing не использован для completeness/absence claim.
Ресурсные CPU/RAM peaks не измерялись; processing stdlib-only, serial,
selected output/report существенно ниже64KiB.

Следующее различающее свидетельство — существующий exact terminal receipt
и archive/part inventory для run/attempt1 с plan/import binding. Добывать только
из разрешённых доступных protected inputs. Недоступность сервера не разрешает
polling, новый solve или отмену старой работы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Старый attempt1 однозначно связан с frozen plan | Пять hashes, submit + original decoded transport | Hash identity не истинность всех producer claims | сохранить |
| Technical delivery completed означает scientific terminal | Canonical receipt paths против saved RUNNING | Разные процессы/gates; current terminal неизвестен | данных недостаточно |
| Final/raw полнота и physical acceptance установлены | В named inputs нет нужного inventory/final measurements | Не доказано отсутствие raw вне named set | данных недостаточно |
| Дальнейшая проверка требует нового solve | Достаточны missing exact terminal/inventory/provenance | Эти inputs пока не получены; server не опрашивается | дополнительно измерить |
