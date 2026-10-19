# RV11 blind source notes

Before candidate/fixes read. S=e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1; Runner J=0c53c6d0f68e0b25fce79388db831da6fc3ae856; Results U=fe27a2a9ed065f9afacecc84113311f30d0c68d6. N=7 source properties.

J `point_artifacts.jl::commit_point_artifacts`: stage raw/model/history→commit JSON→_prepare_generation!→rename generation→root directory sync→verify final commit/hash/budget→bundle receipt→previous pointer then current atomic pointer→prune only after publication. `_atomic_replace_file` single same-directory rename avoids delete gap but itself is not fsync wrapper. Scientific artifact publication uses separate sync helpers.

J `filesystem_repository.jl::save_runtime_checkpoint!` generic codec creates payload and immutable generation metadata; it returns reference, without writing a latest pointer in this function. This is orchestration state, not automatically scientific HDF5/restart identity. It must not inherit scientific publication fsync claims; read-only trace shows no sync helper in this function. Before-candidate correction: initial shorthand latest.yaml removed after exact function body read.

U `state.py::verify_recovery_bundle/StateReader` checks selected identity before payload; `_internal_storage` rejects non-hard HDF5 links, external datasets and virtual storage. J `_require_internal_hdf5_storage` similarly rejects links/layout/storage; hash-valid pointer to external bytes is insufficient ownership. Attempt equality is not process or convergence acceptance.

J `scratch_execution.jl::stage_result_tree` rejects output existence/source overlap, hashes trees before/after copy, verifies commits, syncs files/dirs, rename staged→destination then parent sync. It needs destination filesystem connectivity/worker survival; killed worker cannot promise final copy. Failed staging does not delete source raw tree. Selected fault catalogue: partial write/metadata publication/ENOSPC/invalid identity/external HDF5/NFS loss/worker loss. Existing fixture assertions model only subsets; native durability/NFS/worker loss and RPO/RTO not_measured.

Independent oracle: manipulate one byte/attempt/external dependency with valid outer digest then require reader refusal; inject stage copy/publish failure and retain source arrays/prior pointer. No source blocking defect independently established; generic runtime sync distinction requires honest documentation/measurement.
