from obsidian.shapes import Circle, Rectangle
from obsidian.style import Style
from obsidian.group import Group
from obsidian.infix import EQ

from pysmt.shortcuts import Equals, Real


width = 300
height = 300

bg = Rectangle.from_corner(0, 0, width, height, Style(None))

circle = Circle.new(Style(None))
square = Rectangle.new(Style(None))

# g = Group([bg, circle, square], [
#     circle.bounds.center == bg.bounds.center,
#     circle.bounds.center == square.bounds.center,
#     circle.radius == width/4,   # NOTE is this legal? using a raw float like this?
#     square.width == square.height,
#     square.width == circle.radius * 2**0.5
# ])

print(type(circle.bounds.center.x), type(bg.bounds.center.x))

g = Group([bg, circle, square], [
    circle.bounds.center.x |EQ| bg.bounds.center.x,
    circle.bounds.center.x |EQ| square.bounds.center.x,
    circle.bounds.center.y |EQ| bg.bounds.center.y,
    circle.bounds.center.y |EQ| square.bounds.center.y,
    circle.radius |EQ| Real(width/4),
    square.width |EQ| square.height,
    square.width |EQ| circle.radius * 2**0.5
])

print()
for shape in g.shapes:
    print(shape)
print()

s = g.solve()
print(s)

print()

for var in (square.x, square.y, square.width, square.height):
    print(float(s[var].constant_value()))
