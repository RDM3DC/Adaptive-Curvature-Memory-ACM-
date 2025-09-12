
# Curve Memory Whitepaper (Research Preview)

**Core idea:** We define a reversible mapping between sequences of *glyphs* (from a Curve Memory Alphabet, CMA)
and differentiable curves in ℝ²/ℝ³ (optionally ℝⁿ). Each glyph is a parametric micro-primitive with tunable
state (e.g., signed curvature κ(s), torsion τ(s), arc-length budgets, and control-signatures). Composition
obeys exterior/wedge constraints that ensure well-posed decoding and open the door to *compressible* concatenation.

## 1. Adaptive π (πₐ) coupling

We let π become an adaptive field πₐ that relaxes to the Euclidean π via a damping term μ and optional gradient
steering in a near regime. In “far” starts we update with damping-only; in “near” we include gradient feedback:

  - **Far regime:** α = 0, update

    $$
    \pi_a \leftarrow \pi_a - \mu(\pi_a - \pi)
    $$

  with angle-reduced trig to maintain numerical stability for extreme initial values.
  - **Near regime:** re-enable gradient:

    $$
    \pi_a \leftarrow \pi_a - \alpha \, e \, \frac{\partial P}{\partial \pi_a} - \mu(\pi_a - \pi)
    $$

CMA encoding uses πₐ consistently in curvature/angle parameterizations so that *symbol boundaries* remain
stable while allowing adaptive geometry.

## 2. Glyphs and Combinators

A glyph $g$ is a tuple $(\mathcal{F}, \theta)$ where $\mathcal{F}$ is a parametric family (e.g., arc,
clothoid fragment, cubic segment, helical micro-curve) and $\theta$ are parameters. Combinators:

- **Concatenate** $g_1 \oplus g_2$: end-frame of $g_1$ matches start-frame of $g_2$.
- **Wedge** $g_1 \wedge g_2$: antisymmetric join imposing orientation/area constraints, enabling
  *compressibility* when the exterior product nullifies redundant subspace components.
- **Bind** $\mathcal{B}_\lambda(g)$: weight/attention binding used in decoding; λ obeys ARP-like dynamics.

## 3. Wedge-product Compressibility (Sketch)

Let $c_1, c_2 \in \Lambda^k(V)$ be k-vectors derived from local frame differentials of two glyph segments.
Redundancy implies $c_1$ and $c_2$ have significant overlap in subspaces of $V$.
If $c_1 \wedge c_2 \approx 0$ (or lies in a low-volume subspace), we admit an *equivalence contraction*
rule $(g_1 \oplus g_2) \sim g^\star$ where $g^\star$ is a single glyph whose parameters encode the
combined information—hence **lossless-size** composition under the wedge constraint.

## 4. ARP/MD-ARP Stabilization

We modulate glyph strengths $G_i$ using ARP-style dynamics:

$$
\frac{dG_i}{dt} = \alpha |I_i| - \mu G_i
$$

where $I_i$ is a local evidence/current for glyph $i$ during decoding. This suppresses noise and yields
consistent symbol recovery across scales.

## 5. Decoding
Given a target curve (e.g., polyline or spline), we seek the minimal CMA sequence whose composed transform
matches the curve within tolerance $\epsilon$. We solve by alternating:
1. **Symbol proposal** (discrete search over glyph templates / dynamic programming),
2. **Parameter refinement** (continuous least-squares on frames),
3. **Wedge checks** (attempt equivalence contractions),
4. **ARP stabilization** on glyph weights.

## 6. Curve Hashes
We define a *curve hash* $H(c)$ as a tuple of stable invariants (integrals of κ, τ, signed areas, and
selected wedge components). Under small deformations within admissible ranges, $H$ remains constant, enabling
fast equality checks and deduplication.

## 7. Guarantees (informal)
- **Stability:** πₐ coupling + ARP-stabilized weights ensure bounded decoding error under bounded noise.
- **Minimality:** With wedge contractions, normal forms exist for large classes of inputs.
- **Reversibility:** Encoding/decoding are inverses up to admissible gauge choices (frames and reparameterization).

*Appendix:* symbol tables, normal forms, and proofs-in-progress.
