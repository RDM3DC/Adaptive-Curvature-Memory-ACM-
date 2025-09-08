
from typing import List
from .alphabet import Glyph

def wedge_contract(glyphs: List[Glyph]) -> List[Glyph]:
    """
    Placeholder for wedge-product based contraction rules.
    For now, perform a simple adjacent-family coalesce heuristic.
    """
    if not glyphs:
        return glyphs
    out = [glyphs[0]]
    for g in glyphs[1:]:
        if out and out[-1].family == g.family:
            # naive contraction by averaging parameters when identical families
            theta = dict(out[-1].theta)
            for k,v in g.theta.items():
                if k in theta and isinstance(theta[k], (int,float)) and isinstance(v, (int,float)):
                    theta[k] = 0.5*(theta[k]+v)
                else:
                    theta[k] = v
            out[-1] = type(out[-1])(family=out[-1].family, theta=theta, bind=0.5*(out[-1].bind+g.bind))
        else:
            out.append(g)
    return out
