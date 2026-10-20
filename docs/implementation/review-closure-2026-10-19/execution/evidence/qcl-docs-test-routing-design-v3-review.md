# D3 docs routing — независимый high source review

**Вердикт: CHANGES REQUIRED перед Ready I2.** D3 задаёт полезный native lifecycle,
но оставляет два source-contract gaps. Это не требование получить свежие native
receipts сейчас и не разрешение native/test/CI запусков.

## Binding и scope

D3 SHA256 `c586234a65a647c3896eb17af4ac0ae0b8a02f4f56d41dcbf25728d997282554`;
identity `71a3c92513604ebb6bec44490cee5ccdeb9b72bd2baf3f23ccdeb6bf14aef7a6`;
ledger `0d26e68bad4d54440ba5a3b8425c463b3645813b642fc22b0601f456f4f93b74`.
Governing D1/D2 и prior CPP `f82e57e11833ffefe1cd85b6778bdfcb9d0749476e768472624f0e34fa5a70a2`
известны по предыдущему source review; D3 прочитан целиком с numbered lines.
Selected HEAD повторно прочитан: `2bb05d3651af4509fe7f02c1253b40f1e5146fec`.
Status остаётся4 tracked routing changes +2 untracked helper/fixture;
8 submodules не initialized (`-`), gitlinks не менялись. Selected platform
`f729e2681224d6537538179ab760fefefd575003`, его owner/admission source regions
проверены по указанному exec worktree. Основной checkout не подменял selected API.

Без исполнения Deno/парсеров/компилятора/imports/tests/probes/build/network/solver/
CI; без product/CP/git writes. Только этот report и его identity.

## R1 — P1: для одного действующего trusted route ещё нет точного source contract

Локаторы: D3:57–59,23,67 и128–132. D3 требует отсутствия always-blocked stub,
но одновременно сообщает, что accepted retained Node/Python/Git observations и
CI producer binding отсутствуют; фабрика описана `make_active_docs_attempt(...)`,
а valid inherited control pipe должен появиться от ещё не заданного setup.

Не хватает конкретного **проверяемого source интерфейса** для одного успешного
маршрута: зарегистрированный producer и exact fields/types/byte predicates его
observations; состав аргументов фабрики; откуда native CLI получает ожидаемую
producer identity; handshake/FD lifetime/replay/scope binding; точный запуск из
tasks и отдельного workflow preflight, затем full `ops/ci.ts → deno task check`.
`getuid/geteuid`, `/proc` birth и наличие pipe устанавливают identity живого
процесса, но сами по себе не доказывают, почему именно этот producer trusted.
D3 правильно запрещает same-user JSON authority, однако механизм отличить его
от разрешённого producer ещё не зафиксирован. Existing engineering receipt
показывает exact Deno RED predicates; он не даёт missing Node/Python/Git reader.

Это source gap, а не отсутствие будущих конкретных hashes/measurements. Без
уточнения I2 придётся придумать формат/authority/wiring либо снова отказать всем
реальным CLI inputs. Один лишь opaque in-process type не замыкает actual entrypoint.

Самая дешёвая коррекция D3: выбрать один Root-owned trusted setup adapter,
зафиксировать его exact in-process constructor/observation contracts и reviewed
producer registration; включить его source в native closure. Показать конкретную
argv/FD route для task, workflow preflight и full invocation, включая propagation
через task/process boundaries либо явное обращение к active broker. Retained file
остаётся audit, не authority. Fresh nonce/peer/attempt/source/deadline проверяются
против authority, уже известной native owner вне caller JSON. Не нужны actual
runtime values, server credentials или новая platform/public schema сейчас.

В том же correction зафиксировать bootstrap: ambient `python3` на D3:67 не может
обещать отсутствие pre-check side effects без ограниченного startup. Python
site/PYTHONPATH startup происходит до body self-hash check. Выбрать конкретный
trusted-parent exec exact admitted Python с очищенным startup окружением и
reviewed isolated argv/runtime closure; либо явно ограничить claim/bootstrap
trust. Не переносить эту неопределённость в D2 unit environment.

## R2 — P1: driver/Git binding route не включён явно в bounded supervision

Локаторы: D3:25,31,67,84,101–116; selected
`ops/git.ts:39` (`git`) и `ops/process.ts:15` (`run`).

D3 сохраняет owning sourceGraph и разрешает лишь narrow executable extension.
Он по-прежнему вызывает `run(..., true)` → `Deno.Command.output()`, без deadline
или byte cap; stderr inherited. `ls-tree -rz HEAD` и `status --porcelain` могут
дать большой output или зависнуть. Driver вызывает этот путь до/между/после
units, тогда как описанный private subreaper/cgroup attach относится к
`execute_step`/per-step supervisor и его descendants. Native launcher/driver/Git
не названы участниками того же гарантированного resource/deadline/cancellation
boundary. NDJSON size cap не ограничивает bytes, уже накопленные внутри output().

Поэтому не установлено, кто прекращает hung Git до первого unit, как ограничена
RAM driver при captured Git output и кто сохраняет original failure при driver
OOM/EOF. Monotonic timestamp сам по себе subprocess не останавливает. Это
проверяемая source/API дыра независимо от отсутствующей cgroup delegation сейчас.

Самая дешёвая коррекция: явно включить launcher/driver и **все** Git helpers в
active attempt ownership/deadline/resource/retention boundary до первого запроса,
с bounded driver-protocol/stderr drains и terminal cleanup; определить отдельные
лимиты Git/source-binding output. Либо добавить узкий bounded command adapter
в owning Git path, сохранив sourceGraph семантику. Нельзя назвать existing
unbounded output bounded благодаря одному транспортному cap. Preflight сохраняет
только read-only Git и не запускает version/unit probes.

## Закрытые решения и границы

- R1 предыдущего CPP (`sourceGraph` throws) закрыт **требованием дизайна** D3:126:
  initial/per-step/final failures сохраняют accumulated captures, typed unknown
  и original failure; отсутствие Graph не маскируется measured source mutation.
  Реализация ещё не проверена.
- Exact12 descriptor совместим с derived additional native closure same final
  commit (31–33). Новые Root files и транзитивные imports надо привязать separately;
  текущий dirty2bb не native-ready. Применение owning git API и отдельный Root
  wrapper допустимы; platform private API не выдаётся готовым executor.
- Delegated cgroup cpu/memory/swap/pids, membership-before-gate и terminal-empty
  имеют конкретные source predicates (114). TMP sampled-stop явно отличается
  от hard disk quota и требует explicit active policy; unknown physical metrics
  остаются not_measured. Реальная delegation не доказана.
- D2 dedicated argv/maps не ослаблены; driver только exact Git capability.
  Fixed13 seed сверён с первичными D/runner literals:10dirs/2links/1empty file,
  texts42+15=57B, no-follow inventory, seed/prelaunch/terminal debit и retention.
- Failure retention/raw hashes/lengths/partial capture/invalid UTF8 описаны
  достаточно для source I2, но полноту receipts надо проверять по реализации,
  включая exact plan/env/input/native closure и attempt+step evidence binding.
- Historic RED04589… и proposed typing patch7d65… разделены корректно. Два
  non-null guards остаются approved source narrowing; current fixture получит
  отдельный actual SHA. Нельзя grandfather новые registrations под227. D3:128
  не разрешает дополнительные execution attempts; при добавлении seam assertions
  сверх narrow typing Root должен явно согласовать source fixture delta (130).
  Это можно сделать без запуска новых product calls.
- actual report-layout compatibility, fresh tools/admission/control pipe/cgroup,
  native execution и final CI остаются **runtime evidence gaps** после source
  closure. Их отсутствие не устраняется этим review и не требует probes сейчас.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D3 готов к однозначному I2 без новых architecture choices | R1 producer/factory/actual route неполны | Source review | изменить |
| Binding phase bounded так же, как unit steps | Existing Git Command.output + R2 | Native implementation отсутствует | изменить |
| D3 сохраняет exact12/D2/13-node seed и исправляет retention requirement | D3:29–33,99–126 + primary source | Исполнение0 | сохранить |
| Fresh native/full CI readiness доказана | Fresh receipts отсутствуют | Scope не включает запуск | данных недостаточно |

Source reads консервативно<1MiB; review wall<15min. CPU/RSS/physical I/O не
измерены как hard quotas. STOP. Source-pass/runtime approval не выдавались.
