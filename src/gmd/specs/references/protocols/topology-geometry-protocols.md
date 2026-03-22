# Topology and Geometry Protocols

> Step-by-step methodology for topology and geometry proofs.

## Protocol: General Topology

### When to Use
Properties of topological spaces, continuity, compactness, connectedness.

### Steps
1. **Specify the topological space** — what is the underlying set and topology?
2. **Check key properties**: Hausdorff? Compact? Connected? Second-countable? Metrizable?
3. **For continuity proofs**: use the appropriate definition (ε-δ for metric, preimage of open for general)
4. **For compactness**: choose the right characterization (open cover, sequential, limit point, for metric: total boundedness + completeness)
5. **For connectedness**: distinguish connected vs path-connected vs simply connected
6. **Verify with standard spaces** — R^n, S^n, [0,1], Cantor set, Hawaiian earring

### Common LLM Pitfalls
- Assuming Hausdorff when not stated
- Confusing compact and sequentially compact in non-metrizable spaces
- Using path-connectedness when only connectedness is available

---

## Protocol: Algebraic Topology

### When to Use
Fundamental groups, homology, cohomology, homotopy theory.

### Steps
1. **Identify the space up to homotopy equivalence** when possible
2. **Choose the right tool**:
   - π_1: fundamental group (low-dimensional, specific spaces)
   - H_n: singular/simplicial/cellular homology (computable, functorial)
   - H^n: cohomology (ring structure, cup product)
   - Higher homotopy groups (hard to compute, use spectral sequences)
3. **For fundamental group**: use van Kampen's theorem for decompositions
4. **For homology**: use Mayer-Vietoris for decompositions, long exact sequences for pairs
5. **For covering spaces**: use the correspondence with subgroups of π_1
6. **Verify with known computations**: H_*(S^n), H_*(T^n), H_*(RP^n), H_*(CP^n)

### Common LLM Pitfalls
- Incorrectly applying van Kampen (need path-connected intersection)
- Wrong signs in connecting homomorphisms
- Confusing reduced and unreduced homology

---

## Protocol: Differential Geometry

### When to Use
Manifolds, curvature, connections, Riemannian geometry.

### Steps
1. **Specify the manifold** — dimension, smoothness class, orientable?
2. **Choose coordinates** — set convention lock for coordinate system
3. **For curvature computations**:
   a. Compute Christoffel symbols from metric
   b. Compute Riemann tensor from Christoffels
   c. Contract to Ricci tensor and scalar curvature
   d. Verify Bianchi identities as consistency check
4. **For geodesics**: derive and solve geodesic equations
5. **For comparison theorems**: verify curvature bounds (Bonnet-Myers, Cartan-Hadamard)
6. **Verify with known metrics** — flat space, sphere, hyperbolic space, Schwarzschild

### Common LLM Pitfalls
- Sign convention errors in Riemann tensor (multiple conventions exist!)
- Index placement errors (E001 — Einstein summation)
- Coordinate singularities mistaken for genuine singularities
- Forgetting to check smoothness of transition maps
