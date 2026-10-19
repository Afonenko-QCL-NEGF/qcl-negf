# SCI02 — независимый source-first и CP-DESIGN review

2026-10-19, /root/reviewer, gpt-6.1-sol high.
Candidate `/tmp/qcl-sci02-design.md`,37234bytes,
SHA256 `62c844a81fb91710794995843c843420009590bf527d3f687187a4a606a72be1`.
Hash независимо измерен. Read-only sources: root e0f244d075dd49874ba4f3847f4efa693f3b3622;
Research5458212063a41051328ef8b5d14d63d5ac7dc781;
Core4af6e94808c6e60affbf1050a5184dbc12083335 (numeric3108150);
Runner0c53c6d0f68e0b25fce79388db831da6fc3ae856.

**Verdict: CP-DESIGN PASS для docs-only model passport.**
Новый scientific choice, изменение дозы/каналов/сеток/допусков не предлагаются.
Blocking scientific/source contradiction в candidate не найден.
Implementation requirement ниже сохраняет необходимый source binding при переносе
в owning файл; его следует проверить в CP-CODE, новый design round не нужен.

## Source-first observations до author candidate

Сначала независимо прочитаны Research source.yaml/structure.csv/reference model,
S01/policy docs; Core theory02, presets/scaling/grids, Runner parsing/merging/
configuration_source. Отдельно просмотрены primary PDF pages3/4 полностью,
page1 адресно через text extraction. Own observations переданы coordinator до
открытия candidate, затем выполнено сравнение с ним.

PDF `/tmp/qcl-1911.06582v1.pdf`:2760444bytes,
SHA256 `b103b3da9fa977d1dc682d1e2caf96d74b5f081731e4db0da944af675a58dc70`;
совпадает с Research source.yaml declared artifact. Прочитаны renders
`/tmp/qcl-paper-page-3.png` и `page-4.png`; superscript units проверены визуально.

- Main p3 left opening paragraph содержит sheet quantity4.5×10^10cm^-2.
  Fig3(a) caption p4 содержит4.5×10^10cm^-3. Различие primary и настоящее,
  не ошибка text extraction. Primary erratum/intended caption correction не установлен.
- Geometry sequence, underlined29Å, barriers32.6/19Å, Al.25,56mV/period,200K,
  fosc.20,16.5meV и extraction около41meV найдены в этих pages. Точные model
  offsets/masses/eps/phonon/screening/IFR/acoustic numbers этим не установлены.
- Sheet4.5e14m^-2 соответствует main quantity после conversion, но сохранение
  именно sheet interpretation — declared assumption с caveat, не разрешение
  замолчать caption или исправить scientific input на volume quantity.
- M reference model:70K,56mV, alloyfalse+null values. P analytical policy включает
  alloytrue с .60eV/4.5168e-29m³; S01 переопределяет bias0. Пять channels
  source-derived expected, e–e none определяется typed default и прямым P1,
  а не отсутствием обсуждения e–e в статье.
- configuration_source возвращает last assigning YAML leaf; это не primary
  source формулы/числа. Point-generated assignments и typed defaults нужно
  проверять отдельно от raw M preset.

Paper identity: title/authors/arXivv1 найдены page1; DOI/journal association
опирается на переданный primary metadata audit coordinator и source.yaml,
publisher bytes reviewer не получал. [Versioned author PDF](https://arxiv.org/pdf/1911.06582v1)
остаётся primary для dimensional claim. Publisher/tarball/отдельная figure bytes
не объявлены независимо проверенными.

## Dose chain: independent check

Runner configuration.jl411–423 принимает positive sheet dimension и ionization.
Core presets.jl237: N_D,+²D=fion·N_dop²D. grids.jl18–20 задаёт cell centres
и uniform wˣ; grids.jl66–92 назначает half-open layers, χD, положительную
normalization=ΣwˣχD, затем Nbar_D=(L0²·N_D,+²D)χD/normalization.
Поэтому Σ(L0wˣ)·(Nbar_D/L0³)=fion·N_dop²D [m^-2]. Это donor identity,
не измеренная electron neutrality и не convergence gate.

Source-derived арифметика независимо восстановлена прямым подсчётом центров
на явно заданных edges, без вызова Julia/build_profiles:

| Nz | Layer cell counts | Doped Julia indices | Discrete width nm | Donor volume m^-3 |
| --- | --- | --- | ---: | ---: |
|198|22/53/13/56/19/35|145:163|2.84136363636|1.583746600543913e23|
|96|11/25/7/27/9/17|71:79|2.7759375|1.6210739614994934e23|

Оба используют sheet4.5e14m^-2,fion1 и period29.61nm; для96nodes bar sheet.045,
bar volume.16210739615. Continuum2.90nm даёт1.5517241e23m^-3 и не заменяет
discrete value. Candidate162–180 правильно различает эти three quantities и
не называет arithmetic runtime/profile result. Existing198-node test-source
rtol2e-15 прочитан, не исполнен. Literal caption volume4.5e16m^-3 дал бы
1.305e8m^-2 при2.90nm; это иной input, не equivalent units.
Impurity donor weights wˣ·Nbar_D/L0² подтверждены kernels.jl119;
Poisson использует тот же donor profile. Sheet sum не принимает ни один solver state.

## Formula/value/assigning origins и expected effective state

Candidate193–294 соответствует источникам:

- Geometry/direct-paper observations отделены от explicit material/scattering
  constants и source-unknown origins. Formula locators owning Core не выданы
  за новый independent derivation всех microscopic prefactors.
- Full ionization, uniform doped segment, independent IFR interfaces,
  dielectric/screening/IFR/acoustic/alloy values остаются assumptions.
  Их common DOI не устанавливает numerical value provenance.
- Runner definitions.jl387–443: ordered sources M→P, затем study/variant/
  inclusion overrides; generated run/convergence/temperature/output; generated
  single-study disables optical. Mapping recursive, sequences replace;
  configuration.jl214–235 сохраняет assigning histories.
- planning.jl54–74: point writes voltage/TL/TLO и hashes point-resolved raw;
  configuration_types.jl216–221: last source leaf. Они не подставляют literature
  origin вместо assigning origin. Candidate labels source-derived expected,
  не frozen-plan/native measurement, корректны.
- Core PhysicalModelOptions606–616 и ElectronElectronOptions67–85;
  Runner configuration.jl1896,1930–1940,1957–1958: fixed screening,
  parabolic dispersion, thermal LO, e–e none, domain adaptation none.
  Inactive branch sentinels и include_exchange flag не создают активный e–e.
  Hartree/Poisson не удаляется при none.
- Raw M preset200K(Core)/56mV и publication200K не effective S01.
  Expected source composition0mV/70K/five channels должна быть bound и
  проверена future frozen/runtime identity до submit; этот passport не создаёт run.
- Device405periods/output geometry не умножает period donor sheet и не
  становится accepted experimental target. Curve200K не oracle equilibrium70K.

## Implementation requirement для CP-CODE

Candidate14–15 говорит, что owning файл содержит sections «Проверенный
первичный источник»–«Вердикты и пробелы». При буквальном переносе только68–315
можно потерять immutable source refs из33–67 и identity/not_created оговорки47–51.
**Сохранить в owning passport краткий source/ref block и явное distinction
declared/source-derived/not-created/runtime-unknown**, либо перенести этот
block целиком. Bare Core symbol names без exact source ref не заменяют locators.
Это уточнение authoring, не новый model decision. CP-CODE проверяет diff/links,
сохранность YAML/CSV/source hashes и stated scope four docs only.

## Уровни и ограничения review

Это publication/value attribution и operator/source algebra. Process/run
создан этим task не был; iterative convergence, physics gates, discretization
adequacy и experimental validation unknown/not_measured. Старый runSCI01 имеет
отдельную identity и не относится к not_created здесь.
No product imports/tests/solver/build/server, arrays или branch mutations.
Source-only arithmetic не test execution. Unique primary PDF2.76MB и bounded
текст/две existing renders укладываются в64MiB input envelope; peakCPU/RAM
не инструментировались и не выдаются за measured resource profile. Никаких
private inventories/logs/secret bytes в этот report не включено.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Main/caption единицы противоречат в primary | Hash-verified PDF p3/p4, visual superscripts | Intended correction/erratum unknown | сохранить |
| Declared sheet4.5e14 сохраняется без новой physics | Main text, M/P1, conversion и discrete algebra | Interpretation явно caveated; полный value dataset не из статьи | сохранить |
| Model passport готов к docs-only авторству | Source-first review + candidate matched independent observations | Сохранить source/ref identity block при переносе | изменить |
| Profile/source policy доказывают equilibrium70K | Нет final/raw/runtime measurements | Четыре scientific evidence levels не измерены | данных недостаточно |
