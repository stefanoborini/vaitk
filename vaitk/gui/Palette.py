'''

import copy

from vaitk.gui.enums import ColorGroup, ColorRole
from vaitk.core.color import Color


class Palette:
    def __init__(self):
        self._colors = {}

    def color(self, color_group, color_role):
        return self._colors[(color_group, color_role)]

    def set_color(self, color_group, color_role, color):
        self._colors[(color_group, color_role)] = color

    def set_defaults(self):
        self._colors = {
            (ColorGroup.Active, ColorRole.WindowText): Color(170, 170, 170),
            (ColorGroup.Active, ColorRole.Button): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Light): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Midlight): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Dark): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Mid): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Text): Color(170, 170, 170),
            (ColorGroup.Active, ColorRole.BrightText): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.ButtonText): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.Base): Color(0, 0, 0),
            (ColorGroup.Active, ColorRole.Window): None,
            (ColorGroup.Active, ColorRole.Shadow): Color(0, 0, 0),
            (ColorGroup.Active, ColorRole.Highlight): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.HighlightedText): Color(0, 0, 0),
            (ColorGroup.Active, ColorRole.Link): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.LinkVisited): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.AlternateBase): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.NoRole): Color(255, 255, 255),
            (ColorGroup.Active, ColorRole.ToolTipBase): Color(170, 0, 170),
            (ColorGroup.Active, ColorRole.ToolTipText): Color(255, 255, 0),
            (ColorGroup.Disabled, ColorRole.WindowText): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Button): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Light): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Midlight): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Dark): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Mid): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Text): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.BrightText): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.ButtonText): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.Base): Color(0, 0, 0),
            (ColorGroup.Disabled, ColorRole.Window): None,
            (ColorGroup.Disabled, ColorRole.Shadow): Color(0, 0, 0),
            (ColorGroup.Disabled, ColorRole.Highlight): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.HighlightedText): Color(0, 0, 0),
            (ColorGroup.Disabled, ColorRole.Link): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.LinkVisited): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.AlternateBase): Color(255, 255, 255),  # noqa
            (ColorGroup.Disabled, ColorRole.NoRole): Color(255, 255, 255),
            (ColorGroup.Disabled, ColorRole.ToolTipBase): Color(0, 0, 0),
            (ColorGroup.Disabled, ColorRole.ToolTipText): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.WindowText): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Button): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Light): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Midlight): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Dark): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Mid): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Text): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.BrightText): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.ButtonText): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.Base): Color(0, 0, 0),
            (ColorGroup.Inactive, ColorRole.Window): None,
            (ColorGroup.Inactive, ColorRole.Shadow): Color(0, 0, 0),
            (ColorGroup.Inactive, ColorRole.Highlight): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.HighlightedText): Color(0, 0, 0),
            (ColorGroup.Inactive, ColorRole.Link): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.LinkVisited): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.AlternateBase): Color(255, 255, 255),  # noqa
            (ColorGroup.Inactive, ColorRole.NoRole): Color(255, 255, 255),
            (ColorGroup.Inactive, ColorRole.ToolTipBase): Color(0, 0, 0),
            (ColorGroup.Inactive, ColorRole.ToolTipText): Color(255, 255, 255)
        }

    def copy(self):
        return copy.deepcopy(self)
'''
