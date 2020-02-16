import inspect


class SignalDispatcher:
    def __init__(self, signal, obj, obj_class):
        """
        Initialises the Signal Dispatcher. Signal calls this.
        """
        self._signal = signal
        self._obj = obj
        self._obj_class = obj_class
        self._connected_slots = []

    def emit(self, *args, **kwargs):
        """
        Notifies all registered targets by calling them with the passed
        arguments.

        Args:
            *args: any
            **kwargs: any
                Passed to the targets.

        Returns:
            None
        """
        try:
            kwargs.pop("sender")
        except KeyError:
            pass

        for slot in self._connected_slots:
            if "sender" in inspect.signature(slot).parameters:
                slot(*args, sender=self._obj, **kwargs)
            else:
                slot(*args, **kwargs)

    def connect(self, target):
        """
        Registers a given target so that it can be notified when emit() is
        called. the target must be a callable that will be called.
        The emit() parameters will be passed to this callable.
        If the target contains an explicitly named "sender" argument,
        the sender object will be assigned to this argument when emit
        is called on the target.

        Args:
            target: callable
                The target that will be called when emit is called.

        Returns:
            None

        """
        if isinstance(target, SignalDispatcher):
            target = target.emit

        if target not in self._connected_slots:
            self._connected_slots.append(target)

    def disconnect(self, target):
        """
        Disconnects a previously registered target, so that it is no longer
        notified.

        Args:
            target: callable
                A previously registered target.

        Returns:
            None

        """
        try:
            self._connected_slots.remove(target)
        except ValueError:
            pass


class Signal:
    """
    Dispatches a message to a set of listeners, by encapsulating a listener
    pattern. To be used as a descriptor on a class:

    class MyClass:
        my_signal = Signal()

    """

    def __init__(self):
        """
        Instantiate the Signal descriptor.
        """
        self._dispatchers = {}

    def __get__(self, instance, owner):
        """
        Descriptor protocol __get__
        """
        dispatcher = self._dispatchers.get(instance)
        if dispatcher is None:
            dispatcher = SignalDispatcher(self, instance, owner)
            self._dispatchers[instance] = dispatcher

        return dispatcher
