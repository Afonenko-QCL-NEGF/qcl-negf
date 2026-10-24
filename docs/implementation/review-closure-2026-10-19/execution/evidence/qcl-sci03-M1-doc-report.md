# SCI03-M1: Results README, docs-only freeze

2026-10-20 (local user date). Единственный изменённый этим writer owning файл:
`/tmp/qcl-sci03-M1-results-worktree/README.md`. Добавлено 38 строк, удалений нет.
Existing 14585-byte README сохранён byte-exact как prefix (`cmp` exit0).
Артефакт готов к независимому R; publication/commit этим writer не выполнялись.

## Источники и границы

Read-only primary root HEAD при начале:
`d4113f43cddf02d46025434eb3a9dd8e110e90d6`; прочитаны его AGENTS.md и
docs/architecture.md. Results task worktree HEAD
`33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`, baseline README SHA256
`39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9`.
Входные production/test modifications принадлежали другим writers и сохранены.
Root status/submodule composition были прочитаны, не обновлялись; root dirty
coordinator files и protected original workspace не изменялись.

| Primary witness | SHA256 / immutable binding |
| --- | --- |
| Accepted D `/tmp/qcl-sci03-current-bound-design.md` | `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7` |
| Research owning contract | commit `3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731`, `docs/equilibrium-measurement-contract.md`, file `61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c` |
| Frozen production `src/qcl_negf_results/equilibrium.py` | `bb3d204378fd7d95691cfd9b58360afc6f48ede1b37fe7a0f6d2a6ff06944915` |
| Frozen tests `tests/test_equilibrium_diagnostics.py` | `d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79` |
| Independent implementation CPP `/tmp/qcl-sci03-M1-impl-review.md` | `c529835dfdb9ac374b3933af4403bab26ea2fb0b89494a56918f7960f8be7e8c` |

## Exact content mapping

| README lines | Accepted contract / actual source | Change |
| --- | --- | --- |
| 240–246 | D §5; Research §5.3/A.3; helper138–188, report620 | Existing API reader route, exact additive namespace/version, pinned canonical link; no formula copy |
| 248–253 | Research A.3 μ gate; helper147–164 | One shared μ; inherited exact status/reason/null before zero; independent A/correction norms |
| 255–261 | Research A.3 fields; helper149–180; accumulators526–575 | Five field groups, exact JSON names, state sum defect distinguished from sum of norms; side/variant bound and three terms |
| 263–268 | Research §5.3/A.1–A.3; actual full complex `_Norm` paths553–575 | Weighted complete-matrix norms; units1 vs A/m², no relative-current division/floor, separate side estimate |
| 270–276 | Research A.3; helper142–145,187–188 | Measured Float64 RHS separated from outward-rounded enclosure and scientific accuracy/acceptance |

README added text contains no equations, new tolerances/ε/H, API argument changes,
new read pass, executable recipe, solver command or runtime acceptance claim.
Existing public example is byte-exact unchanged. New fields are explained as
stored represented-state measurements, with no fresh-map/physical accuracy claim.

## Static checks and existing runtime evidence

- `git diff --check -- README.md`: exit0, no output.
- README-only diff: +38/−0. Baseline prefix comparison: exit0.
- Canonical URL repository matches local origin; commit/path exist via `git show`;
  source heading is exactly `### 5.3 Абсолютный represented current без division/J`.
  GitHub heading slug `53-абсолютный-represented-current-без-divisionj` checked from
  that text. Link target and A.3 source section read locally; no network check.
- New heading/table/fences reviewed as Markdown source. No rendering/build/parser
  was run. Production/tests hashes match the supplied frozen inputs after edit.
- Already executed coordinator GREEN receipt was read, not rerun:
  `/tmp/qcl-SCI03-M1-GREEN-2/receipt.json` SHA256
  `af34e8c899fb220c798b9679faa9b4c389ad8752591730cf518b6133d1fa88a0`;
  original.log SHA256
  `4a9c76be35565e97288f064ef85313f8b0b726018c12f1cd68e768fa90c2a350`.
  Raw100 bytes says `51 passed in 11.13s`; receipt exit0, wall11.797s,
  raw_capture_complete=true, no guard_error/stop_reason/overrun. This is bounded
  synthetic software-fixture evidence, not S1/native/scientific acceptance.
  Historical receipt date2026-10-19 preserved.

Only bounded source/text/hash/Git reads and README/artifact writes were performed.
No target execution/imports/parsers/tests/build/Julia/Nix/network/server,
children, stage/commit/push or root/checkpoint edits. CONTRIBUTING docs-only rule
and qcl-physics-audit applied. Read/output stayed within task caps; no claim of
instrumented physical I/O/RSS measurement for this text task.

## Frozen outputs

| Output | SHA256 |
| --- | --- |
| README.md,18619 bytes | `830c67bc0fc0e43c2ae698dbe5c5aa8f518728b6f3f5d760dafb505d3da9e648` |
| `/tmp/qcl-sci03-M1-doc-patch.diff`,4517 bytes | `44be8861b19bf04966eb9a692af95bed9fdb7d8b0975f573dcadea02488a6f32` |

Companion `/tmp/qcl-sci03-M1-doc-identity.json` records exact scope and bindings.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| README объясняет accepted additive fields и unknown μ | Mapping выше; D§5, Research A.3, frozen actual source | Writer source/static verification; independent R ещё предстоит | сохранить |
| Existing text/API и production/tests сохранены | +38/−0, baseline prefix cmp, unchanged source/test hashes | Нет новой runtime проверки writer | сохранить |
| Scientific accuracy/S1 acceptance доказаны | Отсутствует такое свидетельство; GREEN ограничен synthetic fixtures | Roundoff enclosure/domain/fixed-point/experimental error unknown | данных недостаточно |

STOP: docs freeze для отдельного независимого R и coordinator publication.
