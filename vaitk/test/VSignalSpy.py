from ..core.BaseObject import VObject


class VSignalSpy(VObject):
    def __init__(self, signal):
        self._signal_params = []
        self._signal = signal
        self._signal.connect(self._signal_received)

    def _signal_received(self, *args, **kwargs):
        self._signal_params.append((args, kwargs))

    def count(self):
        return len(self._signal_params)

    def last_signal_params(self):
        return self._signal_params[-1]

    def signal_params(self):
        return self._signal_params
