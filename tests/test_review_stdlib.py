"""Dependency-free approval checks against the real RepoGuard implementation.

Run from the repo root:
PYTHONPATH=src python -m unittest discover -s tests -p test_review_stdlib.py -v
This focused fallback does not replace the full pytest suite.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from repoguard.review import ApprovalQueue
from repoguard.tools import RepoTools


class ApprovalQueueRegressionTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory(prefix="repoguard-review-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.queue = ApprovalQueue(RepoTools(self.root))

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def assert_stale(self, proposal):
        with self.assertRaisesRegex(ValueError, "File changed since proposal"):
            self.queue.approve(proposal.proposal_id)
        self.assertEqual(self.queue.get(proposal.proposal_id).status, "pending")
        self.assertIn(proposal, self.queue.pending())

    def test_preview_does_not_write_and_fresh_approval_applies(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 2\n", "Fictional update")
        self.assertIn("-value = 1", proposal.diff)
        self.assertIn("+value = 2", proposal.diff)
        self.assertEqual(target.read_text(), "value = 1\n")
        self.queue.approve(proposal.proposal_id)
        self.assertEqual(target.read_text(), "value = 2\n")
        self.assertEqual(proposal.status, "approved")
        self.assertEqual(self.queue.pending(), [])

    def test_rejection_preserves_original_file(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 9\n")
        self.queue.reject(proposal.proposal_id)
        self.assertEqual(target.read_text(), "value = 1\n")
        self.assertEqual(proposal.status, "rejected")
        self.assertEqual(self.queue.pending(), [])

    def test_same_length_newer_edit_is_preserved(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 2\n")
        target.write_text("value = 3\n", encoding="utf-8")
        self.assert_stale(proposal)
        self.assertEqual(target.read_text(), "value = 3\n")

    def test_new_file_at_proposed_path_is_preserved(self):
        proposal = self.queue.propose("new.py", "value = 2\n")
        target = self.write("new.py", "value = 3\n")
        self.assert_stale(proposal)
        self.assertEqual(target.read_text(), "value = 3\n")

    def test_even_an_empty_new_file_invalidates_creation_proposal(self):
        proposal = self.queue.propose("new.py", "value = 2\n")
        target = self.write("new.py", "")
        self.assert_stale(proposal)
        self.assertTrue(target.exists())
        self.assertEqual(target.read_bytes(), b"")

    def test_deleted_target_is_not_recreated_by_old_proposal(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 2\n")
        target.unlink()  # Only this test's fictional temporary file.
        self.assert_stale(proposal)
        self.assertFalse(target.exists())

    def test_edit_after_character_30000_is_not_truncated_away(self):
        prefix = "# fictional padding\n" * 2000
        self.assertGreater(len(prefix), 30000)
        target = self.write("large.py", prefix + "value = 1\n")
        proposal = self.queue.propose("large.py", prefix + "value = 2\n")
        newer = prefix + "value = 3\n"
        target.write_text(newer, encoding="utf-8")
        self.assert_stale(proposal)
        self.assertEqual(target.read_text(), newer)

    def test_two_proposals_cannot_overwrite_each_others_approved_change(self):
        target = self.write("app.py", "value = 1\n")
        first = self.queue.propose("app.py", "value = 2\n")
        second = self.queue.propose("app.py", "value = 3\n")
        self.queue.approve(first.proposal_id)
        self.assert_stale(second)
        self.assertEqual(target.read_text(), "value = 2\n")

    def test_fresh_proposal_after_stale_failure_can_be_approved(self):
        target = self.write("app.py", "value = 1\n")
        stale = self.queue.propose("app.py", "value = 2\n")
        target.write_text("value = 3\n", encoding="utf-8")
        self.assert_stale(stale)
        self.queue.reject(stale.proposal_id)
        fresh = self.queue.propose("app.py", "value = 4\n")
        self.assertIn("-value = 3", fresh.diff)
        self.queue.approve(fresh.proposal_id)
        self.assertEqual(target.read_text(), "value = 4\n")

    def test_new_file_can_be_created_after_fresh_review(self):
        proposal = self.queue.propose("nested/new.py", "value = 2\n")
        self.assertFalse((self.root / "nested").exists())
        self.queue.approve(proposal.proposal_id)
        self.assertEqual((self.root / "nested/new.py").read_text(), "value = 2\n")

    def test_approved_proposal_cannot_be_replayed_after_another_edit(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 2\n")
        self.queue.approve(proposal.proposal_id)
        target.write_text("value = 3\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already approved"):
            self.queue.approve(proposal.proposal_id)
        self.assertEqual(target.read_text(), "value = 3\n")

    def test_rejected_proposal_cannot_be_approved_later(self):
        target = self.write("app.py", "value = 1\n")
        proposal = self.queue.propose("app.py", "value = 2\n")
        self.queue.reject(proposal.proposal_id)
        with self.assertRaisesRegex(ValueError, "already rejected"):
            self.queue.approve(proposal.proposal_id)
        self.assertEqual(target.read_text(), "value = 1\n")


if __name__ == "__main__":
    unittest.main()
