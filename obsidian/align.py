from pysmt.shortcuts import FreshSymbol, Equals
from pysmt.typing import REAL


def left_align(shapes):
    s = FreshSymbol(REAL)
    return [Equals(shape.bounds.left_edge, s) for shape in shapes]


def right_align(shapes):
    s = FreshSymbol(REAL)
    return [Equals(shape.bounds.right_edge, s) for shape in shapes]


def top_align(shapes):
    s = FreshSymbol(REAL)
    return [Equals(shape.bounds.top_edge, s) for shape in shapes]


def bottom_align(shapes):
    s = FreshSymbol(REAL)
    return [Equals(shape.bounds.bottom_edge, s) for shape in shapes]
