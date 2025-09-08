from curve_memory import encode_curve
from curve_memory.compression import wedge_contract

def test_wedge_contract_basic():
    pts = [(0,0),(1,0),(2,0),(3,0)]
    cma = encode_curve(pts)
    glyphs = [type("Obj", (), g) for g in cma["glyphs"]]
    # dummy Glyph-like objects
    contracted = wedge_contract(glyphs)
    assert isinstance(contracted, list)
    assert len(contracted) <= len(glyphs)
