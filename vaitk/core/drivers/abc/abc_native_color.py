from abc import ABCMeta, abstractmethod


class ABCNativeColor(metaclass=ABCMeta):
    @abstractmethod
    def rgb(self):
        """Returns the equivalent rgb of the native color"""

    @abstractmethod
    @property
    def red(self):
        """Returns the red component"""

    @abstractmethod
    @property
    def green(self):
        """Returns the green component"""

    @abstractmethod
    @property
    def blue(self):
        """Returns the blue component"""
