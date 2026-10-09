# DOC01/DOC02: границы SCBA и optical response

Owning draft PR: [Core #4](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/4). Изменены только
два абзаца owning документации Core; итоговый source определяется gitlink этого интеграционного
commit.

`09_scba.md` уточняет, что approximate early return inner SCBA требует одновременно
`adaptive_working` и enabled `diagnostic_quality`. `research_continue+enabled` этого выхода не
получает. Подтверждение outer Poisson и final snapshot остаются отдельными проверками со своими
исходными строгими условиями.

`18_optical_response.md` ограничивает отсутствие e–e выбранным baseline. Core поддерживает
stationary SPPA; optical API может читать такой Green state. Приближение bare bubble, `δΣ=0` и
отсутствие vertex corrections сохранены. Это уточнение возможности API, а не доказательство точности
SPPA или gain.

## Свидетельства и ограничения

Два файла: 18 вставленных и 10 удалённых строк. Code, model, defaults, tolerances, сетки, все fenced
formulas, наборы ссылок и assets не изменены. `git diff --check` и сравнение fenced blocks/refs с
исходным Core source прошли. Независимый static review frozen bytes не обнаружил блокирующих
замечаний. Public diff audit не обнаружил известных секретов и private endpoints.

Deno formatter сообщает одинаковые два неформатированных файла до и после правки; исходный
Documenter style сохранён. Проверка формата не объявляется успешной. Documenter build/render и
numerical tests не выполнялись: runtime budget этого docs-only ticket — 0. Existing paper-dependent
числа в соседнем тексте сохранены, первичные статьи заново не проверялись.

SHA256 frozen diff: `ddf0b55c63869e59bf3d61d5f0ac5aaa6d8eeb3fe94e3190d21282dcb90ec1c3`.

| Утверждение                                    | Свидетельство                                                 | Ограничение                      | Решение             |
| ---------------------------------------------- | ------------------------------------------------------------- | -------------------------------- | ------------------- |
| Документация соответствует условиям inner SCBA | Core acceptance/stop functions и два reviewed paragraph hunks | Static source review             | изменить            |
| Baseline e–e и SPPA capability разделены       | Defaults, kernel dispatch и optical API                       | Без quantitative gain validation | изменить            |
| Физический контракт сохранён                   | Code diff пуст; fenced formulas/refs совпали                  | Не numerical acceptance          | сохранить           |
| Научная приёмка установлена этой правкой       | Новых numerical evidence нет                                  | Docs-only scope                  | данных недостаточно |
