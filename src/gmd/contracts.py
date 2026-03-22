"""Research contracts — Pydantic models for claims, deliverables, and acceptance tests.

Adapted from GPD's contracts.py for mathematics research.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class Claim(BaseModel):
    """A mathematical claim to be proved or verified."""

    id: str
    statement: str
    claim_type: str = "theorem"  # theorem | lemma | proposition | corollary | conjecture
    assumptions: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)  # Other claim IDs
    status: str = "unproven"  # unproven | proved | disproved | partial


class Deliverable(BaseModel):
    """An expected output artifact from a phase/plan."""

    id: str
    description: str
    artifact_type: str  # proof | computation | figure | table | manuscript_section
    file_path: str = ""
    acceptance_tests: list[str] = Field(default_factory=list)
    status: str = "pending"  # pending | delivered | verified | rejected


class AcceptanceTest(BaseModel):
    """A concrete test for a deliverable."""

    id: str
    description: str
    test_type: str  # existence | content | verification | consistency
    predicate: str = ""  # Human-readable predicate
    status: str = "pending"  # pending | passed | failed


class ForbiddenProxy(BaseModel):
    """Something that must NOT be used as evidence of completion.

    Prevents agents from claiming success based on superficial signals.
    """

    description: str
    reason: str


class ResearchContract(BaseModel):
    """A complete research contract for a phase or plan.

    Defines what must be achieved, how to verify it, and what NOT to accept.
    """

    phase_id: str
    plan_id: str = ""
    goal: str

    claims: list[Claim] = Field(default_factory=list)
    deliverables: list[Deliverable] = Field(default_factory=list)
    acceptance_tests: list[AcceptanceTest] = Field(default_factory=list)

    forbidden_proxies: list[ForbiddenProxy] = Field(
        default_factory=lambda: [
            ForbiddenProxy(
                description="Agent stating 'proof is complete' without written proof",
                reason="Written proof must exist on disk and pass verification.",
            ),
            ForbiddenProxy(
                description="Proof by appeal to authority without derivation",
                reason="'This follows from [Author]' is not a proof step.",
            ),
            ForbiddenProxy(
                description="Computational output without convergence evidence",
                reason="Numerical results must include convergence analysis.",
            ),
            ForbiddenProxy(
                description="Proof sketch presented as complete proof",
                reason="All steps must be fully justified, not sketched.",
            ),
        ]
    )

    def all_claims_resolved(self) -> bool:
        return all(c.status in ("proved", "disproved") for c in self.claims)

    def all_deliverables_verified(self) -> bool:
        return all(d.status == "verified" for d in self.deliverables)

    def all_tests_passed(self) -> bool:
        return all(t.status == "passed" for t in self.acceptance_tests)


class AgentReturn(BaseModel):
    """Structured return envelope from subagents.

    Every subagent MUST produce this in their SUMMARY.md.
    The orchestrator uses this — not prose — to determine success.
    """

    status: str  # completed | checkpoint | blocked | failed
    files_written: list[str] = Field(default_factory=list)
    files_modified: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    claims_proved: list[str] = Field(default_factory=list)  # Claim IDs
    conventions_proposed: dict[str, str] = Field(default_factory=dict)
    verification_evidence: dict[str, Any] = Field(default_factory=dict)
