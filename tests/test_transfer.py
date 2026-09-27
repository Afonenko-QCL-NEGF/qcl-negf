"""Exercise the transfer CLI against a fake GitHub API and real local Git configs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "ops" / "transfer-github.sh"
TARGET = "Afonenko-QCL-NEGF"
FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
p = Path(os.environ["TRANSFER_STATE"])
s = json.loads(p.read_text())
a = sys.argv[1:]
if a[:2] == ["auth", "status"]: sys.exit(0)
endpoint = next((v for v in a if v.startswith(("repos/", "orgs/"))), "")
if endpoint.startswith("orgs/"):
    print("Afonenko-QCL-NEGF"); sys.exit(0)
parts = endpoint.split("/")
owner, name = parts[1:3]
entry = s["repos"][name]
if "--method" in a and a[a.index("--method") + 1] == "POST":
    assert parts[-1] == "transfer"
    assert "new_owner=Afonenko-QCL-NEGF" in a
    s["posts"].append(name)
    if not s.get("pending"): entry["owner"] = "Afonenko-QCL-NEGF"
    p.write_text(json.dumps(s)); sys.exit(0)
code = s.get("failure", 200)
repo_id = entry["id"]
full = entry["owner"] + "/" + name
if code == 200 and owner == "Afonenko-QCL-NEGF" and entry["owner"] != owner:
    code = 404
    if s.get("collision") == name:
        code, repo_id, full = 200, 9999, owner + "/" + name
print("HTTP/2.0 " + str(code) + " Status\r\nContent-Type: application/json\r\n\r\n", end="")
if code == 200:
    print("REPO\t%s\t%s\ttrue\tfalse" % (repo_id, full)); sys.exit(0)
print("REPO\tnull\tnull\tfalse\tnull")
print("gh: error (HTTP %s)" % code, file=sys.stderr)
sys.exit(1)
'''


class TransferTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.root = self.directory / "checkout with spaces"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("remote", "add", "origin", "https://github.com/AfonenkoA/qcl-negf.git")
        self.child = self.root / "components" / "QCLNEGF.jl"
        self.child.mkdir(parents=True)
        self.git("init", "-q", "-b", "main", cwd=self.child)
        self.git("remote", "add", "origin", "https://github.com/AfonenkoA/QCLNEGF.jl.git", cwd=self.child)
        self.modules = '[submodule "QCLNEGF.jl"]\n path = components/QCLNEGF.jl\n url = https://github.com/AfonenkoA/QCLNEGF.jl.git\n'
        (self.root / ".gitmodules").write_text(self.modules)
        self.state = self.directory / "state.json"
        self.state.write_text(json.dumps({"repos": {
            "QCLNEGF.jl": {"id": 101, "owner": "AfonenkoA"},
            "qcl-negf": {"id": 102, "owner": "AfonenkoA"},
        }, "posts": []}))
        self.bin = self.directory / "bin"
        self.bin.mkdir()
        (self.bin / "gh").write_text(FAKE_GH)
        (self.bin / "gh").chmod(0o755)
        (self.bin / "sleep").write_text('#!/bin/sh\nexit 0\n')
        (self.bin / "sleep").chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
                    "TRANSFER_STATE": str(self.state), "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull}

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", "-C", str(cwd or self.root), *args], text=True).strip()

    def call(self, *args):
        return subprocess.run(["bash", str(SCRIPT), *args, "--root", str(self.root)],
                              env=self.env, text=True, capture_output=True, timeout=15)

    def data(self):
        return json.loads(self.state.read_text())

    def update(self, **values):
        self.state.write_text(json.dumps({**self.data(), **values}))

    def test_plan_is_read_only_and_components_precede_root(self):
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.data()["posts"], [])
        self.assertLess(result.stdout.index("QCLNEGF.jl/transfer"), result.stdout.index("qcl-negf/transfer"))
        self.assertEqual(self.git("remote", "get-url", "origin"), "https://github.com/AfonenkoA/qcl-negf.git")

    def test_apply_and_retry_preserve_worktree_and_set_ssh_push(self):
        for _ in range(2):
            result = self.call("--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.data()["posts"], ["QCLNEGF.jl", "qcl-negf"])
        self.assertEqual((self.root / ".gitmodules").read_text(), self.modules)
        self.assertEqual(self.git("remote", "get-url", "--push", "origin"), f"git@github.com:{TARGET}/qcl-negf.git")
        self.assertEqual(self.git("remote", "get-url", "--push", "origin", cwd=self.child), f"git@github.com:{TARGET}/QCLNEGF.jl.git")

    def test_partial_transfer_skips_completed_component(self):
        data = self.data()
        data["repos"]["QCLNEGF.jl"]["owner"] = TARGET
        self.state.write_text(json.dumps(data))
        result = self.call("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.data()["posts"], ["qcl-negf"])

    def test_collision_in_last_repository_blocks_all_transfers(self):
        self.update(collision="qcl-negf")
        self.assertNotEqual(self.call("--apply").returncode, 0)
        self.assertEqual(self.data()["posts"], [])

    def test_unrelated_local_origin_blocks_transfers(self):
        self.git("remote", "set-url", "origin", "https://github.com/another/qcl-negf.git")
        self.assertNotEqual(self.call("--apply").returncode, 0)
        self.assertEqual(self.data()["posts"], [])

    def test_auth_and_server_errors_are_not_absence(self):
        for status in [401, 403, 500]:
            with self.subTest(status=status):
                self.update(failure=status)
                self.assertNotEqual(self.call("--apply").returncode, 0)
                self.assertEqual(self.data()["posts"], [])

    def test_sync_does_not_transfer_pending_repositories(self):
        self.assertNotEqual(self.call("--sync-local").returncode, 0)
        self.assertEqual(self.data()["posts"], [])

    def test_async_timeout_does_not_claim_success_or_transfer_root(self):
        self.update(pending=True)
        result = self.call("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("still pending", result.stderr)
        self.assertEqual(self.data()["posts"], ["QCLNEGF.jl"])
        self.assertEqual(self.git("remote", "get-url", "origin"), "https://github.com/AfonenkoA/qcl-negf.git")


if __name__ == "__main__":
    unittest.main()
