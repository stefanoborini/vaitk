import pytest
from vaitk import gui, test


def test_init():
    screen = test.TextScreen((40, 40))
    assert gui.Application.vApp is None

    app = gui.Application(["test"], screen=screen)
    try:
        assert gui.Application.vApp is app
        with pytest.raises(Exception):
            gui.Application(["test"], screen=screen)
    finally:
        app.exit()
