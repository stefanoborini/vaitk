class SignalDispatcher:
    def __init__(self, signal, obj, obj_class):
        self._signal = signal
        self._obj = obj
        self._obj_class = obj_class
        self._connected_slots = []

    def emit(self, *args, **kwargs):
        kwargs["sender"] = self._obj

        for slot in self._connected_slots:
            slot(*args, **kwargs)

    def connect(self, target):
        if isinstance(target, SignalDispatcher):
            target = target.emit

        if target not in self._connected_slots:
            self._connected_slots.append(target)

    def disconnect(self, target):
        try:
            self._connected_slots.remove(target)
        except ValueError:
            pass

class Signal:
    """
    Dispatches a message to a set of listeners, by encapsulating a listener
    pattern.
    """

    def __init__(self):
        self._dispatchers = {}

    def __get__(self, instance, owner):
        dispatcher = self._dispatchers.get(instance)
        if dispatcher is None:
            dispatcher = SignalDispatcher(self, instance, owner)
            self._dispatchers[instance] = dispatcher

        return dispatcher

    '''
    def __init__(self):
        """
        Instantiate the Signal. The passed sender is the entity
        that will be communicated as the sender to the receiver.

        Args:
            sender: BaseObject
                The object that will be communicated to the listeners
                as the sender of the notification.
        """
        self._slots = []

    def connect(self, target):
        """
        Registers a given target so that it can be notified when emit() is
        called. the target must be a callable that will be called.
        The emit() parameters will be passed to this callable.

        Args:
            target: callable
                The target that will be called when emit is called.
                Signature must accept *args and **kwargs
        Returns:
            None

        """
        if isinstance(target, Signal):
            slot = target.emit
        else:
            slot = target

        if slot not in self._slots:
            self._slots.append(slot)

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
        if target in self._slots:
            self._slots.remove(target)

    def emit(self, *args, **kwargs):
        """
        Notifies all registered targets by calling them with the passed
        arguments. The additional argument "sender' will be added to
        the kwargs, containing the self.sender.

        Args:
            *args: any
            **kwargs: any
                Passed to the targets.

        Returns:
            None

        """
        if "sender" in kwargs:
            raise ValueError("sender cannot be specified as named argument in "
                             "emit()")

        kwargs["sender"] = self._sender
        for slot in self._slots:
            slot(*args, **kwargs)
    '''
