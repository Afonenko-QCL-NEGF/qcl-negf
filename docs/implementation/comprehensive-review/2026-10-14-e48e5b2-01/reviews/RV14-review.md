# RV14 · Независимый closure review

Blind eight-link findings сохранены в `RV14-blind.md` до чтения candidate/fix. Denominator: Git/source/JULIA workspace/standalone/depot-build/frontend/wheels/manifest/serve сгруппированы ровно в восемь declared links. Review статический: imports/build/tests/self-check/runtime не выполнялись. Full S/component refs и dirty hashes — source-receipt. Прочитанный candidate SHA256 `5ee52ab1ea125033b1df79f56546fcf66e60797812332a6ea31b1abe10528f04`; последующая проверка exact labels не требует source rerun.

**Verdict:** source-link mapping и stale-assets negative обоснованы; executable freshness/reproducibility/import acceptance правильно оставлены `not_measured`. Blocking findings отсутствуют. Future asset discovery/design ticket bounded, не grants installation/build.

Independently established: sourceGraph rejects dirty/mismatched composition; Pkg.develop workspace path differs от Runner Project Core tag route; mkPreparedDepot binds root ref и Manifest hash; buildSolver checks revision and prefetched file hash; frontend derivation has filtered input/native npm hash+Node version; root release frontendBuild precedes four wheel hashes and graph recheck; deploymentManifest binds source+narHash closures; wheel artifacts payload→conditional StaticFiles. These are source contracts, не measurement actual native closures.

Portal `10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb:hatch_build.py:9–14` checks wheel/noneditable target, `index.html` file, at least one JS glob. It reads neither source nor lock hashes. Hypothetical stale index+JS passes this boolean branch; executable stale fixture не запускалась. Root `ops/environment.ts::frontendBuild` and Portal `nix/frontend.nix` are separate generation routes, поэтому direct-wheel risk нельзя назвать demonstrated regression всей release pipeline. Candidate сохраняет это различие.

| Severity / locator | Finding | Коррекция |
|---|---|---|
| P3 · `RV14.md` final table «Direct wheel guard доказывает freshness» | Positive assertion contradicts body and cited existence-only source condition | «Direct wheel guard не доказывает source freshness» |
| P3 · `RV14.md` final table «Standalone receipt переносим по версии» | Body correctly says same version недостаточна; positive label может читаться как opposite rule | «Одной версии недостаточно для переноса standalone receipt» |
| P3 · `RV14.md` final table «Release воспроизводим/принят» | Source-only witness не establishes M07/M08/acceptance; table label лучше назвать unresolved claim явно | «Reproducibility/release acceptance не измерены» |

M06 applies eight selected source links, полного runtime identity closure нет. M07 requires declared bitwise outputs/two builds; M08 consumer self-check and fixtures остаются future scope. M20 CPU/RSS/I/O отсутствуют, не ноль. Researcher/operator/developer role actions точные. Asset ticket READY discovery/design, implementation remains unauthorized; fixture budget ≤2 attempts/1CPU/1GiB/5min/4MiB/no install — conditional on existing prepared environment. Native tests не наделяются scientific acceptance; new root ref не наследует old full-release CI.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Eight source links reproduce selected mapping | Source paths в blind report, Gitlinks S | Actual compiled/imported/runtime refs missing | сохранить |
| Hook guard лишь presence | Exact initialize source conditions | Negative fixture статический, не executed | изменить |
| Version0.2.0 не source identity | Runner tag versus workspace paths | Standalone actual resolved commit неизвестен | данных недостаточно |
| Full native release acceptance отдельно | Source manifests/gates and not_measured M07/M08 | Build/consumer proofs missing | дополнительно измерить |

## Round1 scoped recheck

Candidate SHA256 `3c5ba822fc26ea00a7111dd2c20a3f56d1fbf9854e69c6a9334db0f6050c0dee`: три labels явно говорят не доказывает source freshness / перенос standalone receipt по версии не обоснован / воспроизводимость-приёмка не измерены. P3 findings закрыты; eight-link source graph и original inputs не перечитывались.

## Round2 scoped metric recheck

Candidate SHA256 `430c4bca1cdfa821c80feaaf8f1665243aa51c2a2ac205cb7497f1942b353c0b`: source-locator coverage explicitly administrative; canonical M06 source→build→import/runtime closure `not_measured`. Counts do not confer closure pass. Changed metric sentence only checked; source graph not repeated. Prior findings and original reviewed hashes retained.
