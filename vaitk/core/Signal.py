class Signal(object):
    """
    Dispatches a message to a set of listeners, by encapsulating a listener
    pattern.
    """
    def __init__(self, sender):
        """
        Instantiate the Signal. The passed sender is the entity
        that will be communicated as the sender to the receiver.

        Args:
            sender: BaseObject
                The object that will be communicated to the listeners
                as the sender of the notification.
        """
        self._sender = sender
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
