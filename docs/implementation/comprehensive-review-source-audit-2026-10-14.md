# Аудит источников программы комплексного ревью

Дата: 2026-10-14. Это sanitized snapshot источников для
[программы ревью](../system/comprehensive-review.md), не runtime acceptance
и не новый source lock. Чтение кода, GitHub metadata, публичных manifest
и выбранных сохранённых свидетельств не изменяло сервер, код или результаты.
Научные массивы, credentials, private inventories и site endpoints сюда
не включены.

## Состав исходников и публикация

Фактический root HEAD — e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1. Восемь
components чисты и соответствуют его gitlinks. Изменены root AGENTS,
README, TODO, architecture и deployment runbook; docs/system находится
в working tree. Эти overlay файлы нельзя автоматически приписать HEAD.
Все девять selected commits доступны через GitHub; доступность source
не означает merge в main или release acceptance.
На bootstrap a4ad47f CI/release workflows имеют только workflow_dispatch:
публикация docs branch сама не запускает эти проверки.

| Объект | Свидетельство | Применимость |
| --- | --- | --- |
| Selected root | [e48e5b2](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1) и его gitlinks | Authority выбранного checkout, не installed scientific source |
| Remote root main | 95d4584c6f27d88d18693489b9c134fa9ae82d62 | Migration состав; docs/system отсутствует; selected branch histories diverged |
| Stage1 | [Draft PR8](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/8), a6849e86339182bf5d3250d917404292ad35a2cf | Опубликованная ветка, отдельно от main |
| Corpus | [PR9](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/9), ff50bc2f24c0774eb7de874a60e6d0d96a47197e | Merged в stage1; локальное наличие docs/system не означает, что весь корпус нигде не опубликован |
| Bootstrap | [Open PR17](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/17), a4ad47fbd726dc61f627010498c15f09cb5a305b | На момент проверки 26 commits ahead e48; изменены AiiDA, Contracts, Platform и Portal, другие четыре gitlinks совпадают |

Перед этим authoring проверка установила: 13 из 16 рассматриваемых root docs
уже опубликованы byte-for-byte. Три local версии — root README,
docs/system/README и implementation-entrypoint — содержат отличающиеся
устаревшие uncommitted declarations. Их нельзя перепубликовать как есть.
Текущая правка system README добавляет ссылки на новые материалы, не выполняя
полную reconciliation прежнего текста.

Полезные local worktree materials сохранены. У двух Platform test drafts
итоговые assertions уже опубликованы в ae6a6ca85b8094378eb9dc99a04b3b25fb575a6f;
оставшийся diff относится к fixture/loader/clock/budget context. Это archive
draft, а не потерянный implementation PR. Local i02 delivery note относится
к stage1 a6849e8 + Platform fe8e2 и исторической перепроверке GAP04.
Published replacement — docs/implementation/i14-local-update-ci-boundary.md
на bootstrap a4ad47f и owning application-cd documentation с protected
administrative namespace. Старый путь не переносится в current runbook.
Архивирование worktrees и удаление файлов в этом аудите не выполнялись.

## Минимальный runtime и существующий S01

Итоговый контекст пользователя — чат «Описать состояние реализации плана»,
последний завершённый turn 01a13501-9e47-7611-8a42-6de1489a6561. Его вывод:
минимальный кластер с одним compute работает, S01 физически запущен;
результаты и сходимость не приняты. Additional workers/backends, Portal auth,
централизованное наблюдение и full CI остаются отдельными рубежами.

Первичный сохранённый locator — canonical-update-ROOT-recovery-attempt4 /
ROOT-result.original.json, SHA256
4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3.
Он фиксирует minimal ready/open/completed для release
qcl-5d779b52-s01-20261012, scientific/full CI — false. Submit run —
dfb75b38-6019-4861-b868-f51648c71f02, frozen plan SHA256
4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9.
Последний прочитанный saved status — RUNNING, 2026-10-13 17:46 UTC.
Read-only snapshot не устанавливает live now или terminal result.

Точные JSON locators исходного receipt:
/native_owned_closure/runtime/ready=true,
/native_owned_closure/gate/open=true,
/native_owned_closure/delivery_report/status=completed,
/scientific_accepted=false и /full_release_CI_accepted=false.
Прочитанный status snapshot имеет 7978 bytes и SHA256
d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90.

## Документация и практическая публикация

Core/Runner уже имеют native Documenter; ops/ci.ts:70–75 собирает оба сайта
с root locked Julia workspace. Portal api.py:457–459 раздаёт React assets,
Platform nix/application.nix:13–15 включает их в application,
modules/application.nix:114 проксирует корень. Полный documentation bundle
в этом committed serving пути не локализован.

Отдельная practical HTML публикация существует. Public locator —
Documenter4-publication-ROOT-recovery-attempt1 /
public/documenter-public-artifact.manifest.json, SHA256
1aced715cbcefcef54be998ee1822df9f383969e5e6abdf375a643f3ff00fb35.
Manifest содержит Core34/Runner8 HTML, artifact_only=true,
science_unchanged=true; browser_theme_verified=false,
offline_browser_verified=false. Это предыдущий artifact, не всё a5 evidence.
A5 Runner resource-search summary явно derived, без native screenshot;
online navigation/search reported, offline/Dark-OS/science не приняты.

Сохранённый GUI viewing guide описывает finite viewer и источники a5,
но одновременно содержит recovery history, installed-source различия,
site endpoints и private evidence links. Его целиком нельзя включать
в public docs. Нужны извлечённый стабильный how-to и отдельный private
operator supplement.

## Действующие факты и вопросы к коду

| Локатор выбранного компонента | Наблюдение или вопрос | Решение |
| --- | --- | --- |
| Results fe27a2a, tests/test_equilibrium_diagnostics.py:37–38,112–113 | Hardcoded личные absolute paths ограничивают переносимость tests; [draft PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6), a1492b7 предлагает fix | Проверить existing PR, не создавать дубликат |
| Contracts 923e0c6, README:44/67; export-receipt.schema.json:45–47 | Общий текст о 200000000-byte part расходится с уточнением legacy-only; новый receipt bytes не имеет maximum | Уточнить documentation scope |
| Runner 0c53c6d, schema/PROVENANCE.json | Две vendored schema имеют те же прочитанные SHA256, что Contracts | Сохранить canonical source; drift guard ещё локализовать |
| [Portal 36837e98, exports.py::ExportStore.create/_prepare](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/36837e98a8d1f85820f2807d0212ec92e73c3c7b/src/qcl_negf_api/exports.py); [AiiDA 53e2a205, service.py::list_artifacts](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/53e2a20544a469dd7ee5560243ebe530a6310f0a/src/aiida_qcl_negf/service.py) | Inventory содержит все attempts; composite export выбирает execution_id и открывает plan/files без exact attempt selectors. Это отдельная граница от исправленного CR01 single-file download | Synthetic reproducer; production failure не установлен |
| Portal 10b6c87, src/qcl_negf_api/service.py::AiidaService._call/close | Вызов result без явного deadline требует review blocked-owner responsiveness/close | Bounded failure check, не объявлять наблюдённый hang |
| Runner commit_point_artifacts; Platform activate | Review mutation/durable acknowledgement/prior-state и crash между profiles/allowlist/environment/ready marker | Карта invariants и failure packet; fixtures не NFS/restore proof |
| Cross-language schema и Portal hatch_build.py | Сопоставить valid/invalid corpus bool/int/nonfinite/origin/attempt; проверить compiled assets/source/lock binding | Source review и selected checks, не утверждение установленной регрессии |

Declared package graph не показал cycle: Runner→Core,
Results/AiiDA→Contracts, Portal→AiiDA/Results. Это metadata observation,
не доказательство отсутствия import/runtime cycle. Большие модули выбраны
как hotspots для cohesion/state/complexity review, не признаны дефектами по LOC.
Версия 0.2.0 и Core tag v0.2.0 не идентифицируют фактически импортированный
post-tag gitlink 3108150; build/runtime source нужно устанавливать отдельно.

## Источник методики

Java latest PR13 exact head — a0d1bdb9d8343809560e3ce7f9a2141d4473ee3f.
Прочитаны authoring-methodology.md, blob
597c76be45a30695faafc887ed8e410fc38ce8a7, sources.md, blob
759d42e3bb1e2e6d6db96db148f98c5df531b204, и полная methods.qmd.
Methodology унаследована из PR12; PR12 не назывался последним.
Доступ к книгам/статьям и exact scope выбранных разделов описан в
[QCL методике](../system/documentation-methodology.md).

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Selected code опубликован | Девять GitHub commits и source graph | Publication не main/release acceptance | Сохранить |
| S01 запущен | Submit identity, plan hash, saved RUNNING | Terminal/science verdict не установлен | Дополнительно измерить |
| Native HTML существует | Public manifest и derived a5 observations | Offline/Dark-OS/общий docs hub не приняты | Сохранить |
| Есть переносимость и docs scope вопросы | Точные current locators и existing PR | Полные suites не выполнялись | Изменить |
| Локальные drafts не означают потерянный код | Published assertions и replacement document | History/source scope требует сохранения | Сохранить |
