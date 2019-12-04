import pytest
from vaitk.gui import ScreenArea


@pytest.mark.skip
def test_write(screen_app):
    screen, app = screen_app
    area = ScreenArea(screen, (5, 7, 10, 3))

    area.write((0, 0), "0123456789012345")
    area.write((0, 1), "123456789012345")
    area.write((0, 2), "23456789012345")
    area.write((0, 3), "3456789012345")

    assert screen.string_at(4, 6, 12) == '............'
    assert screen.string_at(4, 7, 12) == '.0123456789.'
    assert screen.string_at(4, 8, 12) == '.1234567890.'
    assert screen.string_at(4, 9, 12) == '.2345678901.'
    assert screen.string_at(4, 10, 12) == '............'


@pytest.mark.skip
def test_clear(screen_app):
    screen, app = screen_app
    area = ScreenArea(screen, (5, 7, 10, 3))

    area.erase()

    assert screen.string_at(4, 6, 12) == '............'
    assert screen.string_at(4, 7, 12) == '.          .'
    assert screen.string_at(4, 8, 12) == '.          .'
    assert screen.string_at(4, 9, 12) == '.          .'
    assert screen.string_at(4, 10, 12) == '............'
