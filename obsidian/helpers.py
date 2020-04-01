from obsidian.arrange import top_align, left_align
from obsidian.group import Group
from obsidian.infix import EQ


def shape_grid(w, h, spacing, factory):
    """
    Returns a Group containing a grid of shapes with `h` rows and `w` columns.
    The margin between shapes is defined by `spacing`.
    `factory` must return uniform fresh instances of the shape to arrange.
    If instances from `factory` are not uniform, unexpected behavior may occur.

    The group's shapes' ordering is produced by flattening the grid in the
    natural way, i.e. by concatenating the lists for each row of shapes in
    order.

    This example produces a 5x5 grid of 10x10 squares with 2px margins:
    >>> grid = shape_grid(w=5, h=5, spacing=2,
            factory=lambda: Rectangle(width=10, height=10))
    """

    constraints = []
    grid = [[factory() for _ in range(w)] for _ in range(h)]

    # align rows and columns
    for row in grid:
        constraints += top_align(row)

    for col in range(w):
        constraints += left_align(row[col] for row in grid)

    # establish spacing between grid elements
    first_row = grid[0]
    first_col = [row[0] for row in grid]

    for a, b in zip(first_row, first_row[1:]):
        constraints.append(b.bounds.left_edge |EQ| a.bounds.right_edge + spacing)

    for a, b in zip(first_col, first_col[1:]):
        constraints.append(b.bounds.top_edge |EQ| a.bounds.bottom_edge + spacing)

    # flatten the grid
    shapes = [shape for row in grid for shape in row]

    return Group(shapes, constraints)
