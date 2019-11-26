from .CoreApplication import VCoreApplication
from .BaseObject import VObject
from .Signal import VSignal
from . import VTimerEvent
import time
import threading


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


class VTimer(VObject):
    def __init__(self):
        super().__init__()
        self._interval = None
        self._single_shot = False
        self.timeout = VSignal(self)
        self._thread = None
        VCoreApplication.vApp.addTimer(self)

    def start(self):
        if self._thread is not None:
            return
        if self._interval is None:
            return
        self._thread = _TimerThread(
            self._interval, self._single_shot, self._timeout)
        self._thread.start()

    def _timeout(self):
        VCoreApplication.vApp.post_event(self, VTimerEvent.VTimerEvent())

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
        if isinstance(event, VTimerEvent.VTimerEvent):
            self.timeout.emit()

    @staticmethod
    def single_shot(timeout, callback):
        timer = VTimer()
        timer.set_interval(timeout)
        timer.set_single_shot(True)
        timer.timeout.connect(callback)
        timer.start()
