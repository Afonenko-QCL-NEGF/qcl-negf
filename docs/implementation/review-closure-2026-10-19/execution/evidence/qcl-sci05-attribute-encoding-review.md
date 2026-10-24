# SCI05-N1-EA1 — independent CP-DESIGN attribute encoding review

2026-10-19. **PASS CP-DESIGN. Принять profile A из design SHA `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206` как точное engineering дополнение для четырёх новых constant attributes.** Это явное решение об отсутствовавшем wire method/cap, а не вывод attribute dtype из D2 dataset paragraph. Bounded fixed raw value-read profile совместим с pinned scalar-String HDF5.jl0.17.4 writer. Frozen JSON schema/science/public model/old native semantics не меняются. Load-bearing design blocker не найден.

Это source/API design verdict. Ни новый Runner N1 writer, ни исправленный Results reader, ни native round-trip, ни linked-library behaviour этим review не приняты как исполненные. Human reapproval для данного разрешённого внутреннего engineering уточнения не требуется. Coordinator binds design+review hashes и готовый bounded implementation scope; review не увеличивает оставшийся C08/engineering grant.

Область≤20 min /1 CPU/2 GiB/read≤3 MiB/output≤48 KiB; единственный новый файл — этот отчёт. Сначала адресно проверены primary pinned HDF5.jl, prepared h5py, HDF5 C headers и owning Runner, затем предложенный профиль/controls. Python/Julia/HDF5 imports, arithmetic processes, parser/tests/build/install/network/native/solver calls=0; product/Git mutations=0; children=0. Данные архива не материализовались. Прочитаны только нужные source/metadata slices, не scientific arrays. Архитектурная граница: Runner пишет, Results независимо читает, Contracts/owning format задают формат; physics/acceptance не переносится в reader.

## Authority и identity

Primary frozen D2 `/tmp/qcl-sci04-design-v2.md` SHA `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c`, §8.3–8.7. §8.3 прямо ограничивает dataset record_json fixed UTF8 scalar1..65536, задаёт group@schema и три dataset attr values. Он **не задаёт** attribute dtype, width или bounded-read implementation. Candidate≤512 нигде не был принят нормой. Предложенный65536 для attrs здесь принимается как engineering cap, без изменения schema marker/version/record fields.

Actual root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`: HEAD `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`; concurrent staged/unstaged documentation, execution evidence и gitlinks (106 tracked status entries при кратком readback). Он не чистый. Actual submodules: Core `+7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`; Runner `9378396a3681c1eddf2c62f16674834fc4465583`; AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`; Contracts `+12fc26462bbab3df76904c6deb01f8c6596de7be`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; Portal `2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; Research `1eacefcd81a50e245ea9da74a0b717b33818c61e`; Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Gitlinks остаются authority, это наблюдение review, не новый lock.

Actual owning Runner9378396 и Results e2fdeda имеют пустой status/recursive submodule status. Results `/tmp/qcl-sci05-results-worktree` — conditional candidate, не normative authority. Core call5 result287/287 сообщён координатором как отдельный результат; этот attribute review его не перепроверяет и не использует как доказательство HDF5 transport.

| Primary source / binding | Проверенный SHA256 / version |
| --- | --- |
| Proposed design `/tmp/qcl-sci05-attribute-encoding-design.md` | `1b0a0e93ead396fe1b8adf37b0f50c148ac4455fd0674bc45261acba4c8ff206` |
| Prepared Julia Manifest | `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47`; HDF50.17.4 tree `26e37af34e8ccb7a8358bd8de1619c7bcb526738`; HDF5_jll2.2.2+0 tree `194d676302b9b6aa53ea1f98ae8607d5caa8de4f` |
| Pinned HDF5.jl Project | `761a141236d499d35acd70ced47a62d54bb279f5637153f278306636f7830367` |
| Pinned HDF5.jl `src/attributes.jl` | `833e769a819c5ce1b24128ca172f1c11d0e222a0c7d8bf30d3fb4ba97fa53246` |
| Pinned HDF5.jl `src/typeconversions.jl` | `1abe93196079179cfdbc1fb010a2572385f483118935f4cf1fda6d6db8932d06` |
| Pinned HDF5.jl `src/dataspaces.jl` | `9e6ccf922624d315ca4459818533b86df049ce46df8bff82b428da8607625b33` |
| Runner `hdf5_backend.jl` | `3ccd096eb9e01df4c5d320a00a15e718e027d78b94892c174fcef611d6359a31` |
| Runner `hdf5.jl` | `c946ba5fb71f035d1a0b564b561700b9a5c3360ed67bf890c668b0ced769d511` |
| Runner `point_artifacts.jl` | `81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a` |
| Root uv.lock | `db19ba9ace32c03d2b0a9da9b11b90f9f16de23c9539aa2276cd3dafd4f56336` |
| Prepared h5py `_hl/attrs.py` | `bfdbfc7c9f406aa1915c10d50e6f3d3db9acffb7aa4505b84dae39954a29d40e` |
| h5py dist-info METADATA | `e461fcf7eb9fee6242205f9225cc178455a0212d1c0cb8f997f7eebf8cd9695e`; version3.16.0 |
| h5py `tests/test_attrs_data.py` | `84bb6d21110d369a4c018ef31951e2ba5cb540e839e209dd93d380ddf16ec48f` |
| Prepared JLL `include/H5Apublic.h` | `d5cbda26036019f1eed9741a389a8f0d7feb3d4ca6312b5efec877668337397f` |
| Prepared JLL `include/H5Tpublic.h` | `7638a0441f19fe1a9494e901ec13f413c4531d9623422e844c56ec45d74bc21f` |

HDF5.jl source root `.build/local-julia-int01/depot-1/packages/HDF5/Xsdf5`; prepared h5py `.venv/lib/python3.14/site-packages/h5py`; JLL header artifact `.build/local-julia-int01/depot-1/artifacts/df5ad26ed9661e47b7b9169ae35190911fa7aaaf`. Home `.julia` HDF50.17.3 не использован как authority. Manifest/package/header identities не доказывают actual loaded native library paths; будущий runtime receipt должен отдельно связать Julia HDF5/HDF5_jll и Python-linked HDF5.

## Независимая source оценка producer и reader

Runner wrapper `hdf5_backend.jl:1–8` вызывает HDF5.jl напрямую. Existing assignments `hdf5.jl:59–61,285–299` передают scalar String instances. Pinned chain:

```text
attributes(parent)[name]=value
  → Attributes.setindex! / write_attribute
  → create_attribute(parent,name,data)
  → datatype(data), dataspace(data)
```

`attributes.jl:81–89,173–183,202–214,382–383`; `typeconversions.jl:213–218` устанавливает fixed byte size `max(sizeof(str),1)` и UTF8 cset; `dataspaces.jl:58` даёт H5S_SCALAR. String instance path отличается от `datatype(String)` и `datatype(Array{String})` на219–231, где размер H5T_VARIABLE. Поэтому предложенные literal assignments source-compatible с fixed UTF8 scalar widths35/1/6/50. `H5T_C_S1` base type используется до size/cset changes; существующий instance путь не следует заменять type-object или массивом.

Prepared h5py high getter `_hl/attrs.py:53–98` получает attr.dtype, создаёт memory type через `h5t.py_create(dtype)`, выделяет array и вызывает read, а для vlen затем декодирует payload. Он не является raw-preserving fixed-string reader только потому, что перед ним проверили width. `get_id` позволяет работать с тем же low AttrID. `H5Apublic.h:891–920` устанавливает entire attribute read с указанным memory type, без отдельного selection/DXPL argument. `H5Tpublic.h:2163–2177` прямо говорит: vlen get_size — pointer size, не длина heap data. `H5Tpublic.h:3020–3030` допускает truncation/padding при type conversion. Это обосновывает отказ от vlen и identical memory/file type вместо fixed-destination conversion.

Ни source high getter, ни HDF5 C headers не являются runtime доказательством raw byte transport на actual linked libs. Именно поэтому embedded-NUL/genuine-vlen controls обязательны до transport GREEN. Дизайн делает достаточно конкретный проверяемый API выбор без заявления hard native sandbox.

## Принятое точное engineering решение

**Область только новой группы:** `/diagnostics/final_fixed_point_audit@schema` и `record_json@{units,logical_axis_order,description}`. Другие historical/native4 attrs и их generic readers не переводятся на этот profile.

| Attribute | Exact decoded constant | L bytes | Canonical Julia width |
| --- | --- | --- | --- |
| group schema | `qcl-negf-final-fixed-point-audit-v1` | 35 | 35 |
| dataset units | `1` | 1 | 1 |
| dataset logical_axis_order | `scalar` | 6 | 6 |
| dataset description | `Versioned final fixed-point raw measurement record` | 50 | 50 |

Утверждаются следующие predicates/semantics:

1. Открыть только четыре известные required attrs, без enumeration/value read всех attrs. Для каждого получить **low file datatype и dataspace**. До NumPy dtype/value-buffer allocation проверить atomic H5T_STRING, `is_variable_str()==false`, H5S_SCALAR и shape(). NULL, `(1,)`, rank>0, compound/array/numeric/opaque отклоняются; one-element array не scalar.
2. Принять width **L≤N≤65536 byte**, cset только ASCII/UTF8, padding только NULLTERM/NULLPAD/SPACEPAD. Это новый явный engineering byte cap. Не считать размер vlen pointer/storage_size доказательством bounded payload. Не использовать candidate≤512 как норму.
3. Только после preflight синтезировать fixed NumPy `S<N>` scalar backing buffer, без object/subarray; выполнить `AttrID.read(target,mtype=file_type)` и получить все N bytes через `target.tobytes()`. Идентичный file/memory type, включая cset/pad/size, удерживается до конца read. High getter, `.get`, dtype inference/auto mtype и `.item()` до raw bytes не используются.
4. Для NULLTERM/NULLPAD удалить **только NUL suffix справа**; NUL с последующими nonzero bytes остаётся corrupt. Для SPACEPAD удалить только space suffix справа. После такого снятия padding NUL внутри value запрещён. Strict ASCII либо UTF8 decode согласно cset, exact constant equality, без surrogateescape/case folding/Unicode normalization/strip. Следовательно, `expected+NUL+junk`, prefix/suffix/leading whitespace не могут скрыться за first-NUL truncation. Constants все ASCII, padding не меняет их semantics.
5. AttrID/type/space закрываются в finally на всех success/error paths. Работать последовательно, не удерживать четыре больших raw/decode buffers одновременно. Dataset wire type/cap/JSON parser rules остаются D2 без изменений.

N=L canonical output принимается и при отсутствии завершающего NUL внутри N bytes; это необходимо для actual pinned Julia instance writer. Reader не навязывает N=L+1 только из названия NULLTERM. Padded widths вплоть до65536 также принимаются при exact logical constant и разрешённом правом padding. Это совместимость fixed wire encodings, не изменение scientific value.

## Память, metadata I/O и TOCTOU

При fixed atomic scalar type и проверенном N value buffer занимает N bytes; raw/decode copies ограничены постоянным множителем. Верхняя сумма declared logical values новой группы — четыре attrs по65536 плюс dataset65536 =327680 B. Canonical four attrs —92 B. Это **не** physical disk-I/O bound, не peak RSS proof и не новый read grant.

Metadata opens/type/space queries и read проходят через тот же caller-owned HDF5 handle на existing `_BudgetStream`; не переоткрывать filename unbudgeted. Candidate `_IOBudget/_BudgetStream` state.py32–106 считает delivered stream bytes до callback, включая HDF5 metadata traffic, отдельно от selected logical bytes. Не заменять эти counters суммой N и не подавлять budget failure в format success. Сколько реально native HDF5 прочитает/кэширует metadata, определяется runtime; whole-process memory на произвольном hostile HDF5 header из atomic-value cap не выводится.

TOCTOU boundary конкретен: preflight и raw read используют **один и тот же открытый AttrID**, его retained type/space, без повторного lookup имени через high getter после check. Buffer размер выбирается из проверенного type именно этого ID. Не использовать stale preflight одного attr и read другого reopened attr. Attribute handling остаётся внутри времени жизни исходного budgeted owner handle; IDs закрывать после read, не до него. Immutable archived-file/hash/identity contract прежнего StateReader сохраняется; concurrent writer/adversarial replacement не становится поддержанным новым trust mode. Данный дизайн не доказывает безопасность native parsing произвольно изменяемого файла и не отменяет existing owner-integrity checks.

Сами low metadata calls также могут читать/выделять native metadata; PASS означает bounded **new value-read allocation profile** под этим typed preflight и прежним execution/stream envelope, а не отсутствие любых native allocations до него. Без этой оговорки claim был бы сильнее доступного source evidence.

## Implementation readiness и совместимость

Принятый producer recipe: четыре literal scalar Julia String assignments из design§5 через HDF5.jl0.17.4. Explicit equivalent creation допустима только с instance `datatype(value)`/scalar dataspace и закрытием handles. `datatype(String)`, `[value]`, Python auto `attrs[name]=str/bytes` не эквивалентны: prepared h5py test_attrs_data224–250 прямо подтверждает vlen auto-creation для последних путей.

`point_artifacts.jl:177–210` generic annotation задаёт только missing description/units/axes, поэтому exact audit attrs следует поставить до annotation либо создать audit group после неё в owning final writer. Нельзя получить generic description=path, units=not_applicable или axes inference вместо exact constants. Дополнительные historical annotation attrs сами по себе не вводят новую required portable inventory. Global annotation behaviour не менять.

По `rg` выбранный Runner src ещё не содержит final_fixed_point_audit/record_json producer. Новых выпущенных final-audit artifacts с vlen attributes в inputs не установлено; это не глобальное доказательство их отсутствия. Если появится обязательная конкретная existing-artifact vlen compatibility, нужна его immutable identity и отдельный bounded-read proof: данный profile его сознательно не принимает. Декодирование vlen с post-read length check не закрывает этот gap; helper process/C shim/new trust boundary в этом task не одобрены.

Selected Results native.py SHA `892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b` содержит historical generic schema attr reads. Candidate native.py SHA `4c4faee51d55abda3532e5bfba165388690fdb6891df9bb30a82e4f9e1a14fb9` (`_audit_attribute:211–235`) пока использует dtype до low-class check,<=512 и high getter; он **не** соответствует принятому здесь profile и не получает CP-CODE этим approval. Candidate state.py SHA `57af749bbc0c5179707871ee43e75db01da2017faa242d08bd888c2aab8ef224` используется только как owning budget entrypoint. Зависимая реализация должна следовать profile A, затем пройти независимый code review/targeted check.

Legacy native4 с absent native group+absent commit record остаётся not_recorded; recovery без final group остаётся not_applicable/not_a_final_state. Новое fixed-only правило не накладывается на старые metadata attrs. Present group/native↔commit identity/equality, one-sided absence/corruption и recovery final-record prohibition остаются D2. JSON status/value/tag semantics, schema ID, measurements/units/physics/gamma/thresholds не меняются.

## Required distinguishing controls до runtime acceptance

Design§6 достаточно конкретен и принимается. До GREEN должны быть фактически представлены:

- Actual pinned Julia scalar-String four-constant writer → independent h5py type/space/cset/width/raw value checks, с native/commit identity/equality.
- Genuine fixed ASCII/UTF8, N=L/L+1/65536, все три pad modes; exact constants и разрешённый suffix проходят. Metadata/value-byte assertions должны подтвердить, что fixture действительно записан нужным fixed encoding, а не auto-vlen/conversion.
- Genuine NULLTERM raw `expected+NUL+X` и interior-NUL suffix fixtures отклоняются. Это ключевой контроль против accidental high getter/first-NUL conversion. Не принимать test, где fixture writer сам заранее обрезал adversarial suffix.
- Genuine scalar vlen ASCII/UTF8 с guard/sentinel подтверждает **ноль value payload reads**, даже для правильной короткой constant. Огромный vlen payload не нужен. Неподдержанные class/shape/N<L/N65537/absurd width отвергаются до value buffer allocation/read; metadata adapters дополняют, но не заменяют genuine HDF5 fixtures.
- Charset/padding invalidity, invalid UTF8/ASCII, wrong constant, leading/prefix/suffix errors; every missing attribute corrupt. ID cleanup и caller stream budget failure проверяются отдельно; tiny insufficient physical-stream budget не увеличивается ради прохода.
- Group-absent legacy/recovery compatibility, present same-state native/commit pair и original identity failure controls остаются.

Same-type raw transfer и source dispatch не объявляются measured library guarantee до этих controls. Actual Julia/Python native HDF5 paths/versions/source hashes и exact source/environment binding входят в runtime receipt. Все вызовы — в оставшемся уже согласованном finite C08/engineering envelope, без новых calls/build/install в этом review.

## Итог и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Attribute cap/method уже следуют из старого D2 dataset paragraph | D2 задаёт dataset type и attr values, не attr dtype/read | Cap65536 принят здесь явно как engineering дополнение | изменить |
| Profile A совместим с pinned Runner String path | HDF5.jl0.17.4 instance datatype+scalar dataspace, exact source hashes | Новый N1 writer/round-trip ещё отсутствует | сохранить |
| Новый value-read bounded profile готов для реализации | Fixed atomic+scalar+L..65536 preflight, same-type raw bytes, strict padding/constants/cleanup | Native metadata RAM/hard library behaviour не доказаны | сохранить |
| Candidate Results<=512/high-getter уже accepted | Candidate source отличается от profile A | Нужны owning implementation и CP-CODE | изменить |
| Old native/JSON/science contract требует изменения | Scoped new attrs, unchanged absent-group/native4/recovery/D2 semantics | Неустановленная future vlen compatibility требует отдельного evidence | сохранить |
| Native transport/runtime/scientific GREEN достигнут | Только source/design evidence | Required genuine controls/receipts ещё впереди | дополнительно измерить |

STOP. Продуктовые исходники не менялись; execution не выполнялся.
