import asyncio
import logging

from traitlets import Unicode, Instance, default

from vaitk.core import BaseObject, Signal, Size
from vaitk.core.drivers.abc.abc_driver import ABCDriver
from vaitk.core.drivers.text.text_screen_driver import TextScreenDriver

logger = logging.getLogger(__name__)


class CoreApplication(BaseObject):
    """
    Core application class. Only one instance is allowed to exist.

    The application owns an asyncio event loop. Use :meth:`run` to run it
    and :meth:`exit` to stop it. Work submitted from other threads is
    marshalled onto the loop with :meth:`post_event`.
    """
    vApp = None

    application_name = Unicode()
    application_version = Unicode()

    about_to_quit = Signal()

    _driver = Instance(ABCDriver)

    def __init__(self, argv, loop=None):
        if CoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        super().__init__(application_name=argv[0])
        self._timers = []
        self._loop = loop if loop is not None else asyncio.new_event_loop()
        self._owns_loop = loop is None
        self._exit_requested = False
        CoreApplication.vApp = self

    @property
    def instance(self):
        return self.vApp

    @property
    def loop(self):
        """The asyncio event loop owned by this application."""
        return self._loop

    @default("_driver")
    def _driver_default(self):
        return TextScreenDriver(Size(40, 30))

    def add_timer(self, timer):
        """Register a timer with the application."""
        if timer not in self._timers:
            self._timers.append(timer)

    def run(self):
        """Run the application's asyncio event loop until :meth:`exit`."""
        if self._exit_requested:
            return
        if self._loop.is_running():
            raise RuntimeError("The application event loop is already running")
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            asyncio.set_event_loop(None)
            if self._exit_requested and self._owns_loop and not self._loop.is_closed():
                self._loop.close()

    def post_event(self, receiver, event):
        """Schedule event delivery on the application loop.

        This method is safe to call from a thread other than the loop thread.
        """
        if self._loop.is_closed():
            return
        self._loop.call_soon_threadsafe(self.send_event, receiver, event)

    def exit(self, retcode=0):
        """Stop the event loop and release the application singleton."""
        if self._exit_requested:
            return
        self._exit_requested = True
        for timer in tuple(self._timers):
            timer.stop()
        self.about_to_quit.emit()
        if self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        CoreApplication.vApp = None
        if self._owns_loop and not self._loop.is_running():
            self._loop.close()

    def send_event(self, receiver, event):
        """Directly send an event to a receiver on the loop thread."""
        receiver.event(event)
