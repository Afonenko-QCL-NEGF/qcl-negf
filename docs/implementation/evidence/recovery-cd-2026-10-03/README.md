# Сохранённые журналы локальной проверки

Это свидетельства конкретных проверок 2026-10-03, а не release graph, научные массивы или общий
статус приёмки. Некоторые regression runs перекрывают полные suites; их счётчики не суммируются.
Команды и ограничения приведены в [отчёте](../../recovery-cd-local-validation.md).

[Автоматически зафиксированный code state](local-code-state.txt) содержит HEAD, ветки, status и
submodule status до документационного handoff commit. Это provenance проверки, а не lock или
источник нового опубликованного состава.

| Журнал                                                                                       | Bytes | SHA-256                                                            |
| -------------------------------------------------------------------------------------------- | ----: | ------------------------------------------------------------------ |
| [python-final-reviewed.txt](python-final-reviewed.txt)                                       |   432 | `1299fdcc5e083bd9f8ee3afdfb30ba4f2b53cc55337944467e1cdf499133b2dc` |
| [aiida-review-full.txt](aiida-review-full.txt)                                               | 16799 | `12e1bf72fcf58363dc09709aadfdfe7dc264f36b8cca17ff815521f5d89ed397` |
| [platform-prefetch-full.txt](platform-prefetch-full.txt)                                     |  2185 | `75c719f2a313b6a87bffa48507b79208f9d652a249b44967d3f5d02c859e4656` |
| [umbrella-cache-final.txt](umbrella-cache-final.txt)                                         |  2080 | `ebea9670aab423ab6f4cadba18014fcd4a2ad89f861cf945a367b71327b85575` |
| [platform-nix-release-final.txt](platform-nix-release-final.txt)                             |   281 | `d9b22cd251999a4b6e1afd0bf13f5d3d47bd12823ef8ffc4cff06e76516c8842` |
| [platform-nix-monitoring.txt](platform-nix-monitoring.txt)                                   |   561 | `5ed4180c63fc72495d0d205a3e97a0bbcaeab443ff5488843e211911d3d505dc` |
| [platform-nix-munge-corrected.txt](platform-nix-munge-corrected.txt)                         |   150 | `30010f18654a33fd5ee7ca12790d3e65e193406ebe23900394464262b352a8d6` |
| [platform-powershell-final.txt](platform-powershell-final.txt)                               |    65 | `d02da13dd21b4ecd5959267314cdbc11bcc8adb5d071326491fdd835460d9749` |
| [core-independent-fixtures.txt](core-independent-fixtures.txt)                               |  1517 | `86b4f2db4cd70ede0016f36c91e2736c1e98f1a8f9295555bb1b85c77bbae64a` |
| [core-basis-pv.txt](core-basis-pv.txt)                                                       |   842 | `1155e0d160ac7c1b0e70c6398e57ce7d44b653a41b36e45dd3da2338a1178514` |
| [results-native-verified.txt](results-native-verified.txt)                                   |   110 | `8f5b825886fad52bb8d818398e190cb486581d193a1a1555bec5ccf72d23fbea` |
| [results-native-reviewed-reexport.txt](results-native-reviewed-reexport.txt)                 |   122 | `2d257a34d300a967a3fa23acda7486e0e722338444fd90510cf412516f102fce` |
| [wheel-smoke.txt](wheel-smoke.txt)                                                           |  1420 | `3415a0079ad84ea2ab3906b312c31c422c867b8687ecc91a299f9e92a448cc03` |
| [runner-bootstrap-path-green.txt](runner-bootstrap-path-green.txt)                           |   454 | `2970edff910ebe52bf76623007d7978e80ffdc69e3ae70382db678dc41bcef13` |
| [runner-telemetry-measure-final.txt](runner-telemetry-measure-final.txt)                     |   569 | `8bca26c49b606e5ecf625b9f403ddfd26c08c2bd4946e4960b662a10d01f9f8e` |
| [runner-telemetry-measure-final.resources.txt](runner-telemetry-measure-final.resources.txt) |   109 | `76bfb93bf858a166cf68f66c27596eed1d7f05cc463e6f4de9b609fdee319912` |
| [runner-docs-final-retry.txt](runner-docs-final-retry.txt)                                   |   989 | `6197c4ea8fbeb99e020a2a324c52cb1d70ce94b30fec52e9a5b4ca3066ed34ec` |
| [runner-pause-import-closure-green.txt](runner-pause-import-closure-green.txt)               |  1946 | `7fce13b55d53748c352702f64fad09cd1386fd5df340d061805763181aa7f905` |
| [runner-hdf5-storage-green.txt](runner-hdf5-storage-green.txt)                               |   756 | `2fa3a3ffa1855bf92d455fb12d5a1e008629158b19ebc8e7e275f5f8be8ef14b` |
| [runner-pause-cli-budget-green.txt](runner-pause-cli-budget-green.txt)                       |   351 | `cd91a277fc398fb7f4280024c8e8f130ea88da9532d897fa4cb7be2ee9ccc1d1` |
| [release-graph-guard.txt](release-graph-guard.txt)                                           |   132 | `b80f5590aae6f06d775a8ffdb16dbc65d3913e844b2eaad4abc1effcb13bfd13` |
| [runner-archive-preflight-green.txt](runner-archive-preflight-green.txt)                     |   788 | `dd211810d57d75dc09344e1fba4f4e1664d31c9fcf1813c344d018a23af04d97` |
| [runner-cli-barrier-logic.txt](runner-cli-barrier-logic.txt)                                 |   953 | `05cd8dc00e82eb0677638b615dd44ea8078f6842207729ded8dd87e632156de0` |
| [runner-hdf5-storage-lock-green.txt](runner-hdf5-storage-lock-green.txt)                     |   756 | `dc92094834a723c9fd24eaecb61e4895282bcd7364408463683698906b3ac2ca` |
| [cli-selfcheck-final.stdout.txt](cli-selfcheck-final.stdout.txt)                             |   471 | `cb978631f14af19ff158b90e2cf6d5c0940fdec8394294764424b9d5fa6cc48e` |
| [cli-selfcheck-final.stderr.txt](cli-selfcheck-final.stderr.txt)                             |   213 | `a594fb6b5dcb8ff0dbf779a1865cb1273493a4ed9373d9d5739336414ddf3900` |
| [runner-final-reviewed-all-v2.txt](runner-final-reviewed-all-v2.txt)                         | 13924 | `287c96bebb6ca160e3431054101a5b51547e4956bbd6a0106ae9ba7e955137bd` |
| [runner-final-reviewed-command.txt](runner-final-reviewed-command.txt)                       |   922 | `03e14acd3df798483ea56b04ca65d9f1ceeca2795d3f4997ad3a190c9f3fa624` |
| [runner-final-reviewed-completed-files.txt](runner-final-reviewed-completed-files.txt)       |  3278 | `c830d75bbf86903dbb4e27841ab67899e1fbed4b4811e7caa970335b83c78c87` |
| [runner-final-reviewed-tail-files.txt](runner-final-reviewed-tail-files.txt)                 |  1074 | `7de4a4a013d23e28c469f93b50ec2713859b96ef8446c8d9a31d24950a669fae` |
| [runner-final-reviewed-tail-harness.txt](runner-final-reviewed-tail-harness.txt)             |  4732 | `4626370043a129e705c54f5858cd22eacfa5419355df864afc697933bab4de26` |
| [runner-final-all.txt](runner-final-all.txt)                                                 | 32633 | `0738aa27c67b2c4fdb2f39b00920f32b51ee9c2631376b504083cce880110613` |
| [runner-final-reviewed-tail.txt](runner-final-reviewed-tail.txt)                             |  5863 | `c2dd4ce1ce81a36b46e4ccecc0a1a2a7e0295dcfb938ef8475990c2d5f5f7ac6` |
| [runner-final-reviewed-tail-command.txt](runner-final-reviewed-tail-command.txt)             |  1240 | `f87ee3928d91319a97f4948a92e83f4e3eb32fa24e3d8127f04c630a46c73a8a` |
| [runner-final-coverage.txt](runner-final-coverage.txt)                                       |   515 | `378489fef50081a7c9ea6ed6fa7d1815e69acbd8ba11dfdfcf2035d0a789bc30` |

У копии `runner-bootstrap-path-green.txt` удалена одна лишняя пустая строка в EOF для
`git diff --check`; содержательные строки сохранены. Таблица хеширует сохранённую копию. Исходный
raw log остаётся в `/tmp/qcl-implementation-tests/runner-bootstrap-path-green.log`, SHA-256
`97eaa6c14bfc496363b5e6c83fd61ed7c32dc30908b7ed57c2a4777a275a7e3d`.
