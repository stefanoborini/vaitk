from vaitk.core import Timer


def test_instantiation(coreapp):
    t = Timer()

    assert t.interval is None
    assert not t.single_shot
    assert not t.is_running()

