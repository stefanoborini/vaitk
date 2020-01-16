from vaitk.gui.Widget import Widget
from vaitk.gui.Palette import Palette
from vaitk.gui.Painter import Painter


class Label(Widget):
    def __init__(self, label="", parent=None):
        super().__init__(parent)
        self._label = label

    def paint_event(self, event):
        painter = Painter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(Palette.ColorGroup.Active,
                                                Palette.ColorRole.WindowText)
        painter.bg_color = self.palette().color(Palette.ColorGroup.Active,
                                                Palette.ColorRole.Window)
        string = ' '*w
        for i in range(0, int(h/2)):
            painter.draw_text((0, i), string)
        painter.draw_text((0, int(h / 2)),
                          self._label + ' ' * (w - len(self._label)))
        for i in range(1+int(h/2), h):
            painter.draw_text((0, i), string)

    def minimum_size(self):
        return (len(self._label), 1)

    def set_text(self, text):
        if text != self._label:
            self._label = text
            self.update()
