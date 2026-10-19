# RV13 selected denominator (frozen before symbol reading)

Root S=`e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; Platform P=`4ce214e29b72276157b10a9267e2f30fef4ac66f`; root overlay receipt `../source-receipt.json`. Stage: public source review only.

Finite selected properties, N=7:

1. A1 — four public roles and mutable storage owners distinct from image/Nix closure.
2. A2 — coordinated PostgreSQL/AiiDA repository snapshot with paused writers and profile binding.
3. A3 — archive manifest/hash/member integrity and no overwrite/retention/disk admission.
4. A4 — restore admission before destructive writes; DB/repository generation mismatch and interrupted restore disposition.
5. A5 — synthetic fixture guarantees separated from PostgreSQL/service/cold-start evidence.
6. A6 — Proxmox/local-lab persistent dataset lifecycle and exclusions for foreign VM/data.
7. A7 — incident→recovered timeline and sanitized inventory contract sufficient to bound public operations, with missing site data affecting only live cells.

Selected roles={controller,worker,cache,submitter}; backends={Proxmox,local-lab}; scenarios={archive-create,checksum/member rejection,restore-to-empty,interrupted DB/repository restore,reinstall/cold-start,foreign/shared dataset exclusion}. Selected catalogue is partial of all possible cells; native cells `not_measured`. N counts seven declared properties, not Cartesian cells.

Budget author ≤12 min, independent reviewer reserve ≤8 min; extracts ≤96 KiB, section ≤8 KiB, ≤1 CPU/≤1 GiB/process. No tests/build/eval/SSH/import/install. Scope only reports and proposed tickets; no operations or product modifications. Stop after A1–A7 dispositions or cap. Site secrets are neither required nor requested for public source findings.

Source-reading erratum, preserving N=7: the initial role vocabulary above was a hypothesis, not discovered topology. `nix/site-preflight.nix::roles` and private-site template actually select `{storage,control,compute,ci}`; controller/worker are service roles, submit is enabled on control, cache is a module rather than a selected image. `tofu/local-lab/main.tf::local.machines` instead selects `{control,storage,worker-1,worker-2}`. Report uses these discovered finite catalogues and does not claim cache/submitter images.
