import curses
import logging
import os
import select
import sys
import threading

from . import Color
from .AbstractScreen import AbstractScreen
from ..consts import Index


logger = logging.getLogger(__name__)


class VException(Exception):
    pass


class CursesScreen(AbstractScreen):
    def __init__(self):
        # Timeout so that ncurses sends out the pure esc key instead of
        # considering it
        # the start of a escape command. We need this to exit insert mode in
        # vai, and
        # it makes sense overall
        os.environ["ESCDELAY"] = "25"
        try:
            self._curses_screen = curses.initscr()
        except Exception:
            raise VException("Cannot initialize screen")
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        self._curses_screen.keypad(1)
        self._curses_screen.nodelay(True)
        self._curses_screen.leaveok(True)
        self._curses_screen.notimeout(True)

        # ncurses is not thread safe, we need a lock to prevent writing
        # collide with reading
        self._curses_lock = threading.Lock()

        # Resolves the rgb color to the screen color
        self._color_lookup_cache = {}

        # Resolves fg, bg native index to the associated color pair index
        self._attr_lookup_cache = {}

        # The first color pair is always defined with index 0 and contains
        # the default fg and bg colors
        self._color_pairs = [(-1, -1)]

        self._cursor_pos = (0, 0)

        VGlobalScreenColor.init(self.num_colors())

    def reset(self):
        self._curses_screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def refresh(self):
        with self._curses_lock:
            self._curses_screen.noutrefresh()
            curses.setsyx(self._cursor_pos[Index.Y], self._cursor_pos[Index.X])
            curses.doupdate()

    def rect(self):
        return (0, 0) + self.size()

    def size(self):
        with self._curses_lock:
            h, w = self._curses_screen.getmaxyx()
        return (w, h)

    def get_key_code(self):
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
        x, y = pos
        w, h = self.size()

        out_string = string

        if y < 0 or y >= h or x >= w:
            logger.error(
                "Out of bound in Screen.write: pos=%s size=%s len=%d '%s'",
                str(pos),
                str(self.size()),
                len(string),
                string)
            return

        out_string = out_string[:w-x]

        if x < 0:
            logger.error(
                "Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'",
                str(pos),
                str(self.size()),
                len(string),
                string)
            out_string = string[-x:]

        if len(out_string) == 0:
            return

        attr = self.get_color_attribute_code(fg_color, bg_color)
        if (x+len(out_string) > w):
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

    def num_colors(self):
        return curses.COLORS

    def get_color_attribute_code(self, fg=None, bg=None):
        """Given fg and bg colors, find and return the correct attribute code
        to apply with chgat"""
        fg_screen = None if fg is None else self._find_closest_color(fg)
        bg_screen = None if bg is None else self._find_closest_color(bg)

        if (fg_screen, bg_screen) in self._attr_lookup_cache:
            return self._attr_lookup_cache[(fg_screen, bg_screen)]

        fg_index = -1 if fg_screen is None else fg_screen.colorIdx()
        bg_index = -1 if bg_screen is None else bg_screen.colorIdx()

        attr = self._get_pair_attr_from_colors(fg_index, bg_index)

        if fg_screen and fg_screen.attr():
            attr |= fg_screen.attr()

        self._attr_lookup_cache[(fg_screen, bg_screen)] = attr
        return attr

    def _get_pair_attr_from_colors(self, fg_index, bg_index):
        t = (fg_index, bg_index)

        if t in self._color_pairs:
            pair_index = self._color_pairs.index((fg_index, bg_index))
        else:
            pair_index = len(self._color_pairs)
            with self._curses_lock:
                curses.init_pair(pair_index, fg_index, bg_index)
            self._color_pairs.append((fg_index, bg_index))

        with self._curses_lock:
            attr = curses.color_pair(pair_index)

        return attr
        # Init color pairs

    def set_cursor_pos(self, pos):
        if self.out_of_bounds(pos):
            logger.error(
                "out of bound in Screen.setCursorPos: %s",
                str(pos))
            return

        self._cursor_pos = pos

    def cursor_pos(self):
        return self._cursor_pos

    def _find_closest_color(self, color):
        screen_color = self._color_lookup_cache.get(color.rgb)
        if screen_color is not None:
            return screen_color

        closest = sorted([(Color.VColor.distance(color, screen_color),
                           screen_color)
                          for index, screen_color in enumerate(
            VGlobalScreenColor.all_colors())
        ],
            key=lambda x: x[0]
        )[0]
        self._color_lookup_cache[color.rgb] = closest[1]
        return closest[1]

    def out_of_bounds(self, pos):
        x, y = pos
        return (x >= self.width() or y >= self.height() or x < 0 or y < 0)


class ScreenColor(object):
    def __init__(self, color_idx, attr, equiv_rgb):
        self._color_idx = color_idx
        self._attr = attr
        self._equiv_rgb = equiv_rgb

    def attr(self):
        return self._attr

    def color_idx(self):
        return self._color_idx

    def equiv_rgb(self):
        return self._equiv_rgb

    @property
    def r(self):
        return self._equiv_rgb[0]

    @property
    def g(self):
        return self._equiv_rgb[1]

    @property
    def b(self):
        return self._equiv_rgb[2]


class VGlobalScreenColor(object):
    @classmethod
    def init(cls, num_colors):
        if num_colors == 8 or num_colors == 256:
            cls.term_0 = ScreenColor(0, None, (0x00, 0x00, 0x00))
            cls.term_1 = ScreenColor(1, None, (0x80, 0x00, 0x00))
            cls.term_2 = ScreenColor(2, None, (0x00, 0x80, 0x00))
            cls.term_3 = ScreenColor(3, None, (0x80, 0x80, 0x00))
            cls.term_4 = ScreenColor(4, None, (0x00, 0x00, 0x80))
            cls.term_5 = ScreenColor(5, None, (0x80, 0x00, 0x80))
            cls.term_6 = ScreenColor(6, None, (0x00, 0x80, 0x80))
            cls.term_6 = ScreenColor(7, None, (0xc0, 0xc0, 0xc0))
            cls.term_8 = ScreenColor(8, None, (0x80, 0x80, 0x80))

            cls.black = ScreenColor(curses.COLOR_BLACK, None, (0, 0, 0))
            cls.darkred = ScreenColor(curses.COLOR_RED, None, (170, 0, 0))
            cls.darkgreen = ScreenColor(curses.COLOR_GREEN, None, (0, 170, 0))
            cls.brown = ScreenColor(curses.COLOR_YELLOW, None, (170, 170, 0))
            cls.darkblue = ScreenColor(curses.COLOR_BLUE, None, (0, 0, 170))
            cls.darkmagenta = ScreenColor(
                curses.COLOR_MAGENTA, None, (170, 0, 170))
            cls.darkcyan = ScreenColor(curses.COLOR_CYAN, None, (0, 170, 170))
            cls.lightgray = ScreenColor(
                curses.COLOR_WHITE, None, (170, 170, 170))

            cls.darkgray = ScreenColor(
                curses.COLOR_BLACK, curses.A_BOLD, (100, 100, 100))
            cls.lightred = ScreenColor(
                curses.COLOR_RED, curses.A_BOLD, (255, 0, 0))
            cls.lightgreen = ScreenColor(
                curses.COLOR_GREEN, curses.A_BOLD, (0, 255, 0))
            cls.yellow = ScreenColor(
                curses.COLOR_YELLOW, curses.A_BOLD, (255, 255, 0))
            cls.lightblue = ScreenColor(
                curses.COLOR_BLUE, curses.A_BOLD, (0, 0, 255))
            cls.lightmagenta = ScreenColor(
                curses.COLOR_MAGENTA, curses.A_BOLD, (255, 0, 255))
            cls.lightcyan = ScreenColor(
                curses.COLOR_CYAN, curses.A_BOLD, (0, 255, 255))
            cls.white = ScreenColor(
                curses.COLOR_WHITE, curses.A_BOLD, (255, 255, 255))

            cls.red = cls.lightred
            cls.green = cls.lightgreen
            cls.blue = cls.lightblue
            cls.magenta = cls.lightmagenta
            cls.cyan = cls.lightcyan
            cls.gray = cls.lightgray

        if num_colors == 256:
            cls.term_9 = ScreenColor(9, None, (0xff, 0x00, 0x00))
            cls.term_10 = ScreenColor(10, None, (0x00, 0xff, 0x00))
            cls.term_11 = ScreenColor(11, None, (0xff, 0xff, 0x00))
            cls.term_12 = ScreenColor(12, None, (0x00, 0x00, 0xff))
            cls.term_13 = ScreenColor(13, None, (0xff, 0x00, 0xff))
            cls.term_14 = ScreenColor(14, None, (0x00, 0xff, 0xff))
            cls.term_15 = ScreenColor(15, None, (0xff, 0xff, 0xff))
            cls.term_16 = ScreenColor(16, None, (0x00, 0x00, 0x00))
            cls.term_17 = ScreenColor(17, None, (0x00, 0x00, 0x5f))
            cls.term_18 = ScreenColor(18, None, (0x00, 0x00, 0x87))
            cls.term_19 = ScreenColor(19, None, (0x00, 0x00, 0xaf))
            cls.term_20 = ScreenColor(20, None, (0x00, 0x00, 0xd7))
            cls.term_21 = ScreenColor(21, None, (0x00, 0x00, 0xff))
            cls.term_22 = ScreenColor(22, None, (0x00, 0x5f, 0x00))
            cls.term_23 = ScreenColor(23, None, (0x00, 0x5f, 0x5f))
            cls.term_24 = ScreenColor(24, None, (0x00, 0x5f, 0x87))
            cls.term_25 = ScreenColor(25, None, (0x00, 0x5f, 0xaf))
            cls.term_26 = ScreenColor(26, None, (0x00, 0x5f, 0xd7))
            cls.term_27 = ScreenColor(27, None, (0x00, 0x5f, 0xff))
            cls.term_28 = ScreenColor(28, None, (0x00, 0x87, 0x00))
            cls.term_29 = ScreenColor(29, None, (0x00, 0x87, 0x5f))
            cls.term_30 = ScreenColor(30, None, (0x00, 0x87, 0x87))
            cls.term_31 = ScreenColor(31, None, (0x00, 0x87, 0xaf))
            cls.term_32 = ScreenColor(32, None, (0x00, 0x87, 0xd7))
            cls.term_33 = ScreenColor(33, None, (0x00, 0x87, 0xff))
            cls.term_34 = ScreenColor(34, None, (0x00, 0xaf, 0x00))
            cls.term_35 = ScreenColor(35, None, (0x00, 0xaf, 0x5f))
            cls.term_36 = ScreenColor(36, None, (0x00, 0xaf, 0x87))
            cls.term_37 = ScreenColor(37, None, (0x00, 0xaf, 0xaf))
            cls.term_38 = ScreenColor(38, None, (0x00, 0xaf, 0xd7))
            cls.term_39 = ScreenColor(39, None, (0x00, 0xaf, 0xff))
            cls.term_40 = ScreenColor(40, None, (0x00, 0xd7, 0x00))
            cls.term_41 = ScreenColor(41, None, (0x00, 0xd7, 0x5f))
            cls.term_42 = ScreenColor(42, None, (0x00, 0xd7, 0x87))
            cls.term_43 = ScreenColor(43, None, (0x00, 0xd7, 0xaf))
            cls.term_44 = ScreenColor(44, None, (0x00, 0xd7, 0xd7))
            cls.term_45 = ScreenColor(45, None, (0x00, 0xd7, 0xff))
            cls.term_46 = ScreenColor(46, None, (0x00, 0xff, 0x00))
            cls.term_47 = ScreenColor(47, None, (0x00, 0xff, 0x5f))
            cls.term_48 = ScreenColor(48, None, (0x00, 0xff, 0x87))
            cls.term_49 = ScreenColor(49, None, (0x00, 0xff, 0xaf))
            cls.term_50 = ScreenColor(50, None, (0x00, 0xff, 0xd7))
            cls.term_51 = ScreenColor(51, None, (0x00, 0xff, 0xff))
            cls.term_52 = ScreenColor(52, None, (0x5f, 0x00, 0x00))
            cls.term_53 = ScreenColor(53, None, (0x5f, 0x00, 0x5f))
            cls.term_54 = ScreenColor(54, None, (0x5f, 0x00, 0x87))
            cls.term_55 = ScreenColor(55, None, (0x5f, 0x00, 0xaf))
            cls.term_56 = ScreenColor(56, None, (0x5f, 0x00, 0xd7))
            cls.term_57 = ScreenColor(57, None, (0x5f, 0x00, 0xff))
            cls.term_58 = ScreenColor(58, None, (0x5f, 0x5f, 0x00))
            cls.term_59 = ScreenColor(59, None, (0x5f, 0x5f, 0x5f))
            cls.term_60 = ScreenColor(60, None, (0x5f, 0x5f, 0x87))
            cls.term_61 = ScreenColor(61, None, (0x5f, 0x5f, 0xaf))
            cls.term_62 = ScreenColor(62, None, (0x5f, 0x5f, 0xd7))
            cls.term_63 = ScreenColor(63, None, (0x5f, 0x5f, 0xff))
            cls.term_64 = ScreenColor(64, None, (0x5f, 0x87, 0x00))
            cls.term_65 = ScreenColor(65, None, (0x5f, 0x87, 0x5f))
            cls.term_66 = ScreenColor(66, None, (0x5f, 0x87, 0x87))
            cls.term_67 = ScreenColor(67, None, (0x5f, 0x87, 0xaf))
            cls.term_68 = ScreenColor(68, None, (0x5f, 0x87, 0xd7))
            cls.term_69 = ScreenColor(69, None, (0x5f, 0x87, 0xff))
            cls.term_70 = ScreenColor(70, None, (0x5f, 0xaf, 0x00))
            cls.term_71 = ScreenColor(71, None, (0x5f, 0xaf, 0x5f))
            cls.term_72 = ScreenColor(72, None, (0x5f, 0xaf, 0x87))
            cls.term_73 = ScreenColor(73, None, (0x5f, 0xaf, 0xaf))
            cls.term_74 = ScreenColor(74, None, (0x5f, 0xaf, 0xd7))
            cls.term_75 = ScreenColor(75, None, (0x5f, 0xaf, 0xff))
            cls.term_76 = ScreenColor(76, None, (0x5f, 0xd7, 0x00))
            cls.term_77 = ScreenColor(77, None, (0x5f, 0xd7, 0x5f))
            cls.term_78 = ScreenColor(78, None, (0x5f, 0xd7, 0x87))
            cls.term_79 = ScreenColor(79, None, (0x5f, 0xd7, 0xaf))
            cls.term_80 = ScreenColor(80, None, (0x5f, 0xd7, 0xd7))
            cls.term_81 = ScreenColor(81, None, (0x5f, 0xd7, 0xff))
            cls.term_82 = ScreenColor(82, None, (0x5f, 0xff, 0x00))
            cls.term_83 = ScreenColor(83, None, (0x5f, 0xff, 0x5f))
            cls.term_84 = ScreenColor(84, None, (0x5f, 0xff, 0x87))
            cls.term_85 = ScreenColor(85, None, (0x5f, 0xff, 0xaf))
            cls.term_86 = ScreenColor(86, None, (0x5f, 0xff, 0xd7))
            cls.term_87 = ScreenColor(87, None, (0x5f, 0xff, 0xff))
            cls.term_88 = ScreenColor(88, None, (0x87, 0x00, 0x00))
            cls.term_89 = ScreenColor(89, None, (0x87, 0x00, 0x5f))
            cls.term_90 = ScreenColor(90, None, (0x87, 0x00, 0x87))
            cls.term_91 = ScreenColor(91, None, (0x87, 0x00, 0xaf))
            cls.term_92 = ScreenColor(92, None, (0x87, 0x00, 0xd7))
            cls.term_93 = ScreenColor(93, None, (0x87, 0x00, 0xff))
            cls.term_94 = ScreenColor(94, None, (0x87, 0x5f, 0x00))
            cls.term_95 = ScreenColor(95, None, (0x87, 0x5f, 0x5f))
            cls.term_96 = ScreenColor(96, None, (0x87, 0x5f, 0x87))
            cls.term_97 = ScreenColor(97, None, (0x87, 0x5f, 0xaf))
            cls.term_98 = ScreenColor(98, None, (0x87, 0x5f, 0xd7))
            cls.term_99 = ScreenColor(99, None, (0x87, 0x5f, 0xff))
            cls.term_100 = ScreenColor(100, None, (0x87, 0x87, 0x00))
            cls.term_101 = ScreenColor(101, None, (0x87, 0x87, 0x5f))
            cls.term_102 = ScreenColor(102, None, (0x87, 0x87, 0x87))
            cls.term_103 = ScreenColor(103, None, (0x87, 0x87, 0xaf))
            cls.term_104 = ScreenColor(104, None, (0x87, 0x87, 0xd7))
            cls.term_105 = ScreenColor(105, None, (0x87, 0x87, 0xff))
            cls.term_106 = ScreenColor(106, None, (0x87, 0xaf, 0x00))
            cls.term_107 = ScreenColor(107, None, (0x87, 0xaf, 0x5f))
            cls.term_108 = ScreenColor(108, None, (0x87, 0xaf, 0x87))
            cls.term_109 = ScreenColor(109, None, (0x87, 0xaf, 0xaf))
            cls.term_110 = ScreenColor(110, None, (0x87, 0xaf, 0xd7))
            cls.term_111 = ScreenColor(111, None, (0x87, 0xaf, 0xff))
            cls.term_112 = ScreenColor(112, None, (0x87, 0xd7, 0x00))
            cls.term_113 = ScreenColor(113, None, (0x87, 0xd7, 0x5f))
            cls.term_114 = ScreenColor(114, None, (0x87, 0xd7, 0x87))
            cls.term_115 = ScreenColor(115, None, (0x87, 0xd7, 0xaf))
            cls.term_116 = ScreenColor(116, None, (0x87, 0xd7, 0xd7))
            cls.term_117 = ScreenColor(117, None, (0x87, 0xd7, 0xff))
            cls.term_118 = ScreenColor(118, None, (0x87, 0xff, 0x00))
            cls.term_119 = ScreenColor(119, None, (0x87, 0xff, 0x5f))
            cls.term_120 = ScreenColor(120, None, (0x87, 0xff, 0x87))
            cls.term_121 = ScreenColor(121, None, (0x87, 0xff, 0xaf))
            cls.term_122 = ScreenColor(122, None, (0x87, 0xff, 0xd7))
            cls.term_123 = ScreenColor(123, None, (0x87, 0xff, 0xff))
            cls.term_124 = ScreenColor(124, None, (0xaf, 0x00, 0x00))
            cls.term_125 = ScreenColor(125, None, (0xaf, 0x00, 0x5f))
            cls.term_126 = ScreenColor(126, None, (0xaf, 0x00, 0x87))
            cls.term_127 = ScreenColor(127, None, (0xaf, 0x00, 0xaf))
            cls.term_128 = ScreenColor(128, None, (0xaf, 0x00, 0xd7))
            cls.term_129 = ScreenColor(129, None, (0xaf, 0x00, 0xff))
            cls.term_130 = ScreenColor(130, None, (0xaf, 0x5f, 0x00))
            cls.term_131 = ScreenColor(131, None, (0xaf, 0x5f, 0x5f))
            cls.term_132 = ScreenColor(132, None, (0xaf, 0x5f, 0x87))
            cls.term_133 = ScreenColor(133, None, (0xaf, 0x5f, 0xaf))
            cls.term_134 = ScreenColor(134, None, (0xaf, 0x5f, 0xd7))
            cls.term_135 = ScreenColor(135, None, (0xaf, 0x5f, 0xff))
            cls.term_136 = ScreenColor(136, None, (0xaf, 0x87, 0x00))
            cls.term_137 = ScreenColor(137, None, (0xaf, 0x87, 0x5f))
            cls.term_138 = ScreenColor(138, None, (0xaf, 0x87, 0x87))
            cls.term_139 = ScreenColor(139, None, (0xaf, 0x87, 0xaf))
            cls.term_140 = ScreenColor(140, None, (0xaf, 0x87, 0xd7))
            cls.term_141 = ScreenColor(141, None, (0xaf, 0x87, 0xff))
            cls.term_142 = ScreenColor(142, None, (0xaf, 0xaf, 0x00))
            cls.term_143 = ScreenColor(143, None, (0xaf, 0xaf, 0x5f))
            cls.term_144 = ScreenColor(144, None, (0xaf, 0xaf, 0x87))
            cls.term_145 = ScreenColor(145, None, (0xaf, 0xaf, 0xaf))
            cls.term_146 = ScreenColor(146, None, (0xaf, 0xaf, 0xd7))
            cls.term_147 = ScreenColor(147, None, (0xaf, 0xaf, 0xff))
            cls.term_148 = ScreenColor(148, None, (0xaf, 0xd7, 0x00))
            cls.term_149 = ScreenColor(149, None, (0xaf, 0xd7, 0x5f))
            cls.term_150 = ScreenColor(150, None, (0xaf, 0xd7, 0x87))
            cls.term_151 = ScreenColor(151, None, (0xaf, 0xd7, 0xaf))
            cls.term_152 = ScreenColor(152, None, (0xaf, 0xd7, 0xd7))
            cls.term_153 = ScreenColor(153, None, (0xaf, 0xd7, 0xff))
            cls.term_154 = ScreenColor(154, None, (0xaf, 0xff, 0x00))
            cls.term_155 = ScreenColor(155, None, (0xaf, 0xff, 0x5f))
            cls.term_156 = ScreenColor(156, None, (0xaf, 0xff, 0x87))
            cls.term_157 = ScreenColor(157, None, (0xaf, 0xff, 0xaf))
            cls.term_158 = ScreenColor(158, None, (0xaf, 0xff, 0xd7))
            cls.term_159 = ScreenColor(159, None, (0xaf, 0xff, 0xff))
            cls.term_160 = ScreenColor(160, None, (0xd7, 0x00, 0x00))
            cls.term_161 = ScreenColor(161, None, (0xd7, 0x00, 0x5f))
            cls.term_162 = ScreenColor(162, None, (0xd7, 0x00, 0x87))
            cls.term_163 = ScreenColor(163, None, (0xd7, 0x00, 0xaf))
            cls.term_164 = ScreenColor(164, None, (0xd7, 0x00, 0xd7))
            cls.term_165 = ScreenColor(165, None, (0xd7, 0x00, 0xff))
            cls.term_166 = ScreenColor(166, None, (0xd7, 0x5f, 0x00))
            cls.term_167 = ScreenColor(167, None, (0xd7, 0x5f, 0x5f))
            cls.term_168 = ScreenColor(168, None, (0xd7, 0x5f, 0x87))
            cls.term_169 = ScreenColor(169, None, (0xd7, 0x5f, 0xaf))
            cls.term_170 = ScreenColor(170, None, (0xd7, 0x5f, 0xd7))
            cls.term_171 = ScreenColor(171, None, (0xd7, 0x5f, 0xff))
            cls.term_172 = ScreenColor(172, None, (0xd7, 0x87, 0x00))
            cls.term_173 = ScreenColor(173, None, (0xd7, 0x87, 0x5f))
            cls.term_174 = ScreenColor(174, None, (0xd7, 0x87, 0x87))
            cls.term_175 = ScreenColor(175, None, (0xd7, 0x87, 0xaf))
            cls.term_176 = ScreenColor(176, None, (0xd7, 0x87, 0xd7))
            cls.term_177 = ScreenColor(177, None, (0xd7, 0x87, 0xff))
            cls.term_178 = ScreenColor(178, None, (0xd7, 0xaf, 0x00))
            cls.term_179 = ScreenColor(179, None, (0xd7, 0xaf, 0x5f))
            cls.term_180 = ScreenColor(180, None, (0xd7, 0xaf, 0x87))
            cls.term_181 = ScreenColor(181, None, (0xd7, 0xaf, 0xaf))
            cls.term_182 = ScreenColor(182, None, (0xd7, 0xaf, 0xd7))
            cls.term_183 = ScreenColor(183, None, (0xd7, 0xaf, 0xff))
            cls.term_184 = ScreenColor(184, None, (0xd7, 0xd7, 0x00))
            cls.term_185 = ScreenColor(185, None, (0xd7, 0xd7, 0x5f))
            cls.term_186 = ScreenColor(186, None, (0xd7, 0xd7, 0x87))
            cls.term_187 = ScreenColor(187, None, (0xd7, 0xd7, 0xaf))
            cls.term_188 = ScreenColor(188, None, (0xd7, 0xd7, 0xd7))
            cls.term_189 = ScreenColor(189, None, (0xd7, 0xd7, 0xff))
            cls.term_190 = ScreenColor(190, None, (0xd7, 0xff, 0x00))
            cls.term_191 = ScreenColor(191, None, (0xd7, 0xff, 0x5f))
            cls.term_192 = ScreenColor(192, None, (0xd7, 0xff, 0x87))
            cls.term_193 = ScreenColor(193, None, (0xd7, 0xff, 0xaf))
            cls.term_194 = ScreenColor(194, None, (0xd7, 0xff, 0xd7))
            cls.term_195 = ScreenColor(195, None, (0xd7, 0xff, 0xff))
            cls.term_196 = ScreenColor(196, None, (0xff, 0x00, 0x00))
            cls.term_197 = ScreenColor(197, None, (0xff, 0x00, 0x5f))
            cls.term_198 = ScreenColor(198, None, (0xff, 0x00, 0x87))
            cls.term_199 = ScreenColor(199, None, (0xff, 0x00, 0xaf))
            cls.term_200 = ScreenColor(200, None, (0xff, 0x00, 0xd7))
            cls.term_201 = ScreenColor(201, None, (0xff, 0x00, 0xff))
            cls.term_202 = ScreenColor(202, None, (0xff, 0x5f, 0x00))
            cls.term_203 = ScreenColor(203, None, (0xff, 0x5f, 0x5f))
            cls.term_204 = ScreenColor(204, None, (0xff, 0x5f, 0x87))
            cls.term_205 = ScreenColor(205, None, (0xff, 0x5f, 0xaf))
            cls.term_206 = ScreenColor(206, None, (0xff, 0x5f, 0xd7))
            cls.term_207 = ScreenColor(207, None, (0xff, 0x5f, 0xff))
            cls.term_208 = ScreenColor(208, None, (0xff, 0x87, 0x00))
            cls.term_209 = ScreenColor(209, None, (0xff, 0x87, 0x5f))
            cls.term_210 = ScreenColor(210, None, (0xff, 0x87, 0x87))
            cls.term_211 = ScreenColor(211, None, (0xff, 0x87, 0xaf))
            cls.term_212 = ScreenColor(212, None, (0xff, 0x87, 0xd7))
            cls.term_213 = ScreenColor(213, None, (0xff, 0x87, 0xff))
            cls.term_214 = ScreenColor(214, None, (0xff, 0xaf, 0x00))
            cls.term_215 = ScreenColor(215, None, (0xff, 0xaf, 0x5f))
            cls.term_216 = ScreenColor(216, None, (0xff, 0xaf, 0x87))
            cls.term_217 = ScreenColor(217, None, (0xff, 0xaf, 0xaf))
            cls.term_218 = ScreenColor(218, None, (0xff, 0xaf, 0xd7))
            cls.term_219 = ScreenColor(219, None, (0xff, 0xaf, 0xff))
            cls.term_220 = ScreenColor(220, None, (0xff, 0xd7, 0x00))
            cls.term_221 = ScreenColor(221, None, (0xff, 0xd7, 0x5f))
            cls.term_222 = ScreenColor(222, None, (0xff, 0xd7, 0x87))
            cls.term_223 = ScreenColor(223, None, (0xff, 0xd7, 0xaf))
            cls.term_224 = ScreenColor(224, None, (0xff, 0xd7, 0xd7))
            cls.term_225 = ScreenColor(225, None, (0xff, 0xd7, 0xff))
            cls.term_226 = ScreenColor(226, None, (0xff, 0xff, 0x00))
            cls.term_227 = ScreenColor(227, None, (0xff, 0xff, 0x5f))
            cls.term_228 = ScreenColor(228, None, (0xff, 0xff, 0x87))
            cls.term_229 = ScreenColor(229, None, (0xff, 0xff, 0xaf))
            cls.term_230 = ScreenColor(230, None, (0xff, 0xff, 0xd7))
            cls.term_231 = ScreenColor(231, None, (0xff, 0xff, 0xff))
            cls.term_232 = ScreenColor(232, None, (0x08, 0x08, 0x08))
            cls.term_233 = ScreenColor(233, None, (0x12, 0x12, 0x12))
            cls.term_234 = ScreenColor(234, None, (0x1c, 0x1c, 0x1c))
            cls.term_235 = ScreenColor(235, None, (0x26, 0x26, 0x26))
            cls.term_236 = ScreenColor(236, None, (0x30, 0x30, 0x30))
            cls.term_237 = ScreenColor(237, None, (0x3a, 0x3a, 0x3a))
            cls.term_238 = ScreenColor(238, None, (0x44, 0x44, 0x44))
            cls.term_239 = ScreenColor(239, None, (0x4e, 0x4e, 0x4e))
            cls.term_240 = ScreenColor(240, None, (0x58, 0x58, 0x58))
            cls.term_241 = ScreenColor(241, None, (0x60, 0x60, 0x60))
            cls.term_242 = ScreenColor(242, None, (0x66, 0x66, 0x66))
            cls.term_243 = ScreenColor(243, None, (0x76, 0x76, 0x76))
            cls.term_244 = ScreenColor(244, None, (0x80, 0x80, 0x80))
            cls.term_245 = ScreenColor(245, None, (0x8a, 0x8a, 0x8a))
            cls.term_246 = ScreenColor(246, None, (0x94, 0x94, 0x94))
            cls.term_247 = ScreenColor(247, None, (0x9e, 0x9e, 0x9e))
            cls.term_248 = ScreenColor(248, None, (0xa8, 0xa8, 0xa8))
            cls.term_249 = ScreenColor(249, None, (0xb2, 0xb2, 0xb2))
            cls.term_250 = ScreenColor(250, None, (0xbc, 0xbc, 0xbc))
            cls.term_251 = ScreenColor(251, None, (0xc6, 0xc6, 0xc6))
            cls.term_252 = ScreenColor(252, None, (0xd0, 0xd0, 0xd0))
            cls.term_253 = ScreenColor(253, None, (0xda, 0xda, 0xda))
            cls.term_254 = ScreenColor(254, None, (0xe4, 0xe4, 0xe4))
            cls.term_255 = ScreenColor(255, None, (0xee, 0xee, 0xee))

            cls.pink = cls.term_210

    @classmethod
    def all_colors(cls):
        return [c for c in list(cls.__dict__.values())
                if isinstance(c, ScreenColor)]
