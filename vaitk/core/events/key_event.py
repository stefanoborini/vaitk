from traitlets import Unicode, Int

from vaitk.core.enums import EventType
from vaitk.core.events.event import Event


class KeyEvent(Event):
    char = Unicode(allow_none=True)
    modifier = Int()

    def __init__(self, char=None, modifier=None):
        super().__init__(
            event_type=EventType.KeyPress,
            char=char,
            modifier=modifier
        )
