import unittest
from vaitk import gui, test, core


class TestVWidget(unittest.TestCase):
    def setUp(self):
        self.screen = test.TextScreen((40, 40))
        self.app = gui.Application([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.BaseCoreApplication.vApp = None
        del self.app

    def testInit(self):
        w = gui.Widget()
        self.assertTrue(isinstance(w, gui.Widget))
