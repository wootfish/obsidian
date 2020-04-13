from obsidian import Canvas, Group, ShapeGrid, EQ
from obsidian.geometry import Rectangle

GRID_W = 5
GRID_H = 2**5
SPACING = 3

BG = "#000000"
RED = "#AA1010"
BLUE = "#3030AA"

squares = ShapeGrid(w=GRID_W, h=GRID_H, spacing=SPACING,
        factory=lambda: Rectangle(width=10, height=10))

for i, square in enumerate(squares.shapes):
    mask = 2 ** (GRID_W - 1 - (i % GRID_W))
    color = BLUE if (i // GRID_W) & mask else RED
    square.style = {"fill": color}

canvas_w = squares.bounds.width + 2*SPACING
canvas_h = squares.bounds.height + 2*SPACING
canvas = Canvas(squares, canvas_w, canvas_h, bg_color=BG)
canvas.save_png("gallery/square_grid.png")
canvas.save_svg("gallery/square_grid.svg")
