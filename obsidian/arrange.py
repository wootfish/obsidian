from pysmt.shortcuts import FreshSymbol, Equals, And
from pysmt.typing import REAL


# TODO these should probably take varargs, so we can just do e.g.
# left_align(shape_1, shape_2, shape_3)


def left_align(shapes):
    s = FreshSymbol(REAL)
    return And(Equals(shape.bounds.left_edge, s) for shape in shapes)


def right_align(shapes):
    s = FreshSymbol(REAL)
    return And(Equals(shape.bounds.right_edge, s) for shape in shapes)


def top_align(shapes):
    s = FreshSymbol(REAL)
    return And(Equals(shape.bounds.top_edge, s) for shape in shapes)


def bottom_align(shapes):
    s = FreshSymbol(REAL)
    return And(Equals(shape.bounds.bottom_edge, s) for shape in shapes)


def center_align_x(shapes):
    """
    Returns a constraint setting the shapes' centers' x-coordinates equal.
    """
    s = FreshSymbol(REAL)
    return And(Equals(shape.center.x, s) for shape in shapes)


def center_align_y(shapes):
    """
    Returns a constraint setting the shapes' centers' y-coordinates equal.
    """
    s = FreshSymbol(REAL)
    return And(Equals(shape.center.y, s) for shape in shapes)


def evenly_spaced(start_point, end_point, shapes):
    n = len(shapes)
    assert n > 1
    constraints = []
    for i in range(n):
        if shapes[i] is None:
            continue
        j = n - i - 1
        x = (start_point.x*j + end_point.x*i) / (n-1)
        y = (start_point.y*j + end_point.y*i) / (n-1)
        constraints.append(Equals(shapes[i].x, x))
        constraints.append(Equals(shapes[i].y, y))
    return And(constraints)
