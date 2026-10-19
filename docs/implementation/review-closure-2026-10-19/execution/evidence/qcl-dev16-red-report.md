# DEV16 frozen RED request

Runner branch `codex/review-closure-schema-provenance`, base0c53c6d0f68e0b25fce79388db831da6fc3ae856. Production/source/schema untouched. Only two permitted test files differ.

Frozen diff `/tmp/qcl-dev16-red.diff` SHA256 ab39c80b0d583d10411e5fd6c4024c28a680935986fb1876817c33ca7430e00c.
New schema suite SHA256 d81fd3f2663727d0b8647ac52d747c2e64f54d52231aaa3c57096bde8c219b7a.
Merge suite SHA256 09fa7cccc6ec8c701cf86135ce6d50c5ca1881323d8b91e9729846b75f8e9cbb.
`git diff --check` passed; Julia not invoked by writer.

Request coordinator's source-bound bounded RED: include schema suite only, `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/contracts/schema_copy_provenance.jl")'`, existing prepared depot, BLAS1, <=120s/1CPU/2GiB. Expected semantic failure: `@test available` because QCLNEGFRunner has no shared QCLSchemaProvenance verifier; no behavior/source writes until explicit coordinator RED release. The other cases are syntactically loaded but guarded until implementation; no missing-method errors are counted as RED. GREEN request will include both permitted files in one invocation if coordinator rebinds remaining packet accordingly.

Read-only YAML0.4.17 checkpoint actual realpath `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/.build/local-julia-int01/depot-1/packages/YAML/M5j6t/src/YAML.jl`; SHA256 24f6e5c7475945658b3bf8625cacaa7c2443726547e0679acd86ff4584d936cb; String load→IOBuffer lines142–143. Constructor SHA2564650446782dcdbe53928affe5dd183d0d0643bb07a04bf7ef4d7c6664d0e8f07; lines183–206 confirm merge flatten bypasses duplicate check. Fixture metadata includes actual valid hashes plus merge and duplicate source, so simple strict_unique_keys alone cannot pass this control. Custom schema merge remains a positive compatibility control.

| утверждение | свидетельство | ограничение | решение |
| --- | --- | --- | --- |
| RED готов к запуску | Frozen diff и два test hashes | Runtime ещё не выполнен | дополнительно измерить |
| Source/schema не изменены | Runner status показывает только два test paths | Git branch локальная | сохранить |
| In-memory YAML API известен | Owning0.4.17 source path+hash | Не runtime proof | сохранить |
