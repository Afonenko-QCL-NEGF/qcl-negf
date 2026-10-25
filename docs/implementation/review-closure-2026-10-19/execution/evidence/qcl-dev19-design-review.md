# DEV19 independent CP-DESIGN

Вердикт: **CHANGES_REQUESTED — одна load-bearing конкретизация R1 перед DEV20 I-ready**. Остальные schema/inventory/import-route границы пригодны для реализации в заявленном scope. Это read-only source/design review; reviewer installs/imports/build/tests/Node/Nix/solver/server не выполнял. Existing static assertion не принят за DOC05/native wheel evidence.

## Binding и source-first

Portal HEAD `b9a876aa22d84dc13435bf970728b033d1345ba8`, branch `codex/review-closure-package-identity`; dirty ровно README и новый docs/package-identity.md. Сначала прочитаны actual hook/Vite/package-lock/package scripts/tsconfig/index/light CSS, root ops/environment.ts+release.ts, Portal nix/frontend.nix, platform nix/application.nix, Runner Project/prepare-workspace routes и Results pyproject/source_ownership helper; собственное краткое заключение передано root **до candidate**. Прочитаны Portal AGENTS/CONTRIBUTING, root architecture/handoff DEV19/20 и primary RV14/RV02/fixcards. Parent stage read-only, новое build разрешение не выводится из D-пакета.

- Owning `docs/package-identity.md` SHA256 `d59be5f43d72d1604bc29ca962d9eb375f17c0a26066974d19caac730279bb59`.
- README `2c37cb053f0f36024249ceaeb9c0cb0b71d4415319295ecf56c9f2e9981b5ae3`.
- Author report `/tmp/qcl-dev19-design-report.md` `1e3e3c9a2fed85775a03de015fdf5ca9586aa2a49f2b2e443c6be8e3ef94ec81`.
- Full patch `/tmp/qcl-dev19-design.patch` `249aa32eac06e8e83f456e4ff5ddf565b04c702e1985ed25701b562b8532f564`; current README diff + new-file diff independently byte-equal. `git diff --check` exit0.

## R1 — blocking: связать receipt publication с новым output в объявленном root

Локаторы candidate:84–92(mode detection),178–199(build lifecycle),279–284(required negatives). Actual source: Vite build.outDir/emptyOutDir в frontend/vite.config.ts:4; baseline hook принимает старые index/JS.

Mode определяется literal byte sequence/count, а до build удаляется **только receipt**. Целое старое static/dist payload остаётся; его обновление делегировано effective Vite config и emptyOutDir. Текущие words «остальные outDir/config variants отвергаются» и «emptyOutDir:true сохраняется» задают нужное намерение, но нет точной implementable границы проверки effective output либо отдельного clean-known-output условия. Проверить лишь наличие одного token недостаточно.

Различающий случай: frontend source config сохраняет единственный token `../src/qcl_negf_api/static` (например как прежнюю строку/комментарий), но effective build.outDir стал иным/computed; либо вывод выключен/перенаправлен config logic. tsc и Vite могут вернуть0, не тронув известный static. Если wrapper затем инвентаризирует оставшиеся старые index/JS и подписывает их новыми input hashes, stale payload получает «fresh» receipt. Это воспроизводит исходную цель RV14 F14.1 без злонамеренного изготовления JSON; self-consistent output hashes сами не подтверждают, что текущая генерация затронула этот root.

Минимальный D выбор (не новый dependency/workflow):

1. Либо exact supported config/recipe guard, достаточный для доказательства actual outDir и emptyOutDir=true; freeze его проверяемые условия и negatives, а не только token count. Если разрешаются лишь два известные concrete config forms, это надо сказать явно; произвольные TS semantics нельзя молча считать проверенными regex.
2. Либо wrapper после проверки ownership/symlink safety независимо очищает/recreates **выбранный известный generated output** перед compiler/Vite; после success принимает только вновь возникший полный payload. Receipt-only invalidation остаётся для обоих режимов. Это убирает усыновление старого output даже при zero-exit/no-output build; не требует нового Node dependency, wheel-hook build или Nix/root workflow change.

Точные правила cleanup при ошибке/unsafe roots должны сохранить original failure и не удалять foreign state. Не добавлять stamp-only/adopt-existing-output mode.

Самый дешёвый fixture: до build положить старый valid index/JS/stamp; mocked controlled compiler exits0, но не пишет выбранный output (или поддержанный test config перенаправляет outDir, оставляя mode token). Build обязан отказать без published receipt; Python hook не принимает прежний tree. Отдельный finite positive runner создаёт новый expected payload и получает receipt. Повторить для source-static/nix-dist. Этот tiny control не требует npm install/native build; он конкретизирует уже требуемый stale-output negative, а не расширяет DEV20 scope.

До этого уточнения нельзя выдать unconditional medium DEV20 READY. Не предлагать ослабление source inventories/выдачу old stamp после compiler error как решение.

## Проверенные положительные решения

- Format v1 задаёт точные field sets/order, duplicates/NaN/types rejection, canonical encoding/LF, max-safe integer sizes, sorted UTF8 path inventories и3canonical digests. Rows содержат только path/bytes/hash; self receipt excluded ровно по одному имени. Generated ignored artifact не maintained revision lock и не builder signature. Dependencies installation byte identity честно вынесена во внешний route receipt; version fields не названы integrity proof.
- Полный current frontend source, lock, recipe wrapper, hidden/public/test files включены; node_modules/dist excluded, symlinks/special/.env/unsafe names rejected; output inventory включает extra/missing/altered CSS/JS/fonts/maps и hidden files. Hook stdlib-only независим от Node generator, no package imports/network/rebuild, editable bypass не release claim. Fail-closed reason enum/RuntimeError и Node verify read-only заданы.
- Lifecycle invalidates stamps до TypeScript, inputs/toolchain checked до/после, publication temporary exclusive same-directory file→flush/fsync→rename last→verify; failed cleanup не переписывает original error. Сериализация одного source tree явно требуется; whole output atomic snapshot не обещан. R1 относится к свежести предъявленного payload до этой atomic receipt publication.
- Source-static и nix-dist различают exact current Nix config replacement; hook для nix-dist преобразует только vite.config.ts bytes, а output читает всегда физический wheel static root. Это не arbitrary receipt-controlled path. Nix installPhase cp dist/. и platform cp ${frontend}/. действительно сохраняют hidden receipt. Wrapper внутри frontend включится в существующий cleanSource route; scripts.build entrypoint сохраняет npm run build у root/Nix. Не требуются root release/Nix hash edits для одной script change без lock/dependency изменения.
- Root release frontendBuild→locked sync→uv build --no-sources→четыре wheel hashes→sourceGraph repeat остаётся прежним outer route. Actual wheel bytes/installed import/browser/theme/offline outcome не объявлен измеренным.

## C2 — Nix projection limitation, не дополнительный blocker текущего baseline

Source `nix/frontend.nix:7–9` исключает basename node_modules/dist **на любой глубине**, затем lib.cleanSourceFilter; candidate106–107 исключает лишь top-level dirs. Для нынешнего перечисленного frontend input tree иных совпадений/filtered payload не обнаружено, current intended transform совместим source-wise. Однако фраза «все будущие regular files» не доказывает universal exact Nix projection: например nested src/dist или фильтруемый backup/compiled file может присутствовать у hook и отсутствовать в Nix source. Он должен дать mismatch/unsupported route, не ignored row или adoption stamp.

В DEV20 сохранить full inventory и fail-closed mismatch; documented source-wise Nix compatibility ограничить текущим/проверенно projection-compatible tree. Cheap fixture может показать, что nested excluded source нельзя молча выкинуть из hook inventory. Изменение фильтра/maintained second SHA list не требуется и не разрешено этой карточкой. Native derivation/Nix source filtering acceptance остаётся DEV22/BUILD, не наследуется из token transform.

## Route matrix и ограничения

Runner standalone Core source tag v0.2.0 и workspace post-tag path разделены корректно. Tag commit independently read `92a217a31f2d0cdec503cb8e9c162709d2a89fd8`; одинаковая version0.2.0 не равна source identity. Results guard проверяет expected file owner по sibling/explicit absolute override/distribution file metadata, но не заменяет trusted wheel/source hashes. Candidate требует independently selected expected owner, actual module file hashes/direct_url/RECORD+trusted artifact; missing metadata explicitly recorded. Relocation/private path sanitization не выдаются за отсутствие private raw evidence.

Frontend receipt schema не содержит timestamps/private roots/env/secrets. Exact outer command/runtime/manifest/derivation/content/native-test-contract fields в отдельном per-route evidence; это derived receipt, не параллельный Git lock. Wholeweb fixed light/current local assets rules сохраняются, CDN/theme injection запрещены. Source CSS содержит color-scheme:light; actual offline/light browser checks здесь not_measured. Один старый missing-asset assertion/HTTP200 не закрывает wheel/native/browser gates.

Build/export/import implementation ещё нет; существующие cmds npmci/npmrunbuild/uvbuild требуют отдельного конечного BUILD admission, документ не запускает их. Указанный lack of malicious-builder attestation не отменяет R1: исправление относится к ordinary supported zero-output build и исходному stale asset invariant.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Receipt/data/schema/hook интерфейс конкретен | explicit fields/inventories/recipe/failure lifecycle | generation freshness R1 ещё требует freeze | изменить |
| Stale old payload не может получить current stamp | token-only mode +receipt-only invalidation оставляют R1 path | actual implementation ещё нет | изменить |
| Current root/Nix modes имеют source route | exact outDir patch и whole output copy | C2 current-tree scope; native not_measured | сохранить |
| Import route identity отделена от version | actual Runner/Results metadata/helper +route matrix | actual route imports/wheels не измерены | сохранить |
| Medium DEV20 unconditional I-ready | R1 acceptance condition не конкретизирована | один narrow D correction достаточен | данных недостаточно |
| Native/browser/fullCI/scientific acceptance | соответствующего evidence нет | D-source review не build/experiment | данных недостаточно |
