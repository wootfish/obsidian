from obsidian import Canvas, Group, EQ
from obsidian.geometry import Circle, Rectangle, Point

# from obsidian.canvas import Canvas
# from obsidian.geometry import Circle, Rectangle, Point
# from obsidian.groups import Group
# from obsidian.infix import EQ

SQRT_2 = 2**0.5

WIDTH = 300
HEIGHT = 300

CIRCLE_STYLE = {"stroke": "#0000ff", "fill_opacity": "0"}
RECT_STYLE = {"stroke": "#ff0000", "fill_opacity": "0"}

circle = Circle(style=CIRCLE_STYLE)
square = Rectangle(style=RECT_STYLE)

g = Group([circle, square], [
    circle.center |EQ| square.center,
    circle.radius |EQ| WIDTH / 4,
    square.width |EQ| square.height,
    square.width |EQ| circle.radius * SQRT_2
])

canvas = Canvas(g, WIDTH, HEIGHT, bg_color="#e0e0e0")
canvas.save_png("gallery/circle_and_square.png")
canvas.save_svg("gallery/circle_and_square.svg")
