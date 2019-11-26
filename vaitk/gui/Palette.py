from . import Color
import copy


class VPalette:
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
            (VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText):
                Color.VColor(rgb=(170, 170, 170)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Button):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Light):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Midlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Dark):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Mid):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Text):
            Color.VColor(rgb=(170, 170, 170)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.BrightText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.ButtonText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Base):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Window):
            None,
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Shadow):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Highlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.HighlightedText):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.Link):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.LinkVisited):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.AlternateBase):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.NoRole):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipBase):
            Color.VColor(rgb=(170, 0, 170)),
            (VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipText):
            Color.VColor(rgb=(255, 255, 0)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.WindowText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Button):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Light):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Midlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Dark):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Mid):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Text):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.BrightText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.ButtonText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Base):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Window):
            None,
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Shadow):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Highlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.HighlightedText):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.Link):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.LinkVisited):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.AlternateBase):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.NoRole):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.ToolTipBase):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Disabled, VPalette.ColorRole.ToolTipText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.WindowText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Button):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Light):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Midlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Dark):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Mid):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Text):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.BrightText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.ButtonText):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Base):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Window):
            None,
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Shadow):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Highlight):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.HighlightedText):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.Link):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.LinkVisited):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.AlternateBase):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.NoRole):
            Color.VColor(rgb=(255, 255, 255)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.ToolTipBase):
            Color.VColor(rgb=(0, 0, 0)),
            (VPalette.ColorGroup.Inactive, VPalette.ColorRole.ToolTipText):
            Color.VColor(rgb=(255, 255, 255))
        }

    def copy(self):
        return copy.deepcopy(self)
