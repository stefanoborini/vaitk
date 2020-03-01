import logging
import itertools

from vaitk.core.point import Point
from vaitk.core.drivers.abc.abc_driver import ABCDriver


logger = logging.getLogger(__file__)


class TextScreenDriver(ABCDriver):
    """
    Dummy Screen that renders information in an indexed buffer, instead of
    the actual terminal screen.
    """

    def __init__(self, size):
        self._size = size

        self._cursor_pos = Point(0, 0)
        self._text = ""
        self._render_output = []

        self.erase()

    def init(self):
        pass

    def deinit(self):
        pass

    @property
    def num_colors(self):
        return 1

    @property
    def cursor_pos(self):
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, pos):
        self._cursor_pos = pos

    def reset(self):
        self.erase()

    def write(self, pos, string, fg_color=None, bg_color=None):
        for pos_x in range(len(string)):
            try:
                self._render_output[pos.y][pos.x+pos_x] = string[pos_x]
            except IndexError:
                print("Invalid write position : ", str(pos), string)

    def get_key_code(self):
        return None

    @property
    def size(self):
        return self._size

    def dump(self):
        ret = []
        ret.append(" "+"".join(list(itertools.islice(itertools.cycle(
            list(map(str, list(range(10))))), self._size[0]+1))))
        # print "+"*(self._size[0]+2)
        for i, r in enumerate(self._render_output):
            ret.append(str(i % 10)+''.join(r)+"+")
        ret.append("+"*(self._size[0]+2))
        return ret

    def __str__(self):
        return "\n".join(self.dump())

    def char_at(self, x, y):
        return self._render_output[y][x]

    def string_at(self, x, y, l):
        return ''.join(self._render_output[y][x:x+l])

    def erase(self):
        self._render_output.clear()
        for h in range(self.size.height):
            row = []
            self._render_output.append(row)
            for w in range(self.size.width):
                row.append('.')
