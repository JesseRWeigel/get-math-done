# Numerical Methods Protocols

> Step-by-step methodology guides for numerical computation and analysis.

## Protocol: Numerical Linear Algebra

### When to Use
Solving linear systems, eigenvalue problems, matrix decompositions, least squares.

### Steps
1. **Classify the problem** — direct solve (Ax = b), eigenvalue (Ax = λx), least squares (min ‖Ax − b‖)?
2. **Characterize the matrix** — sparse/dense, symmetric, positive definite, banded, ill-conditioned?
3. **Compute the condition number** κ(A) = ‖A‖·‖A⁻¹‖ to assess sensitivity to perturbation
4. **Select the appropriate factorization** — LU (general), Cholesky (SPD), QR (least squares), SVD (rank-deficient)
5. **For iterative methods**: choose between Krylov methods (CG for SPD, GMRES for general) and stationary methods (Jacobi, Gauss-Seidel)
6. **Apply preconditioning** if the condition number is large — ILU, AMG, diagonal scaling
7. **Verify the solution** — compute the residual ‖Ax − b‖/‖b‖, check backward stability
8. **Report significant digits** — only claim digits justified by κ(A) × machine epsilon

### Common LLM Pitfalls
- Applying Cholesky to matrices that are not symmetric positive definite
- Ignoring catastrophic cancellation in subtraction of nearly equal numbers
- Confusing forward and backward error analysis
- Recommending Gaussian elimination without pivoting for ill-conditioned systems
- Forgetting that condition number bounds are tight only in the worst case

---

## Protocol: ODE Solver Selection and Verification

### When to Use
Solving initial value problems (IVPs), boundary value problems (BVPs), or systems of ordinary differential equations.

### Steps
1. **Classify the ODE** — order, linearity, autonomy, stiffness
2. **Test for stiffness** — if eigenvalues of the Jacobian have widely varying magnitudes, the system is stiff
3. **Select the method** — explicit RK4 (non-stiff), implicit BDF/Radau (stiff), symplectic integrators (Hamiltonian systems)
4. **Choose step size** — use adaptive step control (embedded RK pairs like Dormand-Prince) with specified absolute and relative tolerances
5. **Verify order of convergence** — halve the step size, check that error decreases by 2^p for a p-th order method
6. **Check conservation laws** — energy, mass, symplectic structure should be preserved if expected
7. **For BVPs**: use shooting method or finite difference discretization with mesh refinement
8. **Validate against known analytical solutions** or method-of-manufactured-solutions

### Common LLM Pitfalls
- Using explicit methods on stiff systems (leads to instability or impractically small step sizes)
- Confusing local truncation error with global error (global error is one order lower)
- Forgetting to verify that adaptive step controllers actually achieve requested tolerance
- Applying fixed-step RK4 and assuming the answer is "accurate enough" without convergence testing

---

## Protocol: PDE Discretization and Solution

### When to Use
Discretizing and solving partial differential equations — elliptic, parabolic, or hyperbolic.

### Steps
1. **Classify the PDE** — elliptic (Laplace, Poisson), parabolic (heat equation), hyperbolic (wave equation)
2. **Choose the discretization** — finite difference (FD), finite element (FEM), finite volume (FV), spectral methods
3. **Verify consistency** — does the discrete operator converge to the continuous operator as h → 0?
4. **Check stability** — von Neumann analysis (Fourier mode growth) for FD, CFL condition for hyperbolic problems
5. **Apply the Lax equivalence theorem** — consistency + stability ⟹ convergence (for linear problems)
6. **For FEM**: verify the weak formulation, choose appropriate element types, check inf-sup condition for mixed problems
7. **Perform mesh refinement study** — confirm the expected convergence rate (h^p for p-th order elements)
8. **Validate boundary conditions** — Dirichlet (essential), Neumann (natural), Robin; ensure correct implementation

### Common LLM Pitfalls
- Violating the CFL condition for explicit time-stepping of hyperbolic PDEs
- Forgetting the inf-sup (LBB) condition in mixed finite element formulations (e.g., Stokes flow)
- Applying central differences to convection-dominated problems without stabilization (SUPG, upwinding)
- Confusing strong and weak imposition of boundary conditions in FEM

---

## Protocol: Optimization Algorithm Selection

### When to Use
Minimizing or maximizing objective functions — unconstrained, constrained, convex, or nonconvex.

### Steps
1. **Characterize the problem** — convex vs nonconvex, smooth vs nonsmooth, constrained vs unconstrained, dimensionality
2. **For unconstrained smooth problems**: gradient descent (simple), L-BFGS (large-scale), Newton's method (small, well-conditioned)
3. **For constrained problems**: identify constraint types — linear, nonlinear, equality, inequality
4. **Choose the method** — interior point (large-scale LP/QP), SQP (nonlinear constrained), augmented Lagrangian, projected gradient
5. **Verify convergence** — check gradient norm, constraint violation, KKT conditions at the solution
6. **For nonconvex problems**: use multiple restarts, check second-order sufficient conditions (Hessian positive definite at solution)
7. **Report convergence rate** — linear, superlinear, or quadratic, and verify empirically
8. **Validate with known test problems** — Rosenbrock, Rastrigin, or domain-specific benchmarks

### Common LLM Pitfalls
- Claiming global optimality for nonconvex problems when only a local minimum was found
- Forgetting to check that the Hessian is positive definite at a critical point (could be saddle point)
- Using gradient descent with a fixed step size without line search (Armijo, Wolfe conditions)
- Confusing KKT necessary conditions with sufficient conditions for nonconvex problems
- Recommending Newton's method without addressing the cost of Hessian computation

---

## Protocol: Convergence Analysis

### When to Use
Proving or verifying that a numerical method converges and quantifying its rate.

### Steps
1. **Define the error metric** — absolute error, relative error, norm choice (L2, L∞, energy norm)
2. **Establish consistency** — show the truncation error vanishes as the discretization parameter → 0
3. **Prove stability** — the method does not amplify errors (use energy estimates, maximum principle, or von Neumann analysis)
4. **Apply the convergence theorem** — for linear problems, consistency + stability ⟹ convergence (Lax-Richtmyer)
5. **Determine the convergence order** — Taylor expand the truncation error, identify the leading term O(h^p)
6. **Verify empirically** — compute errors at several mesh sizes, fit log(error) vs log(h), slope should equal p
7. **Check for order reduction** — boundary conditions, variable coefficients, or stiffness can reduce observed order
8. **Report the convergence table** — mesh size, error, observed order for at least 4 refinement levels

### Common LLM Pitfalls
- Claiming convergence order from only two data points (need at least 3-4 for reliable estimation)
- Confusing truncation error order with convergence order (they differ for some methods)
- Ignoring pre-asymptotic behavior — coarse meshes may not show the asymptotic rate
- Forgetting that nonlinear problems require separate convergence analysis beyond Lax-Richtmyer
