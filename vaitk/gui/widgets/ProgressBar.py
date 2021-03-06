'''
from vaitk.gui.Widget import Widget
from vaitk.gui.Palette import Palette
from vaitk.gui.Painter import Painter


class ProgressBar(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._minimum = 0
        self._maximum = 100
        self._value = 0

    def paint_event(self, event):
        painter = Painter(self)
        w, h = self.size()
        fg_color = self.palette().color(Palette.ColorGroup.Active,
                                        Palette.ColorRole.WindowText)
        bg_color = self.palette().color(Palette.ColorGroup.Active,
                                        Palette.ColorRole.Window)

        final_text = ""
        if len(self._text) > 0:
            final_text += (self._text + " ")

        percentage = int(100 * (self.value() - self.minimum()) /
                         (self.maximum() - self.minimum()))
        percentage_text = ("%d" % percentage) + "%"
        bar_total_length = w - len(final_text) - 2
        if bar_total_length < 5:
            bar_text = percentage_text.rjust(4)
        else:
            bar_fill_length = int(bar_total_length * percentage / 100)
            bar_text = ("="*bar_fill_length) + \
                (' '*(bar_total_length-bar_fill_length))
            bar_text = bar_text[:int(bar_total_length/2)-1] + \
                percentage_text + \
                bar_text[int(bar_total_length/2)-1+len(percentage_text):]

        final_text += '[' + bar_text + ']'
        painter.draw_text((0, 0), final_text, fg_color, bg_color)

    def minimum_size(self):
        if len(self._text) > 0:
            width = len(self._text)+len(" [100%]")
        else:
            width = len("[100%]")

        return (width, 1)

    def set_value(self, value):
        if self._value != value and (self._minimum < value < self._maximum):
            self._value = value
            self.update()

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def set_minimum(self, minimum):
        if self._minimum == minimum:
            return

        self._minimum = minimum
        if self._minimum > self._maximum:
            self._maximum = self._minimum

        if not (self._minimum < self._value < self._maximum):
            self.reset()
        else:
            self.update()

    def set_maximum(self, maximum):
        if self._maximum == maximum:
            return

        self._maximum = maximum
        if self._maximum < self._minimum:
            self._minimum = self._maximum

        if not (self._minimum < self._value < self._maximum):
            self.reset()
        else:
            self.update()

    def reset(self):
        self._value = self._minimum
        self.update()

    def set_range(self, minimum, maximum):
        if self._minimum == minimum and self._maximum == maximum:
            return

        self._minimum = minimum
        self._maximum = maximum

        if self._maximum < self._minimum:
            self._maximum = self._minimum

        if not (self._minimum < self._value < self._maximum):
            self.reset()
        else:
            self.update()

    def set_text(self, text):
        self._text = text

    def text(self):
        return self._text

    def value(self):
        return self._value
'''
