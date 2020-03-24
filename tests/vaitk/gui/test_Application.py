'''
import pytest
from vaitk import gui
from vaitk.core.drivers.text.text_screen_driver import TextScreenDriver


def test_init():
    screen = TextScreenDriver((40, 40))
    assert gui.Application.vApp is None

    app = None
    try:
        app = gui.Application(["test"], screen=screen)
        assert gui.Application.vApp is app
        with pytest.raises(Exception):
            gui.Application(["test"], screen=screen)
    finally:
        if app:
            app.exit()
    assert gui.Application.vApp is None
'''
