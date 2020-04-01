from dataclasses import dataclass, field, fields
from numbers import Real as ABCReal
from typing import Dict, Any

from pysmt.shortcuts import Real, FreshSymbol, And, Equals, Min, Max
from pysmt.typing import REAL

from obsidian.wrap import wrap_real


STYLE = Dict[str, Any]


# yo dawg i heard you like factories...
def SMTField(): return field(default_factory=lambda: FreshSymbol(REAL))
def StyleField(): return field(default_factory=dict)
def PointField(): return field(default_factory=Point)


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
    style: STYLE = StyleField()


@dataclass
class Bounds:
    left_edge: REAL = SMTField()
    right_edge: REAL = SMTField()
    top_edge: REAL = SMTField()
    bottom_edge: REAL = SMTField()

    def __post_init__(self):
        self.width = self.right_edge - self.left_edge
        self.height = self.bottom_edge - self.top_edge
        center_x = (self.left_edge + self.right_edge) / 2
        center_y = (self.top_edge + self.bottom_edge) / 2
        self.center = Point(center_x, center_y)


@dataclass
class Rectangle(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    width: REAL = SMTField()
    height: REAL = SMTField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        left_edge, right_edge = self.x, self.x + self.width
        top_edge, bottom_edge = self.y, self.y + self.height
        center_x = (left_edge + right_edge) / Real(2)
        center_y = (top_edge + bottom_edge) / Real(2)
        return Bounds(left_edge, right_edge, top_edge, bottom_edge)


@dataclass
class Circle(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    radius: REAL = SMTField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        left_edge, right_edge = self.x - self.radius, self.x + self.radius
        top_edge, bottom_edge = self.y - self.radius, self.y + self.radius
        diameter = 2 * self.radius
        return Bounds(left_edge, right_edge, top_edge, bottom_edge)


@dataclass
class Line(Shape):
    pt1: Point = PointField()
    pt2: Point = PointField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        xs = (self.pt1.x, self.pt2.x)
        ys = (self.pt1.y, self.pt2.y)
        left_edge, right_edge = Min(*xs), Max(*xs)
        top_edge, bottom_edge = Min(*ys), Max(*ys)
        return Bounds(left_edge, right_edge, top_edge, bottom_edge)
