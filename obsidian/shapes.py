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


@dataclass
class Bounds:
    left_edge: REAL = SMTField()
    right_edge: REAL = SMTField()
    top_edge: REAL = SMTField()
    bottom_edge: REAL = SMTField()

    def __post_init__(self):
        self.width = self.right_edge - self.left_edge
        self.height = self.bottom_edge - self.top_edge


class Shape:
    """For subclassing by shape dataclasses.

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

    # question: is there a non-ugly way to ensure that the values of the
    # bounds() and center() properties are cached, not regenerated on each
    # access? this would likely improve performance by a lot

    @property
    def bounds(self):
        raise NotImplementedError

    @property
    def center(self):
        bounds = self.bounds
        center_x = (bounds.left_edge + bounds.right_edge) / 2
        center_y = (bounds.top_edge + bounds.bottom_edge) / 2
        return Point(center_x, center_y)


@dataclass
class Point(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        x, y = self.x, self.y
        return Bounds(x, x, y, y)  # just a point!


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


@dataclass
class Text(Shape):
    text: str
    font_size: ABCReal
    anchor_point: Point = PointField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        # FIXME: this class does not know how to compute its bounds!
        # maybe some clever font nerd can figure out how to compute those, but
        # not me.

        # currently it just says the edges all intersect the anchor point, which
        # is not very helpful (but is necessary for using this shape in Groups)

        # Note that even without meaningful bounds you can still left-, center-,
        # or right-align text. You just have to do it via styling. See
        # examples/go_board.py to get an idea of how this works.

        x = self.anchor_point.x
        y = self.anchor_point.y
        return Bounds(x, x, y, y)
