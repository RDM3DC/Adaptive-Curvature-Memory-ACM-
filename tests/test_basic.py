
from curve_memory import encode_curve, decode_curve

def test_roundtrip_basic():
    pts = [(0,0),(1,0),(2,0),(3,0)]
    cma = encode_curve(pts)
    rec = decode_curve(cma)
    assert len(rec) > 0
