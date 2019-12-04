import pytest
from vaitk import gui, test, core


def test_init():
    screen = test.TextScreen((40, 40))
    assert gui.Application.vApp is None

    app = gui.Application([], screen=screen)
    assert gui.Application.vApp is app
    with pytest.raises(Exception):
        gui.Application([], screen=screen)
    app.exit()
    core.CoreApplication.vApp = None
