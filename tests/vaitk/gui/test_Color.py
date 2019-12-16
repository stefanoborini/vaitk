import pytest
from vaitk import gui


def test_color():
    color = gui.Color(255, 25, 127)
    assert color.hex_string() == "FF197F"
    assert color.red == 255
    assert color.green == 25
    assert color.blue == 127


def test_distance():
    color = gui.Color(0, 0, 0)
    color2 = gui.Color(0, 255, 255)

    assert gui.Color.distance(color, color) == 0
    pytest.approx(gui.Color.distance(color, color2), 360.62445840513923744443)
