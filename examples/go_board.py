from string import ascii_lowercase

from itertools import islice

from obsidian.arrange import evenly_spaced
from obsidian.canvas import Canvas
from obsidian.group import Group
from obsidian.infix import EQ
from obsidian.shapes import Point, Rectangle, Line, Circle


width = 600
height = 600
inset = 17


# this is Shusaku's famous "ear-reddening game" from 1846
kifu = ("B[qd];W[dc];B[pq];W[oc];B[cp];W[cf];B[ep];W[qo];B[pe];W[np];B[po];"
        "W[pp];B[op];W[qp];B[oq];W[oo];B[pn];W[qq];B[nq];W[on];B[pm];W[om];"
        "B[pl];W[mp];B[mq];W[ol];B[pk];W[lq];B[lr];W[kr];B[lp];W[kq];B[qr];"
        "W[rr];B[rs];W[mr];B[nr];W[pr];B[ps];W[qs];B[no];W[mo];B[qr];W[rm];"
        "B[rl];W[qs];B[lo];W[mn];B[qr];W[qm];B[or];W[ql];B[qj];W[rj];B[ri];"
        "W[rk];B[ln];W[mm];B[qi];W[rq];B[jn];W[ls];B[ns];W[gq];B[go];W[ck];"
        "B[kc];W[ic];B[pc];W[nj];B[ke];W[og];B[oh];W[pb];B[qb];W[ng];B[mi];"
        "W[mj];B[nd];W[ph];B[qg];W[pg];B[hq];W[hr];B[ir];W[iq];B[hp];W[jr];"
        "B[fc];W[lc];B[ld];W[mc];B[lb];W[mb];B[md];W[qf];B[pf];W[qh];B[rg];"
        "W[rh];B[sh];W[rf];B[sg];W[pj];B[pi];W[oi];B[oj];W[ni];B[qk];W[ok];"
        "B[qe];W[kb];B[jb];W[ka];B[jc];W[ob];B[ja];W[la];B[db];W[cc];B[fe];"
        "W[cn];B[gr];W[is];B[fq];W[io];B[ji];W[eb];B[fb];W[eg];B[dj];W[dk];"
        "B[ej];W[cj];B[dh];W[ij];B[hm];W[gj];B[eh];W[fl];B[fg];W[er];B[dm];"
        "W[fn];B[dn];W[gn];B[jj];W[jk];B[kk];W[ii];B[ik];W[jl];B[kl];W[il];"
        "B[jh];W[co];B[do];W[ih];B[hn];W[hl];B[bl];W[dg];B[gh];W[ch];B[ig];"
        "W[ec];B[cr];W[fd];B[gd];W[ed];B[gc];W[bk];B[cm];W[gs];B[gp];W[li];"
        "B[kg];W[in];B[lj];W[lg];B[gm];W[jf];B[jg];W[im];B[fm];W[kf];B[lf];"
        "W[mf];B[le];W[gf];B[hf];W[ff];B[gg];W[lk];B[kj];W[km];B[lm];W[ll];"
        "B[jm];W[ge];B[he];W[ee];B[ea];W[cb];B[fr];W[fs];B[dr];W[qa];B[ra];"
        "W[pa];B[rb];W[da];B[gi];W[fj];B[fi];W[fa];B[ga];W[gl];B[ek];W[em];"
        "B[ho];W[el];B[en];W[jo];B[kn];W[ci];B[lh];W[mh];B[mg];W[di];B[ei];"
        "W[lg];B[qn];W[rn];B[re];W[sl];B[mg];W[bm];B[am];W[lg];B[eq];W[es];"
        "B[mg];W[ha];B[gb];W[lg];B[ds];W[hs];B[mg];W[sj];B[si];W[lg];B[sr];"
        "W[sq];B[mg];W[hd];B[hb];W[lg];B[ro];W[so];B[mg];W[ss];B[qs];W[lg];"
        "B[sn];W[rp];B[mg];W[cl];B[bn];W[lg];B[ml];W[mk];B[mg];W[pj];B[sf];"
        "W[lg];B[nn];W[nl];B[mg];W[ib];B[ia];W[lg];B[nc];W[nb];B[mg];W[jd];"
        "B[kd];W[lg];B[ma];W[na];B[mg];W[qc];B[rc];W[lg];B[js];W[ks];B[mg];"
        "W[hc];B[id];W[lg];B[fk];W[hj];B[mg];W[hh];B[hg];W[lg];B[gk];W[hk];"
        "B[mg];W[ak];B[lg];W[al];B[bm];W[nf];B[od];W[ki];B[ms];W[kp];B[ip];"
        "W[jp];B[lr];W[oj];B[mr];W[ea];B[sr]")


def get_moves(kifu):
    # extremely fragile parser for the above game record
    moves = kifu.split(";")
    for entry in moves:
        player, ascii_col, ascii_row = entry[0], entry[2], entry[3]
        col = ascii_lowercase.index(ascii_col)
        row = 18-ascii_lowercase.index(ascii_row)
        yield player, col, row


class GoBoard:
    BG_STYLE = {"fill": "#f2b06d"}
    LINE_STYLE = {"stroke": "#101010", "stroke_width": 1}

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

        self.bg = bg
        self.star_points = star_points
        self.constraints = constraints
        self.stones = []

    def rc_to_xy(self, row, col):
        x = self.v_lines[col].pt1.x
        y = self.h_lines[row].pt1.y
        return x, y

    @staticmethod
    def black_stone():
        return Circle(radius=13, style={"stroke": "black", "stroke_width": 1.3, "fill": "#000000"})

    @staticmethod
    def white_stone():
        return Circle(radius=13, style={"stroke": "black", "stroke_width": 1.3, "fill": "#FFFFFF"})

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
        shapes += self.stones
        return Group(shapes, self.constraints)


# set up the board and get a Group representing it
board = GoBoard(width, height, inset)
for player, col, row in islice(get_moves(kifu), 127):  # move 127 is the "ear reddening move"
    board.add_move(player, row, col)
g = board.get_group()

# add marker for most recent move
x, y = board.rc_to_xy(row, col)
marker = Circle(radius=9, style={"stroke_width": 2, "stroke": "#EEEEEE"})
g.shapes.append(marker)
g.constraints.append(marker.bounds.center.x |EQ| x)
g.constraints.append(marker.bounds.center.y |EQ| y)

# render
canvas = Canvas(g, width, height)
canvas.save_png("gallery/go_board.png")
canvas.save_svg("gallery/go_board.svg")
