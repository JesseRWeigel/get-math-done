# Combinatorics and Discrete Mathematics Protocols

> Methodology for enumeration, graph theory, and the probabilistic method.

## Protocol: Enumerative Combinatorics

### When to Use
Counting problems, generating functions, bijective proofs.

### Steps
1. **Define the objects being counted precisely** — what exactly is in the set?
2. **Choose the approach**:
   - Bijective proof (strongest — establishes structural understanding)
   - Generating functions (algebraic — powerful for recurrences)
   - Inclusion-exclusion (for overcounting corrections)
   - Transfer matrix method (for path counting)
3. **For generating functions**:
   a. Determine type: ordinary, exponential, Dirichlet
   b. Set up the recurrence or functional equation
   c. Extract coefficients (partial fractions, residues, or asymptotics)
4. **For bijective proofs**: verify the bijection is well-defined and injective/surjective
5. **Verify with small cases**: compute a(0), a(1), ..., a(10) directly and match
6. **Check OEIS** for the sequence — is this a known sequence?

### Common LLM Pitfalls
- Sign errors in inclusion-exclusion (E001)
- Off-by-one in recurrence initial conditions (E002)
- Confusing labeled and unlabeled counting
- Incorrect coefficient extraction from generating functions

---

## Protocol: Graph Theory

### When to Use
Properties of graphs, coloring, matching, extremal graph theory, spectral graph theory.

### Steps
1. **Define the graph precisely** — simple, directed, weighted, multigraph?
2. **For structural proofs**:
   a. Check if the result is about all graphs or a specific family
   b. Consider induction on vertices/edges
   c. Try probabilistic argument if exact construction is hard
3. **For coloring/chromatic number**:
   a. Lower bound: find cliques, use fractional chromatic number
   b. Upper bound: construct a coloring (greedy, Brooks' theorem, probabilistic)
4. **For matching**: use Hall's theorem (bipartite), Tutte's theorem (general)
5. **For extremal problems**: consider Turán-type results, Ramsey numbers
6. **Verify with small graphs**: K_n, K_{n,m}, C_n, Petersen graph, known examples

### Common LLM Pitfalls
- Confusing vertex and edge coloring
- Forgetting to check bipartiteness before applying bipartite-specific results
- Off-by-one in degree conditions

---

## Protocol: Probabilistic Method

### When to Use
Existence proofs via probability, random graphs, Lovász Local Lemma.

### Steps
1. **Define the probability space** — what is random? What is the distribution?
2. **For first moment method**: compute E[X], show E[X] > 0 (or < n)
3. **For second moment method**: compute Var[X], apply Chebyshev or Paley-Zygmund
4. **For Lovász Local Lemma**:
   a. Identify the bad events
   b. Bound their probabilities
   c. Bound the dependency (each event depends on at most d others)
   d. Verify the LLL condition: p(d+1) ≤ 1 (symmetric) or the general asymmetric condition
5. **For alteration method**: start random, fix violations
6. **Verify the probability computation with small cases**

### Common LLM Pitfalls
- Forgetting independence requirements for union bound
- Incorrect variance computation (missing covariance terms)
- Applying LLL without verifying the dependency condition
- Confusing expectation and probability (E[X] = k does not mean P(X ≥ 1) is large)
