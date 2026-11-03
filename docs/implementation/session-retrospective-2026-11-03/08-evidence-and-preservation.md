# Evidence: происхождение, сохранность и доступность

## 1. Что этот PR сохраняет

Связный public-safe пересказ требований, работы, решений и отказов; before/after Source refs;
классифицированный count; индекс merge/PR; точные границы выполненного и невыполненного; competing
explanations и предложения для будущего анализа. Это docs-only snapshot после пользовательского
STOP. Он не меняет component gitlinks, packages, policies, services или данные.

Исходная session началась27окт2026 в19:03:35UTC, человеческий implementation request —19:03:45UTC.
Текущий public report готовится после поручения оставить всё как есть и публиковать evidence. В
Europe/Minsk публикация может быть уже4ноября; directory date2026-11-03 относится к дате основного
аудита, а не обещает, что все files были написаны до полуночи.

## 2. Уровни свидетельств

| Уровень                 | Что доступно                                                                        | Что проверяет                                                                                           |
| ----------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Public первичный Source | Exact component/root commits, symbols и GitHub links в02/03/07                      | Что было опубликовано и где лежит реализация                                                            |
| Public планы            | Исходный programme и architecture на named published ref                            | Требование/разрешённая альтернатива, а не runtime readiness                                             |
| Public report           | Сводки измерений, отказов, отзывов, local packet locators иSHA                      | Проверяемые claims; требует получения private artifact для независимого воспроизведения некоторых чисел |
| Local primary receipts  | Сохранённые original commands/stdout/stderr/JUnit/manifests/reviews/failed attempts | Факт исполнения, identity, Source, terminal result в указанном scope                                    |
| Local session records   | Root и subagent JSONL, message timestamps, compactions, tool failures               | Кто что поручил/сказал/запустил; не автоматическая атрибуция всей стоимости                             |

Private locators в отчётах относительны к рабочему репозиторию и **не являются файлами этого PR**.
Hash позволяет сверить конкретный полученный artifact, но сам по себе не доказывает истинность
содержимого. Source test PASS не заменяет Native execution; installed readback не заменяет
scientific acceptance.

## 3. Именованные local evidence sets

Все пути ниже — только указатели. Raw contents, SSH/PG параметры и inventories не копируются в
GitHub.

| ID  | Local locator                                                                                         | Что в нём / ограничение                                                                                                                             |
| --- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| E01 | `.build/program-audit-20261103/`                                                                      | Первая самодиагностика, Git diff counts, transcript metadata/timeline; не полный semantic аудит всей недели                                         |
| E02 | `.build/session-evidence-publication-20261103/line-census-summary.json` и `line-census-detailed.json` | Категории/файлы/refs; исходники не экспортируются; метод physical lines, неSLOC                                                                     |
| E03 | `.build/session-evidence-publication-20261103/count_tracked_lines.py`                                 | Локальный воспроизводимый счётчик Git blobs; не новый runtime/module проекта                                                                        |
| E04 | `.build/session-evidence-publication-20261103/publication-index.json`                                 | 250 merge records в выбранных Git ranges; это не250 полезных функций                                                                                |
| E05 | `.build/Results-actual-final-metadata-publication-20261103/`                                          | Source6 review, commit/push/PR42/merge и tree readback; published head qualified                                                                    |
| E06 | `.build/P04-P05-Root127-Results-full-durable-20261103-attempt4/`, `attempt5/`, `attempt6/`            | Original terminal receipts и streams;4 failed,5 interrupted,6 passed. Сокращённый список в04 даёт точные полные directory names                     |
| E07 | `.build/P04-P05-Root127-actual-final-Results-arena-20261103/reconciliation.json`                      | Earlier broad attempt3 INCOMPLETE_LOST_TERMINAL, exit unknown; не PASS                                                                              |
| E08 | `.build/P07-Root127-selected-access-actual-lifetime-measurement-20261103/`                            | ЕдинственныйactualA32 diagnostic, original preservation, accounting, explicit missing residents; tiny engineering inputs, не старый science archive |
| E09 | `.build/P07-Root127-selected-access-allowance-card-independent-review-20261103/`                      | Независимый конечныйA128/B512 bound и исправленная offline арифметика; Source-only                                                                  |
| E10 | `.build/P07-Root127-selected-access-scoped-allowance-independent-review-20261103/`                    | 43 contract checks, unchanged baseline failure applicability; не wholeAiiDAGREEN                                                                    |
| E11 | `.build/P07-Root127-A128-B512-fresh-typed-chain-20261103/`                                            | Prepared driver/config/manifest; execute=false, fresh attempt отсутствовал при freeze. Нельзя запускать по одному этому locator                     |
| E12 | `.build/P20-Root127-main-workload-qualification-design-20261103/`                                     | Source-only полный dynamic design, implementation не начиналась                                                                                     |
| E13 | `.build/P20-Root127-main-workload-qualification-independent-review-20261103/`                         | Два независимых design blocker и оценка necessity/fixed alternative                                                                                 |
| E14 | `.build/P20-Root127-short-command-witness-design-20261103/`                                           | 58-member frozen design/primary probes; новый completed witness не implemented                                                                      |
| E15 | `site/proxmox-single/generated/codex-execution-2026-10-27/state.json` и `handoff.md`                  | Текущий explicit USER STOP и исторические snapshots. Старые nextactions не разрешение продолжить                                                    |
| E16 | Original named network attempt packets в local handoff                                                | Profile/L3/STP/rollback failures и fixed socket recovery. Содержат private network data, в public включён только пересказ                           |

Результаты/диагнозы каждого набора локализованы подробнее в Cxx/Rxx/Txx evidence IDs
документов02/03/04. Это сохраняет возможность проверить causal chain, не превращая публичный docs PR
в дамп всех logs.

## 4. Что намеренно не публикуется

- Пароли, private keys, access tokens, auth headers, certificates/private trust, actual inventories,
  LAN IP/MAC/host names и operational UUID.
- Raw session JSONL и tool-result bodies: они могут содержать посторонние инструкции, secrets,
  paths, private inputs или data. Полный экспорт истории не поручен.
- PG database/repository, NFS/job directories, HDF5 arrays, checkpoints/history segments и прежние
  scientific results. Этот evidence task не меняет ранее установленный режим сохранения научных
  данных.
- Private packet files без редакции; наличие них не означает, что их можно массово приложить к
  issue.
- Environment/package dependency installation или новые benchmark/solver runs ради отчёта.

Directory с signing material не читается и не хэшируется; его содержимое не участвует ни в corpus,
ни в privacy scans. Весь public diff ограничен этим новым docs directory.

## 5. Независимость и несогласия

Report02 написал адресный Source analyst;03 — independent reviewer resource design;04 — author
измерений/allowance, поэтому его оценка собственного метода не считается независимым whole-design
approval. Root интегрирует, отдельно проверяет03 и количественные claims; другой reviewer читает
public corpus кроме собственного03. Source reviews могут находить ошибки, но не подтверждают
runtime, которого они не исполняли.

Сохранены разногласия и исправления: failed identity counterexamples, двухфазный dynamic
bootstrap/main, два неустранённых design blocker, отказ публиковать простойA32 cap, исправленная
offline cardinality, remaining legacy/baseline failures и неизвестный исход interrupted attempt. Их
нельзя скрыть за позднейшим PASS другого scope.

## 6. Что запросить будущему анализу

Сначала выбрать один вопрос: необходимость custom architecture, причинность задержек, ценность
tests, либо correctness numerical contract. Затем выбрать минимальный набор primary artifacts
поE/C/R/T IDs. Перед передачей raw material нужна адресная редакция и проверка приватности. Для
анализа всех четырёх предыдущих недель отдельно установить sessions/Source refs начала октября;
нынешний набор не выдаётся за их полный обзор.

Для воспроизведения count достаточно соответствующих Git objects и локального счётчика; для
воспроизведения timing/Native claims нужны original terminal receipts и commands, а не новый attempt
с похожим названием. Для costs нужны semantics per-actor usage records и интервалы активности, а не
total token counter или число сообщений.

| Утверждение                               | Свидетельство                                           | Ограничение                                   | Решение                              |
| ----------------------------------------- | ------------------------------------------------------- | --------------------------------------------- | ------------------------------------ |
| Evidence можно проверить после сессии     | Stable commits/locators/SHA; original failure retention | Часть primary private и не приложена публично | сохранить локально, выдавать адресно |
| Public PR содержит все raw доказательства | Он содержит связные summaries/refs                      | Secrets/data не публикуются                   | не утверждать                        |
| Reports разрешают продолжить программу    | UserSTOP и paused schedules                             | Старые grants/планы исторические              | сохранить остановку                  |
