import pytest
from vaitk import gui, test, core



@pytest.mark.skip
def test_label(screen_app):
    screen, app = screen_app
    label = gui.Label("hello")
    label.show()
    app.process_events()
    assert (screen.string_at(0, int(screen.size()[1]/2), 5) == "hello")


@pytest.mark.skip
def test_label_change_string(screen_app):
    screen, app = screen_app
    label = gui.Label("hello")
    label.show()
    app.process_events()
    label.set_text("world")
    assert (screen.string_at(0, int(screen.size()[1]/2), 5) == "hello")
    app.process_events()
    assert (screen.string_at(0, int(screen.size()[1]/2), 5) == "world")
