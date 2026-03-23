---
name: review-paper
description: Run citation verification and staged peer review on a completed manuscript
---

<process>

## Review Paper

Standalone review command — runs citation verification and the full referee panel
on a completed manuscript. Can be run at any time after write-paper, or independently.

### Step 1: Locate the Manuscript
Find paper/main.tex (or paper/*.tex). If not found, ask the user to specify the path.
Load the full manuscript and references.bib.

### Step 2: Citation Verification
For every citation in the manuscript:

1. **Existence check**: Does the cited work exist? Verify against:
   - arXiv (search by author + title)
   - MathSciNet / Mathematical Reviews (if accessible)
   - Google Scholar (as fallback)
   - The references.bib entry (DOI, journal, volume, pages)

2. **Statement accuracy**: When the paper cites a specific theorem or result,
   verify the statement matches what the original paper actually proves.
   Flag any mischaracterizations.

3. **Attribution accuracy**: Is the result attributed to the correct author(s)?
   Are there earlier or more appropriate citations?

4. **Completeness**: Are there standard references that should be cited but aren't?
   (e.g., survey articles, foundational results the proof relies on)

Produce a CITATION-REPORT.md with:
- Each citation: VERIFIED / UNVERIFIED / FLAGGED
- Any mischaracterizations found
- Missing citations suggested

### Step 3: Notation Audit
Load convention locks from .gmd/conventions.json.
Scan the manuscript for:
- Notation inconsistencies (same symbol used for different things)
- Convention violations (locked conventions not followed)
- Undefined notation (symbols used before definition)

### Step 4: Staged Peer Review
Spawn gmd-referee with the manuscript. The referee runs 5 independent review perspectives:

#### 4a. Rigor Review
- Is every proof step logically justified?
- Are all assumptions stated and used?
- Are there hidden assumptions or unjustified steps?
- Is the level of detail appropriate for the target journal?

#### 4b. Clarity Review
- Is the paper well-organized and easy to follow?
- Are definitions clear and placed before first use?
- Is the proof strategy explained before diving into details?
- Would a knowledgeable reader understand the key ideas?

#### 4c. Significance Review
- Is the main result new and interesting?
- How does it relate to existing work?
- Is the improvement quantitatively meaningful?
- Is the result strong enough for the target journal?

#### 4d. Novelty Review
- What is the precise new contribution?
- Is this genuinely new, or a minor variation of known results?
- Are the techniques generalizable?
- Does it open new directions?

#### 4e. Completeness Review
- Are all claimed results proved?
- Are all references complete and accurate?
- Are open questions and limitations honestly discussed?
- Is the abstract consistent with the actual results?

### Step 5: Adjudicate and Report
Compile all review perspectives into a unified REVIEW-REPORT.md:
- Overall recommendation: Accept / Minor Revision / Major Revision / Reject
- Required changes (numbered, actionable, prioritized)
- Suggested improvements (non-blocking)
- Citation verification summary

### Step 6: Revision (if needed)
If the recommendation is Minor or Major Revision:
1. Present the required changes to the user
2. If autonomy allows, apply changes automatically
3. Re-compile LaTeX and verify it builds
4. Re-run notation audit
5. Maximum 3 revision iterations

### Step 7: Final Verdict
Produce a final assessment:
- Paper status: Ready for submission / Needs work / Not ready
- Citation verification: X/Y verified
- Review consensus
- Any remaining caveats for the author

</process>
