"""Convention lock management for mathematical notation consistency.

Ensures notation doesn't drift across phases of a research project.
Adapted from GPD's conventions.py for mathematics.
"""

from __future__ import annotations

from typing import Any

from .constants import CONVENTION_FIELDS
from .state import StateEngine, ConventionLock


# ── Convention Field Descriptions ──────────────────────────────────────

CONVENTION_DESCRIPTIONS: dict[str, str] = {
    "index_convention": (
        "How indices are handled: Einstein summation convention (implicit sum "
        "over repeated indices), explicit summation signs, or mixed. Also covers "
        "index placement (upper/lower) and range conventions."
    ),
    "coordinate_system": (
        "Primary coordinate system: Cartesian (x,y,z), polar (r,θ), "
        "spherical (r,θ,φ — physics or math convention for θ/φ ordering), "
        "or domain-specific coordinates."
    ),
    "algebra_convention": (
        "Normalization conventions for algebraic structures. Examples: "
        "physicist vs mathematician Lie algebra normalization (factor of i), "
        "Clifford algebra sign convention, quaternion multiplication order."
    ),
    "function_space_notation": (
        "Notation for function spaces: L^p vs ℒ^p, Sobolev spaces (H^k vs W^{k,p}), "
        "Schwartz space notation, distribution space notation."
    ),
    "set_notation": (
        "Set-theoretic notation: ⊂ means proper or improper subset, "
        "∅ vs {} for empty set, ℕ includes 0 or not, "
        "interval notation [a,b) vs [a,b[."
    ),
    "proof_style": (
        "Primary proof strategy/style: direct proof, proof by contradiction, "
        "proof by contrapositive, structural induction variant (strong, transfinite), "
        "constructive vs classical."
    ),
    "numbering_scheme": (
        "How theorems/lemmas/propositions are numbered: sequential within "
        "sections (Theorem 2.1, 2.2), sequential global (Theorem 1, 2, 3), "
        "named (Banach Fixed Point Theorem)."
    ),
    "symbol_assignments": (
        "Reserved symbols: e.g., ε always for 'small positive number', "
        "n for natural number index, G for group, R for ring/real numbers, "
        "φ for homomorphism vs Euler totient."
    ),
    "category_convention": (
        "Category theory notation (if used): Set/SET/𝐒𝐞𝐭 for category of sets, "
        "Hom vs hom vs Mor for morphism sets, composition order (f∘g = f then g "
        "or g then f), natural transformation notation."
    ),
    "metric_norm_convention": (
        "Metric and norm notation: ||·|| vs ‖·‖, subscript placement for "
        "specific norms (||x||_p), inner product notation ⟨·,·⟩ vs (·,·), "
        "linearity convention (linear in first or second argument)."
    ),
}

# ── Convention Validation ──────────────────────────────────────────────

# Common valid values for quick validation
CONVENTION_EXAMPLES: dict[str, list[str]] = {
    "index_convention": [
        "Einstein summation",
        "Explicit sums",
        "Mixed (Einstein for tensors, explicit for finite sums)",
    ],
    "coordinate_system": [
        "Cartesian (x,y,z)",
        "Polar (r,θ)",
        "Spherical — physics (r,θ,φ: θ=polar, φ=azimuthal)",
        "Spherical — math (r,θ,φ: θ=azimuthal, φ=polar)",
    ],
    "set_notation": [
        "⊂ means proper subset, ⊆ means subset",
        "⊂ means subset (proper or improper)",
        "ℕ includes 0",
        "ℕ = {1,2,3,...} (excludes 0)",
    ],
    "metric_norm_convention": [
        "⟨·,·⟩ linear in first argument (physics)",
        "⟨·,·⟩ linear in second argument (math)",
    ],
}


def get_field_description(field: str) -> str:
    """Get the description for a convention field."""
    return CONVENTION_DESCRIPTIONS.get(field, f"Convention field: {field}")


def get_field_examples(field: str) -> list[str]:
    """Get example values for a convention field."""
    return CONVENTION_EXAMPLES.get(field, [])


def list_all_fields() -> list[dict[str, Any]]:
    """List all convention fields with descriptions and examples."""
    return [
        {
            "field": f,
            "description": get_field_description(f),
            "examples": get_field_examples(f),
        }
        for f in CONVENTION_FIELDS
    ]


def check_conventions(engine: StateEngine) -> dict[str, Any]:
    """Check which conventions are locked and which are missing.

    Returns a report dict with locked, unlocked, and coverage stats.
    """
    state = engine.load()
    locked = {}
    unlocked = []

    for field in CONVENTION_FIELDS:
        if field in state.conventions:
            locked[field] = {
                "value": state.conventions[field].value,
                "locked_by": state.conventions[field].locked_by,
                "rationale": state.conventions[field].rationale,
            }
        else:
            unlocked.append(field)

    return {
        "locked": locked,
        "unlocked": unlocked,
        "coverage": f"{len(locked)}/{len(CONVENTION_FIELDS)}",
        "coverage_pct": round(100 * len(locked) / len(CONVENTION_FIELDS), 1)
        if CONVENTION_FIELDS
        else 100.0,
    }


def diff_conventions(
    engine: StateEngine,
    proposed: dict[str, str],
) -> dict[str, Any]:
    """Compare proposed convention values against current locks.

    Returns conflicts, new fields, and matching fields.
    """
    state = engine.load()
    conflicts = {}
    new_fields = {}
    matching = {}

    for field, proposed_value in proposed.items():
        if field in state.conventions:
            current = state.conventions[field].value
            if current != proposed_value:
                conflicts[field] = {
                    "current": current,
                    "proposed": proposed_value,
                }
            else:
                matching[field] = current
        else:
            new_fields[field] = proposed_value

    return {
        "conflicts": conflicts,
        "new_fields": new_fields,
        "matching": matching,
        "has_conflicts": bool(conflicts),
    }
