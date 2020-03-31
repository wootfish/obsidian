from dataclasses import dataclass
from obsidian.group import Group
from obsidian.shapes import Rectangle, Circle

import drawSvg as draw


def N(sym):
    """Returns raw numeric value for solved symbol."""
    return float(sym.constant_value())


def render_rect(rect, model, target):
    x = N(model[rect.x])
    y = N(model[rect.y])
    w = N(model[rect.width])
    h = N(model[rect.height])
    target.append(draw.Rectangle(x, y, w, h, **rect.style))


def render_circle(circle, model, target):
    x = N(model[circle.x])
    y = N(model[circle.y])
    r = N(model[circle.radius])
    target.append(draw.Circle(x, y, r, **circle.style))


renderers = {
    Rectangle: render_rect,
    Circle: render_circle
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

    def save_png(self, fname):
        if self.rendered is None:
            self.render()
        self.rendered.savePng(fname)
