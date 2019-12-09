import pytest
from vaitk import gui, test, core


@pytest.fixture
def screen_app():
    screen = test.TextScreen((40, 40))
    app = gui.Application(["test"], screen=screen)
    try:
        yield screen, app
    finally:
        del screen
        app.exit()
        del app
