from ..Widget import Widget
from ..Palette import Palette
from ..Painter import Painter


class Dialog(Widget):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
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
        if self._title:

            # 0123456789012
            # +-| hello |-+
            dash_length = (w -                  # total width of the dialog
                           2 -                  # space for the angles
                           # the space for the title itself
                           len(self._title) -
                           2 -                  # the two empty spaces on the
                                                # sides of the title
                           2)                   # the vertical bars
            header = '+' + \
                     "-"*(dash_length/2) + \
                     "| " + \
                     self._title + \
                     " |" + \
                     "-"*(dash_length-(dash_length/2)) + \
                     "+"
        else:
            header = '+'+"-"*(w-2)+"+"

        painter = Painter(self)
        painter.write(0, 0, header, fg, bg)

        for i in range(0, h-2):
            painter.write(0, i+1, '|'+' '*(len(header)-2)+"|", fg, bg)
        painter.write(0, h-1, '+'+"-"*(len(header)-2)+"+", fg, bg)

    def set_title(self, title):
        self._title = title

    def minimum_size(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2, 2)

    def contents_margins(self):
        return (1, 1, 1, 1)
