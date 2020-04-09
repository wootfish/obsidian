from itertools import islice

from obsidian.arrange import evenly_spaced
from obsidian.canvas import Canvas
from obsidian.group import Group
from obsidian.infix import EQ
from obsidian.shapes import Point, Rectangle, Line, Circle, Text


class GoBoard:
    BG_STYLE = {"fill": "#f2b06d"}
    LINE_STYLE = {"stroke": "#101010", "stroke_width": 1}
    TEXT_STYLE = {"fill": "#000000"}

    def __init__(self, width, height, inset, rows=19, cols=19, font_size=15, margin_between_stones=3):
        assert 7 <= rows <= 50
        assert 7 <= cols <= 50

        # initialize properties, and get local references for some of them
        self.rows = rows
        self.cols = cols
        self.font_size = font_size
        self.constraints = constraints = []
        self.bg = bg = Rectangle(0, 0, width, height, self.BG_STYLE)
        self.stones = []

        # derive stone radius from distance between adjacent intersections
        intersection_distance = min((width - 2*inset) / cols,
                                    (height - 2*inset) / rows)
        self.stone_radius = (intersection_distance - margin_between_stones) / 2

        # create points for the 4 corners of the board's grid
        top_left = Point(inset, inset)
        bot_left = Point(inset, height-inset)
        top_right = Point(width-inset, inset)
        bot_right = Point(width-inset, height-inset)

        # make lists of points evenly distributed along each edge of the board
        top_points = [Point() for _ in range(cols)]
        left_points = [Point() for _ in range(rows)]
        right_points = [Point() for _ in range(rows)]
        bottom_points = [Point() for _ in range(cols)]
        constraints.append(evenly_spaced(top_left, top_right, top_points))
        constraints.append(evenly_spaced(top_left, bot_left, left_points))
        constraints.append(evenly_spaced(top_right, bot_right, right_points))
        constraints.append(evenly_spaced(bot_left, bot_right, bottom_points))

        # draw a line between each opposing pair of points
        h_lines = [Line(p1, p2, self.LINE_STYLE) for p1, p2 in zip(left_points, right_points)]
        v_lines = [Line(p1, p2, self.LINE_STYLE) for p1, p2 in zip(top_points, bottom_points)]
        self.h_lines = h_lines
        self.v_lines = v_lines

        # mark the board's "star points"
        self.star_points = star_points = []
        for row in self.get_star_lines(rows):
            for col in self.get_star_lines(cols):
                intersection = self.get_intersection(row, col)
                star_point = Rectangle(width=5, height=5, style={"fill": "#000000"})
                star_points.append(star_point)
                constraints.append(star_point.center |EQ| intersection)

        # annotate the grid rows
        self.grid_coords = grid_coords = []
        for row, pt in enumerate(left_points):
            anchor = Point(inset/2 - 1, pt.y - 3)
            s = str(rows - row)
            grid_coords.append(self.make_text(s, anchor))

        # annotate the grid columns
        col_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz"  # no I (as is conventional)
        for letter, pt in zip(col_letters, bottom_points):
            anchor = Point(pt.x, height - inset/2)
            grid_coords.append(self.make_text(letter, anchor))

    def get_intersection(self, row, col):
        """
        Returns the intersection of the given row and col as a Point.
        """
        x = self.v_lines[col].pt1.x
        y = self.h_lines[row].pt1.y
        return Point(x, y)

    @staticmethod
    def get_star_lines(size):
        """
        Returns the lines on which to put star points for a given side size.
        Conventions vary on non-19x19 boards, but for odd-sized boards star
        points are often placed on each corner's 4-4 point, on the center of
        each side, and at the board's center. For 9x9 and below, the 3-3 point
        is typically used instead of the 4-4.
        """

        stars = []
        if size <= 9:
            stars += [2, size-3]
        else:
            stars += [3, size-4]
        if size % 2 == 1:
            stars.append(size // 2)
        return stars

    def make_black_stone(self):
        return Circle(radius=self.stone_radius, style={"stroke": "black", "stroke_width": 1.3, "fill": "#000000"})

    def make_white_stone(self):
        return Circle(radius=self.stone_radius, style={"stroke": "black", "stroke_width": 1.3, "fill": "#FFFFFF"})

    def make_text(self, string, anchor):
        return Text(string, self.font_size, anchor, GoBoard.TEXT_STYLE)

    def add_stone(self, player, row, col):
        if row >= self.rows: return
        if col >= self.cols: return
        factories = {"B": self.make_black_stone, "W": self.make_white_stone}
        stone = factories[player]()
        intersection = self.get_intersection(row, col)
        self.constraints.append(stone.center |EQ| intersection)
        self.stones.append(stone)

    def get_group(self):
        shapes = [self.bg]
        shapes += self.h_lines
        shapes += self.v_lines
        shapes += self.star_points
        shapes += self.grid_coords
        shapes += self.stones
        return Group(shapes, self.constraints)


def make_board_group(position, width, height, inset, rows=19, cols=19, marker=None, font_size=15):
    # set up the board and get a Group representing it
    board = GoBoard(width, height, inset, rows=rows, cols=cols, font_size=font_size)
    for i in range(len(position)):
        if position[i] == " ": continue
        row, col = (i // 19), i % 19
        board.add_stone(position[i], row, col)
    g = board.get_group()

    # add marker for specified move, if any
    if marker is not None and marker[0] < rows and marker[1] < cols:
        intersection = board.get_intersection(*marker)
        r = board.stone_radius * 0.8
        marker = Circle(radius=r, style={"stroke_width": 2, "stroke": "#EEEEEE"})
        g.shapes.append(marker)
        g.constraints.append(marker.center |EQ| intersection)

    return g


# this position is from move 127 of Shusaku's famous "ear-reddening game"
POSITION = ("         BWW       "
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

WIDTH = 550
HEIGHT = 550
INSET = 34

if __name__ == "__main__":
    g = make_board_group(POSITION, WIDTH, HEIGHT, INSET, marker=(8, 9))
    canvas = Canvas(g)
    canvas.save_png("gallery/go_board.png")
    canvas.save_svg("gallery/go_board.svg")
