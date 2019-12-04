from vaitk import core


def test_instantiation():
    o = core.BaseObject()
    assert o.parent() is None
    assert len(o.children()) == 0


def test_parent():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    assert p.parent() is None
    assert len(p.children()) == 2
    assert p.children()[0] == c1
    assert p.children()[1] == c2
    assert c1.parent() == p
    assert c2.parent() == p
    assert len(c1.children()) == 0
    assert len(c2.children()) == 0


def test_tree():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert p.depth_first_full_tree() == [p, c1, c3, c2]
    assert c2.depth_first_full_tree() == [p, c1, c3, c2]
    assert c2.depth_first_sub_tree() == [c2]
    assert c1.depth_first_sub_tree() == [c1, c3]


def test_traverse_to_root():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert p.traverse_to_root() == [p]
    assert c3.traverse_to_root() == [c3, c1, p]


def test_root():
    p = core.BaseObject()
    c1 = core.BaseObject(p)
    c2 = core.BaseObject(p)
    c3 = core.BaseObject(c1)

    assert p.root() == p
    assert c1.root() == p
    assert c2.root() == p
    assert c3.root() == p


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

    assert (c3_1.depth_first_right_tree() == [
           c3_2, c2_3, c1_2, c2_4, c3_3, c2_5, c1_3])
    assert c3_3.depth_first_right_tree(), [c2_5, c1_3]
