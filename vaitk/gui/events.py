'''
from traitlets import Int
from vaitk.core.enums import EventType
from vaitk.keys import Key, KeyModifier, vai_key_code_to_text, \
    native_to_vai_key_code
from vaitk.core import Event


class FocusInEvent(Event):
    def __init__(self):
        super().__init__(EventType.FocusIn)


class FocusOutEvent(Event):
    def __init__(self):
        super().__init__(EventType.FocusOut)


class PaintEvent(Event):
    def __init__(self):
        super().__init__(EventType.Paint)


class HideEvent(Event):
    def __init__(self):
        super().__init__(EventType.Hide)


class ShowEvent(Event):
    def __init__(self):
        super().__init__(EventType.Show)


class MoveEvent(Event):
    def __init__(self):
        super().__init__(EventType.Move)


class ResizeEvent(Event):
    def __init__(self):
        super().__init__(EventType.Resize)
'''
