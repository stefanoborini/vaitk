from vaitk.core.drivers.curses.curses_native_color import CursesNativeColor


def test_initialisation():
    c = CursesNativeColor(1, (1, 1), (0, 0, 0))
    assert c.rgb == (0, 0, 0)
    assert c.attr == (1, 1)
    assert c.color_idx == 1
