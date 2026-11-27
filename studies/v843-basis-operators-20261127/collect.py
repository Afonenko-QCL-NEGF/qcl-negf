#!/usr/bin/env python3
"""Collect a completed V843 diagnostic DAG on its submit node."""

import argparse
from collections import defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

ROOTS = {
    "B7": ("B7",),
    "B9": ("B9",),
    "B11": ("B11",),
    "BLOCH": ("BLOCH144", "BLOCH288"),
    "IMP17": ("IMP17",),
    "IMP33": ("IMP33",),
    "LO": ("LO17", "LO33"),
    "SHIFT": ("SHIFT",),
}
TRANSPORT = {"T17A32": (17, 32), "T17A128": (17, 128),
             "T33A32": (33, 32), "T33A128": (33, 128)}
RESULT_NAMES = tuple(n for group in ROOTS.values() for n in group) + ("SELECT", "PILOT", *TRANSPORT)
RESIDUALS = ("r_K", "r_Σ", "r_λ")
ROW_FIELDS = ("ν", "J_A_cm2", *RESIDUALS)
FIXED = ("field_kV_cm", "voltage_mV_per_period", "temperature_K", "hartree",
         "method", "spatial_nodes", "energy_nodes", "energy_min_meV", "energy_max_meV",
         "energy_trust_margin_meV", "basis_states", "basis_periods", "basis",
         "qz_nodes", "k_max_nm_inverse", "qz_max_nm_inverse", "seed_eta_meV",
         "embedding_periods", "alpha_sigma", "channels", "light",
         "electron_electron_collisions", "screening", "ifr_correlation", "cold_start",
         "driver_sha256", "device_sha256", "manifest_sha256")
DIGEST = re.compile(r"[0-9a-f]{64}")
REVISION = re.compile(r"[0-9a-f]{40,64}")
WORKER = re.compile(r"qcl-win-[1-6]|linux-[0-9]+")
PRIVATE = re.compile(
    r"(?i)(?:\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:ghp_|github_pat_|ghs_|gho_|ghu_|ghr_)[A-Za-z0-9_]+"
    r"|-----BEGIN [^-]+PRIVATE KEY-----|\b[A-Z]:[\\/][^\s`'\";]*"
    r"|(?<![A-Za-z0-9:])/(?:home|srv|tmp|var|mnt|opt|root|run|Users)/[^\s`'\";]*"
    r"|\bDESKTOP-[A-Za-z0-9-]+\b|\bqcl-condor\b|\bdell\b)"
)
PRIVATE_KEYS = re.compile(
    r"(?i)^(?:hostname|host_name|machine|remote_host|address|ip_address|password|token|key|"
    r"private_key|secret|credential|username|user_name|worker_id|worker|scratch_directory|working_directory)$"
)
FORECAST = {
    "B7": "Повторить максимум 0,162285 на семи модах и локализовать худшую пару.",
    "B9": "При влиянии границ центральные ошибки уменьшатся относительно B7.",
    "B11": "Перемены от расширения окна должны сохранять роли уровней и подпространства.",
    "BLOCH": "Уточнить минимальный прямой зазор между полосами 7 и 8 и проверить устойчивость по фазе и сетке.",
    "IMP17": "Проверить, сохраняется ли ошибка углов после взвешенного действия примесного оператора.",
    "IMP33": "Сопоставить ошибки K33 и K17 на общих исходящих кольцах и во всём действии.",
    "LO": "Разделить ошибку углов и продольной сетки относительно точного углового среднего.",
    "SHIFT": "Для конечных объёмов ожидается взвешенная сопряжённость в пределах округления.",
    "SELECT": "Выбрать минимальный подтверждённый ранг только после статической и литературной сверок.",
    "PILOT": "Одна завершённая карта даёт конечные наблюдаемые и ещё не устанавливает стационарность.",
    **{name: "Сопоставить независимые холодные траектории на зафиксированном базисе." for name in TRANSPORT},
}


def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def clean(value):
    """Only public values survive. Non-finite numeric results stay visibly absent."""
    if isinstance(value, dict):
        return {
            key: clean(item) for key, item in value.items()
            if not PRIVATE.search(key) and (
                not PRIVATE_KEYS.fullmatch(key) or (
                    key.lower() in {"worker", "worker_id"} and isinstance(item, str) and WORKER.fullmatch(item)
                )
            )
        }
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, str):
        return PRIVATE.sub("[скрыто]", value)
    if type(value) is float and not math.isfinite(value):
        return None
    if value is None or type(value) in (str, bool, int, float):
        return value
    return str(value)


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".collect-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def number(value):
    return value if type(value) in (int, float) and math.isfinite(value) else None


def nonnegative(value):
    value = number(value)
    return value if value is not None and value >= 0 else None


def delta_or_none(end, start):
    end, start = number(end), number(start)
    return end - start if end is not None and start is not None and end >= start else None


def read_case(run, name):
    path = run / "results" / f"{name}.toml"
    if not path.is_file() or path.is_symlink():
        return {"status": "missing", "reason": "файл результата отсутствует"}, None, None
    raw = path.read_bytes()
    receipt = {"source_sha256": sha(raw)}
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError):
        return {**receipt, "status": "technical_failure", "reason": "некорректный TOML"}, None, None
    status = data.get("status")
    if not isinstance(status, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", status):
        status = "technical_failure"
        reason = "в результате отсутствует допустимый статус"
    else:
        reason = data.get("reason", data.get("error"))
    receipt["status"] = status
    if reason is not None:
        receipt["reason"] = clean(reason)
    sanitized = clean(data)
    if PRIVATE.search(raw.decode("utf-8")) or sanitized != data:
        return receipt, data, (f"results/{name}.json", json_bytes(sanitized))
    return receipt, data, (f"results/{name}.toml", raw)


def inventory(raw):
    """Map private execute identities onto stable publication labels."""
    if isinstance(raw, dict):
        raw = raw.get("workers", raw.get("slots", raw))
    if isinstance(raw, dict):
        raw = [{"id": key, **value} for key, value in raw.items() if isinstance(value, dict)]
    if not isinstance(raw, list):
        return {}, {}
    public, names = {}, defaultdict(set)
    linux = 0
    for row in raw:
        if not isinstance(row, dict):
            continue
        def value(*keys):
            return next((row[key] for key in keys if row.get(key) not in (None, "", "undefined")), None)

        name = value("id", "worker_id", "worker", "QCLWorkerId", "qcl_worker_id", "name", "Name")
        machine = value("machine", "Machine", "hostname")
        os_name = str(value("os", "op_sys", "OpSys", "platform")).upper()
        if isinstance(name, str) and WORKER.fullmatch(name):
            label = name
        elif os_name == "LINUX" or name in {"qcl-condor", "dell"} or machine in {"qcl-condor", "dell"}:
            linux += 1
            label = f"linux-{linux}"
        else:
            continue
        for key in (name, machine, value("name", "Name", "slot"), label):
            if isinstance(key, str):
                names[key.lower()].add(label)
                names[key.rsplit("@", 1)[-1].lower()].add(label)
        public[label] = {
            "platform": os_name.lower() if os_name in {"WINDOWS", "LINUX"} else None,
            "available_cpus": nonnegative(value("cpus", "total_cpus", "Cpus", "TotalSlotCpus")),
            "available_memory_mib": nonnegative(value("memory_mib", "memory", "Memory", "TotalSlotMemory")),
        }
    return public, {key: next(iter(labels)) for key, labels in names.items() if len(labels) == 1}


def label_for(ad, names):
    for key in ("MachineAttrQCLWorkerId0", "MachineAttrName0", "LastRemoteHost",
                "RemoteHost", "MachineAttrMachine0"):
        value = ad.get(key)
        if isinstance(value, str):
            for token in (value.lower(), value.rsplit("@", 1)[-1].lower()):
                if token in names:
                    return names[token]
                if WORKER.fullmatch(token):
                    return token
    return None


def history_for(dag_id, fixture):
    if fixture is not None:
        ads = load_json(fixture, [])
    elif isinstance(dag_id, str) and re.fullmatch(r"\d+(?:\.0)?", dag_id):
        cluster = dag_id.split(".", 1)[0]
        try:
            proc = subprocess.run(
                ["condor_history", "-json", "-constraint", f"DAGManJobId == {cluster}"],
                capture_output=True, check=True, text=True, timeout=30,
            )
            ads = json.loads(proc.stdout)
        except (OSError, ValueError, subprocess.SubprocessError):
            return [], "htcondor_history_unavailable"
    else:
        return [], "dagman_id_unavailable"
    if not isinstance(ads, list) or not all(isinstance(ad, dict) for ad in ads):
        raise ValueError("history JSON must be a list of ClassAds")
    return ads, "read" if ads else "history_empty"


def accounting(ads, raw_results, hosts, names):
    jobs = []
    for ad in ads:
        # Keep the latest scheduler terminal record for each job and exclude local collector work.
        task = next((ad.get(k) for k in ("QCLStage", "QCLArm", "QCLTask", "DAGNodeName")
                     if ad.get(k) in RESULT_NAMES), None)
        if task is None or ad.get("JobUniverse") == 12:
            continue
        runtime = raw_results.get(task, {}) or {}
        telemetry = runtime.get("runtime", {})
        if not isinstance(telemetry, dict):
            telemetry = {}
        def observed(key):
            return nonnegative(telemetry.get(key, runtime.get(key)))

        node = label_for(ad, names)
        starts = ad.get("NumJobStarts", ad.get("NumShadowStarts"))
        evictions = nonnegative(ad.get("NumJobVacates", ad.get("NumVacates", ad.get("NumShadowExceptions"))))
        # Job-wide CPU can be assigned to a node only for a single attested execution.
        single = starts == 1 and (evictions is None or evictions == 0)
        allocated = next((value for value in (nonnegative(ad.get("CpusProvisioned")),
                                               nonnegative(ad.get("MachineAttrCpus0")),
                                               observed("allocated_cpus"))
                          if value is not None and value > 0), None)
        request = nonnegative(ad.get("RequestCpus"))
        run_s = nonnegative(ad.get("RemoteWallClockTime"))
        ucpu = nonnegative(ad.get("RemoteUserCpu"))
        scpu = nonnegative(ad.get("RemoteSysCpu"))
        cpu_s = ucpu + scpu if ucpu is not None and scpu is not None else None
        queue_s = nonnegative(ad.get("InitialWaitDuration"))
        if queue_s is None:
            queue_s = delta_or_none(ad.get("JobStartDate"), ad.get("QDate"))
        native_execution_s = nonnegative(ad.get("ActivationExecutionDuration"))
        setup_s = nonnegative(ad.get("ActivationSetupDuration"))
        teardown_s = nonnegative(ad.get("ActivationTeardownDuration"))
        transfer = [nonnegative(ad.get(key)) for key in ("InputTransferDuration", "OutputTransferDuration")]
        file_s = sum(transfer) if all(value is not None for value in transfer) else observed("file_transfer_seconds")
        slot_s = allocated * run_s if allocated and run_s is not None and single else None
        active_s = allocated * native_execution_s if allocated and native_execution_s and single else None
        cluster, proc = ad.get("ClusterId"), ad.get("ProcId")
        job_id = f"{cluster}.{proc}" if type(cluster) is int and type(proc) is int else None
        jobs.append({
            "task": task, "job_id": job_id, "worker": node,
            "platform": hosts.get(node, {}).get("platform"),
            "requested_cpus": request, "allocated_cpus": allocated,
            "observed_julia_threads": observed("julia_threads"),
            "observed_blas_threads": observed("blas_threads"),
            "native_job_status": ad.get("JobStatus") if type(ad.get("JobStatus")) is int else None,
            "exit_code": ad.get("ExitCode") if type(ad.get("ExitCode")) is int else None,
            "execution_starts": starts if type(starts) is int else None,
            "possible_evictions": evictions,
            "queue_wait_s": queue_s,
            "allocated_wall_s": run_s,
            "execution_s": native_execution_s if single else None,
            "execution_plus_teardown_s": delta_or_none(ad.get("CompletionDate"), ad.get("JobCurrentStartExecutingDate")) if single else None,
            "cpu_s": cpu_s, "allocated_cpu_s": slot_s, "execution_cpu_budget_s": active_s,
            "cpu_attributed_to_worker": bool(single and node and cpu_s is not None),
            "peak_memory_mib": nonnegative(ad.get("MemoryUsage")),
            "resident_set_kib": nonnegative(ad.get("ResidentSetSize")),
            "setup_s": setup_s,
            "teardown_s": teardown_s,
            "wrapper_setup_s": observed("setup_seconds"),
            "file_transfer_s": file_s,
        })
    # Sequential node attempts can share a DAG node name but never the same ClusterId.ProcId.
    seen, terminal = set(), []
    for job in jobs:
        if job["job_id"] is None or job["job_id"] not in seen:
            terminal.append(job)
        seen.add(job["job_id"])
    grouped = defaultdict(list)
    for job in terminal:
        if job["worker"] is not None:
            grouped[job["worker"]].append(job)
    by_node = {}
    for node in sorted(set(hosts) | set(grouped)):
        rows = grouped[node]
        measured = [job for job in rows if job["cpu_attributed_to_worker"]]
        paired = [job for job in measured if job["allocated_cpu_s"] is not None]
        cpu_s = sum(job["cpu_s"] for job in measured)
        slot_s = sum(job["allocated_cpu_s"] for job in paired)
        paired_cpu_s = sum(job["cpu_s"] for job in paired)
        executing = [job for job in measured if job["execution_cpu_budget_s"]]
        execution_ratio = (sum(job["cpu_s"] for job in executing) /
                           sum(job["execution_cpu_budget_s"] for job in executing)) if executing else None
        allocations = sorted({job["allocated_cpus"] for job in rows if job["allocated_cpus"] is not None})
        utilization = paired_cpu_s / slot_s if slot_s > 0 else None
        reasons = []
        if not rows:
            reasons.append("В истории кампании нет назначения этому узлу. Причина отсутствия назначения не измерена.")
        if len(measured) != len(rows):
            reasons.append("Часть CPU-секунд нельзя привязать к узлу из-за повторных запусков или неполной телеметрии.")
        if len(paired) != len(measured):
            reasons.append("Для части измерений не подтверждено выделение CPU или время слота.")
        if any(job["queue_wait_s"] for job in rows):
            reasons.append("Для некоторых заданий измерено ожидание очереди.")
        if any(job["possible_evictions"] or (job["execution_starts"] or 0) > 1 for job in rows):
            reasons.append("В истории есть вытеснение или повторное начало исполнения.")
        if any(job["setup_s"] or job["wrapper_setup_s"] for job in rows):
            reasons.append("Для части заданий измерено время подготовки окружения.")
        if any(job["file_transfer_s"] for job in rows):
            reasons.append("Для части заданий измерено время передачи файлов.")
        if utilization is not None and utilization < 0.9:
            reasons.append("Учтена неполная загрузка выделенного времени CPU. Разбиение по фазам отсутствует.")
        by_node[node] = {
            **hosts.get(node, {}), "native_jobs": len(rows),
            "allocated_cpus_observed": allocations,
            "cpu_hours": cpu_s / 3600 if measured else None,
            "allocated_cpu_hours_with_measured_use": slot_s / 3600 if paired else None,
            "utilization_measured_subset": utilization,
            "execution_utilization_measured_subset": execution_ratio,
            "execution_utilization_jobs_attributed": len(executing),
            "cpu_jobs_attributed": len(measured),
            "utilization_jobs_attributed": len(paired),
            "observed_reasons_or_limitations": reasons,
        }
    return {
        "definition": ("CPU-часы = (RemoteUserCpu + RemoteSysCpu) / 3600. "
                       "Доля выделения = CPU-секунды / (CPU × RemoteWallClockTime). "
                       "Доля исполнения использует ActivationExecutionDuration при наличии. "
                       "Для узла учитываются атрибутируемые однократные исполнения. "
                       "Подготовка, вычисление, передача и ожидание различаются только при наличии соответствующего измерения."),
        "nodes": by_node, "jobs": terminal,
        "jobs_without_worker_identity": sum(job["worker"] is None for job in terminal),
    }


def transport_result(raw, name):
    raw = raw or {}
    reasons = []
    rings, angles = TRANSPORT[name]
    variation_matches = (number(raw.get("field_kV_cm")), raw.get("radial_nodes"), raw.get("angular_nodes")) == (21, rings, angles)
    if not variation_matches:
        reasons.append("не совпали параметры варианта")
    if raw.get("status") != "measured" or raw.get("scba_converged") is not True:
        reasons.append("строгая сходимость native SCBA не подтверждена")
    rows = raw.get("iterations")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        rows = []
    tail = rows[-8:]
    last = raw.get("last_iteration")
    terminal = {}
    if tail and isinstance(last, dict) and all(key in last and last[key] == tail[-1].get(key) for key in ROW_FIELDS):
        terminal = {key: tail[-1][key] for key in ROW_FIELDS if number(tail[-1][key]) is not None}
    if not all(nonnegative(terminal.get(key)) is not None and terminal[key] <= 1e-8 for key in RESIDUALS):
        reasons.append("терминальные невязки отсутствуют или выше 10⁻⁸")
    indices = [row.get("ν") for row in tail]
    usable_tail = (
        len(tail) == 8 and all(type(i) is int for i in indices)
        and all(b == a + 1 for a, b in zip(indices, indices[1:]))
        and all(number(row.get("J_A_cm2")) is not None for row in tail)
        and all(nonnegative(row.get(key)) is not None for row in tail for key in RESIDUALS)
    )
    currents = [row["J_A_cm2"] for row in tail] if usable_tail else []
    drift = max(currents) - min(currents) if currents else None
    if drift is None:
        reasons.append("нет восьми последовательных конечных наблюдений")

    fixed = {key: raw.get(key) for key in FIXED}
    for package in ("core", "runner"):
        package_identity = raw.get(package)
        fixed[f"{package}_source_tree_sha256"] = (
            package_identity.get("source_tree_sha256") if isinstance(package_identity, dict) else None)
    identity_known = all(value is not None for value in fixed.values()) and all(
        isinstance(value, str) and DIGEST.fullmatch(value) for key, value in fixed.items() if key.endswith("_sha256")
    )
    if not identity_known:
        reasons.append("неполная идентичность источника или физических параметров")
    z, density = raw.get("density_z_nm"), raw.get("density_z_cm_minus_3")
    profile = None
    if (isinstance(z, list) and isinstance(density, list) and len(z) == len(density) and z
            and all(number(x) is not None for x in z + density)):
        profile = (z, density)
    return {
        "qualified": not reasons,
        "identity_known": identity_known,
        "variation_matches": variation_matches,
        "reasons": reasons,
        "J_A_cm2": terminal.get("J_A_cm2"),
        "last8_range_A_cm2": drift,
        "terminal": terminal,
        "density": profile,
        "fixed": fixed,
    }



def compare_basis(results):
    """Compare equal-rank projected functions only on the same recorded coordinate grid."""
    window_rows = {}
    for window in ("B7", "B9", "B11"):
        candidates = (results.get(window) or {}).get("candidates", [])
        window_rows[window] = {row["rank"]: row for row in candidates if isinstance(row, dict)
                               and type(row.get("rank")) is int and row["rank"] > 0}
    differences = []
    for a, b in (("B7", "B9"), ("B9", "B11"), ("B7", "B11")):
        earlier, later = window_rows[a], window_rows[b]
        for rank in sorted(earlier.keys() & later.keys()):
            left, right = earlier[rank], later[rank]
            changes = {}
            for key in ("translation", "translation_nearest", "translation_two_pairs", "edge_pairs_translation"):
                old, new = number(left.get(key)), number(right.get(key))
                changes[key] = new - old if old is not None and new is not None else None
            row = {"windows": [a, b], "rank": rank, "later_minus_earlier": changes}
            axis = left.get("x_nm")
            wave_a, wave_b = left.get("wavefunctions"), right.get("wavefunctions")
            if (isinstance(axis, list) and axis and axis == right.get("x_nm")
                    and isinstance(wave_a, list) and isinstance(wave_b, list)
                    and len(wave_a) == len(wave_b) == rank
                    and all(isinstance(mode, list) and len(mode) == len(axis)
                            and all(number(v) is not None for v in mode) for mode in wave_a + wave_b)):
                overlap = [[math.fsum(x * y for x, y in zip(phi, chi)) for chi in wave_b] for phi in wave_a]
                trace = math.fsum(val * val for mode in overlap for val in mode)
                row["overlap"] = overlap
                row["projector_overlap_trace"] = trace
                row["projector_distance_over_sqrt_2rank"] = math.sqrt(max(0.0, 1 - trace / rank))
            differences.append(row)
    bloch = {}
    for name in ("BLOCH144", "BLOCH288"):
        for grid in (results.get(name) or {}).get("grids", []):
            if isinstance(grid, dict) and type(grid.get("spatial_nodes")) is int:
                bloch[grid["spatial_nodes"]] = {
                    "minimum_gap_meV": number(grid.get("minimum_gap_meV")),
                    "minimum_gap_phase_rad": number(grid.get("minimum_gap_phase_rad")),
                    "min_gap_stable": grid.get("min_gap_stable") if type(grid.get("min_gap_stable")) is bool else None,
                }
    lo, hi = (bloch.get(nodes, {}).get("minimum_gap_meV") for nodes in (144, 288))
    return {"window_comparisons": differences, "bloch_by_grid": bloch,
            "bloch_288_minus_144_gap_meV": hi - lo if lo is not None and hi is not None else None}


def compare_transport(results):
    arms = {name: transport_result(results.get(name), name) for name in TRANSPORT}
    pairs = {}
    for kind, a, b in (
        ("radial_32", "T17A32", "T33A32"), ("radial_128", "T17A128", "T33A128"),
        ("angular_K17", "T17A32", "T17A128"), ("angular_K33", "T33A32", "T33A128"),
    ):
        left, right = arms[a], arms[b]
        same = (left["fixed"] == right["fixed"] and left["identity_known"] and right["identity_known"]
                and left["variation_matches"] and right["variation_matches"])
        strict = left["qualified"] and right["qualified"] and same
        a_j, b_j = left["J_A_cm2"], right["J_A_cm2"]
        delta = b_j - a_j if same and a_j is not None and b_j is not None else None
        ranges = [arm["last8_range_A_cm2"] for arm in (left, right)]
        bound = sum(ranges) if all(value is not None for value in ranges) else None
        lprof, rprof = left["density"], right["density"]
        difference = None
        if lprof and rprof and lprof[0] == rprof[0] and same:
            dz = [y - x for x, y in zip(lprof[1], rprof[1])]
            difference = {"z_nm": lprof[0], "right_minus_left_cm_minus_3": dz,
                          "max_abs_cm_minus_3": max(map(abs, dz))}
        pairs[kind] = {
            "arms": [a, b],
            "kind": "quantitative" if strict else "descriptive" if delta is not None else "unmeasured",
            "fixed_inputs_match": same,
            "delta_J_A_cm2": delta,
            "sum_two_last8_ranges_A_cm2": bound,
            "distinguished_from_observed_drift": (
                abs(delta) > bound if strict and delta is not None and bound is not None else None),
            "density_difference": difference,
        }

    p32, p128 = pairs["radial_32"], pairs["radial_128"]
    d32, d128 = p32["delta_J_A_cm2"], p128["delta_J_A_cm2"]
    cross_delta = d128 - d32 if d32 is not None and d128 is not None else None
    ranges = [arm["last8_range_A_cm2"] for arm in arms.values()]
    bound = sum(ranges) if all(value is not None for value in ranges) else None
    same = all(arm["fixed"] == arms["T17A32"]["fixed"] and arm["identity_known"]
               and arm["variation_matches"] for arm in arms.values())
    if not same:
        cross_delta = None
    strict = same and all(arm["qualified"] for arm in arms.values())
    cross = {
        "definition": "(J33−J17)128 − (J33−J17)32",
        "delta_A_cm2": cross_delta,
        "sum_four_last8_ranges_A_cm2": bound,
        "kind": "quantitative" if strict else "descriptive" if cross_delta is not None else "unmeasured",
        "fixed_inputs_match_all_four": same,
        "distinguished_from_observed_drift": (
            abs(cross_delta) > bound if strict and cross_delta is not None and bound is not None else None),
    }
    pilot = results.get("PILOT") or {}
    trial = results.get("T17A32") or {}
    first = trial.get("iterations")
    prior = pilot.get("last_iteration")
    reproduce = {}
    if (pilot.get("status") == "admitted" and isinstance(prior, dict)
            and isinstance(first, list) and first and isinstance(first[0], dict)
            and first[0].get("ν") == prior.get("ν")
            and all(pilot.get(key) == trial.get(key) for key in (*FIXED, "radial_nodes", "angular_nodes", "core", "runner"))):
        for key in ROW_FIELDS[1:]:
            a, b = number(prior.get(key)), number(first[0].get(key))
            if a is not None and b is not None:
                reproduce[key] = b - a
    return {
        "arms": {name: {key: value for key, value in arm.items() if key != "density"} for name, arm in arms.items()},
        "pairs": pairs, "interaction": cross,
        "cold_start_first_map_minus_pilot": reproduce or None,
        "qualification": (
            "Количественные сравнения требуют сходящихся внутренних серий SCBA, сопоставимых входов, "
            "конечных терминальных невязок и восьми последовательных наблюдений. "
            "Поздний разброс J — мера наблюдённого дрейфа; он не задаёт предел полной ошибки. "
            "Скалярный ток и профиль плотности не удостоверяют пространственную однородность тока."),
    }


def fmt(value):
    if value is None:
        return "н/д"
    if type(value) is float:
        return f"{value:.6g}"
    if type(value) in (str, int, bool):
        safe = clean(value)
        return str(safe).replace("|", "∣").replace("\n", " ")
    return "н/д"


def reason_text(cases, files):
    return " · ".join(f"{n} {fmt(cases[n].get('reason', cases[n]['status']))}" for n in files)



def weighted_errors(rows):
    summaries = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        fields = row.get("fields", {})
        if isinstance(fields, list):
            fields = {value.get("field", value.get("name")): value for value in fields if isinstance(value, dict)}
        if not isinstance(fields, dict):
            continue
        values = []
        for field in ("diagonal", "gaussian_projector"):
            diagnostics = fields.get(field, {})
            if not isinstance(diagnostics, dict):
                continue
            action = diagnostics.get("ring_weighted_action", {})
            error = action.get("relative_l2") if isinstance(action, dict) else None
            if number(error) is not None:
                values.append(f"{field} {fmt(error)}")
        if values:
            summaries.append(f"{fmt(row.get('rule'))} ({', '.join(values)})")
    return ", ".join(summaries)


def measure_text(name, data):
    if name in ("B7", "B9", "B11"):
        candidates = [
            row for row in data[0].get("candidates", []) if isinstance(row, dict)
        ]
        if not candidates:
            return None
        return "ранг (общий, ближайший, две пары) " + " · ".join(
            f"{fmt(row.get('rank'))} "
            f"({fmt(row.get('translation'))}, {fmt(row.get('translation_nearest'))}, "
            f"{fmt(row.get('translation_two_pairs'))})" for row in candidates
        )
    if name == "BLOCH":
        grids = [row for part in data for row in part.get("grids", []) if isinstance(row, dict)]
        if not grids:
            return None
        return "минимальный зазор 7–8 " + " · ".join(
            f"{fmt(row.get('spatial_nodes'))} ячеек, {fmt(row.get('minimum_gap_meV'))} мэВ "
            f"при фазе {fmt(row.get('minimum_gap_phase_rad'))} рад"
            for row in sorted(grids, key=lambda row: row["spatial_nodes"])
        )
    if name in ("IMP17", "IMP33", "LO"):
        grids = [row for part in data for row in part.get("grids", []) if isinstance(row, dict)]
        summaries = []
        for grid in sorted(grids, key=lambda row: row["radial_nodes"]):
            if name == "LO":
                angular = weighted_errors(grid.get("angular_comparisons", []))
                longitudinal = weighted_errors(grid.get("longitudinal_comparisons", []))
                summary = " · ".join(value for value in (
                    f"углы {angular}" if angular else "", f"qz {longitudinal}" if longitudinal else ""
                ) if value)
            else:
                summary = weighted_errors(grid.get("comparisons", []))
                scalar = grid.get("diagonal_k0p30_zero_distance", {})
                if isinstance(scalar, dict) and isinstance(scalar.get("relative_errors"), list):
                    errors = ", ".join(
                        f"{fmt(rule)} {fmt(error)}" for rule, error in
                        zip(scalar.get("rules", []), scalar["relative_errors"])
                    )
                    if errors:
                        summary += f" · скалярная диагональ {errors}"
            if summary:
                summaries.append(f"K{fmt(grid.get('radial_nodes'))} {summary}")
        return "Относительные ошибки действия · " + " · ".join(summaries) if summaries else None
    if name == "SHIFT" and data[0].get("rows"):
        row = data[0]
        return (
            f"совпадение максимумов E239 {fmt(row.get('E239_baseline_matches'))} · "
            f"допуск сопряжённости конечных объёмов {fmt(row.get('finite_volume_adjoint_pass'))}"
        )
    if name in ("SELECT", "PILOT", *TRANSPORT):
        row = data[0]
        if name == "SELECT" and row.get("status") == "admitted":
            return f"выбран ранг {fmt(row.get('rank'))}, P_basis {fmt(row.get('p_basis'))}"
        last = row.get("last_iteration", {})
        if not isinstance(last, dict) or number(last.get("J_A_cm2")) is None:
            return None
        return (f"{fmt(row.get('completed_iterations'))} итераций, "
                f"терминальный J = {fmt(last['J_A_cm2'])} А/см²")
    return None


def render_report(summary, files, raw):
    lines = [
        "# Dupont V843. Базис, операторы и условный транспорт", "",
        f"Ревизия драйверов `{fmt(summary['driver_revision'])}`. DAGMan `{fmt(summary['dagman_job_id'])}`.", "",
        "| Направление | Прогноз | Измерение | Неопределённость | Вывод |",
        "| --- | --- | --- | --- | --- |",
    ]
    uncertainty = {
        "B7": "Эффект ранга и границ оценивается по сопоставимым базисам.",
        "B9": "Совместно меняются центральные и крайние пары.",
        "B11": "Одинаковый максимум не указывает на одинаковые центры.",
        "BLOCH": "Отдельные состояния в близкой группе чувствительны к выбору представления.",
        "IMP17": "Оценка относится к двум заданным матричным тестовым полям.",
        "IMP33": "Сопоставление требует учёта общих колец и радиальной меры.",
        "LO": "Точное угловое среднее используется на тех же узлах qz.",
        "SHIFT": "Граничный уход и ошибка действия внутри окна оцениваются отдельно.",
        "SELECT": "Литературная привязка учитывает разрешение оцифровки.",
        "PILOT": "Одна карта не устанавливает стационарность.",
    }
    for name, group in {**ROOTS, **{n: (n,) for n in ("SELECT", "PILOT", *TRANSPORT)}}.items():
        cards = [raw.get(part) or {} for part in group]
        measured = measure_text(name, cards)
        links = [f"[{part}]({files[part]})" for part in group if part in files]
        evidence = (measured + " · " if measured else "") + (" · ".join(links) or "не получено")
        states = reason_text(summary["cases"], group)
        lines.append(
            f"| {name} | {FORECAST[name]} | {evidence} | "
            f"{uncertainty.get(name, 'Используется поздний диапазон тока каждой серии.')} | {states} |"
        )
    basis = summary["basis_comparison"]
    if basis["window_comparisons"]:
        lines.extend(["", "## Сопоставление базисов", "",
                      "Изменения рассчитаны для одинакового ранга. Норма разности проекторов делится на √(2r).", "",
                      "| Окна | Ранг | Δ ближайшей пары | Δ двух пар | Δ крайних пар | Нормированное расстояние проекторов |",
                      "| --- | ---: | ---: | ---: | ---: | ---: |"])
        for row in basis["window_comparisons"]:
            change = row["later_minus_earlier"]
            lines.append(f"| {' → '.join(row['windows'])} | {row['rank']} | "
                         f"{fmt(change['translation_nearest'])} | {fmt(change['translation_two_pairs'])} | "
                         f"{fmt(change['edge_pairs_translation'])} | "
                         f"{fmt(row.get('projector_distance_over_sqrt_2rank'))} |")
    if len(basis["bloch_by_grid"]) == 2:
        lines.extend(["", "Изменение минимального зазора 7–8 при переходе 144 → 288 ячеек "
                      f"составляет {fmt(basis['bloch_288_minus_144_gap_meV'])} мэВ."])
    cross = summary["transport"]["interaction"]
    lines.extend(["", "## Транспортная чувствительность", "", summary["transport"]["qualification"], "",
                  "| Сравнение | ΔJ, А/см² | Сумма диапазонов за восемь карт, А/см² | Допуск | Различим относительно дрейфа |",
                  "| --- | ---: | ---: | --- | --- |"])
    for name, pair in summary["transport"]["pairs"].items():
        lines.append(f"| {' → '.join(pair['arms'])} | {fmt(pair['delta_J_A_cm2'])} | "
                     f"{fmt(pair['sum_two_last8_ranges_A_cm2'])} | {pair['kind']} | "
                     f"{fmt(pair['distinguished_from_observed_drift'])} |")
    lines.append(f"| {cross['definition']} | {fmt(cross['delta_A_cm2'])} | "
                 f"{fmt(cross['sum_four_last8_ranges_A_cm2'])} | {cross['kind']} | "
                 f"{fmt(cross['distinguished_from_observed_drift'])} |")
    accounting_data = summary["cpu_accounting"]
    lines.extend(["", "## Учёт CPU", "", accounting_data["definition"], "",
                  f"Статус истории HTCondor `{fmt(accounting_data['history_status'])}`. "
                  f"Записей без однозначного узла {accounting_data['jobs_without_worker_identity']}.", "",
                  "| Узел | Доступно CPU | Выделялось CPU | CPU-часы | Доля выделения | Доля исполнения | Наблюдения и ограничения |",
                  "| --- | ---: | --- | ---: | ---: | ---: | --- |"])
    for node, cpu in accounting_data["nodes"].items():
        allocated = ", ".join(map(str, cpu["allocated_cpus_observed"])) or "н/д"
        ratio = cpu["utilization_measured_subset"]
        use = f"{100 * ratio:.2f}%" if ratio is not None else "н/д"
        execution_ratio = cpu["execution_utilization_measured_subset"]
        executing = f"{100 * execution_ratio:.2f}%" if execution_ratio is not None else "н/д"
        limit = " ".join(cpu["observed_reasons_or_limitations"]) or "Замечаний в доступной телеметрии нет."
        lines.append(f"| {node} | {fmt(cpu.get('available_cpus'))} | {allocated} | "
                     f"{fmt(cpu['cpu_hours'])} | {use} | {executing} | {limit} |")
    lines.append("")
    return "\n".join(lines).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--history-json", type=Path, help="read a captured HTCondor ClassAd snapshot")
    args = parser.parse_args()
    run = args.run_directory.resolve()
    out = args.output_directory.resolve()
    if out == run or out == run / "results":
        parser.error("Use a separate output directory for the publication")
    submission = load_json(run / "submission.json", {})
    dag_id = submission.get("dagman_job_id")
    if not isinstance(dag_id, str) or not re.fullmatch(r"\d+(?:\.0)?", dag_id):
        dag_id = None
    revision = submission.get("driver_revision", submission.get("revision"))
    if not isinstance(revision, str) or not REVISION.fullmatch(revision):
        source = run / "revision"
        candidate = source.read_text(encoding="utf-8").strip() if source.is_file() else None
        revision = candidate if isinstance(candidate, str) and REVISION.fullmatch(candidate) else None

    raw, cases, files, payloads = {}, {}, {}, {}
    for name in RESULT_NAMES:
        cases[name], raw[name], artifact = read_case(run, name)
        if artifact:
            path, data = artifact
            files[name] = path
            payloads[path] = data
            cases[name]["artifact"] = path
            cases[name]["artifact_sha256"] = sha(data)

    hosts, names = inventory(load_json(run / "inventory.json", []))
    ads, history_status = history_for(dag_id, args.history_json)
    cpu = accounting(ads, raw, hosts, names)
    cpu["history_status"] = history_status
    summary = {
        "schema": "v843-basis-operators-collection-v1", "campaign": "v843-basis-operators-v1",
        "driver_revision": revision, "dagman_job_id": dag_id,
        "directions": ROOTS, "cases": cases,
        "basis_comparison": compare_basis(raw),
        "transport": compare_transport(raw),
        "cpu_accounting": cpu,
    }
    dag = run / "cluster.dag"
    if dag.is_file():
        summary["dag_sha256"] = sha(dag.read_bytes())
    matrix = load_json(run / "matrix.json", None)
    if matrix is not None:
        payloads["matrix.json"] = json_bytes(clean(matrix))
    forecasts = run / "forecasts.md"
    if forecasts.is_file() and not forecasts.is_symlink():
        payloads["forecasts.md"] = clean(forecasts.read_text(encoding="utf-8")).encode()
    payloads["summary.json"] = json_bytes(clean(summary))
    payloads["report.md"] = render_report(summary, files, raw)
    for path, data in payloads.items():
        atomic_write(out / path, data)
    manifest = "".join(f"{sha(payloads[path])}  {path}\n" for path in sorted(payloads))
    atomic_write(out / "SHA256SUMS", manifest.encode())


if __name__ == "__main__":
    main()
