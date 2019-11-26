from vaitk import core


def test_initialisation():
    v = core.Size(width=4, height=5)
    assert v.height == 5
    assert v.width == 4


def test_as_tuple():
    v = core.Size(width=4, height=5)
    assert v.as_tuple() == (4, 5)
