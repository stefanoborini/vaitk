from vaitk.core.drivers.text.text_native_color import TextNativeColor


def test_initialisation():
    c = TextNativeColor((0, 0, 0))
    assert c.rgb == (0, 0, 0)
