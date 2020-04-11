from dataclasses import field
from typing import Dict, Any

from pysmt.shortcuts import FreshSymbol
from pysmt.typing import REAL


def SMTField(): return field(default_factory=lambda: FreshSymbol(REAL))  # yo dawg i heard you like factories...
def StyleField(): return field(default_factory=dict)


STYLE = Dict[str, Any]
