# make some commonly used classes available at the module level


__all__ = ("Canvas", "Alignments", "TOP_LEFT", "TOP_RIGHT", "BOT_LEFT",
        "BOT_RIGHT", "CENTER", "Group", "ShapeGrid", "AND", "OR", "EQ", "NE",
        "arrange", "geometry", "symbols")


from .canvas import Canvas
from .canvas import Alignments, TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT, CENTER
from .groups import Group, ShapeGrid
from .infix import AND, OR, EQ, NE


# here we patch a bug in pysmt so we can use our infix operators

# in brief: pysmt FNode instances override __or__, but when they get an
# unrecognized `other` argument they raise an exception instead of returning
# NotImplemented. Returning NotImplemented would cause Python to attempt to
# delegate to the right-hand argument's __ror__ method, and would raise a
# ValueError only if that is also unsuccessful. This is the expected behavior.

# to fix this, we wrap FNode.__or__ with a handler that catches the exception
# and returns NotImpelemented so that Python's usual semantics are restored.


from functools import wraps
from pysmt.fnode import FNode
from pysmt.exceptions import PysmtTypeError


def make_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except PysmtTypeError:
            return NotImplemented
    return wrapper


FNode.__or__ = make_wrapper(FNode.__or__)
