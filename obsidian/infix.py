"""
Notes:
may want to expand the list of supported comparisons
(to include eg GT LT GE LE)

also, "not" is currently omitted - should we export pysmt.shortcuts.Not as NOT
for consistency? even though it's not an infix? if we're doing that, should we
rename this file?
"""


__all__ = ['EQ', 'NE']


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
