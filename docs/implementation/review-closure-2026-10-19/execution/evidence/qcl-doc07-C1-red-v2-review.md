# DOC07 C1 RED-source v2: narrow high review

2026-10-20. **APPROVED source-only** на test SHA256
`6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd`.
R1 закрыт, иных blocking findings в correction нет. Предыдущее полное review
`412d4bdaef6aed837faad9748f77b04b7215f00d2cf7b5a389fa69b8df4ca0d2`
сохраняется с resolved R1 и выполненной Fact.status coverage рекомендацией.
STOP перед одним Root RED; executed RED/collection/schema validity не заявлены.

## Exact correction и границы

Verified v1 source SHA c2fdf66a…3bf684 совпал с прежним frozen snapshot.
Actual `diff -u v1-source current` содержит только:

- additional fragment id/file pilot.256 после pilot.0…255;
- additional input path physical.public_leaf_32 после _0…31;
- additional index point_id/path P-10000 после P-0…P-9999;
- новую параметризацию inputs/api × все5 accepted Fact.status с paired
  invalid statuspass; 9 добавленных строк, без новых semantic constraints.

Теперь три cap+1 rows уникальны по object/id/path, имеют те же healthy nested
fields и valid syntactic IDs. Duplicate rejection больше не является причиной
этих negatives: они изолируют соответственно maxItems256/32/10000. Объектные
templates/positive boundary lengths не изменены. Conditions cap не изменён:
appended id pilot.condition по-прежнему отличен от condition-0…11.

Новый Fact.status positive domain — known,partial,unknown,not_assigned,
not_applicable — соответствует accepted canonical Fact definition. Каждая
пара начинается с independent authored fragment и healthy validate, затем
делает single status mutation to pass. Не вводится invented per-name
status/text/source policy. Это C1 shape controls; scientific meaning/full-chain
и attribution остаются C2. Остальные пять-format factories, finite/Atom,
Origin/ValueOrigin/View/Snapshot/Index/closure/required tests не менялись.

## Source binding

| Input | Проверенный SHA256 |
| --- | --- |
| Test v2,31628B/637lines | `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd` |
| v2 report | `b2508701cfacc40933cb6ac541c852989af9c1d10cdd7a5765cd93b62b78787c` |
| v2 identity | `8e53743a2267c3012c9b8d4780ef858a431648626a06915360a81cc1fcbdffe0` |
| v2 full patch | `40e169b6b54f65439b8a77bd0639dcdbf13a54d04a71b1e5b3c931410e1e6389` |
| v1→v2 delta | `9d085d04d81bb0392ed35a151ef3711d19f0b50599cf11bad6960066bb1f20dd` |
| Preserved v1 source | `c2fdf66a51a5b772e270cd520e1c560794c11a39c191bfe2ed8abc61e33bf684` |
| Canonical DOC03 | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Accepted D2 | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| Accepted D2 R | `f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231` |

Patch-v1→patch-v2 отличается только указанным code delta и new-file blob/
line-count headers. Actual new patch payload совпал cmp с current source.
Owning HEAD `12fc26462bbab3df76904c6deb01f8c6596de7be`; sole status
`?? tests/test_model_help.py`; tracked tests diff exit0 и diff --check пустой.
Tracked test_contracts.py/loader/messages SHA прежние:
0231b4d4…63fd7 /41b5b746…744d1 /fd82f76a…05fa.
Два отдельных existence checks schema и C2 helper подтвердили отсутствие exit0.
Production/source budget не маскируется correction: только новый untracked test
source; никаких raised caps, skips, xfails, relaxed assertions или runtime reruns.

## Что этот PASS означает

Ready test-source basis для Root exact binding и единственного C1 RED в его
combined C1/C2 finite budget. Первый RED по-прежнему ожидается на missing
resource/setup loader, но не наблюдался; Python syntax/collection/runtime здесь
не проверялись. New Fact.status cases увеличивают authored parametrization,
не число разрешённых Python calls. Никакого schema-derived expected oracle,
bound proof или scientific claim не добавлено. Literal arbitrary source refs
из старых fixtures остаются только shape data; semantic positives требуют
собственных exact checked sources/bytes/context в C2.

Envelope review≤10min/1CPU/2GiB/read1MiB/output48KiB. Читались только named
source/receipt/primary paths; conservative repeated logical text<700KiB,
physical filesystem/Git object I/O не инструментирован. No imports/parsers/
tests/schemaValidate/Python/network/children/source edits/Git mutations/
build/solver/fullCI; runtime calls0. Записаны только review и identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 cap negatives исправлены | Unique literal cap+1 rows и sole delta | Исполненная mutation check ещё нет | сохранить |
| Fact.status source coverage расширена корректно | Accepted5-status positives+paired invalid для inputs/api | Не collection/runtime receipt | сохранить |
| Остальные fixtures/production/limits сохранены | Exact delta, tracked diff/hashes, schema/helper absence | Предыдущее full source R сохраняет scope | сохранить |
| RED/shape binding/scientific acceptance получены | Ничего не исполнялось | C1 shape-valid≠C2 proof-valid | данных недостаточно |

**APPROVED exact6a39ee…f2ebd. STOP перед Root one RED, без расширения бюджета.**
