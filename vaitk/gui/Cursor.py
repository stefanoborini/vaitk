from .Application import VApplication


class VCursor:
    @staticmethod
    def set_pos(pos):
        VApplication.vApp.screen().set_cursor_pos(pos)

    @staticmethod
    def pos():
        return VApplication.vApp.screen().cursor_pos()
