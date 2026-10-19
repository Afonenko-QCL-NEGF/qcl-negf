# RV13 independent review

Blind primary answer RV13-blind.md сохранён до чтения candidate/fix. Candidate SHA256 `7cd73a8461ed02b54aa1c8fecc71c2ae4b9be23c137b00d7072e5bf4754aa2b1`; Source Platform P=4ce214e29b72276157b10a9267e2f30fef4ac66f, root S/overlay receipt. Frozen A1–A7 N=7 и explicit role erratum совпадают. Native restore/tests/import/eval/server не исполнялись.

Report-quality verdict: **сохранить**. Blocking report findings нет. Candidate source conclusions подтверждены: create binding по profile/database/repository URI; all-writer pause остаётся declared prerequisite; archive integrity не semantic generation consistency; restore_admission precedes mutation; PG commit и subsequent copytree не атомарны. Важное negative об общем filesystem описано правильно: shared AiiDA/Slurm state filesystem разрешён, storage allocations суммируются st_dev, недостаточный combined space отвергается до stop. Wrong generation под correct URI/valid hashes не объявлен автоматически обнаруживаемым.

Источник fake evidence прочитан независимо: exact-byte test не вызывает main restore/pg_restore; query, stop_services и dump подменяются в остальных budget/create cases. Candidate не повышает эти properties до native PostgreSQL/AiiDA/Slurm acceptance. M04 source negatives не measured pass, M09 incident/recovered timeline/RPO/RTO not_measured, M10 private drift unknown, M11 role/backend/scenario cells partial/not_measured. Four roles storage/control/compute/ci отделены от local-lab machines control/storage/worker-1/worker-2. Persisted provider protections не объявлены universal safety guarantee.

Source-risk disposition: без semantic DB/repository checks и independently verified medium recovery evidence недостаточно; priority не превращается в дефект отчёта. Existing proposal RV13-01 надлежащим образом требует evidence design/isolated rehearsal вместо destructive cleanup. Smallest report fix не требуется. В будущем generation mismatch fixture должен показать отказ startup/storage verification, а не приписывать structural verify несущестующий semantic oracle.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Coordinated boundary условна all-writer pause | P state_archive.main/stop_services; A2 | External writers не исключены | сохранить |
| DB/file failure оставляет partial offline target | P pg_restore/copytree; A4 | Live actual service state unmeasured | дополнительно измерить |
| Native restore не наследует byte-fixture pass | P test_state_archive named fixture; A5 | Никакие tests не исполнялись | сохранить |
| Report N=7/negative/invariant/M09–11 корректен | Candidate hash выше; blind A1–A7 | Partial catalogue | сохранить |
