# DOC07 C2 F3 E1: narrow source correction

Один отдельно разрешённый E1 cycle по `/tmp/qcl-doc07-C2-F3-source-E1-plan.json`; original8/8 остаётся исчерпанным, не сброшен. Первичный independent review `/tmp/qcl-doc07-C2-impl-v2-review.md`, SHA256 `78a4046f227f4c07f72c8bd59b4b7f87c960a8314cb915b481f7e254bf5d67f5`. Scope — только `_assigning` и append независимых F3a/F3b controls. Worktree `/tmp/qcl-doc07-c2-worktree`, base `d791dea33f4628cf23c0b8552ebee9e51d7dd605`, branch `codex/review-closure-model-help-bindings`.

**F3a.** Target authority теперь выбирается из checked retained snapshot assignment именно этого leaf, независимо от View.used.status/Atom. Только отсутствие runtime record допускает declared fallback. Явный runtime unknown/redacted не заменяется прежним known frozen assignment. Frozen Evidence разрешён лишь при совпадении status/kind/rule/source с действительной последней assignment и доказанной frozen leaf scope; exact snapshot Evidence указывает тот же target leaf. Numeric status больше не используется в `_assigning`.

**F3b.** Status projection и status выбранного raw target/Evidence должны совпадать; missing status старой frozen assignment трактуется known. Genuine redacted target с source=null и nonnull exact snapshot Evidence принимается, без повышения в known. Проверки kind/rule/source, selector scope и digest сохранены. Новая публичная форма или privacy exception не вводится.

Append-only regression controls:

- Одна retained runtime execution_strategy assignment: healthy exact runtime assigning при emitted used known и unknown; stale frozen config_file projection отвергается в обоих случаях.
- Original same-source runtime/frozen assignment остаётся healthy с обоими Evidence paths и любым numeric display; настоящий missing runtime сохраняет frozen declared-only fallback.
- Genuine raw redacted assignment принимается с nonnull exact Evidence при used known/unknown и не изменяет document.
- Для known fabrication healthy raw redacted имеет producer rule, поэтому одна замена emitted status на known остаётся C1-valid и нарушает только status attribution. Нельзя скрыть этот witness source-or-rule или rule-mismatch ошибкой.
- Wrong-leaf witness имеет в sibling настоящий идентичный redacted record с согласованными snapshot/index/digest bytes. Отказ должен различать именно leaf scope, а не несовпадение kind/status/hash. Дополнительные controls сохраняют wrong kind/rule/digest/source и private-path disclosure rejection.

Предыдущие F1/F2/F4/F5/F6, origin resolver, Index, Snapshot, C1 schema/test/loader не изменялись. В module delta ровно один hunk внутри `_assigning`; все52988 bytes исходного test v2 сохранены exact prefix (`cmp -n 52988` exit0).

| Artifact | Bytes / SHA256 |
| --- | --- |
| Current module |54219 / `47fea02cced504a8f8ff52537275f25a5dfbd652b595f70f79306e3113edf62c` |
| Current C2 test |58236 / `647e38868ac5b71f8bf90bf03fb69a789c569cdf6ce0234bde8b4745065b1cd7` |
| `/tmp/qcl-doc07-C2-F3-E1-module.delta.patch` | `4f6e25cb21ee8f459e83229704934c25d27f7e9c8ec39bee9e8a3ef63340831c` |
| `/tmp/qcl-doc07-C2-F3-E1-regressions.delta.patch` | `b70107fc2126adb613b3794077b38288c6cdce35aa0dbfe5d328beb5d91d7fc4` |
| Preserved `/tmp/qcl-doc07-C2-F3-E1-v2-model_help.py` |53586 / `6e3f6d8ed2e6a0d7e637c48edc87820c62776755803f4d4b62a3961f8b2429bd` |
| Preserved `/tmp/qcl-doc07-C2-F3-E1-v2-test_model_help_bindings.py` |52988 / `ef51509e7b2db13196e5e243193492235d82b516bbc9d93deeb9369000bdc95f` |

Identity `/tmp/qcl-doc07-C2-F3-E1-identity.json`. Старые reports/patches не перезаписывались. Unchanged C1 schema SHA `584971b619218d56f2bdc4b04dfc1361d4850898cdabeca4594203aaf119c241`, C1 tests SHA `b284bd64ad2a891f2fca791c7d32b0a11389399f32c68aa913dba9da5b217177`, loader SHA `41b5b746bbf28cd0e60bb85bc927f1c55ba0ac2695f3271b875f83c057a744d1`.

Выполнены только source/Git/text/hash/cmp/diff operations. Оба no-index --check exit1 для изменённых файлов, diagnostic output пустой. Final status — прежние два untracked owning files; HEAD unchanged, submodules отсутствуют. Никаких target runtime/import/parser/schema/typecheck/tests/formatter/network/build/solver/commit/Root/checkpoint операций. Source reasoning не является runtime outcome.

Envelope15min/1CPU/2GiB/read2MiB/output128KiB. Читались named E1 plan/high review, narrow assigning source, deltas и hashes/prefix; conservative read charge1MiB <2MiB, cached прежний contract не перечитывался целиком. Physical CPU/RSS/I/O не измерены. Additional E1 allowance1/1 использован; автоматического следующего source cycle нет. Shared DOC07 runtime used3/4 неизменён; sole GREEN остаётся Root-owned после independent high R. Scientific/C08/native/fullCI grants не менялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F3a/F3b source correction реализована | Narrow module delta и causal appended controls | Нужен independent high source R; runtime отсутствует | изменить |
| Frozen52988B prefix и другие fixes сохранены | cmp0, single assigning hunk, exact hashes | Root publication отдельно | сохранить |
| C2 runtime/privacy acceptance измерена | Новых runtime свидетельств нет | Sole Root GREEN не выполнялся writer | дополнительно измерить |
| Native/scientific acceptance получена | Свидетельств нет | Source-only software scope | данных недостаточно |

STOP после E1 source correction.
