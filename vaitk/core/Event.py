class Event:

    def __init__(self, event_type):
        self._event_type = event_type
        self._accepted = False

    def accept(self):
        self.set_accepted(True)

    def ignore(self):
        self.set_accepted(False)

    def is_accepted(self):
        return self._accepted

    def set_accepted(self, accepted):
        self._accepted = accepted

    def event_type(self):
        return self._event_type

    def __str__(self):
        return (self.__class__.__name__+"(%d)") % self.event_type()
