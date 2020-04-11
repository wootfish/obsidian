from dataclasses import dataclass, field

from pysmt.shortcuts import Min, Max
from pysmt.typing import REAL

from obsidian.fields import StyleField, SMTField, STYLE
from obsidian.shape import Bounds, Shape


@dataclass
class Point(Shape):
    x: REAL = SMTField()
    y: REAL = SMTField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        x, y = self.x, self.y
        return Bounds(x, x, y, y)  # just a point!


def PointField(): return field(default_factory=Point)


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
