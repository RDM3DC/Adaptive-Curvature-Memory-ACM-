
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class CurveFrame:
    x: float
    y: float
    theta: float  # heading (2D); extend to SE(3) as needed

@dataclass
class CurveHash:
    I_kappa: float
    I_tau: float
    area: float

def kappa_tau_from_polyline(points: List[Tuple[float, float]]):
    """Compute discrete curvature (kappa) and approximate torsion (0 in 2D)."""
    if len(points) < 3:
        return [0.0], [0.0]
    kappas = []
    taus = []
    for i in range(1, len(points)-1):
        x0,y0 = points[i-1]
        x1,y1 = points[i]
        x2,y2 = points[i+1]
        v1 = (x1-x0, y1-y0)
        v2 = (x2-x1, y2-y1)
        a1 = math.atan2(v1[1], v1[0])
        a2 = math.atan2(v2[1], v2[0])
        da = math.atan2(math.sin(a2-a1), math.cos(a2-a1))
        ds = math.hypot(*v1)
        kappas.append(da/max(ds, 1e-12))
        taus.append(0.0)
    return kappas, taus
