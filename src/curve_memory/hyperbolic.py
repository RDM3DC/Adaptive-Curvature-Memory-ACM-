"""Hyperbolic geometry utilities relocated into package namespace."""
from __future__ import annotations
import math
import numpy as np

PI_E = math.pi

def full_turn_deg(r: float, kappa: float) -> float:
    return 360.0 * pi_a_over_pi(r, kappa)

def rotate_cmd(delta_deg_a: float, r: float, kappa: float) -> float:
    d_full = full_turn_deg(r, kappa)
    frac = delta_deg_a / d_full
    return frac * 2 * math.pi

def pi_a_over_pi(r: float, kappa: float, eps: float = 1e-10) -> float:
    if abs(r) < eps or abs(kappa) < eps:
        return 1.0
    x = r / kappa
    if abs(x) < 1e-2:
        x2 = x * x
        sinh_x = x * (1 + x2 * (1/6 + x2 / 120))
    elif abs(x) > 700:
        return 1.0
    else:
        try:
            sinh_x = np.sinh(x)
        except (OverflowError, RuntimeWarning):
            return 1.0
    ratio = (kappa * sinh_x) / r
    if not np.isfinite(ratio) or ratio <= 0.0:
        return 1.0
    return ratio

def pi_a_over_pi_high_precision(r: float, kappa: float, precision: int = 50) -> float:
    try:
        from mpmath import mp, sinh
        original_dps = mp.dps; mp.dps = precision
        try:
            if abs(r) < 1e-50 or abs(kappa) < 1e-50:
                return 1.0
            result = float((kappa * sinh(r / kappa)) / r)
            return result if np.isfinite(result) and result > 0 else 1.0
        finally:
            mp.dps = original_dps
    except ImportError:
        return pi_a_over_pi(r, kappa)

def validate_hyperbolic_params(r: float, kappa: float) -> tuple[bool, str]:
    if not np.isfinite(r):
        return False, f"Radius must be finite, got: {r}"
    if not np.isfinite(kappa):
        return False, f"Curvature must be finite, got: {kappa}"
    if abs(kappa) < 1e-15 and abs(r) > 1e-10:
        return False, "Curvature too small for non-zero radius (near-singular geometry)"
    return True, "Parameters valid"

def adaptive_pi_metrics(r: float, kappa: float) -> dict:
    valid, msg = validate_hyperbolic_params(r, kappa)
    metrics = {
        'r': r,
        'kappa': kappa,
        'valid': valid,
        'validation_message': msg,
        'pi_a_over_pi': 1.0,
        'full_turn_degrees': 360.0,
        'curvature_type': 'euclidean',
        'stability_indicator': 'stable',
        'numerical_regime': 'standard'
    }
    if not valid:
        return metrics
    ratio = pi_a_over_pi(r, kappa)
    metrics['pi_a_over_pi'] = ratio
    metrics['full_turn_degrees'] = 360.0 * ratio
    if abs(kappa) < 1e-10:
        metrics['curvature_type'] = 'euclidean'
    elif kappa > 0:
        metrics['curvature_type'] = 'spherical'
    else:
        metrics['curvature_type'] = 'hyperbolic'
    if abs(r) < 1e-10 or abs(kappa) < 1e-10:
        metrics['numerical_regime'] = 'epsilon_fallback'
    elif abs(r / kappa) < 1e-2:
        metrics['numerical_regime'] = 'taylor_expansion'
    elif abs(r / kappa) > 100:
        metrics['numerical_regime'] = 'large_ratio_stable'
    else:
        metrics['numerical_regime'] = 'standard'
    if ratio == 1.0 and (abs(r) > 1e-10 and abs(kappa) > 1e-10):
        metrics['stability_indicator'] = 'fallback_triggered'
    elif not np.isfinite(ratio):
        metrics['stability_indicator'] = 'unstable'
    else:
        metrics['stability_indicator'] = 'stable'
    return metrics

def geodesic_distance(p1: tuple[float, float, float], p2: tuple[float, float, float], kappa: float) -> float:
    r1 = math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    r2 = math.sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2)
    if r1 == 0: return r2
    if r2 == 0: return r1
    dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
    cos_theta = max(min(dot / (r1 * r2), 1.0), -1.0)
    cosh_val = (math.cosh(r1 / kappa) * math.cosh(r2 / kappa) - math.sinh(r1 / kappa) * math.sinh(r2 / kappa) * cos_theta)
    cosh_val = max(cosh_val, 1.0)
    return kappa * math.acosh(cosh_val)

def move_towards(p: tuple[float,float,float], target: tuple[float,float,float], kappa: float, step: float) -> tuple[float,float,float]:
    dist = geodesic_distance(p, target, kappa)
    if dist == 0 or step <= 0: return p
    frac = min(step / dist, 1.0)
    return (p[0] + frac*(target[0]-p[0]), p[1] + frac*(target[1]-p[1]), p[2] + frac*(target[2]-p[2]))

class HyperbolicConstraint:
    def __init__(self, target: tuple[float,float,float], kappa: float):
        self.target = target; self.kappa = kappa
    def update(self, point: tuple[float,float,float], step: float = 0.1) -> tuple[float,float,float]:
        return move_towards(point, self.target, self.kappa, step)

__all__ = [
    'full_turn_deg','rotate_cmd','pi_a_over_pi','pi_a_over_pi_high_precision','validate_hyperbolic_params',
    'adaptive_pi_metrics','geodesic_distance','move_towards','HyperbolicConstraint'
]
