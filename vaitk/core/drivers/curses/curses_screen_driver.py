import curses
import logging
import os
import select
import sys
import threading

from vaitk.core import Size, Point
from vaitk.core.drivers.abc.abc_driver import ABCDriver
from vaitk.consts import Index
from vaitk.core.drivers.exceptions import DriverException

logger = logging.getLogger(__name__)


class CursesScreenDriver(ABCDriver):
    def __init__(self):
        # The screen
        self._curses_screen = None

        # ncurses is not thread safe, we need a lock to prevent writing
        # collide with reading
        self._curses_lock = threading.Lock()

        # Need to store the current cursor x and y position
        self._cursor_pos = Point(x=0, y=0)

    def init(self):
        # Timeout so that ncurses sends out the pure esc key instead of
        # considering it
        # the start of a escape command. We need this to exit insert mode in
        # vai, and
        # it makes sense overall
        os.environ["ESCDELAY"] = "25"
        with self._curses_lock:
            try:
                self._curses_screen = curses.initscr()
            except Exception:
                raise DriverException("Cannot initialize screen")
            curses.start_color()
            curses.use_default_colors()
            curses.noecho()
            curses.cbreak()
            curses.raw()
            self._curses_screen.keypad(1)
            self._curses_screen.nodelay(True)
            self._curses_screen.leaveok(True)
            self._curses_screen.notimeout(True)

    def deinit(self):
        self.reset()

    @property
    def num_colors(self):
        return curses.COLORS

    @property
    def cursor_pos(self):
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, pos):
        if self.out_of_bounds(pos):
            logger.error(
                "out of bound in Screen.setCursorPos: %s",
                str(pos))
            return

        self._cursor_pos = pos

    @property
    def size(self):
        with self._curses_lock:
            h, w = self._curses_screen.getmaxyx()
        return Size(w, h)

    def reset(self):
        with self._curses_lock:
            self._curses_screen.keypad(0)
            self._curses_screen = None
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    def get_event(self):
        # Prevent to hold the GIL
        select.select([sys.stdin], [], [])

        with self._curses_lock:
            c = self._curses_screen.getch()
            # 27 = Escape character, but it's also used to create multikeys.
            # So we detect a pure escape by getting again. If it returns
            # -1, it means there's no additional keys and it's a pure escape
            if c == 27:
                next_c = self._curses_screen.getch()
                if next_c == -1:
                    pass
                # FIXME later: handle multikeys

        return c

    def write(self, pos, string, fg_color=None, bg_color=None):
        x, y = pos.x, pos.y
        size = self.size
        w, h = size.width, size.height

        out_string = string

        if y < 0 or y >= h or x >= w:
            logger.error(
                f"Out of bound in Screen.write: "
                f"pos={str(pos)} size={str(size)} len={len(string)} "
                f"'{string}'")
            return

        out_string = out_string[:w-x]

        if x < 0:
            logger.error(
                f"Out of bound in Screen.write: "
                f"pos={str(pos)} size={str(size)} len={len(string)} "
                f"'{string}'")
            out_string = string[-x:]

        if len(out_string) == 0:
            return

        attr = self.get_color_attribute_code(fg_color, bg_color)
        if x + len(out_string) > w:
            logger.error(
                "Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'",
                str(pos),
                str(self.size()),
                len(string),
                string)
            out_string = out_string[:w-x]

        if (x+len(out_string) == w):
            with self._curses_lock:
                # Old ncurses trick. We can't write the very last character, so
                # we add everything but the first, and then push everything
                # forward
                self._curses_screen.addstr(y, x, out_string[1:], attr)
                self._curses_screen.insstr(y, x, out_string[0], attr)
                self._curses_screen.noutrefresh()
        else:
            with self._curses_lock:
                self._curses_screen.addstr(y, x, out_string, attr)
                self._curses_screen.noutrefresh()

    def refresh(self):
        with self._curses_lock:
            self._curses_screen.noutrefresh()
            curses.setsyx(self._cursor_pos[Index.Y], self._cursor_pos[Index.X])
            curses.doupdate()

    def set_colors(self, pos, colors):
        """
        Sets the color attributes for a specific line, starting at pos and
        forward until the colors
        array runs out.

        """

        x, y = pos
        w, h = self.size()

        out_colors = colors

        if y < 0 or y >= h or x >= w:
            logger.error(
                "Out of bound in VScreen.setColors: pos=%s size=%s len=%d",
                str(pos),
                str(self.size()),
                len(colors))
            return

        out_colors = out_colors[:w-x]

        if x < 0:
            logger.error(
                "Out of bound in VScreen.setColors: pos=%s size=%s len=%d",
                str(pos),
                str(self.size()),
                len(colors))
            out_colors = colors[-x:]

        if len(out_colors) == 0:
            return

        if (x+len(out_colors) > w):
            logger.error(
                "Out of bound in VScreen.setColors: pos=%s size=%s len=%d",
                str(pos),
                str(self.size()),
                len(colors))
            out_colors = out_colors[:w-x]

        for num, col in enumerate(out_colors):
            if len(col) == 1:
                fg_color = col[0]
                bg_color = None
            elif len(col) == 2:
                fg_color = col[0]
                bg_color = col[1]
            else:
                fg_color = col[0]
                bg_color = col[2]

            attr = self.get_color_attribute_code(fg_color, bg_color)
            with self._curses_lock:
                self._curses_screen.chgat(y, x+num, 1, attr)

    def out_of_bounds(self, pos):
        return (
            pos.x >= self.size.width or
            pos.y >= self.size.height or
            pos.x < 0 or
            pos.y < 0
        )
