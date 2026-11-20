import asyncio
import sys

from vaitk.core import CoreApplication, Timer


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


def test_timer_requires_application(coreapp):
    timer = Timer()
    assert timer.interval is None
    assert not timer.single_shot
    assert not timer.is_running()


def test_single_shot_timer_runs_on_event_loop():
    app = CoreApplication(sys.argv)
    fired = []
    timer = Timer.single_shot_timer(1, lambda: (fired.append(True), app.exit()))
    try:
        assert timer.is_running()
        app.run()
        assert fired == [True]
        assert not timer.is_running()
    finally:
        app.exit()


def test_repeating_timer_can_be_stopped():
    app = CoreApplication(sys.argv)
    fired = []

    def on_timeout():
        fired.append(True)
        timer.stop()
        app.exit()

    timer = Timer(interval=1)
    timer.timeout.connect(on_timeout)
    timer.start()
    try:
        app.run()
        assert fired == [True]
        assert not timer.is_running()
    finally:
        app.exit()
