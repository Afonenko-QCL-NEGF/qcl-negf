# CR03: root delivery caller

Existing release workflow передаёт обязательный `--enrollment` опубликованному Platform API.
Controller-side path задаётся только protected configuration `vars.QCL_DEPLOY_ENROLLMENT_PATH`, без
default, inventory или site value в Git. Target/path проходят bounded ASCII syntax checks до SSH;
malformed/missing input даёт generic diagnostic. Path передаётся одним single-quoted remote argv;
manifest остаётся stdin, прежние workflow pins/assemble/gates/timeouts сохранены.

Два локальных synthetic calls: RED — 2/34 pass, 32 fail; GREEN — 34/34 pass. Проверены actual Bash
run block, hand-literal expected decisions, fake SSH literal argv/stdin и POSIX tokenization.
Реальный SSH и remote shell не исполнялись. Limits 60 s/128 KiB на вызов, без CPU/RAM caps; failed
original log сохранён. `git diff --check` прошёл; новые CI/deploy calls отсутствуют.

SHA256 frozen workflow diff: `03ea75723689ec1ae4e936b9139c72ddca1a8d6dbc564abcfb54ffec9c906915`.

Это совместимость source caller с API. String validation не устанавливает защиту remote
registry/known_hosts, identity, initial CI→controller trust, environment protection или actual
admission. Эти проверки принадлежат Platform/site и остаются отдельными gates. Actual protected
inventory/path configuration не получены; delivery не запускалась. CR02/I14 и scientific acceptance
не заявляются.

| Утверждение                            | Свидетельство                                      | Ограничение                                       | Решение             |
| -------------------------------------- | -------------------------------------------------- | ------------------------------------------------- | ------------------- |
| Caller передаёт required enrollment    | Exact published API и reviewed workflow diff       | Installed tooling/site configuration не проверены | изменить            |
| Malformed input блокируется до SSH     | 34 synthetic cases и generic diagnostic assertions | Bounded ASCII syntax                              | сохранить           |
| Remote argument сохраняет literal path | Captured fake argv/stdin и POSIX tokenization      | Remote shell/SSH не исполнялись                   | сохранить           |
| Production delivery принята            | Нового runtime evidence нет                        | Inventory/trust/admission gates отсутствуют       | данных недостаточно |
