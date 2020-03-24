'''
from vaitk import gui


def test_palette(screen_app):
    screen, app = screen_app
    assert isinstance(app.palette(), gui.Palette)
'''
