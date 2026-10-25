# DOC07 C2 F3 E1 — final narrow independent high CPP

**PASS_SOURCE. F3a/F3b закрыты.** Actual `_assigning` delta исправляет выбор authority и поддержку redacted status, сохраняя target-leaf Evidence scope, kind/rule/source/hash checks и declared-only fallback при отсутствии runtime record. Блокирующих замечаний в narrow E1 не найдено. Source candidate пригоден к уже выделенному Root-only sole GREEN; фактический runtime PASS этой проверкой не установлен.

## Exact input и provenance

| Артефакт | SHA256 |
| --- | --- |
| Actual module54219 B | `47fea02cced504a8f8ff52537275f25a5dfbd652b595f70f79306e3113edf62c` |
| Actual test58236 B | `647e38868ac5b71f8bf90bf03fb69a789c569cdf6ce0234bde8b4745065b1cd7` |
| Первые52988 B test, independent hash | `ef51509e7b2db13196e5e243193492235d82b516bbc9d93deeb9369000bdc95f` |
| Module delta | `4f6e25cb21ee8f459e83229704934c25d27f7e9c8ec39bee9e8a3ef63340831c` |
| Regression delta | `b70107fc2126adb613b3794077b38288c6cdce35aa0dbfe5d328beb5d91d7fc4` |
| Prior high review | `78a4046f227f4c07f72c8bd59b4b7f87c960a8314cb915b481f7e254bf5d67f5` |
| Explicit E1 plan | `0825186875a3481647c075106ba7b1888be3e73f8168bca1e7705ca051a1588d` |
| Author report / identity | `27d6895a4916d1aacfe3be3049f1cbb682cae1c3882319cec53563bee5abad33` / `2f9c57b9b70a634504d6eb6f3f9510c23d7ae8f782c8d9899bd73d4232b1999c` |
| Frozen D2 / canonical | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` / `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Unchanged C1 schema / tests | `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241` / `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177` |

Worktree `/tmp/qcl-doc07-c2-worktree`, exact HEAD `d791dea33f4628cf23c0b8552ebee9e51d7dd605`. Read-only `GIT_OPTIONAL_LOCKS=0` status: два прежних untracked owning files module/test; submodules отсутствуют. Module delta содержит один hunk только внутри `_assigning`; test52988-byte prefix независимо подтверждён. Новый public format, field, trust root, target import или schema validator не добавлен.

Primary basis — frozen D2 R6/R2 и canonical InputView assigning/Evidence/privacy clauses:510–538; prior F3a/F3b review; actual narrow source/test deltas. Авторский report прочитан после primary source. Нормативный контракт не пересматривается.

## F3a: authority не зависит от emitted numeric status

`model_help.py:881–890` ищет точный target leaf в checked retained Snapshot, используя его assigning record и точный `/inputs/<index>/assigning` selector. `View.used.status` и Atom больше не выбирают источник authority. Explicit runtime unknown/redacted record остаётся target, потому что это dict, а не None; прежняя known frozen assignment его не заменяет. Только отсутствие runtime target допускает plan fallback на891–892.

Status/kind/rule/source target проверяются на893–898. Exact runtime selector разрешён на899–901. Frozen-plan Evidence допускается на903–908 только при наличии точного declared leaf proof и совпадении status/kind/rule/source с действительной target assignment. Поэтому frozen Evidence остаётся допустимым при совпадении genuine последней assignment, но не становится обходом для старого отличающегося record. Далее сохраняются exact Evidence/container/selector/digest и record projection checks:911–926.

Regression helper `test_model_help_bindings.py:1104` авторствует tiny literal runtime assignment, удаляет неиспользуемые origin claims и переиздаёт Snapshot/receipt/index hashes. Actual used Atom остаётся прежним; known и unknown display имеют правильные собственные формы. Эти изменения исключают stale-hash/context-mask.

- :1122 проверяет healthy runtime assignment при обоих numeric display statuses и отвергает старую, но настоящую frozen assignment в обоих случаях. Новые expected values не вычисляются production helper.
- :1134 сохраняет original same-source case с обоими точными Evidence paths и known/unknown numeric display.
- :1144 сохраняет genuine missing-runtime declared-only fallback; used не заполняется из плана.

Эти пары непосредственно различают прежний emitted-status authority shortcut. F3a CLOSED_SOURCE.

## F3b: redacted — отдельный допустимый status, без повышения в known

Новый predicate893 требует соответствие emitted status самому retained target; прежнее безусловное требование target.status=known удалено. Predicate915 отдельно сверяет status с exact Evidence record. Legacy frozen assignment без status по-прежнему интерпретируется known, как в исходном private fixture; это не превращает explicit unknown/redacted в known. Existing kind/rule/source checks сохранены, C1 source=null privacy rule не ослаблен.

Healthy :1155 использует genuine raw redacted config_file/source=null/rule=null, exact nonnull snapshot Evidence, known/unknown numeric display и проверку отсутствия мутации. Public shape соответствует accepted redacted branch. `used` и assigning status остаются независимыми.

Controls :1166 содержат различающие C1-valid semantic mutations:

- `known_status`: исходный raw redacted имеет execution_strategy/fixed_strategy rule. Поэтому единственная замена emitted status на known удовлетворяет C1 known source-or-rule shape и отвергается именно по ложной status attribution.
- `wrong_leaf`: sibling содержит настоящий идентичный redacted record; snapshot/index/used Evidence переизданы перед healthy check. После замены только selector отказ обусловлен target leaf scope, а не неравенством record/hash.
- `wrong_kind`, `wrong_rule`, `digest`: сами формы допустимы; меняется только семантическая связь или digest с корректным digest spelling.

Квалификация coverage: дополнительные `public_source` и `private_path` probes сохраняют emitted status redacted, но присваивают ему nonnull source. Они уже нарушают C1 source=null и потому **не считаются C2 semantic proof внутри schema-valid precondition**. Это избыточные defensive rejection probes; они не нужны для закрытия F3b и не дают отдельного schema-validation claim. Их наличие не ослабляет core pairs, не требует handwritten C1 validator и не является blocker. Все healthy и основные distinguishing пары выше C1-valid по source shape; C1/parser execution reviewer не выполнял.

F3b CLOSED_SOURCE. Нового права публиковать private paths, выдумывать producer rule/source или поднимать redacted в known нет.

## Сохранение scope и пределы

Unchanged части module переиспользованы из предыдущего полного high CPP и focused cycle8 review. F1/F2/F4/F5/F6 corrections, multipoint private inputs, origin resolver/ordered reasons D2:178, Snapshot declared-vs-used checks и public format dispatch не изменены данным hunk. Этот narrow verdict не является ещё одним полным новым audit всех branches, native/source capture или production integration.

Все выводы о closure основаны на source trace и independent literal fixtures. Нет измеренных импортов, exception behaviour, collection, test pass, runtime privacy или scientific attribution. Native/public/finalCI/science acceptance не подразумеваются.

Named ledger: explicit E1 plan, prior cached review/contract, narrow assigning source, module/regression deltas, appended test ranges, hashes/prefix и read-only Git metadata. Conservative current logical read charge1MiB <2MiB; physical I/O/CPU/RSS не измерены. Выход <96KiB. Target runtime/parser/import/typecheck/tests/format/network/build/solver/server/children/Git mutation/product/checkpoint writes:0. Записи — только report и companion identity.

Original engineering8/8 остаётся исчерпанным. Отдельный E1 использован1/1; review не сбрасывает ни один cap и не выделяет ещё один source cycle. Shared DOC07 runtime used3/4 сохраняется по coordinator provenance; единственный исходно выделенный GREEN принадлежит Root. При последующем runtime failure автоматического repair/retry grant здесь нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F3a authority shortcut закрыт | Source881–912, independent known/unknown/stale/same-source/missing pairs | Runtime не выполнялся | сохранить |
| F3b genuine redacted Evidence принимается без known fabrication | Source893/915 и C1-valid основные pairs1155/1166 | Два дополнительных probes вне C1 precondition не считаются C2 proof | сохранить |
| Candidate source eligible для sole Root GREEN | Exact narrow delta, unchanged prefix/C1 и previous high CPP | Только прежний finite runtime slot, без rerun grant | дополнительно измерить |
| Native/public/scientific acceptance достигнута | Свидетельств нет | Private software evidence only | данных недостаточно |

STOP — PASS_SOURCE; original8/8 и E1 1/1 сохранены, runtime0.
