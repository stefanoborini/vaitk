from traitlets import Unicode, Int

from vaitk.core.events.event_type import EventType
from vaitk.core.events.event import Event
from vaitk.keys import KeyModifier


class KeyEvent(Event):
    char = Unicode(allow_none=True)
    modifier = Int()

    def __init__(self, char=None, modifier=KeyModifier.NoModifier):
        super().__init__(
            event_type=EventType.KeyPress,
            char=char,
            modifier=modifier
        )
