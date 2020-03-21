from vaitk.core.events.event import Event
from vaitk.core.enums import EventType


class TimerEvent(Event):
    """
    Event representing the expiration of a timer
    """
    def __init__(self):
        super().__init__(EventType.Timer)
