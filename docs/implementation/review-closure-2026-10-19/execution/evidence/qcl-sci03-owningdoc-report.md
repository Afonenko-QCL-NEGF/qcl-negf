# SCI03 — owning Research document после approved D2

2026-10-19. D / Sol ultra. Это точный перенос принятого source design в owning
docs, **не третий scientific design round**. Independent CP-CODE ещё не выполнен;
commit/staging/push/PR этим task не выполнялись. Scientific acceptance и runtime
READY не заявляются.

## Source и review binding

Owning checkout:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-research`.
Ветка, уже созданная координатором, —
`codex/review-closure-equilibrium-criteria`; HEAD
`b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3`. Initial owning status clean.
Root при чтении `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8` с concurrent Core
untracked test, AiiDA/Platform internals, checkpoint/evidence/tooling. Они
сохранены и не входят в owning patch.

| Input / output | Bytes / SHA256 |
| --- | --- |
| Approved D2 `/tmp/qcl-sci03-design-v2.md` | 40 812 / `788ab058f1c52520d79aa621dcecd0d525f2562b7fcf2ea10da2c664989c8018` |
| Independent final CP-DESIGN R2 `/tmp/qcl-sci03-design-v2-review.md` | Review SHA256 `351b58065dfd4dd45bbacf95a451a6daa22adaeacaee09149457f8e0ba295442`; прочитан полностью |
| Новый owning `docs/equilibrium-measurement-contract.md` | 45 385 / `758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f` |
| Полный owning patch `/tmp/qcl-sci03-owningdoc.patch` | 46 036 / `652ea2c3a6446d7cf07fd62b2b4ce99e52b7ebce886bf53d5f136ecc38ad9148` |

Scope R2 — **APPROVED только для bounded measurement/pilot design**. R1-01–03
закрыты; finite accuracy/bounds, full scientific/discretization acceptance,
runtime/admission остаются отдельными unresolved gates. Полномочие переносить
этот exact body получено от координатора после review, без нового scientific
решения.

## Owning diff

Единственное изменение Research — новый
`docs/equilibrium-measurement-contract.md`. README не редактировался: optional
link не требовался для данного exact-copy поручения. Никаких code/config/plan/
values/criteria изменений нет.

Краткий wrapper до корпуса фиксирует статус R2, exact accepted body identity,
14 source hashes и неизвестные accuracy/tail/conditioning/admission. Внутри
markers `BEGIN SCI03_REVIEWED_D2_BODY` / `END SCI03_REVIEWED_D2_BODY` сохранены
**все 40 812 bytes D2 без единого изменения**, включая source snapshot,
historical candidate labels, primary URLs и formula/threshold text. Wrapper
объясняет исторический заголовок SCI03-D1; новая scientific version не выдумана.

После корпуса добавлена только навигация: C/R/Research/V ведут на immutable
component trees; P1/milestone/science/architecture — на pinned root9f8b08bb
paths. Remotes прочитаны из actual Git, а canonical paths проверены локально.
Standalone Research не объявлен содержащим Core/Results/root или primary PDFs;
доступность сетевых references/offline inputs вне workspace честно unknown.
Временные `/tmp` paths в unchanged audit body отмечены historical receipts,
не obligatory inputs для published reader. Новых downloads/network probes нет.

Формулы, сохранённые strict thresholds, пять mechanisms/e–e none, S1 slots/caps,
H+ΔE/4 и unresolved blockers полностью унаследованы из accepted body. Wrapper
не назначает scientific constants и не переносит evaluator в Research/UI.

## Выполненные проверки

Чтение/сравнение/hash/Markdown использовало Python standard library и read-only
Git; продуктовые imports, Julia, scientific tests/solver/native не запускались.

- Извлечённый marker-body побайтно равен D2; длина40 812 и SHA256 совпали.
- Повторно совпали все14 owning file hashes из D2§11 и шесть protected SCI02
  inputs ниже. Это source checks, не numerical validation.
- Десять Markdown tables согласованы по columns; fences сбалансированы,
  trailing whitespace нет, final newline присутствует. В документе12 ссылок:
  пять неизменённых primary URLs и семь новых pinned wrapper references.
  URL availability не проверялась сетью; все wrapper canonical paths/trees
  доступны в объявленном local integration workspace.
- `git diff --check` завершился exit0. `git diff --no-index --check /dev/null`
  для нового Markdown вернул обычный diff exit1 с пустыми stdout/stderr:
  whitespace diagnostics отсутствуют; exit1 не интерпретировался как solver/test
  result. Полный generated patch содержит new-file mode100644 и один file section.
- Финальный owning status содержит ровно
  `?? docs/equilibrium-measurement-contract.md`; других tracked/untracked edits
  в Research нет. Index не менялся. Никакие Git mutations не выполнялись.

| Protected SCI02 input, Research-relative | SHA256 без изменения |
| --- | --- |
| literature/reference-2019/source.yaml | `55342a4b75ab22974c483dc0c2efe9b207d2b39502219e7d13d581af5acd10b5` |
| literature/reference-2019/structure.csv | `4aef262aa5c83d60ec1666a60e3b92b8c0ef73d51c9bc51840a8489296a24615` |
| config/model/reference-2019-70k.yaml | `78444c7a358fabef315e07e028d3d65f65fec07efd119ac9ca238cc25c110829` |
| config/policies/analytical-diagnostic.yaml | `fbbb2b4afe9eac694e71b29c77883930072416250f0f75e86d8ffaf3821c49b0` |
| config/studies/equilibrium-0-70.yaml | `2fde52250d6ab85240d556f8c59b70ce1a065e04800d531dea95d9a2f3a8c0e9` |
| config/equilibrium.yaml | `90ca47d51a90501c2822c72b1221f5a9b7fbe2850ea02f5de7ede1b43aa222ab` |

Managed owning directory находится вне writable roots; выполнена одна scoped
escalated write, явно разрешённая поручением, только в новый Markdown. Review,
hash/reads и patch/report записи не расширяли scientific scope. **0 scientific
attempts, 0 solver CPU-hours, 0 product imports/test/build/benchmark/install/fullCI,
0 network/server operations**. Старые S01 arrays/run и protected checkout не
читались. CPU/RSS не измерялись и не выдаются за production resource profile.

## Следующий gate

Independent high CP-CODE проверяет exact owning document/patch hashes, body
identity, единственный owned path, pinned links/standalone caveats и unchanged
scientific inputs. До него не выполнять publication; координатор остаётся
единственным владельцем Git/checkpoint операций. Работа этого author task
остановлена после передачи concrete reviewable diff.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Accepted D2 перенесён без изменения body | Exact40812 bytes/SHA256 и marker comparison | Independent CP-CODE ещё нужен | сохранить |
| Модель/inputs/strict policy сохранены |14 owning hashes,6 protected hashes, один Markdown diff | Frozen/runtime plan не создавался | сохранить |
| Документ читается с явными source routes |12 URLs, pinned wrapper paths и standalone caveat | Remote availability не проверялась | сохранить |
| Physical/discretization acceptance и runtime READY получены | Missing accuracy/bounds/guards/admission | Docs-only operation не numerical result | данных недостаточно |
