# D05: native host root and protected image-stage preparation

The Platform component now owns two separate, disabled-by-default operations:
absolute growth of an existing native root LV/ext4 filesystem and preparation
of a protected temporary image filesystem in an existing thin pool. Private
inputs bind host/boot identity, exact storage identities, finite limits and
fresh admission. The selected source is the published Platform gitlink.

Owning source: [Platform #9](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/9).
Shared pools and foreign guests are preserved. Image copy/cutover and additive
host swap have separate contracts and are not performed by this preparation.
The protected host volume remains outside the QCL runtime wipe set.

Independent review repaired multi-segment LVM handling, loaded mount-unit
safety, canonical device aliases, volatile usage comparisons, namespace scope,
strict filesystem UUIDs, numeric postconditions and normalized mount options.
The Ansible collection remains pinned to `community.general` 13.4.0.

| Claim | Evidence | Limitation | Decision |
| --- | --- | --- | --- |
| Original storage guard repairs have regression coverage | 45 scenarios and syntax pass at the preceding repair source | Recording fake native boundary; retained fork warnings | Keep |
| Final normalized mount-option repair is covered | Ten new positive/negative cases and syntax pass on the selected source | Actual Ansible task engine; native commands remain fake | Keep |
| The complete final 55-case packet passed | Full packet reached its 360-second deadline without a pytest summary | Original partial log retained; no automatic rerun | Insufficient data; do not claim a full-suite pass |
| The change is ready for publication | Independent source reviews, diff check and scan of 2,082 added lines found no credential/address matches | Pattern/literal scan cannot prove absence of unknown secrets | Keep the reviewed source |
| Native disk, persistence and scientific acceptance are established | No server mutation, boot check or solver invocation in these packets | Fresh native admission and subsequent operations remain separate | Insufficient data |

The ten bounded test invocations, including failed and timed-out attempts, are
retained. These engineering checks neither change the physical model nor
establish S01 scientific acceptance.
