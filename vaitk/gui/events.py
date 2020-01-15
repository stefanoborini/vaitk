from traitlets import Int
from vaitk.core.enums import EventType
from vaitk.keys import Key, KeyModifier, vai_key_code_to_text, \
    native_to_vai_key_code
from vaitk.core import Event


class KeyEvent(Event):
    key_code = Int()

    def __init__(self, key_code):
        super().__init__(EventType.KeyPress)
        self.key_code = key_code

    @property
    def key(self):
        return self.key_code & Key.Mask

    @property
    def modifiers(self):
        return self.key_code & KeyModifier.Mask

    @property
    def text(self):
        return vai_key_code_to_text(self.key_code)

    @classmethod
    def from_native_key_code(cls, native_key_code):
        key_code = native_to_vai_key_code(native_key_code)
        if key_code is None:
            raise ValueError(f"Unknown native key code {native_key_code}")
        return cls(key_code)


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
