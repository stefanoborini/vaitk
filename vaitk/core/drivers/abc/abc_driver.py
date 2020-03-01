from abc import abstractmethod, ABCMeta


class ABCDriver(metaclass=ABCMeta):
    """
    ABC for the interface of a generic driver to a input/output device.
    """

    @abstractmethod
    def init(self):
        """Initialises the device"""

    @abstractmethod
    def deinit(self):
        """Deinitialises the device"""

    @property
    @abstractmethod
    def num_colors(self):
        """
        Returns the supported number of colors
        """

    @property
    @abstractmethod
    def cursor_pos(self):
        """Gets the current position of the cursor"""

    @cursor_pos.setter
    @abstractmethod
    def cursor_pos(self, pos):
        """Set the current position of the cursor"""

    @property
    @abstractmethod
    def size(self):
        """Returns the size of the accessible area."""

    @abstractmethod
    def reset(self):
        """Resets the screen"""

    @abstractmethod
    def write(self, pos, string, fg_color=None, bg_color=None):
        """
        Writes a string at a given position and with given foreground
        and background colors
        """

    @abstractmethod
    def get_key_code(self):
        """Gets the keycode from a device. This method must be blocking."""

