"""Every script is tested both ways: good input passes, bad input is caught.

Run: python3 -m unittest discover tests
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")


def run(script, *args, cwd, now=None):
    env = dict(os.environ)
    env.pop("OPS_CONFIG", None)
    if now:
        env["OPS_NOW"] = now
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                          cwd=cwd, env=env, capture_output=True, text=True)


class Workspace(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        shutil.copytree(os.path.join(ROOT, "templates", "ops"), os.path.join(self.dir, "ops"))
        shutil.copy(os.path.join(ROOT, "templates", "ops.config.json"), self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def path(self, *parts):
        return os.path.join(self.dir, *parts)


class DispatchTest(Workspace):
    def test_full_lifecycle(self):
        r = run("dispatch.py", "add", "--to", "content", "--title", "Fix the late brief", cwd=self.dir,
                now="2026-10-28T08:00:00Z")
        self.assertEqual(r.returncode, 0, r.stderr)
        task = r.stdout.strip()
        self.assertEqual(task, "D-20261028-01")
        self.assertEqual(run("dispatch.py", "ack", task, "--plan", "replay a week", cwd=self.dir).returncode, 0)
        done = run("dispatch.py", "done", task, "--root-cause", "clock skew", "--prevention", "test_clock",
                   "--sweep", "n/a: only one scheduler", "--verification", "ran twice on time",
                   "--cleanup", "removed tmp files", cwd=self.dir)
        self.assertEqual(done.returncode, 0, done.stderr)
        item = json.load(open(self.path("ops", "DISPATCH.json")))["items"][0]
        self.assertEqual(item["status"], "done")

    def test_done_refused_without_five_items(self):
        task = run("dispatch.py", "add", "--to", "content", "--title", "x", cwd=self.dir).stdout.strip()
        r = run("dispatch.py", "done", task, "--root-cause", "found it", cwd=self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("prevention", r.stderr)
        item = json.load(open(self.path("ops", "DISPATCH.json")))["items"][0]
        self.assertEqual(item["status"], "new")

    def test_overdue_flags_unacknowledged_and_late(self):
        run("dispatch.py", "add", "--to", "a", "--title", "never acked", cwd=self.dir, now="2026-10-01T00:00:00Z")
        t2 = run("dispatch.py", "add", "--to", "b", "--title", "acked but late", "--due-days", "2",
                 cwd=self.dir, now="2026-10-01T00:00:00Z").stdout.strip()
        run("dispatch.py", "ack", t2, "--plan", "soon", cwd=self.dir, now="2026-10-01T01:00:00Z")
        r = run("dispatch.py", "overdue", cwd=self.dir, now="2026-10-05T00:00:00Z")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not acknowledged", r.stdout)
        self.assertIn("past due", r.stdout)

    def test_overdue_clean_when_fresh(self):
        run("dispatch.py", "add", "--to", "a", "--title", "fresh", cwd=self.dir, now="2026-10-01T00:00:00Z")
        r = run("dispatch.py", "overdue", cwd=self.dir, now="2026-10-01T02:00:00Z")
        self.assertEqual(r.returncode, 0, r.stdout)


class HandoffTest(Workspace):
    GOOD = "Updated 2026-10-28 09:00\n" + "\n".join(
        ["## Done", "## In progress", "## Not done", "## Next", "## Blocked on", "## Branches",
         "## Uncommitted or unpushed"]) + "\n"

    def write(self, name, text):
        with open(self.path("ops", "handoff", name), "w") as f:
            f.write(text)

    def test_good_record_passes(self):
        self.write("a.md", self.GOOD)
        self.assertEqual(run("handoff_check.py", cwd=self.dir).returncode, 0)

    def test_missing_section_and_stamp_fail(self):
        self.write("a.md", "# no stamp\n## Done\n")
        r = run("handoff_check.py", cwd=self.dir)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Updated", r.stdout)
        self.assertIn("## Blocked on", r.stdout)

    def test_stale_record_fails(self):
        self.write("a.md", self.GOOD.replace("2026-10-28 09:00", "2020-01-01 09:00"))
        repo = self.path("repo")
        os.makedirs(repo)
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")
        subprocess.run(["git", "init", "-q", repo], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", "work"], check=True, env=env)
        r = run("handoff_check.py", "--repo", repo, cwd=self.dir)
        self.assertEqual(r.returncode, 1)
        self.assertIn("stale", r.stdout)


class ReconcileTest(Workspace):
    def log(self, *rows):
        with open(self.path("ops", "deliveries.jsonl"), "w") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")

    def test_on_time(self):
        self.log({"id": "morning-brief", "at": "2026-10-28T09:20:00Z"})
        r = run("reconcile.py", "--date", "2026-10-28", cwd=self.dir, now="2026-10-28T12:00:00Z")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("on time", r.stdout)

    def test_missing_and_late(self):
        self.log({"id": "weekly-report", "at": "2026-10-26T19:30:00Z"})
        r = run("reconcile.py", "--date", "2026-10-26", cwd=self.dir, now="2026-10-27T00:00:00Z")
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing", r.stdout)   # morning brief never came
        self.assertIn("late", r.stdout)      # weekly report came after its grace window

    def test_not_due_yet_is_not_missing(self):
        self.log()
        r = run("reconcile.py", "--date", "2026-10-28", cwd=self.dir, now="2026-10-28T08:00:00Z")
        self.assertEqual(r.returncode, 0)
        self.assertIn("not due yet", r.stdout)

    def test_tomorrows_early_run_is_not_counted_today(self):
        self.log({"id": "morning-brief", "at": "2026-10-29T08:30:00Z"})
        r = run("reconcile.py", "--date", "2026-10-28", cwd=self.dir, now="2026-10-29T10:00:00Z")
        self.assertIn("missing", r.stdout)


class RulesTest(Workspace):
    def test_template_registry_is_alive(self):
        cfg = json.load(open(self.path("ops.config.json")))
        cfg["rules_root"] = ROOT
        json.dump(cfg, open(self.path("ops.config.json"), "w"))
        r = run("rules_check.py", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_dead_enforcer_is_reported(self):
        reg = {"rules": [{"id": "X-1", "rule": "no broken links", "tier": "gate",
                          "enforced_by": "gone.py", "marker": "check"}]}
        json.dump(reg, open(self.path("ops", "RULES-REGISTRY.json"), "w"))
        r = run("rules_check.py", cwd=self.dir)
        self.assertEqual(r.returncode, 1)
        self.assertIn("X-1", r.stdout)

    def test_marker_removed_is_reported(self):
        with open(self.path("enforcer.py"), "w") as f:
            f.write("# rewritten, the check is gone\n")
        reg = {"rules": [{"id": "X-2", "rule": "r", "tier": "scheduled", "enforced_by": "enforcer.py",
                          "marker": "def check_links"}]}
        json.dump(reg, open(self.path("ops", "RULES-REGISTRY.json"), "w"))
        self.assertEqual(run("rules_check.py", cwd=self.dir).returncode, 1)


if __name__ == "__main__":
    unittest.main()
