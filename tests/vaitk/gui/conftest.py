import pytest
from vaitk import gui, test


@pytest.fixture
def screen_app():
    screen = test.TextScreen((40, 40))
    app = None
    try:
        app = gui.Application(["test"], screen=screen)
        yield screen, app
    finally:
        del screen
        if app:
            app.exit()
        del app
