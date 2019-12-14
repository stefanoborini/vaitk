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


