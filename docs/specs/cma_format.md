
# CMA Container Format (v0.3)

A CMA file is JSON with fields:

- `version`: string, e.g., "0.3"
- `pi_mode`: {"euclidean" | "adaptive"}, with optional fields for πₐ parameters {alpha, mu}
- `glyphs`: array of glyph records:
  - `family`: {"arc","clothoid","cubic","helix","custom"}
  - `theta`: parameter dict (family-specific)
  - `bind`: optional weight/binding (float), ARP-managed
- `frames`: optional array of SE(2)/SE(3) frames if precomputed
- `hash`: optional curve-hash for deduplication
- `meta`: author, created_at, notes

Example:
```json
{
  "version": "0.3",
  "pi_mode": {"type": "adaptive", "alpha": 0.1, "mu": 0.02},
  "glyphs": [
    {"family":"clothoid","theta":{"L":0.5,"k0":0.0,"k1":1.2},"bind":0.93}
  ],
  "meta": {"created_at": "2025-09-08T00:00:00Z", "notes":"spiral test"}
}
```
