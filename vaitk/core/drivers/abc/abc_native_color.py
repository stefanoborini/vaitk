from abc import ABCMeta, abstractmethod


class ABCNativeColor(metaclass=ABCMeta):
    """
    Represents a native color. Subclasses will
    have additional methods and state to represent the native
    color in the associated driver.
    """
    @property
    @abstractmethod
    def rgb(self):
        """
        Returns the equivalent rgb of the native color as a tuple
        of ints.
        """

    @property
    @abstractmethod
    def red(self):
        """Returns the red component"""

    @property
    @abstractmethod
    def green(self):
        """Returns the green component"""

    @property
    @abstractmethod
    def blue(self):
        """Returns the blue component"""
