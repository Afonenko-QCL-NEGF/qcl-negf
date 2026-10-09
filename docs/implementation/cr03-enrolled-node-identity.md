# CR03: enrolled node identity и frozen trust

Owning Platform требует protected enrollment registry и active pool v2. Target — маршрут, permanent
machine identity — отдельное свидетельство. Registry связывает
enrollment/name/role/hostname/UUID/machine-id и trusted routes; actual worker observation
дополнительно устанавливает Slurm NodeName и boot. Duplicate/legacy/partial/wrong identity не
получает fallback по ready release.

Pure local controller binding выполняется до runtime writes/flock. Unresolved CR04 receipts
проверяются read-only до snapshot/remote child и повторно under lock; затем controller remote/local
machine+boot должны совпасть. Protected descriptor walk проверяет весь namespace
registry/known_hosts; verified trust bytes заморожены в root-protected operation snapshot. Все
subsequent SSH/Nix copies используют только этот snapshot.

Selected nodes проверяются до prefetch/quiesce, перед copy и перед RESUME/open. Activation получает
expected node binding; check возвращает bound node+release envelope. Drift после начала maintenance,
включая первый target до copy, оставляет closed/unknown state и прекращает later dispatch. Startup
использует общий enrollment/binding API; CR02 persistent shutdown intent и normal lifecycle
coordination — отдельный следующий ticket.

## Локальные проверки и пределы

Final selected fake suite: 55 tests, 0.405 s, OK. Перед исправлением независимый review обнаружил
first-target drift; отдельный RED воспроизвёл boot/machine/ NodeName subcases, затем GREEN проверил
новый case и прежние 54 выбранных регрессии. Первые четыре source calls и дополнительный isolated
compatibility call сохранены, включая initial missing API и obsolete legacy assertions. Original
failed logs не заменены успешным итогом.

Budget: initial four calls, один отдельный compatibility call, два review-fix calls; каждый ≤60
s/256 KiB streamed diagnostics. CPU/RAM caps отсутствуют. Все remote/system command boundaries и
root-protected filesystem observations в этих tests — fakes; scientific solver attempts 0. Source
diff/Markdown format checks прошли. Full Platform suite, native CR04 timing cases, Nix eval/ build,
real SSH/Slurm/DMI/provider trust, CI/deploy не выполнялись.

Actual protected inventory/known_hosts и supported Slurm observation convention ещё не предъявлены
для production acceptance. Старые tooling/role metadata, legacy pool и wrappers без enrollment fail
closed; migration/initial bootstrap нужны отдельно. Initial CI→controller trust не доказан operation
snapshot. Whole I14 fleet/VM stop barrier и manually resolved research не установлены. Release/Code
identity, CR05 profile recovery, numerical model/tolerances и normal shutdown wait не менялись.

SHA256 final frozen eight-file diff:
`0da2c45abcf69b87535d3901b613c2ab52c3af0d8a6dca30e909be5043451e6b`.

| Утверждение                                            | Свидетельство                             | Ограничение                                      | Решение             |
| ------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------ | ------------------- |
| Alias/ready release не заменяет enrolled machine       | Registry/binding/envelope fixtures        | Synthetic identity                               | изменить            |
| Wrong owner и unknown receipt блокируют новую mutation | Local binding и unresolved-order fixtures | Actual protected inputs отсутствуют              | сохранить           |
| Post-maintenance drift прекращает later dispatch       | Genuine RED и final 55-case GREEN         | Fake transport boundaries                        | изменить            |
| Frozen trust не переоткрывает mutable source path      | Descriptor/snapshot/substitution fixtures | Privileged root trusted; не hardware attestation | сохранить           |
| Production/I14/scientific acceptance достигнута        | Таких свидетельств нет                    | Отдельные runtime/operator gates                 | данных недостаточно |
