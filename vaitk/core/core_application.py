import logging

from traitlets import Unicode, Instance, default

from vaitk.core import BaseObject, Signal, Size
from vaitk.core.drivers.abc.abc_driver import ABCDriver
from vaitk.core.drivers.text.text_screen_driver import TextScreenDriver

logger = logging.getLogger(__name__)


class CoreApplication(BaseObject):
    """
    Core application class. Only one instance is allowed to exist.
    """
    vApp = None

    application_name = Unicode()
    application_version = Unicode()

    about_to_quit = Signal()

    _driver = Instance(ABCDriver)

    def __init__(self, argv):
        super().__init__(application_name=argv[0])

        self._timers = []

        if CoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        CoreApplication.vApp = self

    @property
    def instance(self):
        return self.vApp

    @default("_driver")
    def _driver_default(self):
        return TextScreenDriver(Size(40, 30))

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
