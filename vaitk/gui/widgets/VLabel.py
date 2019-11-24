from ..VWidget import VWidget
from ..VPainter import VPainter
from ..VPalette import VPalette


class VLabel(VWidget):
    def __init__(self, label="", parent=None):
        super().__init__(parent)
        self._label = label

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                                VPalette.ColorRole.WindowText)
        painter.bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                                VPalette.ColorRole.Window)
        string = ' '*w
        for i in range(0, int(h/2)):
            painter.drawText((0, i), string)
        painter.drawText((0, int(h/2)), self._label + ' '*(w-len(self._label)))
        for i in range(1+int(h/2), h):
            painter.drawText((0, i), string)

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        if text != self._label:
            self._label = text
            self.update()
