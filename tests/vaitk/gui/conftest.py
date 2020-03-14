'''
import pytest

from vaitk import gui
from vaitk.core.drivers.text.text_screen_driver import TextScreenDriver


@pytest.fixture
def screen_app():
    screen = TextScreenDriver((40, 40))
    app = None
    try:
        app = gui.Application(["test"], screen=screen)
        yield screen, app
    finally:
        del screen
        if app:
            app.exit()
        del app
'''
