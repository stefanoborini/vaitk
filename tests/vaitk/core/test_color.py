import pytest
from vaitk.core.color import Color, rgb_distance


def test_color():
    color = Color(255, 25, 127)
    assert color.hex_string() == "FF197F"
    assert color.red == 255
    assert color.green == 25
    assert color.blue == 127


def test_distance():
    color = Color(0, 0, 0)
    color2 = Color(0, 255, 255)

    assert Color.distance(color, color) == 0
    assert (
        Color.distance(color, color2) ==
        pytest.approx(360.62445840513923744443))


def test_rgb_distance():
    assert (
        rgb_distance((0, 0, 0), (0, 255, 255)) ==
        pytest.approx(360.62445840513923744443))