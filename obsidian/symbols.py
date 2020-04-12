from dataclasses import dataclass

from numbers import Real as ABCReal

from obsidian.shape import Bounds, Shape
from obsidian.groups import Group
from obsidian.geometry import Point, Circle, Line, PointField
from obsidian.fields import SMTField, StyleField, STYLE
from obsidian.infix import EQ

from pysmt.typing import REAL


@dataclass
class Text(Shape):
    text: str
    font_size: ABCReal = 16
    anchor_point: Point = PointField()
    style: STYLE = StyleField()

    @property
    def bounds(self):
        # FIXME: this class does not know how to compute its bounds!
        # Maybe some clever font nerd can figure those out, but not me.

        # Currently it just says the edges all intersect the anchor point, which
        # is not very helpful (but is necessary for using this shape in Groups).

        # Note that even without meaningful bounds you can still left-, center-,
        # or right-align text. You just have to do it via styling. See
        # examples/go_board.py for a sample of what this might look like.

        x = self.anchor_point.x
        y = self.anchor_point.y
        return Bounds(x, x, y, y)


@dataclass
class XorSymbol(Group):
    diameter: REAL = SMTField()
    style: STYLE = StyleField()  # suggested fields: 'stroke', 'stroke_width'

    def __post_init__(self):
        shapes = self.shapes
        constraints = self.constraints

        circle = Circle(style=self.style)
        top_pt = Point(circle.center.x, circle.bounds.top_edge)
        left_pt = Point(circle.bounds.left_edge, circle.center.y)
        right_pt = Point(circle.bounds.right_edge, circle.center.y)
        bottom_pt = Point(circle.center.x, circle.bounds.bottom_edge)
        h_line = Line(left_pt, right_pt, style=self.style)
        v_line = Line(top_pt, bottom_pt, style=self.style)

        shapes += [circle, h_line, v_line]
        constraints += [circle.bounds.width |EQ| self.diameter]


@dataclass
class EqSymbol(Group):
    w: REAL = SMTField()
    h: REAL = SMTField()
    style: STYLE = StyleField()  # suggested fields: 'stroke', 'stroke_width'

    def __post_init__(self):
        shapes = self.shapes
        constraints = self.constraints

        line_1 = Line(style=self.style)
        line_2 = Line(style=self.style)

        shapes += [line_1, line_2]
        constraints += [
            line_1.pt1.y |EQ| line_1.pt2.y,           # line 1 is horizontal
            line_2.pt1.y |EQ| line_2.pt2.y,           # line 2 is horizontal
            line_2.pt1.y |EQ| line_1.pt1.y + self.h,  # line 2 is below line 1
            line_1.pt2.x |EQ| line_1.pt1.x + self.w,  # line 1 has width w
            line_2.pt1.x |EQ| line_1.pt1.x,           # line 2's left point is below line 1's
            line_2.pt2.x |EQ| line_1.pt2.x,           # line 2's right point is below line 1's
        ]
