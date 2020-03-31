from random import Random
choice = Random(3**20 % (2**20-1)).choice  # arbitrary nontrivial constant seed

from obsidian.align import top_align, left_align
from obsidian.canvas import Canvas
from obsidian.group import Group
from obsidian.helpers import shape_grid
from obsidian.infix import EQ
from obsidian.shapes import Rectangle


width = 300
height = 300

BG = "#000000"
RED = "#AA1010"
BLUE = "#3030AA"

bg = Rectangle(0, 0, width, height, {"fill": BG})

squares = shape_grid(w=20, h=20, spacing=3,
        factory=lambda: Rectangle(width=10, height=10))

for square in squares.shapes:
    square.style = {"fill": choice((RED, BLUE))}

g = Group([squares, bg], [
    squares.bounds.center.x |EQ| bg.bounds.center.x,
    squares.bounds.center.y |EQ| bg.bounds.center.y,
    ])

print("Working...")
canvas = Canvas(g, width, height)
canvas.save_png("gallery/square_grid.png")
canvas.save_svg("gallery/square_grid.svg")
