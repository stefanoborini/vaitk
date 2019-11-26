from .BaseObject import VObject
from .Signal import VSignal


class VCoreApplication(VObject):
    """
    Core application class. Only one instance is allowed to exist.
    """
    vApp = None

    def __init__(self, argv):
        super().__init__()
        self._timers = []

        if VCoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VCoreApplication.vApp = self
        self.aboutToQuit = VSignal(self)

    def add_timer(self, timer):
        """
        Add a timer to the application.
        This routine should not be called manually.
        """
        self._timers.append(timer)

    def exit(self, retcode=0):
        """
        Exits the application.
        """
        VCoreApplication.vApp = None

    def send_event(self, receiver, event):
        """
        Directly send an event to a receiver.
        """
        receiver.event(event)

    def application_name(self):
        raise NotImplementedError()

    def application_version(self):
        raise NotImplementedError()

    def instance(self):
        raise NotImplementedError()

    def exec_(self):
        raise NotImplementedError()

    def process_events(self, flags):
        raise NotImplementedError()

    def post_event(self, receiver, event):
        raise NotImplementedError()

    def send_posted_event(self, receiver, event_type):
        raise NotImplementedError()

    def remove_posted_event(self, receiver, event_type):
        raise NotImplementedError()

    def has_pending_events(self):
        raise NotImplementedError()

    def notify(self, receiver, event):
        raise NotImplementedError()

    def application_dir_path(self):
        raise NotImplementedError()

    def application_file_path(self):
        raise NotImplementedError()

    def starting_up(self):
        raise NotImplementedError()

    def closing_down(self):
        raise NotImplementedError()

    def set_event_filter(self, event_filter):
        raise NotImplementedError()
