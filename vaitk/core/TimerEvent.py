from vaitk.core.enums import EventType
from .Event import Event


class TimerEvent(Event):
    def __init__(self):
        super().__init__(EventType.Timer)
