"""Single source of truth for all directory/file names and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# ── Environment Variables ──────────────────────────────────────────────

ENV_GMD_HOME = "GMD_HOME"
ENV_GMD_PROJECT = "GMD_PROJECT"
ENV_GMD_INSTALL_DIR = "GMD_INSTALL_DIR"
ENV_GMD_DEBUG = "GMD_DEBUG"
ENV_GMD_AUTONOMY = "GMD_AUTONOMY"

# ── File Names ─────────────────────────────────────────────────────────

STATE_MD = "STATE.md"
STATE_JSON = "state.json"
STATE_WRITE_INTENT = ".state-write-intent"
ROADMAP_MD = "ROADMAP.md"
CONFIG_JSON = "config.json"
CONVENTIONS_JSON = "conventions.json"

PLAN_PREFIX = "PLAN"
SUMMARY_PREFIX = "SUMMARY"
RESEARCH_MD = "RESEARCH.md"
RESEARCH_DIGEST_MD = "RESEARCH-DIGEST.md"
CONTINUE_HERE_MD = ".continue-here.md"

# ── Directory Names ────────────────────────────────────────────────────

GMD_DIR = ".gmd"
OBSERVABILITY_DIR = "observability"
SESSIONS_DIR = "sessions"
TRACES_DIR = "traces"
KNOWLEDGE_DIR = "knowledge"
PAPER_DIR = "paper"
SCRATCH_DIR = ".scratch"

# ── Git ────────────────────────────────────────────────────────────────

CHECKPOINT_TAG_PREFIX = "gmd-checkpoint"
COMMIT_PREFIX = "[gmd]"

# ── Autonomy Modes ─────────────────────────────────────────────────────

AUTONOMY_SUPERVISED = "supervised"
AUTONOMY_BALANCED = "balanced"
AUTONOMY_YOLO = "yolo"
VALID_AUTONOMY_MODES = {AUTONOMY_SUPERVISED, AUTONOMY_BALANCED, AUTONOMY_YOLO}

# ── Research Modes ─────────────────────────────────────────────────────

RESEARCH_EXPLORE = "explore"
RESEARCH_BALANCED = "balanced"
RESEARCH_EXPLOIT = "exploit"
RESEARCH_ADAPTIVE = "adaptive"
VALID_RESEARCH_MODES = {RESEARCH_EXPLORE, RESEARCH_BALANCED, RESEARCH_EXPLOIT, RESEARCH_ADAPTIVE}

# ── Model Tiers ────────────────────────────────────────────────────────

TIER_1 = "tier-1"  # Highest capability
TIER_2 = "tier-2"  # Balanced
TIER_3 = "tier-3"  # Fastest

# ── Verification Severity ──────────────────────────────────────────────

SEVERITY_CRITICAL = "CRITICAL"  # Blocks all downstream work
SEVERITY_MAJOR = "MAJOR"        # Must resolve before conclusions
SEVERITY_MINOR = "MINOR"        # Must resolve before publication
SEVERITY_NOTE = "NOTE"          # Informational

# ── Convention Lock Fields (Mathematics) ───────────────────────────────

CONVENTION_FIELDS = [
    "index_convention",           # Einstein summation, explicit sums, etc.
    "coordinate_system",          # Cartesian, polar, spherical, etc.
    "algebra_convention",         # Physicist vs mathematician normalization
    "function_space_notation",    # L^p, Sobolev, Schwartz, etc.
    "set_notation",               # Inclusion, membership, operations
    "proof_style",                # Direct, contradiction, induction framework
    "numbering_scheme",           # Theorem/lemma/proposition numbering
    "symbol_assignments",         # Reserved symbols for specific objects
    "category_convention",        # Category theory conventions (if applicable)
    "metric_norm_convention",     # Metric and norm notation
]

# ── Verification Checks ───────────────────────────────────────────────

VERIFICATION_CHECKS = [
    "logical_validity",           # Each step follows from previous
    "base_case_verification",     # Induction base cases explicitly checked
    "special_case_testing",       # Known solvable instances, boundary cases
    "counterexample_search",      # Systematic attempt to break claims
    "known_identity_matching",    # Results compared against known theorems
    "type_consistency",           # Objects have correct types throughout
    "convergence_verification",   # Series, limits, integrals justified
    "assumption_tracking",        # All hypotheses used, no circular reasoning
    "uniqueness_checking",        # When uniqueness claimed, verified
    "constructive_witness",       # Existence proofs produce constructions
    "literature_comparison",      # Results compared with published work
    "notation_consistency",       # Convention locks respected throughout
    "completeness",               # All cases handled, no missing branches
]


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved paths for a GMD project."""

    root: Path

    @property
    def gmd_dir(self) -> Path:
        return self.root / GMD_DIR

    @property
    def state_md(self) -> Path:
        return self.gmd_dir / STATE_MD

    @property
    def state_json(self) -> Path:
        return self.gmd_dir / STATE_JSON

    @property
    def state_write_intent(self) -> Path:
        return self.gmd_dir / STATE_WRITE_INTENT

    @property
    def roadmap_md(self) -> Path:
        return self.gmd_dir / ROADMAP_MD

    @property
    def config_json(self) -> Path:
        return self.gmd_dir / CONFIG_JSON

    @property
    def conventions_json(self) -> Path:
        return self.gmd_dir / CONVENTIONS_JSON

    @property
    def observability_dir(self) -> Path:
        return self.gmd_dir / OBSERVABILITY_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.observability_dir / SESSIONS_DIR

    @property
    def traces_dir(self) -> Path:
        return self.gmd_dir / TRACES_DIR

    @property
    def knowledge_dir(self) -> Path:
        return self.root / KNOWLEDGE_DIR

    @property
    def paper_dir(self) -> Path:
        return self.root / PAPER_DIR

    @property
    def scratch_dir(self) -> Path:
        return self.root / SCRATCH_DIR

    @property
    def continue_here(self) -> Path:
        return self.gmd_dir / CONTINUE_HERE_MD

    def phase_dir(self, phase: str) -> Path:
        return self.root / f"phase-{phase}"

    def plan_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{PLAN_PREFIX}-{plan_number}.md"

    def summary_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{SUMMARY_PREFIX}-{plan_number}.md"

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [
            self.gmd_dir,
            self.observability_dir,
            self.sessions_dir,
            self.traces_dir,
            self.knowledge_dir,
            self.scratch_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) looking for .gmd/ directory."""
    current = start or Path.cwd()
    while current != current.parent:
        if (current / GMD_DIR).is_dir():
            return current
        current = current.parent
    raise FileNotFoundError(
        f"No {GMD_DIR}/ directory found. Run 'gmd init' to create a project."
    )


def get_layout(start: Path | None = None) -> ProjectLayout:
    """Get the project layout, finding the root automatically."""
    env_project = os.environ.get(ENV_GMD_PROJECT)
    if env_project:
        return ProjectLayout(root=Path(env_project))
    return ProjectLayout(root=find_project_root(start))
