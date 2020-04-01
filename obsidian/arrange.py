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


def evenly_spaced(start_point, end_point, shapes):
    n = len(shapes)
    assert n > 1
    constraints = []
    for i in range(n):
        j = n - i - 1
        x = (start_point.x*j + end_point.x*i) / (n-1)
        y = (start_point.y*j + end_point.y*i) / (n-1)
        constraints.append(Equals(shapes[i].x, x))
        constraints.append(Equals(shapes[i].y, y))
    return constraints
