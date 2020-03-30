from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


Properties = Enum("Properties",
        "stroke stroke_weight "
        "fill fill_opacity "
        )
stroke, stroke_weight, fill, fill_opacity = Properties


@dataclass
class Style:
    styles: Dict[Properties, Any]
