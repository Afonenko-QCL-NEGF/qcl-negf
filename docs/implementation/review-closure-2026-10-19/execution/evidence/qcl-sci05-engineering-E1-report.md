# SCI05 engineering E1 — STOP после единственного дополнительного раунда

Основание: отдельный конечный engineering extension координатора `/tmp/qcl-checkpoint-SCI05-engineering-E1.json`; это третий раунд, исходные 2/2 не переименованы и не скрыты. Core HEAD `e86ac74c4fe04a8999b889970c5a9f3c65575694`, начальный status пуст. Изменён только `test/numerics/final_audit_evidence.jl`. Писатель прекратил работу; дальнейшее исполнение принадлежит координатору после отдельного review.

## Первичное свидетельство и причина

Сначала прочитаны C08-DIAGNOSTIC-3 raw/receipt: 275 pass, 1 fail, 1 error. Это сохранённый RED, а не приёмка. Raw SHA256 `3ea0c064402917a29df4abae74447c4d17078865469fd62ef7d6cbfd3efc0ece`; receipt `15c50c17b266692734fc58afcb806c0613a0cd7fe67734734f1f3c543328fd93`. Затем прочитан независимый ready contract G1/G2 `/tmp/qcl-sci05-diagnostic-gap-audit.md`, SHA256 `33157fef096a7945c68fe1bcaf54477304704be1b60ee9345c1dcd498659580a`.

G1: ordinary transpose породил complex population и ожидаемый существующим API DomainError realness, тогда как старый тест требовал числовой return. G2: прежнее независимое выражение n−S/3 создавало ненулевую ширину при точном uniform n=1 из-за interval reciprocal 1/3; нулевой product forward error не покрывал эту ширину. Причины берутся из сохранённого результата и независимого audit, не из нового исполнения.

## Изменения

G1: исходный malformed transpose и отдельный `wrong_number` сохранены. Дополнительно независимая scalar complex weighted sum накапливается из literal 2x2 `wrong` matrix entries. Её real projection сравнивается с прежним wrong_number; imaginary part нарушает прежний public gate 1e−10 даже с прежним Bmatrix allowance. Public вызов должен бросить именно DomainError, с точным reason `number functional is not real`; обе компоненты error value сравниваются с independent scalar в прежнем Bmatrix. Другие исключения немедленно rethrow; отсутствие исключения даёт failed assertion, чужой DomainError reason/value также не проходит. Product функция, structural limit и message не менялись. Healthy number, wrong_number-vs-healthy, wrong weights/gs, lambda masking, coherence controls сохранены.

G1 error ledger: обе компоненты complex weighted sum используют тот же конечный scalar 2x2 graph, четыре weighted terms и фиксированный prefactor, что и retained literal real projection. Применён прежний Bmatrix=2^24*gamma4096 без увеличения; для imaginary rejection allowance вычитается из numerator, а Bmatrix добавляется к нормировке, поэтому allowance не ослабляет существующий realness gate. Это fixture-specific comparison nonzero components, не новое физическое acceptance правило.

G2: независимый exactU вычисляется как `la*(3*n[j]−S)/(9*q)`; projected numerator образуется до reciprocal. Это точная алгебраическая эквивалентность `la/(3*q)*(n[j]−S/3)`, без epsilon/snapping/neutral branch. Directed reference operation ledger теперь: exact input points → directed sum S → PB(3)*nf[j]−S → multiply la → divide by PB(9)*q. Для frozen uniform exact Float64 inputs при384 bits projected numerator точен и равен point0; generic outward arithmetic для остальных inputs сохранена. В reference tuple добавлен только внутренний промежуточный projected numerator для прямого positive control до product solve. Проверки point0 numerator/exactU, нулей actual Up/zeta/ratios/neutrality и положительного lambda*delta denominator добавлены явно.

PBall division, γ3/γ32, inverse4/3, short cap, Bmatrix, physical limits, inputs, units и negative amplitudes не менялись. Все old observed mutants (−Up, /4, ×1.1, constant shift, altered density, factor2 residual numerator/ratio), near-zero/measured-zero и public raw rU/mixed checks сохранены. Product calls/solve count не увеличены. Новых production, public API, format или scientific contract изменений нет.

## Статическая проверка и ограничения

`git diff --check` exit0. Diff: один тестовый файл,33 insertions/5 deletions. Новый SHA256 `ede25dde26d72c313fb15e8bfcc515e8d29673b41336535c760a6eb0113309e9`; patch SHA256 `87d2180206e1bbb573fa5b654b3e29cbc07c29775d26b2a8a758fc2e1a184993`. Исходный test SHA256 `d4ac564013d46021a84b323338635f6860f16d1aa76e4b417c4aaf64debf64c4`. Остальные tracked Core files неизменны по clean initial status и final diff; шесть production hashes, authoritative HEAD tree и предыдущие syntax artifact hashes сохранены в identity JSON. Original failed raw/receipts и syntax artifacts не перезаписывались. Original dirty checkout не затрагивался.

Julia/parser/import/tests/build/install/network/server/SCBA/Poisson executions=0; Python processes=0; новых C08 calls=0; stage/commit/push=0; подагентов нет. Сохранённый RED использован как исходное воспроизведение по поручению; GREEN не измерен. Общий C08 max8 неизменен:3 уже израсходованы,5 остаются у координатора. S1 experiment caps, 0mV/70K/no e-e, physics и strict criteria неизменны.

Новая code correction после этого STOP не разрешена данным E1. Если независимый review или execution потребует physics/threshold/schema правку либо ещё один corrective round, требуется concrete blocker координатору, без автономного четвёртого цикла.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| G1 проверяет конкретный realness rejection | Typed DomainError, exact msg, independent complex scalar и обе компоненты value | Новый test ещё не исполнен | изменить |
| G2 сохраняет exact zero до reciprocal | Алгебраически равный projected numerator и новые point0 assertions | Новый directed graph ещё не исполнен | изменить |
| Критерии и production сохранены | Diff только permitted test path; hashes identity JSON | Tiny fixture source check, не scientific acceptance | сохранить |
| GREEN после E1 установлен | Нового запуска нет | Review и bounded coordinator execution впереди | дополнительно измерить |
