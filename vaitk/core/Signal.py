class Signal(object):
    def __init__(self, sender):
        self._sender = sender
        self._slots = []

    def connect(self, target):
        if isinstance(target, Signal):
            slot = target.emit
        else:
            slot = target

        if slot not in self._slots:
            self._slots.append(slot)

    def disconnect(self, target):
        if target in self._slots:
            self._slots.remove(target)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)
