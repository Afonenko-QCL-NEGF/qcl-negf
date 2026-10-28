# Совместимость подготовленного Julia depot

Режим Runner описан отдельно в
[native capture](../components/QCLNEGFRunner.jl/docs/depot-native-capture.md).

Root source graph по-прежнему выводится из committed gitlinks. Depot v1 привязан к exact producer
graph. Root сохраняет прежние extension metadata/Unicode bytes при normalization v1; portable worker
v1 по-прежнему принимает только шесть полей. Ручной retagging `sources` не поддерживается. Без
original trusted receipt шесть v1 полей не доказывают, что producer graph не сфальсифицирован.

V2 сохраняет original `sources`, Julia/Manifest, URL/SRI archive и добавляет закрытый
`compatibility`. CURRENT selected graph задаёт source URL новой сборки. Совпадение native dependency
inputs позволяет reuse старого qualified archive при docs-only или обычном runtime source изменении
без local selector. Project/Manifest/Artifacts/native factory/recipe меняют inputs.
Root/Nix/portable worker проверяют bindings; это не измерение native platform при чтении JSON.

## Явная подготовка и qualification

Из чистого опубликованного CURRENT checkout выполните отдельную разрешённую native операцию:

```sh
deno task solver:depot /var/lib/qcl-negf-artifacts/attempt-new --format v2 --profile production-build --test-workers 2
```

Команда реализует выбранную pinned Nix Julia factory, запускает её на immutable selected project с
пустыми HOME/depot, `JULIA_LOAD_PATH=@:@stdlib`, generic CPU target и pinned CA bundle. JULIA
override не используется. Pkg builds и autoprecompile отключены. Manifest обязан остаться
неизменным; captured external source/artifact trees проверяются. Registry присутствует и сохраняется
в archive, но script не сравнивает его с заранее объявленным registry tree. Workers выбираются по
ресурсам конкретного native builder; production/null и local-debug/2 режимы сохраняются.

Output содержит `native-facts.json`, `depot.tar.gz`, `depot-candidate.json`. Candidate имеет schema
`qcl-negf.julia-depot-candidate.v1`, **не** usable depot format. Unknown selector не получает
approval от одного успешного execution. Trusted builder SOURCE review exact external
selector/augmentation closure устанавливает отсутствие чтения изменяемого local runtime source за
пределами inputs. Current locked HDF5/MPI Linux default входит в supported qualification, включая
MPICH default и actual effective preferences/platform/lazy selection. Optional custom local `.pkg`,
preferences, overrides и неизвестные path dependencies требуют отдельной поддержки/qualification.

В том же owned output namespace сохраните SOURCE review и explicit qualification JSON:

```text
{
  schema: qcl-negf.julia-depot-qualification.v1,
  candidate_sha256: SHA256 exact raw depot-candidate.json,
  inputs_sha256: SHA256 canonical candidate.inputs,
  native_facts_sha256: SHA256 canonical candidate.native_facts,
  source_review: {path: relative/path.md, bytes: positive integer, sha256: exact raw SHA256}
}
```

Объекты закрытые, unknown/duplicate fields запрещены. Review path нормализован, лежит внутри owned
namespace; symlinks/hardlinks/path escape и writable-by-others inputs отвергаются. Qualification —
assertion trusted builder о завершённом SOURCE/native review. Hash связывает точные bytes, но не
доказывает смысл текста. Команда не создаёт approval сама:

```sh
deno task solver:depot /var/lib/qcl-negf-artifacts/attempt-new --format v2 --test-workers 2 --qualification qualification.json
```

Finalize повторно связывает CURRENT inputs, original candidate/facts/archive и review. Julia/build
не переигрываются; `solver-depot.json` создаётся только новым immutable output. Original producer
`sources` сохраняется даже при другом CURRENT docs-only graph. Ошибка или существующий output не
вызывает repair/replay. Failed original attempt сохраняют, исправление получает новый receipt.

## Использование

```sh
deno task solver:build /var/lib/qcl-negf-artifacts/attempt-new/solver-depot.json --test-workers 2
deno run --allow-read --allow-write --allow-run ops/application_cd.ts /var/lib/qcl-negf-artifacts/attempt-new/solver-depot.json release.json --test-workers 2
```

Profile/workers должны выбирать exact qualified Julia factory. Local-debug archive отдельно
производится с `--profile local-debug`; равенство VERSION разных factory не принимается за ABI
proof. V2 mismatch отклоняется до archive prefetch/application build. Same-FD capture,
UTF8/duplicate/depth/ 64 KiB guards и normalized consumed JSON SHA/length сохраняются. Selected Nix
проверяет inputs повторно. Metadata/sourcegraph/qualification не входят в depot/runtime derivation:
только archive URL/hash попадают в depot builder. Build result связывает actual stdout drv/output и
installed Manifest; release `solver_build` сохраняет прежние четыре поля.

`workerDepotBinding` экспортирует bounded portable binding из actual Root build result и exact
selected source-graph record. Для v2 `records/depot.json` — exact normalized consumed JSON bytes;
original raw input остаётся у publisher в Root receipt. Portable worker проверяет source/lock/
native/consumed joins, а не запускает Nix или independently измеряет native compatibility.

Source fixtures не запускают Julia/Pkg/build. Native factory installCheck, actual v2 prepare,
external selector/default qualification, offline package installCheck и deployment — разные gates.
Source GREEN не заменяет ни один из них и не объявляет scientific acceptance.
