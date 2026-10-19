# DEV08 ratio propagation — frozen implementation

2026-10-19, I medium. Only
`test/numerics/principal_value_independent_oracle.jl` changed.
No Julia/import/tests/solver/build/install/network/Git actions; no source,
docs or DEV03/04/06 edits. All original failed logs remain untouched.

Accepted design SHA256:
`cdbed6971dce106613face5c1235f7ab914a49ba1fdadf8c1987a37002d4b17c`;
independent review SHA256:
`374672b3d4cce86fd8f1272c9464d0c72ddc52a89b5f6272300ebdcd06567238`.

New full fixture SHA256:
`4533b1058eb351d5796df18c86ac3b2e2af767078e16bd4cec25588b8e34f70a`.
Incremental diff `/tmp/qcl-dev08-ratio.diff`, SHA256
`d3a8a9bf4ef81591c2fab3ff5134a28291e8d3e8ed3f54950fe4f11d0774f139`.
Before fixture SHA256:
`bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e`.

ATOL=RTOL=2e-13 retained. All discrete literals, finiteness, zero/sign/
diagonal/cyclic, center/omitted-cell/tail/window and measured first-order
positivity assertions retained without change. Only the two unjustified
ratio-isapprox predicates replaced by accepted outward interval.

Independent expected errors are `(2/N)/(2pi)` for N17/33/65. Each separately
recomputed measured error has finite/positive/(0,1) and unchanged strict
scalar isapprox checks; failed precondition triggers a labelled fatal stop
before ratio work. No reuse of earlier W3 call as evidence for a later call.
`B=nextfloat(ATOL)` bounds existing scalar gate. Endpoint additions/
subtractions and quotient divisions use prevfloat/nextfloat as designed;
nonfinite/nonpositive endpoints stop before division, invalid resulting
interval stops. No denominator floor, empirical multiplier or new ratio
atol/rtol. Endpoints come only from independent expected errors. Each interval
contains independent grid ratio rho=NB/NA and the measured quotient.

Pure scalar controls add zero operator evaluations: healthy inputs and
independent +/-ATOL/2 perturbations pass; constant and second-order ratios
are excluded; common multiplier2 keeps ratio but fails strict functional
amplitude; common sign reversal keeps ratio but fails positivity and strict
amplitude. Existing functional evidence therefore remains mandatory.

Independent source/hash checks confirm other fixtures unchanged:
- DEV03: 6adaeea85abf95e21dd0beb763dada3a73d588cae1ed5a5d536eb0e8841a2a1e
- DEV04: 9aab7a4eea3a7fcb93033d2c9f6f3b420f6b1872843168e0deb98461f2602730
- DEV06: 17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01

No runtime result claimed here. Parent reports DEV03 GREEN2=16pass,
DEV04 GREEN2=183pass (exact donor guard witnessed), DEV06 GREEN1=248pass;
this author did not rerun them. Existing DEV08 GREEN1 failure retained.
Root owns remaining DEV08 GREEN2, invocation2, ≤120s/1CPU/2GiB,
≤16MiB temporary/2MiB logs in existing ready environment. Stop on failure/
timeout/nonfinite/precondition, preserve raw evidence, no automatic retry.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Ratio follows unchanged scalar error gates | Independent outward endpoints, fatal guards, retained functional assertions | Updated runtime not_measured | дополнительно измерить |
| Sign/amplitude/order distinctions retained | Explicit pure scalar controls and original operator controls | Assertions not yet executed | сохранить |
| Production/other fixtures/docs unchanged | Scoped incremental diff and original fixture hashes | No new scientific acceptance evidence | сохранить |
| DEV08 fully passed | New predicate not executed here | Root GREEN2 required, last allowed invocation | данных недостаточно |
