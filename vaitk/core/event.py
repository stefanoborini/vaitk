from traitlets import HasTraits, UseEnum, Bool

from vaitk.core.enums import EventType


class Event(HasTraits):
    event_type = UseEnum(EventType)
    accepted = Bool(False)

    def __init__(self, event_type):
        super().__init__(event_type=event_type)

    def accept(self):
        self.accepted = True

    def ignore(self):
        self.accepted = False

    def __str__(self):
        return f"{self.__class__.__name__}(event_type={self.event_type})"
