# Execute Phase Workflow

> Detailed workflow for the execute-phase command. Read this before executing.

## Pre-Execution Checklist

- [ ] STATE.md loaded and current phase identified
- [ ] ROADMAP.md parsed for phase goal
- [ ] All PLAN-*.md files for current phase discovered
- [ ] Convention locks loaded and verified
- [ ] Rollback checkpoint tag created
- [ ] Context budget assessed

## Wave Computation

1. Parse all plans for dependency graph
2. Group into waves: Wave 1 = no deps, Wave 2 = depends only on Wave 1, etc.
3. Verify no circular dependencies
4. If circular: STOP, flag to user

## Per-Wave Execution

For wave N:

### 1. Pre-Wave
```
log_wave_start(wave_N)
for each plan in wave:
  verify plan.depends_on all in completed plans
```

### 2. Parallel Execution
```
results = parallel_map(wave.plans, execute_plan)

where execute_plan(plan):
  for task in plan.tasks (wave-ordered):
    checkpoint_tag = create_checkpoint(phase, plan.id)
    result = spawn(gmd-executor, {
      task: task,
      conventions: current_locks,
      error_catalog: llm-math-errors,
      context_budget: 50%
    })
    verify_artifacts(result.files_written)
    commit_task_artifacts(task, result)
    log_task_complete(task.id, result.status)
```

### 3. Post-Wave Verification (if configured)
```
if config.workflow.verify_between_waves == "auto":
  check_convention_consistency()
  if has_computation:
    check_numerical_stability()
```

### 4. State Update
```
update_state({
  plans_completed: += wave.plans,
  total_tasks_completed: += wave.task_count
})
```

## Post-Phase Verification

```
verdict = spawn(gmd-verifier, {
  artifacts: all_phase_artifacts,
  conventions: current_locks,
  evidence: collected_evidence
})

if verdict.overall == "PASS":
  advance_phase()
  return SUCCESS

if verdict.overall == "PARTIAL" or "FAIL":
  gap_plans = create_gap_closure_plans(verdict.failures)
  execute_gap_plans(gap_plans, max_iterations=2)

  re_verdict = spawn(gmd-verifier, {re-verify})
  if re_verdict.overall == "PASS":
    advance_phase()
  else:
    flag_unresolved(re_verdict.all_failures)
```

## Failure Routing Matrix

| Failure Type | Route To | Max Retries |
|-------------|----------|-------------|
| Logical error in proof | gmd-executor (targeted re-derivation) | 2 |
| Missing base case | gmd-executor (add base case) | 1 |
| Convention drift | Convention resolution | 1 |
| Counterexample found | gmd-executor (fix or reformulate) | 2 |
| Literature disagreement | gmd-researcher + gmd-executor | 1 |
| Convergence unjustified | gmd-executor (add justification) | 2 |
| Type inconsistency | gmd-executor (fix types) | 1 |
| Incomplete cases | gmd-executor (add missing cases) | 1 |

## Context Pressure Protocol

If context usage > config.workflow.context_budget_warning_pct:
1. Log warning
2. If in middle of task: create checkpoint (.continue-here.md)
3. Summarize progress so far
4. Return with status: checkpoint
