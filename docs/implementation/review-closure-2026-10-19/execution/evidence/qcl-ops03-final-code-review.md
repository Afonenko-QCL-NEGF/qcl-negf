# OPS03 exact repair — final code recheck, runtime gate incomplete

**Вердикт: R1 representation repair ADDRESSED static; CP-CODE NOT READY.** GREEN2 прерван harness guard_exception, поэтому полного required test result нет. Это не observed product regression и не product PASS.

## Exact source repair

Самостоятельно проверен diff frozen full patches DIAG1→GREEN2: кроме Git blob metadata изменены ровно три expressions в ops/application_release.py. Они добавляют fresh `dict(bindings[name]['identity'])` в controller-local verify_controller_authority :2781, check :2797 и fleet_health :2836. Их source trace/необходимость установлены `/tmp/qcl-ops03-diag1-review.md` SHA4a7786f9a273c9813c95e31bd478ff8e03ab3f8efa87ea76dfe450c79a7878c6.

Canonical `probe`/bind_node_observation остаётся immutable; `_activate_owned` получает исходный proxy и accepted once-only binder сам делает protected copy. `identity_value` остаётся dict-only; no None fallback, new observer/trust root/flags, skipped node checks либо authority downgrade. Local authority→helper→check→controller fleet-health strict-input representations теперь source-compatible; реальное достижение всех stages этим чтением не утверждается.

Hashes независимо пересчитаны:

| Input | SHA-256 |
| --- | --- |
| GREEN2 full patch, 190821 B | db537a222ef74b72b49d6521c340445b00465bf2199f38377d29f5865c275498 |
| ops/application_release.py | 1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0 |
| ops/worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |
| tests/test_application_release.py | f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21 |
| tests/test_worker_lifecycle.py | 7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b |
| tests/test_worker_shutdown_intent.py | 53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3 |
| author GREEN2 candidate report | 4f72943c4cf3f76a5eb26aa382f4dfd1380e76b4c83061528bbc35c0358f6ecf |

Tests byte-identical independently reviewed DIAG f560; therefore R2–R5 corrections/negative assertions, O01–18/LI01–10 and bounded diagnostic messages не изменены repair. Worker bytes unchanged. Baseline Platform6c5b11f3c74d44fed8b2c159f890b83e0b5456b9, accepted B scope прежний. Это narrow recheck, прежние source controls не переаудировались глобально.

## Actual GREEN2 outcome

Root `/tmp/qcl-OPS03-GREEN-2/receipt.json` SHA0f230716871aff0abcb749289aeab3cd413a90b453645eaeb4ffc0ae68a54ade; original.log SHA03a77fc8fe616a35134e8c35e252aace6bea37480f6891a20d745ace74e35464 (15 B); guard-error.txt SHA3d3401bb9303b090605e1dd80196a029331e542e73cc8d106aaf8f32ce80ba31 (809 B).

Receipt связывает все три exact fixture hashes, Python harness v4 SHA60f1e75cad84047e6a9322dab4d2531ca50713bac4893956bd6d9c68a654c38d и full selected command. Exit−9, wall1.964s, sampled RSS75075584 B, sampled TMP22604 B, stop_reason guard_exception, raw_capture_complete=true, raw_capture_error=null. Log содержит только 15 progress dots; итоговых counts/assertion outcomes нет. Dots не заменяют completed test denominator.

### Новый blocker H1 — non-atomic temporary sampler

`/tmp/qcl-python-targeted-run-v4.py:59`:
`sum(p.stat().st_size for p in temporary.rglob('*') if p.is_file())`.

Между is_file и stat обычный atomic publisher удалил/переименовал свой temp; второй stat получил FileNotFoundError для `/tmp/qcl-OPS03-GREEN-2/tmp/.../runtime/tmp...`. Outer guard exception path корректно killed/drained child и сохранил original exception/receipt. Следовательно packet outcome interrupted-by-harness, не failed assertion product; product test denominator unknown. Источник raw output не потерян, overrun=false.

Я пропустил эту ordinary file-lifecycle race при прежнем source review harness. Проверка raw capture тогда не обнаружила отдельный sampler defect; прежний review не доказывает race-free enumeration. Нужен отдельный frozen harness repair review перед любым новым packet.

Cheapest narrow correction contract: sample each discovered entry через один stat/lstat и использовать тот же result для file-type/size; tolerate только concurrent ENOENT/FileNotFoundError данного observation (включая directory enumeration disappearance), не permission/IO/other guard failures. Такая выборка остаётся sampled, не hard disk quota/peak proof. Сохранить full raw collector/finally/fallback/write-all/post-drain-overrun и unknown outcomes; не менять product/tests для устранения monitor race. Проверить source exact delta и отдельно finite attempt admission/counter у root. Этот report не запускает и не разрешает новый автоматический rerun.

## Решение и сохранённые границы

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Три strict observation boundaries исправлены без authority weakening | Exact patch delta и unchanged canonical binder/schema | Только static; full runtime interrupted | сохранить |
| R2–R5/O/LI controls сохранены | Byte-equal reviewed f560 + unchanged other tests | Required suite result пока отсутствует | сохранить |
| GREEN2 доказывает product failure/PASS | Guard traceback, exit−9, 15 progress dots | Test denominator unknown | данных недостаточно |
| CP-CODE закрыт | Full required runtime evidence не получен | H1 и separately bound final packet нужны | дополнительно измерить |
| Native/OS/bootstrap/protected prepare role/CR04/full CI/science закрыты | Такого evidence нет | Все прежние residuals и independent gates открыты | данных недостаточно |

Historical RED1/RED2/GREEN1/DIAG1/GREEN2 сохранены: пять consumed calls, counters не сбрасываются. Reviewer не исполнял tests/imports/helper/build/Git/native, не редактировал source/harness; только source/hash/receipt inspection и запись этого /tmp report. До нового concrete root checkpoint/admission не продолжать test loop.
