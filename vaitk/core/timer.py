import logging

from traitlets import Bool, Integer

from vaitk.core.events.timer_event import TimerEvent
from vaitk.core.signal import Signal
from vaitk.core.core_application import CoreApplication
from vaitk.core.base_object import BaseObject


logger = logging.getLogger(__name__)


class Timer(BaseObject):
    """
    An asyncio-backed timer.

    Timer callbacks are delivered on the application's event-loop thread.
    The interval is expressed in milliseconds.
    """
    timeout = Signal()
    single_shot = Bool(False)
    interval = Integer(None, allow_none=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._handle = None
        self._application = CoreApplication.vApp
        if self._application is None:
            raise RuntimeError("A CoreApplication must exist before creating a Timer")
        self._application.add_timer(self)

    def start(self):
        """Start the timer; repeated calls while running have no effect."""
        if self.is_running() or self.interval is None:
            return
        if self.interval < 0:
            raise ValueError("Timer interval must not be negative")
        self._schedule()

    def stop(self):
        """Cancel the pending timer callback, if any."""
        if self._handle is not None:
            self._handle.cancel()
            self._handle = None

    def is_running(self):
        """Return whether a timer callback is currently scheduled."""
        return self._handle is not None and not self._handle.cancelled()

    def timer_event(self, event):
        """Deliver a timer event by emitting the timeout signal."""
        if isinstance(event, TimerEvent):
            self.timeout.emit()

    @classmethod
    def single_shot_timer(cls, interval, callback):
        """Schedule callback once after interval milliseconds."""
        timer = cls(interval=interval, single_shot=True)
        timer.timeout.connect(callback)
        timer.start()
        return timer

    def _schedule(self):
        self._handle = self._application.loop.call_later(
            self.interval / 1000.0, self._send_timer_event)

    def _send_timer_event(self):
        self._handle = None
        self._application.send_event(self, TimerEvent())
        if not self.single_shot and self._application.vApp is self._application:
            self._schedule()
