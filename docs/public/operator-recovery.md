# [Восстановление прерванного запуска](@id operator-recovery)

Цель оператора — установить, какое точное состояние прерванной попытки можно
проверить и какой следующий шаг поддерживает выбранная версия системы.
Проверенный checkpoint, восстановление сервисов и продолжение вычисления —
отдельные возможности. Наличие этой страницы не подтверждает готовность
конкретной установки или научную пригодность сохранённого состояния.

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
| Exact checkpoint | Явно выбранный native5 pointer или immutable StateRef проверяют вместе с полной исходной Identity и всеми declared dependencies. |
| Научный результат | Process exit, восстановление, сходимость, физические проверки, дискретизация и экспериментальная валидация читаются отдельно. |

## [Staging и сохранность данных](@id staging-prerequisites)

До копирования определите объём metadata и payload, конечный byte budget,
свободное место и владельца целевого хранения. Сохраните исходные pointers,
immutable manifests и их зависимости, failed logs и request/attempt identity.
Для продолжения нужны declared native payloads, history frontier и witness
ancestry выбранного состояния. Проверяйте копию owning reader; строка
`verified` в receipt не заменяет readback полного набора зависимостей.

Не выбирайте файлы по именам «latest» или «final». Аналитический export,
progress snapshot и незавершённая публикация не являются exact checkpoint.
History-only manifest с `checkpoint=null` корректно описывает историю, но не
даёт возможности точного восстановления. Родительский tail после выбранного
cutoff остаётся самостоятельным научным свидетельством: его не присоединяют
к продолженной траектории и не удаляют. Автоматического GC нет.

Worker-local scratch и shared staging не заменяют backup. Проверка локального
artifact root не доказывает cross-node/LAN durability или restore на другой
машине. Перенос verified closure в новый scratch root требует отдельной
поддержанной операции P07 import; его нельзя заменить копированием pointer.

Чужие jobs/VM, исходные результаты и диски сохраняют свои identity и владельцев.
Recovery не разрешает удалять failed evidence, форматировать существующие
диски или заменять state/data. Для инфраструктурного restore сначала
устанавливают archive boundary и полный набор зависимых данных; успешный
локальный import не доказывает восстановление сервисов или независимость
внешней backup-копии.

## [Явный выбор exact состояния](@id recovery-selection)

Выберите один root-relative pointer и полную ожидаемую Identity исходной
попытки. В ней должны совпадать execution/point/attempt, branch, model и
frozen-plan hashes. Не подставляйте Identity будущей дочерней попытки.
Вместо pointer можно явно передать ранее сохранённый immutable StateRef.

| Locator | Возможность |
| --- | --- |
| `ATTEMPT/current.json` | Выбранный live manifest и его history frontier; exact recovery доступен только при соответствующем ненулевом checkpoint. |
| `ATTEMPT/recovery/current.json` | Явно выбранный последний exact cutoff после проверки его declaration, зависимостей и native datasets. |
| Immutable StateRef | Фиксированные Identity, state ID, sequence и manifest hash; последующие обновления pointer не расширяют cutoff. |

Owning reader проверяет pointer, hash-pinned manifest, declared payload hashes,
native layout/schema, shapes/dtypes, history reachability и witness ancestry.
Он не ищет `previous.json`, не переключается с live на recovery и не делает
fallback после ошибки. Оператор может отдельно выбрать другой известный
pointer или StateRef; его проверяют заново с собственной исходной Identity.
Pointer, изменившийся во время проверки, вызывает отказ. Отказ не означает
cold start, ремонт pointer или разрешение удалить данные.

Для чтения задают положительный `maximum_metadata_bytes`: это общий allowance
всех metadata reads одного вызова, включая повторные чтения. Streamed hashing
native files, внутренняя память HDF5 и явная загрузка полного solver state —
отдельные расходы. Этот allowance не ограничивает общий размер данных,
память процесса или продолжительность исследования. Fixed-length scalar HDF5
JSON проверяется и учитывается до чтения; неподдержанный variable-length
metadata reader отклоняет до payload access.

## [Передача в новую попытку](@id recovery-handoff)

Текущий Runner умеет открыть `VerifiedExactCheckpoint` и явно загрузить его
public solver state. Чтение не запускает solver. Численную совместимость
problem/options/runtime и восстановление состояния проверяет публичный API
Core; одного успешного metadata read для этого недостаточно.

Для выбора parent в CLI `run-plan` предусмотрены все три параметра вместе:
`--parent-pointer`, `--parent-identity`, `--parent-metadata-bytes`.
Pointer относителен к существующему output artifact root; отдельный identity
file содержит полную Identity исходной попытки, allowance — положительное
целое число. Дочерняя попытка получает больший attempt number, сохраняет
точную связь с parent StateRef и исходные frozen plan bytes. Текущая проверка
parent допускает ровно одну выбранную точку с совпадающими execution/point.
Legacy `--recovery-bundle` отклоняется и не является маршрутом восстановления.

Продолжение stationary расчёта в выбранной версии пока закрыто явным отказом
`native5_final_writer_unavailable` до создания output и compute. Связка typed
writer, Results/AiiDA transport и Core consumer должна пройти собственную
приёмку; перенос в новый scratch требует квалифицированного P07 import.
Поэтому эта глава не предлагает команду для возобновления научного расчёта.
Новая попытка допустима после подтверждения всех этих возможностей и явного
разрешения на её научное исполнение.

В handoff сохраните выбранные execution/point, source StateRef/attempt,
проверенные hashes, identity предполагаемой дочерней попытки и причины
недоступности следующего шага. Успешное открытие checkpoint означает проверку
его объявленной целостности. Научный статус читают отдельно по сохранённому
Core assessment. `not_measured` сохраняет причину отсутствия измерения и не
становится `pass`.

## [Owning справка](@id recovery-owning-references)

Ссылки между Core, Runner и operator относятся к единому bundle; их локальные
цели и anchors проверяет итоговая сборка, после отдельных owning-графов.

```@raw html
<ul>
<li><a href="../runner/user/results.html#operator-recovery-route">Runner: полный маршрут recovery</a> и <a href="https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/c8ac293798b8bd2505fe59063d79077f14d32018/docs/src/user/results.md">закреплённый source этой справки</a>.</li>
<li><a href="../core/theory/12_validation.html#researcher-final-route">Core: чтение финальной точки и критериев</a>. Формулы и пороги принадлежат Core и <a href="https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/46fb51fbd594be80127cf543c7160fc69d8e3b2d/docs/equilibrium-measurement-contract.md">Research contract</a>.</li>
<li><a href="https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc/src/qcl_negf_contracts/artifacts.py">Contracts: artifact format</a>. Эта глава не вводит отдельного формата или критерия научной приёмки.</li>
</ul>
```
