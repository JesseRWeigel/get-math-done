# Number Theory Protocols

> Methodology for analytic and algebraic number theory.

## Protocol: Analytic Number Theory

### When to Use
Distribution of primes, L-functions, sieve methods, exponential sums.

### Steps
1. **Formulate the problem analytically** — express counting functions via Dirichlet series or integrals
2. **Identify the relevant L-function or zeta function**
3. **For prime counting**: use partial summation / Abel summation to relate sums to integrals
4. **For sieve methods**: choose the sieve (Eratosthenes, Selberg, large sieve, GPY)
5. **Estimate error terms carefully**:
   a. Use big-O, little-o, and Vinogradov notation consistently
   b. Track implied constants — are they effective?
   c. Check uniformity of error terms in parameters
6. **Verify with known results**: PNT, Dirichlet's theorem, Bombieri-Vinogradov
7. **Check numerical consistency** for small values (first 100 primes, specific L-function values)

### Common LLM Pitfalls
- Incorrect convergence claims for Dirichlet series (E004)
- Sign errors in complex analysis contour shifts
- Confusing effective and ineffective estimates
- Off-by-one in inclusion-exclusion (E001)

---

## Protocol: Algebraic Number Theory

### When to Use
Number fields, rings of integers, ideal theory, class groups, Galois theory.

### Steps
1. **Specify the number field** — degree, discriminant, signature
2. **Compute the ring of integers** if not known
3. **For ideal factorization**: use Dedekind's theorem for splitting of primes
4. **For class number**: compute using Minkowski bound
5. **For units**: use Dirichlet's unit theorem to determine rank
6. **For Galois theory**:
   a. Determine the Galois group
   b. Identify subgroups and fixed fields
   c. Apply the fundamental theorem
7. **Verify with known fields**: Q(√d) for small d, cyclotomic fields Q(ζ_n)

### Common LLM Pitfalls
- Forgetting that Z[√d] might not be the full ring of integers (e.g., d ≡ 1 mod 4)
- Incorrect norm computations for ideals
- Confusing the Galois group with the automorphism group when the extension is not Galois

---

## Protocol: Combinatorial Number Theory

### When to Use
Additive combinatorics, Ramsey theory on integers, sum-product phenomena.

### Steps
1. **Formulate precisely** — what sets, what operations, what bounds?
2. **For additive problems**: consider sumset estimates (Plünnecke-Ruzsa, Freiman)
3. **For Ramsey-type**: identify the partition structure, apply Hales-Jewett or Rado's theorem
4. **For density results**: use Szemerédi's theorem / Green-Tao as benchmarks
5. **For sum-product**: identify the field/ring, apply Elekes-Ronyai or Bourgain-Katz-Tao
6. **Verify small cases explicitly** — compute for n ≤ 20

### Common LLM Pitfalls
- Incorrect application of probabilistic method bounds
- Sign/constant errors in density increment arguments
- Confusing results over F_p with results over Z
