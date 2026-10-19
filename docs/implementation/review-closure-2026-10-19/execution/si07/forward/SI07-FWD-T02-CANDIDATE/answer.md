Архивный source установлен только по заявлению receipt; научная приёмка по этим файлам не установлена.

1. **Source и identity.** В `archive-receipt.json#/archive_source` указаны root `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8` и Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`. Именно их следует связывать с архивом. В `current-checkout.json` другие ревизии: root `965ebed95d2b627423805d10c46d0ae8dd425e9d`, Core `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`; файл прямо обозначает текущий checkout, а не producer receipt. Содержимое исходников и gitlinks здесь не предоставлено, поэтому независимой проверки происхождения нет.

Receipt задаёт `execution_id=SI07-public-E`, `attempt=2`, `state_id=SI07-public-state`, `state_sequence=3` и `plan_fingerprint=cc502a4746c8985c9bfbe6ab9043718889533612a676d7786e38fa278c887e7d`. Это заявленные идентификаторы; sequence 3 не доказывает число итераций или финальную сходимость. Нет истории других attempts и состояний.

2. **Final state.** `archive-receipt.json#/final_owner` объявляет `physics.h5`, но `present_in_packet=false`, `bytes=null`, `sha256=null`; также `raw_payload_present=false`. Следовательно, файл отсутствует в предоставленном пакете. Из этого нельзя заключить, что он не был создан при расчёте. Размер и hash неизвестны, а не равны нулю. Нельзя проверить целостность, native schema, committed/final status, согласованность U/G, restart-пригодность или содержимое массивов.

`process_exit_code=0` подтверждает лишь записанный нулевой код завершения процесса. `producer_assessment=not_measured` следует сохранить буквально: это не `pass`, не `fail` и не `not_applicable`. SCBA/Poisson-сходимость, физические gates, достаточность дискретизации и экспериментальная валидация остаются неизвестными.

3. **Равновесная приёмка.** `frozen-plan.json` заявляет вопрос «equilibrium 0mV per period 70K», каналы LO, acoustic, impurity, IFR, alloy и `electron_electron=none`. Сам файл помечен как synthetic metadata, не executable plan. Это описание намерения, а не доказательство фактической конфигурации. Один нулевой bias не доказывает равновесие: нужны согласованные chemical potentials, температуры контактов и baths, граничные условия и отсутствие другого drive. Их нет.

Нет наблюдаемых для проверки равновесного FDR/current oracle и нет архивных определений критериев, нормировок, весов, единиц, допусков и поведения около нуля. Поэтому нельзя назначить универсальный порог тока или вычислить относительную ошибку относительно нуля. Также нельзя независимо связать сокращённый frozen plan с указанным fingerprint без полного канонического плана и правил его хеширования.

Минимальный следующий шаг — предоставить существующий `physics.h5` с размером/hash и native contract/schema, полный frozen plan/model identity и историю/финальные witnesses того же execution, attempt и state. Для интерпретации нужны совместимый reader подтверждённой версии и owning acceptance definitions архивного Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, в частности `src/numerics/reference/acceptance_metadata.jl::_acceptance_metric_metadata` и `docs/src/theory/12_validation.md` (их наличие и содержимое на этой ревизии сейчас не проверены). Это позволит проверить существующий результат без нового расчёта.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Архиву заявлены исторические root/Core | `archive-receipt.json#/archive_source` | Нет независимой проверки producer source | Сохранить |
| Текущий checkout отличается | `current-checkout.json` против receipt | Не определяет содержимое архива | Сохранить |
| Объявлен final owner `physics.h5` | Receipt: файл не в пакете, bytes/hash неизвестны | Final state и целостность не проверены | Данных недостаточно |
| Process exit записан как 0 | `#/process_exit_code` | Научная приёмка не следует из exit code | Сохранить |
| Producer assessment — `not_measured` | `#/producer_assessment` | Ни успех, ни физическая ошибка не доказаны | Сохранить |
| Равновесная приёмка возможна как отдельная проверка | Заявленная постановка 0 mV/period, 70 K | Нет условий равновесия, критериев и payload | Данных недостаточно |

Выполнено только чтение разрешённых метаданных и frozen skills; тесты, solver, сеть и изменения repo не выполнялись. CPU/RSS не измерялись. Аудит операций: `/tmp/qcl-si07-forward-fresh/SI07-FWD-T02-CANDIDATE/operations.json`.
