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
    def num_nominal_colors(self):
        """
        Returns the nominal number of colors.
        This is the driver nominal number. For example curses
        can nominally render 8 colors in 8 color mode, but it
        can represent up to 16 because you can combine the
        bold attribute with a color to produce another color.
        """

    @property
    @abstractmethod
    def num_representable_colors(self):
        """
        Returns the number of colors that can be represented.
        This always matches the total number of representable colors
        in the native palette.
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
    def get_event(self):
        """Gets an event from a device. This method must be blocking."""

