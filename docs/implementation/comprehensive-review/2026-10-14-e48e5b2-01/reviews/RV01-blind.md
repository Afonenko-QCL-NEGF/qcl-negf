# RV01 · Blind primary metadata check

Первичные inputs читались до RV01 candidate. Sizes до чтения: 51 840 + 46 353 + 7 978 + 43 521 + 1 444 = 151 136 bytes, ниже 256 KiB. Один проход read_bytes + SHA256 + JSON parse; numerical payloads/archives не открывались. Sanitized selection ниже, credentials/paths инфраструктуры не выводятся.

- `canonical-update-ROOT-recovery-attempt4/ROOT-result.original.json` SHA256 `4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3`; root keys `failure`, `one_update_transport`, `native_owned_closure`, `actor_closed`, `outcome_unknown`, `retained_raw_bytes`, `capture_bytes_upper`, `originals`, `owning_gate_Code_fleet_acceptance_required_separately`, `scientific_accepted`, `full_release_CI_accepted`, `retry_performed`.
- `freeze600-ROOT-recovery-attempt1/owning-plan.native-original.json` SHA256 `4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9`; root keys `fingerprint`, `executions`, `name`, `points`, `resources`, `root_kind`, `root_definition_id`, `campaign`, `maximum_solver_runs`, `inclusions`, `science_archive_preflight`, `nodes`, `scientific_fingerprint`, `schema`, `model_revision`, `computation_count`.
- `S01-memory-status60-ROOT-attempt2/early-status-derived.json` SHA256 `d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90`; root keys `RUN_UUID`, `owning_profile`, `workflow`, `descendants`, `reports`, `CalcJob`, `Slurm`, `log_tails`, `binding_state`, `scientific_accepted`, `final_HDF5_assumed`, `observer_started`, `submit_performed`.
- `S01-memory-status60-ROOT-attempt2/control.transport.native-original.json` SHA256 `1f8762528996ce904f181a721f0f463d3b33f2c4d66fb7ebf2634aae41b848cb`; root keys `argv`, `exit_code`, `failure`, `stdout_base64`, `stderr_base64`, `output_truncated`, `local_before_epoch`, `local_after_epoch`, `native_closed_inferred_from_transport`.
- `S01-submit-ROOT-recovery-attempt1/installed-submit-stdout.original.bin` SHA256 `bd40aaae80a2a5e9816555fa1a340a8253014428e8ddf99040b0cea50ed4b976`; root keys `submitted`, `submitted_UUID`, `scientific_accepted`, `automatic_retry`, `owning_summary`, `manager_original`, `input_PLAN_sha256`, `native_load_original_receipt`, `native_load_original_receipt_sha256`, `Slurm_job_ID`, `input_provenance_verified`, `fingerprint`, `scientific_fingerprint`, `physical_comparable_fingerprint`, `automatic_solver_retries`.

## Receipt five-pointer denominator

- `/native_owned_closure/runtime/ready` = `True`.
- `/native_owned_closure/gate/open` = `True`.
- `/native_owned_closure/delivery_report/status` = `completed`.
- `/scientific_accepted` = `False`.
- `/full_release_CI_accepted` = `False`.

## Независимый предварительный вывод

Технический receipt должен интерпретироваться отдельно от solver convergence, physics, discretization и experiment. RUNNING является saved observation, не live state. Exact root S не означает совпадение installed/imported release; frozen native plan и submission identity требуют отдельных pointers. Первичных HDF5 matrices/axes/weights/final receipts в этих пяти metadata files нет: численная acceptance не восстанавливается из технического completion. Экспорт/части нельзя считать полными по одному receipt без declared part inventory.

## Identity selections

```json
{
  "status/RUN_UUID": "dfb75b38-6019-4861-b868-f51648c71f02",
  "status/workflow": {
    "uuid": "dfb75b38-6019-4861-b868-f51648c71f02",
    "pk": 11,
    "process_state": "waiting",
    "process_status": "Waiting for child processes: 16",
    "exit_status": null
  },
  "status/CalcJob": {
    "uuid": "bb7b9d59-863f-440e-b687-b83ac596f9bb",
    "pk": 18,
    "process_state": "waiting",
    "process_status": "Monitoring scheduler: job state RUNNING",
    "exit_status": null,
    "attempt": 1,
    "execution_id": "execution-1"
  },
  "status/Slurm": {},
  "status/final_HDF5_assumed": false,
  "status/binding_state": "scheduler_job_ID_available",
  "plan/model_revision": "transport-contract-v2",
  "plan/computation_count": 1,
  "submit/submitted_UUID": "dfb75b38-6019-4861-b868-f51648c71f02",
  "submit/Slurm_job_ID": null,
  "submit/native_load_original_receipt": "/home/tolya/Загрузки/qcl-negf/.build/server-resume-20261012-recovery/owning-load600-ROOT-recovery-attempt1/caller-output/stdout.original.bin"
}
```

Original byte I/O total после selections: 250 432 bytes (<256 KiB). Transport stdout decoded only in memory; source archive untouched.
