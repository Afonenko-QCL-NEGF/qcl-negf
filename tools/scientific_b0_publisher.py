"""Root adapter primitive for one irrevocably preconsumed B0 scientific slot.

No CLI, startup effects, deployment, credentials, checkpoint discovery or scientific
execution. The owning adapter supplies trusted directory descriptors, filenames,
source identity and bound admission data. All publishers MUST share this lock.
This module establishes durable byte custody; hashes/booleans are not native proof.
An authenticated receiving operator must recreate the local sealed fd in worker
root custody. A coordinator-owned fd is deliberately not claimed to be root-owned.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
import re
import stat


MAX_CHECKPOINT = 2 * 1024 * 1024
MAX_INTENT = 48 * 1024
UINT64 = (1 << 64) - 1
GIB = 1 << 30
TIB = 1 << 40
B0_CAPS = dict(attempts=1, execution_node_hours=72, resident_bytes=128 * GIB,
               written_bytes=2 * TIB, read_bytes=4 * TIB, log_bytes=GIB)
S1_CAPS = dict(attempts=13, execution_node_hours=936, resident_bytes=2 * TIB,
               written_bytes=44 * TIB, read_bytes=88 * TIB, log_bytes=13 * GIB)
COUNTERS = ("scientific_submits", "scientific_execution_node_hours",
            "scientific_written_bytes", "scientific_read_bytes",
            "scientific_resident_bytes")
BUDGET_KEYS = frozenset(("read", "write", "log", "resident", "inodes", "calls",
                         "scopes", "wall_ns", "memory"))
INTENT_KEYS = frozenset(("schema", "consume_ref", "cp_revision", "slot_id",
                       "attempt_id", "nonce", "admission_sha256", "source_graph",
                       "model", "plan", "criteria", "runtime", "native_kit",
                       "release", "code", "profiles_digest", "total", "stop",
                       "root_boot", "root_deadline_ns"))
HASH_KEYS = ("admission_sha256", "source_graph", "model", "plan", "criteria",
             "runtime", "native_kit", "release", "code", "profiles_digest")
TRANSITION = "B0.transition.json"
BEFORE = "B0.before.json"
FINISH = "B0.finish.json"
ERROR = "B0.first-error.json"


class Denied(ValueError):
    """No new capability may be issued."""


class InDoubt(RuntimeError):
    """Transition custody exists: spent/unknown until same-ID Root reconcile.

    No rollback, refund, new transition, or repeated fd issuance is permitted.
    """


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def _pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise Denied("duplicate JSON key")
        out[key] = value
    return out


def _invalid_constant(value):
    raise Denied("nonfinite JSON number")


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise Denied("nonfinite JSON number")
    return number


def _parse(data, bound, canonical=False):
    if type(data) is not bytes or not 0 < len(data) <= bound:
        raise Denied("JSON byte bound")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_invalid_constant, parse_float=_finite_float)
        if type(value) is not dict:
            raise Denied("JSON object required")
        if canonical and _canonical(value) != data:
            raise Denied("noncanonical JSON")
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError, OverflowError) as exc:
        raise Denied("invalid JSON") from exc


def _uint(value, positive=False):
    if type(value) is not int or not (1 if positive else 0) <= value <= UINT64:
        raise Denied("uint64 required (booleans forbidden)")
    return value


def _identifier(value):
    if type(value) is not str or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", value):
        raise Denied("bounded identifier required")
    return value


def _digest(value):
    if type(value) is not str or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise Denied("SHA256 required")
    return value


def _name(value):
    _identifier(value)
    if value in (".", ".."):
        raise Denied("basename required")
    return value


def _keys(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise Denied("unknown or missing schema keys")


def _budget(value):
    _keys(value, BUDGET_KEYS)
    for number in value.values():
        _uint(number)
    if value["log"] > value["write"]:
        raise Denied("log is included in write")


def _intent(data, intent_id):
    value = _parse(data, MAX_INTENT, canonical=True)
    _keys(value, INTENT_KEYS)
    if value["schema"] != "qcl-b0-consumed-intent.v1":
        raise Denied("intent schema")
    for key in ("consume_ref", "slot_id", "attempt_id", "nonce", "root_boot"):
        _identifier(value[key])
    if value["consume_ref"] != _identifier(intent_id):
        raise Denied("transition identity mismatch")
    if _uint(value["cp_revision"], positive=True) != 1:
        raise Denied("initial B0 escrow revision must be one")
    _uint(value["root_deadline_ns"], positive=True)
    for key in HASH_KEYS:
        _digest(value[key])
    _budget(value["total"])
    _budget(value["stop"])
    total, stop = value["total"], value["stop"]
    limits = dict(read=B0_CAPS["read_bytes"], write=B0_CAPS["written_bytes"],
                  log=B0_CAPS["log_bytes"], resident=B0_CAPS["resident_bytes"],
                  memory=B0_CAPS["resident_bytes"], wall_ns=72 * 3600 * 10**9)
    if any(total[key] > cap for key, cap in limits.items()):
        raise Denied("B0 total cap exceeded")
    if any(stop[key] > total[key] for key in BUDGET_KEYS):
        raise Denied("STOP must be reserved inside total")
    if not all(total[key] > 0 for key in BUDGET_KEYS):
        raise Denied("finite positive total required")
    if not all(stop[key] > 0 for key in BUDGET_KEYS):
        raise Denied("finite positive STOP reservation required")
    return value


def _binding(binding, intent_bytes, intent, root_now_ns, root_boot):
    """Exact Root gate bindings, not a claim that caller data proves native facts."""
    _keys(binding, ("intent_sha256", "ready_sha256", "p0_sha256",
                    "admission_receipt_sha256", "worker_once", "children"))
    for key in ("intent_sha256", "ready_sha256", "p0_sha256", "admission_receipt_sha256"):
        _digest(binding[key])
    if binding["intent_sha256"] != _hash(intent_bytes):
        raise Denied("intent differs from Root admitted binding")
    if binding["admission_receipt_sha256"] != intent["admission_sha256"]:
        raise Denied("admission receipt mismatch")
    once = binding["worker_once"]
    _keys(once, ("uuid", "dev", "ino", "owner", "dir_dev", "dir_ino"))
    _identifier(once["uuid"])
    for key in ("dev", "ino", "owner", "dir_dev", "dir_ino"):
        _uint(once[key])
    if not once["ino"] or not once["dir_ino"] or once["owner"] != 0:
        raise Denied("worker once must identify adopted root custody")
    # These values belong to the Root host domain only. Worker deadlines must
    # receive a distinct local anchor via the authenticated transfer adapter.
    _uint(root_now_ns)
    if _identifier(root_boot) != intent["root_boot"]:
        raise Denied("Root boot mismatch")
    remaining = intent["root_deadline_ns"] - root_now_ns
    if not 0 < remaining <= 72 * 3600 * 10**9:
        raise Denied("Root deadline expired or outside B0 wall cap")
    if intent["total"]["wall_ns"] > remaining:
        raise Denied("Root remaining wall bound insufficient")
    children = binding["children"]
    if type(children) is not dict or not 1 <= len(children) <= 32:
        raise Denied("bounded named disjoint children required")
    sums = {key: 0 for key in BUDGET_KEYS}
    for name, budget in children.items():
        _identifier(name)
        if name == "STOP":
            raise Denied("STOP is separately reserved")
        _budget(budget)
        for key in BUDGET_KEYS:
            sums[key] += budget[key]
    if any(sums[key] + intent["stop"][key] > intent["total"][key] for key in BUDGET_KEYS):
        raise Denied("child partitions overlap total/STOP allowance")
    # Freeze against mutations by the trusted caller during the durable phase.
    return _parse(_canonical(binding), MAX_INTENT, canonical=True)


def _directory(fd):
    st = os.fstat(fd)
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o022:
        raise Denied("trusted owner directory required")
    return st


def _regular(fd):
    st = os.fstat(fd)
    if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid()
            or st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o600):
        raise Denied("private owner regular file required")
    return st


def _read(dirfd, name, bound):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dirfd)
    try:
        before = _regular(fd)
        if not 0 < before.st_size <= bound:
            raise Denied("file byte bound")
        chunks, count = [], 0
        while True:
            chunk = os.read(fd, min(65536, bound + 1 - count))
            if not chunk:
                break
            chunks.append(chunk)
            count += len(chunk)
            if count > bound:
                raise Denied("file exceeds bound")
        after = _regular(fd)
        identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if identity(before) != identity(after) or count != after.st_size:
            raise Denied("unstable file snapshot")
        return b"".join(chunks)
    finally:
        os.close(fd)


def _write_all(fd, data):
    view = memoryview(data)
    while view:
        count = os.write(fd, view)
        if count <= 0:
            raise OSError("short write")
        view = view[count:]


def _exclusive(dirfd, name, data):
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
                 | os.O_CLOEXEC, 0o600, dir_fd=dirfd)
    try:
        os.fchmod(fd, 0o600)
        _regular(fd)
        _write_all(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.fsync(dirfd)


def _exists(dirfd, name):
    try:
        os.stat(name, dir_fd=dirfd, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def _resync(dirfd, name):
    """Reaffirm durability of existing custody after an interrupted fsync."""
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dirfd)
    try:
        _regular(fd)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.fsync(dirfd)


@contextmanager
def _locked(lock_dirfd, lock_name):
    _directory(lock_dirfd)
    fd = os.open(_name(lock_name), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW
                 | os.O_CLOEXEC, 0o600, dir_fd=lock_dirfd)
    try:
        _regular(fd)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


def _mirrors(cp_dirfds, cp_names):
    if len(cp_dirfds) != 2 or len(cp_names) != 2:
        raise Denied("exactly two mirrors required")
    targets = []
    for directory, name in zip(cp_dirfds, cp_names):
        st = _directory(directory)
        targets.append((st.st_dev, st.st_ino, _name(name)))
    if targets[0] == targets[1]:
        raise Denied("distinct mirrors required")


def _prepare(old, intent, root_head, binding, root_now_ns):
    checkpoint = _parse(old, MAX_CHECKPOINT)
    if type(root_head) is not str or not re.fullmatch(r"[0-9a-f]{40}", root_head):
        raise Denied("current root commit required")
    source = checkpoint.get("source")
    if type(source) is not dict or source.get("root_head") != root_head:
        raise Denied("checkpoint source mismatch")
    if "currentrootcommit" in source and source["currentrootcommit"] != root_head:
        raise Denied("checkpoint source aliases disagree")
    if "currentrootcommit" in checkpoint and checkpoint["currentrootcommit"] != root_head:
        raise Denied("checkpoint source aliases disagree")
    counters = checkpoint.get("counters")
    if type(counters) is not dict:
        raise Denied("missing measured counters")
    for key in COUNTERS:
        if key not in counters or _uint(counters[key]) != 0:
            raise Denied("B0 initialization requires measured scientific zero")
    if "B0_scientific_escrow" in checkpoint:
        raise Denied("B0 is already spent/outstanding")
    # The real checkpoint schema has no synthetic measured increments. Budget
    # reservation lives only in this campaign object; counters stay actual zero.
    checkpoint["B0_scientific_escrow"] = {
        "schema": "qcl.b0.escrow.v1", "state": "PRECONSUMED",
        "intent_id": intent["consume_ref"], "intent_sha256": _hash(_canonical(intent)),
        "checkpoint_revision": intent["cp_revision"],
        "before_sha256": _hash(old), "root_head": root_head,
        "requested": dict(B0_CAPS), "debited": dict(B0_CAPS),
        "campaign_maximum": dict(S1_CAPS),
        "campaign_remaining": {key: S1_CAPS[key] - B0_CAPS[key] for key in S1_CAPS},
        "intent": intent,
        "custody_binding": binding, "root_preconsume_monotonic_ns": root_now_ns,
        "normal": {key: intent["total"][key] - intent["stop"][key]
                   for key in BUDGET_KEYS},
        "stop": intent["stop"], "partition_rule": "normal+STOP=total; disjoint children",
    }
    data = _canonical(checkpoint)
    if len(data) > MAX_CHECKPOINT:
        raise Denied("consumed checkpoint exceeds bound")
    return data


def _replace_mirrors(cp_dirfds, cp_names, data, intent_id):
    for directory, name in zip(cp_dirfds, cp_names):
        temporary = name + ".B0-" + intent_id + ".tmp"
        _exclusive(directory, temporary, data)
        os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
        os.fsync(directory)


def _reread(cp_dirfds, cp_names, expected):
    for directory, name in zip(cp_dirfds, cp_names):
        if _read(directory, name, MAX_CHECKPOINT) != expected:
            raise InDoubt("consumed mirror reread differs")


def _finish(custody_dirfd, transition):
    data = _canonical({"schema": "qcl.b0.finish.v1", "intent_id": transition["intent_id"],
                       "after_sha256": transition["after_sha256"], "state": "PRECONSUMED"})
    _exclusive(custody_dirfd, FINISH, data)
    if _read(custody_dirfd, FINISH, MAX_INTENT) != data:
        raise InDoubt("finish reread differs")


def _error(custody_dirfd, intent_id, exc):
    # Preserve first error only. Failure of this write never refunds the slot.
    try:
        _exclusive(custody_dirfd, ERROR, _canonical({"intent_id": intent_id,
                   "state": "spent/in_doubt", "error_type": type(exc).__name__,
                   "message": str(exc)[:512]}))
    except Exception:
        pass


def _sealed_readonly(data):
    fd = os.memfd_create("qcl-B0-consumed-intent", os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
    readonly = None
    try:
        _write_all(fd, data)
        seals = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, seals)
        readonly = os.open("/proc/self/fd/" + str(fd), os.O_RDONLY | os.O_CLOEXEC)
        a, b = os.fstat(fd), os.fstat(readonly)
        if ((a.st_dev, a.st_ino, a.st_uid) != (b.st_dev, b.st_ino, os.geteuid())
                or fcntl.fcntl(readonly, fcntl.F_GET_SEALS) != seals
                or fcntl.fcntl(readonly, fcntl.F_GETFL) & os.O_ACCMODE != os.O_RDONLY):
            raise InDoubt("sealed descriptor verification failed")
        result, readonly = readonly, None
        return result
    finally:
        if readonly is not None:
            os.close(readonly)
        os.close(fd)


def preconsume_b0_intent(cp_dirfds, cp_names, expected_sha256, intent_bytes, intent_id,
                         *, lock_dirfd, custody_dirfd, root_head, custody_binding,
                         root_now_ns, root_boot, lock_name="checkpoint.publisher.lock"):
    """Consume once, return a readonly sealed intent fd only after durable custody.

    Inputs are already authorized Root adapter facts, not worker request paths.
    Root boot/deadline are opaque Root-domain bindings; worker monotonic time is
    never compared here. Admission/native evidence must be checked by the caller.
    The caller owns the returned fd. Any failure after custody starts is spent,
    including fd creation/delivery failure. Repeated calls never issue another fd.
    """
    intent = _intent(intent_bytes, intent_id)
    binding = _binding(custody_binding, intent_bytes, intent, root_now_ns, root_boot)
    _digest(expected_sha256)
    _mirrors(cp_dirfds, cp_names)
    _directory(custody_dirfd)
    with _locked(lock_dirfd, lock_name):
        if any(_exists(custody_dirfd, name) for name in (TRANSITION, BEFORE, FINISH, ERROR)):
            raise InDoubt("existing transition custody; same-ID reconciliation only")
        old = _read(cp_dirfds[0], cp_names[0], MAX_CHECKPOINT)
        if old != _read(cp_dirfds[1], cp_names[1], MAX_CHECKPOINT) or _hash(old) != expected_sha256:
            raise Denied("mirror CAS failed")
        data = _prepare(old, intent, root_head, binding, root_now_ns)
        transition = {"schema": "qcl.b0.transition.v1", "intent_id": intent_id,
                      "before_sha256": expected_sha256, "after_sha256": _hash(data),
                      "intent": intent, "root_head": root_head,
                      "custody_binding": binding, "root_preconsume_monotonic_ns": root_now_ns}
        transition_bytes = _canonical(transition)
        if len(transition_bytes) > MAX_INTENT * 2:
            raise Denied("transition byte bound")
        try:
            # Persist before first: even interrupted/empty intent custody blocks
            # every new grant. No rollback or automatic cleanup of temp files.
            _exclusive(custody_dirfd, BEFORE, old)
            _exclusive(custody_dirfd, TRANSITION, transition_bytes)
            _replace_mirrors(cp_dirfds, cp_names, data, intent_id)
            _finish(custody_dirfd, transition)
            _reread(cp_dirfds, cp_names, data)
            envelope = {"schema": "qcl.b0.consumed-intent.v1", "intent_id": intent_id,
                        "checkpoint_sha256": _hash(data),
                        "checkpoint_revision": intent["cp_revision"], "intent": intent}
            return _sealed_readonly(_canonical(envelope))
        except Exception as exc:
            _error(custody_dirfd, intent_id, exc)
            raise InDoubt("B0 spent/in_doubt; original custody retained") from exc


def reconcile_b0_same_intent(cp_dirfds, cp_names, intent_id, *, lock_dirfd,
                             custody_dirfd, lock_name="checkpoint.publisher.lock"):
    """Root-only reconciliation of identical interrupted custody; NEVER issue fd.

    A lost response cannot distinguish delivery, therefore recovery cannot mint a
    capability. Empty/truncated/conflicting custody requires manual investigation.
    Existing writer lock migration is a separate installation gate.
    """
    _identifier(intent_id)
    _mirrors(cp_dirfds, cp_names)
    _directory(custody_dirfd)
    with _locked(lock_dirfd, lock_name):
        transition = _parse(_read(custody_dirfd, TRANSITION, MAX_INTENT * 2),
                            MAX_INTENT * 2, canonical=True)
        _keys(transition, ("schema", "intent_id", "before_sha256", "after_sha256", "intent",
                           "root_head", "custody_binding", "root_preconsume_monotonic_ns"))
        if transition["schema"] != "qcl.b0.transition.v1" or transition["intent_id"] != intent_id:
            raise InDoubt("different transition identity")
        intent = _intent(_canonical(transition["intent"]), intent_id)
        before = _read(custody_dirfd, BEFORE, MAX_CHECKPOINT)
        if _hash(before) != _digest(transition["before_sha256"]):
            raise InDoubt("before custody mismatch")
        root_now_ns = transition["root_preconsume_monotonic_ns"]
        binding = _binding(transition["custody_binding"], _canonical(intent), intent,
                           root_now_ns, intent["root_boot"])
        data = _prepare(before, intent, transition["root_head"], binding, root_now_ns)
        if _hash(data) != _digest(transition["after_sha256"]):
            raise InDoubt("after custody mismatch")
        try:
            _resync(custody_dirfd, BEFORE)
            _resync(custody_dirfd, TRANSITION)
            snapshots = [_read(directory, name, MAX_CHECKPOINT)
                         for directory, name in zip(cp_dirfds, cp_names)]
            for current in snapshots:
                if current not in (before, data):
                    raise InDoubt("mirror has unrelated bytes")
            for directory, name, current in zip(cp_dirfds, cp_names, snapshots):
                if current == before:
                    temporary = name + ".B0-reconcile-" + intent_id + ".tmp"
                    if _exists(directory, temporary):
                        if _read(directory, temporary, MAX_CHECKPOINT) != data:
                            raise InDoubt("recovery temporary differs")
                        _resync(directory, temporary)
                    else:
                        _exclusive(directory, temporary, data)
                    os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
                # Includes an already renamed mirror whose prior directory
                # fsync failed: visible bytes alone do not establish durability.
                os.fsync(directory)
            _reread(cp_dirfds, cp_names, data)
            expected_finish = _canonical({"schema": "qcl.b0.finish.v1", "intent_id": intent_id,
                               "after_sha256": transition["after_sha256"], "state": "PRECONSUMED"})
            if _exists(custody_dirfd, FINISH):
                if _read(custody_dirfd, FINISH, MAX_INTENT) != expected_finish:
                    raise InDoubt("finish conflict")
                # A previous fsync may have failed even with visible bytes.
                _resync(custody_dirfd, FINISH)
            else:
                _finish(custody_dirfd, transition)
            _reread(cp_dirfds, cp_names, data)
            return {"intent_id": intent_id, "state": "PRECONSUMED_NO_REISSUE",
                    "checkpoint_sha256": _hash(data)}
        except Exception as exc:
            _error(custody_dirfd, intent_id, exc)
            raise InDoubt("same-ID reconcile remains spent/in_doubt") from exc
