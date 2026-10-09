# S01: локальные проверки операторов Core

Проверены исходники Core `3108150dd1b6b1377470b384b15c26e272fe5c5d`,
выбранные gitlink корневого проекта. Изменений физической модели, сеток,
рассеяния или допусков не было. Новые SCBA/Poisson расчёты не запускались.

| Проверка | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Аналитические равновесные anchors | `test/physics/analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl`: 11/11 assertions | Скалярные KMS, представленное конечное окно sum rule, LO balance и manufactured zero-current reservoir | сохранить |
| Production LO discretization | `test/physics/production_lo_equilibrium_discretization.jl`: 14/14 assertions, восемь конечных contractions | Целые и дробные energy shifts; refinement ordering. Самосогласованного решения нет | сохранить |
| Выбранный runtime | Julia 1.13.0, проверены `pathof`, версии и SHA исходников внутри успешных вызовов | Использован существующий локальный cache; cold build не проверен | сохранить |
| Научная приёмка S01 | Новых nonlinear attempts и final scientific artifacts нет | Эти проверки не устанавливают сходимость SCBA/Poisson, достаточность campaign grids или экспериментальную валидацию | данных недостаточно |

Пакет включал три вызова с общим пределом 360 s. Первый завершился до
включения тестов из-за ошибочного прямого импорта Roots в wrapper корневого
Project. После адресного исправления wrapper два целых test files прошли;
исходники и зависимости проекта не менялись. Фактическое суммарное время —
189.09 s, вывод — 4313 bytes, новых массивов результатов нет.

Исходный отказ и предупреждения Julia `StyledStrings → Markdown` сохранены
в локальных логах. SHA-256 успешных логов:
`361fa2b7f20fbdd6c45e4f341da79361e04ff1c2a5fdc4138ef9add92d0a433c`
и `a5ea0403955161aed713f9b5305228cb687f529d265a4737f77d42685eed4b01`.
Полные численные residual values этот пакет не сохранял; повторных
contractions ради их вывода не выполняли.

Windows/Hyper-V boot/network проверка I07 недоступна: пользователь подтвердил
отсутствие Windows-хоста. Её статус — `not_measured`. Наличие Linux tools
на ноутбуке не заменяет boot/network приёмку libvirt: `/dev/kvm` и доступный
libvirt socket не обнаружены. Проверки отдельных backend остаются отдельными
от приёмки Proxmox и научной приёмки.
