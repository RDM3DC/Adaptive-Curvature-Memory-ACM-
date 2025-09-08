"""
Exterior Algebra / Geometric Algebra utilities for Curve Memory.

Implements minimal wedge product and inner product operators for R^n vectors.
"""
from typing import List

def wedge(u: List[float], v: List[float]) -> float:
    """Compute scalar wedge (2D area) for 2D vectors."""
    if len(u) == 2 and len(v) == 2:
        return u[0]*v[1] - u[1]*v[0]
    raise NotImplementedError("Only 2D wedge implemented")

def inner(u: List[float], v: List[float]) -> float:
    """Dot product."""
    return sum(ui*vi for ui,vi in zip(u,v))
