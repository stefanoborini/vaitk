from traitlets import HasTraits, UseEnum, Bool

from vaitk.core.events.event_type import EventType


class Event(HasTraits):
    event_type = UseEnum(EventType)
    accepted = Bool(False)

    def __init__(self, event_type, *args, **kwargs):
        super().__init__(event_type=event_type, *args, **kwargs)

    def accept(self):
        self.accepted = True

    def ignore(self):
        self.accepted = False

    def __str__(self):
        return f"{self.__class__.__name__}(event_type={self.event_type})"
