# RV13 blind-first primary answer

Candidate/fixes не читались. Source S/overlay receipt; Platform P=4ce214e29b72276157b10a9267e2f30fef4ac66f clean. Frozen denominator A1–A7 N=7, role erratum сохранён: site-preflight roles storage/control/compute/ci; local-lab machines control/storage/worker-1/worker-2. Native cells not_measured.

A1: modules/storage/state-archive и site-preflight отделяют mutable mounted state/NFS datasets от image/Nix closure; controller/worker — service role vocabulary, cache не отдельная selected image. OS rollback не DB rollback.

A2: state_archive::main create требует root/writers-paused, core.psql_dos profile, local socket database/user/empty password и exact repository URI, DB physical size; stop_services останавливает API/daemon и empty-queue Slurm перед pg_dump/pack. writers-paused — декларация operator, не техническое исключение всех внешних writers. Один bundle/hash не доказывает semantic DB↔repository generation consistency; generation/UUID/object verification обязательны после restore.

A3: admission запрещает overwrite, staging внутри sources, лишний retention и недостаток budget/free space; source_files запрещает symlink/nonregular entries. verify сверяет archive sidecar/member set/file hashes+sizes, rejects duplicates/traversal/links. Это integrity, не authenticity; trusted sidecar и external copy нужны отдельно. sidecar publication crash не successful backup.

A4: restore до stop/pg_restore проверяет paths/database/PG major/empty targets, dedicated data filesystem/WAL/tablespaces, grouped st_dev allocations с DB reserve. Shared AiiDA+Slurm filesystem не запрещён сам по себе: allocations суммируются. PG single transaction не делает file-copy atomic; DB success/file-copy failure оставляет offline nonempty partial targets, следующий blind retry запрещён. Tool не содержит самостоятельного semantic generation oracle.

A5: test_complete_local_state_archive_verifies_and_restores_exact_fixture_bytes извлекает synthetic dump bytes; patched subprocess/query/stop_services не live PostgreSQL/service restore. Native restore/cold/reinstall/UUID continuity not_measured.

A6: tofu persistent dataset prevent_destroy/external disks и host-storage исключения foreign/shared objects задают desired ownership, не proof live disk topology/target authorization. Не применять import/destroy/replace без private inventory/admission.

A7: incident→offline→verification→startup timeline обязан содержать exact source, archive hash, profile/DB/object identity, dataset/device mappings, role/backend, operation bounds, original failure/restore receipts и secret references без secret bytes. Сейчас нет timestamps native incident/recovery или measured RTO; public source conclusions возможны без secrets, operation live gate остаётся blocked при missing site data.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Snapshot координируется остановкой known writers | P state_archive::main/stop_services | External writers operator prerequisite | сохранить |
| Byte hashes не semantic generation oracle | P pack/verify/restore | UUID/object checks external | дополнительно измерить |
| Admission предшествует destructive restore | P restore_admission/main | Quota/WAL growth не гарантированы | сохранить |
| Fake bytes tests не live restore | P test_state_archive.py::test_complete_local_state_archive_verifies_and_restores_exact_fixture_bytes | M09–11 native unknown | данных недостаточно |
