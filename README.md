# Get Math Done

> An AI copilot for autonomous mathematics research — from conjecture to proof to publication.

**Inspired by [Get Physics Done](https://github.com/psi-oss/get-physics-done)** — the open-source AI copilot that autonomously conducts physics research, including training models and generating academic papers. Get Math Done adapts GPD's battle-tested architecture (dual-write state engine, wave-based parallel execution, content-addressed verification, git ratcheting) for the domain of pure and applied mathematics.

## Vision

Mathematics demands absolute rigor — a single sign error in a proof invalidates everything downstream. LLMs are increasingly capable at mathematical reasoning, but they fail in predictable ways: off-by-one errors in induction, false commutativity assumptions, incorrect convergence radius claims, and subtle sign errors in combinatorial arguments.

Get Math Done wraps LLM capabilities in a verification-first framework that:
- **Locks notation** across proof phases (index conventions, coordinate systems, algebra conventions)
- **Verifies proofs** through multi-pass checking: logical validity, special case testing, counterexample search, known identity matching
- **Decomposes research** into phases with clear deliverables: literature survey → conjecture formation → proof strategy → proof execution → verification → paper writing
- **Recovers from failures** through git ratcheting, targeted gap-closure, and failure-specific routing to specialist agents

## Architecture

Adapted from GPD's three-layer design:

### Layer 1 — Core Library (Python)
Pure stdlib + Pydantic. State management, phase lifecycle, git operations, convention locks, verification kernel.

### Layer 2 — MCP Servers
- `gmd-state` — Project state queries
- `gmd-conventions` — Mathematical notation lock management
- `gmd-protocols` — Domain-specific methodology protocols (algebra, analysis, topology, combinatorics, number theory, etc.)
- `gmd-patterns` — Cross-project learned error patterns
- `gmd-verification` — Proof verification checks
- `gmd-errors` — Known LLM math failure modes

### Layer 3 — Agents & Commands
Markdown-based specialist agents:
- `gmd-planner` — Task decomposition and dependency planning
- `gmd-executor` — Primary proof/computation execution
- `gmd-verifier` — Post-hoc proof verification (logical validity, special cases, counterexamples)
- `gmd-plan-checker` — Pre-execution feasibility checking
- `gmd-researcher` — Literature survey and known results discovery
- `gmd-paper-writer` — LaTeX manuscript generation
- `gmd-referee` — Multi-perspective peer review panel

## Convention Lock Fields

Mathematics-specific notation consistency across phases:
1. Index convention (Einstein summation, explicit sums, etc.)
2. Coordinate system
3. Algebra convention (physicist vs mathematician normalization)
4. Function space notation (L^p, Sobolev, etc.)
5. Set notation (inclusion, membership, operations)
6. Proof style (direct, contradiction, induction framework)
7. Numbering scheme (theorems, lemmas, propositions)
8. Symbol assignments (reserved symbols for specific objects)
9. Category theory conventions (if applicable)
10. Metric/norm convention

## Verification Framework

Mathematical-specific verification checks:
1. **Logical validity** — each step follows from previous, no gaps
2. **Base case verification** — induction base cases explicitly checked
3. **Special case testing** — known solvable instances, boundary cases
4. **Counterexample search** — systematic attempt to break claims
5. **Known identity matching** — results compared against known theorems/identities
6. **Dimensional/type consistency** — objects have correct types throughout
7. **Convergence verification** — series, limits, integrals properly justified
8. **Assumption tracking** — all hypotheses used, no circular reasoning
9. **Uniqueness checking** — when uniqueness claimed, verified
10. **Constructive witness** — existence proofs produce explicit constructions where possible
11. **Literature comparison** — results compared with published work
12. **Notation consistency** — convention locks respected throughout
13. **Completeness** — all cases handled, no missing branches

## Status

**Early development** — Building core infrastructure. Contributions welcome!

## Relationship to GPD

This project reuses ~60% of GPD's domain-agnostic infrastructure (state engine, phase lifecycle, git ratcheting, wave execution, observability, MCP server framework) and replaces the physics-specific 40% (protocols, verification checks, convention locks, error catalog) with mathematics equivalents.

We plan to showcase this in the [GPD Discussion Show & Tell](https://github.com/psi-oss/get-physics-done/discussions) once operational.

## Getting Started

```bash
# Coming soon
npx get-math-done
```

## Contributing

We're looking for contributors with:
- Mathematics research experience (any subfield)
- Experience with AI-assisted theorem proving
- Familiarity with GPD's architecture
- LaTeX and academic publishing experience

See the [Issues](../../issues) for specific tasks that need help.

## License

MIT
