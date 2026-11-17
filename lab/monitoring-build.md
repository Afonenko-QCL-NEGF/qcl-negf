# Сборка Beszel со светлой темой

Используем один Beszel: native hub и штатные native agents. Агенты не изменяются.
Hub получает два patch светлой темы и один patch отображения доступности метрик;
новый backend, package manager или dispatcher
для этого не нужен. Сборку выполняем отдельно от установки и проверки метрик.

В Beszel 0.21.2 документированного force-light ENV/config нет. Его собственный
`ThemeProvider` и первый HTML paint читают OS/localStorage; простого изменения
`defaultTheme` недостаточно. Дополнительно log/container-info/fullscreen views
используют принудительно тёмные Shiki и background tokens. Первый patch фиксирует
эти пути и удаляет переключатели из navbar/login. Admin links открывают отдельную
PocketBase UI на `/_/`, вне Beszel provider: второй patch фиксирует её
`activeColorScheme`, первый paint и убирает OS listener/picker.

Исходники и зависимости:

| Источник | Публичная версия / commit | Локальная дельта |
| --- | --- | --- |
| [Beszel](https://github.com/henrygd/beszel/tree/v0.21.2) | `v0.21.2`, `c97759f0ca4badc824ab0ff43f1571cc3c8f3a72` | [Monitoring UI patch](patches/beszel-v0.21.2-light-monitoring.patch), 8 файлов |
| [PocketBase](https://ganigeorgiev.com/git/pocketbase/pocketbase) | `v0.42.2`, `9873ed8ffdf2e7a99bd57e269a33f7cea51620d9` | [Admin UI patch](patches/pocketbase-v0.42.2-light-admin.patch), 3 файла |
| Beszel: текущие метрики | Тот же `v0.21.2` / `c97759f…` | [Missing metrics patch](patches/beszel-v0.21.2-missing-metrics.patch), ещё 1 UI файл |
| [Bun](https://github.com/oven-sh/bun/releases/tag/bun-v1.4.4) | `1.4.4`, Linux amd64 baseline archive | Только инструмент сборки в `/tmp` |

Проверенная среда: Go 1.27.4, Node 26.13.1, npm 12.2.2, Bun 1.4.4, GNU Make.
Это запись выполненной сборки, а не дополнительный exact-version guard приложения.

Перед сборкой выбрать свободный builder по свежим CPU/RAM/disk facts и native
состоянию jobs. Если узел исполняет jobs, сначала запретить новые назначения штатным
drain и дождаться завершения текущих. Не обновлять общий runtime во время jobs.
Для этой сборки использованы 4 CPU, 4 GiB RAM, swap 0, timeout 20 минут и log cap
10 MiB. Если user cgroup limits недоступны, bounded build не заменять unbounded.

Ниже используется системный Bun, при его отсутствии — официальный latest.
Системные Go/Node/npm принимаются без exact-version checks; недостающие
инструменты устанавливаются штатным менеджером ОС или официальным stable installer.
Source по умолчанию выбирается из последнего upstream release; PocketBase
берётся из его Go dependency. При новом source patches проверяются и при
необходимости адресно переносятся. Для воспроизведения описанного опыта можно
явно задать BESZEL_REF=v0.21.2. Собственных hash-snapshot/allowlist здесь нет.

Рецепт для Linux amd64 запускается из корня checkout с этими patches; установка
Go/Node/systemd и deployment сюда не включены. Native Go/npm/Bun caches остаются в
временной build directory; глобальная установка Bun не требуется.

```bash
build_root=$(mktemp -d /tmp/beszel-light.XXXXXX)
cp lab/patches/*.patch "$build_root/"
cat > "$build_root/build.sh" <<'BUILD'
set -Eeuo pipefail
build_root=$BESZEL_BUILD_ROOT
exec > >(head -c 10485760 > "$build_root/build.log") 2>&1
trap 'printf "exit_code=%s\n" "$?" > "$build_root/outcome.txt"' EXIT
export GOMAXPROCS=4 CGO_ENABLED=0 GOTOOLCHAIN=auto
export GOPATH="$build_root/go-path" GOCACHE="$build_root/go-cache"
export GOMODCACHE="$build_root/go-mod-cache"
export npm_config_cache="$build_root/npm-cache"
export BUN_INSTALL_CACHE_DIR="$build_root/bun-cache"
if ! command -v bun >/dev/null; then
  mkdir -p "$build_root/tools"
  curl -fL --max-time 120 -o "$build_root/bun.zip" \
    https://github.com/oven-sh/bun/releases/latest/download/bun-linux-x64-baseline.zip
  unzip -p "$build_root/bun.zip" bun-linux-x64-baseline/bun > "$build_root/tools/bun"
  chmod 755 "$build_root/tools/bun"
  export PATH="$build_root/tools:$PATH"
fi
{ go version; node --version; npm --version; bun --version; } > "$build_root/toolversions.txt"
beszel_ref=${BESZEL_REF:-$(curl -fsSL https://api.github.com/repos/henrygd/beszel/releases/latest |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')}
git clone --depth 1 --branch "$beszel_ref" https://github.com/henrygd/beszel.git "$build_root/beszel"
pocketbase_ref=$(awk '$1 == "ganigeorgiev.com/pocketbase/pocketbase" { print $2 }' "$build_root/beszel/go.mod")
git clone --depth 1 --branch "$pocketbase_ref" \
  https://ganigeorgiev.com/git/pocketbase/pocketbase "$build_root/pocketbase"
patch -p1 -d "$build_root/beszel" -i "$build_root/beszel-v0.21.2-light-monitoring.patch"
patch -p1 -d "$build_root/beszel" -i "$build_root/beszel-v0.21.2-missing-metrics.patch"
patch -p1 -d "$build_root/pocketbase" -i "$build_root/pocketbase-v0.42.2-light-admin.patch"
git -C "$build_root/beszel" diff --check
git -C "$build_root/pocketbase" diff --check
(cd "$build_root/pocketbase/ui" && npm ci --no-audit --no-fund && npm run build)
(cd "$build_root/beszel/internal/site" && bun install --frozen-lockfile && bun run build)
cd "$build_root/beszel"
go mod edit -replace="ganigeorgiev.com/pocketbase/pocketbase=$build_root/pocketbase"
make build-hub SKIP_WEB=true
git diff --exit-code -- internal/site/bun.lock internal/site/package-lock.json
git -C "$build_root/pocketbase" diff --exit-code -- ui/package-lock.json
git diff --binary > "$build_root/beszel-source.diff"
git -C "$build_root/pocketbase" diff --binary > "$build_root/pocketbase-source.diff"
go version -m build/beszel_linux_amd64 > "$build_root/buildinfo.txt"
file build/beszel_linux_amd64 > "$build_root/linkage.txt"
grep -q 'statically linked' "$build_root/linkage.txt"
build/beszel_linux_amd64 --version
BUILD
systemd-run --user --wait --pipe --collect --unit=beszel-light-build \
  -p MemoryMax=4G -p MemorySwapMax=0 -p CPUQuota=400% -p RuntimeMaxSec=1200 \
  --setenv="BESZEL_BUILD_ROOT=$build_root" --setenv="BESZEL_REF=${BESZEL_REF:-}" /bin/bash "$build_root/build.sh"
```

`SKIP_WEB=true` использует уже собранные штатными package scripts UI, без второго
install. PocketBase `ui/embed.go` встраивает его `ui/dist`; локальный Go replace
выбирает patched source только при сборке. Полученный static binary не требует
этого временного пути при запуске. `go mod tidy` из Make добавляет только replace
и удаляет две checksum строки заменённого PocketBase module; прочие dependency
pins не изменялись. PocketBase `package-lock.json`, Beszel `bun.lock` и
`package-lock.json` при проверенной сборке остались неизменными.

Третий patch меняет только systems-table UI. Создание record даёт pending и
нулевые defaults; pause очищает CPU/RAM/disk, сохраняя `info.v`
(`internal/hub/systems/system_manager.go::onRecordCreate/onRecordUpdate`). Поэтому
одного наличия версии недостаточно: текущие CPU/RAM/disk показываются только при
`status=up`, непустом `info.v` и конечном числовом значении. Для остальных состояний
и отсутствующих/нечисловых значений показано `—` с пояснением «Нет текущих данных».
Измеренное число `0` сохраняется как `0.00%`; root-disk/multiple-filesystem view
проходит тот же guard после безусловного hook. Backend/collector не изменены.
Это не per-metric validity certificate: штатный backend не различает числовой
ноль, полученный измерителем, и ноль после внутреннего отказа измерителя при up.

Сборка выполнена успешно: оба frontend build, TypeScript, upstream Make,
`--version`, ELF/buildinfo с `CGO_ENABLED=0`. Это не полный light-theme gate.
Приёмка deployment, login и метрик ведётся отдельно по фактической установленной
версии; source/build не подменяют эти свидетельства.

После сборки или обновления проверить браузером OS dark и сохранённые
`ui-theme=dark`/`pbColorScheme=dark`: первый paint, login/reset/OTP, dashboard,
CPU/RAM/disk/network charts, loading/error states, settings/dialogs/dropdowns,
log/info fullscreen и PocketBase `/_/` login/collections/logs/backups. Проверить
computed surfaces/native controls и неизменность вида после смены OS appearance.
Отдельно дождаться fresh samples и history всех нужных agents; отсутствие метрики
не считать нулём. Наличие agent на PVE host не является per-VM или per-job учётом.

Stock hub update может заменить собственную сборку и убрать patches. Обновлять
в обслуживание на idle/drained builder: выбрать новый upstream source, адресно
перенести patches, повторить затронутые build/browser checks и только затем
заменить hub. Штатные agents продолжают использовать release binaries; отдельный
package factory, постоянный dispatcher или вторая система мониторинга не нужны.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Static hub собирается | Два frontend build, Make, version, ELF/buildinfo | Отдельная build среда | сохранить |
| Одного изменения defaultTheme достаточно | Prepaint, hard dark logs и отдельный PocketBase UI | Разные UI paths | изменить обе UI адресно |
| Все views и метрики приняты | Build этого не измеряет | Нужны browser/runtime samples | дополнительно проверить |
