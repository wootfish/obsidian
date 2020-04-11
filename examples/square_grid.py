from obsidian import Canvas, Group, ShapeGrid, EQ
from obsidian.geometry import Rectangle


grid_w = 5
grid_h = 2**5

BG = "#000000"
RED = "#AA1010"
BLUE = "#3030AA"

squares = ShapeGrid(w=grid_w, h=grid_h, spacing=3,
        factory=lambda: Rectangle(width=10, height=10))

for i, square in enumerate(squares.shapes):
    color = BLUE if (i // grid_w) & (2**(i%grid_w)) else RED
    square.style = {"fill": color}

print("Working...")
canvas = Canvas(squares, bg_color=BG)
canvas.save_png("gallery/square_grid.png")
canvas.save_svg("gallery/square_grid.svg")
