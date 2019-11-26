from .Label import Label
from ..Painter import Painter
from ..Palette import VPalette


class ToolTip(Label):
    _instance = None
    @classmethod
    def show_text(cls, pos, text):
        """
        Shows the tooltip text at screen position pos.
        Only one tooltip is allowed. If another tooltip is already present,
        it will be moved and the text changed.
        """
        if cls._instance is None:
            cls._instance = ToolTip(text, parent=None)
        cls._instance.set_text(text)
        cls._instance.resize((len(text), 1))
        cls._instance.move(pos)
        cls._instance.show()

    @classmethod
    def hide_text(cls):
        """Hides the tooltip if present"""
        if cls._instance is not None:
            Label.hide(cls._instance)

    def paint_event(self, event):
        painter = Painter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                                VPalette.ColorRole.ToolTipText)
        painter.bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                                VPalette.ColorRole.ToolTipBase)
        painter.draw_text((0, 0), self._label)
