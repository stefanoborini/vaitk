import logging

from vaitk.consts import Index
from vaitk.gui.AbstractRectangularArea import AbstractRectangularArea


class ScreenArea(AbstractRectangularArea):
    def __init__(self, screen, rect):
        self._screen = screen
        self._rect = rect
        self.logger = logging.getLogger(self.__class__.__name__)
        if hasattr(self, "debug"):
            self.logger.setLevel(self.debug)
        else:
            self.logger.setLevel(logging.CRITICAL+1)

    def write(self, pos, string, fg_color=None, bg_color=None):
        rel_x, rel_y = pos
        w, h = self.size()

        if rel_y < 0 or rel_y >= h or rel_x >= w:
            self.logger.error(
                ("Out of bound in VScreenArea.write: "
                 "pos=%s size=%s len=%d '%s'") % (
                    str(pos), str(self.size()), len(string), string))
            return

        out_string = string
        if rel_x < 0:
            self.logger.error(
                ("Out of bound in VScreenArea.write: "
                 "pos=%s size=%s len=%d '%s'") % (
                    str(pos), str(self.size()), len(string), string))
            out_string = string[-rel_x:]
            rel_x = 0

        if len(out_string) == 0:
            return

        if (rel_x+len(out_string) > w):
            self.logger.error(
                ("Out of bound in VScreenArea.write: "
                 "pos=%s size=%s len=%d '%s'") % (
                    str(pos), str(self.size()), len(string), string))
            out_string = out_string[:w-rel_x]

        top_left_x, top_left_y = self.top_left()
        self._screen.write((rel_x+top_left_x, rel_y+top_left_y),
                           out_string,
                           fg_color,
                           bg_color)

    def set_colors(self, pos, colors):
        rel_x, rel_y = pos
        w, h = self.size()

        if rel_y < 0 or rel_y >= h or rel_x >= w:
            self.logger.error(
                ("Out of bound in VScreenArea.setColors: "
                 "pos=%s size=%s len=%d") % (
                    str(pos), str(self.size()), len(colors)))
            return

        out_colors = colors
        if rel_x < 0:
            self.logger.error(
                ("Out of bound in VScreenArea.setColors: "
                 "pos=%s size=%s len=%d") % (
                    str(pos), str(self.size()), len(colors)))
            out_colors = colors[-rel_x:]
            rel_x = 0

        if len(out_colors) == 0:
            return

        if (rel_x+len(out_colors) > w):
            self.logger.error(
                ("Out of bound in VScreenArea.setColors: "
                 "pos=%s size=%s len=%d") % (
                    str(pos), str(self.size()), len(colors)))
            out_colors = out_colors[:w-rel_x]

        top_left_x, top_left_y = self.top_left()
        self._screen.set_colors(
            (rel_x+top_left_x, rel_y+top_left_y), out_colors)

    def rect(self):
        return self._rect

    def screen(self):
        return self._screen

    def erase(self):
        for y in range(self.height()):
            self.write((0, y), ' '*self.width())

    def out_of_bounds(self, pos):
        x, y = pos
        return (x >= self.size()[Index.SIZE_WIDTH] or
                y >= self.size()[Index.SIZE_HEIGHT] or x < 0 or y < 0)
