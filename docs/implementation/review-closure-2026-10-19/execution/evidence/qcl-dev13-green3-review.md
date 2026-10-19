# DEV13 final R4 re-review — CP-CODE

**Вердикт: scoped CP-CODE PASS** для frozen bounded Portal software implementation. R1–R4 ADDRESSED; source blockers в данном narrow final review не обнаружены. Root GREEN3:169passed. Это не native AiiDA/process-exit/full CI/deploy/scientific acceptance. Reviewer target imports/tests/build/runtime/Git mutations/source edits не выполнял.

## Exact binding и порядок проверки

Сначала независимо прочитаны actual incremental source, surrounding dispatch/lease paths, regression fixture и сравнение frozen packages; затем author report, RED3 и completed GREEN3 evidence.

- Portal HEAD `fa80b5b5920dc16dfb911d164939b3d23e6be186`.
- Full frozen `/tmp/qcl-dev13-green3.diff` SHA256 `c0675261cee2db5328bf1d95b7849d917c7643e0b22eb2b674bd390e18676336`,101,221B. Current tracked diff + new-file diff reconstructed independently byte-equal.
- Incremental `/tmp/qcl-dev13-r4-fix.diff` SHA256 `7e133368d558e2cbb7da93efb17118ddaeadfe717643483671a70c63a463dc63`: только `_release` queued-work resolution и Future signal вне Condition.
- Actual `service.py` SHA256 `b4dd4da7da85bdfca7993da3928dcf720f78e4f3ca8e70e27a2df36b79d01ef3`; current actor test `3eeb041b5d673e5e3fbdc5d48cbc094c91874a9fc2610a3b24022c62011b1f37`.
- Author `/tmp/qcl-dev13-green3-report.md` verified SHA256 `9c671499d5f751adeea182cf342da94de73d64d93399fe385fef1a106a302c82`.
- api/exports/settings production bytes unchanged from GREEN2. First877 lines of prior actor fixture remain exact prefix of current file; added R4 tests не переписывают R1–R3/ASGI controls. Все9 original finite ASGI assertions сохранены, прежние4 parameter cells не менялись. `git diff --check` exit0.

## R4 source reasoning

`src/qcl_negf_api/service.py::_release:409–439` помечает lease closing и в том же Condition critical section, который защищает owner dequeue, находит и удаляет **только** queued messages этого lease. Перед освобождением lock их state=expired, error=обычный ValueError("Artifact reader is closed"), `_expire_lease` снимает unstarted outstanding. Ни backend, ни handle exit здесь не вызываются.

При close-wins ни normal dispatch, ни queued deadline expiry не могут позже найти старое сообщение и обратиться к удалённому registry entry: mailbox entry уже снята до priority cleanup. Отдельный Future получает сохранённый terminal message state/error и не остаётся orphan. При dispatch-wins сообщение уже отсутствует в queue, его running outstanding не сбрасывается; actual owner return снимает его по прежнему R2. Close не пытается прервать running backend.

`self._signal(cancelled)`425 вызывается **вне** Condition/RLock; synchronous Future callbacks не запускаются под metadata lock. Последующий wait снова берёт Condition и использует тот же remaining absolute deadline, не начинает новый budget. Повторный close не создаёт второй exit; registry/context cleanup остаётся owner-only. Другие messages и leases не отменяются.

Это закрывает missing-lease KeyError обоих вариантов read/seek без `.get` fallback, suppression или forced unload. R1 dispatch fence, R2 running counts и R3 canonical report event сохраняются неизменными и входят в текущий selected runtime set.

## Distinct RED и current GREEN

Root `/tmp/qcl-DEV13-RED-3/receipt.json` + original raw подтверждают **2 expected failures** до production fix: queued read и queued seek получили KeyError вместо local closed-reader ValueError. Receipt exit1/wall3.027s/sampledRSS56,143,872B/log10,230B/stopnone. Tests после RED3 сохранены с тем же frozen hash по root witness и current hash verification; receipt сам по себе не содержит code manifest, поэтому не подменяет эту binding chain.

Current test `test_queued_reader_close_cancels_unstarted_work_without_losing_other_leases` явно подтверждает independent R started, queued reader под Condition, close до release; затем backendcount0 для отменённой операции, expected ValueError, primary single exit, **no premature unload**, healthy actor read, чтение через другой ещё открытый lease, оба once-only exits на owner, final completed и один unload. Parametrized read/seek. Test-local isolated OWNER_GUARD нужен для сохранения negative crash без загрязнения следующих fixtures; finally ожидает actual owner Future. Catch KeyError только в negative-fixture cleanup не является test success: distinguishing assertions до него требуют ValueError/healthy owner/independent lease и RED действительно fail-ил.

Root `/tmp/qcl-DEV13-GREEN-3/receipt.json` и original raw проверены после появления completed receipt:

- Пять файлов: actor_deadlines,service,stream_disconnect,exports,api.
- **169 passed in7.99s**, exit0, wall9.682s, stopnone; обе R4 cases включены.
- Sampled process-tree RSS200,962,048B, stdout/stderr260B, tmp0; selected .venv Python3.14 locked setup, no sync/download.
- Limits90s/1CPU/1GiB sampledRSS/16MiB tmp/2MiB output. RSS monitor50ms не hard cgroup proof; эти числа не native production SLO.
- Root сообщает шестой invocation в разрешённом finite DEV13 packet. Reviewer runs=0; дополнительный rerun не нужен и не подразумевается этим PASS.

## Сохранённые границы

PASS относится к прочитанному implementation и selected synthetic backend/handle/API fixtures на frozen source. Existing healthy API,4 finite ASGI cells,2 stalled post-header deadline cells, R1–R3 regression cells и R4 controls входят в169passing set. Healthy finite response требует actual close; stalled response возвращает bounded caller abort/deferred cleanup и не утверждает backend termination.

Это не полный exhaustive fault matrix: ранее отдельно отмеченная exit/unload-failure coverage не превращается в measured fact этим набором. Source предусматривает failed/once-only behavior, однако отдельного native failure-path/process-exit/real-profile receipt нет. Uninterruptible backend/filesystem work может пережить caller deadline; close stopping не называется completed. Нет нового durable exactly-once/reconciliation store, auto retry/reset или cross-crash promise. Old failed source snapshots/RED receipts сохраняются.

Новые production tests не запускались reviewer. Никаких native AiiDA daemon/profile/SSH/Slurm/services, frontend browser flow/full CI, model/SCBA/Poisson или experimental gates данный report не закрывает. DOC12 TEXT acceptance остаётся contract evidence;169synthetic tests добавляют software evidence только указанного scope.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R4 queued close безопасно отзывает unstarted work | atomic source +2semanticRED→GREEN controls | synthetic handles, no hard backend kill | сохранить |
| Running counts,mutation fence,late report diagnostics сохранены | prior source checks,unchanged877lines,selected169pass | process-local semantics | сохранить |
| Other lease и healthy API продолжают работать | R4 explicit independent read/lease assertions +existing suite | selected fixtures only | сохранить |
| Frozen DEV13 software CP-CODE готов | exact package hashes/current equality +169pass receipt | no exhaustive/native/fullCI claim | сохранить |
| Native/process-exit/scientific/release acceptance | corresponding measurements отсутствуют | unit/API fixture PASS не заменяет их | данных недостаточно |
