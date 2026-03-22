---
name: new-project
description: Initialize a new mathematics research project
---

<process>

## Initialize New Mathematics Research Project

### Step 1: Create project structure
Create the `.gmd/` directory and all required subdirectories:
- `.gmd/` — project state and config
- `.gmd/observability/sessions/` — session logs
- `.gmd/traces/` — execution traces
- `knowledge/` — research knowledge base
- `.scratch/` — temporary working files (gitignored)

### Step 2: Gather project information
Ask the user:
1. **Project name**: What is this research project about?
2. **Research question**: What specific mathematical question are you investigating?
3. **Domain**: Which area of mathematics? (algebra, analysis, topology, combinatorics, number theory, etc.)
4. **Model profile**: deep-theory (default), computational, exploratory, review, or paper-writing?
5. **Research mode**: explore, balanced (default), exploit, or adaptive?

### Step 3: Create initial ROADMAP.md
Based on the research question, create a phase breakdown:

```markdown
# [Project Name] — Roadmap

## Phase 1: Literature Survey
**Goal**: Identify known results, open problems, and standard techniques for [topic]

## Phase 2: Problem Specification
**Goal**: Precisely state the conjecture/problem and identify the proof strategy

## Phase 3: Main Results
**Goal**: Prove the main theorem(s)

## Phase 4: Verification
**Goal**: Independent verification of all proofs

## Phase 5: Paper Writing
**Goal**: Write publication-ready manuscript
```

Adjust phases based on the specific research question. Some projects need more phases (e.g., numerical computation phase), some need fewer.

### Step 4: Initialize state
Create STATE.md and state.json with:
- Project name and creation date
- Phase listing from ROADMAP
- Phase 1 set as active
- Research mode and autonomy mode

### Step 5: Initialize config
Create `.gmd/config.json` with user's choices.

### Step 6: Initialize git
If not already a git repo, initialize one. Add `.scratch/` to `.gitignore`.
Commit the initial project structure.

### Step 7: Convention prompting
Ask if the user wants to pre-set any conventions:
- Standard notation for the domain
- Proof style preferences
- Symbol assignments

Lock any conventions the user specifies.

### Step 8: Summary
Display:
- Project structure created
- Phases from roadmap
- Active conventions
- Next step: run `plan-phase` to begin Phase 1

</process>
