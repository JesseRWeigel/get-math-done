# Known LLM Mathematics Failure Modes

> This catalog documents systematic failure patterns of LLMs in mathematical reasoning.
> The verifier and plan-checker cross-reference against these patterns.

## Critical Errors (High Frequency)

### E001: Sign Errors in Combinatorial Arguments
**Pattern**: Incorrect signs in inclusion-exclusion, alternating sums, Möbius inversion.
**Example**: Computing |A∪B∪C| and missing a (-1)^{k+1} factor.
**Guard**: Explicitly track signs in every term. Verify small cases.

### E002: Off-by-One in Induction
**Pattern**: Base case starts at wrong value, or inductive step assumes n ≥ k but base case only covers n = k-1.
**Example**: Proving P(n) for n ≥ 1 but base case only checks P(0), missing P(1) when the inductive step requires n ≥ 1.
**Guard**: Verify base case covers exactly the starting point of the inductive step's range.

### E003: False Commutativity Assumptions
**Pattern**: Assuming operations commute when they don't.
**Example**: Matrix multiplication, operator composition, non-abelian group elements, limits and infinite sums.
**Guard**: Explicitly check commutativity before using it. Flag any exchange of order.

### E004: Incorrect Convergence Radius / Domain Claims
**Pattern**: Using a power series outside its radius of convergence, or claiming convergence without proof.
**Example**: Using Taylor series for log(1+x) at x=2, claiming ∑1/n^s converges for s>0.
**Guard**: Explicitly verify convergence before any series manipulation.

### E005: Unjustified Exchange of Limits
**Pattern**: Swapping limit operations without verifying conditions.
**Example**: Exchanging ∑ and ∫ without dominated convergence, swapping lim and ∫ without uniform convergence.
**Guard**: Every limit exchange must cite the theorem justifying it (DCT, MCT, uniform convergence, etc.).

## Serious Errors (Medium Frequency)

### E006: Measure-Zero Set Confusion
**Pattern**: Treating measure-zero sets as empty, or confusing "almost everywhere" with "everywhere."
**Example**: Claiming a continuous function that is zero a.e. is identically zero (true), then applying same reasoning to a non-continuous function (false).
**Guard**: Track regularity assumptions. "a.e." claims need the right function space.

### E007: Dimension Counting Errors
**Pattern**: Incorrect dimension of kernels, images, quotient spaces.
**Example**: Rank-nullity applied with wrong ambient space dimension.
**Guard**: Verify dimensions independently using multiple methods.

### E008: Incorrect Negation of Quantifiers
**Pattern**: ¬(∀x ∃y P(x,y)) becomes ∃x ∀y ¬P(x,y), but LLMs sometimes produce ∃x ∃y ¬P(x,y).
**Example**: Negating the definition of continuity, uniform continuity, or limit.
**Guard**: Write out quantifier negation step by step.

### E009: Confusing Necessary and Sufficient Conditions
**Pattern**: Proving the converse instead of the original implication.
**Example**: Proving "if convergent then Cauchy" when asked to prove "if Cauchy then convergent."
**Guard**: Explicitly state which direction is being proved at the start.

### E010: Incomplete Case Analysis
**Pattern**: Missing cases in proof by cases, especially edge cases.
**Example**: Proving for n even and n odd but missing n=0, or handling positive and negative but missing zero.
**Guard**: Enumerate all cases explicitly. Verify union of cases covers the domain.

## Moderate Errors (Common but Usually Caught)

### E011: Misapplied Theorems
**Pattern**: Using a theorem without verifying its hypotheses apply.
**Example**: Applying the implicit function theorem without checking the Jacobian condition, using Fubini's theorem for non-integrable functions.
**Guard**: Before applying any named theorem, explicitly verify all hypotheses.

### E012: Notation Drift
**Pattern**: Using the same symbol for different things in different parts of a proof.
**Example**: Using ε for both the small number in the proof and a parameter of the problem.
**Guard**: Convention locks prevent this. Also: declare all notation upfront.

### E013: Circular Reasoning
**Pattern**: Using the conclusion (or an equivalent statement) as a step in the proof.
**Example**: In proving A⟹B, using B to establish A without acknowledging circularity.
**Guard**: Track the logical dependency graph. No claim should depend on itself.

### E014: Incorrect Generalization from Examples
**Pattern**: Checking a finite number of cases and claiming the general result.
**Example**: "Verified for n=1,...,10, therefore true for all n."
**Guard**: Examples are evidence, not proof. Always require a general argument.

### E015: Confusing Pointwise and Uniform Properties
**Pattern**: Proving pointwise convergence when uniform convergence is needed, or vice versa.
**Example**: Claiming a pointwise limit of continuous functions is continuous.
**Guard**: Always specify which type of convergence/continuity is being used.

## How to Use This Catalog

1. **Plan-checker**: Before execution, identify tasks where specific errors are likely. Add explicit guards.
2. **Executor**: Consult relevant entries when performing work of that type. Follow guards.
3. **Verifier**: After execution, cross-reference results against applicable error patterns.
4. **Pattern library**: When a new error pattern is discovered, add it here.
