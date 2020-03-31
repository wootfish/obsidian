from numbers import Real as ABCReal

from pysmt.shortcuts import Real


def wrap_real(x):
    return Real(x) if isinstance(x, ABCReal) else x
