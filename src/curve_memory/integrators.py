"""
Path integration for CMA glyphs in SE(2) / SE(3).
"""
from typing import List, Tuple
import math

def integrate_se2(glyphs) -> List[Tuple[float,float]]:
    """Very rough SE(2) integration of glyph sequence into a polyline."""
    pts = [(0.0,0.0)]
    x,y,theta = 0.0,0.0,0.0
    for g in glyphs:
        th = g.theta
        k = float(th.get("k",0.0))
        L = float(th.get("L",1.0))
        if abs(k)<1e-6:
            x += L*math.cos(theta); y += L*math.sin(theta)
        else:
            R = 1.0/max(abs(k),1e-6)
            dtheta = L*k
            x += R*(math.sin(theta+dtheta)-math.sin(theta))
            y -= R*(math.cos(theta+dtheta)-math.cos(theta))
            theta += dtheta
        pts.append((x,y))
    return pts
