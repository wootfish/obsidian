from dataclasses import dataclass
from typing import Callable

from obsidian.arrange import top_align, left_align
from obsidian.shape import Shape, Bounds
from obsidian.helpers import cached_property

from pysmt.fnode import FNode
from pysmt.shortcuts import Equals, And, Min, Max, get_model
from pysmt.typing import REAL


class Group(Shape):
    """For representing a collection of at least one Shape and any number of
    constraints, or for subclassing by shape group dataclasses.

    The expected pattern is for subclasses to define some fields and a
    __post_init__() method which uses the fields' values to initialize
    self.shapes and possibly extend self.constraints.

    If subclasses want Shape's Real -> pysmt.Real conversion feature, they must
    explicitly invoke it by calling super().__post_init__() within their own
    __post_init__() methods.
    """

    _bounds = None

    def __init__(self, shapes=None, constraints=None):
        self.shapes.extend(shapes or [])
        self.constraints.extend(constraints or [])

    @property
    def bounds(self):
        """Default bounds method. This is guaranteed to work, and should be fast
        enough with small number of shapes. Subclasses with large numbers of
        shapes may see performance benefits from overriding this method.
        """
        if self._bounds is None:
            left_edge   = Min(shape.bounds.left_edge   for shape in self.shapes)
            right_edge  = Max(shape.bounds.right_edge  for shape in self.shapes)
            top_edge    = Min(shape.bounds.top_edge    for shape in self.shapes)
            bottom_edge = Max(shape.bounds.bottom_edge for shape in self.shapes)
            self._bounds = Bounds(left_edge, right_edge, top_edge, bottom_edge)
        return self._bounds

    @cached_property
    def shapes(self):
        # can't set this in __init__ because we want it to be available to
        # dataclass subclasses
        return []

    @cached_property
    def constraints(self):
        constraints = []
        for shape in self.shapes:
            try: constraints.extend(shape.constraints)
            except AttributeError: pass
        return constraints

    def solve(self):
        formula = And(self.constraints)
        model = get_model(formula)
        assert model is not None  # check for unsatisfiability
        return model


@dataclass
class ShapeGrid(Group):
    """This is a Group containing a grid of shapes with `h` rows and `w` cols.
    The margin between shapes is defined by `spacing`.

    `factory` must return identical, unique instances of the shape to arrange.
    If instances from `factory` are not uniform, unexpected behavior may occur.

    The group's shapes' ordering is produced by flattening the grid in the
    natural way, i.e. by concatenating the lists for each row of shapes in
    order.

    This example builds a 5x5 grid of squares with 10px sides and 2px margins:
    >>> grid = ShapeGrid(w=5, h=5, spacing=2,
            factory=lambda: Rectangle(width=10, height=10))
    """

    w: REAL
    h: REAL
    spacing: REAL  # TODO does this one have to be explicitly defined?
    factory: Callable

    def __post_init__(self):
        w, h = self.w, self.h
        spacing = self.spacing
        factory = self.factory
        constraints = self.constraints

        grid = [[factory() for _ in range(w)] for _ in range(h)]

        # align rows and columns
        for row in grid:
            constraints.append(top_align(row))

        for col in range(w):
            constraints.append(left_align(row[col] for row in grid))

        # establish spacing between grid elements
        first_row = grid[0]
        first_col = [row[0] for row in grid]

        for a, b in zip(first_row, first_row[1:]):
            constraints.append(Equals(b.bounds.left_edge,
                                      a.bounds.right_edge + spacing))

        for a, b in zip(first_col, first_col[1:]):
            constraints.append(Equals(b.bounds.top_edge,
                                      a.bounds.bottom_edge + spacing))

        # flatten the grid and store it
        self.shapes.extend(shape for row in grid for shape in row)

    @cached_property
    def bounds(self):
        ul_bounds = self.shapes[0].bounds
        br_bounds = self.shapes[-1].bounds
        return Bounds(ul_bounds.left_edge, br_bounds.right_edge,
                      ul_bounds.top_edge, br_bounds.bottom_edge)

    def by_rows(self):
        yield from self.shapes

    def by_cols(self):
        for col in range(self.w):
            yield from self.shapes[col::self.w]
