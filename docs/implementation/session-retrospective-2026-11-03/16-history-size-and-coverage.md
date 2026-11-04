# Исторические срезы размера и покрытие Git-истории

Это вспомогательное quantitative evidence к13–15. Метод text-line categories тот же, что в01; не
semanticSLOC и не developerhours. Срезы выбираются из first-parent истории каждого named published
component tip по commit-time cutoffUTC. Это независимые component snapshots на дату, а не обещание,
что они были одновременно установлены или выбраны Root. Creation = первый видимый parentless Git
import, который уже содержит код; pre-import development не восстановлен. Отдельно Root содержит
gitlinks, поэтому они не разворачиваются повторно.

| Epoch          | 8components text lines | 8components source/build | 8components tests/fixtures | 8components schemas | Root text lines | Root plans/evidence |
| -------------- | ---------------------: | -----------------------: | -------------------------: | ------------------: | --------------: | ------------------: |
| creation       |                164,396 |                   54,401 |                     29,014 |               6,997 |           4,282 |                   0 |
| 2026-10-01     |                164,399 |                   54,401 |                     29,014 |               6,997 |           4,701 |                   0 |
| 2026-10-10     |                223,746 |                   68,795 |                     49,990 |               7,229 |          14,186 |               3,414 |
| 2026-10-19     |                243,607 |                   72,793 |                     59,617 |               8,174 |         108,111 |              92,142 |
| 2026-10-24     |                258,666 |                   79,534 |                     66,821 |               8,550 |         219,066 |             185,908 |
| 2026-10-26     |                285,653 |                   92,866 |                     78,004 |               8,550 |         220,464 |             185,908 |
| published-head |                431,278 |                  135,240 |                    145,206 |              34,895 |         223,255 |             187,197 |

## Проверенный universe

| Repository         | First visible commit                                                                                                                                | Published ancestors | All local visible commits | Shallow |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------: | ------------------------: | ------- |
| Root               | [1e10299e99f8](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/1e10299e99f8d9f73a5dc3d3b53141459091d1fa) · 2026-09-26T20:29:26+01:00           |                 312 |                       328 | false   |
| QCLNEGF.jl         | [92a217a31f2d](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/92a217a31f2d0cdec503cb8e9c162709d2a89fd8) · 2026-09-26T20:28:05+01:00         |                  41 |                        52 | false   |
| QCLNEGFRunner.jl   | [c924d07dfa32](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/c924d07dfa32949c72d390252a8cfd584668d6c9) · 2026-09-26T20:28:05+01:00   |                 104 |                       105 | false   |
| qcl-negf-contracts | [c7cd6670f008](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/c7cd6670f0086a4d57ff913807ef3f2ab4f10430) · 2026-09-26T20:28:05+01:00 |                  49 |                        59 | false   |
| qcl-negf-results   | [abf3d54950f1](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/abf3d54950f1acaea55c5f300458b128a26fbeb0) · 2026-09-26T20:28:05+01:00   |                  93 |                       100 | false   |
| qcl-negf-aiida     | [d5e793b57df8](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/d5e793b57df82af71cf6efcdfc9db3928b8f9a44) · 2026-09-26T20:28:05+01:00     |                  77 |                        83 | false   |
| qcl-negf-platform  | [66115da942ed](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/66115da942ed46e61fb60e95f33d9d9b5a8137bd) · 2026-09-26T20:28:05+01:00  |                 222 |                       234 | false   |
| qcl-negf-portal    | [dd7a28606311](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/dd7a28606311ee53f77931b2e82faac37324fdc8) · 2026-09-26T20:28:05+01:00    |                  80 |                        87 | false   |
| qcl-negf-research  | [f884750b7657](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/f884750b76570403f614a3b15afc7fb831b91d04) · 2026-09-26T20:28:05+01:00  |                  16 |                        22 | false   |

Full metadata universe:994 commits reachable from9 named published tips;1070 visible local commits
including76 outside those published ancestry sets. Outside includes side/private/evidence work and
does not automatically mean missing productionhistory. Nonshallow confirms no shallow boundary for
examined ancestry; does not prove every deleted remote branch or pre-Git source is available.

Semantic reading was targeted by decision/file history; this does not claim every line of every994
diff was reviewed. Commit metadata and tree contents prove code evolution, not original human
intent, runtime success or causal attribution of every hour. Root/committer names are not evidence
that the human personally wrote/approved each change.

## Exact snapshot refs

### Root

| Epoch          | Source commit                                                                                                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [1e10299e99f8d9f73a5dc3d3b53141459091d1fa](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/1e10299e99f8d9f73a5dc3d3b53141459091d1fa) |
| 2026-10-01     | [efb68778a9267cb11c6e9f49701ea2c247c35645](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/efb68778a9267cb11c6e9f49701ea2c247c35645) |
| 2026-10-10     | [3efa593973ede266b35bb2d9ee45ff1424772996](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/3efa593973ede266b35bb2d9ee45ff1424772996) |
| 2026-10-19     | [514cd9707a32cde60c630d60986973a898d35b18](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/514cd9707a32cde60c630d60986973a898d35b18) |
| 2026-10-24     | [46709f7a89f0d537c055b01af784f3210fc7e204](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/46709f7a89f0d537c055b01af784f3210fc7e204) |
| 2026-10-26     | [d395044ac09b28c2ff573724f8911d625df43bf5](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/d395044ac09b28c2ff573724f8911d625df43bf5) |
| published-head | [a29fe2fb19aba0bab216c520653627316f099cce](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/a29fe2fb19aba0bab216c520653627316f099cce) |

### QCLNEGF.jl

| Epoch          | Source commit                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [92a217a31f2d0cdec503cb8e9c162709d2a89fd8](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/92a217a31f2d0cdec503cb8e9c162709d2a89fd8) |
| 2026-10-01     | [4143ed54cecef7a858a6a372b624dfab11280df5](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/4143ed54cecef7a858a6a372b624dfab11280df5) |
| 2026-10-10     | [3108150dd1b6b1377470b384b15c26e272fe5c5d](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/3108150dd1b6b1377470b384b15c26e272fe5c5d) |
| 2026-10-19     | [e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee) |
| 2026-10-24     | [5b1cdd458eb07ff8c7c792642eda58d9061e1017](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/5b1cdd458eb07ff8c7c792642eda58d9061e1017) |
| 2026-10-26     | [0df7dd5a481c2c339e8520d2291c035253e7c0e2](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/0df7dd5a481c2c339e8520d2291c035253e7c0e2) |
| published-head | [01d472141a91c9429f43f7237460a17592d65845](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/commit/01d472141a91c9429f43f7237460a17592d65845) |

### QCLNEGFRunner.jl

| Epoch          | Source commit                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [c924d07dfa32949c72d390252a8cfd584668d6c9](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/c924d07dfa32949c72d390252a8cfd584668d6c9) |
| 2026-10-01     | [f21cbfc386d63bab89373aa98253ab074fbf9b46](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/f21cbfc386d63bab89373aa98253ab074fbf9b46) |
| 2026-10-10     | [0c53c6d0f68e0b25fce79388db831da6fc3ae856](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/0c53c6d0f68e0b25fce79388db831da6fc3ae856) |
| 2026-10-19     | [1acc165650fd4f4c2d49605cc679f90e3f6fcdae](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/1acc165650fd4f4c2d49605cc679f90e3f6fcdae) |
| 2026-10-24     | [f0e5950e6a4b4551aa54f039e9718042f34df8aa](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/f0e5950e6a4b4551aa54f039e9718042f34df8aa) |
| 2026-10-26     | [8264f48c01ccc524548036d4b3f44552a76f19b5](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/8264f48c01ccc524548036d4b3f44552a76f19b5) |
| published-head | [97ab889ff83b73d9fad5d34e278309b2efe3b299](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/97ab889ff83b73d9fad5d34e278309b2efe3b299) |

### qcl-negf-contracts

| Epoch          | Source commit                                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [c7cd6670f0086a4d57ff913807ef3f2ab4f10430](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/c7cd6670f0086a4d57ff913807ef3f2ab4f10430) |
| 2026-10-01     | [69abedd7429ea81e7a36a6cadc39702ab9d56def](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/69abedd7429ea81e7a36a6cadc39702ab9d56def) |
| 2026-10-10     | [e5c056c47fc3bde3e0ca32866692d740ef9b325c](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/e5c056c47fc3bde3e0ca32866692d740ef9b325c) |
| 2026-10-19     | [12fc26462bbab3df76904c6deb01f8c6596de7be](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/12fc26462bbab3df76904c6deb01f8c6596de7be) |
| 2026-10-24     | [f4009c933183d8537e289d2fa5fa898defd2d9b5](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/f4009c933183d8537e289d2fa5fa898defd2d9b5) |
| 2026-10-26     | [41209389109d387912b0410a5244dbc29ff1ff42](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/41209389109d387912b0410a5244dbc29ff1ff42) |
| published-head | [5eb0e61a9fc12fa2215291e47b7cd28888ce64cc](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc) |

### qcl-negf-results

| Epoch          | Source commit                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [abf3d54950f1acaea55c5f300458b128a26fbeb0](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/abf3d54950f1acaea55c5f300458b128a26fbeb0) |
| 2026-10-01     | [8fadceebe819e94b95310767f463c1b0f0ffc7b1](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/8fadceebe819e94b95310767f463c1b0f0ffc7b1) |
| 2026-10-10     | [fe27a2a9ed065f9afacecc84113311f30d0c68d6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/fe27a2a9ed065f9afacecc84113311f30d0c68d6) |
| 2026-10-19     | [de70638a982f91b7e125ab1cfc70a2daef2a656d](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/de70638a982f91b7e125ab1cfc70a2daef2a656d) |
| 2026-10-24     | [a0b426759959d9011a41e8d8812704774f950eda](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/a0b426759959d9011a41e8d8812704774f950eda) |
| 2026-10-26     | [f811d7c43bef8a70eb79ef74d554f08496a9af1c](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/f811d7c43bef8a70eb79ef74d554f08496a9af1c) |
| published-head | [10a32422b90a21ee728e73283217ac6b81bcf760](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/10a32422b90a21ee728e73283217ac6b81bcf760) |

### qcl-negf-aiida

| Epoch          | Source commit                                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [d5e793b57df82af71cf6efcdfc9db3928b8f9a44](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/d5e793b57df82af71cf6efcdfc9db3928b8f9a44) |
| 2026-10-01     | [4a81b93b35040d4cac4afda24cfebff22aa7fa8e](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/4a81b93b35040d4cac4afda24cfebff22aa7fa8e) |
| 2026-10-10     | [53e2a20544a469dd7ee5560243ebe530a6310f0a](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/53e2a20544a469dd7ee5560243ebe530a6310f0a) |
| 2026-10-19     | [d8f8092ca1c76523d85384b4bac8198d8bfa736b](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/d8f8092ca1c76523d85384b4bac8198d8bfa736b) |
| 2026-10-24     | [76013a453463c5f6663f9af7194769dc1a236885](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/76013a453463c5f6663f9af7194769dc1a236885) |
| 2026-10-26     | [7f4223eaff86b3a6104743098162ffa3fc4e0334](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/7f4223eaff86b3a6104743098162ffa3fc4e0334) |
| published-head | [336358dfd10c698e4b4a71d8c93562aaa8ee7182](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/336358dfd10c698e4b4a71d8c93562aaa8ee7182) |

### qcl-negf-platform

| Epoch          | Source commit                                                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [66115da942ed46e61fb60e95f33d9d9b5a8137bd](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/66115da942ed46e61fb60e95f33d9d9b5a8137bd) |
| 2026-10-01     | [f4766be33d3aa66a75bcb2c6354c334b23471380](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/f4766be33d3aa66a75bcb2c6354c334b23471380) |
| 2026-10-10     | [b365b706af304ed66c7107721742a90fd8153f86](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/b365b706af304ed66c7107721742a90fd8153f86) |
| 2026-10-19     | [f5bc368654414039f7368bb19ca3201fa7f29f9d](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/f5bc368654414039f7368bb19ca3201fa7f29f9d) |
| 2026-10-24     | [7c753b8a1c429394fd6602c069a41ae967a29557](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/7c753b8a1c429394fd6602c069a41ae967a29557) |
| 2026-10-26     | [1b1370d2b8e83a267a97c8d49df14db220123478](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/1b1370d2b8e83a267a97c8d49df14db220123478) |
| published-head | [c47097225a4a798e4124e30245c7b5b2063eb32a](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/c47097225a4a798e4124e30245c7b5b2063eb32a) |

### qcl-negf-portal

| Epoch          | Source commit                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| creation       | [dd7a28606311ee53f77931b2e82faac37324fdc8](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/dd7a28606311ee53f77931b2e82faac37324fdc8) |
| 2026-10-01     | [7c8b8408c49dc374b23d60e2d5eed85e2d840282](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/7c8b8408c49dc374b23d60e2d5eed85e2d840282) |
| 2026-10-10     | [36837e98a8d1f85820f2807d0212ec92e73c3c7b](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/36837e98a8d1f85820f2807d0212ec92e73c3c7b) |
| 2026-10-19     | [2622de5ee28b454ff4f809cc3dd00c1e5bc2295d](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/2622de5ee28b454ff4f809cc3dd00c1e5bc2295d) |
| 2026-10-24     | [c7fc4b1efa6015e130e8d47ceba71bdfc33ce791](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/c7fc4b1efa6015e130e8d47ceba71bdfc33ce791) |
| 2026-10-26     | [104481fdce8e11c9734b8b5b0f2743c9e5760151](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/104481fdce8e11c9734b8b5b0f2743c9e5760151) |
| published-head | [2c31e5fd597600ac632c292969c02dce0e50d020](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/commit/2c31e5fd597600ac632c292969c02dce0e50d020) |

### qcl-negf-research

| Epoch          | Source commit                                                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| creation       | [f884750b76570403f614a3b15afc7fb831b91d04](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/f884750b76570403f614a3b15afc7fb831b91d04) |
| 2026-10-01     | [32ffce94e18cd95f502b99772146b2019c42d396](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/32ffce94e18cd95f502b99772146b2019c42d396) |
| 2026-10-10     | [5458212063a41051328ef8b5d14d63d5ac7dc781](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/5458212063a41051328ef8b5d14d63d5ac7dc781) |
| 2026-10-19     | [3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731) |
| 2026-10-24     | [2d0e5326aecd3a17aaef610cf6c28982098eebc5](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/2d0e5326aecd3a17aaef610cf6c28982098eebc5) |
| 2026-10-26     | [408ca413a8df865110edfb480db2c8544452b8d0](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/408ca413a8df865110edfb480db2c8544452b8d0) |
| published-head | [46fb51fbd594be80127cf543c7160fc69d8e3b2d](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/commit/46fb51fbd594be80127cf543c7160fc69d8e3b2d) |
