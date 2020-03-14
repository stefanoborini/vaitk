'''
from vaitk.gui.Application import Application


class Cursor:
    @staticmethod
    def set_pos(pos):
        Application.vApp.screen().set_cursor_pos(pos)

    @staticmethod
    def pos():
        return Application.vApp.screen().cursor_pos()
'''
