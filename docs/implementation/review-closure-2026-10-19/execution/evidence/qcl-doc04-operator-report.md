# DOC04 public operator slice — author freeze

2026-10-20. Docs-only, public authored prose; готово для независимого high R.
Единственный новый product file: `docs/public/operator-recovery.md` в isolated
`/tmp/qcl-doc04-operator-worktree`. Root/main/checkpoint и другие slices не менялись.

## Source binding и isolation

Явно порученный local clone создан через `git clone --no-hardlinks --no-checkout`
из primary root, затем checkout exact
`d4113f43cddf02d46025434eb3a9dd8e110e90d6` на branch
`codex/review-closure-docs-operator-reader`. Network и submodule init отсутствуют.
Начальный status чист; final status только `?? docs/public/`, содержащий ровно
новый chapter. Восемь gitlinks прочитаны; selected Runner1acc/Coree431/Research3ed/
Contracts12fc использованы через immutable `git show` из доступных component repos.
Они не копировались/обновлялись в clone.

| Primary input | Immutable identity / SHA256 |
| --- | --- |
| Accepted D `/tmp/qcl-doc04-design.md` | `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b` |
| Accepted R `/tmp/qcl-doc04-design-review.md` | `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164` |
| Frozen pilot plan `/tmp/qcl-doc04-root-worktree/ops/docs/pilot-plan.json` | `cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50` |
| Approved canonical DOC03 candidate `/tmp/qcl-doc07-canonical-candidate.md` | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`; this is file SHA256, not Git commit |
| Its accepted independent D2 R | `f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231` |
| Root AGENTS / architecture at d4113 | `ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330` / `8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7` |
| Root `docs/single-server-deployment.md` at d4113 | `8f659f7ee6dc3a5ff89acba052b1eadbcbeb2436fa6429d47d8dd400948da242` |
| Runner `docs/src/user/results.md` at `1acc165650fd4f4c2d49605cc679f90e3f6fcdae` | `39e1178fc88a940b69ad61298d54538f44d1e39df6b9d9c2dd8e5264f395f561` |
| Runner `src/cli.jl`, same commit | `aa5e129312707a7927e1bc97caf4c830c7cf9ed29cf12c648f8afbd7fbcf2cd0` |
| Runner `src/infrastructure/persistence/point_artifacts.jl`, same commit | `9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4` |
| Core `docs/src/theory/12_validation.md` at `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee` | `be55b03e7a228aebad88b24410d2633cd575ae63211a01ff4187f2c1bb95755b` |

## Content/source mapping

| Chapter | Primary witness | Preserved boundary |
| --- | --- | --- |
| Source/known/unknown prerequisites | Root architecture; DOC03 approved candidate1012–1059 | Archive identity vs current source; docs binding, metadata availability, value origin and science remain independent; missing/corrupt mandatory artifact refuses |
| Staging/data preservation | Root runbook188–294, architecture storage boundary; Runner results119–194 | Metadata/payload budget before copy; raw/pointers/failed attempts retained; local publication differs from LAN/restore; no final pruning for recovery |
| Acknowledged selection | Runner results24–71; point_artifacts684–713 | Verify current then previous with digest/commit/receipt/all artifacts; pending not resume; explicit no-valid-generation error |
| New-attempt handoff | Runner results39–46,166–194; CLI74–91 | Exact existing run-plan/recovery-bundle grammar; separate OUTPUT, attempt increases, cumulative budget retained, complete prior-final closure; execution clearly labelled |
| Scientific interpretation | Core validation12–60; Research contract at3ed8a9f | No formulas/thresholds or new criterion evaluator; operational recovery does not establish scientific acceptance |

One `text` fence contains the exact conceptual CLI syntax from selected Runner,
not an executable installation-specific recipe. All uppercase placeholders are
explained. No real hosts, usernames, absolute private paths, SSH, credentials,
inventory values, historical raw receipts/logs or numerical arrays are in chapter.
Protected S01, foreign jobs/VM and existing disks/data remain preserved.
No automatic deploy/format/cancel/restore command was added.

## Link/anchor/static checks

Pilot primary URL is exactly `operator/recovery.html#operator-recovery`.
Explicit Documenter anchors in chapter:
`operator-recovery`, `recovery-prerequisites`, `staging-prerequisites`,
`recovery-selection`, `recovery-handoff`, `recovery-owning-references`.
No duplicate explicit IDs. The pilot's `operator-recovery-route` remains the
selected Runner results anchor, not a duplicate renamed root anchor.

Cross-section targets:

- `../runner/user/results.html#operator-recovery-route`: selected Runner source
  has exact `@id operator-recovery-route`; complete existing owner page graphs
  are accepted pilot support policy.
- `../core/theory/12_validation.html#researcher-final-route`: selected Core source
  has exact `@id researcher-final-route`.
- Three external HTTPS source refs use exact 40-hex commits and existing paths:
  Runner results1acc, Research equilibrium contract3ed, Contracts artifacts12fc.
  Paths verified with `git show`/`cat-file`; public URI refs contain no query,
  userinfo or private locator. They are source references, not downloaded assets.

`git diff --no-index --check /dev/null docs/public/operator-recovery.md`: exit0,
no output. This explicitly checks the new untracked file. Markdown source reviewed:
one closed text fence, valid parallel tables/list, no math/code API definition.
Chapter is below24KiB. `rg` source scan and manual public-content review find no
private path/SSH/secret/templateTODO. No rendered/browser/link-network proof is
claimed; final path/anchor/offline serving checks remain later pilot gates.

Only local clone/checkout setup explicitly authorized for isolation changed Git
metadata. No stage/commit/push or further Git mutations. No target execution,
imports/parsers/tests/Julia/Nix/render/build/network/server or children. No palette
or UI changes: accepted fixed-light rule remains intact. Named source text reads
are bounded below3MiB; physical Git object copy/I/O/RSS not instrumented.

Companions: `/tmp/qcl-doc04-operator-identity.json` and
`/tmp/qcl-doc04-operator-patch.diff`; chapter hash/bytes recorded in identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Public operator journey covers source→readiness→failure retention→handoff | Exact mapping and source checks above | New authored prose awaits independent high R | сохранить |
| CLI and selection route reflect implemented source | Selected Runner CLI74–91, reader684–713, owning docs | Source-only, no actual run/import/restore | сохранить |
| Native readiness, successful restore or scientific acceptance established | No installation evidence supplied or executed | Missing runtime/inventory/admission are not pass | данных недостаточно |

STOP before independent high R and Root copy/publication.
