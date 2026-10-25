# DEV07 local harness v1 — source eligibility review

2026-10-19. **PASS для monotone tightening accepted C08 v3** и normal-stop
eligibility внутри L-JL120s. Hard realtime, hard RSS/TMP/output quota и transient
peak proof не установлены. Никакой harness/helper здесь не импортирован и не
исполнен, Julia calls0. Этот review не является fresh runtime BIND/admission.

Фактически пересчитаны:

- `/tmp/qcl-julia-dev07-run-v1.py`:
  `62b7250c6be7344f5afb767b6f9153f2074fde7c9967ff1bd2e88551c56ace9a`.
- Supplied diff: `f3bb1fa4b9819a32e30c04e680f2a1a73c7d2a59b9db301d4a1d5ab4e57698ac`.
- Base `/tmp/qcl-julia-c08-run-v3.py`:
  `d454f20503108bfa7b40df921b7e4acf4fd4d049bbaf1801c4a3a05de36ad112`.
- RawCapture helper: `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f`.
- TEMP sampler: `16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e`.

Actual `diff -u base candidate` соответствует supplied diff: только
CPU570/575→90/95, child wall570→90, sampled RSS4→2GiB, raw threshold/post-drain
envelope8→2MiB и receipt fields этих же limits. Hash-guarded helper/sampler
composition, allowlisted trusted component fixtures, affinity1, offline prepared
runtime/project/depot, BLAS/Julia threads1, own TMPDIR16MiB, raw preservation,
SIGTERM/SIGKILL/drain/fallback, failure/exit predicates не менялись.

Прочитан accepted base review `/tmp/qcl-sci05-local-bind-harness-review.md`;
его исторический source/runtime BIND не переносится на текущий запуск.
Старые caveats сохранены: process-tree RSS/TEMP/output sampled, RLIMIT_CPU
per-process, raw drain может превысить output envelope с честным failure,
non-daemon capture/I/O/scan overhead не дают hard deadline. При ordinary stop
90s trigger + inherited nominal23s cleanup=113s, остаётся nominal7s до120s;
это плановый reserve, не доказанная wall upper bound для arbitrary kernel/I/O.

Harness root по-прежнему main shared checkout
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, **не** isolated
`/tmp/qcl-dev07-absolute-worktree`. Поэтому до вызова координатор обязан
связать fresh main owning HEAD/file bytes с принятым DEV07 test SHA,
exact argv, prepared project paths и current admission. Этот review не
подтверждает перенос source, staging/publication или latest resource state.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Resource predicates только ужесточены | Exact source diff и hashes | Sampling не hard quota | сохранить |
| Guard/raw-capture composition сохранена | Base/hash-bound helper и sampler equality | Runtime не выполнялся | сохранить |
| Normal-stop nominal reserve входит в120s | 90+23=113s | Overhead/I/O не hard bounded | сохранить |
| Exact DEV07 call уже READY/выполнен | Здесь таких данных нет | Fresh BIND/admission main bytes/argv остаётся координатору | дополнительно измерить |

**STOP.** Tooling source eligible; imports/parsers/tests/network/server,
Git mutations и runtime attempts не выполнялись.
