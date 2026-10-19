# SCI02 — owning Research docs candidate для CP-CODE

2026-10-19. Автор D / gpt-6.1-sol ultra. Этап: docs-only authoring после
независимого CP-DESIGN PASS; **CP-CODE ещё не проведён**, commit/push не выполнены.

Owning checkout:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-research`.
Ветка `codex/review-closure-model-passport` создана от чистого Research
`5458212063a41051328ef8b5d14d63d5ac7dc781`. HEAD остался тем же, staging пуст.
Root/другие компоненты не редактировались этим task; их concurrent изменения
сохранены и не включены в owning review diff.

## Review binding

- Принятый design: `/tmp/qcl-sci02-design.md`, 37 234 bytes,
  SHA256 `62c844a81fb91710794995843c843420009590bf527d3f687187a4a606a72be1`.
- Независимый CP-DESIGN receipt `/tmp/qcl-sci02-review.md`, SHA256
  `45258bc2665b4dacdb95f76e4d1c7adc0c219b4cf0ca5093e02cf6a33c098609`.
- Полный review diff **включает новый untracked passport** и три tracked edits:
  `/tmp/qcl-sci02-review.diff`, 37 863 bytes, SHA256
  `750cd60b9edc1972fbcded4bc2ae6d62c70cc653f326bff704c5f30e6835998f`.
- Docs check receipt `/tmp/qcl-sci02-check.json`, SHA256
  `985cfe9255530d744116d54ef4f862766bb5ab39be9c94744de2f1bca4793230`.

CP-DESIGN requirement выполнен: в owning passport сохранён блок полных refs
root `e0f244d075dd49874ba4f3847f4efa693f3b3622`,
Research `5458212063a41051328ef8b5d14d63d5ac7dc781`,
Core `4af6e94808c6e60affbf1050a5184dbc12083335`, numerical parent
`3108150dd1b6b1377470b384b15c26e272fe5c5d`,
Runner `0c53c6d0f68e0b25fce79388db831da6fc3ae856` и symbol map.
`run=not_created`, `null` identity с причиной, runtime/imported-producer unknown
и source-derived expected значения явно отделены от будущего frozen/runtime
evidence. Refs — локаторы этого source audit, состав release задаётся gitlinks.

Технический body из design от «Проверенный первичный источник» до конца
«Вердикты и пробелы» перенесён без изменения текста; убрана только последняя
пустая строка, бывшая separator перед исключённым design-only Acceptance.
Статус рабочего dirty root из design в публикуемый passport не переносился.
Вместо него добавлено краткое введение о source-only scope и сохранении модели;
полный source/ref/identity блок оставлен. Новых научных assumptions нет.

## Owning diff

| Файл | Изменение | SHA256 финальных bytes |
| --- | --- | --- |
| `docs/reference-2019-model-passport.md` | Новый паспорт: primary identity/hash/pages, sheet/volume caveat, donor-normalization chain, formula/value/assigning/default origins, expected S01, unknown levels | `653dc08a55575043b3b95ee43c0ff5413914f39ae6b554c9993345514d5f8f3c` |
| `docs/scientific-inputs.md` | Узкая ссылка на passport и caveat без смены sheet value | `3c8e33fee9ebb6ece8e05dae49f4fdd6fccd19f74b6e1fbea27eccfebcd78688` |
| `docs/equilibrium-s01.md` | Устаревшая строка primary-not-checked заменена проверенным статусом/caveat; прочие criteria/gates сохранены | `cc4e6b31ffa8d74c39d06afda28f63dfac955d101437ea28bcb5d298e9ac9815` |
| `literature/README.md` | Одна ссылка на passport и предел attribution | `ecedcbeac9b4ada122b642f3f6a5d8cf3e19e76897c075c522c220c125863ea5` |

Модель сохраняет 0 mV/period, lattice/LO 70 K, sheet4.5e14 m⁻²,
LO/acoustic/impurity/IFR/alloy и e–e mode none. Полнота ионизации и material
numbers остаются declared assumptions с неизвестными primary value origins.
Caption conflict не объявлен доказанной опечаткой или исправленным input.
Geometry200 K/56 mV и digitized curve не принимают equilibrium70 K.

## Выполненные проверки и пределы

`python3 /tmp/qcl-sci02-check.py` завершился exit0 после исправления whitespace:

- Scope ровно четыре `.md` по tracked diff + untracked inventory; staging пуст,
  HEAD равен согласованному base.
- Technical body совпадает с принятой версией за исключением одной EOF
  separator newline; все полные immutable refs и unknown/not_created markers есть.
- Девять относительных Markdown-ссылок существуют; fences сбалансированы,
  trailing whitespace отсутствует, файлы заканчиваются newline.
- `git diff --check` для tracked и `git diff --no-index --check` для нового
  passport не сообщили whitespace defects. Full diff содержит четыре file sections.
- Шесть protected hashes ниже точно совпадают с исходным design audit;
  остальные tracked non-doc paths отсутствуют в owning diff.

| Protected input | SHA256 без изменения |
| --- | --- |
| `literature/reference-2019/source.yaml` | `55342a4b75ab22974c483dc0c2efe9b207d2b39502219e7d13d581af5acd10b5` |
| `literature/reference-2019/structure.csv` | `4aef262aa5c83d60ec1666a60e3b92b8c0ef73d51c9bc51840a8489296a24615` |
| `config/model/reference-2019-70k.yaml` | `78444c7a358fabef315e07e028d3d65f65fec07efd119ac9ca238cc25c110829` |
| `config/policies/analytical-diagnostic.yaml` | `fbbb2b4afe9eac694e71b29c77883930072416250f0f75e86d8ffaf3821c49b0` |
| `config/studies/equilibrium-0-70.yaml` | `2fde52250d6ab85240d556f8c59b70ce1a065e04800d531dea95d9a2f3a8c0e9` |
| `config/equilibrium.yaml` | `90ca47d51a90501c2822c72b1221f5a9b7fbe2850ea02f5de7ede1b43aa222ab` |

Первая docs check нашла `new blank line at EOF` в новом файле, exit3 у
`git diff --no-index --check`. Причина — перенесённый separator перед design-only
Acceptance. Сохранён исходный failure text/diagnosis:
`/tmp/qcl-sci02-check.failed-1.txt`, SHA256
`8d34dc52e611718cca2ac1bba48beda99ba6cf3191f1eeb82c7e650fb5a496a2`.
Удалена только одна newline; повторная адресная проверка exit0. Это документационная
проверка, не продуктовый red/green test и не scientific result.

Проверка использовала Python standard library для чтения/сравнения Markdown,
hashes и subprocess Git, **без imports продукта/численной среды**. Не запускались
product tests, build, solver, benchmarks, SCBA/Poisson, новые downloads или server
actions. **0 scientific attempts, 0 solver CPU-hours**. Fresh production resource
admission не требуется этой docs-only операции и не объявляется полученным;
CPU/RAM не инструментировались и не выдаются за measured resource profile.
S1 caps/научный scope не изменены. Report и review diff каждый ниже64 KiB.

## Следующий gate

Независимый CP-CODE проверяет exact полный diff и указанное source binding,
ограничение четырьмя docs, absence of value/config changes, ссылки и корректное
разделение unknown от scientific pass. Только после его принятия координатор
может поручить commit/push/PR в активном P1 scope. Текущий task их не выполнял.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Reviewed design перенесён в owning docs | Full diff/hash, body comparison, source/ref block | CP-CODE ещё ожидается | изменить |
| Scientific input и пять channels/e–e none сохранены | Protected hashes + четыре Markdown-only paths | Frozen/runtime identity не создана | сохранить |
| Links/Markdown format согласованы | 9 link checks, fences/whitespace и Git checks exit0 | Product tests/build не выполнялись | сохранить |
| Паспорт устанавливает equilibrium70 K | Final U/G и numerical evidence отсутствуют | Convergence/physics/discretization/experiment не измерялись | данных недостаточно |
