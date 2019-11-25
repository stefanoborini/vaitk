import unittest
from vaitk import gui


class TestVColor(unittest.TestCase):
    def testVColor(self):
        color = gui.VColor((255, 25, 127))
        self.assertEqual(color.rgb, (255, 25, 127))
        self.assertEqual(color.hex_string(), "FF197F")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 25)
        self.assertEqual(color.b, 127)
