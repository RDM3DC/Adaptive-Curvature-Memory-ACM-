
from typing import List, Tuple, Dict, Any
import json, math
from .alphabet import Glyph, GlyphFamily
from .geometry import kappa_tau_from_polyline
from .compression import wedge_contract

def encode_curve(points: List[Tuple[float,float]], pi_mode: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Encode a polyline into a CMA JSON dict.
    This is a minimal heuristic encoder: map curvature patterns to simple glyphs.
    """
    if pi_mode is None:
        pi_mode = {"type":"adaptive","alpha":0.1,"mu":0.02}
    kappas, taus = kappa_tau_from_polyline(points)
    glyphs: List[Glyph] = []
    for k in kappas:
        fam = GlyphFamily.CLOTHOID if abs(k) < 0.5 else GlyphFamily.ARC
        glyphs.append(Glyph(family=fam, theta={"k": float(k), "L": 1.0}, bind=1.0))
    glyphs = wedge_contract(glyphs)
    return {
        "version":"0.3",
        "pi_mode": pi_mode,
        "glyphs":[{"family":g.family.value, "theta":g.theta, "bind":g.bind} for g in glyphs],
        "meta":{"created_at": None}
    }
