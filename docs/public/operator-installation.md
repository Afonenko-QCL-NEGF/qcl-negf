# [Маршрут установки и обновления](@id operator-installation-route)

Эта глава задаёт порядок действий оператора. Она не сообщает состояние конкретной
установки. Готовность каждого шага подтверждают его сохранённые source и native
свидетельства; отсутствующее измерение остаётся `not_measured`. Успешный процесс,
собранный образ, работающий SSH и научно принятое решение — разные результаты.

## Подготовить установку и её границы

Начните с [развёртывания](../single-server-deployment.md): определите владельца
хоста, VM, дисков, данных и действующих jobs; сохраните выбранный source graph,
план и identities попытки. Проверьте фактические свободные RAM/storage, резервы,
четыре роли и nginx до тяжёлого bootstrap. Не удаляйте неизвестные процессы или
каталоги. Private site, ключи и inventories не входят в публичную документацию.

Готовность этого шага — проверенное владение и доступ, актуальные ресурсы,
закрытый admission и отдельный план сохранения нужных данных. Исторические
числа из runbook не заменяют сегодняшние измерения. SOURCE-проверка не
подтверждает boot, backend или наличие установленного сервиса.

## Выбрать OS и application отдельными этапами

Соберите и проверьте image по [Linux guide](../../components/qcl-negf-platform/docs/linux-workers.md).
Проверка структуры и содержимого образа предшествует передаче; сама передача
предшествует отдельным first boot, enrollment и smoke. Accepted image не
разрешает autostart, открытие admission или Slurm RESUME. Сеть и хранилище
привязывают к фактическому owned host и его возможностям.

Обновления App/UI/сервисов всего кластера устанавливают и проверяют только после подтверждения
остановки всех jobs. Чужие и unknown-owned jobs защищены; их отмена требует отдельного решения.
Application обновляют по [application CD](../../components/qcl-negf-platform/docs/application-cd.md).
Ordinary maintenance update использует свой публичный owner и gates. Закрытый
инженерный путь с metadata staging, выбором закрытого контекста и public local
activation — отдельная scoped операция того же владельца. Не придумывайте
`force` или обход gate. Выбранный профиль, actual runtime, Code/release binding,
здоровье services и закрытый admission проверяются после активации отдельно.

ACK означает принятую команду, а не завершённую phase. При timeout или unknown
сначала сверяйте ту же unit, InvocationID, owner и receipt. Не повторяйте
activation вслепую и не выдавайте старый процесс за загруженный новый App.

## Принять первый Linux worker и QGA

[Первый boot и enrollment](../../components/qcl-negf-platform/docs/linux-workers.md#первый-boot-enrollment-и-допуск)
требуют actual machine/boot/OS, сети, mount и защиты принадлежащих установке
ресурсов. Host adapter, capacity, IP-change, reboot и NetworkManager имеют
отдельные проверки; bridge configuration не доказывает, что внешний LAN/DHCP
доступен или что worker после reboot сохранил правильную identity.

Для каждого owned QEMU guest после install, first boot и reboot выполните
[приёмку guest agent](../../components/qcl-negf-platform/docs/guest-agent.md#приёмка-и-выбор-канала):
проверьте канал, ordinary ping и короткую команду. Declared enable не является
working protocol. При timeout сначала различите client/protocol, guest service
и VM; сохраните первоначальный отказ. Resync, restart и новая попытка требуют
своего решения, а не автоматического повторения неизвестной операции.

## Установить transport и принять ресурсный допуск

[Resource integration](../../components/qcl-negf-platform/docs/host-resource-integration.md#source-installation-и-отдельная-n-приёмка)
определяет UID roles, защищённые private origins, public authorization,
known_hosts, effective SSHD/sudo и native checklist. Копирование ключа не
подтверждает restricted RPC: нужны настоящие hops и root-observed caller,
process generation, cgroup и executable protocol. Не подставляйте `SUDO_UID`,
PID или job selector вместо наблюдения фактического caller.

До допуска jobs отдельно проверьте host capacity/reserves, paid ownership,
backend/image/kernel binding, Slurm registration и closed gates. SOURCE или
synthetic fixture не квалифицирует native backend. [Native attempts](../../components/qcl-negf-platform/docs/native-attempts.md)
связывают обычный lifecycle с настоящим AiiDA process/Code/profile и Slurm
allocation; policy JSON и exit0 сами по себе такого доказательства не дают.
Учитывайте раздельно metadata accounting, RSS, ограничение вывода delivery и
владение NFS write domain: одинаковые числа из разных budgets не взаимозаменяемы.

## Выполнить synthetic, затем отдельный научный опыт

После инженерных checks выполните предусмотренный synthetic/smoke и сохраните
его реальные входы, source, run/attempt, выходы и причины отказа. Не называйте
его научной приёмкой. Новый физический расчёт требует собственной постановки,
frozen model/plan и критериев; scheduler и UI не выбирают сходимость, сетку
или физические допуски. Результат читают по owning Core/Runner/Contracts
свидетельствам, а не по зелёному статусу процесса.

## Восстановить прерванное действие без replay

При отказе остановитесь на последнем доказанном состоянии. Сохраните original
logs/receipts, unit/InvocationID, identities и частичные owned artifacts.
[Recovery](operator-recovery.md) отделяет проверку старого результата, явный
выбор exact состояния и передачу в новую попытку. [Operations](../../components/qcl-negf-platform/docs/operations.md)
описывает эксплуатационные границы. Не удаляйте неизвестные locks/partials,
не повторяйте публикацию или активацию из-за одного оборванного SSH и не
заменяйте отсутствующее evidence предполагаемым успехом.

## Обновить инструкции и установленную справку

Правку делает owning component: edit, review и owning PR, затем Root обновляет
опубликованный gitlink/composition. Новый documentation request связывает
actual graph, selected source bytes, reviews, recipes и применимость
подготовленных dependencies. Текстовые изменения не требуют пересборки App
или нового solver run. Docs producer и его depot/assets provenance сохраняют
собственную identity; граф справки может отличаться от source работающего App.

После подтверждения остановки всех jobs кластера и принятой сборки
[установка документации в API](../../components/qcl-negf-platform/docs/operations.md#документация-в-установленном-api)
является отдельной операцией: immutable public directory и exact bundle SHA
задают парой, затем проверяют actual versioned HTTP routes, inventory,
MIME/cache/ETag/CSP, локальные ссылки и светлую тему. Наличие output в store
не означает, что API уже выдаёт этот bundle. D-only публикация не открывает
admission и не переигрывает App/Code/solver activation или научный опыт.
