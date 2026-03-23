# Publishing Plan — Chromatic Number Paper & GPD Show & Tell

## Status: Pending — complete review/verification first

---

## Step 1: Review and Verify the Paper

Before publishing anything:
1. Run `/gmd:verify-work` in ~/Projects/chromatic-number-random-graphs/ (13-check verification)
2. Run `/gmd:review-paper` (once implemented — citation verification + 5-perspective referee panel)
3. Manually verify key citations against original papers:
   - Frieze 1990 (Discrete Math 81(2):171-175) — two-point concentration of α(G(n,p))
   - Grimmett-McDiarmid 1975 — greedy IS size bounds
   - Alon-Krivelevich 1997 — O(√(n/log n)) concentration width
4. Resolve C₀ constant inconsistency (paper says 3+o(1) in Remark 4.7, verification pinned C₀=2)

## Step 2: Create the Research Output Repo

Create a public repo for the full research trail:
```bash
cd ~/Projects/chromatic-number-random-graphs
gh repo create JesseRWeigel/chromatic-number-random-graphs --public --source=. --push \
  --description "Improved concentration of χ(G(n, n^{-1/2})) — produced by get-math-done"
```

This repo should contain everything: knowledge/, spec/, proofs/, paper/, .gmd/ state.
People can see the entire autonomous research process, not just the final paper.

## Step 3: Post Paper

### Option A: Zenodo (recommended — gives DOI, no endorsement needed)
- Upload PDF to https://zenodo.org
- Get a permanent DOI for citation
- Free, indexed by Google Scholar

### Option B: GitHub repo (already done if Step 2 is complete)
- The repo itself IS the publication
- More transparent than a bare PDF — shows full research trail

### Option C: arXiv (if endorsement available)
- Target: math.CO (Combinatorics)
- Requires endorsement from someone with arXiv posting rights in math.CO
- Best prestige, but blocked without endorsement

### Option D: viXra (no endorsement, lower prestige)
- Free, no endorsement needed
- Lower prestige than arXiv

### Option E: SSRN
- Free, no endorsement
- Primarily social sciences but accepts math

**Recommended approach**: GitHub repo (Step 2) + Zenodo (DOI) + mention in GPD Show & Tell.
If endorsement becomes available later, also post to arXiv.

## Step 4: Post in GMD Repo Discussions

Create a "Show & Tell" or "Research Output" discussion category in get-math-done:

**Title**: First test run: Improved chromatic number concentration for G(n, n^{-1/2})

**Body**: Summary of the research, link to the chromatic-number-random-graphs repo,
what the system did autonomously, what was caught by verification, what needs
human review. Include link to the paper (Zenodo DOI or repo).

## Step 5: Post in GPD Repo Discussions (Show & Tell)

**Title**: Get-X-Done: Adapting GPD's Architecture for 8 Research Domains (with first math paper)

**Body** (draft below):

---

We adapted GPD's architecture to create autonomous AI research copilots for 8 domains beyond physics. The first one — **get-math-done** — just completed its first end-to-end test run, producing a 9-page paper that improves a 1997 result by Noga Alon on chromatic number concentration.

### What we built

Eight open-source repos, all following GPD's three-layer architecture (Python core + MCP servers + agent/command markdown):

| Repo | Domain | Status |
|------|--------|--------|
| [get-math-done](https://github.com/JesseRWeigel/get-math-done) | Mathematics | **Tested** — first paper produced |
| [get-review-done](https://github.com/JesseRWeigel/get-review-done) | Systematic reviews / meta-analyses | Infrastructure complete |
| [get-legal-done](https://github.com/JesseRWeigel/get-legal-done) | Legal research / brief writing | Infrastructure complete |
| [get-quant-done](https://github.com/JesseRWeigel/get-quant-done) | Quantitative finance | Infrastructure complete |
| [get-engineering-done](https://github.com/JesseRWeigel/get-engineering-done) | Engineering analysis | Infrastructure complete |
| [get-chem-done](https://github.com/JesseRWeigel/get-chem-done) | Computational chemistry | Infrastructure complete |
| [get-bio-done](https://github.com/JesseRWeigel/get-bio-done) | Bioinformatics | Infrastructure complete |
| [get-policy-done](https://github.com/JesseRWeigel/get-policy-done) | Policy analysis | Infrastructure complete |

Each repo has: 6 MCP servers, 7 agents, 5-6 slash commands, domain-specific protocols, an LLM error catalog, a verification kernel, and an `npx` installer (e.g., `npx get-math-done --local`).

### The test run: chromatic number concentration

We ran get-math-done on this problem: *Can concentration of χ(G(n,p)) be improved at p = n^{-1/2}?*

The system autonomously:
- **Phase 1**: Surveyed 40+ years of literature across 8 tasks in 5 waves (parallel agents)
- **Phase 2**: Specified the theorem and proof strategy — the plan-checker caught a real error (confusing X_k with α(G) in Kim-Vu applicability) and forced a strategy revision
- **Phase 3**: Proved the greedy upper bound theorem — the plan-checker caught another error (a coupling argument that fails because conditioning on max IS correlates with all edges)
- **Phase 4**: Assembled the final result
- **Phase 5**: Generated a 9-page LaTeX paper with 14 references, reviewed by the referee agent

**Result**: χ(G(n, n^{-1/2})) is concentrated on O(n^{1/2}/ln²n) values w.h.p., improving Alon-Krivelevich (1997) by a factor of ln^{3/2}(n).

The full research trail (survey, specs, proofs, paper) is at: [chromatic-number-random-graphs](https://github.com/JesseRWeigel/chromatic-number-random-graphs)

### Transparency note

This paper has passed get-math-done's built-in verification (13-check framework, plan-checker error detection, referee review) but has **not yet been peer-reviewed by human mathematicians**. The citations need verification against original papers, and the constant analysis should be double-checked. We're publishing the full research trail so the community can inspect every step of the reasoning. AI-assisted research needs this kind of transparency.

### What GPD's architecture gave us

The key GPD patterns that made this work:
- **Convention locks** prevented notation drift across 5 phases
- **Plan-checker** caught 3 real mathematical errors before they propagated into proofs
- **Wave-based parallel execution** ran literature survey tasks concurrently
- **Verification kernel** with content-addressed verdicts confirmed proof correctness
- **Artifact recovery protocol** handled sandbox isolation (subagent file writes not persisting)

### What's next

The other 7 domains have complete infrastructure but haven't been tested on real problems yet. Each has 2-5 concrete research test items defined as GitHub issues. Contributors welcome — especially domain experts who can validate the protocols and error catalogs.

### Connection to GPD

This was inspired directly by GPD's success on physics research (including [our GW research using GPD](https://github.com/psi-oss/get-physics-done/discussions/24)). The architecture generalizes cleanly — about 60% of GPD's infrastructure is domain-agnostic. We replaced the physics-specific 40% (protocols, verification checks, convention locks, error catalog) with equivalents for each domain.

---

## GPD Feature Parity Gaps to Address

Commands/features GPD has that we should add to all get-X-done repos:
- `/gmd:review-paper` — standalone citation verification + referee panel (being built)
- Hypothesis branching (branch-hypothesis, compare-branches)
- arxiv-submission packaging
- Bibliographer agent (citation verification via INSPIRE/ADS/arXiv)
- Consistency checker agent (cross-phase convention drift)
- Notation coordinator agent (global notation audit)
- Debugger agent (numerical debugging and convergence)
- Health check command (gpd health --fix equivalent)
- Sync state command
- Pause/resume with .continue-here.md (command exists, needs testing)
- Statusline context percentage display (implemented)
- Update check hook
- Full adapter layer for Gemini CLI, Codex, OpenCode (currently Claude Code only)
