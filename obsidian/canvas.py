from dataclasses import dataclass
from enum import Enum

from .groups import Group
from .helpers import N
from .infix import EQ
from .geometry import Rectangle, Circle, Line, Point
from .symbols import Text

import drawSvg as draw


Alignments = Enum("Alignments", "TOP_LEFT TOP_RIGHT BOT_LEFT BOT_RIGHT CENTER")
TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT, CENTER = Alignments


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


def render_shape(shape, model, target):
    if isinstance(shape, Group):
        for subshape in shape.shapes:
            render_shape(subshape, model, target)
    else:
        assert type(shape) in renderers  # make sure we know how to render this
        renderer = renderers[type(shape)]
        renderer(shape, model, target)


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
    bg_color: str = None
    alignment: Alignments = CENTER  # if alignment is None, we won't add
                                    # constraints to place the group's center
                                    # anywhere specific on the canvas - in this
                                    # case, the user is responsible for making
                                    # sure the group is positioned correctly

    model = None
    rendered = None

    def render(self, use_cached_model=False):
        bounds = self.group.bounds
        width = self.width or bounds.width
        height = self.height or bounds.height

        align_rules = []
        if self.alignment in (TOP_LEFT, TOP_RIGHT):
            align_rules += [bounds.top_edge |EQ| 0]
        if self.alignment in (BOT_LEFT, BOT_RIGHT):
            align_rules += [bounds.bottom_edge |EQ| height]
        if self.alignment in (TOP_LEFT, BOT_LEFT):
            align_rules += [bounds.left_edge |EQ| 0]
        if self.alignment in (TOP_RIGHT, BOT_RIGHT):
            align_rules += [bounds.right_edge |EQ| width]
        if self.alignment is CENTER:
            align_rules += [self.group.center |EQ| Point(width/2, height/2)]

        if align_rules:
            group = Group([self.group], align_rules)
        else:
            group = self.group

        if use_cached_model and self.model is not None:
            model = self.model
        else:
            model = self.model = group.solve()

        # if width or height ended up depending on bounds, convert to int now
        width = width if isinstance(width, int) else int(N(model[width]))
        height = height if isinstance(height, int) else int(N(model[height]))

        drawing = draw.Drawing(width, height)

        if self.bg_color is not None:
            bg = Rectangle(0, 0, width, height, {"fill": self.bg_color})
            render_rect(bg, model, drawing)

        render_shape(group, model, drawing)
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
