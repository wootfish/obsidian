from dataclasses import dataclass
from obsidian.group import Group
from obsidian.helpers import N
from obsidian.shapes import Rectangle, Circle, Line, Text

import drawSvg as draw


def M(sym, drawing):
    """
    Intended for y-coordinates. Works like N(), but also flips the value along
    the y-axis. An act of open rebellion against drawSvg.

    In Obsidian, the origin is in the top left with the +y direction pointing
    down. drawSvg places it in the bottom left, with +y pointing upward. This
    function simplifies conversions. Some render methods may need additional
    adjustment (e.g. render_rect must additionally adjust by rect height).
    """
    return drawing.height - N(sym)



def render_rect(rect, model, target):
    assert len(rect.style) > 0
    w = N(model[rect.width])
    h = N(model[rect.height])
    x = N(model[rect.x])
    y = M(model[rect.y], target) - h
    target.append(draw.Rectangle(x, y, w, h, **rect.style))


def render_circle(circle, model, target):
    assert len(circle.style) > 0
    x = N(model[circle.x])
    y = M(model[circle.y], target)
    r = N(model[circle.radius])
    target.append(draw.Circle(x, y, r, **circle.style))


def render_line(line, model, target):
    assert len(line.style) > 0
    x1, y1 = N(model[line.pt1.x]), M(model[line.pt1.y], target)
    x2, y2 = N(model[line.pt2.x]), M(model[line.pt2.y], target)
    target.append(draw.Line(x1, y1, x2, y2, **line.style))


def render_text(text, model, target):
    x = N(model[text.anchor_point.x])
    y = M(model[text.anchor_point.y], target)
    target.append(draw.Text(text.text, text.font_size, x, y, center=True, **text.style))


renderers = {
    Rectangle: render_rect,
    Circle: render_circle,
    Line: render_line,
    Text: render_text,
}


@dataclass
class Canvas:
    group: Group
    width: float = None
    height: float = None

    rendered = None

    def render(self):
        bounds = self.group.bounds
        model = self.group.solve()
        width = self.width or int(N(model[bounds.right_edge]))
        height = self.height or int(N(model[bounds.bottom_edge]))

        drawing = draw.Drawing(width, height)

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
