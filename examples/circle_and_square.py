from obsidian.canvas import Canvas
from obsidian.shapes import Circle, Rectangle
from obsidian.group import Group
from obsidian.infix import EQ

from pysmt.shortcuts import Real

bg_style = {"fill": "#e0e0e0"}
circ_style = {"stroke": "#0000ff", "fill_opacity": "0"}
rect_style = {"stroke": "#ff0000", "fill_opacity": "0"}

width = 300
height = 300

bg = Rectangle(0, 0, width, height, bg_style)

circle = Circle(style=circ_style)
square = Rectangle(style=rect_style)

g = Group([bg, circle, square], [
    circle.bounds.center.x |EQ| bg.bounds.center.x,
    circle.bounds.center.x |EQ| square.bounds.center.x,
    circle.bounds.center.y |EQ| bg.bounds.center.y,
    circle.bounds.center.y |EQ| square.bounds.center.y,
    circle.radius |EQ| Real(width/4),
    square.width |EQ| square.height,
    square.width |EQ| circle.radius * 2**0.5
])

print("\n==== Shapes:")
for shape in g.shapes:
    print(shape)

print("\n==== Constraints:")
for constraint in g.constraints:
    print(constraint)

print("\nSolving...")
s = g.solve()

print("\n==== Solution:")
print(s)

print("\n==== Shape Parameters:")
print("\nSquare:")
for label, var in zip('xywh', (square.x, square.y, square.width, square.height)):
    print('    ' + label + ':', float(s[var].constant_value()))

print("\nCircle:")
for label, var in zip('xyr', (circle.x, circle.y, circle.radius)):
    print('    ' + label + ':', float(s[var].constant_value()))

print()


print("\n==== Rendering...")
canvas = Canvas(g, width, height)
canvas.save_png("gallery/circle_and_square.png")
canvas.save_svg("gallery/circle_and_square.svg")
