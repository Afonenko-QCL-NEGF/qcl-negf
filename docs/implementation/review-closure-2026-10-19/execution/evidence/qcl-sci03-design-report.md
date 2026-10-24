# SCI03-D1 — отчёт для независимого CP-DESIGN

2026-10-19. D / Sol ultra. **Design candidate завершён; independent review ещё
не выполнен.** Никакого CP-SCI READY, scientific acceptance или native admission
этот report не устанавливает. Код/components/root coordination не менялись.

## Передаваемый immutable candidate

- `/tmp/qcl-sci03-design.md`: **40 020 bytes**, SHA256
  `ceffa4f2ca941510451f1d28a9f0cbaff7277e10411230c0b1dc8ab26c649509`.
- Разрешённые deliverables ровно два: этот design и данный report. Новые PDF,
  scripts, arrays, fixtures, архивы, package environments или commits не созданы.
- Role/model/limits получены от координатора: SCI03 D ultra, source/literature/
  arithmetic ≤2h/1CPU/2GiB/output256KiB, максимум2 design review rounds. Independent
  review rounds ещё не использованы. CPU/RSS не инструментировались и не
  называются measured resource profile.

Source binding:

| Источник | Фактический commit / состояние |
| --- | --- |
| Managed root | `7d179b28647f0b89347d2d6358f08cf2fe479653`, `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` |
| Core | `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, status clean |
| Research | `b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3`, status clean |
| Results | `17574ca4c5495f74d86ed9bef51c60dea8265062`, status clean |
| Root concurrent overlay | Modified Runner/Portal gitlinks; dirty AiiDA/Platform internals; checkpoint and unrelated execution evidence/tests. Сохранены, не включались в этот task |

Полный `git submodule status --recursive` прочитан. Выбранные Core/Research/Results
совпали с task brief. Source hashes14 owning files проверены непосредственно
по bytes и перечислены в design. SCI02 паспорт прочитан в опубликованном owning
Research; `/tmp/qcl-sci02-primary-audit.json` и `/tmp/qcl-sci02-report.md` были
метаданными контекста, не приняты вместо published source.

## Что сделано и почему это полезно

1. Разведены exact equilibrium targets и finite numerical accuracy. Сохранены
   все strict tolerances, actual unweighted/weighted norms, denominator floors,
   near-zero branches, applicability и значения пяти уровней verdict.
2. Primary FD (Smirnov2.30–31), FDR (Fotso–Freericks42), DOS (Lee–Wacker B2),
   current/full-coherence/finite-basis caveat (Wacker2–6) прочитаны и привязаны
   к exact primary/source hashes. Bosco70K/200K и dose-caption conflict сохранены.
3. Выведены полезные deterministic coefficients: μ-bracket→FDR
   `√2/(4kBT)≈58.61166754 eV⁻¹`, same-basis number/density trace bounds,
   абсолютный per-side represented current bound через Green и selfenergy FDR
   defects. Эти bounds не используют arbitrary tolerance или division/J=0.
4. Бюджет deterministic errors складывается с коэффициентами1 по triangle
   inequality. Нет выдуманных fractional allocations и RSS independence.
   Каждое missing remainder/conditioning значение остаётся unknown.
5. Каждому unresolved member assigned конкретный existing S1 slot. Отмечено,
   что C[−.30,1.20] и W[−.45,1.05] — разные окна, поэтому C−W нельзя объявить
   чистым k-cutoff error без общих domain/tail/interaction bounds.
6. Predeclared H protocol — **+ΔE/4 phase** выбранного разрешённого single
   final variant, новый plan/state, та же physics/mesh density/strict criteria.
   H не используется для tuning; новая acceptance version после pilot требует
   независимого held-out свидетельства. Это предложение CP-DESIGN в пределах
   разрешённого H initial/phase protocol, не уже выполненный freeze/submit.

## Проверки самого candidate и ограничения

Выполнена адресная проверка документов Python standard library, без импорта
продукта/NumPy/Julia и без запуска C08 или другого runtime:

- 14 source SHA256 совпали с таблицей design; all source paths существуют.
- 8 Markdown tables имеют согласованное число columns: 3/3/3/4/3/3/2/4;
  91 rows всего; 14 code-fence lines сбалансированы, trailing whitespace нет,
  файл заканчивается ровно одной newline.
- Exact arithmetic двух real 2×2 controls на `fractions.Fraction` проверила полную
  matrix identity §5.3: thermal zero-defect даёт trace0/bound0; noncommuting
  defect даёт trace `−860681/1108800`, upper bound≈2.243894493536362. Это
  проверка собственной algebra design, **не** product test/physical solution.
- Пересчитаны точными SI ratios kBT70K=.006032133283501625eV и μ coefficient,
  physical conversions strict rU/rλ/neutrality, PSD64Nb·eps coefficients.

Первый formatting check обнаружил неодинаковое число столбцов strict-norms
table `[3,3,2,...]`: separator без пробела был ошибочно преобразован в mathematical
bar при экранировании `|` внутри формул. Исправлены только эти separators;
повторная проверка таблиц/source hashes/algebra exit0. Это documentation defect,
не numerical red/green test. Исходная причина/текст отказа сохранены здесь;
дополнительный failed-log файл не создавался по output-only контракту.

Primary retrieval failures также сохранены: sandbox FD/FDR
`URLError: Temporary failure in name resolution`; allowed network FD прошёл,
initial FDR read отказал `source exceeds 1 MiB read cap`; после установленного
размера один corrected4MiB bounded read получил1195786 bytes и Eq42 сp.8.
HTTP bytes держались только в памяти. FD HTML hash получен с того же primary URL;
его непрерывный string check `(2.30)/(2.31)` дал false из-за HTML-разметки,
формулы/номера независимо прочитаны web tool на primary page. Материал/formula
не выдуманы по этой failed string heuristic.
Точные primary hashes и limitations в design§2. New network body bytes вместе
с discarded partial FDR read:2 257 333 (<128MiB literature ceiling).

**0 scientific attempts, 0 solver CPU-hours, 0 Julia/product imports/test/builds,
0 server probes/benchmarks/install/fullCI.** Новые numerical data не создавались.
Старые S01 raw/run/attempt и protected checkout не читались. Fresh native
admission отсутствует; читаемые local source и primary articles её не заменяют.

## Научные blockers, которые нельзя назвать pass

Нет finite target εη/εμ/εn/εsheet/εU/εJ_abs, выведенных из intended distinguishing
scale; identities с exact0 не задают единственный finite tolerance. Existing
project residual thresholds — необходимые policy gates, не общий error bound.
Не установлены нелинейный inverse-map/contraction bound, continuum energy/k/qz
tail remainder, basis-period truncation и mixed cutoff/window interaction bounds.
Двух сеток на ось и одного H недостаточно, чтобы автоматически доказать эти
остатки. Полная numerical accuracy/physical acceptance поэтому остаётся
`данных недостаточно`. Никакие thresholds не ослаблялись.

Известные локальные bounds §5 могут быть измерены finite pilot после закрытия
source/oracle/admission/guards/plan gates. Его назначение — получить недостающие
коэффициенты/диагностику, не принимать себя задним числом. Если evidence не
даёт bound в разрешённом каталоге, конечный честный результат — остающийся gap;
дополнительные executions не добавляются молча.

## Next-ready и review request

Независимый R получает только immutable design bytes/hash, поставленный вопрос,
объявленную модель и первичные source locators. Он должен проверить formulas,
строгость норм/thresholds, scientific unknown semantics и допустимость H phase
в существующем S1. Автор не закрывает свой CP-DESIGN. Успешный review этого
design разрешает owning docs/reducer contracts; не принимает численное решение.

После review ready source/design tasks: SCI04/O08-03 final-U/G-density audit,
SCI06 reducer для §5.3 coefficient measurements с literal independent oracle,
SCI12 mapping/tail/interaction/H details, SCI03-ACC finite target basis.
SCI07/08 guards/admission и SCI09 frozen plans блокируют pilot launch; это не
повторный вопрос пользователю о уже утверждённых S1/B/G1 правах.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SCI03 имеет concrete reviewable design | Exact file/hash, primary/source formula chain, static/algebra checks | Independent CP-DESIGN ещё нужен | изменить |
| Existing physics и strict gates сохранены | Fourteen source hashes, explicit actual thresholds/norms | Runtime plan/state не создан | сохранить |
| Дополнительные scalar coefficients не произвольны | μ derivative, trace/Cauchy bounds и exact2×2 check | Все относятся к указанной represented domain | сохранить |
| S1 уже physical accepted / native READY | Source-only design, missing finite targets/bounds/admission | Solver/physical/discretization evidence отсутствует | данных недостаточно |
| Pilot и H могут закрывать gaps автоматически | Finite approved slots и predeclared measurement protocol | Нет гарантии bound/сходимости; no retroactive threshold tuning | дополнительно измерить |
