from obsidian.shapes import Circle, Rectangle
from obsidian.style import Style
from obsidian.group import Group

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

g = Group([bg, circle, square], [
    Equals(circle.bounds.center.x, bg.bounds.center.x),
    Equals(circle.bounds.center.x, square.bounds.center.x),
    Equals(circle.bounds.center.y, bg.bounds.center.y),
    Equals(circle.bounds.center.y, square.bounds.center.y),
    Equals(circle.radius, Real(width/4)),
    Equals(square.width, square.height),
    Equals(square.width, circle.radius * 2**0.5)
])

print()
for shape in g.shapes:
    print(shape)
print()

s = g.solve()
print(s)

print()

print(s[square.x].constant_value())
print(s[square.y].constant_value())
print(s[square.width].constant_value())
print(s[square.height].constant_value())
