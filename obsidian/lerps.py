from typing import Tuple


"""
Linear interpolation algorithms for numbers, colors, etc.

TODO: Color lerp that does a better job of providing visual linearity.
      (lol that's gonna suck to write... fuck a perceptual color space)
"""


def _parse_color(c):  # c: str
    return (int(c[1:3], 16),
            int(c[3:5], 16),
            int(c[5:7], 16))

def _nf(n):
    """Packs a number n to 2-digit hex, suitable for use in color codes."""
    assert 0 <= n <= 255
    return hex(n)[2:].rjust(2, '0')

def _pack_color(c):  # c: Tuple[int]
    return "#" + ''.join(map(_nf, c))

def lerp_floats(f1, f2, steps):
    """Interpolates from f1 to f2 over `steps` steps and returns a tuple
    including both endpoints as well as any intermediate values.

    (Note: this is NOT immune to floating point weirdness! The classic
    pathological examples do in fact all apply here. Caveat emptor.)

    >>> lerp_floats(1.5, 5, steps=7)
    (1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
    >>> lerp_floats(1.5, 5, 5)
    (1.5, 2.2, 2.9, 3.5999999999999996, 4.3, 5.0)
    """

    step_size = (f2-f1) / steps
    return tuple(f1 + i*step_size for i in range(steps+1))

def lerp_ints(i1, i2, steps):
    return tuple(round(f) for f in lerp_floats(i1, i2, steps))

def lerp_colors(c1, c2, steps):
    """
    Expects colors formatted like #0069FF
    Outputs them in the same format
    """

    t1 = _parse_color(c1)
    t2 = _parse_color(c2)

    return tuple(_pack_color(t) for t in zip(
        lerp_ints(t1[0], t2[0], steps),
        lerp_ints(t1[1], t2[1], steps),
        lerp_ints(t1[2], t2[2], steps)
    ))
