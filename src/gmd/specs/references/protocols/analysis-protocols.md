# Analysis Protocols

> Step-by-step methodology guides for analysis (real, complex, functional).

## Protocol: Real Analysis Proof

### When to Use
Limits, continuity, differentiation, integration, sequences and series.

### Steps
1. **State the ε-δ / ε-N framework** explicitly when needed
2. **Identify the function space** — continuous, Lipschitz, C^k, L^p?
3. **For convergence proofs**:
   a. State precisely what type: pointwise, uniform, L^p, almost everywhere
   b. Choose the right tool (MCT, DCT, Fatou, Dini, Arzelà-Ascoli)
   c. Verify all hypotheses of the convergence theorem
4. **For differentiation**: check differentiability before computing derivatives
5. **For integration**: verify integrability before manipulating integrals
6. **Check boundary/endpoint behavior** — what happens at the edges of the domain?
7. **Verify with known functions** — polynomials, exponentials, trig functions

### Common LLM Pitfalls
- Exchanging limits without justification (E005)
- Confusing pointwise and uniform convergence (E015)
- Using DCT without finding the dominating function
- Forgetting to check measurability

---

## Protocol: Complex Analysis Proof

### When to Use
Holomorphic/meromorphic functions, contour integration, residues, conformal maps.

### Steps
1. **Specify the domain** — open, connected, simply connected?
2. **Check holomorphicity** — Cauchy-Riemann equations, or composition of holomorphic functions
3. **For contour integrals**:
   a. Specify the contour precisely (closed? orientation?)
   b. Identify poles and their orders inside the contour
   c. Compute residues carefully
   d. Verify the contour avoids branch cuts
4. **Apply Cauchy's integral formula** when the function is holomorphic on and inside the contour
5. **For series representations**: specify the domain of convergence (disk, annulus)
6. **Check: is the result conformally invariant?**
7. **Verify with known examples** — e^z, 1/z, log z, rational functions

### Common LLM Pitfalls
- Forgetting branch cut issues with log, sqrt, and fractional powers
- Incorrect residue computation (especially for higher-order poles)
- Applying Cauchy's theorem when the domain isn't simply connected
- Sign errors in contour orientation

---

## Protocol: Functional Analysis Proof

### When to Use
Banach spaces, Hilbert spaces, operators, spectral theory, distributions.

### Steps
1. **Identify the space** — complete? separable? reflexive?
2. **Specify the topology** — norm, weak, weak*, strong operator, etc.
3. **For operator proofs**:
   a. Is the operator bounded/unbounded? What is its domain?
   b. Is it linear? Self-adjoint? Compact? Normal?
   c. Check continuity = boundedness (for linear operators between Banach spaces)
4. **Apply the Big Theorems carefully**:
   - Open Mapping Theorem: requires surjective bounded linear between Banach
   - Closed Graph Theorem: requires closed linear between Banach
   - Uniform Boundedness: requires pointwise bounded family on Banach
   - Hahn-Banach: check the version (real, complex, separation)
5. **For spectral theory**: specify the type of spectrum (point, continuous, residual)
6. **Verify with L^2, ℓ^2** as concrete examples

### Common LLM Pitfalls
- Applying Banach space theorems to incomplete spaces
- Confusing norm topology and weak topology convergence
- Using reflexivity without establishing it
- Incorrect domain specification for unbounded operators

---

## Protocol: Measure Theory

### When to Use
σ-algebras, measures, measurable functions, integration, probability.

### Steps
1. **Specify the measure space** — (X, Σ, μ). What is the σ-algebra?
2. **Check measurability** of all functions before integrating
3. **For convergence of integrals**, apply in order of preference:
   a. Monotone Convergence Theorem (non-negative, increasing)
   b. Dominated Convergence Theorem (need a dominating function in L^1)
   c. Fatou's Lemma (weaker conclusion but weaker hypotheses)
4. **For product measures**: verify σ-finiteness before applying Fubini/Tonelli
5. **Distinguish "a.e." from "everywhere"** — track where measure-zero exceptions matter
6. **For Radon-Nikodym**: check absolute continuity

### Common LLM Pitfalls
- Measure-zero confusion (E006)
- Exchanging integrals without Fubini hypotheses (E005)
- Forgetting σ-finiteness for product measures
- Treating almost-everywhere equality as equality
