"""Disposable local custody fixtures only; no production checkpoint or solver.

Source packet: these tests have NOT been run. Execution needs its own finite grant.
"""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    "scientific_b0_publisher", Path(__file__).resolve().parents[1] / "tools" / "scientific_b0_publisher.py")
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def digest(value):
    return hashlib.sha256(value).hexdigest()


class B0PublisherTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dirs = []
        for name in ("mirror-a", "mirror-b", "custody", "lock"):
            path = self.root / name
            path.mkdir(mode=0o700)
            fd = os.open(path, os.O_DIRECTORY | os.O_RDONLY)
            self.addCleanup(os.close, fd)
            self.dirs.append(fd)
        self.head = "6" * 40
        self.checkpoint = {"source": {"root_head": self.head}, "counters": {
            key: 0 for key in publisher.COUNTERS}, "unrelated": {"label": "keep", "actual": 7}}
        self.old = canonical(self.checkpoint)
        for name in ("mirror-a", "mirror-b"):
            path = self.root / name / "checkpoint.json"
            path.write_bytes(self.old)
            path.chmod(0o600)
        budget = dict(read=4 * publisher.TIB, write=2 * publisher.TIB,
                      log=publisher.GIB, resident=128 * publisher.GIB,
                      memory=128 * publisher.GIB, inodes=1024, calls=4096,
                      scopes=1024, wall_ns=72 * 3600 * 10**9)
        self.intent = dict(schema="qcl-b0-consumed-intent.v1", consume_ref="B0-one",
                           cp_revision=1, slot_id="S1", attempt_id="B0", nonce="unique-nonce",
                           root_boot="root-boot", root_deadline_ns=72 * 3600 * 10**9 + 100,
                           total=budget, stop={key: 1 for key in publisher.BUDGET_KEYS})
        self.intent.update({key: "a" * 64 for key in publisher.HASH_KEYS})

    def binding(self, intent):
        return dict(intent_sha256=digest(canonical(intent)), ready_sha256="b" * 64,
                    p0_sha256="c" * 64, admission_receipt_sha256=intent["admission_sha256"],
                    worker_once=dict(uuid="once-B0", dev=8, ino=102, owner=0,
                                     dir_dev=8, dir_ino=100),
                    children={"worker": {key: intent["total"][key] - intent["stop"][key]
                                           for key in publisher.BUDGET_KEYS}})

    def call(self, *, intent=None, expected=None):
        return publisher.preconsume_b0_intent(
            self.dirs[:2], ("checkpoint.json", "checkpoint.json"),
            expected or digest(self.old), canonical(intent or self.intent), "B0-one",
            lock_dirfd=self.dirs[3], custody_dirfd=self.dirs[2], root_head=self.head,
            custody_binding=self.binding(intent or self.intent), root_now_ns=100,
            root_boot="root-boot")

    def read_mirror(self, index=0):
        return (self.root / ("mirror-a", "mirror-b")[index] / "checkpoint.json").read_bytes()

    def assert_untouched(self):
        self.assertEqual(self.read_mirror(), self.old)
        self.assertEqual(self.read_mirror(1), self.old)
        self.assertEqual(list((self.root / "custody").iterdir()), [])

    def reconcile(self, identity="B0-one"):
        return publisher.reconcile_b0_same_intent(
            self.dirs[:2], ("checkpoint.json", "checkpoint.json"), identity,
            lock_dirfd=self.dirs[3], custody_dirfd=self.dirs[2])

    def test_durable_consume_preserves_actual_zero_and_debits_only_escrow(self):
        fd = self.call()
        self.addCleanup(os.close, fd)
        data = self.read_mirror()
        self.assertEqual(data, self.read_mirror(1))
        cp = json.loads(data)
        self.assertEqual(cp["counters"], self.checkpoint["counters"])
        self.assertEqual(cp["unrelated"], self.checkpoint["unrelated"])
        self.assertEqual(cp["source"], self.checkpoint["source"])
        escrow = cp["B0_scientific_escrow"]
        self.assertEqual(escrow["debited"], publisher.B0_CAPS)
        self.assertEqual(escrow["campaign_maximum"], publisher.S1_CAPS)
        self.assertEqual(escrow["campaign_remaining"]["attempts"], 12)
        envelope = json.loads(os.read(fd, publisher.MAX_INTENT * 2))
        self.assertEqual(envelope["checkpoint_sha256"], digest(data))
        self.assertEqual(envelope["intent"], self.intent)
        self.assertTrue((self.root / "custody" / publisher.FINISH).exists())

    def test_descriptor_is_readonly_and_fully_sealed_owned_by_actual_euid(self):
        fd = self.call()
        self.addCleanup(os.close, fd)
        seals = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL
        self.assertEqual(fcntl.fcntl(fd, fcntl.F_GET_SEALS), seals)
        self.assertEqual(fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE, os.O_RDONLY)
        self.assertEqual(os.fstat(fd).st_uid, os.geteuid())
        with self.assertRaises(OSError):
            os.write(fd, b"X")
        writable = os.open("/proc/self/fd/" + str(fd), os.O_RDWR)
        try:
            with self.assertRaises(OSError):
                os.write(writable, b"X")
            with self.assertRaises(OSError):
                os.ftruncate(writable, 0)
        finally:
            os.close(writable)

    def test_second_call_and_same_id_recovery_never_issue_another_fd(self):
        fd = self.call()
        os.close(fd)
        with mock.patch.object(publisher, "_sealed_readonly", side_effect=AssertionError("reissued")):
            with self.assertRaises(publisher.InDoubt):
                self.call(expected=digest(self.read_mirror()))
            self.assertEqual(self.reconcile()["state"], "PRECONSUMED_NO_REISSUE")
            with self.assertRaises(publisher.InDoubt):
                self.reconcile("B0-other")

    def test_stale_digest_and_mismatched_mirror_deny_before_custody(self):
        with self.assertRaises(publisher.Denied):
            self.call(expected="0" * 64)
        self.assert_untouched()
        (self.root / "mirror-b" / "checkpoint.json").write_bytes(self.old + b" ")
        with self.assertRaises(publisher.Denied):
            self.call()
        self.assertEqual(list((self.root / "custody").iterdir()), [])

    def test_common_lock_conflict_denies_before_any_custody(self):
        lock = os.open("checkpoint.publisher.lock", os.O_CREAT | os.O_RDWR, 0o600, dir_fd=self.dirs[3])
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                self.call()
            self.assert_untouched()
        finally:
            os.close(lock)

    def test_fsync_failure_retains_before_and_spent_error_no_grant(self):
        real_fsync = os.fsync
        calls = 0

        def fail_once(fd):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected before-directory fsync")
            return real_fsync(fd)

        with mock.patch.object(publisher.os, "fsync", side_effect=fail_once):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        self.assertTrue((self.root / "custody" / publisher.BEFORE).exists())
        self.assertTrue((self.root / "custody" / publisher.ERROR).exists())
        with self.assertRaises(publisher.InDoubt):
            self.call()
        with self.assertRaises(FileNotFoundError):
            self.reconcile()

    def test_partial_mirror_keeps_debit_recovery_same_id_only_no_fd(self):
        real_replace = os.replace
        calls = 0

        def replace_once(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected second mirror rename")
            return real_replace(*args, **kwargs)

        with mock.patch.object(publisher.os, "replace", side_effect=replace_once):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        self.assertIn("B0_scientific_escrow", json.loads(self.read_mirror()))
        self.assertEqual(self.read_mirror(1), self.old)
        with self.assertRaises(publisher.InDoubt):
            self.call()
        with mock.patch.object(publisher, "_sealed_readonly", side_effect=AssertionError("grant")):
            self.assertEqual(self.reconcile()["state"], "PRECONSUMED_NO_REISSUE")
        self.assertEqual(self.read_mirror(), self.read_mirror(1))
        self.assertTrue((self.root / "custody" / publisher.ERROR).exists())

    def test_memfd_failure_remains_spent(self):
        with mock.patch.object(publisher, "_sealed_readonly", side_effect=OSError("fd failure")):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        self.assertEqual(self.read_mirror(), self.read_mirror(1))
        self.assertIn("B0_scientific_escrow", json.loads(self.read_mirror()))
        with self.assertRaises(publisher.InDoubt):
            self.call()

    def test_actual_counter_missing_bool_nonzero_or_source_mismatch_deny(self):
        for mutation in ("missing", "bool", "nonzero", "source"):
            with self.subTest(mutation=mutation):
                cp = copy.deepcopy(self.checkpoint)
                if mutation == "missing":
                    del cp["counters"]["scientific_read_bytes"]
                elif mutation == "bool":
                    cp["counters"]["scientific_read_bytes"] = False
                elif mutation == "nonzero":
                    cp["counters"]["scientific_read_bytes"] = 1
                else:
                    cp["source"]["root_head"] = "7" * 40
                data = canonical(cp)
                for name in ("mirror-a", "mirror-b"):
                    (self.root / name / "checkpoint.json").write_bytes(data)
                with self.assertRaises(publisher.Denied):
                    self.call(expected=digest(data))
                self.assertEqual(list((self.root / "custody").iterdir()), [])

    def test_strict_intent_rejects_bool_unknown_nan_duplicate_and_noncanonical(self):
        for mutate in (lambda x: x.update(unknown=True),
                       lambda x: x.update(cp_revision=True),
                       lambda x: x["total"].update(calls=False),
                       lambda x: x["stop"].update(read=x["total"]["read"] + 1)):
            intent = copy.deepcopy(self.intent)
            mutate(intent)
            with self.assertRaises(publisher.Denied):
                self.call(intent=intent)
            self.assert_untouched()
        for raw in (b'{"x":1,"x":2}\n', b'{"x":NaN}\n', b'{"x":Infinity}\n', b'{"x":1e999}\n',
                    json.dumps(self.intent).encode()):
            with self.assertRaises(publisher.Denied):
                publisher._intent(raw, "B0-one")

    def test_existing_escrow_symlink_and_hardlink_refused(self):
        cp = copy.deepcopy(self.checkpoint)
        cp["B0_scientific_escrow"] = None
        data = canonical(cp)
        for name in ("mirror-a", "mirror-b"):
            (self.root / name / "checkpoint.json").write_bytes(data)
        with self.assertRaises(publisher.Denied):
            self.call(expected=digest(data))
        path = self.root / "mirror-a" / "checkpoint.json"
        path.unlink()
        path.symlink_to(self.root / "mirror-b" / "checkpoint.json")
        with self.assertRaises(OSError):
            self.call(expected=digest(data))
        path.unlink()
        os.link(self.root / "mirror-b" / "checkpoint.json", path)
        with self.assertRaises(publisher.Denied):
            self.call(expected=digest(data))
        self.assertEqual(list((self.root / "custody").iterdir()), [])

    def test_bounded_snapshot_and_short_writes(self):
        with mock.patch.object(publisher.os, "write", return_value=0):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        self.assertTrue((self.root / "custody" / publisher.BEFORE).exists())
        with self.assertRaises(publisher.InDoubt):
            self.call()

    def test_reconcile_never_overwrites_unrelated_mirror(self):
        with mock.patch.object(publisher, "_replace_mirrors", side_effect=OSError("interrupted")):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        unrelated = canonical({"source": "other"})
        (self.root / "mirror-b" / "checkpoint.json").write_bytes(unrelated)
        with self.assertRaises(publisher.InDoubt):
            self.reconcile()
        self.assertEqual(self.read_mirror(1), unrelated)

    def test_root_clock_binding_and_partition_unknowns_deny(self):
        for which in ("wrong-hash", "unknown", "overlap", "worker-owner", "clock", "boot"):
            with self.subTest(which=which):
                binding = self.binding(self.intent)
                now, boot = 100, "root-boot"
                if which == "wrong-hash":
                    binding["intent_sha256"] = "0" * 64
                elif which == "unknown":
                    binding["unknown"] = True
                elif which == "overlap":
                    binding["children"]["other"] = binding["children"]["worker"].copy()
                elif which == "worker-owner":
                    binding["worker_once"]["owner"] = os.geteuid() or 1000
                elif which == "clock":
                    now = self.intent["root_deadline_ns"]
                else:
                    boot = "worker-boot"
                with self.assertRaises(publisher.Denied):
                    publisher.preconsume_b0_intent(
                        self.dirs[:2], ("checkpoint.json", "checkpoint.json"), digest(self.old),
                        canonical(self.intent), "B0-one", lock_dirfd=self.dirs[3],
                        custody_dirfd=self.dirs[2], root_head=self.head,
                        custody_binding=binding, root_now_ns=now, root_boot=boot)
                self.assert_untouched()

    def test_finish_file_fsync_failure_never_issues_fd(self):
        real_exclusive = publisher._exclusive

        def fault(directory, name, data):
            if name == publisher.FINISH:
                raise OSError("injected finish fsync failure")
            return real_exclusive(directory, name, data)

        with mock.patch.object(publisher, "_exclusive", side_effect=fault):
            with mock.patch.object(publisher, "_sealed_readonly", side_effect=AssertionError("early fd")):
                with self.assertRaises(publisher.InDoubt):
                    self.call()
        self.assertEqual(self.read_mirror(), self.read_mirror(1))
        self.assertFalse((self.root / "custody" / publisher.FINISH).exists())
        self.assertEqual(self.reconcile()["state"], "PRECONSUMED_NO_REISSUE")

    def test_oversized_or_mutating_checkpoint_rejected_before_debit(self):
        path = self.root / "mirror-a" / "checkpoint.json"
        path.write_bytes(b" " * (publisher.MAX_CHECKPOINT + 1))
        with self.assertRaises(publisher.Denied):
            self.call()
        self.assertEqual(list((self.root / "custody").iterdir()), [])
        path.write_bytes(self.old)
        real_read = os.read
        mutated = False

        def read_then_change(fd, count):
            nonlocal mutated
            data = real_read(fd, count)
            if data and not mutated:
                mutated = True
                path.write_bytes(self.old + b" ")
            return data

        with mock.patch.object(publisher.os, "read", side_effect=read_then_change):
            with self.assertRaises(publisher.Denied):
                self.call()
        self.assertEqual(list((self.root / "custody").iterdir()), [])

    def test_repeat_interrupted_same_id_recovery_reuses_exact_temp_without_grant(self):
        with mock.patch.object(publisher, "_replace_mirrors", side_effect=OSError("initial stop")):
            with self.assertRaises(publisher.InDoubt):
                self.call()
        with mock.patch.object(publisher.os, "replace", side_effect=OSError("recovery interrupted")):
            with self.assertRaises(publisher.InDoubt):
                self.reconcile()
        with mock.patch.object(publisher, "_sealed_readonly", side_effect=AssertionError("grant")):
            self.assertEqual(self.reconcile()["state"], "PRECONSUMED_NO_REISSUE")
        self.assertEqual(self.read_mirror(), self.read_mirror(1))
