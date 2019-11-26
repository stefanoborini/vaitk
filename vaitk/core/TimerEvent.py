from .Event import VEvent


class VTimerEvent(VEvent):
    def __init__(self):
        super().__init__(VEvent.EventType.Timer)
