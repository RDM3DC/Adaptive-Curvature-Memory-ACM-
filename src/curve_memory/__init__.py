"""
curve_memory: Reference implementation of Curve Memory Alphabet (CMA).
"""
from .alphabet import Glyph, GlyphFamily
from .encoder import encode_curve
from .decoder import decode_curve
from .compression import wedge_contract
from .geometry import CurveFrame, CurveHash, kappa_tau_from_polyline
from .cma3d import curve_memory_3d, reconstruct_from_memory, rmf_sweep

__all__ = [
	'Glyph', 'GlyphFamily', 'encode_curve', 'decode_curve', 'wedge_contract',
	'CurveFrame', 'CurveHash', 'kappa_tau_from_polyline',
	'curve_memory_3d', 'reconstruct_from_memory', 'rmf_sweep'
]
