# SCI05-N1-EA1: кодировка четырёх constant HDF5 attributes

Статус: **инженерное предложение для отдельного high review; не утверждённая норма и не разрешение возобновить I**. Это source audit и уточнение отсутствующего wire method, не новый scientific/record-schema design. Дата: 2026-10-19. Продуктовые файлы не изменены.

## 1. Вопрос, граница и вывод

Как Runner записывает, а independent Results проверяет точные D2 constant attribute values, не материализуя неограниченный vlen string heap? Frozen D2 §8.3 задаёт значения четырёх attributes, но fixed-width/UTF-8/65536 ограничение прямо относится к dataset `record_json`; распространение этого правила на attributes из одного текста D2 не следует.

**Предлагается сохранить существующий scalar-String producer путь Runner и отдельно закрепить bounded fixed-string consumer profile только для этих четырёх новых attributes.** Закреплённый HDF5.jl 0.17.4 уже создаёт из scalar Julia `String` fixed-width UTF-8 scalar, ширина которого равна числу байтов значения. Это не тот же dispatch, что `datatype(String)` или массив строк: последние используют vlen. Никакой существующий final-audit producer и никакой выпущенный portable final-audit artifact настоящим аудитом не установлен.

Для reader предлагается fixed atomic HDF5 string, scalar dataspace, ASCII либо UTF-8 charset, ширина `L..65536` bytes (`L` — длина соответствующей constant в UTF-8), без vlen. Читать следует в bounded raw buffer с **тем же memory datatype, что file datatype**, затем удалить только разрешённый правый padding, строго декодировать и сравнить с exact constant. Это заменяет произвольный candidate `<=512` предел и high-level attribute getter; ни candidate wire choice, ни настоящее предложение не считаются принятыми автоматически.

Предел 65536 для attributes — **явно предлагаемое engineering уточнение**, повторно использующее уже известный record byte ceiling; он не выводится из действующей формулировки D2 и не является физическим допуском. Он допускает обычные padded fixed strings, не привязывая reader к точной ширине Julia writer. Сужать до `N=L` ради удобства reader нет необходимости.

Record object fields, schema ID/version, scientific statuses, единицы, formulas, strict thresholds, native4 обязательные markers, history/numeric datasets, отсутствие группы в старом final native4 и recovery semantics остаются по D2. Применять новый preflight к историческим `/metadata` либо другим native4 attributes не предлагается. Новый public reader/service/oracle не нужен.

## 2. Identity и первичные свидетельства

Root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, `git rev-parse HEAD=9d8cf0cad32743791cc3b80ac7c2a948dab02f48`. Root `git status --short` был dirty: owning gitlinks Core/Runner/Contracts и координационные docs/evidence; эти изменения принадлежат параллельной кампании. Original dirty checkout `/home/tolya/Загрузки/qcl-negf` не изменялся.

Фактический recursive status при начале аудита:

```text
+e86ac74c4fe04a8999b889970c5a9f3c65575694 components/QCLNEGF.jl
 9378396a3681c1eddf2c62f16674834fc4465583 components/QCLNEGFRunner.jl
 d8f8092ca1c76523d85384b4bac8198d8bfa736b components/qcl-negf-aiida
+12fc26462bbab3df76904c6deb01f8c6596de7be components/qcl-negf-contracts
 b067723c82382689bff5cc366981c56e99b926f8 components/qcl-negf-platform
 2622de5ee28b454ff4f809cc3dd00c1e5bc2295d components/qcl-negf-portal
 1eacefcd81a50e245ea9da74a0b717b33818c61e components/qcl-negf-research
 e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae components/qcl-negf-results
```

HEAD gitlinks: Runner `23860d9e660a3cddf6cb5203d449d1b62f3745a1`, Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`, Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`. Прочитанный Runner working tree чистый на фактическом `9378396a3681c1eddf2c62f16674834fc4465583`; выбранный Results чистый на `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Candidate `/tmp/qcl-sci05-results-worktree` имеет тот же base HEAD и изменения `native.py`, `state.py`, новый test; это NOT_READY candidate, не нормативный источник.

Прочитаны root `AGENTS.md`, `docs/architecture.md`; component-local `AGENTS.md` в owning Runner/Results не найден. Из навыков прочитаны `using-superpowers` (его subagent-stop применим), `brainstorming` для ограниченного engineering design и `qcl-results-analysis` как граница чтения метаданных; архивы/научные массивы не анализировались. Дополнительные агенты не создавались по поручению координатора.

| Источник | Exact SHA256 / revision | Локатор и установленный факт |
| --- | --- | --- |
| `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` | §8.3, строки361–388: dataset wire type/caps и четыре attr values; attribute dtype не задан |
| `/tmp/qcl-sci04-design-v2-review.md` | `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1` | Accepted D2 review identity; его согласие не является runtime evidence |
| Runner `src/infrastructure/persistence/hdf5_backend.jl` | `3ccd096eb9e01df4c5d320a00a15e718e027d78b94892c174fcef611d6359a31` | строки1–8: wrapper `attributes` использует HDF5.jl напрямую |
| Runner `src/infrastructure/persistence/hdf5.jl` | `c946ba5fb71f035d1a0b564b561700b9a5c3360ed67bf890c668b0ced769d511` | строки59–61,285–299: обычные scalar String assignments; строка635: generic tree annotation |
| Runner `src/infrastructure/persistence/point_artifacts.jl` | `81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a` | `_annotate_physics_tree!`:177–210 и `_physical_dataset`:214–220; missing attrs получают generic defaults |
| Prepared Julia `Manifest.toml` | `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47` | `.build/local-julia-int01/import-phase-1/environment/julia/Manifest.toml`:196–214; HDF50.17.4 tree `26e37af34e8ccb7a8358bd8de1619c7bcb526738`, HDF5_jll2.2.2+0 tree `194d676302b9b6aa53ea1f98ae8607d5caa8de4f` |
| Pinned HDF5.jl `Project.toml` | `761a141236d499d35acd70ced47a62d54bb279f5637153f278306636f7830367` | Depot `.build/local-julia-int01/depot-1/packages/HDF5/Xsdf5`; version0.17.4. Другая найденная копия `/home/tolya/.julia/packages/HDF5/8g5ny` version0.17.3 исключена из выводов о pinned API |
| Pinned HDF5.jl `src/attributes.jl` | `833e769a819c5ce1b24128ca172f1c11d0e222a0c7d8bf30d3fb4ba97fa53246` | `Attributes.setindex!`:382–383 → `write_attribute`:202–214 → `create_attribute(data)`:81–89 → `datatype(data)`/`dataspace(data)`; String write:173–183 различает fixed/vlen |
| Pinned HDF5.jl `src/typeconversions.jl` | `1abe93196079179cfdbc1fb010a2572385f483118935f4cf1fda6d6db8932d06` | `cset(AbstractString)`:19; `datatype(str::AbstractString)`:213–218 fixed `max(sizeof(str),1)` UTF8; `datatype(::Type{S})` и `datatype(::Array{S})`:219–231 vlen; `unpad`:23–35 может обрезать на первом NUL |
| Pinned HDF5.jl `src/dataspaces.jl` | `9e6ccf922624d315ca4459818533b86df049ce46df8bff82b428da8607625b33` | строка58 `dataspace(::AbstractString)=H5S_SCALAR` |
| Root `uv.lock` | `db19ba9ace32c03d2b0a9da9b11b90f9f16de23c9539aa2276cd3dafd4f56336` | строки601–614: h5py3.16.0; installed wheel tag cp314-manylinux_2_28_x86_64 соответствует lock wheel SHA `e4360f15875a532bc7b98196c7592ed4fc92672a57c0a621355961cafb17a6dd` |
| Prepared h5py `_hl/attrs.py` | `bfdbfc7c9f406aa1915c10d50e6f3d3db9acffb7aa4505b84dae39954a29d40e` | `.venv/lib/python3.14/site-packages/h5py/_hl/attrs.py`:53–98; high getter получает `h5t.py_create(dtype)`, выделяет массив и вызывает `attr.read(arr,mtype=htype)`; `get_id` открывает low AttrID |
| Prepared h5py dist-info `METADATA` | `e461fcf7eb9fee6242205f9225cc178455a0212d1c0cb8f997f7eebf8cd9695e` | `.venv/lib/python3.14/site-packages/h5py-3.16.0.dist-info/METADATA`:2–3 подтверждает version3.16.0; native HDF5 runtime identity этим не установлена |
| Prepared h5py `tests/test_attrs_data.py` | `84bb6d21110d369a4c018ef31951e2ba5cb540e839e209dd93d380ddf16ec48f` | строки224–250: high-level Python `bytes` и `str` assignments создают vlen; это отличается от Julia scalar String |
| Prepared JLL `include/H5Apublic.h` | `d5cbda26036019f1eed9741a389a8f0d7feb3d4ca6312b5efec877668337397f` | Artifact `df5ad26ed9661e47b7b9169ae35190911fa7aaaf`:891–920; `H5Aread(attr,type,buf)` читает entire attribute и автоматически преобразует тип; transfer property argument отсутствует |
| Prepared JLL `include/H5Tpublic.h` | `7638a0441f19fe1a9494e901ec13f413c4531d9623422e844c56ec45d74bc21f` | строки2163–2177: размер vlen string type — sizeof pointer, не heap payload size; строки3020–3030: conversion может truncate/pad |
| Selected Results `native.py` | `892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b` | commit e2fdeda; `_required_group`:54–62, native identity:173–199 используют исторические generic attr reads |
| NOT_READY candidate Results `native.py` | `4c4faee51d55abda3532e5bfba165388690fdb6891df9bb30a82e4f9e1a14fb9` | `/tmp/qcl-sci05-results-worktree/.../native.py`:211–235; fixed<=512 preflight, затем high getter. Это предмет будущей правки после D+R |
| NOT_READY candidate Results `state.py` | `57af749bbc0c5179707871ee43e75db01da2017faa242d08bd888c2aab8ef224` | `_IOBudget`:32–61, `_BudgetStream`:70–106; physical stream bytes считаются отдельно от logical selected bytes |

Contracts source binding прочитан как JSON: `/tmp/qcl-sci05-contracts-source-binding.json`, head `12fc26462bbab3df76904c6deb01f8c6596de7be`, validator SHA `1c19ba7f27912c739b349fb7c517a9030be3c4f50c4b75932c08d0c02f3219d1`, schema SHA `ef25a90acfdc8445a20fb53bc40a861de355e07a8abca4dd90f7ee9a0143dc28`. Его runtime/format acceptance не доказывает HDF5 transport acceptance.

## 3. Рассмотренные варианты

| Вариант | Совместимость и стоимость | Решение в этом предложении |
| --- | --- | --- |
| A. Fixed scalar attributes; существующая Julia instance-String запись; low-level raw fixed чтение | Совместим с установленным Runner dispatch; ещё не выпущенная новая группа получает явный bounded profile. Нет vlen allocation на её value-read пути; небольшой private helper | **Рекомендуется** |
| B. Только точная fixed ширина `N=L`, только UTF8 | Также совместим с Runner, но без необходимости отвергает fixed ASCII и padded эквивалентные constants. Не нужен для bound | Не выбирать |
| C. Принимать vlen attributes через high getter или перевод в fixed memory type | Проверка decoded length запоздала; `dtype.itemsize` vlen — размер pointer. Fixed destination не доказывает отсутствие внутренних unbounded allocations при conversion. `H5Aread` не имеет DXPL argument для подстановки vlen allocator | Не выбирать; нет bounded recipe в рассмотренных API |

При требовании совместимости с уже существующими **новыми** final-audit artifacts с vlen attributes нужны их immutable identity и отдельный доказанный bounded read mechanism. Таких artifacts/source requirement в переданном наборе нет. Вводить helper process, C shim, новый trust boundary или менять schema сейчас не требуется и не предлагается.

## 4. Предлагаемый attribute profile A

Применимость: только required attributes `/diagnostics/final_fixed_point_audit@schema` и `record_json@{units,logical_axis_order,description}` при наличии новой группы. Generic attrs других объектов остаются на прежнем пути.

| Attribute | Exact value | UTF-8 bytes L | Canonical Runner N |
| --- | --- | --- | --- |
| group `schema` | `qcl-negf-final-fixed-point-audit-v1` | 35 | 35 |
| dataset `units` | `1` | 1 | 1 |
| dataset `logical_axis_order` | `scalar` | 6 | 6 |
| dataset `description` | `Versioned final fixed-point raw measurement record` | 50 | 50 |

Reader preflight **до value read / numpy allocation**:

1. Открыть только attribute с известным именем; не перечислять и не читать все attrs.
2. Получить low-level file type и space; сначала проверить class `H5T_STRING`, `is_variable_str()==false`, space class `H5S_SCALAR` (shape `()`, не NULL и не `(1,)`). Compound/array/opaque/numeric types отвергнуть до преобразования arbitrary dtype в numpy.
3. `N=file_type.get_size()`, `L<=N<=65536`; charset ровно `CSET_ASCII` либо `CSET_UTF8`; strpad ровно `STR_NULLTERM`, `STR_NULLPAD` либо `STR_SPACEPAD`. После этих проверок NumPy backing dtype — synthesized fixed `S<N>`, `kind='S'`, `itemsize=N`, без object/vlen/subarray.
4. Attr data не имеет dataset DCPL/chunk/filter/external storage настроек. Data allocation для fixed scalar — N bytes; никаких dataset-specific `chunks/compression/external` проверок на attr не добавлять. `H5Aget_storage_size` не нужен как oracle bound и тем более не разрешает читать vlen: основное доказательство — fixed atomic type + scalar + N cap. Общий HDF5 metadata/file overhead остаётся под прежним stream I/O и execution envelope.

После preflight: `target=numpy.empty((), dtype=numpy.dtype(f'S{N}'))`; `attribute.read(target, mtype=file_type)`; `raw=target.tobytes()`. Явный memory type равен file type, поэтому строковый type conversion не должен скрыть suffix. `parent.attrs[name]`, `.get(name)`, `attribute.read` с автоматически выбранным типом и numpy scalar `.item()` до raw `tobytes()` здесь не используются.

Padding: для NULLTERM и NULLPAD удалить только NUL suffix справа; **NUL с последующими ненулевыми bytes не отбрасывать на первом NUL**. Для SPACEPAD удалить только space suffix справа. В оставшейся строке любой NUL — corrupt. Декодировать строго ASCII для `CSET_ASCII`, строго UTF-8 для `CSET_UTF8`, сравнить с exact constant; никаких `surrogateescape`, Unicode normalization, `strip()` либо case folding. Все четыре constants ASCII, поэтому byte equality после указанного padding также проверяет exact value. `expected + NUL + junk` всегда corrupt.

Все IDs (`AttributeID`, type, space) закрываются при success и при каждом отказе. Attributes обрабатываются последовательно, raw buffers не копятся между ними. Максимальные logical value bytes для этой новой группы: `4*65536+65536=327680` вместе с dataset; это **не bound physical file I/O** и не дополнительный grant. На обычном producer четыре attr values занимают92 bytes. NumPy/raw/decode copies дают лишь постоянный множитель от byte cap; строгий whole-process RAM bound на произвольный hostile HDF5 metadata этим не заявляется. Existing `_BudgetStream` должен оставаться обёрткой того же handle, учитывая и metadata reads; logical byte cap не заменяет physical counter.

## 5. Producer recipe и prerequisites для I

Рецепт привязан к pinned HDF5.jl0.17.4 source, **не исполнялся**:

```julia
# Exactly these literal String instances, never datatype(String) or [value].
attributes(audit_group)["schema"] = "qcl-negf-final-fixed-point-audit-v1"
attributes(record_dataset)["units"] = "1"
attributes(record_dataset)["logical_axis_order"] = "scalar"
attributes(record_dataset)["description"] = "Versioned final fixed-point raw measurement record"
```

Это проходит через instance `datatype(value)` и scalar `dataspace(value)`; отдельная ручная byte-array кодировка attribute не нужна. Если implementation использует explicit creation, точный эквивалент — `dtype=HDF5.datatype(value)`, `space=HDF5.dataspace(value)`, `HDF5.create_attribute(parent,name,dtype,space)`, `HDF5.write_attribute(attr,dtype,value)`, закрыть attr/type/space в `finally`. Нельзя заменять instance на `datatype(String)`, массив строк или Python `attrs[name]=str/bytes`, сохраняя прежний claim.

Prerequisites перед CP-CODE/runtime:

- Отдельный high reviewer принимает либо отвергает profile A, включая новый explicit attribute cap65536 и padding rules; координатор связывает одобренный hash, источники и оставшийся бюджет. Данный автор сам norm не утверждает.
- Runner N1 writer ещё должен быть реализован на разрешённых D2 owning paths: portable object/state binding один раз, unchanged dataset fixed UTF8 scalar1..65536 без chunk/filter/external/vlen, атрибуты по рецепту, native↔commit semantic equality. Это самостоятельная работа I, сейчас её результата нет.
- Generic `_annotate_physics_tree!` не должен подменить `description` на path, `units` на `not_applicable`, axes на inferred value. Создать exact attrs до annotation (его `haskey` сохраняет заданные values), либо добавить новый group после generic annotation в конкретном final-write пути; не изменять global annotation semantics. Набор дополнительных historical annotations не становится новым mandatory v1 inventory.
- Results private attr helper меняется после D+R: low-type/scalar preflight перед dtype allocation, accepted fixed width до65536, raw identical-memory-type read, right-padding handling, resource cleanup. Existing dataset raw helper показывает подход, но его наличие не доказывает attribute round-trip.
- Runtime identity HDF5.jl/HDF5_jll из prepared manifest и actual Python-linked native HDF5 должна попасть в **будущий** receipt вместе с source hashes. Читать wheel source допустимо для API design, но он не доказывает actual native library version/behaviour. Никакие imports в данном аудите не делались.

## 6. Точные controls для будущей уже разрешённой targeted проверки

Все controls manufactured transport fixtures, без solve, без изменения физической приёмки. Не тратить calls на огромную vlen строку: маленький genuine vlen attribute с guard/sentinel вокруг low-level value-read достаточен для различающего свидетельства отказа **до** чтения payload. Adapter test полезен для недоступных malformed metadata values, но не заменяет genuine HDF5 round-trip.

| Control | Ожидаемое свидетельство |
| --- | --- |
| Julia generic instance-String recipe четырёх constants | Independent h5py metadata: scalar, fixed STRING, UTF8, widths35/1/6/50; raw bytes равны literal constants; transport pass на той же portable record identity |
| Fixed ASCII и UTF8; width L; padded width L+1 и upper boundary65536; три признанных pad modes | Pass при exact value после только правого padding. ASCII fixtures создавать explicit fixed type / NumPy `S`, не Python high-level str/bytes auto-vlen |
| Одна constant заменена другим byte; prefix/suffix/leading whitespace | Corrupt; при SPACEPAD допустим только padding справа согласно типу |
| NULLTERM raw `expected + NUL + b'X'`; также raw `prefix + NUL + suffix` | Corrupt с raw read; control специально ловит first-NUL truncation/high-getter conversion |
| Invalid UTF8/ASCII byte, NUL внутри value, unknown charset/strpad через bounded metadata adapter | Corrupt, без permissive decode или normalization |
| Genuine scalar vlen UTF8 и ASCII attrs, в том числе семантически правильная constant | Corrupt до value-read; sentinel подтверждает ноль payload reads. Нулевой `dtype.itemsize`/pointer-size/storage-size не даёт обхода |
| Missing attr; numeric/compound/array type; NULL dataspace; `(1,)` и rank>0 | Corrupt до payload read/allocation; scalar-one-element array не принимается как scalar |
| Fixed width65537; N<L; guarded absurd metadata width | Corrupt до value-read/allocation; counter/sentinel проверяет этот порядок |
| Existing ordinary native4 с отсутствием новой группы и обоих record copies | Прежнее `not_recorded`; не добавлять к historical metadata новый fixed-only gate |
| Existing recovery без новой группы | Прежнее not_applicable/not_a_final_state; наличие запрещённого final record остаётся corrupt по D2 |
| Present group, same-state native/commit semantic pair; tiny insufficient physical I/O budget | Pair проверяется прежним validator; physical budget fails через существующий stream, его cap не увеличивается |

Порядок дешёвого будущего доказательства: metadata/preflight guards → tiny independent fixed/padding round-trip → Runner-produced native/commit tiny fixture и existing absent-group compatibility. Source/control agreement не объявлять runtime GREEN до receipt. Все исполнения вписываются в уже выделенный координатором оставшийся общий C08/engineering budget; этот документ его не увеличивает.

## 7. Ограничения, решение и STOP

В данном поручении были только чтение исходников/lock/headers, Git read-only identity и создание этого файла в `/tmp`. Python/Julia/HDF5 imports, tests, builds, install, network/server operations, Git mutations, product edits, новые model subsamples отсутствуют. Runtime numeric/scientific acceptance не проверялась. Бюджет поручения20min/1CPU/2GiB/read3MiB/output64KiB не превращён в дополнительный кампанийный runtime grant; прочитаны точечные небольшие исходники/срезы и hashes.

Конкретного основания переоткрывать frozen v1 object schema, measurement definitions, scientific decision либо trust boundary не найдено. Есть один узкий engineering approval point: закрепить proposed attr profile A, затем reviewer/coordinator разрешает зависимую реализацию. Если обязательным станет vlen compatibility, а bounded path не будет доказан, dependent consumer остаётся NOT_READY с локатором `H5Aread`/vlen allocation gap; это нельзя закрыть post-read length check или новым автономным redesign.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Scalar String Runner путь уже соответствует fixed UTF8 scalar encoding | Runner9378396 wrapper/assignments; pinned HDF5.jl0.17.4 instance dispatch | Новый final-audit writer ещё отсутствует; runtime round-trip не запускался | сохранить |
| D2 attr values известны, attr wire method отсутствует | D2 hash §8.3; отдельный dataset dtype paragraph | Нельзя выдавать candidate<=512 за принятую норму | изменить |
| Profile A позволяет bounded read без vlen heap materialization на новом value-read пути | fixed atomic type+scalar+N preflight; raw AttrID.read с identical type; H5T size semantics | Proposal требует independent high review; не whole-file adversarial sandbox proof | изменить |
| Vlen high getter или fixed-destination conversion имеет доказанный heap bound | В рассмотренных API такого доказательства нет; H5Aread entire value, H5T vlen size pointer | Native libs не импортировались/не измерялись | данных недостаточно |
| Исторические native4/group-absent semantics требуют изменения | Ни D2, ни фактический producer этого не требуют | Future compatibility fixtures ещё не исполнялись | сохранить |
| SCI05 N1/I либо transport/runtime GREEN установлен | Только source audit и proposal, без writer/receipt | Нужны D+R approval и scoped controls под remaining envelope | дополнительно измерить |

STOP: файл передан координатору для отдельного high review; product/source changes и I не начаты.
