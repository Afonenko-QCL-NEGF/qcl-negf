# RV01 · Независимый review

Blind первичные выводы сохранены в `RV01-blind.md` до чтения candidate. Denominator: пять saved files, пять gate JSON pointers, source/installed/imported identity, plan/run/attempt/raw completeness и пять evidence levels. Review metadata-only; source bytes не менялись; originals cumulative I/O 250 432 bytes (<256 KiB), arrays/archives/imports/live runtime не читались. Прочитанный candidate SHA256 `46c526814765da9010ff9eb90afff9f74f3e3e0882f84f37f73d05e0f4d3a598`; review соответствует Candidate 2026-10-14 17:44–17:47 UTC.

**Verdict:** пригоден как bounded metadata passport с двумя неблокирующими wording замечаниями; физическая/численная приёмка не установлена. SHA256 пяти files и five receipt pointers независимо совпали. Plan schema/model_revision/computation_count, submit run UUID/plan fingerprints и derived attempt/status подтверждены первичными selections. Original transport decoded 22 339 bytes и содержит run UUID; полное сравнение `/aiida/CalcJob`/`plan_sha256` reviewer заново не выполнил в оставшемся I/O envelope. Эта независимая глубина явно ограничена; авторский detailed original linkage остаётся source-located assertion, не second independent measurement.

| Severity / locator | Finding | Исправление |
|---|---|---|
| P3 · `RV01.md` финальная таблица, строка «S01 одна попытка известного frozen plan» | Selected evidence устанавливает observed attempt=1, но не отсутствие других attempts до/после сохранённого status. Текст выше честно ограничен saved slice, заголовок claim может читаться сильнее | «Известна attempt 1 S01 с данным frozen plan» |
| P3 · `RV01.md` финальная таблица, строка «Научная приёмка установлена» | Row evidence=false + decision недостаточно корректен по смыслу, но формулировка assertion звучит противоположно | «Scientific acceptance не подтверждена выбранными данными» |

Reader source locators существуют: Results commit `fe27a2a9ed065f9afacecc84113311f30d0c68d6`, `multipart.py::_validate_part_set/_validate_receipt`, `native.py::validate_native_handle`, `model.py::canonical_bytes/validate_model`. Читались адресные source checks, не выполнялся reader/import. Версионная оговорка legacy multipart/native корректна. Разделение metadata integrity и истинности producer statements сохранено; installed label не выдаётся imported source commit. Самый дешёвый следующий шаг — exact terminal receipt+raw closure без нового solve.

M06/M18/M19/M20 применены локально: пять metadata originals не scientific closure; `not_measured` не pass; allocated resources не telemetry. Role actions researchers/operator/developer обозначены; imported/raw missing не скрыты. Отчёт секционно <8 KiB, ссылки cards/receipt существуют. Blind независимость ограничена собственным finite I/O cap, не согласованием с автором.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Technical ready/open/completed при scientific=false и CI=false | SHA `4c8e877…`, пять exact receipt pointers | Saved producer claims, не runtime сейчас | сохранить |
| Run UUID/plan fingerprints и observed attempt1 согласованы | SHA plan `4d69332…`, submit `bd40aaa…`, derived status `d6a022f…`; blind selections | Не доказывает отсутствие других attempts; original detailed linkage partially sampled | изменить |
| Terminal convergence/physics/discretization/experiment неизвестны | Выбранные metadata без final matrices/refinements/experimental evidence | Нет численного verdict | данных недостаточно |
| Повторный submit не восстанавливает старую provenance | Exact saved identity required | Terminal/archive closure ещё missing | сохранить |

## Round1 scoped recheck

Перечитаны только два final-table labels нового candidate SHA256 `85cb1310d13328ccf96d61f5f106bf671c72130b3d3a97f775b924995f6784c3`: «Известна attempt 1 указанного frozen plan» и «Научная приёмка не подтверждена». Оба P3 закрыты; primary originals не перечитывались. Metadata passport verdict сохранён; предел независимого original-linkage review прежний.
