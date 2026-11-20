import asyncio
import sys

from vaitk.core import CoreApplication


def test_basic_initialisation():
    app = CoreApplication(sys.argv)
    try:
        assert app.instance == CoreApplication.vApp
        assert app.application_name == sys.argv[0]
        assert app.application_version == ""
        assert isinstance(app.loop, asyncio.AbstractEventLoop)
    finally:
        app.exit()
    assert CoreApplication.vApp is None


def test_post_event_is_dispatched_by_loop():
    app = CoreApplication(sys.argv)
    received = []

    class Receiver:
        def event(self, event):
            received.append(event)
            app.exit()

    try:
        app.post_event(Receiver(), object())
        app.run()
        assert len(received) == 1
    finally:
        app.exit()


def test_exit_stops_running_loop():
    app = CoreApplication(sys.argv)
    app.loop.call_soon(app.exit)
    app.run()
    assert CoreApplication.vApp is None
