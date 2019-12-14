from enum import IntEnum


class EventType(IntEnum):
    NoEvent = 0
    Timer = 1
    KeyPress = 6
    FocusIn = 8
    FocusOut = 9
    Paint = 12
    Move = 13
    Resize = 14
    Show = 17
    Hide = 18
