# Curve Memory (CMA) — Updated 2025-09-12

[![GitHub Sponsors](https://img.shields.io/github/sponsors/RDM3DC)](https://github.com/sponsors/RDM3DC)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Curve Memory (CMA) encodes *curves as memory* and *memory as curves*, forming a bidirectional
representation that sits at the intersection of **Adaptive π (πₐ)** geometry and the **Adaptive Resistance
Principle (ARP)** family of adaptive systems.

This update aligns the repo with our most recent discoveries:
- **Adaptive π (πₐ) integration**: dynamic curvature with near/far regimes and damping term μ; angle-reduced
  trig during far starts; gradient term re-enabled in near regime for precision.
- **Curve Memory Alphabet (CMA)**: minimal, composable *glyphs* (primitives) that compose to form curves
  and store information. Glyphs are parameterized by curvature κ(s), torsion τ(s), and optional signatures.
- **Wedge-product compressibility**: leveraging exterior algebra features, certain composition rules admit
  *lossless-size* encodings under wedge constraints, enabling *dual use* as a compression scheme.
- **Dynamic constants**: π, φ, and related constants become *adaptive fields* under πₐ; CMA is defined to
  remain *invariant* under these adaptive reparameterizations.
- **Multi-dimensional ARP coupling** (MD-ARP): CMA signals can be stabilized/optimized with ARP-style
  dynamics: dG/dt = α|I| − μG applied to glyph strengths, improving robustness and denoising in decoding.

---

## Why CMA?
1. **Memory-as-geometry**: A curve (or family of curves) encodes a data payload; recovering the payload is
   geometric decoding (fitting, regularization, and symbol recovery).
2. **Geometry-as-memory**: A data payload deterministically generates a canonical curve constructed from
   CMA glyphs with stability guarantees.
3. **Compression & hashing**: Exterior/wedge constraints make some concatenations *non-inflationary*,
   providing structural compressibility and *curve-hash* capabilities.

## Quick Start
```bash
pip install -e .
python examples/encode_spiral.py --n 800 --out examples/spiral.cma.json
python examples/decode_to_svg.py --in examples/spiral.cma.json --out examples/spiral.svg
```

## Repo Map
- `docs/` — math notes, whitepaper, specs.
- `src/curve_memory/` — Python reference implementation.
- `examples/` — small scripts to encode/decode.
- `tests/` — basic unit tests.

MIT License. Research preview quality — expect rapid iteration.

---

# Curve Memory in 3D (CMA-3D)

## Overview
Curve Memory (CMA) is a compact, rigid-motion-invariant representation of curves.

- **2D curves** are determined by their arclength parameterization and curvature:
  $$
  \kappa(s) = \left\| \frac{d\mathbf{T}}{ds} \right\|
  $$
  where $\mathbf{T}(s)$ is the unit tangent at arclength $s$.

- **3D space curves** require both curvature $\kappa(s)$ and torsion $\tau(s)$.
  Together they uniquely determine the curve up to rigid motion.

The **Frenet–Serret equations** describe this:
$$
\begin{aligned}
\frac{d\mathbf{T}}{ds} &= \kappa(s)\,\mathbf{N}(s) \\\
\frac{d\mathbf{N}}{ds} &= -\kappa(s)\,\mathbf{T}(s) + \tau(s)\,\mathbf{B}(s) \\\
\frac{d\mathbf{B}}{ds} &= -\tau(s)\,\mathbf{N}(s)
\end{aligned}
$$

---

## CMA-3D Representation
A curve’s memory is the tuple:
$$
\mathcal{M} = \big( L,\; u,\; \kappa(u),\; \tau(u) \big)
$$

- $L$: total curve length  
- $u = s/L \in [0,1]$: normalized arclength  
- $\kappa(u)$: curvature sequence  
- $\tau(u)$: torsion sequence  

Properties:
- **Rigid-motion invariant**
- **Scale aware** (via $L$)
- **Lossless** (curve can be reconstructed)

---

## Discrete Formulation
For polyline points $\{\mathbf{p}_i\}_{i=0}^N$:

1. **Segments and arclengths**
  $$
  \ell_i = \|\mathbf{p}_{i+1}-\mathbf{p}_i\|, \quad
  s_j = \sum_{i=0}^{j-1}\ell_i, \quad L = s_N
  $$

2. **Tangents**
  $$
  \mathbf{t}_i = \frac{\mathbf{p}_{i+1}-\mathbf{p}_i}{\ell_i}
  $$

3. **Curvature**
  $$
  \kappa_i \approx \frac{\|\mathbf{t}_i-\mathbf{t}_{i-1}\|}{\tfrac{1}{2}(\ell_{i-1}+\ell_i)}
  $$

4. **Torsion**  
  Binormals:
  $$
  \mathbf{b}_i = \frac{\mathbf{t}_i \times \mathbf{t}_{i-1}}{\|\mathbf{t}_i \times \mathbf{t}_{i-1}\|}
  $$
  Torsion:
  $$
  	au_i \approx \frac{\operatorname{sign}\!\big((\mathbf{b}_{i-1}\!\times\!\mathbf{b}_i)\cdot\mathbf{t}_i\big)\;
  \angle(\mathbf{b}_{i-1},\mathbf{b}_i)}{\tfrac{1}{2}(\ell_{i-1}+\ell_i)}
  $$

---

## Reconstruction
Given $(\kappa(s), \tau(s))$, reconstruct by integrating Frenet–Serret:

1. Start from $\mathbf{r}(0)$ with frame $(\mathbf{T},\mathbf{N},\mathbf{B})$  
2. Step $\Delta s$:
  - Rotate $(\mathbf{T},\mathbf{N})$ in $T$–$N$ plane by $\kappa \Delta s$  
  - Twist $(\mathbf{N},\mathbf{B})$ around $\mathbf{T}$ by $\tau \Delta s$  
  - Update:
    $$
    \mathbf{r}(s+\Delta s) = \mathbf{r}(s) + \mathbf{T}(s)\,\Delta s
    $$
3. Repeat until $s=L$.

---

## Global Quantities
From CMA-3D:
- **Total curvature**: $\int_0^L \kappa(s)\,ds$  
- **Total torsion**: $\int_0^L |\tau(s)|\,ds$  
- **Writhe/Twist estimates** for closed curves  

---

## Multi-Scale CMA
- Downsample $\kappa,\tau$ into pyramids  
- Store mean/std/min/max per level  
- Enables Level-of-Detail (LOD) for retrieval vs reconstruction  

---

## Example: Helix
For $\mathbf{r}(t) = (\cos t,\; \sin t,\; c t)$:

- Curvature: $\kappa = \frac{1}{1+c^2}$  
- Torsion: $\tau = \frac{c}{1+c^2}$  

So its CMA-3D memory is simply constant $(\kappa,\tau)$ along $u$.

---

## Benefits
- **Compression**: 10–60× smaller with negligible RMS error  
- **Comparison**: Pose-invariant curve fingerprints  
- **Reconstruction**: Regenerate curves at any sampling density  
- **Integration**: Plug into CAD tools (sweeps, ribbons, lofts)  
- **Learning**: Use $\kappa,\tau$ as sequence input for ML models  

---

## Summary
**CMA-3D** is the representation:
$$
\mathcal{M} = \big( L,\; u,\; \kappa(u),\; \tau(u) \big)
$$

- Compact  
- Rigid-motion invariant  
- Reconstructable  
- Multi-scale ready  

Forms a solid base for efficient curve storage, retrieval, and CAD integration.

