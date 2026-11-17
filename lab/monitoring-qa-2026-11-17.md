# Browser QA мониторинга, 17 ноября 2026

Проверена установленная сборка Beszel 0.21.2 с описанными UI patches.
Source, patches и сборка описаны в [monitoring-build](monitoring-build.md).
Этот отчёт добавляет browser/native-data evidence; сходимость научного solver
и per-job accounting он не проверяет.

Native Chromium использовал системный CA без `ignoreHTTPS` и без переопределения
`HOME`. В browser context заданы OS dark и сохранённые `ui-theme=dark`,
`pbColorScheme=dark`; отдельный проход добавил `--force-dark-mode` и смену
OS light → dark после загрузки. Credentials читались из приватного файла в память;
токены и пароли в evidence не выводились. Screenshots, DOM/CSS snapshots и native
records сохранены приватно; адреса, system IDs, аккаунты и inventories сюда не включены.

Последний отдельный native read завершён 17 ноября в 16:15 UTC: все три actual
agents — PVE host, CachyOS worker и Ubuntu guest — `up`, версия `0.21.2`, текущие
CPU/RAM/disk конечны. У всех есть history; последние timestamps продвинулись между
проходами. Наблюдавшийся возраст последних samples по timestamps — 4.8–30.3 s.
Графики CPU, памяти, диска и сети открылись для каждой системы на реальных данных.

В проверенных views не наблюдались `.dark` или `data-color-scheme=dark`; root
сохранил `color-scheme: light only` при исходных dark preferences и после смены OS.
Проверены login, home, settings form/select, command dialog, charts трёх систем,
systemd info sheet, PocketBase login/collections/logs/backups. Home и admin backups
также просмотрены визуально. Body text/background контраст составляет примерно
16.66:1 для Beszel и 14.93:1 для PocketBase; это проверка базового текста, а не
полный accessibility audit всех графических элементов.

Отрицательные случаи различены:

- **Native missing:** штатный API перевёл только PVE monitoring record в `paused`.
  Версия агента сохранилась, CPU/RAM/disk стали нулевыми defaults; GUI показал три
  `—`, не `0%`. Затем record возобновлён, получены свежие `up`/числовые поля.
  Позднейший отдельный native read подтвердил `up` всех трёх agents. Агентские и
  научные службы не останавливались.
- **Zero presentation:** browser-only routing подменил только три отображаемых
  значения одной строки на числовой ноль при `up` и валидной версии. GUI сохранил
  три `0,00%`. Это presentation fixture, не измеренный нулевой CPU/RAM/disk и не
  backend data modification; routing снят с закрытием тестового context.
- **Loading:** задержан только ответ реального statistics request в тестовом
  браузере. Loading surface осталась светлой, затем реальный ответ доставлен.
  Backend outage этим не воспроизводился.
- **Error:** настоящий запрос неизвестного маршрута вернул HTTP 404; error view
  осталась светлой. Это не проверка всех возможных отказов backend.

В проверенных frontend views `pageerror` не зарегистрирован. Один из тестовых
скриптов повторил read-only restore-check после закрытия context и получил harness
error; первичный resume уже завершился. Ошибка harness сохранена, исправлена без
повторного pause; отдельный последующий native read подтвердил восстановление.

Ограничения runtime QA: actual agents не предоставили journal capability и
log/fullscreen controls. Эти пути и container log/info fullscreen не объявлены
проверенными; ради QA новые capabilities или workloads не включались. Числовой
ноль от `up` агента также не доказывает отдельно валидность каждого collector.
Обобщённого утверждения «все возможные views прошли» этот отчёт не делает.

Приватные первичные locators, доступные оператору:

| Artifact / выборка | Содержимое |
| --- | --- |
| `stage1-summary.json` | Login/home и три native histories |
| `stage2-summary.json` | Views и отрицательные случаи, включая harness warning |
| `stage4-summary.json` | Authenticated admin/OS switch/fresh agents |
| `fresh-history-final.json` | Три свежие строки |
| `pve-paused-native.json` | Native status/info при pause |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Три agents дают actual метрики и history | Native records, advancing timestamps, три chart views | Host metrics, не per-job измерения | сохранить |
| Missing и zero различимы в GUI | Native pause → dashes; отдельный zero fixture → проценты | Ноль fixture не измерен | сохранить |
| Проверенные views остаются светлыми при dark preferences | Login, home, admin, CSS и OS-switch snapshots | Не все optional paths доступны | сохранить forced-light patches |
| Все log/fullscreen views проверены runtime | Journal controls недоступны | Source/build не заменяют browser evidence | данных недостаточно |
