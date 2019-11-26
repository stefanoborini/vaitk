import unittest
from vaitk import core


class TestVRect(unittest.TestCase):
    def testVRect(self):
        r = core.Rect((2, 3), (4, 5))
        self.assertIsInstance(r.size, core.Size)
        self.assertIsInstance(r.top_left, core.VPoint)

    def testVRectIsNull(self):
        r = core.Rect((2, 3), (4, 5))
        self.assertFalse(r.is_null())

        r = core.Rect((2, 3), (0, 0))
        self.assertTrue(r.is_null())

    def testVRectIntersects(self):
        self.assertTrue(core.Rect((0, 0), (18, 1)).intersects(
            core.Rect((4, 0), (142, 40))))

    def testVRectDimensionality(self):
        r = core.Rect((2, 3), (4, 5))

        self.assertEqual(r.x, 2)
        self.assertEqual(r.y, 3)
        self.assertEqual(r.width, 4)
        self.assertEqual(r.height, 5)
        self.assertEqual(r.size.width, 4)
        self.assertEqual(r.size.height, 5)
        self.assertEqual(r.top_left.x, 2)
        self.assertEqual(r.top_left.y, 3)
        self.assertEqual(r.top_right.x, 5)
        self.assertEqual(r.top_right.y, 3)
        self.assertEqual(r.bottom_left.x, 2)
        self.assertEqual(r.bottom_left.y, 7)
        self.assertEqual(r.bottom_right.x, 5)
        self.assertEqual(r.bottom_right.y, 7)
        self.assertEqual(r.left, 2)
        self.assertEqual(r.right, 5)
        self.assertEqual(r.top, 3)
        self.assertEqual(r.bottom, 7)

    def testVRectTuple(self):
        self.assertEqual(core.Rect.tuple.x((2, 3, 4, 5)), 2)
        self.assertEqual(core.Rect.tuple.y((2, 3, 4, 5)), 3)
        self.assertEqual(core.Rect.tuple.width((2, 3, 4, 5)), 4)
        self.assertEqual(core.Rect.tuple.height((2, 3, 4, 5)), 5)
