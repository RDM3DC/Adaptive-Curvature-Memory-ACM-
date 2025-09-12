"""CMA-3D: 3D Curve Memory representation.

A compact, rigid-motion-invariant representation of 3D space curves using
arclength-normalized curvature kappa(s) and torsion tau(s), plus multi-scale summaries.

Public functions:
    curve_memory_3d(points, *, levels=3)
    reconstruct_from_memory(mem, *, ds=None, start=None, frame=None)
    rmf_sweep(points)

This is a standalone helper module (numpy-only) and not yet tightly
integrated with the 2D Curve Memory Alphabet pipeline.
"""
from __future__ import annotations
from typing import Dict, Any, Optional, Tuple
import numpy as np

_EPS = 1e-12

def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    n = np.clip(n, _EPS, None)
    return v / n

def _safe_angle(u: np.ndarray, v: np.ndarray) -> float:
    dot = np.clip(np.dot(u, v), -1.0, 1.0)
    return float(np.arccos(dot))

def poly_arclength(points: np.ndarray):
    diffs = np.diff(points, axis=0)
    seg_len = np.linalg.norm(diffs, axis=1)
    s = np.empty(points.shape[0])
    s[0] = 0.0
    s[1:] = np.cumsum(seg_len)
    L = float(s[-1])
    return seg_len, s, L

def discrete_tangent(points: np.ndarray) -> np.ndarray:
    diffs = np.diff(points, axis=0)
    if diffs.size == 0:
        return np.zeros_like(points)
    T_seg = _normalize(diffs)
    Np = points.shape[0]
    T_v = np.zeros_like(points)
    T_v[0] = T_seg[0]
    T_v[-1] = T_seg[-1]
    if Np > 2:
        T_v[1:-1] = _normalize(T_seg[:-1] + T_seg[1:])
    return T_v

def discrete_curvature(points: np.ndarray, s: np.ndarray) -> np.ndarray:
    N = points.shape[0]
    if N < 3:
        return np.zeros(N)
    diffs = np.diff(points, axis=0)
    Lseg = np.linalg.norm(diffs, axis=1)
    T = discrete_tangent(points)
    kappa = np.zeros(N)
    for i in range(1, N-1):
        ds = 0.5*(Lseg[i-1] + Lseg[i])
        dT = T[i] - T[i-1]
        kappa[i] = np.linalg.norm(dT) / max(ds, _EPS)
    if N >= 2:
        kappa[0] = kappa[1]
        kappa[-1] = kappa[-2]
    return kappa

def discrete_torsion(points: np.ndarray, s: np.ndarray) -> np.ndarray:
    N = points.shape[0]
    if N < 4:
        return np.zeros(N)
    diffs = np.diff(points, axis=0)
    Lseg = np.linalg.norm(diffs, axis=1)
    T = discrete_tangent(points)
    B = np.zeros_like(points)
    for i in range(1, N):
        cross = np.cross(T[i], T[i-1])
        nrm = np.linalg.norm(cross)
        if nrm < 1e-9:
            B[i] = B[i-1] if i > 1 else np.array([0.0, 0.0, 1.0])
        else:
            B[i] = cross / nrm
    B[0] = B[1]
    tau = np.zeros(N)
    for i in range(2, N-1):
        ds = 0.5*(Lseg[i-1] + Lseg[i])
        bi_1 = B[i-1]
        bi = B[i]
        ang = _safe_angle(bi_1, bi)
        sgn = np.sign(np.dot(np.cross(bi_1, bi), T[i]))
        tau[i] = sgn * ang / max(ds, _EPS)
    tau[0] = tau[1]
    tau[1] = tau[2]
    tau[-1] = tau[-2]
    return tau

def multiscale_pack(u: np.ndarray, kappa: np.ndarray, tau: np.ndarray, levels: int = 3) -> Dict[str, Any]:
    packs = []
    ku, tu = kappa.copy(), tau.copy()
    uu = u.copy()
    for _ in range(max(1, levels)):
        packs.append({
            'u': uu,
            'kappa': ku,
            'tau': tu,
            'stats': {
                'kappa_mean': float(np.mean(ku)),
                'kappa_std': float(np.std(ku)),
                'kappa_max': float(np.max(ku)),
                'kappa_min': float(np.min(ku)),
                'tau_mean': float(np.mean(tu)),
                'tau_std': float(np.std(tu)),
                'tau_max': float(np.max(tu)),
                'tau_min': float(np.min(tu)),
            }
        })
        idx = np.linspace(0, uu.shape[0]-1, max(2, (uu.shape[0]+1)//2)).astype(int)
        uu = uu[idx]; ku = ku[idx]; tu = tu[idx]
    return {
        'levels': packs,
        'global': {
            'kappa_L1': float(np.trapz(np.abs(kappa), u)),
            'tau_L1': float(np.trapz(np.abs(tau), u)),
            'kappa_L2': float(np.sqrt(np.trapz(kappa*kappa, u))),
            'tau_L2': float(np.sqrt(np.trapz(tau*tau, u))),
        }
    }

def curve_memory_3d(points: np.ndarray, *, levels: int = 3) -> Dict[str, Any]:
    points = np.asarray(points, dtype=float)
    assert points.ndim == 2 and points.shape[1] == 3, "points must be (N,3)"
    seg_len, s, L = poly_arclength(points)
    if L < _EPS:
        u = s*0.0
        kappa = np.zeros_like(s)
        tau = np.zeros_like(s)
        return {'L': 0.0, 'u': u, 'kappa': kappa, 'tau': tau, 'pack': multiscale_pack(u, kappa, tau, levels)}
    u = s / L
    kappa = discrete_curvature(points, s)
    tau = discrete_torsion(points, s)
    return {'L': float(L), 'u': u, 'kappa': kappa, 'tau': tau, 'pack': multiscale_pack(u, kappa, tau, levels)}

def frenet_step(T: np.ndarray, N: np.ndarray, B: np.ndarray, k: float, t: float, ds: float):
    ang_k = k * ds
    c = np.cos(ang_k); s = np.sin(ang_k)
    T_new = c*T + s*N
    N_new = -s*T + c*N
    B_new = B
    ang_t = t * ds
    ct = np.cos(ang_t); st = np.sin(ang_t)
    N_final = ct*N_new + st*np.cross(T_new, N_new)
    B_final = np.cross(T_new, N_final)
    T_final = _normalize(T_new); N_final = _normalize(N_final); B_final = _normalize(B_final)
    return T_final, N_final, B_final

def reconstruct_from_memory(mem: Dict[str, Any], *, ds: Optional[float] = None,
                             start: Optional[np.ndarray] = None,
                             frame: Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]] = None) -> np.ndarray:
    u = mem['u']; kappa = mem['kappa']; tau = mem['tau']; L = float(mem['L'])
    if L < _EPS:
        return np.zeros((2,3))
    def interp(arr, u_query):
        return np.interp(u_query, u, arr)
    M = max(50, u.shape[0])
    ds = (L / M) if ds is None else float(ds)
    M = max(2, int(np.ceil(L / max(ds, _EPS))))
    p = np.zeros(3) if start is None else np.asarray(start, float)
    if frame is None:
        T = np.array([1.0, 0.0, 0.0]); N = np.array([0.0, 1.0, 0.0]); B = np.array([0.0, 0.0, 1.0])
    else:
        T, N, B = frame; T = _normalize(np.asarray(T,float)); N = _normalize(np.asarray(N,float)); B = _normalize(np.asarray(B,float))
    pts = [p.copy()]; s_acc = 0.0
    for _ in range(M-1):
        s_acc = min(L, s_acc + ds)
        uq = s_acc / L
        k = float(interp(kappa, uq)); t = float(interp(tau, uq))
        T, N, B = frenet_step(T, N, B, k, t, ds)
        p = p + T * ds
        pts.append(p.copy())
    return np.stack(pts, axis=0)

def rmf_sweep(points: np.ndarray):
    pts = np.asarray(points, float)
    Np = pts.shape[0]
    T = discrete_tangent(pts)
    Nv = np.zeros_like(pts); Bv = np.zeros_like(pts)
    a = np.array([1.0,0.0,0.0])
    if Np == 0:
        return T, Nv, Bv
    if abs(np.dot(a, T[0])) > 0.9:
        a = np.array([0.0,1.0,0.0])
    Bv[0] = _normalize(np.cross(T[0], a))
    Nv[0] = _normalize(np.cross(Bv[0], T[0]))
    for i in range(1, Np):
        vT = T[i]
        Np_i = _normalize(Nv[i-1] - vT * np.dot(vT, Nv[i-1]))
        Bp_i = _normalize(np.cross(vT, Np_i))
        Nv[i] = Np_i; Bv[i] = Bp_i
    return T, Nv, Bv

__all__ = [
    'curve_memory_3d',
    'reconstruct_from_memory',
    'rmf_sweep'
]

if __name__ == "__main__":
    t = np.linspace(0, 6*np.pi, 600)
    pts = np.stack([np.cos(t), np.sin(t), 0.1*t], axis=1)
    mem = curve_memory_3d(pts, levels=3)
    rec = reconstruct_from_memory(mem, ds=mem['L']/600)
    print('mem keys:', list(mem.keys()))
    print('rec shape:', rec.shape)
