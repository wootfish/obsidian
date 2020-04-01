from dataclasses import dataclass
from obsidian.group import Group
from obsidian.helpers import N
from obsidian.shapes import Rectangle, Circle, Line

import drawSvg as draw


def render_rect(rect, model, target):
    assert len(rect.style) > 0
    x = N(model[rect.x])
    y = N(model[rect.y])
    w = N(model[rect.width])
    h = N(model[rect.height])
    target.append(draw.Rectangle(x, y, w, h, **rect.style))


def render_circle(circle, model, target):
    assert len(circle.style) > 0
    x = N(model[circle.x])
    y = N(model[circle.y])
    r = N(model[circle.radius])
    target.append(draw.Circle(x, y, r, **circle.style))


def render_line(line, model, target):
    assert len(line.style) > 0
    x1, y1 = line.pt1.x, line.pt1.y
    x2, y2 = line.pt2.x, line.pt2.y
    target.append(draw.Line(x1, y1, x2, y2, **line.style))


renderers = {
    Rectangle: render_rect,
    Circle: render_circle,
    Line: render_line,
}


@dataclass
class Canvas:
    group: Group
    width: float
    height: float

    rendered = None

    def render(self):
        model = self.group.solve()
        drawing = draw.Drawing(self.width, self.height)

        for shape in self.group.shapes:
            renderer = renderers[type(shape)]
            renderer(shape, model, drawing)

        self.rendered = drawing

    def save_svg(self, fname):
        if self.rendered is None:
            self.render()
        self.rendered.saveSvg(fname)
        print("Wrote", fname)

    def save_png(self, fname):
        if self.rendered is None:
            self.render()
        self.rendered.savePng(fname)
        print("Wrote", fname)
