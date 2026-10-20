# Независимая проверка фактического CHECK4

Вердикт **PASS_SOURCE_RESOURCE_GATE** для CHECK4 и mixed prerequisites FORMAT3(v8),LINT3(v8),CHECK4(v9). Блокирующих замечаний по прочитанным результатам нет. Compiler exit0 и resource gate проверены отдельно. Unit E1, scientific/native acceptance и устранение причины CHECK3 не заявляются.

Рецензент читал сохранённые JSON/raw, исходные identities и Git metadata; разрешённая metadata-only PythonJSON/SHA постобработка не импортировала и не исполняла проверяемый код. Scripts/compiler/tests/network/solver/re-execution/children0. Записаны только этот отчёт и identity в `/tmp`; CP/READY/product не менялись.

## Фактическое свидетельство

`/tmp/qcl-DOCS-ROUTING-SOURCE-CHECK-4/receipt.json`:3576B SHA256 `bdff66bb2d42b02884ce4a21eda0339c8e8729c7e72faeb7b71d74b2aad7e71d`. Receipt verdict CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW; target_calls1, attempt_consumedtrue, child exit0, stop_reason/guard_error/raw_capture_error null. `original.log`:88B SHA256 `04d40e18cad60bff4992e517b0a3b5e8bdab983c1944034cd919f20f827b8f91`, фактические bytes/hash совпадают с receipt. Raw содержит две строки Check для helper/fixture; raw_capture_complete=true, collector_construction_attempted=true, collector_terminal=true, overrun=false.

Resource gate: wall1.688758397998754s≤120s; RSS attempted34=valid34+unknown0, valid≥1. N/A1 имеет отдельный proof Popen.poll_returncode_before_RSS_attempt с тем же PID3094878, returncode0 и elapsed1.681994255981408s. Он не посчитан valid RSS. Sampled RSS285835264B<1073741824B; sampled ownedTMP3011380B<16777216B, TMP36samples, initial220/final3011380B. Exact limits:120s, affinity1CPU, RLIMIT_CPU120s, RSS1GiB/TMP16MiB/raw2MiB. Это sampled limits, не hard quota, startup peak или полная transient RSS трасса.

RSS_failure_diagnostics=[]; events_seen/dropped/capture_errors0, truncatedfalse, birth_identity not_read_by_RSS_sampler. Следовательно этот запуск не создал различающего failure свидетельства. Причина CHECK3 остаётся UNKNOWN; race/zombie/causefixed не установлены.

Source before=after=actual current files: helper `12fbb1d8c754536135e7b919ca14a465532bd3910bdff7f68ef6fdb129376bab`, fixture `a629e366cdebacc9d6ffbef1458990cf00232d99ca3cb1668696c169fc4a1164`. Config actual SHA `a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce` совпадает. H/P/wrapper actual SHA соответственно `e02576c6b421b158a00a570ca729b076737d47c1e79111606d15fb60a2cba01e` / `e32f4b534b928cef44cc8e9f35f242e979752b12b70e9eea687c5cca3cc3b2af` / `1dd84dcdf977f458b960e6dd78dbb100e4d3c3c83a60e29430d630a455f91f1a`, равны принятым source review identities.

Exact argv: pinned deno2.8.3 binary, `check --config /tmp/qcl-docs-test-routing-worktree/deno.json --no-lock --no-npm --no-remote ops/docs_tests.ts tests/docs_test_routing_test.ts`. Cwd exact isolated worktree. environment_clear=true; только DENO_DIR/TMPDIR/HOME, каждый в private CHECK4 owned-tmp. Runtime SHA в receipt равен frozen `cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c`; огромный runtime binary повторно не читался в рамках этого review. Test_registration=false и observed_engine_tests=null: source check не доказывает232 unit outcomes.

## Mixed source identities и история

FORMAT3 receipt SHA `26228b8059235d0c6f37ac32a08a4a65a3af5976058c34913f9ba83f0629b714`; raw84B SHA `16730458a0bb58d3ac5d7f9b94f775368ede6566c55f85dc0ccde4316bddd4d6`; counter8→9cap11. LINT3 receipt SHA `fc42be7624a2af8238a5bcc5059ef1b7469c4e79cad7fd661b38131433ebe5a8`; raw16B SHA `0ac7c2631e5af776de63c5209860d6c55979825c853537ecee2289736c3856fd`; counter9→10cap11. Оба фактически прочитаны, bytehash/raw complete/terminal/error/env/limits/exactargv проверены; каждый valid3unknown0 и отдельный N/A1. Они сохраняют собственные v8 scope/H5cecec/P813afe и wrappers878571/1410db; CHECK4 использует currentv9 identities. FORMAT3 source_before остаётся исходным unformatted ancestry, source_after=S; LINT3 before=after=S. Они не исполнялись повторно.

Accepted format+pure CPP actual SHA `8ac8702532f17c9fc43149578cfa64bc477bd69679bf5b403d7174b1c615c3b3` совпадает с READY accepted_cpp/format_binding. Failed CHECK3 receipt SHA `a399281f3159ffd88cc014a5fd8504110fb8c272e21472cab5404e3ff67eb05a` неизменён;32valid1unknown, consumed FAILED остаётся historical failure. Новый успешный CHECK4 не переклассифицирует CHECK3.

## Root и полномочия

Root engineering plan SHA `eaf8a1f9cc2930fce32f97cca61a638190cd52f1b3e453d03b201b42cb22465d`: отдельный finite append1call11→12cap12,120s/1CPU/1GiB/16MiB/2MiB, общий пакет5calls600s10MiB с единственным unused E1. READY actual SHA `ab2dd7890cc98fade3c3cdb00f780c423985508e806a17700b74adfa235c9799` совпадает с receipt; handoff actual SHA `898ad49c41dc4fbbe6d93fa7c320acf810d473290781ac9a15a8c5e4d0e5bef0` совпадает с READY. Outer SHA `c871349f78bc034433cda7d215d345e24aae38d08ee7a2aa7beb9da1bdf12af7`: wrapper_returncode0, wall2.07982763502514s, outer_failure=null, stdout/stderr empty. Эти JSON не заменяют независимую проверку outcome.

Фактический Root HEAD107bac5697b37cf0e47c3feb44883a907837645c; все8 recursive gitlinks совпадают с предыдущим review, ведущих +/−/U нет. Status содержит только прежний изменённый checkpoint и4 untracked evidence/publication файла. CP snapshot SHA `2c0d28fe4467a0a85d2397bfcbc8e7b9905e8a21f3cb5f06f60c547ab3c22502`: counters.targeted_test_total_calls90, milestone_source_tools_calls12; resource_current source used12/cap12, productcap91, targeted_test_active=null, source_tool_active=null. Фактический CHECK4 завершён известным outcome; unknown resource sample0. Routing_source_v9.state/runtime в CP ещё содержит pre-execution текст: это устаревшая summary, а не основание объявить actual result неизвестным; Root следует reconcile summary с actual receipt. E1 folder отсутствует, product90→91 остаётся уникальным unused; этот отчёт не создаёт unit READY.

В одном metadata-selection response рецензент вывел слишком много строк и получил truncation; нужные CP поля затем отдельно выбраны компактно. Не заявляется соблюдение общего output ceiling. Физические review CPU/RSS/I/O не измерены. Выполнение проверяемого harness не повторялось.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| CHECK4 source outcome и sampled resource gate приняты | receipt bdff66bb + raw04d40e18,34valid0unknown | source check не unit/science | сохранить |
| Mixed prerequisites сопоставимы | exact FMT3/LINT3/v9CHECK4 identities, formatCPP8ac870 | разные H/P сохраняются раздельно | сохранить |
| Source12/12 исчерпан, E1 product90→91 unused | CP counters, отсутствующий E1 folder | Root обязан fresh reconcile/READY перед unit | сохранить |
| Причина CHECK3 устранена | свидетельства нет, diagnostic events0 | cause UNKNOWN | данных недостаточно |
| CP v9 summary ещё pre-execution | routing_source_v9.state/runtime против actual receipt | counters уже12, action известен завершённым | изменить |

STOP review-only. Root может использовать этот exact outcome binding при собственной final READY проверке E1; дополнительных source calls нет.
