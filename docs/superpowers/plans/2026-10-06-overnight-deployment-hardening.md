# Проверка развёртывания и перенос подтверждённых исправлений

> **For agentic workers:** Use superpowers:executing-plans for coordination and test-driven-development for common bug fixes. Independent component tasks may use the existing delegated agents.

**Goal:** К 09:00 Europe/Minsk 7 октября завершить серверную проверку инфраструктуры и ограниченное диагностическое исследование, сохранив исправления в общих компонентах.

**Architecture:** Platform владеет bootstrap профиля PostgreSQL/AiiDA, TLS и проверкой конфигурации nginx. AiiDA владеет получением полного набора committed artifacts. Superproject выбирает опубликованные component commits через gitlinks; private site хранит измеренный inventory и секреты.

**Tech Stack:** NixOS, Nix, Python, Deno, AiiDA, PostgreSQL, Slurm, nginx, Proxmox; переносимый worker — libvirt/KVM.

**Spec:** Поручение пользователя от 2026-10-06; `docs/architecture.md`, `docs/single-server-deployment.md`, `AGENTS.md`.

## Global Constraints

- Deadline: 2026-10-07T06:00:00Z. Детальные finite budgets и fresh measurements сохраняются отдельно в ignored deployment artifacts.
- Не изменять модель, сетки, рассеяние и научные допуски ради скорости либо сходимости.
- Scientific campaigns: одна попытка каждой, aggregate 1800 s, максимум 24 CPU / 32 GiB / 8 GiB output; CI один final-ready dispatch, ноль reruns.
- Новая root revision требует собственной release приёмки. Native reuse допустим только по совпавшим derivation, contents и test contract.
- Сохранять первоначальные failed receipts, mutable state, данные и историю Code; секреты и private inventory не включать в Git.
- Слияние PR требует отдельного разрешения; подготовка, публикация PR и проверка порученного deployment разрешены.

## Review Focus

- Unix-socket hostname: реальные параметры драйвера должны выбирать ожидаемые socket и database; существующее непустое хранилище не переинициализировать.
- TLS listener: реальный nginx должен принимать сгенерированную конфигурацию; gixy и Nix evaluation не заменяют `nginx -t`.
- Engineering credentials: тестовый сертификат не подтверждает работоспособность production certificate и runtime credentials.
- Artifact retrieval: LO generation artifacts должны доходить до parser вместе с неизменённым scientific identity.
- Negative diagnostic: завершение процесса и инфраструктурный успех не превращают несошедшийся расчёт в scientific pass.

### Task 1: Platform bootstrap и TLS

**Files:** `components/qcl-negf-platform/ops/bootstrap.ts`, `ops/bootstrap_profile.py`, `modules/application.nix`, `modules/persistent-state.nix`, относящиеся tests. В этой же границе устранены PG cold-start ordering и export spool; CI owning module поддерживает site-defined per-unit NSS routing.

**Interfaces:** существующий declarative bootstrap; PostgreSQL Unix socket через supported storage `engine_kwargs.connect_args`; NixOS TLS options и runtime credentials.

- [x] Воспроизвести неверный Unix-socket URL и отсутствие SSL directives в регрессионных проверках.
- [x] Исправить owning flow; добавить guards непустой provenance и повторного запуска.
- [x] Выполнить применимые component tests и независимый review diff.

### Task 2: Настоящая проверка nginx до тяжёлой сборки

**Files:** `components/qcl-negf-platform/ops/bootstrap_build.py`, `nix/site-preflight.nix`, `tests/test_bootstrap_build.py`.

**Interfaces:** `--check-nginx` проверяет фактические executable/config paths; изолированный namespace и dummy credentials предназначены только для engineering preflight.

- [x] Регрессионная проверка отвергает конфигурацию SSL без certificate directives.
- [x] Реальный `nginx -t` обязателен; невозможность запуска означает failed preflight.
- [x] Проверить bounded logs, failure preservation и совместимость существующего CLI.

### Task 3: AiiDA retrieval

**Files:** owning CalcJob retrieval implementation в `components/qcl-negf-aiida`, соответствующие execution/recovery tests.

**Interfaces:** сохранённые result commits и referenced generation artifacts передаются parser без изменения наблюдаемых или критериев.

- [x] Воспроизвести отсутствующий LO artifact в retrieved tree.
- [x] Исправить retrieve contract и проверить parser/recovery, включая negative diagnostic.
- [x] Опубликовать component change и обновить superproject gitlink после review.

### Task 4: Единый final source и серверные gates

- [ ] Собрать reviewed source composition; проверить четыре roles, реальный nginx config, builder identity, index ownership и fresh admission.
- [ ] Выполнить ограниченную production build с измеренными максимальными CPU/RAM; подписать без private signing key на CI.
- [ ] Передать signed closures, проверить services и release readiness; открыть admission только после обязательных проверок.
- [ ] Запустить один final-ready CI на новой source revision; исходные failures оставить отдельными.

### Task 5: Исследование, восстановление и worker

- [ ] Зафиксировать frozen plans, actual Code/release/job identity и ограниченный ресурсный бюджет; выполнить две диагностические кампании по одной попытке.
- [ ] Сохранить результат и provenance; независимо разобрать инфраструктурный и научный статусы.
- [ ] Согласованно архивировать controller state и проверить восстановление в отдельной VM.
- [ ] Подготовить generic worker image и инструкцию подключения к Arch/libvirt; проверить boot, отсутствие site secrets и связи с source revision.
- [ ] Вернуть production распределение ресурсов и дать таблицу утверждение / свидетельство / ограничение / решение.
