from vaitk import core
from vaitk.core import Size, Point


def test_initialization():
    r = core.Rect(Point(2, 3), Size(4, 5))

    assert r.x == 2
    assert r.y == 3
    assert r.width == 4
    assert r.height == 5
    assert isinstance(r.size, Size)
    assert isinstance(r.top_left, Point)
    assert isinstance(r.top_right, Point)
    assert isinstance(r.bottom_left, Point)
    assert isinstance(r.bottom_right, Point)
    assert r.x == 2
    assert r.y == 3
    assert r.width == 4
    assert r.height == 5
    assert r.size.width == 4
    assert r.size.height == 5
    assert r.top_left.x == 2
    assert r.top_left.y == 3
    assert r.top_right.x == 5
    assert r.top_right.y == 3
    assert r.bottom_left.x == 2
    assert r.bottom_left.y == 7
    assert r.bottom_right.x == 5
    assert r.bottom_right.y == 7
    assert r.left == 2
    assert r.right == 5
    assert r.top == 3
    assert r.bottom == 7


def test_initialization_from_tuple():
    r = core.Rect((1, 2), (3, 4))
    assert r.size.as_tuple() == (3, 4)
    assert r.top_left.as_tuple() == (1, 2)


def test_from_tuple():
    r = core.Rect.from_tuple((1, 2, 3, 4))
    assert r.size.as_tuple() == (3, 4)
    assert r.top_left.as_tuple() == (1, 2)


def test_is_null():
    r = core.Rect.from_x_y_width_height(2, 3, 4, 5)
    assert not r.is_null()

    r = core.Rect.from_x_y_width_height(2, 3, 0, 0)
    assert r.is_null()


def test_intersects():
    assert core.Rect.from_x_y_width_height(0, 0, 18, 1).intersects(
        core.Rect.from_x_y_width_height(4, 0, 142, 40))
    assert not core.Rect.from_x_y_width_height(0, 0, 3, 3).intersects(
        core.Rect.from_x_y_width_height(4, 4, 1, 1))


def test_as_tuple():
    r = core.Rect.from_x_y_width_height(2, 3, 4, 5)
    assert r.as_tuple() == (2, 3, 4, 5)


def test_move_to():
    r = core.Rect.from_x_y_width_height(2, 3, 4, 5)
    r.move_to(Point(4, 5))
    assert r.x == 4
    assert r.y == 5
