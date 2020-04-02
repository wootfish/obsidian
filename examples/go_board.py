from itertools import islice

from obsidian.arrange import evenly_spaced
from obsidian.canvas import Canvas
from obsidian.group import Group
from obsidian.infix import EQ
from obsidian.shapes import Point, Rectangle, Line, Circle, Text


width = 550
height = 550
inset = 34


# this position is from move 127 of Shusaku's famous "ear-reddening game"
position = ("         BWW       "
            "   B     BW W WWB  "
            "  WW B  WBBWW WB   "
            "           BBB  B  "
            "     B    B    BB  "
            "  W            BWW "
            "             WWWBBB"
            "              BWWWB"
            "         B  BWWBBB "
            "            WWB BW "
            "  W           WBBW "
            "              WBWB "
            "            W WBWW "
            "  W      B BW WB   "
            "      B W  BWBWBW  "
            "  B B  B   BWWBWW  "
            "     BWBW WWBBBBWW "
            "      B  WW WBB BW "
            "        W  W B B B ")


class GoBoard:
    BG_STYLE = {"fill": "#f2b06d"}
    LINE_STYLE = {"stroke": "#101010", "stroke_width": 1}
    TEXT_STYLE = {"fill": "#000000"}

    def __init__(self, width, height, inset):
        constraints = []
        bg = Rectangle(0, 0, width, height, self.BG_STYLE)

        top_left = Point(inset, inset)
        bot_left = Point(inset, height-inset)
        top_right = Point(width-inset, inset)
        bot_right = Point(width-inset, height-inset)

        top_points = [Point() for _ in range(19)]
        left_points = [Point() for _ in range(19)]
        right_points = [Point() for _ in range(19)]
        bottom_points = [Point() for _ in range(19)]

        constraints += evenly_spaced(top_left, top_right, top_points)
        constraints += evenly_spaced(top_left, bot_left, left_points)
        constraints += evenly_spaced(top_right, bot_right, right_points)
        constraints += evenly_spaced(bot_left, bot_right, bottom_points)

        h_lines = [Line(p1, p2, self.LINE_STYLE) for p1, p2 in zip(left_points, right_points)]
        v_lines = [Line(p1, p2, self.LINE_STYLE) for p1, p2 in zip(top_points, bottom_points)]
        self.h_lines = h_lines
        self.v_lines = v_lines

        star_points = []
        for row in (3, 9, 15):
            for col in (3, 9, 15):
                x, y = self.rc_to_xy(row, col)
                star_point = Rectangle(width=5, height=5, style={"fill": "#000000"})
                star_points.append(star_point)
                constraints.append(star_point.bounds.center.x |EQ| x)
                constraints.append(star_point.bounds.center.y |EQ| y)

        grid_coords = []
        for row, pt in enumerate(left_points):
            anchor = Point(inset/2 - 1, pt.y + 3)
            s = str(row)
            grid_coords.append(Text(s, 15, anchor, self.TEXT_STYLE))

        col_letters = "ABCDEFGHJKLMNOPQRST"  # no I - the usual convention
        for letter, pt in zip(col_letters, bottom_points):
            anchor = Point(pt.x, inset/2 - 1)
            grid_coords.append(Text(letter, 15, anchor, self.TEXT_STYLE))

        self.bg = bg
        self.star_points = star_points
        self.grid_coords = grid_coords
        self.constraints = constraints
        self.stones = []

    def rc_to_xy(self, row, col):
        x = self.v_lines[col].pt1.x
        y = self.h_lines[row].pt1.y
        return x, y

    @staticmethod
    def black_stone():
        return Circle(radius=12, style={"stroke": "black", "stroke_width": 1.3, "fill": "#000000"})

    @staticmethod
    def white_stone():
        return Circle(radius=12, style={"stroke": "black", "stroke_width": 1.3, "fill": "#FFFFFF"})

    def add_move(self, player, row, col):
        # if we really wanted to get fancy we'd make this method check for
        # captured stones & remove them (but that sounds like a lot of work)
        factories = {"B": self.black_stone, "W": self.white_stone}
        stone = factories[player]()
        x, y = self.rc_to_xy(row, col)
        self.constraints.append(stone.x |EQ| x)
        self.constraints.append(stone.y |EQ| y)
        self.stones.append(stone)

    def get_group(self):
        shapes = [self.bg]
        shapes += self.h_lines
        shapes += self.v_lines
        shapes += self.star_points
        shapes += self.grid_coords
        shapes += self.stones
        return Group(shapes, self.constraints)


# set up the board and get a Group representing it
board = GoBoard(width, height, inset)
for i in range(len(position)):
    if position[i] == " ": continue
    row, col = (18-i // 19), i % 19
    board.add_move(position[i], row, col)
g = board.get_group()


# add marker for most recent move
x, y = board.rc_to_xy(10, 9)
marker = Circle(radius=8, style={"stroke_width": 2, "stroke": "#EEEEEE"})
g.shapes.append(marker)
g.constraints.append(marker.bounds.center.x |EQ| x)
g.constraints.append(marker.bounds.center.y |EQ| y)


# render
canvas = Canvas(g, width, height)
canvas.save_png("gallery/go_board.png")
canvas.save_svg("gallery/go_board.svg")
