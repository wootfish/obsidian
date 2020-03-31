"""
Notes:
may want to expand the list of supported comparisons
(to include eg GT LT GE LE)

also, "not" is currently omitted - should we export pysmt.shortcuts.Not as NOT for consistency? even though it's not an
infix? if we're doing that, should we rename this file?
"""


__all__ = ['AND', 'OR', 'EQ', 'NE']


from functools import wraps
from numbers import Real as ABCReal

from pysmt.shortcuts import And, Or, Not, Equals, NotEquals, Real

from obsidian.wrap import wrap_real


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
    @wraps(f)
    def wrapper(lhs, rhs):
        return f(wrap_real(lhs), wrap_real(rhs))
    return wrapper


AND = Infix(real_wrapper(And))
OR = Infix(real_wrapper(Or))
EQ = Infix(real_wrapper(Equals))
NE = Infix(real_wrapper(NotEquals))
