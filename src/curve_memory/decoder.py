
from typing import Dict, Any, List, Tuple
import math

def decode_curve(cma: Dict[str,Any]) -> List[Tuple[float,float]]:
    """
    Decode a CMA JSON dict into a polyline (very rough reconstruction).
    Each glyph contributes a short segment; real implementation would integrate frames.
    """
    pts: List[Tuple[float,float]] = [(0.0,0.0)]
    x,y,theta = 0.0,0.0,0.0
    for g in cma.get("glyphs", []):
        th = g["theta"]
        k = float(th.get("k", 0.0))
        L = float(th.get("L", 1.0))
        # naive arc step
        if abs(k) < 1e-6:
            dx, dy = L*math.cos(theta), L*math.sin(theta)
            x += dx; y += dy
        else:
            R = 1.0/max(abs(k), 1e-6)
            dtheta = L * k
            theta_mid = theta + 0.5*dtheta
            x += R * (math.sin(theta + dtheta) - math.sin(theta))
            y -= R * (math.cos(theta + dtheta) - math.cos(theta))
            theta += dtheta
        pts.append((x,y))
    return pts
