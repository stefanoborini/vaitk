from traitlets import HasTraits, Int


class Color(HasTraits):
    red = Int()
    green = Int()
    blue = Int()

    def __init__(self, red, green, blue):
        super().__init__(red=red, green=green, blue=blue)

    def hex_string(self):
        return "{:02X}{:02X}{:02X}".format(self.red, self.green, self.blue)

    @staticmethod
    def distance(color1, color2):
        return (
                (color1.red - color2.red)**2 +
                (color1.green - color2.green)**2 +
                (color1.blue - color2.blue)**2
        )
