from vaitk.core.drivers.abc.abc_native_color import ABCNativeColor


class TextNativeColor(ABCNativeColor):
    """
    Representation of a text native color.
    """
    def __init__(self, rgb):
        self._rgb = rgb

    @property
    def rgb(self):
        return self._rgb

    @property
    def red(self):
        return self._rgb[0]

    @property
    def green(self):
        return self._rgb[1]

    @property
    def blue(self):
        return self._rgb[2]
