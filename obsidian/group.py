from dataclasses import dataclass
from typing import List
from pysmt.shortcuts import get_model, And, Min, Max

from .shapes import Bounds, Shape, Point


@dataclass
class Group:
    shapes: List[Shape]
    constraints: List  # of pysmt constraints

    def __post_init__(self):
        # for convenience, we want to let the caller pass groups in alongside shapes
        # however, we can't leave these groups in self.shapes because we want it to have uniform type
        # so we filter the groups out here and merge their shape & constraint lists with our existing ones
        groups = [group for group in self.shapes if isinstance(group, Group)]
        self.shapes = [shape for shape in self.shapes if not isinstance(shape, Group)]
        for group in groups:
            self.shapes += group.shapes
            self.constraints += group.constraints

    @property
    def bounds(self):
        left_edge   = Min(shape.bounds.left_edge   for shape in self.shapes)
        right_edge  = Max(shape.bounds.right_edge  for shape in self.shapes)
        top_edge    = Min(shape.bounds.top_edge    for shape in self.shapes)
        bottom_edge = Max(shape.bounds.bottom_edge for shape in self.shapes)
        return Bounds(left_edge, right_edge, top_edge, bottom_edge)

    def solve(self):
        model = get_model(And(self.constraints))
        return model  # TODO more, eg:
                      # - make solver configurable
                      # - detect & warn when there are multiple solutions
                      # - bring in extra constraints (if we decide to add any ways of specifying those)
                      # - maybe cache result?
