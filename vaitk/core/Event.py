class VEvent:
    class EventType:
        NoEvent = 0
        Timer = 1
        KeyPress = 6
        FocusIn = 8
        FocusOut = 9
        Paint = 12
        Move = 13
        Resize = 14
        Show = 17
        Hide = 18

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
