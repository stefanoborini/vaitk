import unittest
from vaitk import gui, test, core


class TestVApplication(unittest.TestCase):
    def testInit(self):
        screen = test.TextScreen((40, 40))
        self.assertTrue(gui.Application.vApp is None)

        app = gui.Application([], screen=screen)
        self.assertTrue(gui.Application.vApp is app)
        self.assertRaises(
            Exception, lambda: gui.Application([], screen=screen))
        app.exit()
        core.CoreApplication.vApp = None
