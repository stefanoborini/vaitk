from vaitk import core
from vaitk.core.BaseObject import (
    depth_first_full_tree,
    depth_first_sub_tree,
    traverse_to_root,
    root,
    depth_first_right_tree
)


def test_instantiation():
    o = core.BaseObject()
    assert o.parent is None
    assert len(o.children) == 0


def test_parent():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    assert p.parent is None
    assert len(p.children) == 2
    assert p.children[0] == c1
    assert p.children[1] == c2
    assert c1.parent == p
    assert c2.parent == p
    assert len(c1.children) == 0
    assert len(c2.children) == 0


def test_tree():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert depth_first_full_tree(p) == [p, c1, c3, c2]
    assert depth_first_full_tree(c2) == [p, c1, c3, c2]
    assert depth_first_sub_tree(c2) == [c2]
    assert depth_first_sub_tree(c1) == [c1, c3]


def test_traverse_to_root():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert traverse_to_root(p) == [p]
    assert traverse_to_root(c3) == [c3, c1, p]


def test_root():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert root(p) == p
    assert root(c1) == p
    assert root(c2) == p
    assert root(c3) == p


def test_right_tree():
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

    assert (depth_first_right_tree(c3_1) == [
           c3_2, c2_3, c1_2, c2_4, c3_3, c2_5, c1_3])
    assert depth_first_right_tree(c3_3), [c2_5, c1_3]
