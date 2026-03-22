"""Content-addressed verification kernel.

Runs predicates over evidence registries and produces SHA-256 verdicts.
Adapted from GPD's kernel.py for mathematical proof verification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .constants import VERIFICATION_CHECKS, SEVERITY_CRITICAL, SEVERITY_MAJOR, SEVERITY_MINOR, SEVERITY_NOTE


class Severity(str, Enum):
    CRITICAL = SEVERITY_CRITICAL
    MAJOR = SEVERITY_MAJOR
    MINOR = SEVERITY_MINOR
    NOTE = SEVERITY_NOTE


@dataclass
class CheckResult:
    """Result of a single verification check."""

    check_id: str
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    severity: Severity
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    """Complete verification verdict with content-addressed hashes."""

    registry_hash: str
    predicates_hash: str
    verdict_hash: str
    overall: str  # PASS | FAIL | PARTIAL
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    results: dict[str, CheckResult] = field(default_factory=dict)
    summary: str = ""

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.CRITICAL
        ]

    @property
    def major_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.MAJOR
        ]

    @property
    def all_failures(self) -> list[CheckResult]:
        return [r for r in self.results.values() if r.status == "FAIL"]

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "FAIL")

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_hash": self.registry_hash,
            "predicates_hash": self.predicates_hash,
            "verdict_hash": self.verdict_hash,
            "overall": self.overall,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "results": {
                k: {
                    "check_id": v.check_id,
                    "name": v.name,
                    "status": v.status,
                    "severity": v.severity.value,
                    "message": v.message,
                    "evidence": v.evidence,
                    "suggestions": v.suggestions,
                }
                for k, v in self.results.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ── Predicate Type ─────────────────────────────────────────────────────

# A predicate takes an evidence registry and returns a CheckResult
Predicate = Callable[[dict[str, Any]], CheckResult]


# ── Built-in Math Predicates ──────────────────────────────────────────

def check_logical_validity(evidence: dict[str, Any]) -> CheckResult:
    """Check that each proof step follows from the previous."""
    proof_steps = evidence.get("proof_steps", [])
    gaps = evidence.get("logical_gaps", [])

    if not proof_steps:
        return CheckResult(
            check_id="logical_validity",
            name="Logical Validity",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No proof steps provided for verification.",
        )

    if gaps:
        return CheckResult(
            check_id="logical_validity",
            name="Logical Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(gaps)} logical gap(s) in proof.",
            evidence={"gaps": gaps},
            suggestions=[
                f"Address gap: {g}" for g in gaps[:5]
            ],
        )

    return CheckResult(
        check_id="logical_validity",
        name="Logical Validity",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(proof_steps)} proof steps verified.",
    )


def check_base_case(evidence: dict[str, Any]) -> CheckResult:
    """Check induction base cases are explicitly verified."""
    uses_induction = evidence.get("uses_induction", False)
    base_cases = evidence.get("base_cases", [])
    base_cases_verified = evidence.get("base_cases_verified", [])

    if not uses_induction:
        return CheckResult(
            check_id="base_case_verification",
            name="Base Case Verification",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="Proof does not use induction.",
        )

    if not base_cases:
        return CheckResult(
            check_id="base_case_verification",
            name="Base Case Verification",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="Proof uses induction but no base cases identified.",
            suggestions=["Identify and explicitly verify all base cases."],
        )

    unverified = [b for b in base_cases if b not in base_cases_verified]
    if unverified:
        return CheckResult(
            check_id="base_case_verification",
            name="Base Case Verification",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(unverified)} base case(s) not verified.",
            evidence={"unverified": unverified},
        )

    return CheckResult(
        check_id="base_case_verification",
        name="Base Case Verification",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(base_cases)} base case(s) verified.",
    )


def check_special_cases(evidence: dict[str, Any]) -> CheckResult:
    """Check known solvable instances and boundary cases."""
    special_cases = evidence.get("special_cases", [])
    special_cases_checked = evidence.get("special_cases_checked", [])

    if not special_cases:
        return CheckResult(
            check_id="special_case_testing",
            name="Special Case Testing",
            status="WARN",
            severity=Severity.MAJOR,
            message="No special cases identified for testing.",
            suggestions=[
                "Identify known solvable instances to test against.",
                "Check boundary/degenerate cases (n=0, n=1, empty set, etc.).",
            ],
        )

    unchecked = [s for s in special_cases if s not in special_cases_checked]
    if unchecked:
        return CheckResult(
            check_id="special_case_testing",
            name="Special Case Testing",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(unchecked)} special case(s) not checked.",
            evidence={"unchecked": unchecked},
        )

    return CheckResult(
        check_id="special_case_testing",
        name="Special Case Testing",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(special_cases)} special case(s) verified.",
    )


def check_counterexamples(evidence: dict[str, Any]) -> CheckResult:
    """Check systematic counterexample search was conducted."""
    counterexample_search = evidence.get("counterexample_search_conducted", False)
    counterexamples_found = evidence.get("counterexamples_found", [])

    if not counterexample_search:
        return CheckResult(
            check_id="counterexample_search",
            name="Counterexample Search",
            status="WARN",
            severity=Severity.MAJOR,
            message="No systematic counterexample search conducted.",
            suggestions=[
                "Attempt to construct counterexamples to main claims.",
                "Test with random/adversarial inputs where applicable.",
            ],
        )

    if counterexamples_found:
        return CheckResult(
            check_id="counterexample_search",
            name="Counterexample Search",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(counterexamples_found)} counterexample(s)!",
            evidence={"counterexamples": counterexamples_found},
            suggestions=["Review proof — counterexamples indicate an error."],
        )

    return CheckResult(
        check_id="counterexample_search",
        name="Counterexample Search",
        status="PASS",
        severity=Severity.MAJOR,
        message="Systematic counterexample search found no issues.",
    )


def check_known_identities(evidence: dict[str, Any]) -> CheckResult:
    """Check results against known theorems and identities."""
    identities_checked = evidence.get("known_identities_checked", [])
    identity_mismatches = evidence.get("identity_mismatches", [])

    if not identities_checked:
        return CheckResult(
            check_id="known_identity_matching",
            name="Known Identity Matching",
            status="WARN",
            severity=Severity.MAJOR,
            message="No known identities checked against.",
            suggestions=["Compare results with established theorems in the area."],
        )

    if identity_mismatches:
        return CheckResult(
            check_id="known_identity_matching",
            name="Known Identity Matching",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Results disagree with {len(identity_mismatches)} known identity/theorem(s).",
            evidence={"mismatches": identity_mismatches},
        )

    return CheckResult(
        check_id="known_identity_matching",
        name="Known Identity Matching",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Consistent with {len(identities_checked)} known identity/theorem(s).",
    )


def check_type_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check objects have correct mathematical types throughout."""
    type_errors = evidence.get("type_errors", [])

    if type_errors:
        return CheckResult(
            check_id="type_consistency",
            name="Type Consistency",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(type_errors)} type inconsistency/ies.",
            evidence={"errors": type_errors},
        )

    return CheckResult(
        check_id="type_consistency",
        name="Type Consistency",
        status="PASS",
        severity=Severity.CRITICAL,
        message="All mathematical objects have consistent types.",
    )


def check_convergence(evidence: dict[str, Any]) -> CheckResult:
    """Check series, limits, and integrals are properly justified."""
    convergence_claims = evidence.get("convergence_claims", [])
    convergence_justified = evidence.get("convergence_justified", [])

    if not convergence_claims:
        return CheckResult(
            check_id="convergence_verification",
            name="Convergence Verification",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No convergence claims to verify.",
        )

    unjustified = [c for c in convergence_claims if c not in convergence_justified]
    if unjustified:
        return CheckResult(
            check_id="convergence_verification",
            name="Convergence Verification",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(unjustified)} convergence claim(s) not justified.",
            evidence={"unjustified": unjustified},
        )

    return CheckResult(
        check_id="convergence_verification",
        name="Convergence Verification",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(convergence_claims)} convergence claims justified.",
    )


def check_assumptions(evidence: dict[str, Any]) -> CheckResult:
    """Check all hypotheses used, no circular reasoning."""
    assumptions_stated = evidence.get("assumptions_stated", [])
    assumptions_used = evidence.get("assumptions_used", [])
    circular_deps = evidence.get("circular_dependencies", [])

    if circular_deps:
        return CheckResult(
            check_id="assumption_tracking",
            name="Assumption Tracking",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="Circular reasoning detected.",
            evidence={"circular": circular_deps},
        )

    unused = [a for a in assumptions_stated if a not in assumptions_used]
    if unused:
        return CheckResult(
            check_id="assumption_tracking",
            name="Assumption Tracking",
            status="WARN",
            severity=Severity.MINOR,
            message=f"{len(unused)} stated assumption(s) not used in proof.",
            evidence={"unused": unused},
            suggestions=["Remove unnecessary assumptions or verify they're needed."],
        )

    return CheckResult(
        check_id="assumption_tracking",
        name="Assumption Tracking",
        status="PASS",
        severity=Severity.MAJOR,
        message="All assumptions tracked, no circular reasoning.",
    )


def check_notation_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check convention locks respected throughout."""
    notation_violations = evidence.get("notation_violations", [])
    conventions_checked = evidence.get("conventions_checked", 0)

    if notation_violations:
        return CheckResult(
            check_id="notation_consistency",
            name="Notation Consistency",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"{len(notation_violations)} notation violation(s) found.",
            evidence={"violations": notation_violations},
        )

    return CheckResult(
        check_id="notation_consistency",
        name="Notation Consistency",
        status="PASS",
        severity=Severity.MINOR,
        message=f"Notation consistent across {conventions_checked} convention(s).",
    )


def check_completeness(evidence: dict[str, Any]) -> CheckResult:
    """Check all cases handled, no missing branches."""
    missing_cases = evidence.get("missing_cases", [])
    total_cases = evidence.get("total_cases", 0)

    if missing_cases:
        return CheckResult(
            check_id="completeness",
            name="Completeness",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(missing_cases)} case(s) not handled.",
            evidence={"missing": missing_cases},
        )

    if total_cases == 0:
        return CheckResult(
            check_id="completeness",
            name="Completeness",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No case analysis to verify.",
        )

    return CheckResult(
        check_id="completeness",
        name="Completeness",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {total_cases} case(s) handled.",
    )


# ── Default predicate registry ─────────────────────────────────────────

DEFAULT_PREDICATES: dict[str, Predicate] = {
    "logical_validity": check_logical_validity,
    "base_case_verification": check_base_case,
    "special_case_testing": check_special_cases,
    "counterexample_search": check_counterexamples,
    "known_identity_matching": check_known_identities,
    "type_consistency": check_type_consistency,
    "convergence_verification": check_convergence,
    "assumption_tracking": check_assumptions,
    "notation_consistency": check_notation_consistency,
    "completeness": check_completeness,
}


# ── Verification Kernel ────────────────────────────────────────────────

class VerificationKernel:
    """Content-addressed verification kernel.

    Runs predicates over evidence registries and produces
    SHA-256 verdicts for reproducibility and tamper-evidence.
    """

    def __init__(self, predicates: dict[str, Predicate] | None = None):
        self.predicates = predicates or dict(DEFAULT_PREDICATES)

    def _hash(self, data: str) -> str:
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def verify(self, evidence: dict[str, Any]) -> Verdict:
        """Run all predicates against evidence and produce a verdict."""
        # Hash inputs
        evidence_json = json.dumps(evidence, sort_keys=True, default=str)
        registry_hash = self._hash(evidence_json)

        predicate_names = json.dumps(sorted(self.predicates.keys()))
        predicates_hash = self._hash(predicate_names)

        # Run predicates
        results: dict[str, CheckResult] = {}
        for check_id, predicate in self.predicates.items():
            try:
                result = predicate(evidence)
                results[check_id] = result
            except Exception as e:
                results[check_id] = CheckResult(
                    check_id=check_id,
                    name=check_id.replace("_", " ").title(),
                    status="FAIL",
                    severity=Severity.MAJOR,
                    message=f"Predicate raised exception: {e}",
                )

        # Determine overall status
        has_critical_fail = any(
            r.status == "FAIL" and r.severity == Severity.CRITICAL
            for r in results.values()
        )
        has_major_fail = any(
            r.status == "FAIL" and r.severity == Severity.MAJOR
            for r in results.values()
        )

        if has_critical_fail:
            overall = "FAIL"
        elif has_major_fail:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        # Hash the results for tamper-evidence
        results_json = json.dumps(
            {k: v.message for k, v in results.items()},
            sort_keys=True,
        )
        verdict_hash = self._hash(
            f"{registry_hash}:{predicates_hash}:{results_json}"
        )

        # Build summary
        pass_count = sum(1 for r in results.values() if r.status == "PASS")
        fail_count = sum(1 for r in results.values() if r.status == "FAIL")
        skip_count = sum(1 for r in results.values() if r.status == "SKIP")
        warn_count = sum(1 for r in results.values() if r.status == "WARN")

        summary = (
            f"{overall}: {pass_count} passed, {fail_count} failed, "
            f"{warn_count} warnings, {skip_count} skipped "
            f"out of {len(results)} checks."
        )

        return Verdict(
            registry_hash=registry_hash,
            predicates_hash=predicates_hash,
            verdict_hash=verdict_hash,
            overall=overall,
            results=results,
            summary=summary,
        )
