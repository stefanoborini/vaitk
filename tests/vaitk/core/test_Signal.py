import pytest
from vaitk import core


def test_signal():
    arg = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x, *args, **kwargs):
        arg.append(x)
    signal.connect(slot)

    signal.emit(3)

    assert len(arg) == 1
    assert arg[0] == 3

    signal.disconnect(slot)
    signal.emit(3)

    assert len(arg) == 1
    assert arg[0] == 3


def test_double_registration():
    arg = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x, *args, **kwargs):
        arg.append(x)

    signal.connect(slot)
    signal.connect(slot)

    assert len(signal._slots) == 1


def test_disconnect_not_registered():
    arg = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x, *args, **kwargs):
        arg.append(x)
    signal.disconnect(slot)

    signal.emit(1)
    assert len(arg) == 0


def test_sender():
    sender_list = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x, sender, *args, **kwargs):
        sender_list.append(sender)

    signal.connect(slot)
    signal.emit(3)

    assert sender_list[0] == sender


def test_sender_invalid_argument():
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x, *args, **kwargs):
        pass

    with pytest.raises(ValueError):
        signal.emit(3, sender="whatever")
