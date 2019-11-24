from .. import Key, KeyModifier, nativeToVaiKeyCode, vaiKeyCodeToText
from ..core import VEvent


class VKeyEvent(VEvent):
    def __init__(self, key_code):
        super().__init__(VEvent.EventType.KeyPress)
        self._key_code = key_code
        self._accepted = False

    def keyCode(self):
        return self._key_code

    def key(self):
        return self._key_code & Key.Mask

    def modifiers(self):
        return self._key_code & KeyModifier.Mask

    def text(self):
        return vaiKeyCodeToText(self._key_code)

    @staticmethod
    def fromNativeKeyCode(native_key_code):
        key_code = nativeToVaiKeyCode(native_key_code)
        if key_code is None:
            return None
        return VKeyEvent(key_code)


class VFocusEvent(VEvent):
    def __init__(self, focus_type):
        super().__init__(focus_type)


class VPaintEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Paint)


class VHideEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Hide)


class VShowEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Show)


class VMoveEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Move)


class VResizeEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Resize)
