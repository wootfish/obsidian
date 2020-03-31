from random import choice

from obsidian.align import top_align, left_align
from obsidian.canvas import Canvas
from obsidian.shapes import Rectangle
from obsidian.group import Group
from obsidian.infix import EQ


width = 300
height = 300


BG = "#000000"
ZERO = "#1010AA"
ONE = "#AA1010"


def square_grid(w, h, size, spacing):
    grid = [[Rectangle(width=size, height=size) for _ in range(w)] for _ in range(h)]
    constraints = []

    # align rows and columns
    for row in grid:
        constraints += top_align(row)
    for col in range(w):
        constraints += left_align(row[col] for row in grid)

    # establish spacing between cells
    first_row = grid[0]
    first_col = [row[0] for row in grid]

    for a, b in zip(first_row, first_row[1:]):
        constraints.append(b.x |EQ| a.x + size + spacing)

    for a, b in zip(first_col, first_col[1:]):
        constraints.append(b.y |EQ| a.y + size + spacing)

    shapes = [rect for row in grid for rect in row]  # flattens the grid
    return Group(shapes, constraints)


bg = Rectangle(0, 0, width, height, {"fill": BG})


squares = square_grid(w=20, h=20, size=10, spacing=3)
for square in squares.shapes:
    square.style = {"fill": choice((ZERO, ONE))}


g = Group([squares, bg], [
    squares.bounds.center.x |EQ| bg.bounds.center.x,
    squares.bounds.center.y |EQ| bg.bounds.center.y,
    ])


print("Working...")
canvas = Canvas(g, width, height)
canvas.save_png("/tmp/test.png")
print("Saved to /tmp/test.png")
