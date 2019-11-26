import unittest
from vaitk import core


class testVSize(unittest.TestCase):
    def testVSize(self):
        v = core.Size(width=4, height=5)
        self.assertEqual(v.height, 5)
        self.assertEqual(v.width, 4)
        self.assertEqual(tuple(v), (4, 5))

    def testVSizeTuple(self):
        self.assertEqual(core.Size.tuple.width((2, 3)), 2)
        self.assertEqual(core.Size.tuple.height((2, 3)), 3)
