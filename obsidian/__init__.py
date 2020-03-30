# in here we patch a bug in pysmt so we can use our infix operators

# basically: pysmt FNode instances override __or__, but when they get an
# unrecognized other argument they raise an exception instead of returning
# NotImplemented. Returning NotImplemented would cause Python to attempt to
# delegate to the right-hand argument's __ror__ method, and would raise a
# ValueError only if that is unsuccessful. This is the expected behavior.

# to fix this, we wrap FNode.__or__ with a handler that catches the exception
# and returns NotImpelemented so that Python's usual semantics are restored.

# i'll admit this is an ugly solution, but it's faster than a pull request :)


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
