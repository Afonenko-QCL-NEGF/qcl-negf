# DEV13 RED-3 — queued reader close lifecycle, tests-only

Independent R4 review `/tmp/qcl-dev13-green2-review.md` SHA256
`96ccd6d0368cf8e078cd2589615b1a257d60090eabcaee241e9719d8cac3abc4`.
Root GREEN2 receipt `167passed`, wall9.738s/RSS201035776/log260B/stopnone,
`/tmp/qcl-DEV13-GREEN-2`. Это baseline existing denominator, R4 им не покрыт.
Root explicit finite extension: RED3+GREEN3,90s each, DEV13 total6/540s;
implementation/test execution остаётся на root; мной runtime не выполнялся.

## Freeze

Только `tests/test_actor_deadlines.py` изменён после GREEN2:
SHA256 `3eeb041b5d673e5e3fbdc5d48cbc094c91874a9fc2610a3b24022c62011b1f37`.
Incremental `/tmp/qcl-dev13-red3-tests.diff` SHA256
`8c3adb152763b4b09ef007282fb1f4d29f601cac483560cd24a333a30af13c2f`.
Baseline tests сохранены `/tmp/qcl-dev13-green2-actor-tests.py`.
Все4 product hashes unchanged: service397e3c4c…b6a6e24,
api d324a918…96ea5e63, exports1116d371…250351a8, settingsfc8986ec…10c3897c.
Никаких production fixes до root semantic RED3 release.

## Differentiating Event control

`test_queued_reader_close_cancels_unstarted_work_without_losing_other_leases`
parameterized read/seek (2cells).

1. Открыты primary + independent artifact leases. Unrelated list_runs backend
   signals started и held Event, actor ready; все call/io deadlines1s.
2. Primary reader read/seek admitted в очередь; observer под actorCondition
   подтверждает exact queued reader operation до close.
3. Immediate reader.close возвращает stopping; observer подтверждает closing
   до backendrelease, пока exits ещё нет. Timeout не используется как witness
   ordering, deadline не повышен для обхода race.
4. Release unrelated backend до call/io deadlines; bounded join clients.
   Queued request должен получить ordinary local closed-reader ValueError,
   никакого backendcall/useafterclosed, KeyError либо orphan waiter.
5. Primary exitcount1, owner ещё не unload; independent GET и secondaryreader
   остаются работоспособны. Repeated primaryclose completed0/0; secondaryclose
   exitcount1; explicit actorclose completed, единственный unload после него.

Backend Stream дополнительно отвергает read/seek после actual stream.close.
Все exits должны выполняться на owner. Event release/helperjoins стоят вfinally.
Expected semantic RED currentproduction: owner cleanup pop-ит primary lease,
queuedmessage вызывает missing-registry KeyError, typed-refusal assertion fails.

Этот negative fixture временно заменяет OWNER_GUARD отдельным Lock, чтобы
ожидаемый crash не отравил соседнюю parametercell; actual ownerfuture bounded
wait выполнен до восстановления monkeypatch. Health/unload/exits assertions
внутри test по-прежнему запрещают crash. Fixturefinally перехватывает только
точный ожидаемый owner KeyError после сохранения distinguishing assertion;
это не product-success и не force-unload/guard reset живого owner. Fake backend
не имеет native resources/profile. Existing regression tests и original ASGI
fourcells не менялись.

## Checks/request

Source-only Ruff format/check testfile PASS; gitdiffcheckPASS. Projectimports,
tests/build/install/Git mutation/SSH/solver мной не выполнялись.
Root RED3 exact selection — only new two cells:
`components/qcl-negf-portal/tests/test_actor_deadlines.py::test_queued_reader_close_cancels_unstarted_work_without_losing_other_leases`.
Runtime result ещё pending; stop до semanticRED3 и production release.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R4 отдельно различается | Confirmed queue→closing→release и typed/no-backend/health assertions | Пока source-only | дополнительно измерить |
| Production unchanged | Existing4hashes | R4 fix ещё отсутствует | сохранить |
| Existing167pass закрывает R4 | Нет такого assertion в old denominator | SourceCHANGES_REQUESTED действует | данных недостаточно |
