from vaitk import core


def test_initialisation():
    v = core.Size(width=4, height=5)
    assert v.height == 5
    assert v.width == 4

