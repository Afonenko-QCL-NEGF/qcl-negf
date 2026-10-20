# I2I: focused native TAP parser conformance

**Source candidate; STOP fresh independent high CPP.** Изменены только
ops/docs_tests_native.py::validate_unit_report и focused literal fixtures в
tests/test_docs_test_native.py. Worktree HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; Root107 — отдельный контекст Root.

Accepted I2H review SHA256
`c5ceb1df3d7ac2c99352b7bf67dde0c1f8a928485cfd430a5a43d456cb01ee7c`
сверен. Перед изменениями exact четыре I2H файла скопированы в
`/tmp/qcl-docs-routing-i2h-before-i2i`; manifest.sha256:4 OK. Backup меньше4MiB.
Substantive TAP correction design-v1, pure FORMAT3 final-v8 review и actual
native production reader прочитаны. Старый DESIGN_ONLY scope не использован
как grant: реализация разрешена новым focused поручением Root.

Fixtures написаны перед production correction; собственного исполнения RED/
GREEN нет. Pure parser не импортируется и не служит shared oracle. Literal
Node TAP13/Deno TAP14 inputs и ожидаемые typed summaries заданы независимо.

Изменение reader узкое:

- positive safe-integer expected, включая отказ bool/float/zero/overflow;
- result-only anchored case-insensitive standalone SKIP/TODO directive gate;
  ASCII word boundary соответствует указанному JS regex, включая SKIPé;
  aggregate zero counters и названия skipped/todo без directive проходят;
- Deno требует ровно один immediate literal header
  `# ./tests/docs_static_slice_test.ts` после version14. Caller-controlled path,
  headerless/foreign/repeated/misplaced header и arbitrary comment не допускаются;
- единственная exact plan, contiguous exact result IDs/count; дополнительная
  несовпадающая plan теперь также отвергается;
- existing Node seven exact counters tests/suites/pass/fail/cancelled/skipped/
  todo сохраняются обязательными ровно по одному, включая zero skipped/todo.

API unit/capture и typed summary shape не менялись. Existing Python unittest
fixture expected20 и его return expectation сохранены. Existing TAP stderr,
version/full-layout и failed-result gates сохранены; новая result directive
проверка не подменяет counters blanket regex. Остальная parser architecture,
descriptor/route, B3/B4 mechanics и acceptance status не менялись.

Добавленные paired controls: healthy Node zero counters; healthy exact Deno
header; mixed-case SKIP/TODO с/без reason и tab; ordinary skipped/todo names;
missing/duplicate/nonzero каждого из7 Node counters; headerless, foreign,
absolute/file URL, repeated, misplaced, other selected file и unknown comments;
stderr, bailout/not-ok, missing/extra/conflicting plans; two-result positive
и same-count duplicate/reordered/gapped IDs. Deno early plan после header
остаётся positive: новая позиционная норма plan не вводилась.

Выполнены source/hash/Git reads, frozen manifest4 OK и diff --check двух changed
paths без whitespace diagnostics. Nominal8 Python methods и8 Deno registrations
сохранены. TS pair frozen I2H; pure pair/config/ops/git/Git index/CP не менялись.
Scripts/parser/import/compiler/formatter/linter/tests/solver/native/network/
CI/science executions0, children0. Product90/source11 unchanged, E1unused.
Math97PASS/PR10G1 — контекст поручения Root, здесь не переаттестован.
Не заявлены native READY, cause RSS fixed или S1.

Полный I2H→I2I delta7885bytes, SHA256
`6e5c13053e11044f2c9f46b1d7788ec2fc8239d6643983d6877c6d95de4f8c85`.
Exact old4/new4 manifest — companion identity. Historical failures не удалялись.

Поручение12min/1CPU/1GiB/read≤2MiB/output≤64KiB. Два ранних bounded content
selection дали truncation. Exact aggregate transcript/I/O counters не снимались.
Повторные full-file diff/check/hash reads могут превышать cumulative2MiB cap,
если считать каждое перечитывание; соблюдение этого cap **не заявляется**.
CPU/RSS/physical I/O и exact output bytes не измерялись; complete envelope
compliance не сертифицируется. Дополнительное target execution ради измерений
не выполнялось. Дальнейшие source reads остановлены, только fresh high CPP.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Native ready TAP defects исправлены | Узкий reader diff и literal paired controls | Source-only, controls не исполнялись | дополнительно измерить |
| Python20 и typed summary сохранены | Existing fixture unchanged; literal Node/Deno expected summaries | Нет runtime acceptance | сохранить |
| I2H/B3/B4/provider gates закрыты этим packet | Не менялись | Отдельные прежние remaining gates | данных недостаточно |
| Native READY/RSS cause/S1 доказаны | Нет таких execution/evidence | Source gate их не подразумевает | данных недостаточно |
