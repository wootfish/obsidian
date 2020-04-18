from functools import wraps
from numbers import Real as ABCReal

from pysmt.shortcuts import Real, Equals

from obsidian.arrange import top_align, left_align
from obsidian.shape import Bounds


def wrap_real(x):
    return Real(x) if isinstance(x, ABCReal) else x


def cached_property(f):
    """
    Python adds functools.cached_property() in 3.8; since we're only targeting
    Python 3.7 we need to use this instead. This is implemented differently than
    functools.cached_property, but is functionally equivalent for our purposes.
    """

    @wraps(f)
    def get(self):
        try:
            return self.__property_cache[f]
        except AttributeError:
            self.__property_cache = {}
        except KeyError:
            pass
        x = self.__property_cache[f] = f(self)
        return x

    return property(get)


def N(sym):
    """Returns raw numeric value for solved symbol."""
    return float(sym.constant_value())


def maybe_get_from_model(val, model):
    """
    If val is a Python-native real, return val.
    Otherwise, attempt to resolve val within model and return the result.

    Useful for handling parameters which may be passed either as numeric
    constants or in terms of the solver's variables.
    """
    return val if isinstance(val, ABCReal) else N(model[val])
