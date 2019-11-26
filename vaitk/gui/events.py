from .. import Key, KeyModifier, native_to_vai_key_code, vai_key_code_to_text
from ..core import Event


class KeyEvent(Event):
    def __init__(self, key_code):
        super().__init__(Event.EventType.KeyPress)
        self._key_code = key_code
        self._accepted = False

    def key_code(self):
        return self._key_code

    def key(self):
        return self._key_code & Key.Mask

    def modifiers(self):
        return self._key_code & KeyModifier.Mask

    def text(self):
        return vai_key_code_to_text(self._key_code)

    @staticmethod
    def from_native_key_code(native_key_code):
        key_code = native_to_vai_key_code(native_key_code)
        if key_code is None:
            return None
        return KeyEvent(key_code)


class FocusEvent(Event):
    def __init__(self, focus_type):
        super().__init__(focus_type)


class PaintEvent(Event):
    def __init__(self):
        super().__init__(Event.EventType.Paint)


class HideEvent(Event):
    def __init__(self):
        super().__init__(Event.EventType.Hide)


class ShowEvent(Event):
    def __init__(self):
        super().__init__(Event.EventType.Show)


class MoveEvent(Event):
    def __init__(self):
        super().__init__(Event.EventType.Move)


class ResizeEvent(Event):
    def __init__(self):
        super().__init__(Event.EventType.Resize)
