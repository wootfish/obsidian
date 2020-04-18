"""
Note: may want to expand the list of supported comparisons
(to include eg GT LT GE LE)
"""


__all__ = ['EQ', 'NE', 'ABOVE_BY', 'BELOW_BY', 'LEFT_BY', 'RIGHT_BY']


from functools import wraps

from pysmt.shortcuts import And, Equals, NotEquals

from obsidian.helpers import wrap_real
from obsidian.geometry import Point


class Infix:
    """
    Cute little hack for defining custom infix operators.
    Attrib: https://code.activestate.com/recipes/384122/#c5
    Usage:

    >>> import operator
    >>> mul = Infix(operator.mul)
    >>> 4 |mul| 4
    16
    >>> div = Infix(operator.truediv)
    >>> 8 |div| (2 |div| 2)
    8.0
    """

    def __init__(self, f):
        self.f = f

    def __ror__(self, other):
        return Infix(lambda x: self.f(other, x))

    def __or__(self, other):
        return self.f(other)


def real_wrapper(f):
    """
    Wraps a two-argument function and ensures its arguments are pysmt Reals.
    """

    @wraps(f)
    def wrapper(lhs, rhs):
        return f(wrap_real(lhs), wrap_real(rhs))
    return wrapper


def point_equals(lhs, rhs):
    if isinstance(lhs, Point) and isinstance(rhs, Point):
        return And(Equals(lhs.x, rhs.x),
                   Equals(lhs.y, rhs.y))
    return Equals(lhs, rhs)


def point_not_equals(lhs, rhs):
    if isinstance(lhs, Point) and isinstance(rhs, Point):
        return Or(NotEquals(lhs.x, rhs.x),
                  NotEquals(lhs.y, rhs.y))
    return NotEquals(lhs, rhs)


EQ = Infix(real_wrapper(point_equals))
NE = Infix(real_wrapper(point_not_equals))


def ABOVE_BY(margin):
    """
    Returns an infix operator that takes two Shape arguments and returns a
    constraint positioning the first Shape's lower edge above the second Shape's
    top edge with a distance defined by `margin`.

    For instance, to position shape_1 ten pixels above shape_2, use:
    >>> shape_1 | ABOVE_BY(10) | shape_2

    The above expression is equivalent to:
    >>> shape_1.bounds.bottom_edge + 10 |EQ| shape_2.bounds.top_edge
    """

    return Infix(lambda s1, s2: Equals(
        s1.bounds.bottom_edge + margin,
        s2.bounds.top_edge
    ))


def BELOW_BY(margin):
    """
    Like ABOVE_BY but places the first shape below the second one.
    """

    return Infix(lambda s1, s2: Equals(
        s1.bounds.top_edge - margin,
        s2.bounds.bottom_edge
    ))


def LEFT_BY(margin):
    """
    Like ABOVE_BY but places the first shape to the left of the second one.
    """

    return Infix(lambda s1, s2: Equals(
        s1.bounds.right_edge + margin,
        s2.bounds.left_edge
    ))


def RIGHT_BY(margin):
    """
    Like ABOVE_BY but places the first shape to the right of the second one.
    """

    return Infix(lambda s1, s2: Equals(
        s1.bounds.left_edge - margin,
        s2.bounds.right_edge
    ))
