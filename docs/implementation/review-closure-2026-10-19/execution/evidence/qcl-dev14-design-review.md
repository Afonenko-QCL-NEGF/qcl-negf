# DEV14 independent CP-DESIGN

**Вердикт: PASS / ready_implementation в exact two-path scope.** Spec compliance и quality приняты; blocking gaps отсутствуют. CP-CODE, implementation и runtime checks этим review не выполнены.

Candidate `/tmp/qcl-dev14-design.md`, SHA256 `fc444f0f774eeedcf2ce6619359506330fa0073293752ed80ae327f162885523` независимо проверен. Source-first observations отправлены координатору до получения/чтения candidate; готовый авторский диагноз для исходного вывода не использовался.

## Source binding и независимые observations

Actual root при reviewer observation: `eb59809a4e601c9bd1d4859228d68502679b6d93`; Contracts `e5c056c47fc3bde3e0ca32866692d740ef9b325c`, Runner `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, Core `a8d2c0de21dfdce3ed3c7c585c555656443f6d89`. Contracts clean; Portal dirty принадлежит другой карточке. Candidate e0f244d и старый dirty status — исторический author observation до root commit, не текущая source freeze. Нужные owning refs/bytes не изменились; implementation receipt обязан записать фактический source заново.

Прочитаны applicable root AGENTS/architecture, Contracts README/CONTRIBUTING (component AGENTS отсутствует), DEV14/P1/autonomy§4, RV07 F07.3/RV19 P19A originals и owning schema/validator/Core/Runner source. Никаких tests/import/build/install/solver/server/product edits. В `/tmp` записан только этот reviewer receipt.

- `Contracts run.schema.json:1420–1440`: production required содержит energy_chunk; leaf integer/minimum1, без default/description. Runner `configuration_sources.jl:31–59` merges files в указанном порядке до schema validation; `_parse_production` configuration.jl:914–935 требует/читает mapping key. Core typed default64 не назначает missing merged key.
- `Core production_contracts.jl:88–99`: energy_chunk::Int=64 — default прямого typed constructor. `production_operators.jl:418–438,483–504,545–569`: consecutive energy-index partitions, buffer capacity min(chunk,NE), last_energy min(first+chunk−1,NE). Поэтому proposed «maximum number of energy points per execution chunk» точнее «chunk count»: это размер execution batch, не число batches и не energy-grid spacing/eV. Все energy indices остаются в цикле; предложение не вводит grid/model change или accuracy claim.
- Core numerical file blob IDs независимо сравнены 3108150→a8d2c0d: contracts `506792ca13984911444974800fd53b06476fe321`, operators `db3ae118a1b5c018b57e3320b7e4675dd8e4877d`, обе пары равны. Приёмка current Core в целом из этого не следует.
- `Runner configuration_types.jl:209–222` фактически returns last explicit history либо nothing при absent/empty history. Proposed description разграничивает constructor default и configuration-source provenance; docstring/full origins остаются DEV15.
- `Contracts artifacts.py:37–39,69–95`: 200000000 constants явно legacy read-only; current single archive bytes — Python int≥0, bool исключён, без ceiling, confined .tar.xz и multipart rejection. `export-receipt.schema.json:45–48` integer/minimum0 без maximum; allOf исключает multipart. README44 локально двусмысленен, README67 уже имеет правильный legacy/current scope.
- Existing test_contracts.py:42–58 проверяет300000000 в двух validators и семь invalid updates. Это прочитанный regression anchor, не выполненный тест. Zero positive assertion отсутствует; source допускает0.

Все пять candidate Contracts SHA256 (README/schema/export-schema/artifacts/test file) совпали с actual bytes. Canonical run schema baseline SHA256 `01ebc5aa635ae98d864fda23606d3228efc6020c68066496539227002ada6390`.

## Exact candidate assessment

1. **README paragraph accepted verbatim.** 200000000 decimal bytes грамматически относится только к legacy archived qcl-negf.export-parts.v1; current single-archive receipt не получает fixed ceiling. Contract/HDF5 versions и scientific caveat сохранены. Это ограничение format validator, не обещание unlimited allocation; candidate отдельно сохраняет consumer resource quotas.
2. **Description accepted verbatim.** Positive integer maximum energy points/chunk соответствует трём operator implementations и shorter-tail case. Required merged declarative input/no schema-assigned default и Core constructor/provenance distinction верны. Число64 не превращается в schema default/effective assigning origin.
3. **Scope accepted.** Только README44 paragraph и JSON Pointer `/$defs/production/properties/energy_chunk/description`; type/minimum/required/default/validator/export schema/registry/test/Runner bytes не меняются. Whole-file JSON reformat запрещён. Не требуется новый subsystem/test/helper/API/scientific decision.
4. **Acceptance accepted.** Old parsed schema брать из immutable Git object; candidate description exact, baseline description absent; удаление единственного нового leaf должно дать equality всего document. Reviewed textual diff отдельно подтверждает отсутствие file-wide rewrite; unchanged hashes/name-only сохраняют validator/registry/tests. Это достаточный source check для metadata-only correction, не proof baseline correctness.
5. **Optional regression accepted с пределами.** Maximum1 centrally admitted L-PY invocation, ready locked environment, no sync/install/implicit retries; source-only sufficient, отсутствие runtime фиксируется not_measured. Assertion denominator/zero gap/две реализации с возможной общей design error указаны честно. Нет numerical env requirement.
6. **Publication accepted.** DEV14 публикует canonical owning change после CP-CODE. DEV15 может design на reviewed diff; DEV16 copy/provenance implementation ждёт published canonical source и accepted drift seam. Не править две schema copies независимо. После canonical description change временная byte divergence ожидаема, её нельзя объявить current synchronized pass.

P1/EXEC и latest engineering grant разрешают этот обратимый internal change без повторного human question; CP-DESIGN author+independent reviewer/coordinator — нужный technical gate. Historical PLAN/standby passage не отменяет прямое активированное поручение. Numerical/science/final-CI counters не расходуются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| energy_chunk wording описывает count energy points/chunk | Core partition/capacity/tail; schema/Runner required leaf | Runtime и performance не измерены | сохранить |
| 200MB относится только legacy multipart | Current validator/schema/constants/README67 | Не unlimited operational allocation | изменить README44 |
| Description-only change сохраняет behavior | Exact one-leaf parsed equality и scoped textual diff предусмотрены | Implementation ещё нет | сохранить design |
| DEV14 можно передать medium writer | Exact two-path wording/invariants/checks accepted | CP-CODE/publication отдельно | сохранить |
| Scientific/native/full release accepted | Соответствующих receipts нет | Source/design-only | данных недостаточно |
