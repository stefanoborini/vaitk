from vaitk.core import Rect, Size, Point


def test_initialization_from_point_and_size():
    r = Rect(Point(2, 3), Size(4, 5))

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


def test_is_null():
    r = Rect(Point(2, 3), Size(4, 5))
    assert not r.is_null()

    r = Rect(Point(2, 3), Size(0, 0))
    assert r.is_null()


def test_intersects():
    assert Rect(Point(0, 0), Size(18, 1)).intersects(
        Rect(Point(4, 0), Size(142, 40)))
    assert not Rect(Point(0, 0), Size(3, 3)).intersects(
        Rect(Point(4, 4), Size(1, 1)))


def test_move_to():
    r = Rect(Point(2, 3), Size(4, 5))
    r.move_to(Point(4, 5))
    assert r.x == 4
    assert r.y == 5
