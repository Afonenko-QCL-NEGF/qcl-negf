# SCI05 — независимый narrow review последней syntax correction

2026-10-19. **APPROVE source-only для exact трёхпробельной correction; eligible для coordinator C08 call2 после обычного fresh BIND.** Новых source findings в этой узкой правке нет. D2 не переоткрывается, полный третий contract/code cycle не проводится. Успешный Julia parse, численные assertions и scientific acceptance этим review не установлены.

Scope≤10 min /1 CPU/1 GiB/read≤1 MiB/output≤32 KiB. Сначала прочитаны original failed raw/receipt, затем actual diff/исходник и hashes; author report прочитан последним. Единственный новый файл — этот review. Проверяющий не менял продукт, harness, original evidence или Git; Julia/parser/import/tests/build/install/network/server/solver calls=0, дополнительных C08 calls=0. Подагенты не создавались. Использован ранее прочитанный `qcl-physics-audit` в source-only границе.

## Identity и original failure

Owning Core `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`: фактический HEAD `90f1048d290d6ec9518754e288333c694fe874de`; `git status --short` содержит только modified `test/numerics/final_audit_evidence.jl`; recursive submodule status пуст. Никакого другого tracked Core diff нет. Source tree identity на HEAD из frozen correction identity: `33d66e0539f254a1492a37be64bc826b83e84b7d`.

| Проверенный артефакт | SHA256 |
| --- | --- |
| `/tmp/qcl-SCI05-C08-CORE-1/original.log` | `7bf8efd9db1986388edb93f2918266e105d03bf34566574283bf455b4fb671bf` |
| `/tmp/qcl-SCI05-C08-CORE-1/receipt.json` | `72a3d601d394a8be429022f63226eb5102785411e476f4cd9ce7bd80ebe094aa` |
| `/tmp/qcl-sci05-syntax-correction.patch` | `fd9b32d0c90dd54188fe101cd5e234e6525373002d08e7adba958967230d0ce8` |
| `/tmp/qcl-sci05-syntax-correction-identity.json` | `fb6d6e8bf797d26f26963b7fc10d910638db0aed714e2c23d1c32d6dc000515c` |
| `/tmp/qcl-sci05-syntax-correction-report.md` | `6b604e1d680a3b87d4757ac746de11f032556a7eb67d61b515ef7470a92c189d` |
| Accepted unchanged harness `/tmp/qcl-julia-c08-run-v3.py` | `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112` |
| Test before | `6a2e954230c119a92e11e70c5bc8d31376fc06e209faa907429b9f6ee13455b5` |
| Actual test after | `d4ac564013d46021a84b323338635f6860f16d1aa76e4b417c4aaf64debf64c4` |

Original log явно фиксирует `ParseError` в `test/numerics/final_audit_evidence.jl:172:64`, в выражении `2.0^-20.*(...)`, с сообщением `ambiguous . syntax; add whitespace to clarify`. Stack относится к top-level include этого файла; output численных assertions отсутствует. Receipt подтверждает этот exact before-test SHA, accepted harness v3, exit1, wall2.238s, sampled peak RSS400576512 B, raw output1253 B, raw_capture_complete=true, без guard/capture/output errors. Это failed C08 invocation1, а не numerical RED assertion или доказательство проблемы физики. Original raw/receipt hashes совпали correction identity и не переписаны.

## Точная правка и семантическая граница

Actual `git diff` совпадает с frozen patch и содержит ровно три вставки ASCII space:

| Строка | Before → after | Назначение прежнего control |
| --- | --- | --- |
| 172 | `2.0^-20.*` → `2.0^-20 .*` | Raw-vs-mixed Σ mutant с прежним factor2⁻²⁰ |
| 303 | `1.1.*` → `1.1 .*` | Observed Poisson output mutant ×1.1 |
| 664 | `0.125.*` → `0.125 .*` | Mixed-step rU mutant с прежним α=1/8 |

До правки38516 B, после фактически38519 B. `git diff --ignore-all-space --exit-code -- test/numerics/final_audit_evidence.jl` успешен с пустым diff; обычный diff показывает только указанные три пробела. `git diff --check` успешен. Не добавлено/удалено ни чисел, ни операторов, ни operand, ни assertions.

**Вывод о причине:** вставки отделяют конец числового литерала от dotted multiplication `.*` именно на границе, указанной original lexer/parser diagnostic. Line172 — наблюдённый отказ. Line303/664 имеют тот же статический pattern numeric-literal непосредственно перед `.*`; они исправлены в том же узком lexical scope. Отдельных runtime failures этих строк и успешного нового parse здесь не наблюдалось; такой результат нельзя получить из whitespace comparison.

**Вывод о сохранении oracle:** α, amplitude×1.1, independent expected quantities, interval graph, γ bounds, D2 overflow status mapping, thresholds, units, history/context/availability inventory и predicate/assertion branches не изменены. Никакой oracle assertion не удалён и не ослаблен. Нормализованное whitespace equality — вспомогательное свидетельство; решающим для scope является обычный трёхстрочный diff с unchanged числовыми выражениями. Новых physical/model/evaluator решений нет.

## Остальные пять принятых файлов

Фактические SHA совпадают принятым CPP2/HEAD90f1048; `git diff --name-only` содержит только test:

| File | Неизменившийся SHA256 |
| --- | --- |
| `src/QCLNEGF.jl` | `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |

Следовательно, source acceptance прежней production instrumentation и namespace correction не изменяется этой правкой. DEV05 и все прочие tracked Core файлы отсутствуют в diff. При этом выбранный Core остаётся dirty ровно этой разрешённой test overlay, которая должна быть связана с call2 по after SHA, а не только по прежнему HEAD.

## Eligibility, budget и STOP

Coordinator C08 call2 может использовать exact after-test SHA и прежний accepted harness v3 в remaining finite grant. Требуются обычные source/admission/argv bindings; этот review их не подменяет и test сам не запускает. Consumed=1/8 по first receipt и поручению; additional calls этим review=0. Оставшийся test budget не создаёт новых corrective code rounds: это последний согласованный corrective round. Если после call2 обнаружится семантический failure, он сохраняется как concrete blocker; никакого автоматического third edit/test loop.

Hard realtime/RSS/TMP/output limitations accepted harness review сохраняются. No numerical pass/SCBA convergence/physical gates/discretization/experiment claims. Author report не заявляет runtime pass; независимая source оценка с этим согласуется.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Original lexical failure адресован минимальной правкой | Raw ParseError172, exact3 ASCII spaces в172/303/664 | Новый Julia parse не выполнялся | сохранить |
| Oracle/математика/допуски не ослаблены | Actual three-line diff, +3 B, whitespace-only comparison | Numerical assertions ещё не измерены | сохранить |
| Остальные пять accepted source files сохранены | Actual SHA equality и single-path Git diff | Call2 обязан bind dirty after-test SHA | сохранить |
| Exact correction source eligible для call2 | Narrow independent review без новых findings | Coordinator-only remaining grant, без дополнительных code rounds | дополнительно измерить |
| Runtime/scientific acceptance достигнута | Такого evidence нет | First invocation только ParseError; новый runtime здесь отсутствует | данных недостаточно |

STOP после этого отчёта. No execution, code edits или Git mutations проверяющим.
