from dataclasses import dataclass
from enum import Enum
from functools import wraps

from .groups import Group
from .helpers import N, maybe_get_from_model
from .infix import EQ
from .geometry import Rectangle, Circle, Line, Point
from .symbols import Text

import drawSvg as draw


Alignments = Enum("Alignments", "TOP_LEFT TOP_RIGHT BOT_LEFT BOT_RIGHT CENTER")
TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT, CENTER = Alignments


class ModelCache:
    def __init__(self, model, cache):
        self.model = model
        self.cache = cache

    def __getitem__(self, item):
        cache = self.cache
        if item not in cache:
            cache[item] = self.model[item]
        return cache[item]


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


def style_join(base, extra):
    return dict(base, **extra)  # only works because we know all style dict keys will be str - we'll have to change this if they ever become something else (eg Enum elements)


def render_rect(rect, model, target, style=None):
    style = style_join(style or {}, rect.style)
    assert len(style) > 0
    w = N(model[rect.width])
    h = N(model[rect.height])
    x = N(model[rect.x])
    y = M(model[rect.y], target) - h
    target.append(draw.Rectangle(x, y, w, h, **style))


def render_circle(circle, model, target, style=None):
    style = style_join(style or {}, circle.style)
    assert len(style) > 0
    x = N(model[circle.x])
    y = M(model[circle.y], target)
    r = N(model[circle.radius])
    target.append(draw.Circle(x, y, r, **style))


def render_line(line, model, target, style=None):
    style = style_join(style or {}, line.style)
    assert len(style) > 0
    x1, y1 = N(model[line.pt1.x]), M(model[line.pt1.y], target)
    x2, y2 = N(model[line.pt2.x]), M(model[line.pt2.y], target)
    target.append(draw.Line(x1, y1, x2, y2, **style))


def render_text(text, model, target, style=None):
    style = style_join(style or {}, text.style)
    assert len(style) > 0
    x = N(model[text.anchor_point.x])
    y = M(model[text.anchor_point.y], target)
    target.append(draw.Text(text.text, text.font_size, x, y, center=True, **style))


def render_shape(shape, model, target, style=None):
    style = style or {}
    if isinstance(shape, Group):  # isinstance check also catches Group subclasses (the type() lookup below would not)
        if hasattr(shape, 'style'):
            style = style_join(style, shape.style)
        for subshape in shape.shapes:
            render_shape(subshape, model, target, style)
    else:
        assert type(shape) in renderers  # make sure we know how to render this
        renderer = renderers[type(shape)]
        renderer(shape, model, target, style)


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
    margin: float = None  # if width or height are absent, default to group's width or height, plus 2*margin (TODO)
    bg_color: str = None
    alignment: Alignments = CENTER  # if alignment is None, we won't add
                                    # constraints to place the group's center
                                    # anywhere specific on the canvas - in this
                                    # case, the user is responsible for making
                                    # sure the group is positioned correctly

    model = None
    rendered = None

    def get_align_rules(self):
        bounds = self.group.bounds
        width = self.get_width()
        height = self.get_height()
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
        return align_rules

    def get_width(self, model=None):
        if self.width is not None:
            width = self.width
        else:
            assert self.group is not None
            margin = self.margin or 0
            width = self.group.bounds.width + margin

        if model is None:
            return width
        return int(maybe_get_from_model(width, model))

    def get_height(self, model=None):
        if self.height is not None:
            height = self.height
        else:
            assert self.group is not None
            margin = self.margin or 0
            height = self.group.bounds.height + margin

        if model is None:
            return height
        return int(maybe_get_from_model(height, model))

    def render(self, use_cached_model=False, var_cache=None, simplify=False):
        """
        If you want to cache variable lookups for performance reasons (eg when
        rendering an animation where shapes' styles may change between frames
        but their positions won't) then pass an empty dict to var_cache. To
        share a cache between multiple calls, pass them the same dict.
        """

        # figure out whether we're adding alignment constraints, and if so
        # create a new Group encapsulating them + the existing Group
        align_rules = self.get_align_rules()
        if align_rules:
            group = Group([self.group], align_rules)
        else:
            group = self.group

        # get a model for our group, possibly by running it thru the solver
        if use_cached_model and self.model is not None:
            model = self.model
        else:
            model = self.model = group.solve(simplify=simplify)

        # wrap the model with a caching abstraction if requested to do so
        if var_cache is not None:
            model = ModelCache(model, var_cache)

        # get width and height as ints (even if they weren't specified as such)
        width = self.get_width(model)
        height = self.get_height(model)

        # initialize the drawing
        drawing = draw.Drawing(width, height)
        if self.bg_color is not None:
            bg = Rectangle(0, 0, width, height, {"fill": self.bg_color})
            render_rect(bg, model, drawing)

        # draw the group and return the result
        render_shape(group, model, drawing)
        self.rendered = drawing
        return drawing

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


def render(group, *args, **kwargs):
    """Helper function. For simple renders, removes the need to instantiate a
    Canvas directly. Helps to cut down on boilerplate when working in Jupyter
    notebooks as well. Supports passing parameters to the Canvas through
    *args or **kwargs."""
    canvas = Canvas(group, *args, **kwargs)
    canvas.render()
    return canvas.rendered
