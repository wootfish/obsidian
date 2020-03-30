from dataclasses import dataclass

from pysmt.shortcuts import Real, FreshSymbol, And
from pysmt.typing import REAL

from .style import Style


@dataclass
class Point:
    x: REAL
    y: REAL

    @classmethod
    def new(cls, x=None, y=None):
        return cls(FreshSymbol(REAL) if x is None else Real(x),
                   FreshSymbol(REAL) if y is None else Real(y))

    def __eq__(self, other):
        return And(self.x == other.x, self.y == other.y)


@dataclass
class Bounds:
    left_edge: REAL
    right_edge: REAL
    top_edge: REAL
    bottom_edge: REAL
    width: REAL
    height: REAL
    center: Point


@dataclass
class Rectangle:
    x: REAL
    y: REAL
    width: REAL
    height: REAL
    style: Style

    @classmethod
    def new(cls, style):
        x, y = FreshSymbol(REAL), FreshSymbol(REAL)
        w, h = FreshSymbol(REAL), FreshSymbol(REAL)
        return cls(x, y, w, h, style)

    @classmethod
    def from_corner(cls, x, y, width, height, style):
        return cls(Real(x), Real(y), Real(width), Real(height), style)

    @property
    def bounds(self):
        left_edge, right_edge = self.x, self.x + self.width
        top_edge, bottom_edge = self.y, self.y + self.height
        center_x = (left_edge + right_edge) / Real(2)
        center_y = (top_edge + bottom_edge) / Real(2)
        return Bounds(left_edge, right_edge, top_edge, bottom_edge,
                self.width, self.height, Point(center_x, center_y))


@dataclass
class Circle:
    x: REAL
    y: REAL
    radius: REAL
    style: Style

    @classmethod
    def new(cls, style):
        x, y, r = FreshSymbol(REAL), FreshSymbol(REAL), FreshSymbol(REAL)
        return cls(x, y, r, style)

    @property
    def bounds(self):
        left_edge, right_edge = self.x - self.radius, self.x + self.radius
        top_edge, bottom_edge = self.y - self.radius, self.y + self.radius
        diameter = 2 * self.radius
        return Bounds(left_edge, right_edge, top_edge, bottom_edge,
                diameter, diameter, Point(self.x, self.y))
