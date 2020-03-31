from dataclasses import dataclass
from typing import List
from pysmt.shortcuts import get_model, And, Min, Max

from .shapes import Bounds, Shape


@dataclass
class Group:
    shapes: List[Shape]
    constraints: List  # of pysmt constraints

    @property
    def bounds(self):
        left_edge   = Min(shape.bounds.left_edge   for shape in self.shapes)
        right_edge  = Max(shape.bounds.right_edge  for shape in self.shapes)
        top_edge    = Min(shape.bounds.top_edge    for shape in self.shapes)
        bottom_edge = Max(shape.bounds.bottom_edge for shape in self.shapes)
        width, height = right_edge - left_edge, bottom_edge - top_edge
        center_x = (left_edge + right_edge) / 2
        center_y = (top_edge + bottom_edge) / 2
        return Bounds(left_edge, right_edge, top_edge, bottom_edge,
                width, height, Point(center_x, center_y))

    def solve(self):
        model = get_model(And(self.constraints))
        return model  # TODO more (eg make solver configurable, detect when there are multiple solutions, draw in extra constraints if we decide to add any ways of specifying those)

    @classmethod
    def from_groups(cls, *groups):
        shapes = [shape for group in groups for shape in group.shapes]
        constraints = [constraint for group in groups for constraint in group.constraints]
        return cls(shapes, constraints)
