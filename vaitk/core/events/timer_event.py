from vaitk.core.events.event import Event
from vaitk.core.events.event_type import EventType


class TimerEvent(Event):
    """
    Event representing the expiration of a timer
    """
    def __init__(self):
        super().__init__(event_type=EventType.Timer)
