import pytest
from traitlets import TraitError

from vaitk import core


def test_initialisation():
    v = core.Point(x=4, y=5)
    assert v.x == 4
    assert v.y == 5


def test_invalid_arguments():
    with pytest.raises(TraitError):
        core.Point(x="foo", y=5)


def test_sum():
    v1 = core.Point(x=4, y=5)
    v2 = core.Point(x=2, y=3)
    vres = v1+v2
    assert vres.x == 6
    assert vres.y == 8


def test_difference():
    v1 = core.Point(x=4, y=5)
    v2 = core.Point(x=2, y=2)
    vres = v1-v2
    assert vres.x, 2
    assert vres.y, 3


def test_as_tuple():
    v1 = core.Point(x=4, y=5)
    assert v1.as_tuple() == (4, 5)
