from vaitk import gui
import vaitk


def test_draw_text(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.draw_text((10, 10), "hello")
    assert screen.string_at(10, 10, 5) == "hello"


def test_draw_text_formatted(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.draw_text((10, 11, 11, 3), "hello",
                      align=vaitk.Alignment.AlignLeft)
    assert screen.string_at(10, 11, 11) == "hello      "
    assert screen.string_at(10, 12, 11) == "           "
    assert screen.string_at(10, 13, 11) == "           "

    painter.draw_text((10, 11, 11, 3), "hello",
                      align=vaitk.Alignment.AlignHCenter)
    assert screen.string_at(10, 11, 11) == "   hello   "
    assert screen.string_at(10, 12, 11) == "           "
    assert screen.string_at(10, 13, 11) == "           "

    painter.draw_text((10, 11, 11, 3), "hello",
                      align=vaitk.Alignment.AlignRight)
    assert screen.string_at(10, 11, 11) == "      hello"
    assert screen.string_at(10, 12, 11) == "           "
    assert screen.string_at(10, 13, 11) == "           "
    painter.draw_text((10, 11, 11, 3), "hello",
                      align=vaitk.Alignment.AlignVCenter)
    assert screen.string_at(10, 11, 11) == "           "
    assert screen.string_at(10, 12, 11) == "hello      "
    assert screen.string_at(10, 13, 11) == "           "

    painter.draw_text((10, 11, 11, 3), "hello",
                      align=vaitk.Alignment.AlignBottom)

    assert screen.string_at(10, 11, 11) == "           "
    assert screen.string_at(10, 12, 11) == "           "
    assert screen.string_at(10, 13, 11) == "hello      "


def test_draw_line_horiz(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.draw_line((10, 10), 5, vaitk.Orientation.Horizontal)
    assert screen.string_at(10, 10, 5) == "-----"


def test_draw_line_vert(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.draw_line((10, 10), 5, vaitk.Orientation.Vertical)

    assert screen.string_at(10, 10, 1) == "|"
    assert screen.string_at(10, 11, 1) == "|"
    assert screen.string_at(10, 12, 1) == "|"
    assert screen.string_at(10, 13, 1) == "|"
    assert screen.string_at(10, 14, 1) == "|"


def test_fill_rect(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.fill_rect((10, 10, 5, 5))
    assert screen.string_at(10, 10, 5) == "+---+"
    assert screen.string_at(10, 11, 5) == "|   |"
    assert screen.string_at(10, 12, 5) == "|   |"
    assert screen.string_at(10, 13, 5) == "|   |"
    assert screen.string_at(10, 14, 5) == "+---+"


def test_draw_rect(screen_app):
    screen, app = screen_app
    w = gui.Widget()
    w.resize((40, 40))
    painter = gui.Painter(w)
    painter.draw_rect((10, 10, 5, 5))
    assert screen.string_at(10, 10, 5) == "+---+"
    assert screen.string_at(10, 11, 5) == "|...|"
    assert screen.string_at(10, 12, 5) == "|...|"
    assert screen.string_at(10, 13, 5) == "|...|"
    assert screen.string_at(10, 14, 5) == "+---+"
