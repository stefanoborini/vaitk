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

    @property
    def rgb(self):
        return self.red, self.green, self.blue

    @staticmethod
    def distance(color1, color2):
        """
        Returns the distance between two colors as calculated by
        the sum of the squared differences between each channel.
        """
        return rgb_distance(color1.rgb, color2.rgb)


def rgb_distance(rgb1, rgb2):
    return math.sqrt(
        (rgb1[0] - rgb2[0])**2 +
        (rgb1[1] - rgb2[1])**2 +
        (rgb1[2] - rgb2[2])**2
    )
