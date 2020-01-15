from vaitk.gui.Widget import Widget
from vaitk.gui.Palette import Palette
from vaitk.gui.Painter import Painter


class Frame(Widget):
    def __init__(self, parent=None):
        super(Frame, self).__init__(parent)
        self._title = None

    def paint_event(self, event):
        if self.is_enabled():
            if self.is_active():
                color_group = Palette.ColorGroup.Active
            else:
                color_group = Palette.ColorGroup.Inactive
        else:
            color_group = Palette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)
        w, h = self.size()
        painter = Painter(self)
        painter.fill_rect((0, 0, w, h))
        if self._title:
            dash_length = 0  # FIXME
            painter.draw_text((0, dash_length),
                              " " + self._title + " ", fg, bg)

    def set_title(self, title):
        self._title = title

    def minimum_size(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2, 2)

    def contents_margins(self):
        return (1, 1, 1, 1)
