# Проверка научного плана через HTCondor

Подготовьте каталог с `runner/` из рабочей копии приложения, `plan.json`,
`payload.sh` и `short-run.submit`. `plan.json` создаёт команда
`runner/bin/qcl-negf plan …` из инструкции в [README](../../README.md).
Перед подачей выполните `Pkg.instantiate()` для `runner/`. В окружении
Linux worker должны быть доступны системная Julia 1.13 и зависимости этого
манифеста в Julia depot. Установка зависимостей выполняется при подготовке
окружения worker.

```sh
condor_submit -dry-run short-run.classad short-run.submit
condor_submit short-run.submit
```

После возврата каталога `result` проверьте `series_result.json` и статус задания.
Независимая проверка текущего поколения описана в [analysis](../../analysis/README.md).
Ограничения `short-run.submit` предназначены для малой инженерной постановки.
