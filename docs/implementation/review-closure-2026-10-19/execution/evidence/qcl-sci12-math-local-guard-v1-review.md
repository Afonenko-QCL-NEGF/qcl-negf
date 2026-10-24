# SCI12Math local guard v1 — независимый source review

2026-10-20. **CHANGES_REQUIRED_SOURCE_ONLY: один блокер сохранности original raw.** Это source-only verdict для SHA `5aa294ebcd86969d1bef07f1d108fd607e250978170641e4609d9d5ebb9a09e4`; не execution READY, не разрешение target call и не научная приёмка. Дочерних агентов нет.

## Точный блокер B1

В `/tmp/qcl-sci12-math-local-guard-v1.py:309–313` порядок следующий: успешный `subprocess.Popen` с stdout pipe; потенциально выбрасывающий исключение `observe()`; только затем `collector_attempted=True` и `RawCapture`.

Воспроизводимый по source control flow случай: процесс уже выдал байты в pipe; `sampler.sample_owned_temporary_bytes(temporary)` внутри `observe():270` выбрасывает OSError, не являющийся ENOENT (helper:39–41 явно его пробрасывает). Обработчик :317–319 сохраняет исключение и переходит в finally. `stop_owned` :322 останавливает/reap собственный процесс. Collector точно ещё не пытались создать, поэтому R1b UNKNOWN branch :326 не применяется. В ветви :339–341 выполняется только `stream.close()`: `process.stdout` не читается, уже выданные исходные байты не попадают в `original.log`. Попытка честно получает STOP/incomplete, но original failed raw потерян. Это отдельный дефект provenance, не ложный PASS и не вопрос Contracts origin.

Минимальная correction: после успешного `Popen` немедленно установить `collector_attempted=True`, создать `RawCapture`, затем выполнить первое live `observe()`. Тогда потенциально падающее наблюдение происходит при continuous reader. Альтернатива — bounded drain только в доказанной ветви `collector_attempted=False`; UNKNOWN ownership должен по-прежнему запрещать competing read/close. В проверенном lifecycle reference v7 известная ветвь отсутствующего collector имела drain fallback (:540 далее); текущий v1 его не сохраняет. Runtime failure injection в этом review не выполнялась. Нужна адресная source correction и проверка её exact новых байтов до Root READY; guard здесь не изменялся.

## Остальные проверенные свойства

* Exact clear child environment :301–310 задаёт candidate `PYTHONPATH`, без target `-I`; argv :408–409 запускает только frozen fixture через `-m pytest -q --tb=short -p no:cacheprovider`. Autoload plugins отключён, write-bytecode запрещён, thread variables1, HOME/TMPDIR принадлежат попытке. Frozen candidate pyproject задаёт только `--strict-markers`; closure связывает pyproject и отказывает при implicit parent conftest/config.
* Fixture :39–51 проверяет actual Results package/module origins. Contracts :55–56 только импортирует ContractError; `QCL_NEGF_TEST_CONTRACTS_SOURCE` не доказывает actual Contracts ownership. Это явно ограничено plan/report, отдельного source blocker здесь нет.
* Closure :96–119 охватывает все перечисленные Results/src и selected Contracts/src `*.py`, fixture и pyproject с exact keys/hashes; RED требует absent new module и null product hash; GREEN требует exact будущий product hash. Это ограниченный trusted source closure, не OS import sandbox и не заморозка всех third-party dependencies.
* Helper :227–231 читается/хешируется и исполняется из того же buffer через `reviewed_module`:122–128. Before/after checks :351–356 связывают source closure, runtime, H/P/READY, helpers, F2 review и references. Actual Git HEAD/status не проверяются guard: Root обязан зафиксировать их перед/после target; JSON attestation не является аутентификацией от другого процесса того же пользователя.
* R1b :312,326–334 различает construction attempted/unknown и запрещает competing read/close; assigned live collector :398–401 принудительно завершает guard без отмены watchdog. `finish(2)` и raw length/hash readback проверяются до capture verdict. B1 относится к другой, known-not-attempted ветви.
* R2 :274–285 записывает N/A только после предшествующего `Popen.poll()` terminal returncode; любой attempted live RSS None немедленно задаёт stop reason и остаётся в итоговом отказе :369–370. Требуется хотя бы один valid sample; missing RSS не заменён нулём.
* Wall90/early78, affinity1CPU и RLIMIT_CPU90, sampled RSS1GiB/TMP32MiB, raw2MiB заданы явно. Cleanup ограничен своей process group/Popen, watchdog остаётся до terminal collector. Это не hard RSS/disk quota, не доказательство transient peak, не запрет escaped descendants и не гарантия CPU всего дерева. Aggregate180s/4MiB, concurrency1, no rerun и глобальный счётчик остаются обязанностью Root, не выдуманным локальным ledger.
* Root handoff :218–223 связывает meaningful source/guard review, predecessor, budget и source files; guard не создаёт CP/approvals. Нет требования pure PASS. RED прогноз97=2literal+95call-phase assertion, GREEN прогноз97PASS не превращаются в observed verdict: :243 оставляет outcomes null, :384 требует independent complete97case review.

## Identity и история

Четыре входных SHA совпали с заданием:

| Вход | SHA256 |
| --- | --- |
| guard-v1.py | `5aa294ebcd86969d1bef07f1d108fd607e250978170641e4609d9d5ebb9a09e4` |
| plan-v1.json | `2260d9cb6dfe5e7695968a3287cad7dc87a109e0e16447221dc9534484b39da5` |
| report-v1.md | `c86aa27e369ad5b0b6137667476de22f622a3aa7cea593c2e6051dcbfd5c0471` |
| identity-v1.json | `0b335c27ead7ff0146a0cd5e08f6c738712e7b293e9932778b0ccc227972480f` |
| RawCapture helper | `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` |
| sampler helper | `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e` |
| lifecycle reference v7 | `33c0dcdbe74e1ad67d2e1fd208443c16619abcdac18c66518c8a3e40ab38dbd6` |
| frozen F2 | `995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d` |
| accepted F2 review | `c855f328402a217225b13fda3821000a8a6e55ed6894235e42b57802f3e69ec9` |

Selected Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` HEAD `107bac5697b37cf0e47c3feb44883a907837645c` и все8 recursive gitlinks подтверждены read-only. В момент чтения Root status уже содержал modified execution/checkpoint.json и4 untracked execution evidence/publication files; это не source diff guard, pristine root не заявляется. Candidate `/tmp/qcl-sci12-math-results-worktree` HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`, status только `?? tests/test_equilibrium_map_math.py`, recursive submodule status пуст. Первое чтение Git/архитектуры было в исходном общем cwd HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` с прежним dirty docs; этот checkout не принят за execution Root и не менялся review.

Predecessor receipt `/tmp/qcl-DOCS-ROUTING-GREEN-1/receipt.json` SHA `ea7d990e99e87834148d10b8c7ec7c3e0ac0c701c152de967b6bbacb45d66cf3` сохраняет consumed87→88, FAILED/exit1, complete24575B raw, 41valid/0unknown RSS. Hash original.log `f86a8761f4aac28e7798d14c76c2e8a9fe27c85f61daa4d093a21b4f4ac19b30` совпал; содержимое полного raw здесь не рецензировалось повторно. Math88→89→90 остаются prospective, C08source8/8 не менялся. Никакого reset/rerun или new counter reservation review не создаёт.

## Учёт и отклонение этого review

Только text reads, read-only Git, SHA/size, source walkthrough и два новых /tmp review outputs. Scripts/import/parser/compiler/pytest/numeric/SCBA/HDF5/network/target0; product/index/CP/READY/counter/source writes0. CPU/RSS/physical I/O не измерены. Один поиск `rg` по `.venv/lib/python3.14/site-packages` с glob `*.py` был шире необходимого; фактический объём прочитанного содержимого неизвестен и мог превысить разрешённые2MiB review reads. Это отклонение сообщено Root, поиск не повторялся; within-envelope или resource PASS не заявляются. Tool output был ограничен; одно text output было усечено, оно не используется как полное свидетельство. Исходники самого guard и обоих helpers прочитаны полностью отдельными неусечёнными выдачами. Доставленные review files не являются исправлением guard.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Known-not-attempted collector сохраняет emitted raw | guard309–313,317–341; sampler39–41 | На exception пути pipe не читается; execution0 | изменить |
| UNKNOWN ownership и live RSS не маскируются как успех | guard326–334,274–285,369–370,398–401 | Только source reasoning | сохранить |
| Routing/source/stage связываются с reviewed bytes | guard96–128,200–231,301–310,351–356 | Root semantic gates внешние; Contracts actual origin неизвестен | сохранить |
| RED/GREEN и scientific acceptance получены | execution artifacts Math отсутствуют | Calls и science не выполнялись | данных недостаточно |
| Review прошёл resource envelope | Broad site-packages rg, content read unknown | Не измерено; возможное превышение2MiB | данных недостаточно |

STOP: B1 требует узкой source correction; данный review не даёт execution READY.
