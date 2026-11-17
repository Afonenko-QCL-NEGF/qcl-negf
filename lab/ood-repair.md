# Штатная интеграция Open OnDemand и HTCondor

Open OnDemand остаётся готовым интерфейсом; очередь, размещение, передача файлов,
история и отмена принадлежат HTCondor. Здесь поддерживается локальная подача из
Project Manager в HTCondor на той же машине. Собственного backend или scheduler нет.

Проверенная исходная база — `ood_core` 0.31.1 и Open OnDemand 4.2.5. Это описание
проверенных исходников, а не требование равенства версий установленных инструментов.
Первичный adapter совпал с
[upstream tag v0.31.1](https://github.com/OSC/ood_core/blob/v0.31.1/lib/ood_core/job/adapters/htcondor.rb).
Project Manager использует существующие
[SmartAttributes и шаблоны проектов](https://osc.github.io/ood-documentation/latest/how-tos/project-management/project-manager.html).

В исходной интеграции обнаружены связанные ошибки:

- Job Composer передаёт `native=nil` и `cores=nil`, а Project Manager — пустые
  dependency kwargs. Adapter должен принимать эти штатные producer-входы.
- Native HTCondor options должны передаваться отдельными аргументами `-a` и
  `key=value`. RAM задаётся через `native.request_memory`: `Script` этой исходной
  базы ещё не хранит отдельное поле `memory`.
- Передаются временный скрипт и явно выбранные входные файлы. Общая файловая
  система между submit и execute machines не предполагается; project и depot
  целиком не копируются.
- HTCondor ID `6.0` нельзя разбирать как Rails ID `6` с format `0`. Полный ID
  сохраняется в GET, DELETE и STOP routes; для DOM используется безопасное имя.
- Job details ожидает native Hash с состоянием и причиной. Завершённый job читается
  из `condor_history`; отсутствие записи в queue и history остаётся `UNKNOWN`.
  Отмена показывает `REMOVED`, а не успешное нормальное завершение.
  Старый cache со статусом `completed` также перепроверяется через native query;
  generic cache status не превращается в подтверждённое native состояние.
- Форматирование длительности использует действительную сигнатуру Rails DateHelper
  и сохраняет отсутствующее значение как `nil`.

Для каждого owning компонента нужен **один полный patch против исходной базы**:
Core patch применяется относительно корня gem, Dashboard patch — относительно
`/var/www/ood/apps/sys/dashboard`. Нельзя наслаивать incremental patches и затем
проверять идемпотентность только первого из них. Оригиналы установленной базы
сохраняются вне репозитория перед первой правкой.

Используется обычный конечный порядок `patch`, который может выполнять Ansible:

1. Если полный reverse dry-run проходит, нужная правка уже применена.
2. Иначе выполнить полный forward dry-run, затем применить тот же patch.
3. Если оба dry-run не проходят, остановить эту правку и сверить изменившийся
   upstream source вручную. Не перезаписывать неизвестную дельту.
4. Проверить Ruby syntax, producer/consumer contracts и затронутый native путь;
   после независимого review перезапустить пользовательский PUN и обновить страницу.

Внешние обновления OOD могут исправить эти ошибки иначе. Тогда patch пересматривается
по актуальному source и проверкам. Сверка версии вместо проверки поведения не нужна.

Переносимые Minitest contracts находятся в `lab/tests/ood_adapter_test.rb` и
`lab/tests/job_details_test.rb`. Они загружают выбранные исходники через
`OODCORE_ROOT` и `OOD_DASHBOARD_ROOT` в обычном bundle окружении. Scheduler calls
и запись project cache заменены; приложение/PUN не загружается, jobs не создаются.
Проверяются native Hash, CPU/RAM/input producer, dependencies, cancel command,
terminal history и UNKNOWN, legacy cache, dotted routes, DateHelper и ERB DOM IDs.

Из корня этого репозитория, для пакетного OOD окружение можно выбрать так:

```sh
export OOD_DASHBOARD_ROOT=/var/www/ood/apps/sys/dashboard
export BUNDLE_GEMFILE="$OOD_DASHBOARD_ROOT/Gemfile"
export BUNDLE_WITHOUT=development:test:doc
export GEM_HOME=/opt/ood/gems
export GEM_PATH="/opt/ood/gems:$(env -u GEM_HOME -u GEM_PATH ruby -e 'puts Gem.path.join(File::PATH_SEPARATOR)')"
export OODCORE_ROOT=$(/opt/ood/gems/bin/bundle show ood_core)
/opt/ood/gems/bin/bundle exec ruby lab/tests/ood_adapter_test.rb
/opt/ood/gems/bin/bundle exec ruby lab/tests/job_details_test.rb
```

В уже настроенном bundle достаточно выбрать два source roots и выполнить последние
две команды его обычным `bundle`. Системные Gem paths сохраняются; отдельная установка
development/test gems ради этих contracts не нужна. Проверенные contracts не заменяют
настоящий GUI submit/status/cancel и проверку процессов на execute machine.

Найден и исправлен также фактический сбой открытой карточки: после следующего
30-секундного poll native ответ уже был `COMPLETED`, но обращение к элементу
внутри `<template>` через обычный querySelector вызывало исключение. Адресная
правка ищет его через `template.content` и сохраняет раскрытое состояние.

Ansible сохраняет исходный `projects.js`; при Dashboard patch выполняет обычные
Node/esbuild/Sass и Rails asset precompile с уже установленными зависимостями,
без сети и без install. Старые public assets сохраняются для открытых браузеров.
Сборка ограничена2CPU/4GiB/180s. Если source уже применён, а build оборвался,
после чтения исходного failed log повторяется тот же play с
`-e qcl_rebuild_ood_assets=true`. Это обычный ручной повтор сборки, не отдельная
система допуска или receipts. На проверенной Ubuntu Sass JS поставлялся0644;
вызов через системный Node не требует менять package permissions.

Готовая форма содержит CPU, RAM в MiB, явный список входных файлов и переменную
окружения для длительности smoke. `AutoMemory` и `AutoInputFiles` — небольшие
дополнения существующего SmartAttributes API с сохранением через штатный controller.
Их можно включать через project template или `launcher_default_items`. Эти два вида
пока не добавлены в JS-меню «Add new option». Непустые job dependencies отклоняются
явно; поддержка workflows, Docker и удалённой SSH-подачи этим результатом не заявлена.

При проверке нужны свидетельства обеих сторон: выбранные GUI значения и native
ClassAd с `RequestCpus`, `RequestMemory`, `TransferInput`; затем event log, stdout,
stderr и возвращённые outputs. Для отмены проверить исчезновение payload/process
family и возврат allocation, сохранив соседний job. HTTP 200 и исчезновение кнопки
сами по себе этого не доказывают. Инженерный smoke не означает научную сходимость.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Нужен собственный scheduler/backend | Штатные OOD producer и HTCondor ClassAd проходят после конечной правки | Квалифицирован локальный vanilla путь | сохранить готовые инструменты |
| RAM уже передаётся обычным `Script.memory` | Исходный `Script` 0.31.1 этого поля не хранит | Новые upstream версии могут иметь другой API | изменить через явный native producer |
| Исчезновение job из queue доказывает завершение | Native history различает normal exit и remove | History может уже не содержать запись | читать history; missing оставить UNKNOWN |
| Исходный patch подходит после любого обновления | Только dry-run и затронутые проверки устанавливают применимость | Новая upstream дельта требует review | дополнительно проверить |
