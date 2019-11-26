import unittest
from vaitk import core


class TestVObject(unittest.TestCase):
    def testInstantiation(self):
        o = core.BaseObject()
        self.assertEqual(o.parent(), None)
        self.assertEqual(len(o.children()), 0)

    def testParent(self):
        p = core.BaseObject()
        c1 = core.BaseObject(p)
        c2 = core.BaseObject(p)
        self.assertEqual(p.parent(), None)
        self.assertEqual(len(p.children()), 2)
        self.assertEqual(p.children()[0], c1)
        self.assertEqual(p.children()[1], c2)
        self.assertEqual(c1.parent(), p)
        self.assertEqual(c2.parent(), p)
        self.assertEqual(len(c1.children()), 0)
        self.assertEqual(len(c2.children()), 0)

    def testTree(self):
        p = core.BaseObject()
        c1 = core.BaseObject(p)
        c2 = core.BaseObject(p)
        c3 = core.BaseObject(c1)

        self.assertEqual(p.depth_first_full_tree(), [p, c1, c3, c2])
        self.assertEqual(c2.depth_first_full_tree(), [p, c1, c3, c2])
        self.assertEqual(c2.depth_first_sub_tree(), [c2])
        self.assertEqual(c1.depth_first_sub_tree(), [c1, c3])

    def testTraverseToRoot(self):
        p = core.BaseObject()
        c1 = core.BaseObject(p)
        c3 = core.BaseObject(c1)

        self.assertEqual(p.traverse_to_root(), [p])
        self.assertEqual(c3.traverse_to_root(), [c3, c1, p])

    def testRoot(self):
        p = core.BaseObject()
        c1 = core.BaseObject(p)
        c2 = core.BaseObject(p)
        c3 = core.BaseObject(c1)

        self.assertEqual(p.root(), p)
        self.assertEqual(c1.root(), p)
        self.assertEqual(c2.root(), p)
        self.assertEqual(c3.root(), p)

    def testRightTree(self):
        p = core.BaseObject()
        c1_1 = core.BaseObject(p)
        c2_2 = core.BaseObject(c1_1)
        c3_1 = core.BaseObject(c2_2)
        c3_2 = core.BaseObject(c2_2)
        c2_3 = core.BaseObject(c1_1)
        c1_2 = core.BaseObject(p)
        c2_4 = core.BaseObject(c1_2)
        c3_3 = core.BaseObject(c2_4)
        c2_5 = core.BaseObject(c1_2)
        c1_3 = core.BaseObject(p)

        self.assertEqual(c3_1.depth_first_right_tree(), [
                         c3_2, c2_3, c1_2, c2_4, c3_3, c2_5, c1_3])
        self.assertEqual(c3_3.depth_first_right_tree(), [c2_5, c1_3])
