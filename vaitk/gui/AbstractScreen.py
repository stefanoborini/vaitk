from abc import abstractmethod
from .AbstractRectangularArea import AbstractRectangularArea


class AbstractScreen(AbstractRectangularArea):
    @abstractmethod
    def num_colors(self):
        """
        Returns the supported number of colors
        """

    @abstractmethod
    def cursor_pos(self):
        """Gets the current position of the cursor"""

    @abstractmethod
    def set_cursor_pos(self, pos):
        """Sets the position of the cursor"""

    @abstractmethod
    def reset(self):
        """Resets the screen"""

    @abstractmethod
    def write(self, pos, string, fg_color=None, bg_color=None):
        """
        Writes a string at a given position and with given foreground
        and background colors
        """
