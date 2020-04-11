from dataclasses import dataclass, fields
from numbers import Real as ABCReal

from obsidian.fields import SMTField

from pysmt.shortcuts import Real
from pysmt.typing import REAL


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

    Provides a __post_init__ method which replaces any real-annotated fields'
    values with their pysmt.Real equivalents, so that native Python numbers can
    be passed into shape dataclasses without issue.
    """

    def __post_init__(self):
        for field in fields(self):
            if field.type is not REAL:
                continue
            attr = getattr(self, field.name)
            if isinstance(attr, ABCReal):
                setattr(self, field.name, Real(attr))

    @property
    def bounds(self):
        raise NotImplementedError

    @property
    def center(self):
        from obsidian.geometry import Point
        bounds = self.bounds
        center_x = (bounds.left_edge + bounds.right_edge) / 2
        center_y = (bounds.top_edge + bounds.bottom_edge) / 2
        return Point(center_x, center_y)
