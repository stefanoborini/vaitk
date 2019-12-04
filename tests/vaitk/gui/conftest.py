import pytest
from vaitk import gui, test, core


@pytest.fixture
def screen_app():
    screen = test.TextScreen((40, 40))
    app = gui.Application([], screen=screen)
    yield screen, app

    del screen
    app.exit()
    core.CoreApplication.vApp = None
    del app
