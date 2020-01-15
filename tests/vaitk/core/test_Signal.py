from vaitk import core


def test_signal():
    arg = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x):
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

    def slot(x):
        arg.append(x)

    signal.connect(slot)
    signal.connect(slot)

    assert len(signal._slots) == 1


def test_disconnect_not_registered():
    arg = []
    sender = core.BaseObject()
    signal = core.Signal(sender)

    def slot(x):
        arg.append(x)
    signal.disconnect(slot)

    signal.emit(1)
    assert len(arg) == 0
