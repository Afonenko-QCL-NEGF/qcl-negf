# DOC06 RED fixtures v2 — narrow independent high R1 recheck

**PASS_SOURCE — R1 закрыт.** Три lexical cap controls теперь причинно различают under/over границу при сохранённой healthy selected schema. Других изменений вне узкой correction не найдено. Exact packet готов к Root binding и sole first RED; tests/imports/parsers не выполнялись, RED/GREEN не наблюдены.

## Frozen identity

| Input | SHA-256 |
| --- | --- |
| Current `/tmp/qcl-doc06-worktree/tests/docs_static_slice_test.ts`,27558 B | `13c33da622b4d1c2e779dda4221057617b8fbd10942824dec52cf78e19fe80f2` |
| v2 report,7520 B | `a447c77653f36dc03b8a0d11c3b11c7462f85e9dc3de1371076e7cabc1bc14c3` |
| v2 identity,1101 B | `5e3429ed821849053bdaeb44e491f58f0bc20c820c1c9b2032bfdfea3117bc5b` |
| v1→v2 delta,3724 B | `dd0912fbedf4045405a37a7ad2f6ae05e6e290848cc66ac89a92c6bd222cf3ed` |
| v2 full patch,28240 B | `a18068a82bea5d105553af601be1428121be01e9c67fafa90ebfa5f6c3600cae` |
| Preserved v1 test,25901 B | `3714933c7f34dc6da97db1189422e9381cf6d73589215e5692845402a260eb50` |
| Preserved v1 full patch,26555 B | `28103817025c8d10c1da5aa68f511bd9c360cb329e6d08fe1701ce0480b9ad13` |
| Preserved v1 report,12103 B | `4571d5d56d602105a8d730f9ba15036114ee8b5538b7c6de4f98922ced4d5697` |
| Unchanged DOC06 harness | `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e` |

Worktree status по-прежнему только new test. Исходные D34b80d / D-R385c2ae4 / v1-R603b5edd и harness-R293be95e сохраняют свои scopes. Они здесь не переаудируются и не переписываются. Canonical pointer erratum не меняется. Полный independent text diff v1→v2 совпадает по содержанию с frozen delta: удалены ровно три прежние malformed cap rows, скорректирован комментарий и добавлены helper + три paired cases. Удалений/ослаблений остальных assertions нет; полный patch только хеширован, не применялся.

## Проверка причинности R1

`schemaWithUnusedExample(fragment)` берёт прежнюю healthy `schema()` и добавляет `$defs.unused.examples=[fragment]`. Исходный production `$ref`, object/required membership, integer/minimum1 и отсутствие schema default сохраняются. Это невыбранная annotation branch; её payload не становится Fact text или выбранным default.

Обе копии — PATHS[6] packaged и PATHS[7] canonical — получают один и тот же constructed string. Поэтому packaged mismatch больше не может объяснить over refusal. Under и over используют sources(79,31), а не constant64 fallback.

| Lexical bound | Under | Over | Почему другие caps/shape не маскируют |
| --- | --- | --- | --- |
| depth≤32 | 20 вложенных arrays; с wrappers≤24 | 34 arrays; с wrappers≥38 | Healthy selected path цел; strings/tokens/file bytes малы |
| string≤16384 B | 16000 ASCII x | 16385 ASCII x | Строка только в unused branch, не в Fact text; shallow/small token count |
| tokens≤32768 | 101 zero literals | 32770 zero literals | Over превышает даже numeric-only token count; safe finite zeros, shallow nesting, нет длинной строки |

Largest token schema по конструкции меньше67KiB/file и128KiB cap. Две копии плюс tiny остальные fixtures существенно меньше512KiB aggregate. Strings/depth cases меньше этого максимума. File count остаётся9; source receipt содержит только fixed paths/size/hash и не растёт с содержимым на десятки KiB. Таким образом другой заявленный source/file/count/receipt/docstring/Fact cap не обязан первым отвергать эти конструкции. Это статический расчёт формы/размера, не измеренный runtime/IO или JSON parsing.

Каждый under sibling требует non-refused projection, independently literal selected `{type:'integer',minimum:1,required:true}`, status known и exact `/$defs/production/properties/energy_chunk`, null/not_assigned schema default, typed79 и explicit31. Adapter, blanket-refusing unused branches, больше не проходит. Over требует refused при той же selected shape и меняет только целевой payload относительно пары. Таким образом исходный malformed/missing-path masking R1 устранён без production-derived oracle и без нового API/reason contract.

Номинальный count54 сохраняется: три Deno.test registrations заменены тремя paired registrations, внутри по два serial fixture runs. Существующая owned TMP cleanup/evidence граница не менялась. При future runtime подставляемые receipt sizes/hashes по-прежнему формируются actual fixture bytes.

## Сохранённые ограничения и execution gate

Count13 case остаётся одновременно duplicate-path input; это ранее известный **неблокирующий coverage limit**, явно сохранённый v2 report. В fixed9 allowlist невозможно добавить13 разных допустимых paths. Не вводились новые refusal reasons, расширение allowlist или claims отдельной count-guard причинности.

Ни один численный limit/unsupported policy/default-origin distinction не ослаблен. Остальные controls сохраняют ранее reviewed v1 source verdict, но заново глобально не проверялись. Harness hash совпадает с ранее PASS_SOURCE, его source review повторно не открывался. Call readiness требует exact corrected fixture placement в fixed Root, runtime/helper/source/operation binding и внешнего finite counter. Нельзя считать отсутствующий в fixed Root test intended missing-adapter RED. Generic CI routing/full CI этим review не admitted.

Root DOC06 calls по поручению0/2; reviewer calls0, counter не изменялся. Никакой automatic third phase/test loop или product implementation этим PASS не разрешаются. Expected first missing-adapter RED и future GREEN должны иметь original raw/receipt и собственную классификацию; этот source PASS не является результатом исполнения.

## Named read ledger

Envelope≤10min/1CPU/1GiB/read2MiB/output32KiB. Полный размер named file списан даже для early-quit extract; cached tool/context использован для повторного анализа.

| Group | Upper bound B |
| --- | ---: |
| v2 report+identity text | 8621 |
| v2 test/report/identity SHA pass | 36179 |
| v2 selected text extract, full file charged | 27558 |
| Full frozen delta | 3724 |
| Independent diff old+new test | 53459 |
| SHA pass v1 test/patch/report, v2 delta/full patch, unchanged harness | 106038 |
| **Total source-read upper bound** | **235579** |

Metadata/Git и собственные review artifacts отдельно; physical I/O/RSS не измерены. Reviewer target code/import/parser/tests/network/build/children/product edits/checkpoint/Git mutations/science/C08 —0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 malformed-shape masking закрыт | Exact delta, healthy unused branch и paired assertions | Source-only, runtime ещё впереди | сохранить |
| Остальные controls и harness сохранены | Independent v1→v2 diff, v1 artifacts и H hashes | Не повторный full review | сохранить |
| Count13 независимо доказывает count guard | Construction с duplicates не менялся | Known nonblocking coverage limit | данных недостаточно |
| Root first RED source готов | Exact v2 packet + existing harness PASS | Actual placement/binding/call отдельно | сохранить |
| RED/GREEN/native/public/science доказаны | Новых execution receipts нет | Calls reviewer0 | данных недостаточно |

**STOP. PASS_SOURCE exact v2 R1 correction; Root sole first RED после binding.**
