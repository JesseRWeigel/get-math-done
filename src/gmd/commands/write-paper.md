---
name: write-paper
description: Generate a publication-ready mathematical manuscript
---

<process>

## Write Paper

### Overview
Transform completed research into a LaTeX manuscript ready for journal submission.

### Step 1: Paper Readiness Audit
Verify all prerequisites are met:
1. All research phases completed with passing verification
2. Conventions consistent across all phases
3. All claims proved and verified
4. Research digest available
5. Citation list prepared

If not ready: report what's missing and which phase to revisit.

### Step 2: Scope and Outline
Ask user (or determine from state):
- Target journal (AMS, Annals, arXiv preprint, etc.)
- Key result to highlight
- Target audience level
- Page limit constraints

Create paper outline based on standard mathematical paper structure.

### Step 3: Scaffold LaTeX
Create paper/ directory with:
- main.tex (using appropriate journal class)
- references.bib (bibliography)
- Theorem environment definitions
- Convention-locked notation macros

### Step 4: Wave-Parallelized Drafting
Spawn gmd-paper-writer agents in dependency order:

**Wave 1**: Results section + Methods/Proofs section (no deps)
**Wave 2**: Introduction (needs: Results, to state the main theorem)
**Wave 3**: Discussion / Open Questions (needs: Results + Methods)
**Wave 4**: Conclusions (needs: all above)
**Wave 5**: Abstract (written LAST — needs everything)
**Wave 6**: Appendices (if any)

After each wave:
- Verify LaTeX compiles (pdflatex)
- Check notation consistency
- Verify cross-references resolve

### Step 5: Citation Verification
Spawn gmd-bibliographer (when implemented) or manual check:
- All cited results exist
- Citations are to the correct paper
- BibTeX entries are complete
- No missing citations for key results used

### Step 6: Peer Review
Spawn gmd-referee for staged review:
- Rigor review
- Clarity review
- Significance review
- Novelty review
- Completeness review

### Step 7: Revision Loop
If review requires changes (max 3 iterations):
1. Apply required changes
2. Re-compile LaTeX
3. Re-run notation/citation checks
4. Re-submit to referee

### Step 8: Final Package
Produce submission-ready package:
- main.tex (compilable)
- references.bib
- Any figures
- arXiv submission checklist

</process>
