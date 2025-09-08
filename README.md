# Curve Memory (CMA) — Updated 2025-09-08 10:04:13

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
