import time
import threading
import logging

from traitlets import Bool, Integer

from vaitk.core.timer_event import TimerEvent
from vaitk.core.signal import Signal
from vaitk.core.CoreApplication import CoreApplication
from vaitk.core.BaseObject import BaseObject


logger = logging.getLogger(__name__)


class _TimerThread(threading.Thread):
    def __init__(self, timeout, single_shot, callback):
        super(_TimerThread, self).__init__()
        self.daemon = True
        self._timeout = timeout
        self._single_shot = single_shot
        self._callback = callback
        self.stop = threading.Event()

    def run(self):
        while True:
            time.sleep(self._timeout/1000.0)
            if self.stop.is_set():
                break
            self._callback()
            if self._single_shot:
                break


class Timer(BaseObject):
    """
    Represents a timer that the user can control.
    Once instantiated, it is started with the appropriate
    method start(). One can connect to the timeout Signal to have
    methods or function called when the timer expires.

    When the timer expires, the timeout Signal

    """
    # The signal emitted every time the timer reaches expiration
    timeout = Signal()

    # If true, the timer will expire only once. If False, it will keep
    # firing every interval ms.
    single_shot = Bool(False)

    # The interval between TimerEvents to be delivered, in milliseconds.
    # If None, the timer will not start.
    interval = Integer(None, allow_none=True)

    def __init__(self, *args, **kwargs):
        """
        Creates a new empty Timer.
        """
        super().__init__(*args, **kwargs)
        self._thread = None
        CoreApplication.vApp.add_timer(self)

    def start(self):
        """
        Starts the timer.
        """
        if self._thread is not None:
            return
        if self.interval is None:
            return
        self._thread = _TimerThread(
            self.interval, self.single_shot, self._send_timer_event)
        self._thread.start()

    def stop(self):
        """
        Stops a currently running timer at the next expiration.
        """
        if self._thread:
            self._thread.stop.set()

        # XXX problem here. We could incur in deletion of the secondary
        # thread as it's still running.
        self._thread = None

    def is_running(self):
        """
        Returns true if the timer is running.
        """
        return self._thread is not None

    def timer_event(self, event):
        """
        Internal reimplementation. Used to trigger the emit() of the
        self.timeout signal from the main thread.

        Args:
            event: TimerEvent

        Returns:
            None
        """
        if isinstance(event, TimerEvent):
            self.timeout.emit()

    @classmethod
    def single_shot_timer(cls, interval, callback):
        """
        Creates a single shot timer.
        Args:
            interval: The timeout in millisec
            callback: The routine to call when the timeout occurs.

        Returns:
            None

        """
        timer = cls(interval=interval, single_shot=True)
        timer.timeout.connect(callback)
        timer.start()

    def _send_timer_event(self):
        """Helper internal method. Dispatches the event from the secondary
        thread to the main thread via the event loop."""
        CoreApplication.vApp.post_event(self, TimerEvent())

