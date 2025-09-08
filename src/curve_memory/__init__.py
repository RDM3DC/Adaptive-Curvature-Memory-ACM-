"""
curve_memory: Reference implementation of Curve Memory Alphabet (CMA).
"""
from .alphabet import Glyph, GlyphFamily
from .encoder import encode_curve
from .decoder import decode_curve
from .compression import wedge_contract
from .geometry import CurveFrame, CurveHash, kappa_tau_from_polyline
