from ..VWidget import VWidget
from ..VPalette import VPalette
from ..VPainter import VPainter

class VFrame(VWidget):
    def __init__(self, parent=None):
        super(VFrame, self).__init__(parent)
        self._title = None

    def paintEvent(self, event):
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)
        w, h = self.size()
        painter = VPainter(self)
        painter.fillRect( (0,0,w,h) )
        if self._title:
            title_pos = int((w - len(self._title)) / 2)
            painter.drawText( (0, dash_length), " " + self._title + " ", fg, bg)

    def setTitle(self, title):
        self._title = title

    def minimumSize(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2,2)

    def contentsMargins(self):
        return (1,1,1,1)
