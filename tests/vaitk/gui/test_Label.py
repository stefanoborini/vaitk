import unittest
from vaitk import gui, test, core


class TestVLabel(unittest.TestCase):
    def setUp(self):
        self.screen = test.TextScreen((40, 40))
        self.app = gui.Application([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.BaseCoreApplication.vApp = None
        del self.app

    @unittest.skip
    def testVLabel(self):
        label = gui.Label("hello")
        label.show()
        self.app.process_events()
        self.assertEqual(self.screen.string_at(
            0, int(self.screen.size()[1]/2), 5), "hello")

    @unittest.skip
    def testVLabelChangeString(self):
        label = gui.Label("hello")
        label.show()
        self.app.process_events()
        label.set_text("world")
        self.assertEqual(self.screen.string_at(
            0, int(self.screen.size()[1]/2), 5), "hello")
        self.app.process_events()
        self.assertEqual(self.screen.string_at(
            0, int(self.screen.size()[1]/2), 5), "world")
