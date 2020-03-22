from vaitk.core import Event
from vaitk.core.events.event_type import EventType


def test_event_initialisation():
    ev = Event(EventType.Timer)

    assert ev.event_type == EventType.Timer
    assert not ev.accepted

    ev.accept()

    assert ev.accepted

    ev.ignore()

    assert not ev.accepted
