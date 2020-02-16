import pytest
from vaitk import core


class MyClass(core.BaseObject):
    signal1 = core.Signal()
    signal2 = core.Signal()


class MyClass2(core.BaseObject):
    signal1 = core.Signal()


def test_basic_usage():
    c = MyClass()

    def slot(arg1, arg2, sender):
        assert arg1 == "hello"
        assert arg2 == 123
        assert sender == c

    c.signal1.connect(slot)
    c.signal1.emit("hello", 123)


def test_double_registration():
    arg = []
    sender = MyClass()

    def slot(x, *args, **kwargs):
        arg.append(x)

    sender.signal1.connect(slot)
    sender.signal1.connect(slot)

    sender.signal1.emit(1)

    assert len(arg) == 1


def test_no_object_crosstalk():
    c1 = MyClass()
    c2 = MyClass()

    def slot(arg1, arg2, sender):
        assert arg1 == "hello"
        assert arg2 == 123
        assert sender == c1

    c1.signal1.connect(slot)
    c2.signal1.connect(slot)
    c1.signal1.emit("hello", 123)


def test_connect_to_signal():
    c1 = MyClass()
    c2 = MyClass()

    def slot(arg1, arg2, sender):
        assert arg1 == "hello"
        assert arg2 == 123
        assert sender == c2

    c1.signal1.connect(c2.signal1)
    c2.signal1.connect(slot)
    c1.signal1.emit("hello", 123)


def test_disconnect():
    arg = []
    sender = MyClass()

    def slot(x, *args, **kwargs):
        arg.append(x)

    sender.signal1.connect(slot)
    sender.signal1.emit(1)
    sender.signal1.disconnect(slot)
    sender.signal1.emit(1)

    assert len(arg) == 1


def test_disconnect_not_registered():
    arg = []
    sender = MyClass()

    def slot(x, *args, **kwargs):
        arg.append(x)

    sender.signal1.disconnect(slot)

    sender.signal1.emit(1)
    assert len(arg) == 0


def test_sender_argument_ignored():
    c = MyClass()

    def slot(x, sender):
        assert sender == c

    c.signal1.connect(slot)
    c.signal1.emit(3, sender="whatever")


def test_slot_sender_required():
    c = MyClass()

    def slot1(x, sender):
        assert x == 3
        assert sender == c

    def slot2(x):
        assert x == 3

    def slot3(*args, **kwargs):
        assert args[0] == 3
        assert "sender" not in kwargs

    c.signal1.connect(slot1)
    c.signal1.connect(slot2)
    c.signal1.connect(slot3)
    c.signal1.emit(3)
