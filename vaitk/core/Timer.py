import time
import threading
import logging

from vaitk.core import TimerEvent
from .CoreApplication import CoreApplication
from .BaseObject import BaseObject
from .Signal import Signal


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
    def __init__(self):
        super().__init__()
        self._interval = None
        self._single_shot = False
        self.timeout = Signal(self)
        self._thread = None
        CoreApplication.vApp.add_timer(self)

    def start(self):
        if self._thread is not None:
            return
        if self._interval is None:
            return
        self._thread = _TimerThread(
            self._interval, self._single_shot, self._timeout)
        self._thread.start()

    def _timeout(self):
        CoreApplication.vApp.post_event(self, TimerEvent())

    def set_single_shot(self, single_shot):
        self._single_shot = single_shot

    def set_interval(self, interval):
        self._interval = interval

    def stop(self):
        if self._thread:
            self._thread.stop.set()

        # XXX problem here. We could incur in deletion of the secondary
        # thread as it's still running.
        self._thread = None

    def is_running(self):
        return self._thread is not None

    def timer_event(self, event):
        if isinstance(event, TimerEvent):
            self.timeout.emit()

    @staticmethod
    def single_shot(timeout, callback):
        timer = Timer()
        timer.set_interval(timeout)
        timer.set_single_shot(True)
        timer.timeout.connect(callback)
        timer.start()
