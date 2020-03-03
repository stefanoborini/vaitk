from vaitk.core.drivers.abc.abc_native_color import ABCNativeColor


class CursesNativeColor(ABCNativeColor):
    def __init__(self, color_idx, attr, rgb):
        self._color_idx = color_idx
        self._attr = attr
        self._rgb = rgb

    def attr(self):
        return self._attr

    def color_idx(self):
        return self._color_idx

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

