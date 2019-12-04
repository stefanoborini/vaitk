from vaitk import gui


def test_color():
    color = gui.Color((255, 25, 127))
    assert color.rgb == (255, 25, 127)
    assert color.hex_string() == "FF197F"
    assert color.r == 255
    assert color.g == 25
    assert color.b == 127
