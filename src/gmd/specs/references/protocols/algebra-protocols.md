# Algebra Protocols

> Step-by-step methodology guides for algebraic proof construction.

## Protocol: Group Theory Proof

### When to Use
Proving properties of groups, subgroups, quotient groups, homomorphisms.

### Steps
1. **State the claim precisely** — include all quantifiers and conditions
2. **Identify the group structure** — what is the group, what is the operation?
3. **Check: is the group finite or infinite?** — different techniques apply
4. **For finite groups**: consider order arguments, Lagrange's theorem, Sylow theorems
5. **For infinite groups**: consider generators and relations, normal subgroups
6. **Verify group axioms** if constructing a new group (closure, associativity, identity, inverses)
7. **Check homomorphism properties** if applicable (preserves operation, kernel, image)
8. **Apply relevant structure theorems** — fundamental theorem of finitely generated abelian groups, Jordan-Hölder, etc.
9. **Verify against known examples** — does the result hold for Z, S_n, D_n, GL_n?

### Common LLM Pitfalls
- Assuming abelian when the group is not (E003)
- Forgetting to check well-definedness of operations on cosets
- Confusing left and right cosets in non-normal subgroups
- Off-by-one in order counting for permutation groups

---

## Protocol: Linear Algebra Proof

### When to Use
Proving properties of vector spaces, linear maps, matrices, eigenvalues.

### Steps
1. **State the problem in terms of linear maps** (not just matrices when possible)
2. **Identify the field** — is it R, C, Q, or a finite field?
3. **Check dimensions** — use rank-nullity as a sanity check
4. **For existence proofs**: construct explicitly when possible
5. **For matrix proofs**: consider whether the result is basis-independent
6. **Apply spectral theory** where relevant (eigenvalues, diagonalization, Jordan form)
7. **Verify with small examples** — 2×2 or 3×3 matrices
8. **Check special cases** — zero matrix, identity matrix, diagonal matrices

### Common LLM Pitfalls
- Dimension counting errors (E007)
- Confusing row rank and column rank (they're equal, but the arguments differ)
- Forgetting that eigenvalue results differ over R vs C
- Assuming diagonalizability without justification

---

## Protocol: Ring and Module Theory

### When to Use
Properties of rings, ideals, modules, field extensions.

### Steps
1. **Identify the ring** — commutative? unital? integral domain? PID? UFD?
2. **Check ring axioms** if constructing a new ring
3. **For ideal proofs**: verify absorption property, not just closure
4. **For module proofs**: specify the base ring clearly
5. **Apply structure theorems** — Chinese Remainder Theorem, primary decomposition
6. **For field extensions**: specify the base field, compute degree
7. **Check: does the result use commutativity?** Flag if so (E003)

### Common LLM Pitfalls
- Assuming commutativity in non-commutative rings (E003)
- Confusing left and right ideals
- Applying PID results to non-PID rings
- Forgetting that quotient ring construction requires a two-sided ideal

---

## Protocol: Commutative Algebra

### When to Use
Properties of commutative rings, prime/maximal ideals, localization, completion.

### Steps
1. **Identify the ring properties** — Noetherian? local? graded?
2. **For prime ideal arguments**: use Zorn's Lemma carefully (state AC usage)
3. **For localization**: specify the multiplicative set
4. **Apply Nakayama's Lemma** when working with local rings/finitely generated modules
5. **Use going-up/going-down** for integral extensions
6. **Verify with polynomial rings** as test cases

### Common LLM Pitfalls
- Misapplying Nakayama without the correct finiteness condition
- Confusing associated primes and minimal primes
- Incorrect localization arguments (forgetting what inverts)
