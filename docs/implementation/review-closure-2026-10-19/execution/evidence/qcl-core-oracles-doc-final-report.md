# Core oracle owning document — final factual status update

Автор `/root/oracle_carrier_design`, ultra, 2026-10-19. **FROZEN, STOP**.
Единственный изменённый Core path:
`docs/src/development/review_oracle_contracts.md`. Производственные source,
tests, equations, methods, input/expected arrays, code fences, tolerances,
physical criteria, resource limits и S1 не изменены. Git, Julia imports,
tests/runtime, solver, build, SSH и новые design work — 0.

## Frozen incremental artifacts

| Artifact | SHA256 |
| --- | --- |
| Before owning document | `61508afc44b57954b2d1c5d843c333aa8fb4a14fb9a1b1ffa811afc0798fece3` |
| Final owning document | `673bc9641318b01ffe29bcbe6edc6198b5e243a0d246af8072a2190a70e072f2` |
| `/tmp/qcl-core-oracles-doc-status-only.diff` | `140fab36e6a16c77e44fe25842a59ca7f4d847f057e69e83f2b7035dcdeab7cf` |

Before snapshot сохранён `/tmp/qcl-core-oracles-doc-before.md`; incremental
diff создан plain `diff -u`, не Git. Изменены только readiness/status,
фактические observations и receipt identities. Все17 fenced blocks
сравнены byte-for-byte через awk/cmp: одинаковы. Whitespace scan пуст.
Формулы/таблицы current/Poisson/kernel/PV arithmetic и code predicates
сохранены. DEV05/07 остаются design_blocked, six-oracle readiness не заявлена.

## Основание status updates

- TEXT/DESIGN PASS owning61508… и ratio CP-DESIGN PASS review
  `374672b3d4cce86fd8f1272c9464d0c72ddc52a89b5f6272300ebdcd06567238`.
- Final CP-CODE PASS review
  `2cc83ef336d85cd96d0b9e3dde9b6f677524d8f8dacde8379b4c422f9b459f98`.
- Прочитаны root raw receipt.json/original.log для всех четырёх текущих
  attempts; все exit0/rawcomplete=true/stopnull с matching fixture hashes.
  Автор тесты не повторял. Owning document теперь self-contained: полные
  fixture/review/raw receipt/log hashes и counts, без /tmp normative inputs.

| Card | Attempt | Assertions | Fixture SHA256 |
| --- | --- | --- | --- |
| DEV03 | GREEN2 | 16/16 | `6adaeea85abf95e21dd0beb763dada3a73d588cae1ed5a5d536eb0e8841a2a1e` |
| DEV04 | GREEN2 | 183/183 | `9aab7a4eea3a7fcb93033d2c9f6f3b420f6b1872843168e0deb98461f2602730` |
| DEV06 | GREEN1 | 248/248 | `17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01` |
| DEV08 | GREEN2 | 211/211:13 literal+198 continuum/scalar | `4533b1058eb351d5796df18c86ac3b2e2af767078e16bd4cec25588b8e34f70a` |

658 — сумма targeted assertions, не fullsuite/fullCI/coverage/scientific
acceptance. DEV04 GREEN2 теперь является runtime witness exact-ND fatal
guard перед двумя direct5×5 Poisson calls и synthetic construction для
конкретного frozen carrier; не обещает это для иных inputs. Historical
review's not_measured и original failed GREEN1 artifacts не переписывались.
В owning O08-06 сохранён весь прежний failure observation GREEN1 (13/13,
107 pass/1 fail, exit1 и original hashes), рядом добавлена текущая GREEN2
evidence; failure не превращён в pass задним числом. ATOL=RTOL2e-13,
derived ratio proof и separate sign/amplitude/positivity controls сохранены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning pending statuses устарели | Accepted374672…/2cc83ef… и matching root logs | Только bounded selected fixtures | изменить |
| Методы/уравнения/допуски требуют новой правки | Incremental diff factual-only;17 fenced blocks byte-equal | Source/design не пересматривались | сохранить |
| Targeted runtime прошёл | Четыре raw logs,658 assertions, fixture identities | Не fullCI/SCBA/science | сохранить |
| Full model/scientific acceptance завершена | Требуемых coupled/absolute/scientific свидетельств нет | DEV05/07blocked,S1 unchanged | данных недостаточно |
