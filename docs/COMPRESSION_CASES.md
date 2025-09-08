# Compression Cases in Curve Memory

CMA supports **wedge-product compressibility**, enabling *lossless-size* composition when
adjacent glyphs overlap in subspace directions.

## Example Cases
1. **Parallel Arcs**
   - Two arcs with identical curvature directions ⇒ contraction into one longer arc.

2. **Clothoid + Arc**
   - If clothoid curvature stabilizes into constant value matching the arc ⇒ merge.

3. **Opposite Pairs**
   - Arc followed by inverse arc ⇒ cancellation.

## Benchmark Plan
- Generate synthetic polylines.
- Encode into CMA glyphs.
- Apply `wedge_contract` and measure size savings.
- Compare compression ratio across curve families.

---
*Placeholder for compression experiments.*
