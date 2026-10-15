from __future__ import annotations

from dataclasses import asdict, dataclass
import difflib
from pathlib import Path
from typing import Any

from .risk import assess_path_risk
from .tools import RepoTools


@dataclass
class ChangeProposal:
    proposal_id: int
    path: str
    reason: str
    original_content: str
    original_exists: bool
    proposed_content: str
    diff: str
    risk: dict[str, str]
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ApprovalQueue:
    """Stages proposed file replacements and requires an explicit decision."""

    def __init__(self, tools: RepoTools) -> None:
        self.tools = tools
        self._proposals: dict[int, ChangeProposal] = {}
        self._next_id = 1

    def propose(self, path: str, proposed_content: str, reason: str = "") -> ChangeProposal:
        target = self.tools._safe(path)
        try:
            original = target.read_text(encoding="utf-8")
            original_exists = True
        except FileNotFoundError:
            original = ""
            original_exists = False

        diff = "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                proposed_content.splitlines(keepends=True),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
            )
        )
        proposal = ChangeProposal(
            proposal_id=self._next_id,
            path=path,
            reason=reason,
            original_content=original,
            original_exists=original_exists,
            proposed_content=proposed_content,
            diff=diff,
            risk=assess_path_risk(path),
        )
        self._proposals[proposal.proposal_id] = proposal
        self._next_id += 1
        return proposal

    def get(self, proposal_id: int) -> ChangeProposal:
        return self._proposals[proposal_id]

    def pending(self) -> list[ChangeProposal]:
        return [p for p in self._proposals.values() if p.status == "pending"]

    def approve(self, proposal_id: int) -> ChangeProposal:
        proposal = self.get(proposal_id)
        if proposal.status != "pending":
            raise ValueError(f"Proposal {proposal_id} is already {proposal.status}")
        target = self.tools._safe(proposal.path)
        if target.exists() != proposal.original_exists:
            raise ValueError("File changed since proposal; review a fresh diff")
        if proposal.original_exists and target.read_text(encoding="utf-8") != proposal.original_content:
            raise ValueError("File changed since proposal; review a fresh diff")
        self.tools.write_file(proposal.path, proposal.proposed_content)
        proposal.status = "approved"
        return proposal

    def reject(self, proposal_id: int) -> ChangeProposal:
        proposal = self.get(proposal_id)
        if proposal.status != "pending":
            raise ValueError(f"Proposal {proposal_id} is already {proposal.status}")
        proposal.status = "rejected"
        return proposal

