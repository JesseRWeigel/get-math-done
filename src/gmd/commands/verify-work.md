---
name: verify-work
description: Run the 13-check mathematical verification framework
---

<process>

## Verify Work

### Overview
Run post-hoc verification on completed phase work using the 13-check framework.

### Step 1: Collect Artifacts
Gather all output from the current phase:
- Proof files (LaTeX/markdown)
- Computation scripts and results
- SUMMARY files from executors

### Step 2: Build Evidence Registry
Extract verification evidence from artifacts:
- Proof steps and their justifications
- Assumptions stated and used
- Special cases tested
- Convergence claims made
- Convention usage

### Step 3: Run Verification
Spawn gmd-verifier with:
- All phase artifacts
- Evidence registry
- Convention locks
- LLM error catalog

### Step 4: Process Verdict
Parse the VERIFICATION-REPORT.md:
- If PASS: record in state, proceed
- If PARTIAL: create targeted gap-closure for MAJOR failures
- If FAIL: create gap-closure for CRITICAL failures, block downstream

### Step 5: Route Failures
For each failure, route to the appropriate agent:
- Logical errors → gmd-executor (targeted re-derivation)
- Convention drift → convention resolution
- Literature disagreements → gmd-researcher + gmd-executor
- Convergence failures → gmd-executor with convergence task

### Step 6: Update State
Record verification results in STATE.md:
- Verdict hash (content-addressed)
- Pass/fail counts
- Any unresolved issues

</process>
