# SI07 FORMAL-1: независимая формальная проверка

**Вердикт: formal format pass для frozen 12-file bundle. Поведение не измерено.** Выполнены ровно четыре quick_validate calls, по одному на пакет, повторов нет; forward samples = 0. Кандидаты и проект не изменялись.

Root HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`; checkout dirty, полный initial `git status --short` и recursive submodule status сохранены в identity. Источник кандидата определяется SHA файлов ниже, а не одним HEAD.

## Identity и ограничение полномочий

Bundle: `/tmp/qcl-SI07-FORMAL-1/packages`; ровно 12 файлов, 70591 байт. До копирования original aggregate guard 65,536 B остановил freeze-helper. Попыток validator тогда 0, attempt folder не создан. Root затем явно расширил aggregate cap до 81,920 B, сохранив per-file <65,536 B, прочие caps и тот же logical FORMAL-1. Сохранены original helper v1, его SHA и companion receipt первоначального failure; stderr companion переписан из tool output и не выдается за исходный redirected log.

Формальный runtime: один CPU affinity, 512 MiB RLIMIT_AS, 15 s RLIMIT_CPU, timeout 30 s/process; по 64 KiB RLIMIT_FSIZE на stdout/stderr (128 KiB combined). Temporary directory фактически пуст после каждого процесса; cap 1 MiB проверен postflight, отдельная filesystem quota не создавалась. Валидатор и helper не пишут временные данные, bytecode отключён. Aggregate formal wall cap 120 s; наблюдено 0.463790 s.

Python 3.14.7, PyYAML 6.0.3; actual version/origin/sys.path записаны отдельным bounded binding/manual процессом до quick_validate calls. В prepared venv есть editable `.pth`; применены `-I -S -B` и точечное добавление установленного site-packages без обработки `.pth`. Target project imports в binding отсутствуют. Команды child-процессов полностью сохранены в каждом receipt. Только stdlib wrapper и установленный PyYAML; установок, native/product tests, solver/build/benchmark/profile/server/SSH действий нет.

Python binary SHA-256 `dd65a07e8f535525443d63e2bd6dd10efbf22bf22e0b6d65e634266acc7ac976`.
quick_validate SHA-256 `ee6dba90f44d37171c5a6edb8095979c54919ff6822c1a907afca2e78c48738c`. В полностью прочитанном исходнике нет объявленной версии: version неизвестна, source hash является identity.
Локальный официальный UI reference SHA-256 `ffac39318e408108141d40f820968e59f70434a891694f9bf1d25be8237b150c`.
Loaded `yaml/__init__.py` SHA-256 `b19dfcc333d6a75dfd73073901164507252f271b41d3b5f7d85510033a0547a7`; остальные module origins и sys.path в identity.

## Frozen files

| Пакет / путь | Байты | SHA-256 |
| --- | ---: | --- |
| `qcl-research-framing/SKILL.md` | 5280 | `5c3833087f43e9e639e2b3f3022b1df00682473b8aa2c200b72a0ac53d54e500` |
| `qcl-research-framing/agents/openai.yaml` | 452 | `e1ad31b68e4749ffb1bf88de23fd465f27b91e7c94786cef943db25f304c60ae` |
| `qcl-research-framing/references/brief.md` | 7743 | `5acf06b37185d31f25b8b52a08bd62d6dfe2d5e8d5244afc9da1eedf272a9f0e` |
| `qcl-physics-audit/SKILL.md` | 5425 | `b9a4265d90964efeacfff6eac997f22e9fa9214c3d713ed704191a7dd46127fe` |
| `qcl-physics-audit/agents/openai.yaml` | 429 | `f51b508e3ad0a1103c851c0c1ef5aef79e0c63064f9ee02321e7db8a225ae318` |
| `qcl-physics-audit/references/physics-checks.md` | 8994 | `a2b41df68de6ced8921e43a8f46bb123b84381fe9cc30441211cc8d306d5fb29` |
| `qcl-results-analysis/SKILL.md` | 6717 | `89bdd7be7b91cb46da1663777a639fab0f6ce738a989c0e0cfa633c92d3da4bc` |
| `qcl-results-analysis/agents/openai.yaml` | 393 | `b4974c1c32d462d7d1128a6a058980f1a1b712a3460d83d6925fa0ad78985423` |
| `qcl-results-analysis/references/comparison.md` | 8555 | `ae11f2a66bbc43289f64ef850180d5bf165ca77b1a24e95fed8c2df008a9860f` |
| `qcl-performance-audit/SKILL.md` | 11631 | `597043c2c3a660ae18c84c17ba96729ba393b2e4f53491574af3d156c408ea3b` |
| `qcl-performance-audit/agents/openai.yaml` | 404 | `2a8721c4ee8de5fae982cad3f112ff5df1ae2aef6dca633b14ea980733f25836` |
| `qcl-performance-audit/references/telemetry.md` | 14568 | `c7a463d9e5397f331b1b4ab5a73c2c19daf02c42c4c0ae70e1193d3efc1fe7d5` |

Финальное сравнение всех original/copy SHA подтвердило совпадение; copies read-only, layout ровно по manifest. Git mutations не выполнялись.

## Наблюдения формальной проверки

| Пакет | quick_validate exit | Wall, s | short_description, Unicode chars |
| --- | ---: | ---: | ---: |
| `qcl-performance-audit` | 0 | 0.115188 | 50 |
| `qcl-physics-audit` | 0 | 0.115025 | 46 |
| `qcl-research-framing` | 0 | 0.115212 | 48 |
| `qcl-results-analysis` | 0 | 0.115294 | 41 |

Каждый original stdout содержит `Skill is valid!`, stderr пуст. Один отдельный manual/binding процесс завершился с exit 0; это не дополнительный quick_validate call. Все raw stdout/stderr, receipt command/hash/exit/wall и manual property observations находятся в `raw/`; общие raw logs 8427 B.

Отдельно от quick_validate проверены: frontmatter name==folder basename; поддерживаемые frontmatter/UI keys и типы фактически присутствующих значений; непустые required strings; UI строки в кавычках и ключи без кавычек; длина short_description 25–64 Unicode code points; точное literal `$skill-name` в default_prompt; отсутствие TODO/TBD/FIXME/PLACEHOLDER markers; существование локальных Markdown targets внутри standalone package. Все эти наблюдения положительны. Дополнительных policy/dependencies/assets нет, их runtime semantics не проверялись.

Root-relative owning locators в inline code остаются явно обозначенными repository-relative locators, не обещанием наличия root в standalone. Package-local Markdown targets доступны в frozen copy. Внешние URL перечислены с `network_verified=false`; публикации и target sites не открывались, содержательная научная достоверность этим pass не устанавливается.

## Изоляция и пределы независимости

При начальном широком `rg` ошибочно напечатались snippets исторических reviews и SI04/SI06 evidence. Полные эти reports не открывались, но read-scope leak нарушил требование слепоты; о нём немедленно сообщено Root. Минимальный известный список ниже; исходный tool output был truncated, поэтому исчерпывающий список экспозиции не утверждается. Формальные source/hash/YAML/path observations получены непосредственно из frozen files и установленного валидатора. Forward оценивание передано Root другому fresh evaluator; текущий evaluator не готовил prompts или expected diagnoses и не запускал samples.

- `docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/reviews/RV17-review.md:9,11,15,17,18,22`
- `docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/reviews/RV17-blind.md:3,17`
- `docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/reviews/final-artifact-review.md:5`
- `docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-si04-design-review.md:3,56,67`
- `docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-si04-checkmatrix.md:4`
- `docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-si06-engineering-route-audit.md:27`

## Утверждение / свидетельство / ограничение / решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Frozen candidate определён точно | 12 SHA-256, 70,591 B, original/copy recheck; identity JSON | Dirty root HEAD не описывает overlay без file hashes | сохранить |
| Формат прошёл четыре quick_validate | Четыре independent process receipts; exit 0 и actual stdout/stderr | Validator проверяет frontmatter/name grammar/часть placeholders, не поведение | сохранить |
| UI и package-local links соответствуют проверенным формальным требованиям | Отдельный bounded YAML/manual process, per-property raw observations | Не UI rendering, не внешние URL/научная проверка | сохранить |
| Исходный aggregate envelope был достаточен | Freeze guard failure при 70,591 >65,536 B | До failure validators=0; amendment до81,920 B выдан Root отдельно | изменить |
| Независимость forward evaluator сохранена здесь | Сохранён read-scope leak; samples0 | Видимы snippets прежних выводов; этот evaluator не подходит для blind forward | данных недостаточно |
| Поведенческая, runtime и scientific acceptance установлены | Новых samples/native/solver/build/server receipts нет | Только formal-format evidence | дополнительно измерить |

Формальный этап остановлен. Никаких forward samples, reruns или расширения вычислительного этапа не выполняется.
