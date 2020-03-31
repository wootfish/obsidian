from dataclasses import dataclass, field, fields
from numbers import Real as ABCReal
from typing import Dict, Any

from pysmt.shortcuts import Real, FreshSymbol, And, Equals
from pysmt.typing import REAL

from obsidian.wrap import wrap_real


STYLE = Dict[str, Any]


def SMTField(): return field(default_factory=lambda: FreshSymbol(REAL))


class Shape:
    """For subclassing by data classes.

    Provides a __post_init__ method which looks for any fields annotated as REAL
    and, if their values are instances of numbers.Real, wraps their values with
    pysmt.shortcuts.Real() to keep them from breaking infix notation. This
    allows callers of __init__ to pass in Python-native ints, floats, etc, to
    dataclass constructors in place of pysmt literals without issue.
    """

    def __post_init__(self):
        for field in fields(self):
            if field.type is not REAL: continue
            attr = getattr(self, field.name)
            if isinstance(attr, ABCReal): setattr(self, field.name, Real(attr))


@dataclass
class Point(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    style: STYLE = field(default_factory=dict)


@dataclass
class Bounds:
    left_edge: REAL = SMTField()
    right_edge: REAL = SMTField()
    top_edge: REAL = SMTField()
    bottom_edge: REAL = SMTField()
    width: REAL = SMTField()
    height: REAL = SMTField()
    center: Point = field(default_factory=Point)


@dataclass
class Rectangle(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    width: REAL = SMTField()
    height: REAL = SMTField()
    style: STYLE = field(default_factory=dict)

    @property
    def bounds(self):
        left_edge, right_edge = self.x, self.x + self.width
        top_edge, bottom_edge = self.y, self.y + self.height
        center_x = (left_edge + right_edge) / Real(2)
        center_y = (top_edge + bottom_edge) / Real(2)
        return Bounds(left_edge, right_edge, top_edge, bottom_edge,
                self.width, self.height, Point(center_x, center_y))


@dataclass
class Circle(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    radius: REAL = SMTField()
    style: STYLE = field(default_factory=dict)

    @property
    def bounds(self):
        left_edge, right_edge = self.x - self.radius, self.x + self.radius
        top_edge, bottom_edge = self.y - self.radius, self.y + self.radius
        diameter = 2 * self.radius
        return Bounds(left_edge, right_edge, top_edge, bottom_edge,
                diameter, diameter, Point(self.x, self.y))
