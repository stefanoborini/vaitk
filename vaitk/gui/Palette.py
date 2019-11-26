from . import Color
import copy


class Palette:
    class ColorGroup:
        Active, Disabled, Inactive = list(range(3))

    class ColorRole:
        WindowText, \
            Button, \
            Light, \
            Midlight, \
            Dark, \
            Mid, \
            Text, \
            BrightText, \
            ButtonText, \
            Base, \
            Window, \
            Shadow, \
            Highlight, \
            HighlightedText, \
            Link, \
            LinkVisited, \
            AlternateBase, \
            NoRole, \
            ToolTipBase, \
            ToolTipText = list(range(20))

    def __init__(self):
        self._colors = {}

    def color(self, color_group, color_role):
        return self._colors[(color_group, color_role)]

    def set_color(self, color_group, color_role, color):
        self._colors[(color_group, color_role)] = color

    def set_defaults(self):
        self._colors = {
            (Palette.ColorGroup.Active, Palette.ColorRole.WindowText):
                Color.Color(rgb=(170, 170, 170)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Button):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Light):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Midlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Dark):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Mid):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Text):
            Color.Color(rgb=(170, 170, 170)),
            (Palette.ColorGroup.Active, Palette.ColorRole.BrightText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.ButtonText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Base):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Window):
            None,
            (Palette.ColorGroup.Active, Palette.ColorRole.Shadow):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Highlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.HighlightedText):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Active, Palette.ColorRole.Link):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.LinkVisited):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.AlternateBase):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.NoRole):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Active, Palette.ColorRole.ToolTipBase):
            Color.Color(rgb=(170, 0, 170)),
            (Palette.ColorGroup.Active, Palette.ColorRole.ToolTipText):
            Color.Color(rgb=(255, 255, 0)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.WindowText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Button):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Light):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Midlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Dark):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Mid):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Text):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.BrightText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.ButtonText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Base):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Window):
            None,
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Shadow):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Highlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.HighlightedText):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.Link):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.LinkVisited):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.AlternateBase):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.NoRole):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.ToolTipBase):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Disabled, Palette.ColorRole.ToolTipText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.WindowText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Button):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Light):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Midlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Dark):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Mid):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Text):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.BrightText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.ButtonText):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Base):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Window):
            None,
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Shadow):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Highlight):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.HighlightedText):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.Link):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.LinkVisited):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.AlternateBase):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.NoRole):
            Color.Color(rgb=(255, 255, 255)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.ToolTipBase):
            Color.Color(rgb=(0, 0, 0)),
            (Palette.ColorGroup.Inactive, Palette.ColorRole.ToolTipText):
            Color.Color(rgb=(255, 255, 255))
        }

    def copy(self):
        return copy.deepcopy(self)
