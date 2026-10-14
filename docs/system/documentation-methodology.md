# Методика подготовки документации QCL-NEGF

Статус: предлагаемая адаптация, 2026-10-14. Документация должна позволять
исследователю понять модель и результат, оператору выполнить безопасную
процедуру, разработчику изменить код с известными последствиями. Связный
учебный текст, точная справка и инструкция по конкретной цели нужны каждому
из этих читателей в разных ситуациях.

Основа адаптации — [методика курса Java](https://github.com/BSU-RFCT-Afonenko-Courses/Java/blob/a0d1bdb9d8343809560e3ce7f9a2141d4473ee3f/docs/authoring-methodology.md)
на exact head последнего PR13; она унаследована из PR12. Прочитанная
[глава о методах](https://github.com/BSU-RFCT-Afonenko-Courses/Java/blob/a0d1bdb9d8343809560e3ce7f9a2141d4473ee3f/theory/chapters/methods.qmd)
показывает реализованный подход: знакомый пример развивается, результат
виден, объяснение называет действие и границу переноса. В QCL сохраняется
этот способ изложения. Пять проектов курса, Quarto/QRC и отказ от старых
aliases не становятся обязательной структурой научной системы.

## Связная глава и точная справка

Глава читается самостоятельно. Новый предмет появляется после ясной
потребности: например, спектр допустимых состояний ещё не задаёт их
занятость, поэтому требуется меньшая функция Грина. Необходимые математические
и физические предпосылки объясняются рядом; знакомство с квантовой механикой
не заменяет определения выбранных NEGF conventions. Обозначения, units,
energy zero и порядок индексов сохраняются по всему рассуждению.

Короткое точное правило даёт опору небольшому примеру. Читатель может
предсказать результат; затем видит результат и его причину. Следующий
вариант меняет одно существенное условие, позволяя проверить перенос
понимания. Это последовательность мысли, без обязательных одинаковых
блоков «Правило», «Прогноз», «Причина». Абзац развивает один шаг объяснения;
заголовок называет предмет или механизм. Полнота определяется тем, можно
ли понять вывод без автора, а не квотой слов или числом таблиц.

Формальная reference отвечает на адресный запрос: уравнение, assumptions,
normalization, допустимый input, units, signature, result, effects и errors.
Julia API не пересказывает вывод self-energy; он даёт краткий contract
и canonical equation link. Runbook ведёт к цели с prerequisites,
entry/exit criteria и поведением при отказе. Он ссылается на справку,
а recovery history хранит датированные факты отдельно. Такое различение
соответствует [Diátaxis](https://www.diataxis.fr/start-here/) и не требует
четырёх копий одного текста.

Историю научных и инженерных решений сохраняем там, где она объясняет
действующее ограничение. Старые operational receipts и исходные массивы
не удаляются ради нового оглавления. Стабильные equation/model IDs и
совместимые публичные ссылки меняются только с явной migration.

## Книги статьи и происхождение утверждений

Для содержательного блока выбирается одна книжная линия объяснения,
дополненная первичными статьями для конкретной модели, формулы или
материального значения. Книга помогает выстроить рассказ; сама по себе
она не подтверждает, что solver реализует её approximation. Статья о
геометрии QCL не становится источником всех scattering parameters.

Для каждого существенного input различаются formula origin, value origin
и effective assigning origin. Первые два принадлежат Core/Research,
последний — resolved configuration Runner. Source file с override
объясняет, кто назначил число, но не где оно было измерено. Numerical
tolerance требует основания и роли, а не выдуманной статьи.

Читатель главы получает предметное объяснение и ссылки при утверждениях.
Служебный рассказ «какие источники соединил автор» находится в авторском
source ledger. Там фиксируются издание/DOI, точная глава/страница/формула,
доступная часть, проверенные утверждения и конкретный пробел. Печатная и
PDF-страница различаются. Аннотация и оглавление не выдаются за полный
текст. Практический образец такого разделения есть в актуальном
[Java sources.md](https://github.com/BSU-RFCT-Afonenko-Courses/Java/blob/a0d1bdb9d8343809560e3ce7f9a2141d4473ee3f/docs/sources.md).

Начальная карта источников для автора:

| Источник | Роль и exact scope доступного материала | Следующий пробел |
| --- | --- | --- |
| Datta, Quantum Transport Atom to Transistor; [официальный frontmatter](https://assets.cambridge.org/052163/1459/frontmatter/0521631459_frontmatter.htm) | Кандидат книжной линии: self-consistent field, broadening, coherent/incoherent transport; доступно оглавление, не текст глав | Прочитать выбранную главу легально перед содержательной адаптацией |
| Haug и Jauho; [официальная страница книги](https://link.springer.com/book/10.1007/978-3-540-73564-9) | Кандидат formal conventions; проверены description/TOC | Full chapter и точные equation locators ещё нужны |
| Jirauschek и Kubis; [авторский HTML](https://arxiv.org/html/1412.3563v1) | Прочитаны выбранные II, IV, VIII.2–VIII.4; сравнить модели, cascade и scattering | Eq165 real-space dimensions нельзя без вывода переносить в finite-basis arrays |
| Lee и Wacker; [авторский HTML](https://arxiv.org/html/cond-mat/0212059v1) | Прочитаны II.2 Eq4–10 и II.3 Eq11–16 | Diagonal dominance, discarded principal value и representative k не объявлять exact contract текущего Core |

Это список доступа и кандидатов, а не удостоверение прочтения полных книг
или проверки всей физики. Если конкретный пробел не закрывает открытая
первичная статья, запросить нужный chapter/library access; не покупать
и не устанавливать материалы автоматически. Пересказ сохраняет attribution,
точная цитата оформляется отдельно с соблюдением условий источника.

## Документация рядом с кодом

Короткие facts следует хранить в source владельца и генерировать представления.
Длинный вывод и архитектурное «почему» остаются в owning Markdown chapters.
Предлагаемые средства ниже оцениваются одновременно; это кандидаты,
не поручение установить весь набор.

| Source of truth | Представление и граница |
| --- | --- |
| Julia docstrings и types | Существующий [Documenter](https://documenter.juliadocs.org/stable/man/syntax/) через @docs/@autodocs; units, effects, equation links. [Doctests](https://documenter.juliadocs.org/latest/man/doctests/) только bounded; экспортная coverage не вся expert семантика |
| Python docstrings/type hints | mkdocstrings + [Griffe](https://mkdocstrings.github.io/griffe/guide/users/loading/) со static AST и allow_inspection=False. Альтернатива [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) требует gate на imports, side effects и locked dependencies |
| FastAPI routes/models/Field descriptions | Существующий authenticated OpenAPI (api.py:255–257); [route metadata](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/) дополняется source-level bounded schema export, без старта service |
| TS JSDoc/TSDoc | [TypeDoc](https://typedoc.org/documents/Doc_Comments.html) для выбранных public exported interfaces; UI internals не требуют отдельной энциклопедии |
| Contracts JSON Schema descriptions/examples | Generated field reference; normative schema не копируется вручную. Runner typed values и effective origin остаются отдельными facts |
| Nix mkOption descriptions/type/default/example | Locked-version nixosOptionsDoc; [код генератора](https://github.com/NixOS/nixpkgs/blob/master/nixos/lib/make-options-doc/default.nix) сам содержит описание option→docs механизма; master не runtime pin |
| OpenTofu variables/outputs descriptions | Кандидат [terraform-docs](https://terraform-docs.io/reference/terraform-docs/) для module tables/output check; совместимость с выбранным OpenTofu проверяется отдельно |
| Canonical example source | Включать исходник по ссылке/include, не paste copies. [Literate.jl](https://fredrikekre.github.io/Literate.jl/v2/) — кандидат для commented Julia→Markdown; выполнение явно bounded. Quarto code evaluation выключено по умолчанию в предлагаемом docs пути; frozen output имеет provenance |

Изменение поведения сопровождается правкой owning docstring/schema/example
и targeted check. Generated HTML, signature tables и model cards не
редактируются независимо. Генератор не проверяет физическую правильность,
architecture intent, error semantics или соответствие статьи реализации.
Для этих связей сохраняются stable IDs и содержательная review.

## Учебный образец малости смешанного шага

Следующий фрагмент — аналитическая иллюстрация, без измеренного solver run.
Его фиксированный масштаб объясняет отношение двух величин и не заменяет
production definition residual.

Малый шаг самосогласования может означать осторожное смешивание. Чтобы
понять, насколько состояние удовлетворяет уравнению, сначала сравним его
с кандидатом, который это уравнение строит. Обозначим текущую собственную
энергию через $\Sigma_n$, а результат одного отображения SCBA — через
$F(\Sigma_n)$. При линейном смешивании с $0<\alpha\leq1$

$$
\Sigma_{n+1}=\Sigma_n+\alpha\bigl(F(\Sigma_n)-\Sigma_n\bigr).
$$

Возьмём одну и ту же норму и фиксированный положительный масштаб
$S=100\,\mathrm{meV}$. Для иллюстрации определим
$r_{\mathrm{raw}}=\|F(\Sigma_n)-\Sigma_n\|/S$ и
$r_{\mathrm{step}}=\|\Sigma_{n+1}-\Sigma_n\|/S$.
Оба отношения безразмерны. Однородность нормы даёт
$r_{\mathrm{step}}=\alpha r_{\mathrm{raw}}$.

Пусть кандидат отличается от текущего состояния на $10\,\mathrm{meV}$
по этой норме. Тогда raw residual равен $0.1$. При $\alpha=0.01$
шаг имеет норму $0.1\,\mathrm{meV}$, а его относительная величина — $0.001$.
Состояние мало изменилось потому, что взята одна сотая предложенной поправки.
Это вычисление ничего не говорит об уменьшении raw residual после шага.

Изменим только $\alpha$ на $0.5$, оставив то же состояние и кандидат.
Шаг теперь равен $5\,\mathrm{meV}$, его отношение — $0.05$; исходная
невязка по-прежнему $0.1$. Следовательно, величина шага зависит от
алгоритма смешивания. Для проверки уравнения нужна свежая невязка
в проверяемом состоянии, а для outer solve — согласованные U/G.

Это равенство выведено для scalar linear mixing и общей фиксированной
нормировки. Его нельзя автоматически переносить на Anderson/Pulay,
state-dependent denominators или все native metrics. Универсального
допуска здесь нет. [Численная политика Core](../../components/QCLNEGF.jl/docs/src/physics/numerical-policy.md)
и [паспорта критериев](../../components/QCLNEGF.jl/docs/src/theory/12_validation.md)
задают реальные definitions и границы. Даже малая raw residual ещё не
доказывает достаточность дискретизации или экспериментальную валидацию.

## Приёмка текста

Пробный срез должен дать полную самостоятельную главу, отдельную точную
reference и один исполнимый по условиям runbook. Независимый читатель
объясняет результат примера и границу его переноса, находит public symbol,
units, источник и failure condition. Все три reader journeys проверяются
без обязательного линейного чтения всей документации.

Примеры явно имеют статус analytic, illustrative или measured. Measured
пример связывает output с source/model/plan/artifact; иллюстрация не
становится научным свидетельством. Static link/format checks отделяются
от docs build, чтения HTML, offline/light checks и scientific acceptance.
Временная draft версия не объявляется окончательно принятым учебником.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Rule и развивающийся пример дают применимый стиль | Exact Java методика и methods chapter | Их предмет и инфраструктура отличаются от QCL | Сохранить |
| Facts можно приблизить к коду | Existing Documenter/OpenAPI и candidate generators | Generated signature не доказывает семантику | Изменить |
| Книги и статьи имеют разные роли | Author source/access ledger | Полные книги ещё не прочитаны | Дополнительно измерить |
| Малый смешанный шаг не равен raw residual | Аналитическая формула при явно заданных условиях | Не numerical verdict существующего S01 | Сохранить |
| Полнота будущего учебника ещё не установлена | Нужен пробный срез и независимый read-through | Нет общей published reader acceptance | Данных недостаточно |
