from vaitk.core import Size, Point
from vaitk.core.drivers.text.text_screen_driver import TextScreenDriver
from vaitk.keys import KeyModifier


def test_instantiation():
    driver = TextScreenDriver(Size(40, 30))
    assert driver.size.width == 40
    assert driver.size.height == 30
    assert driver.num_nominal_colors == 1
    assert driver.num_representable_colors == 1
    assert driver.cursor_pos.x == 0
    assert driver.cursor_pos.y == 0


def test_write():
    driver = TextScreenDriver(Size(40, 30))

    driver.write(Point(0, 0), "hello")
    assert driver.string_at(Point(0, 0), 5) == "hello"

    driver.write(Point(2, 0), "hello")
    assert driver.string_at(Point(0, 0), 7) == "hehello"

    assert driver.char_at(Point(1, 0)) == "e"

    driver.erase()
    assert driver.string_at(Point(0, 0), 7) == " "*7


def test_get_event():
    driver = TextScreenDriver(Size(40, 30))

    driver.type_string("Hello")

    ev = driver.get_event()
    assert ev.modifier == KeyModifier.NoModifier
    assert ev.char == "H"
