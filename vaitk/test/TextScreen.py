import itertools

from ..gui.AbstractScreen import AbstractScreen


class TextScreen(AbstractScreen):
    """
    Dummy Screen that renders information in an indexed buffer, instead of
    the actual terminal
    screen.
    """

    def __init__(self, size):
        self._cursor_pos = (0, 0)
        self._size = size
        self._text = ""

        self._render_output = []
        for h in range(self._size[1]):
            row = []
            self._render_output.append(row)
            for w in range(self._size[0]):
                row.append('.')

        self.erase()
        self._log = []
        self._log.append("Inited screen")

    def erase(self):
        self._render_output = []
        for h in range(self._size[1]):
            row = []
            self._render_output.append(row)
            for w in range(self._size[0]):
                row.append('.')

    def reset(self):
        pass

    def deinit(self):
        self._log.append("Deinited screen")

    def refresh(self):
        self._log.append("Refresh")

    def size(self):
        return self._size

    def cursor_pos(self):
        return self._cursor_pos

    def set_cursor_pos(self, pos):
        self._cursor_pos = pos

    def addstr(self, *args):
        pass

    def getch(self, *args):
        if len(self._text) == 0:
            return -1
        char_ret, self._text = self._text[0], self._text[1:]

        return char_ret

    def type_text(self, text):
        self._text = text

    def get_color(self, fg, bg):
        return 0

    def write(self, pos, string, fg_color=None, bg_color=None):
        for pos_x in range(len(string)):
            try:
                self._render_output[pos[1]][pos[0]+pos_x] = string[pos_x]
            except Exception:
                print("Invalid write position : ", str(pos), string)

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

    def num_colors(self):
        return 8

    def rect(self):
        return (0, 0) + self.size()