from dataclasses import dataclass
from typing import List
from pysmt.shortcuts import get_model, And, Min, Max, is_sat

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

    _bounds = None

    @property
    def bounds(self):
        if self._bounds is None:
            left_edge   = Min(shape.bounds.left_edge   for shape in self.shapes)
            right_edge  = Max(shape.bounds.right_edge  for shape in self.shapes)
            top_edge    = Min(shape.bounds.top_edge    for shape in self.shapes)
            bottom_edge = Max(shape.bounds.bottom_edge for shape in self.shapes)
            self._bounds = Bounds(left_edge, right_edge, top_edge, bottom_edge)
        return self._bounds

    @bounds.setter
    def bounds(self, val):
        self._bounds = val

    @property
    def center(self):
        bounds = self.bounds
        center_x = (bounds.left_edge + bounds.right_edge) / 2
        center_y = (bounds.top_edge + bounds.bottom_edge) / 2
        return Point(center_x, center_y)

    def solve(self):
        formula = And(self.constraints)
        model = get_model(formula)
        assert model is not None  # check for unsatisfiability
        return model  # TODO more, eg:
                      # - make solver configurable
                      # - detect & warn when there are multiple solutions
                      # - bring in extra constraints (if we decide to add any ways of specifying those)
                      # - maybe cache result?
