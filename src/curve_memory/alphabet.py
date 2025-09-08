
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class GlyphFamily(str, Enum):
    ARC = "arc"
    CLOTHOID = "clothoid"
    CUBIC = "cubic"
    HELIX = "helix"
    CUSTOM = "custom"

@dataclass
class Glyph:
    family: GlyphFamily
    theta: Dict[str, Any]
    bind: float = 1.0  # ARP-managed weight
