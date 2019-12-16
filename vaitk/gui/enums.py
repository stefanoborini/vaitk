from enum import IntEnum


class FocusPolicy(IntEnum):
    NoFocus = 0
    StrongFocus = 11


class Orientation(IntEnum):
    Horizontal = 1
    Vertical = 2


class LineStyle(IntEnum):
    NoLine = 0
    Full = 1


class CornerCapStyle(IntEnum):
    NoCap = 0
    Plus = 1


class LineCapStyle(IntEnum):
    NoCap = 0
    Plus = 1


class Alignment(IntEnum):
    AlignLeft = 0x1
    AlignRight = 0x2
    AlignHCenter = 0x4
    AlignTop = 0x20
    AlignBottom = 0x40
    AlignVCenter = 0x80
    AlignCenter = AlignHCenter | AlignVCenter


class ColorGroup(IntEnum):
    Active = 0
    Disabled = 1
    Inactive = 2


class ColorRole(IntEnum):
    WindowText = 0
    Button = 1
    Light = 2
    Midlight = 3
    Dark = 4
    Mid = 5
    Text = 6
    BrightText = 7
    ButtonText = 8
    Base = 9
    Window = 10
    Shadow = 11
    Highlight = 12
    HighlightedText = 13
    Link = 14
    LinkVisited = 15
    AlternateBase = 16
    NoRole = 17
    ToolTipBase = 18
    ToolTipText = 19

