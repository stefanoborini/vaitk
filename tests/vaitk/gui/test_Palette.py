import unittest
from vaitk import gui, test, core


class TestVPalette(unittest.TestCase):
    def setUp(self):
        self.screen = test.TextScreen((40, 40))
        self.app = gui.Application([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.CoreApplication.vApp = None
        del self.app

    def testPalette(self):
        self.assertTrue(isinstance(self.app.palette(), gui.Palette))
