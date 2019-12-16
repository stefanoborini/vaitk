import logging

from traitlets import Unicode


from .BaseObject import BaseObject
from .Signal import Signal


logger = logging.getLogger(__name__)


class CoreApplication(BaseObject):
    """
    Core application class. Only one instance is allowed to exist.
    """
    vApp = None

    application_name = Unicode()
    application_version = Unicode()

    def __init__(self, argv):
        super().__init__(application_name=argv[0])

        self._timers = []
        self.aboutToQuit = Signal(self)

        if CoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        CoreApplication.vApp = self

    @property
    def instance(self):
        return self.vApp

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
        CoreApplication.vApp = None

    def send_event(self, receiver, event):
        """
        Directly send an event to a receiver.
        """
        receiver.event(event)
