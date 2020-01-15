from traitlets import HasTraits, Int
import math


class Color(HasTraits):
    """
    Describes a color in RGB format
    """
    red = Int(min=0, max=255)
    green = Int(min=0, max=255)
    blue = Int(min=0, max=255)

    def __init__(self, red, green, blue):
        super().__init__(red=red, green=green, blue=blue)

    def hex_string(self):
        """Returns the color as a hexadecimal string"""
        return "{:02X}{:02X}{:02X}".format(self.red, self.green, self.blue)

    @staticmethod
    def distance(color1, color2):
        """
        Returns the distance between two colors as calculated by
        the sum of the squared differences between each channel.
        """
        return math.sqrt(
                (color1.red - color2.red)**2 +
                (color1.green - color2.green)**2 +
                (color1.blue - color2.blue)**2
        )
