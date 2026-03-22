# Probability and Statistics Protocols

> Methodology for measure-theoretic probability and mathematical statistics.

## Protocol: Probability Theory

### When to Use
Convergence of random variables, limit theorems, martingales, stochastic processes.

### Steps
1. **Specify the probability space** — (Ω, F, P). What σ-algebra?
2. **For convergence proofs**, identify the type:
   - Almost sure (strongest)
   - In probability
   - In L^p
   - In distribution (weakest)
   - Relationships: a.s. → in prob → in dist; L^p → in prob
3. **For limit theorems**:
   - LLN (weak/strong): check independence and moment conditions
   - CLT: check Lindeberg or Lyapunov conditions for non-iid case
   - LIL: check iid with finite variance
4. **For martingales**:
   a. Verify adapted to the filtration
   b. Verify integrability: E[|X_n|] < ∞
   c. Verify martingale property: E[X_{n+1}|F_n] = X_n
   d. Apply convergence theorems (bounded, L^2, uniform integrability)
5. **For characteristic functions**: use Lévy continuity theorem for convergence in distribution
6. **Verify with known distributions** — Gaussian, Poisson, exponential

### Common LLM Pitfalls
- Confusing types of convergence (E015 analog)
- Applying CLT without verifying moment conditions
- Treating conditional expectation as a number rather than a random variable
- Forgetting measurability requirements

---

## Protocol: Mathematical Statistics

### When to Use
Estimation theory, hypothesis testing, decision theory, asymptotic statistics.

### Steps
1. **Specify the statistical model** — what family of distributions? What parameter space?
2. **For estimation**:
   - MLE: write likelihood, check regularity conditions, derive score equation
   - Bayes: specify prior, compute posterior, derive Bayes estimator
   - Check: is the estimator unbiased? Consistent? Efficient?
3. **For hypothesis testing**:
   - State H_0 and H_1 precisely
   - Choose test statistic, derive its distribution under H_0
   - Compute power function
   - Apply Neyman-Pearson lemma (if applicable)
4. **For asymptotics**:
   - MLE: verify regularity conditions (identifiability, support independence, smoothness)
   - Apply delta method for functions of estimators
   - Fisher information computation
5. **Verify with exponential family** models (closed-form solutions available)

### Common LLM Pitfalls
- Confusing one-sided and two-sided tests
- Incorrect Fisher information computation (missing negative sign or wrong parameterization)
- Forgetting to check regularity conditions before claiming asymptotic normality
- Misapplying the delta method (need smoothness at the true parameter value)
