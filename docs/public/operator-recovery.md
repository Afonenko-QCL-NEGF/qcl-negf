# [Восстановление прерванного запуска](@id operator-recovery)

Цель оператора — передать совместимое acknowledged состояние в новую попытку,
сохранив исходную попытку и причины её отказа. Начните с immutable release/source
identity и frozen plan, затем проверьте комплектность recovery и границу
разрешённого исполнения. Наличие этой страницы не устанавливает готовность
конкретной установки или возможность восстановить её данные.

## [Исходники и prerequisites](@id recovery-prerequisites)

Для выбранного execution/point установите source attempt, frozen plan и identity
модели. Свяжите их с сохранённым release manifest, точной root revision и
gitlinks компонентов. Текущий checkout, имя каталога или страница другой версии
не заменяют provenance архивного результата. Если связь не сохранена, запишите
её как неизвестную и остановите зависящий от неё вывод.

Привязка документации к release/source, доступность входных metadata и научный
статус — отдельные факты. Отсутствующий bundle/fragment не стирает независимо
проверенные metadata попытки. При отсутствующей привязке нельзя подставить
текущие defaults, значения из другого attempt или reference origin вместо
неизвестного actual origin.

| Что проверяют | Как читать результат |
| --- | --- |
| Source/release identity | Нужна проверяемая связь с выбранной попыткой; совпадения имён недостаточно. |
| Metadata и artifact inventory | Недостающий факт остаётся unknown; missing/corrupt обязательный artifact или hash вызывает отказ проверки, а не ноль или `pass`. |
| Готовность исполнения | Fresh inventory/admission, доступ к данным и credentials проверяют для конкретного этапа. Недостающий prerequisite блокирует этот этап. |
| Recovery | Совместимая verified generation и полный набор её declared dependencies позволяют подготовить передачу в новую попытку. |
| Научный результат | Process exit, восстановление, сходимость, физические проверки, дискретизация и экспериментальная валидация читаются отдельно. |

## [Staging и сохранность данных](@id staging-prerequisites)

До копирования определите объём metadata и payload, конечный byte budget,
свободное место и владельца целевого хранения. Сохраните pointers, поколения,
commit/receipt, failed logs, request/attempt identity и исходные массивы.
Проверяйте копию тем же owning reader; один receipt со строкой `verified`
не заменяет readback и проверку всех declared artifacts.

Копируйте generation целиком. Для многоточечного execution нужны также prior
final archives, перечисленные в hash-bound `execution_progress.json`.
Аналитический export, progress snapshot и каталог `pending-*` не являются
полным состоянием restart. Final archives не удаляют ради recovery budget.

Worker-local scratch служит рабочим хранением. Он и shared staging не заменяют
backup. При включённом recovery Runner пишет непосредственно в `OUTPUT`,
обходя перенос только в конце execution. Receipt с
`publication_scope: local_filesystem` подтверждает свою локальную область;
cross-node/LAN durability и фактический restore требуют отдельных свидетельств.

Существующий S01, чужие jobs/VM, исходные результаты и диски сохраняют свои
identity и владельцев. Recovery не разрешает отменять чужие jobs, удалять
failed evidence, форматировать существующие диски или заменять state/data.
Для инфраструктурного restore сначала согласуют archive boundary и полный
набор зависимых данных; успешный локальный import не доказывает восстановление
сервисов или независимость внешней backup-копии.

## [Выбор acknowledged generation](@id recovery-selection)

Owning reader начинает с `current.json`: проверяет digest pointer, commit,
receipt и каждый declared artifact. Если current corrupt, он проверяет
`previous.json` тем же способом. Имя «latest» не даёт преимущества перед
проверенной previous generation. Её source identity и уже израсходованный
вычислительный бюджет сохраняются.

| Доступное состояние | Ожидаемый результат |
| --- | --- |
| Только `pending-*` или progress snapshot | Acknowledged recovery недоступен; исходные файлы и логи сохраняют. |
| Current corrupt, previous проходит все проверки | Используют verified previous, явно указав выбранное поколение и source attempt. |
| Оба acknowledged candidates отсутствуют или не проходят проверку | Явный отказ `no valid acknowledged recovery generation`; сохраняют pointers и причины отказа. |
| Полная verified generation и обязательные prior finals доступны | Готовят совместимый import в новый явно разрешённый attempt. |

Отказ выбора не означает cold start, ремонт pointer или разрешение удалить
данные. Новое вычисление с другой инициализацией требует собственной явно
разрешённой identity. Совместимость модели, grids, алгоритмов/runtime и
накопленного бюджета проверяет Runner/native restart reader.

## [Передача в новую попытку](@id recovery-handoff)

После проверки входов и получения конечного бюджета оператор использует
существующий CLI маршрут. Это execution: команда продолжает вычисление.
Ниже только синтаксис с условными именами `PLAN`, `OUTPUT`, `ID`, `N`,
`DIRECTORY`; они не обозначают данные какой-либо установки.

```text
qcl-negf run-plan PLAN OUTPUT --execution-id ID --attempt N --recovery-bundle DIRECTORY
```

`OUTPUT` выбирают отдельно для этого import; `N` должен превышать source
attempt. Solver/mixer state и использованные cumulative iteration coordinates
восстанавливаются с проверкой frozen plan/model/runtime compatibility.
Для completed-point dependencies передают `--archive-bundle DIRECTORY` с
деревом `DIRECTORY/archive/EXECUTION/POINT/final/` и задают конечный
`--archive-byte-budget BYTES`. Missing/corrupt prior-final closure вызывает
отказ до solve, а не повторное вычисление уже завершённых точек.

В handoff сохраните выбранные execution/point, source generation/attempt,
проверенные hashes/receipts, identity новой попытки, её output и разрешённый
бюджет. Исходная failed attempt остаётся доступной. Успешный import означает
операционное восстановление; научную пригодность returned state читают по
сохранённому Core assessment. `not_measured` сохраняет причину отсутствия
измерения и не становится `pass`.

## [Owning справка](@id recovery-owning-references)

Ссылки между Core, Runner и operator относятся к единому bundle; их локальные
цели и anchors проверяет итоговая сборка, после отдельных owning-графов.

```@raw html
<ul>
<li><a href="../runner/user/results.html#operator-recovery-route">Runner: полный маршрут recovery</a> и <a href="https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/1acc165650fd4f4c2d49605cc679f90e3f6fcdae/docs/src/user/results.md">закреплённый source этой справки</a>.</li>
<li><a href="../core/theory/12_validation.html#researcher-final-route">Core: чтение финальной точки и критериев</a>. Формулы и пороги принадлежат Core и <a href="https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731/docs/equilibrium-measurement-contract.md">Research contract</a>.</li>
<li><a href="https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/12fc26462bbab3df76904c6deb01f8c6596de7be/src/qcl_negf_contracts/artifacts.py">Contracts: artifact format</a>. Эта глава не вводит отдельного формата или критерия научной приёмки.</li>
</ul>
```
